from django.db import models
from django.db.models import Count
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag
from .forms import EmailPostForm, PostForm
from .models import Post
from credentials import readcredentials

from haystack.query import SearchQuerySet

def post_list(request, tag_slug=None):
    object_list = Post.publishedobjects.order_by('published_date')
    search_term = ''

    tag = None
    if tag_slug:
        tag         = get_object_or_404 (Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if 'search' in request.GET:
        search_term = request.GET['search']
        object_list = object_list.filter(text__icontains=search_term)

    paginator = Paginator(object_list, 10) # posts per page
    page = request.GET.get('page') # current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = { 'page'       : page,
                'posts'      : posts,
                'tag'        : tag  ,
                'search_term': search_term}
    return render(request,
                  'notes/post_list.html',
                  context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)


    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects .filter(status='published'
                                ).filter(tags__in=post_tags_ids
                                ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')
                                           ).order_by('-same_tags',
                                                      '-published_date')[:5]
    return render(request,
                  'notes/post_detail.html',
                  {'post'         : post,
                   'similar_posts': similar_posts,
                   },
                   )


def post_edit(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post                = form.save(commit=False)
            post.author         = request.user
            # post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            response = redirect('/notes/{0}/{1}/{2}/{3}/'.format(year, month, day, post.slug))
            return response
    else:
        form = PostForm(instance=post)
    return render(request,
                  'notes/post_edit.html',
                  {'form': form, 'viewname': _('Edit note')})


def post_new(request, year=timezone.now().year, month=timezone.now().month, day=timezone.now().day, post=""):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post                = form.save(commit=False)
            post.author         = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            response = redirect('/notes/{0}/{1}/{2}/{3}/'.format(year, month, day, post.slug))
            return response
    else:
        form = PostForm()
    return render(request,
                  'notes/post_edit.html',
                  {'form': form, 'viewname': _('New note')})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status='published')
    sent = False

    if request.method == 'POST': # Form submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaneddata = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = '{} ({}) recommends you reading "{}"'.format(cleaneddata['name'],
                                                                   cleaneddata['email'],
                                                                   post.title,)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,
                                                                    post_url,
                                                                    cleaneddata['name'],
                                                                    # cleaneddata['comments'],
                                                                    )
            send_mail(subject,
                      message,
                      readcredentials()[1],
                      [cleaneddata['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request,
                  'notes/post_share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})



def search_titles(request):
    articles = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text',''))

    return render_to_response('search.html', {'articles' : articles})
