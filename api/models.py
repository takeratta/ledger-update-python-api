from __future__ import unicode_literals
from django.db import models
from django.utils.html import mark_safe
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator

# Helpers

# Create your models here.

class View(models.Model):
	name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name

class Device(models.Model):
	name = models.CharField(max_length=255)
	identifier = models.CharField(max_length=255, unique=True)
	target_ID = models.CharField(max_length=255, unique=True)
	views = models.ManyToManyField(View)

	def __str__(self):
		return self.name + " (" + self.identifier + ")"

class Category(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __str__(self):
		return self.name

class App(models.Model):
	name = models.CharField(max_length=255, unique=True)
	BOLOS_app_name = models.CharField(max_length=255)
	icon = models.ImageField(upload_to='apps/icons/')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return self.name

class Firmware(models.Model):
	identifier = models.CharField(max_length=255)
	device = models.ForeignKey(Device, on_delete=models.CASCADE)
	views = models.ManyToManyField(View)
	pre_release_version = models.BooleanField(default = False)
	release_date = models.DateTimeField()
	osu_hash = models.CharField(max_length=64, validators=[MinLengthValidator(64),  RegexValidator(
            regex='^[a-fA-F0-9]*$',
            message='Hash must be an hexadecimal value',
            code='invalid_hash'
        ),], default="0000000000000000000000000000000000000000000000000000000000000000")
	osu_perso = models.CharField(max_length=255)
	osu_firmware = models.CharField(max_length=255)
	osu_firmware_key = models.CharField(max_length=255)
	final_perso = models.CharField(max_length=255)
	final_firmware = models.CharField(max_length=255)
	final_firmware_key = models.CharField(max_length=255)
	final_hash = models.CharField(max_length=64, validators=[MinLengthValidator(64),  RegexValidator(
            regex='^[a-fA-F0-9]*$',
            message='Hash must be an hexadecimal value',
            code='invalid_hash'
        ),], default="0000000000000000000000000000000000000000000000000000000000000000")
	def __str__(self):
		return self.device.name + " " + self.identifier

class Version(models.Model):
	identifier = models.CharField(max_length=255)
	app = models.ForeignKey(App, on_delete=models.CASCADE)
	devices = models.ManyToManyField(Device)
	views = models.ManyToManyField(View)
	app_hash = models.CharField(max_length=64, validators=[MinLengthValidator(64),  RegexValidator(
            regex='^[a-fA-F0-9]*$',
            message='Hash must be an hexadecimal value',
            code='invalid_hash'
        ),], default="0000000000000000000000000000000000000000000000000000000000000000")
	bolos_min_firmware = models.ForeignKey(Firmware, related_name="min_version", blank=True, null=True)
	bolos_max_firmware = models.ForeignKey(Firmware, related_name="max_version", blank=True, null=True)
	perso = models.CharField(max_length=255)
	firmware = models.CharField(max_length=255)
	firmware_key = models.CharField(max_length=255)
	pre_release_version = models.BooleanField(default = False)
	release_date = models.DateTimeField()
	def __str__(self):
		return self.identifier
