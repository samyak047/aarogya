
from rest_framework import serializers
from .models import State, Division, District, Nrc, Referral, Status, Refree, UserNrc, News
from django.contrib.auth.models import User
from .testmodel import Test

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('message', 'createdAt')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ('state',)

class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.CharField(source = 'state.state')
    class Meta:
        model = Division
        fields = ('division','state')

class DistrictSerializer(serializers.HyperlinkedModelSerializer):
	#division = serializers.CharField(source = 'division.division')
	class Meta:
		model = District
		fields = ('district',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('username','password')


class NewsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = News
		fields = ('news', 'createdAt')

class RefreeSerializer(serializers.HyperlinkedModelSerializer):
 	class Meta:
 		model = Refree
 		fields = ('mailId', 'name', 'totalCount', 'successCount', 'fakeCount')

class NrcSerializer(serializers.HyperlinkedModelSerializer):
    district = serializers.CharField(source = 'district.district')
    division = serializers.CharField(source = 'district.division.division')
    state = serializers.CharField(source = 'district.division.state')
    class Meta:
        model = Nrc
        fields = ('nrcCode','nrcName', 'bedCapacity', 'bedAvailable', 'waiting', 'requested', 'district', 'division', 'state', 'totalTreated', 'totalSamFound', 'successRate')

class ReferralSerializer(serializers.ModelSerializer):
	nrcCode = serializers.CharField(source = 'nrc.nrcCode')
	nrcName = serializers.CharField(source = 'nrc.nrcName')
	#district = serializers.CharField(source = 'nrc.district.district')
	#division = serializers.CharField(source = 'nrc.district.division.division')
	#state = serializers.CharField(source = 'nrc.district.division.state.state')
	refree = serializers.CharField(source = 'refree.mailId')
	
	class Meta:
		model = Referral
		fields = ('refree','pk','childName', 'gender', 'age', 'height', 'weight', 'motherName','fatherName','address','tehsil','contactNo','nrcCode',
		'nrcName','umac', 'isEdema','isThinLimb', 'isSwellingStomach','isBrownHair','isHygiene','isFever','isLossOfApetite')
	


	def create(self, validated_data):
		print(validated_data)
		#nrcCode = validated_data['nrc.nrcCode'
		
		#nrc = Nrc.objects.get(nrcCode = nrcCode)
		mailId = validated_data['refree']['mailId']
		nrcCode = validated_data['nrc']['nrcCode']
		validated_data.pop('refree',None)
		validated_data.pop('nrc',None)
		validated_data.pop('pk', None)
		validated_data.pop('nrcName', None)
		validated_data.pop('district', None)
		validated_data.pop('division', None)
		validated_data.pop('state', None)
		
		#l = [validated_data['isEdema'],validated_data['umac'],validated_data['isRural'],validated_data['isHygiene'],validated_data['age'],1,validated_data['height'],validated_data['weight'],validated_data['isBrownHair'],validated_data['isThinLimb'],validated_data['isSwellingStomach'],validated_data['isFever'],validated_data['isLossOfApetite']]
		#print(l)
		#t = Test()
		#prob = t.test(l)
		#print(prob)
		#print('Probability of SAM: {:.2f}'.format(prob[0][1]*100))
		try:
			refree = Refree.objects.get(mailId = mailId)
		except:
			refree = Refree.objects.create(mailId = mailId)
		
		nrc = Nrc.objects.get(nrcCode = nrcCode)
		
		if refree.isBlocked == True:
			print('User Blocked')
			ref = Referral()
		else:
			ref = Referral.objects.create(refree = refree, nrc = nrc, **validated_data)
			nrc.requested += 1
			nrc.save()
			refree.totalCount += 1
			refree.save()
			Status.objects.create(referral = ref, message = "Started")
			l = [ref.isEdema, ref.umac, ref.isRural, ref.isHygiene, ref.age, 1, ref.height, ref.weight, ref.isBrownHair, ref.isThinLimb, ref,isSwellingStomach, ref.isFever, ref.isLossOfApetite ]
			t = Test()
			prob = t.test(l)
			print()
			print("Referral Saved")
		return ref

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Refree
		fields = ('name', 'mailId')
	def create(self, validated_data):
		print(validated_data)
		try:
			if len(Refree.objects.filter(mailId = validated_data['mailId'])) == 0:
				ref = Refree.objects.create(mailId = validated_data['mailId'], name = validated_data['name'])
				return ref
		except:
			return 'Error Occured'
			


