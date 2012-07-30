from django.shortcuts import render_to_response
from codecollision.log.models import Posts, TermRelationships, TermTaxonomy, Comments
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from datetime import datetime
import math
import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, Comment


# sanitize HTML
def sanitizeHtml(value, base_url=None):
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = 'p i strong b u a pre br'.split()
    validAttrs = 'href src width height'.split()
    urlAttrs = 'href src'.split()  # Attributes which should have a URL
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val)  # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val)  # Calculate the absolute url
                tag.attrs.append((attr, val))

    return soup.renderContents().decode('utf8')


# JSON GET COMMENTS
def get_comments_json(request):
    if request.method == 'GET':

        # select posts in category
        commentID = None
        if 'commentID' in request.GET:
            commentID = request.GET.get('commentID')

        if 'postID' in request.GET:
            postID = request.GET.get('postID')

        if commentID != None and commentID > 0:
            comments = Comments.objects.filter(comment_post_id=postID, comment_approved='1', comment_id__gt=commentID).order_by('comment_parent', 'comment_date')
        else:
            comments = Comments.objects.filter(comment_post_id=postID, comment_approved='1').order_by('comment_parent', 'comment_date')

        # create python list
        commentList = []
        for item in comments:

            # construct python dictionary
            data = {'pk': item.comment_id, 'parent_pk': item.comment_parent, 'depth': 0, 'fields': {'comment_author': item.comment_author, 'comment_author_url': item.comment_author_url, 'comment_date': str(item.comment_date), 'comment_content': item.comment_content}}

            # find index of parent comment
            index = next((i for i in xrange(len(commentList)) if commentList[i]['pk'] == data['parent_pk']), None)

            # add data at found index position
            if index is not None:
                # update depth
                data['depth'] = commentList[index]['depth'] + 1
                # find last inserted child comment to parent comment
                childIndex = next((i for i in xrange(len(commentList) - 1, -1, -1) if commentList[i]['parent_pk'] == data['parent_pk']), None)
                #update index if child found
                if childIndex is not None:
                    index = childIndex

                commentList.insert(index + 1, data)

            # append to end of list
            else:
                commentList.append(data)

        # Add to dictionary
        commentDictionary = {'comment_list': commentList}

        #serialize
        serialized = simplejson.dumps(commentDictionary)
        return HttpResponse(serialized, mimetype='application/json')


# JSON SUBMIT COMMENT
def submit_comment(request):
    if request.method == 'GET':

        content = ''
        name = 'Anonymous'
        url = ''
        postID = 0
        parent = 0

        if 'comment' in request.GET:
            content = request.GET.get('comment').strip()

        if content == "" or content == "Comment":
            data = {'status': 'empty_comment'}
            #serialize
            serialized = simplejson.dumps(data)
            return HttpResponse(serialized, mimetype='application/json')

        # get remaining comment data
        if 'name' in request.GET:
            name = request.GET.get('name').strip()
            if name == "Name" or name == "":
                name = "Anonymous"

        if 'url' in request.GET:
            url = request.GET.get('url').strip()
            if url == "URL" or url == "":
                url = ""
            elif (url.find("http://") == -1):
                url = 'http://' + url

        if 'postID' in request.GET:
            postID = request.GET.get('postID')
        if 'parent' in request.GET:
            parent = request.GET.get('parent')

        # sanitize values
        name = sanitizeHtml(name)
        url = sanitizeHtml(url)
        content = sanitizeHtml(content)

        ip = request.META['HTTP_X_FORWARDED_FOR']
        utcdate = datetime.utcnow()
        userAgent = request.META['HTTP_USER_AGENT']

        # GET POST tuple with postID
        post = Posts.objects.get(id=postID)
        # increment comment_count in Post tuple
        post.comment_count += 1
        post.save()

        # CREATE COMMENT
        comment = Comments(comment_post_id=post, comment_author=name, comment_author_url=url, comment_author_ip=ip, comment_date=utcdate, comment_date_gmt=utcdate, comment_content=content, comment_karma=0, comment_approved=1, comment_agent=userAgent, comment_type='', comment_parent=parent)
        comment.save()

        data = {'status': 'success'}

        #serialize
        serialized = simplejson.dumps(data)
        return HttpResponse(serialized, mimetype='application/json')


# JSON POSTS
def get_posts_json(request, select='none', selectName='all', page='1'):

    type = 'post'

    # select posts in category
    if select == 'category' and selectName != 'all':
        # Get Post IDS filtered by category
        postsInCategory = TermRelationships.objects.filter(post__post_type='post', post__post_status='publish', term_taxonomy__term__name=selectName).values('post')
        # Select posts from category filter set
        posts = Posts.objects.filter(id__in=postsInCategory)

    # select page
    elif select == 'page':
        type = 'page'
        posts = Posts.objects.filter(post_status='publish', post_name=selectName)

    # select single post
    elif select != 'none' and select != 'category':
        selectName = select
        posts = Posts.objects.filter(post_status='publish', post_name=selectName)

    # select all posts
    else:
        posts = Posts.objects.filter(post_status='publish', post_type='post')

    # specific page number requested
    entriesPerPage = 3
    pageNumber = int(page)
    maxPages = math.ceil(float(len(posts)) / float(entriesPerPage))

    # PAGE NUMBERS
    nextPage = pageNumber + 1
    previousPage = pageNumber - 1

    entryStart = (pageNumber - 1) * entriesPerPage
    entryEnd = entryStart + entriesPerPage
    posts = posts[entryStart:entryEnd]

    # create python object for serialization
    postDictionary = {'post_list': []}
    dic = {}
    for item in posts:
        # get categories in post
        postCategories = TermRelationships.objects.filter(post__id=item.id)
        categoryList = []
        # create categories string
        for category in postCategories:
            categoryList.append(category.term_taxonomy.term.name)

        # construct python dictionary
        dic = {'fields': {'post_title': item.post_title, 'post_name': item.post_name, 'post_content': item.post_content, 'post_type': item.post_type, 'post_date': str(item.post_date), 'comment_count': item.comment_count, 'post_categories': categoryList}, 'pk': item.id}
        # append to list
        postDictionary['post_list'].append(dic)

    # add properties
    postDictionary['type'] = type
    postDictionary['selectName'] = selectName
    postDictionary['max_pages'] = maxPages
    postDictionary['next_page'] = nextPage
    postDictionary['previous_page'] = previousPage

    #serialize
    serialized = simplejson.dumps(postDictionary)
    return HttpResponse(serialized, mimetype='application/json')


# INDEX
def get_posts(request, select='none', selectName='all', page='1'):

    type = 'post'
    selection = 'all'

    # select posts in category
    if select == 'category' and selectName != 'all':
        # Get Post IDS filtered by category
        postsInCategory = TermRelationships.objects.filter(post__post_type='post', post__post_status='publish', term_taxonomy__term__name=selectName).values('post')
        # Select posts from category filter set
        posts = Posts.objects.filter(id__in=postsInCategory)

    # select page
    elif select == 'page':
        type = 'page'
        posts = Posts.objects.filter(post_status='publish', post_name=selectName)

    # select single post
    elif select != 'none' and select != 'category':
        selection = 'single'
        posts = Posts.objects.filter(post_status='publish', post_name=select)

    # select all posts
    else:
        posts = Posts.objects.filter(post_status='publish', post_type='post')

    # specific page number requested
    entriesPerPage = 3
    pageNumber = int(page)
    maxPages = math.ceil(float(len(posts)) / float(entriesPerPage))

    # PAGE NUMBERS
    nextPage = pageNumber + 1
    previousPage = pageNumber - 1

    entryStart = (pageNumber - 1) * entriesPerPage
    entryEnd = entryStart + entriesPerPage
    posts = posts[entryStart:entryEnd]

    # get all categories list
    categories = TermTaxonomy.objects.select_related().filter(count__gt=0, taxonomy='category').order_by('term__name')

    # create python objects
    postDictionary = {'post_list': []}
    dic = {}
    for item in posts:
        # get categories in post
        postCategories = TermRelationships.objects.filter(post__id=item.id)
        categoryList = []
        # create categories string
        for category in postCategories:
            categoryList.append(category.term_taxonomy.term.name)

        # STRIP POST CONTENT AFTER <!--more-->
        if selection != 'single':
            moreIndex = item.post_content.find('<!--more-->')
            if moreIndex != -1:
                item.post_content = item.post_content[0:moreIndex]
                # ADD CONTINUE LINK
                item.post_content += "<h6><a class='postLink' href='/" + item.post_name + "/'>Continue...</a></h6>"

        # construct python dictionary
        dic = {'fields': {'post_title': item.post_title, 'post_name': item.post_name, 'post_content': item.post_content, 'post_date': item.post_date, 'post_categories': categoryList}, 'pk': item.id}
        # append to list
        postDictionary['post_list'].append(dic)

    # add properties
    postDictionary['type'] = type
    postDictionary['selectName'] = selectName
    postDictionary['max_pages'] = maxPages
    postDictionary['next_page'] = nextPage
    postDictionary['previous_page'] = previousPage
    postDictionary['categories'] = categories

    return render_to_response('log/index.html', postDictionary, context_instance=RequestContext(request))
