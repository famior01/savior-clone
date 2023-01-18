from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from user.models import User 
from .forms import UserChangeForm

# Create your views here.

class UserUpdateView(UpdateView):
  model = User
  form_class = UserChangeForm  # from forms.py
  template_name = 'user/update.html'

  def get_success_url(self, **kwargs):
    return reverse("profiles:profile-detail-view", kwargs={'pk':self.request.user.pk})