from django.db.models.signals import post_save, pre_save
from notifications.signals import notify
from .forms import ZakatPostForm, ZakatPostsCommentForm
from .models import ZakatPosts
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UpVote, DownVote, ZakatPosts, ZakatPostsComment

# This will be called when a new post is created. 
@receiver(post_save, sender=DownVote)
def DownVoteCreated(sender, instance, created, **kwargs):
    recipient = instance.post.creator.user # this is the user who created the post
    user = instance.user # this is the user who upvoted the post

    if recipient != user and instance.downvoted and instance.created:
        notify.send(user, recipient=recipient, verb=f'Downvoted Your post # {instance.post.post_number}')


@receiver(post_save, sender=UpVote)
def UpvoteCreated(sender, instance, created, **kwargs):
    recipient = instance.post.creator.user # this is the user who created the post
    user = instance.user # this is the user who upvoted the post

    if recipient != user and instance.upvoted and instance.created:
        notify.send(user, recipient=recipient, verb=f'Upvoted Your post # {instance.post.post_number}')


