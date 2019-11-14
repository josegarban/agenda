from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.http import HttpResponse, request

import os

from .models import Upload
from .forms import UploadForm

# Autocomplete
from dal import autocomplete


@login_required
def user_upload_table(request):
    uploads = Upload.objects.all()
    user = request.user
    context = { 'uploads': uploads,
                'user': user}
    return render(request, 'uploadlist.html', context)

@login_required
def user_upload_upload(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploadinfo = form.save(commit=False)
            user = request.user
            uploadinfo.username = user.username
            uploadinfo = form.save()
        return user_upload_table(request)

    else:
        form = UploadForm()

    return render(request,
                  'user_upload_upload.html',
                  {'form': form})


@login_required
def user_upload_delete(request, id):

    if request.method == 'POST':
        upload = Upload.objects.get(id=id)
        upload.delete()

    uploads = Upload.objects.all()
    context = { 'uploads': uploads }
    return render(request, 'uploadlist.html', context)
