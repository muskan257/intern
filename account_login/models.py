
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def upload_location(instance, filename):
	u = User.objects.get(id = instance.user_id)
	return "{}/{}".format(str(u.username), filename)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	internship1 = models.TextField(max_length=500, blank=True)
	internship2= models.TextField(max_length=500, blank=True)
	internship3 = models.TextField(max_length=500, blank=True)
	internship4=models.TextField(max_length=500, blank=True)
	profile_picture = models.ImageField(null=True, blank=True, upload_to=upload_location, default='/default.jpg')

	def __str__(self):
		return self.user.username + "'s profile."

	@property
	def get_full_name(self):
		return "{} {}".format(self.user.first_name, self.user.last_name)

	

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()


