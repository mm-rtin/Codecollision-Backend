from django.db import models

STATUS_CHOICES = (
    ('closed', 'closed'),
    ('open', 'open'),
)

POST_STATUS_CHOICES = (
    ('draft', 'draft'),
    ('inherit', 'inherit'),
    ('private', 'private'),
    ('publish', 'publish'),
)

POST_TYPE_CHOICES = (
    ('attachment', 'attachment'),
    ('page', 'page'),
    ('post', 'post'),
    ('revision', 'revision'),
)

USER_STATUS_CHOICES = (
    (0, "active"),
)


class Links(models.Model):
    link_id = models.BigIntegerField(primary_key=True, db_column='link_id')
    link_url = models.CharField(max_length=765)
    link_name = models.CharField(max_length=765)
    link_image = models.CharField(max_length=765)
    link_target = models.CharField(max_length=75)
    link_description = models.CharField(max_length=765)
    link_visible = models.CharField(max_length=60)
    link_owner = models.BigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=765)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=765)

    class Meta:
        db_table = u'wp_links'
        verbose_name_plural = "Links"

    def __unicode__(self):
        return u"%s %s" % (self.link_name, self.link_url)


class Options(models.Model):
    option_id = models.BigIntegerField(primary_key=True, db_column='option_id')
    blog_id = models.IntegerField()
    option_name = models.CharField(unique=True, max_length=192)
    option_value = models.TextField()
    autoload = models.CharField(max_length=60)

    class Meta:
        db_table = u'wp_options'
        verbose_name_plural = "Options"

    def __unicode__(self):
        return self.option_name


class Users(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID')  # Field name made lowercase.
    user_login = models.CharField(max_length=180)
    user_pass = models.CharField(max_length=192)
    user_nicename = models.CharField(max_length=150)
    user_email = models.CharField(max_length=300)
    user_url = models.CharField(max_length=300)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=180)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=750)

    class Meta:
        db_table = u'wp_users'
        verbose_name_plural = "Users"


class Usermeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, db_column='user_id')
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        db_table = u'wp_usermeta'
        verbose_name_plural = "Usermeta"


class Posts(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID')  # Field name made lowercase.
    post_author = models.BigIntegerField()
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=60, choices=POST_STATUS_CHOICES)
    comment_status = models.CharField(max_length=60, choices=STATUS_CHOICES)
    ping_status = models.CharField(max_length=60, choices=STATUS_CHOICES)
    post_password = models.CharField(max_length=60)
    post_name = models.CharField(max_length=600)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=765)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=60, choices=POST_TYPE_CHOICES)
    post_mime_type = models.CharField(max_length=300)
    comment_count = models.BigIntegerField()

    class Meta:
        db_table = u'wp_posts'
        verbose_name_plural = "Posts"
        ordering = ['-post_date_gmt', ]

    def __unicode__(self):
        output = self.post_title + "(" + self.post_status + ")"
        return output


class Terms(models.Model):
    term_id = models.BigIntegerField(primary_key=True, db_column='term_id')
    name = models.CharField(max_length=600)
    slug = models.CharField(unique=True, max_length=255)
    term_group = models.BigIntegerField()

    class Meta:
        db_table = u'wp_terms'
        ordering = ['name', ]
        verbose_name_plural = "Terms"

    def __unicode__(self):
        output = self.name + '(%d)' % self.term_id
        return output


class TermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key=True, db_column='term_taxonomy_id')
    term = models.ForeignKey(Terms, db_column='term_id')
    taxonomy = models.CharField(max_length=96)
    description = models.TextField()
    parent = models.BigIntegerField()
    count = models.BigIntegerField()

    class Meta:
        db_table = u'wp_term_taxonomy'
        verbose_name_plural = "TermTaxonomies"

    def __unicode__(self):
        output = self.taxonomy + '(%d)' % self.term_taxonomy_id
        return output


class TermRelationships(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='id')  # Field name made lowercase.
    post = models.ForeignKey(Posts, db_column='object_id')
    term_taxonomy = models.ForeignKey(TermTaxonomy, db_column='term_taxonomy_id')
    term_order = models.IntegerField()

    class Meta:
        db_table = u'wp_term_relationships'
        verbose_name_plural = "TermRelationships"

    def __unicode__(self):
        output = 'PostID = %d taxonomyID = %d' % (self.post.id, self.term_taxonomy.term_taxonomy_id)
        return output


class Postmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True, db_column='meta_id')
    post_id = models.ForeignKey(Posts, db_column='post_id')
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        db_table = u'wp_postmeta'
        verbose_name_plural = "Postmeta"

    def __unicode__(self):
        return u"%s: %s" % (self.meta_key, self.meta_value)


class Comments(models.Model):
    comment_id = models.BigIntegerField(primary_key=True, db_column='comment_ID')  # Field name made lowercase.
    comment_post_id = models.ForeignKey(Posts, db_column='comment_post_ID')
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=300, blank=True)
    comment_author_url = models.CharField(max_length=600, blank=True)
    comment_author_ip = models.CharField(max_length=300, db_column='comment_author_IP')  # Field name made lowercase.
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField()
    comment_content = models.TextField()
    comment_karma = models.IntegerField()
    comment_approved = models.CharField(max_length=60)
    comment_agent = models.CharField(max_length=765)
    comment_type = models.CharField(max_length=60, blank=True)
    comment_parent = models.BigIntegerField()
    user_id = models.BigIntegerField(default=0)

    class Meta:
        db_table = u'wp_comments'
        ordering = ['-comment_date_gmt']
        verbose_name_plural = "Comments"

    def __unicode__(self):
        return u"%s by %s" % (self.comment_id, self.comment_author)


class Commentmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    comment_id = models.ForeignKey(Comments, db_column='comment_id')
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        db_table = u'wp_commentmeta'
