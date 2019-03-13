from django import forms
import json, requests
from .models import Nrc
from django.contrib.auth.models import User

class StatusUpdate(forms.Form):
	message = forms.CharField(label = 'Message', required = False)


	def clean(self):
		cleaned_data = super().clean()
		print(cleaned_data)



class RegisterForm(forms.Form):
	username = forms.CharField(label = 'Username')
	name = forms.CharField(label = 'Name')

	nrcCode = forms.CharField(label = 'NRC Code')
	email = forms.EmailField(label = 'E-mail')
	password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput())
	
	def clean(self):
		cleaned_data = super().clean()
		p1 = cleaned_data.get("password1")
		p2 = cleaned_data.get("password2")
		nrcCode = cleaned_data.get("nrcCode")
		username = cleaned_data.get("username")
		if len(User.objects.filter(username=username)) > 0:
			raise forms.ValidationError('Username already Exists')
		if len(p1) < 8:
			raise forms.ValidationError('Password should be minimum 8 characters long.')
		if p1 != p2:
			raise forms.ValidationError('Both Password fields should be same.')
		if len(Nrc.objects.filter(nrcCode = nrcCode)) == 0:
			raise forms.ValidationError('No NRC with this NRC Code.')
			

class RegisterPatientForm(forms.Form):
	childName = forms.CharField(label = 'Child Name')
	genderChoices = [('Male', 'Male'), ('Female', 'Female')]
	gender = forms.CharField(label = 'Gender', widget = forms.RadioSelect(choices = genderChoices))
	age = forms.IntegerField(label = 'Age (in months)')
	motherName = forms.CharField(label = "Mother's Name")
	fatherName = forms.CharField(label = "Father's Name")
	contactNo = forms.CharField(label = "Contact number")
	address = forms.CharField(label = "Address")
	tehsil = forms.CharField(label = "Tehsil / Block")
	def clean(self):
		cleaned_data = super().clean()
		contactNo = cleaned_data.get("contactNo")
		age = cleaned_data.get("age")
		if age < 1:
			raise forms.ValidationError('Invalid age')
		if len(contactNo) != 0 or not contactNo.isdigit():
			print('Enter a valid contact number')
			raise forms.ValidationError('Enter a valid contact number')
	
	
	
class ReferPatientForm(forms.Form):
	refreeMailId = forms.EmailField(label = 'Your E-mail Id')
	childName = forms.CharField(label = 'Child Name')
	genderChoices = [('Male', 'Male'), ('Female', 'Female')]
	gender = forms.CharField(label = 'Gender', widget = forms.RadioSelect(choices = genderChoices))
	age = forms.IntegerField(label = 'Age (in months)')
	motherName = forms.CharField(label = "Mother's Name")
	fatherName = forms.CharField(label = "Father's Name")
	contactNo = forms.CharField(label = "Contact number")
	address = forms.CharField(label = "Address")
	tehsil = forms.CharField(label = "Tehsil / Block")
	nrcCode = forms.CharField(label = 'NRC Code')
	
	
