from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Instructor, Profile, Student


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Student)
def assign_student_to_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name="Student")
        profile = instance.profile
        user = profile.user
        user.groups.add(group)


@receiver(post_save, sender=Instructor)
def assign_instructor_to_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name="Instructor")
        profile = instance.profile
        user = profile.user
        user.groups.add(group)
