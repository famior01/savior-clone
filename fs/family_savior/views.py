from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from notifications.signals import notify
from notifications.models import Notification
from django.urls import reverse_lazy, reverse



def home(request):
  hello = "Hello, World!"
  context = {
    'hello': hello,
  }
  return render(request, 'main/home.html', context)


# https://github.com/django-notifications/django-notifications link 
# not working
# def show_notifications(request):
#   user = request.user
#   read_list = Notifications.objects.filter(unread=False)
#   print(read_list, '***************\n\n')
#   context = {
#     'read_list': read_list,
#   }
#   print('\n\n**********',context, '***************\n\n')
#   return render(request, 'zakat_posts:main-post-view', context)


# for notificaitons 
def notifications_read(request, pk):
  user = request.user
  obj = Notification.objects.get(recipient=user, pk=pk)
  obj.mark_as_read()

  return redirect('zakat_posts:main-post-view')


def notifications_delete(request, pk):
  user = request.user
  obj = Notification.objects.get(recipient=user, pk=pk)
  obj.delete()
  return redirect('zakat_posts:main-post-view')


def DeleteAllNotifications(request):
  user = request.user
  obj = Notification.objects.filter(recipient=user)
  print(obj, '***************\n\n')
  obj.delete()
  return redirect('zakat_posts:main-post-view')


# Read all notification, but remain them to show in the notification list
def ReadAllNotifications(request):
  user = request.user
  obj = Notification.objects.filter(recipient=user)
  print(obj, '******from read all*********\n\n')
  for i in obj:
    i.mark_as_read()
  return redirect('zakat_posts:main-post-view')

# # show all notification which are unread or read
# def show_notifications(request):
#   user = request.user
#   obj = Notification.objects.filter(recipient=user)
#   print(obj, '********from show notifications*******\n\n')
#   list_read_unread = [i for i in obj if i.unread == True]
#   context = {
#     'list_read_unread': list_read_unread,
#     'hello': 'hello',
#   }
#   print('\n\n**********',context, '***************\n\n')
#   return render(request, 'zakat_posts:main-post-view', context)