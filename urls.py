from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',

    # MEDIA REDIRECT
    (r'^robots\.txt$', 'django.views.generic.simple.redirect_to', {'url': 'http://media.codecollision.com/robots.txt'}),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': 'http://media.codecollision.com/favicon.ico'}),


    # flash.codecollision.com
    # -----------------------------------------
    (r'^wp/$', 'codecollision.wp.views.index'),
    (r'^gateway/$', 'codecollision.wp.gateway.gw'),
    (r'^crossdomain\.xml$', 'codecollision.wp.views.crossdomain'),


    # json API
    # -----------------------------------------
    (r'^json/getposts/$', 'codecollision.log.views.get_posts_json'),
    (r'^json/getcomments/$', 'codecollision.log.views.get_comments_json'),
    (r'^json/submitcomment/$', 'codecollision.log.views.submit_comment'),

    # codecollision.com
    # -----------------------------------------

    # JSON RESPONSE
    # index
    (r'^json/$', 'codecollision.log.views.get_posts_json'),
    # category
    (r'^(category)/([a-zA-Z0-9-+]*)/json/$', 'codecollision.log.views.get_posts_json'),
    # category with page number
    (r'^(category)/([a-zA-Z0-9-+]*)/([0-9]*)/json/$', 'codecollision.log.views.get_posts_json'),
    # single log entry
    (r'^([a-zA-Z0-9-]*)/json/$', 'codecollision.log.views.get_posts_json'),
    # page entry
    (r'^(page)/([a-zA-Z0-9-]*)/json/$', 'codecollision.log.views.get_posts_json'),

    # TEMPLATE RESPONSE
    # index
    (r'^$', 'codecollision.log.views.get_posts'),
    # category
    (r'^(category)/([a-zA-Z0-9-+]*)/$', 'codecollision.log.views.get_posts'),
    # category with page number
    (r'^(category)/([a-zA-Z0-9-+]*)/([0-9]*)/$', 'codecollision.log.views.get_posts'),
    # single log entry
    (r'^([a-zA-Z0-9-]*)/$', 'codecollision.log.views.get_posts'),
    # page entry
    (r'^(page)/([a-zA-Z0-9-]*)/$', 'codecollision.log.views.get_posts'),






    # codecollision.com/polls - learning app
    (r'^polls/$', 'codecollision.polls.views.index'),
    (r'^polls/(?P<poll_id>\d+)/$', 'codecollision.polls.views.detail'),
    (r'^polls/(?P<poll_id>\d+)/results/$', 'codecollision.polls.views.results'),
    (r'^polls/(?P<poll_id>\d+)/vote/$', 'codecollision.polls.views.vote'),

    # 404 - catchall - breaks APPEND_SLASH
    #(r'^[\w]*', 'codecollision.log.views.index'),
)
