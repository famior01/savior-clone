# from __future__ import absolute_import, unicode_literals
# from celery import shared_task
# from django.shortcuts import render
# from .models import IWatch
# from profiles.models import Profile
# from django.shortcuts import render, redirect
# from .forms import IWatchModelForm
# from django.views.generic import CreateView
# from django.urls import reverse_lazy


# @shared_task
# def upload_video(form):
#   # only author will be able to update the post
#   profile = Profile.objects.get(user=self.request.user)
#   form.instance.creator = profile
#   if form.instance.creator == profile:
#     return super().form_valid(form)
#   else:
#     form.add_error(None, "You are not authorized to update this post")
#     return super().form_invalid(form)
