from django.http import HttpResponse
from teambirthdays.models import Member
from teambirthdays.serializers import MemberSerializer
from rest_framework import generics
from datetime import datetime

class ViewEmployees(generics.ListAPIView):
	serializer_class = MemberSerializer
	def get_queryset(self):
		queryset = Member.objects.all()

		flavor = self.request.query_params.get('flavor', None)		
		name = self.request.query_params.get('name',None)
		# Month must be entered as three letter abbrev; eg Nov
		month_abbrev = self.request.query_params.get('month',None)
		
		if flavor is not None:
			queryset = queryset.filter(favorite_ice_cream__iexact=flavor)
		if name is not None:
			queryset = queryset.filter(name__iexact=name)
		if month_abbrev is not None:
			month = datetime.strptime(month_abbrev,'%b')
			month = datetime.strftime(month,'%m')
			queryset = queryset.filter(birthday__month=month)		
                return queryset
		
