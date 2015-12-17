from rest_framework import serializers
from teambirthdays.models import Member

class MemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = Member
		fields = ('name','birthday','favorite_ice_cream')
	
