# Create your models here.

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from todo.models import Task

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()\
               .filter(status='published').filter(published_date__lte=timezone.now())

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name=_('author'))
    title = models.CharField(max_length=200, verbose_name=_('title'))
    text = RichTextUploadingField(verbose_name=_('text'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    published_date = models.DateTimeField(blank=True, null=True, verbose_name=_('published date'))
    # published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250,
                            unique_for_date='published_date',
                            verbose_name=_('slug')
                            )
    tags = TaggableManager()
    tasks = models.ManyToManyField( "todo.Task", related_name="tasks", null=True,
                                    blank=True,  verbose_name="Task")

    objects = models.Manager()
    publishedobjects = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name=_('status'),
                              )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) # Convert the title into a slug
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('notes:post_detail',
                       args=[self.published_date.year,
                             self.published_date.month,
                             self.published_date.day,
                             self.slug]
                       )

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title


# class Comment(models.Model): #Not used in this version
#     post    = models.ForeignKey   (Post,
#                                    on_delete=models.CASCADE,
#                                    related_name='comments')
#     name    = models.CharField    (max_length=80)
#     email   = models.EmailField   ()
#     body    = RichTextUploadingField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active  = models.BooleanField (default=True)
#
#     class Meta:
#         ordering = ('created',)
#
#     def __str__(self):
#         return 'Comment by {} on {}'.format(self.name, self.post)
