from django.db import models
from django.contrib.auth.models import User


class Refree(models.Model):
	mailId = models.CharField(primary_key = True, max_length = 200)
	name = models.CharField(max_length = 200)
	isBlocked = models.BooleanField(default = False)
	fakeCount = models.IntegerField(default = 0)
	successCount = models.IntegerField(default = 0)
	totalCount = models.IntegerField(default = 0)

	def __str__(self):
		return str(self.mailId)

class State(models.Model):
	state = models.CharField(primary_key = True, max_length = 100)
	def __str__(self):
		return str(self.state)	

class Division(models.Model):
	division = models.CharField(primary_key = True, max_length = 100)
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.division)

class District(models.Model):
	district = models.CharField(primary_key = True, max_length = 100)
	division = models.ForeignKey(Division, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.district)


class Nrc(models.Model):
	nrcCode = models.CharField(primary_key = True, max_length = 100)
	nrcName = models.CharField(null = False, max_length = 100)
	bedCapacity = models.IntegerField(default = 0)
	bedAvailable = models.IntegerField(default = 0)
	waiting = models.IntegerField(default = 0)
	requested = models.IntegerField(default = 0)
	totalTreated = models.IntegerField(default = 0)
	totalSamFound = models.IntegerField(default = 0)
	district = models.ForeignKey(District, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.nrcName)
	def successRate(self):
		try:
			return (self.totalTreated / self.totalSamFound)
		except:
			return 0

class UserNrc(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	nrc = models.ForeignKey(Nrc, on_delete = models.CASCADE)
	isApproved = models.BooleanField(default = False)
	def __str__(self):
		return str(self.user.username)

class Referral(models.Model):
	refree = models.ForeignKey(Refree, on_delete = models.CASCADE)
	isActive = models.BooleanField(default = True)
	childName = models.CharField(null = False, max_length = 100)
	gender = models.CharField(max_length = 10)
	age = models.IntegerField(default = 0)
	height = models.FloatField(null = True)
	weight = models.FloatField(null = True)
	motherName = models.CharField(null = False, max_length = 100)
	fatherName = models.CharField(null = False, max_length = 100)
	address = models.CharField(null = False, max_length = 400)
	tehsil = models.CharField(null = False, max_length = 100)
	contactNo = models.CharField(null = False, max_length = 12)
	nrc = models.ForeignKey(Nrc, on_delete = models.CASCADE)
	createdAt = models.DateTimeField(auto_now_add = True)
	
	isEdema = models.IntegerField(default = 0)
	isThinLimb = models.IntegerField(default = 0)
	isSwellingStomach = models.IntegerField(default = 0)
	isBrownHair = models.IntegerField(default = 0)
	isHygiene = models.IntegerField(default = 0)
	isFever = models.IntegerField(default = 0)
	isRural = models.IntegerField(default = 1)
	isLossOfApetite = models.IntegerField(default = 0)

	umac = models.IntegerField(default = 0)


	def __str__(self):
		return str(self.childName)


class Status(models.Model):
	referral = models.ForeignKey(Referral, on_delete = models.CASCADE)
	message = models.CharField(null = False, max_length = 400)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedby = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.message)


class News(models.Model):
	news = models.TextField(null = False)
	createdAt = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return str(self.news)



