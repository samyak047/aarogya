from django.urls import path
from . import views

urlpatterns = [

	path('register/', views.Register.as_view()),
	path('referrals/<mailId>', views.ReferralList.as_view()),
	path('status/<pk>', views.StatusList.as_view()),
	path('news/', views.NewsList.as_view()),
	path('top/contributers', views.RefreeList.as_view()),
	path('top/contributers', views.RefreeList.as_view()),
	path('top/nrc', views.TopNrcList.as_view()),	

	path('all/states/', views.StatesList.as_view()),
	path('all/division/', views.DivisionList.as_view()),
	path('all/district/', views.DistrictList.as_view()),
	path('all/nrc/', views.NrcList.as_view()),

	path('spec/division/<state>', views.CustomDivisionList.as_view()),
	path('spec/district/<state>', views.CustomDistrictList.as_view()),
	path('spec/nrc/<district>', views.CustomNrcList.as_view()),	


	path('nrc/referrals/', views.nrcReferrals),
	path('nrc/referrals/<pk>', views.updateStatus),
	path('accounts/register', views.register),
	path('nrc/register/patient', views.registerPatient),
	path('refer/', views.referPatient),
	
	path('', views.index),
	

]