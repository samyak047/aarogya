from .serializers import ReferralSerializer, StatusSerializer, StateSerializer, DivisionSerializer, DistrictSerializer
from .serializers import UserSerializer, NrcSerializer, RegisterSerializer, NewsSerializer, RefreeSerializer
from rest_framework import generics
from .models import State, Division, District, Nrc, Referral, Status, Refree, UserNrc, News
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StatusUpdate, RegisterForm, RegisterPatientForm, ReferPatientForm
import csv

class StatesList(generics.ListCreateAPIView):
    queryset = State.objects.all().order_by('state')
    serializer_class = StateSerializer

class DivisionList(generics.ListCreateAPIView):
    queryset = Division.objects.all().order_by('division')
    serializer_class = DivisionSerializer

class DistrictList(generics.ListCreateAPIView):
	queryset = District.objects.all().order_by('district')
	serializer_class = DistrictSerializer

class NrcList(generics.ListCreateAPIView):
	queryset = Nrc.objects.all().order_by('nrcName')
	serializer_class = NrcSerializer


class CustomDivisionList(generics.ListCreateAPIView):
	serializer_class = DivisionSerializer
	def get_queryset(self):
		try:
			queryset = Division.objects.filter(state = State.objects.get(state = self.kwargs['state'].replace("_", " "))).order_by('division')
		except:
			queryset = []
		return queryset

class CustomDistrictList(generics.ListCreateAPIView):
	serializer_class = DistrictSerializer
	def get_queryset(self):
		print('ok')
		try:
			divisionList = Division.objects.filter(state = State.objects.get(state = self.kwargs['state'].replace("_"," "))).order_by('state')
			queryset = []
			for division in divisionList:
				queryset += District.objects.filter(division = division)
		except:
			queryset = []
		return queryset

class CustomNrcList(generics.ListCreateAPIView):
	serializer_class = NrcSerializer
	def get_queryset(self):
		try:
			queryset = Nrc.objects.filter(district = District.objects.get(district = self.kwargs['district'])).order_by('nrcName')
		except:
			queryset = []
		return queryset

class NewsList(generics.ListCreateAPIView):
	serializer_class = NewsSerializer
	def get_queryset(self):
		try:
			queryset = News.objects.all().order_by('-createdAt')
		except:
			queryset = ['No news to show',]
		return queryset

class RefreeList(generics.ListCreateAPIView):
	serializer_class = RefreeSerializer
	def get_queryset(self):
		try:
			queryset = Refree.objects.all().order_by('-successCount')
			if(len(queryset) > 5):
				queryset = queryset[:5]
		except:
			queryset = ['No users to show']
		return queryset

class TopNrcList(generics.ListCreateAPIView):
	serializer_class = NrcSerializer
	def get_queryset(self):
		try:
			queryset_unsorted = Nrc.objects.all().exclude(totalSamFound = 0)
			#print('TOTALLLLLL')
			#print(str(queryset[0].successRate()))
			#print(str(queryset))
			queryset = sorted(queryset_unsorted, key=lambda x: -x.successRate())
			if(len(queryset) > 5):
				queryset = queryset[:5]
		except:
			queryset = ['No Nrcs to show']
		return queryset



class Register(generics.ListCreateAPIView):
	serializer_class = RegisterSerializer
	queryset = []






class StatusList(generics.ListCreateAPIView):
    serializer_class = StatusSerializer

    def get_queryset(self):
    	pk = self.kwargs['pk']
    	queryset = []
    	try:
    		ref = Referral.objects.get(pk = pk)
    		queryset = Status.objects.filter(referral = ref).order_by('-createdAt')
    	except:
    		pass
    	return queryset


class ReferralList(generics.ListCreateAPIView):

	serializer_class = ReferralSerializer

	def get_queryset(self):
		print('ok')
		mailId = self.kwargs['mailId']
		try:
			refree = Refree.objects.get(mailId = mailId)
			queryset = Referral.objects.filter(refree = refree).order_by('-createdAt')
		except:
			queryset = []
		return queryset





@login_required
def nrcReferrals(request):
	user = request.user
	nrc = Nrc()
	args = {}

	try:
		userNrc = UserNrc.objects.get(user = user)
		nrc = userNrc.nrc
		if userNrc.isApproved == True:
			referrals = Referral.objects.filter(nrc = nrc).order_by('-createdAt')
		else:
			args['msg'] = 'Your account is not verified by Admin.'
			print('Unauthorised')
			referrals = []
	except:
		args['msg'] = 'Failed'
		referrals = []
	args['referrals'] = referrals
	args['user'] = user
	args['nrc'] = nrc
	print(args)
	return render(request, 'nrcReferrals.html', args)


@login_required
def updateStatus(request, pk):
	user = request.user

	if len(Referral.objects.filter(pk = pk)) == 0:
		return render(request, 'updateStatus.html', {'error': 'No Referral with pk' +  str(pk), 'User':user,})

	ref = Referral.objects.get(pk = pk)
	statusList = Status.objects.filter(referral = ref).order_by('-createdAt')
	if len(statusList) == 0:
		return render(request, 'updateStatus.html', {'error': 'No Status Available', 'User':user})
	
	latestMessage = statusList[0].message
	print(latestMessage)
	if request.method == 'POST' and latestMessage != 'Request Closed':
		try:
			unrc = UserNrc.objects.get(user = user)
			referral = Referral.objects.get(pk = pk)
			

				
			if 'FakeData' in request.POST:
				print('Fake Data')
				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'Marked as Fake', updatedby = user)
					Status.objects.create(referral = referral, message = 'Request Closed', updatedby = user)
					referral.refree.fakeCount += 1
					referral.refree.save()
					if referral.refree.fakeCount >= 3:
						referral.refree.isBlocked = True
						referral.refree.save()
						print('Refree blocked')
					referral.isActive = False
					referral.save()
					unrc.nrc.requested -= 1
					unrc.nrc.save()
		
			elif 'ApproveForCheckup' in request.POST:
				print('Approved')
				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'Approved for checkup', updatedby = user)

			elif 'FoundSAM' in request.POST:
				print('SAM Found')
				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'SAM Found', updatedby = user)
					unrc.nrc.waiting += 1
					unrc.nrc.requested -= 1
					unrc.nrc.totalSamFound += 1
					unrc.nrc.save()

			elif 'NotFoundSAM' in request.POST:
				print('SAM not Found')

				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'SAM not found', updatedby = user)
					Status.objects.create(referral = referral, message = 'Request Closed', updatedby = user)
					referral.isActive = False
					referral.save()
					unrc.nrc.requested -= 1
					unrc.nrc.save()


			elif 'Admit' in request.POST:
				print('Admit Request')
				if unrc.isApproved == True:
					if unrc.nrc.bedAvailable > 0:
						Status.objects.create(referral = referral, message = 'Admitted', updatedby = user)
						unrc.nrc.bedAvailable -= 1
						unrc.nrc.waiting -= 1
						unrc.nrc.save()
					else:
						Status.objects.create(referral = referral, message = 'No bed Available', updatedby = user)

				
			
			elif 'Discharge' in request.POST:

				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'Discharged', updatedby = user)
					print('Discharged')
					unrc.nrc.bedAvailable += 1
					unrc.nrc.save()

			elif 'FollowbackCheckup1' in request.POST:

				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'First Followback Checkup Done', updatedby = user)
			
			elif 'FollowbackCheckup2' in request.POST:

				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'Second Followback Checkup Done', updatedby = user)
			
			elif 'FollowbackCheckup3' in request.POST:

				if unrc.isApproved == True:
					Status.objects.create(referral = referral, message = 'Third Followback Checkup Done', updatedby = user)
					Status.objects.create(referral = referral, message = 'Patient Treated', updatedby = user)
					Status.objects.create(referral = referral, message = 'Request Closed', updatedby = user)
					referral.isActive = False
					referral.save()
					unrc.nrc.totalTreated += 1
					unrc.nrc.save()
					referral.refree.successCount += 1
					referral.refree.save()
			else:
				form = StatusUpdate(request.POST)
				if form.is_valid():
					try:
						message = form.cleaned_data['message']
						referral = Referral.objects.get(pk = pk)
						unrc = UserNrc.objects.get(user = user)
						if unrc.isApproved == True:
							Status.objects.create(referral = referral, message = message, updatedby = user)
					except:
						print('Failed to update')
				print('posted')
		except:
			print('Wrong request')
	
	
	print(pk)
	try:
		ref = Referral.objects.get(pk = pk)
		statusList = Status.objects.filter(referral = ref).order_by('-createdAt')
		latestMessage = statusList[0].message
		print(latestMessage)
		if latestMessage == 'Request Closed':
			return render(request, 'updateStatus.html', {'statusList': statusList, 'User':user,})

		else:
			if latestMessage == 'Started':
				name = ['Mark As Fake', 'Approve For Checkup']
				value = ['FakeData', 'ApproveForCheckup']
			
			elif latestMessage == 'Approved for checkup':
				name = ['SAM Found', 'Not Found Sam']
				value = ['FoundSAM', 'NotFoundSAM']
			elif latestMessage == 'SAM Found' or latestMessage == 'No bed Available':
				name = ['Admit']
				value = ['Admit']
			elif latestMessage == 'Admitted':
				name = ['Discharge']
				value = ['Discharge']
			elif latestMessage == 'Discharged':
				name = ['First Checkup Done']
				value = ['FollowbackCheckup1']
			elif latestMessage == 'First Followback Checkup Done':
				name = ['Second Checkup Done']
				value = ['FollowbackCheckup2']
			elif latestMessage == 'Second Followback Checkup Done':
				name = ['Third Checkup Done']
				value = ['FollowbackCheckup3']
			else:
				name = []
				value = []
			
			

	except:
		statusList = []
		name = []
		value = []

	form = StatusUpdate()
	if len(name) == 2:
		name1 = name[0]
		name2 = name[1]
		val1 = value[0]
		val2 = value[1]
		return render(request, 'updateStatus.html', {'pk': pk, 'statusList': statusList, 'User':user, 'form':form, 'name1': name1, 'name2': name2, 'val1' : val1, 'val2' : val2 })
	elif len(name) == 1:
		name1 = name[0]
		val1 = value[0]
		return render(request, 'updateStatus.html', {'pk': pk, 'statusList': statusList, 'User':user, 'form':form, 'name1': name1, 'val1' : val1 })
	elif latestMessage != 'Request Closed':
		return render(request, 'updateStatus.html', {'pk': pk, 'statusList': statusList, 'User':user, 'form':form})
	else:
		return render(request, 'updateStatus.html', {'pk': pk, 'statusList': statusList, 'User':user})
				


def register(request):
	if(request.method == 'POST'):
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			name = form.cleaned_data['name']
			nrcCode = form.cleaned_data['nrcCode']
			nrc = Nrc.objects.get(nrcCode = nrcCode)
			user = User.objects.create_user(username = username, email = email, password = password)
			UserNrc(user = user, nrc = nrc).save()
			print('Registration Complete')
			return redirect("login/")
		else:
			return render(request, 'register.html', {'form' : form})
	else:	
		form = RegisterForm()
		args = {'form': form}
		return render(request, 'register.html', args)


def index(request):
	return render(request, 'index.html')



@login_required
def registerPatient(request):
	if(request.method == 'POST'):
		form = RegisterPatientForm(request.POST)
		if form.is_valid():
			print(request.user.email)
			childName = form.cleaned_data['childName']
			gender = form.cleaned_data['gender']
			age = form.cleaned_data['age']
			address = form.cleaned_data['address']
			tehsil = form.cleaned_data['tehsil']
			contactNo = form.cleaned_data['contactNo']
			motherName = form.cleaned_data['motherName']
			fatherName = form.cleaned_data['fatherName']
			try:
				ref = Refree.objects.get(mailId = request.user.email)
			except:
				ref = Refree(mailId = request.user.email, name = request.user.username).save()
			nrc = UserNrc.objects.get(user = request.user).nrc
			print('ookk')
			Referral.objects.create(refree = ref, nrc = nrc, childName = childName, motherName = motherName, fatherName = fatherName, gender = gender, age = age, address = address, tehsil = tehsil, contactNo = contactNo )
			print('Registered')
			form = RegisterPatientForm()
			args = {'form' : form, 'msg' : 'Patient Successfully Registered'}
			return render(request, 'registerPatient.html', args)
		else:
			args = {'form' : form}
			return render(request, 'registerPatient.html', args)

	form = RegisterPatientForm()
	args = {'form' : form}
	return render(request, 'registerPatient.html', args)

def referPatient(request):
	args = {}
	if request.method == 'POST':
		form = ReferPatientForm(request.POST)
		if form.is_valid():
			mailId = form.cleaned_data['refreeMailId']
			name = form.cleaned_data['refreeName']
			childName = form.cleaned_data['childName']
			motherName = form.cleaned_data['motherName']
			fatherName = form.cleaned_data['fatherName']
			contactNo = form.cleaned_data['contactNo']
			address = form.cleaned_data['address']
			tehsil = form.cleaned_data['tehsil']
			age = form.cleaned_data['age']
			gender = form.cleaned_data['gender']
			nrcCode = form.cleaned_data['nrcCode']
			try:
				nrc = Nrc.objects.get(nrcCode = nrcCode)
				try:
					refree = Refree.objects.get(mailId = mailId)
				except:
					refree = Refree(mailId = mailId, name = name).save()
				Referral.objects.create(refree = refree, nrc = nrc, childName = childName, motherName = motherName, fatherName = fatherName, gender = gender, age = age, address = address, tehsil = tehsil, contactNo = contactNo )
				msg = 'Referral Sucessfully Generated'
			except:
				msg = 'Referral Failed'
			args['msg'] = msg
		else:
			args['msg'] = 'Form Validation Failed'


	form = ReferPatientForm()
	args['form'] = form
	return render(request, 'referPatient.html', args)


