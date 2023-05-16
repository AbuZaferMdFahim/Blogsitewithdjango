from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from .models import Blog
from user.models import User,Follow
from notification.models import Notification

@receiver(post_save, sender = Blog)
def noticationwhenblogcreated(instance, created, *args, **kwargs):
    if created:
        followers = instance.user.followers.all()

        for data in followers:
            follower = data.followed_by

            if not data.muted:
                Notification.objects.create(
                    content_object = instance,
                    user = follower,
                    text = f"{instance.user.username} posted a new Blog",
                    notification_types = "Blog"
                )

@receiver(post_save, sender = Follow)
def noticationwhenfollow(instance, created, *args, **kwargs):
    if created:
        followed = instance.followed
 
        if not instance.muted:
            Notification.objects.create(
                content_object = instance,
                user = followed,
                text = f"{instance.followed_by.username} started following you",
                notification_types = "Follow"
            )

@receiver(m2m_changed, sender = Blog.likes.through)
def notificationwhenliked(instance, pk_set, action, *args, **kwargs):
    pk = list(pk_set)[0]
    user = User.objects.get(pk = pk)

    if action == "post_add":
        Notification.objects.create(
            content_object = instance,
            user = instance.user,
            text = f"{user.username} likes your blog",
            notification_types = "Like"  
        )
