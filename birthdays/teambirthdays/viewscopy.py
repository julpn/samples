from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from teambirthdays.models import Member
from teambirthdays.serializers import MemberSerializer
from rest_framework import generics

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

class ViewEmployees(generics.ListAPIView):
	serializer_class = MemberSerializer
	def get_queryset(self):
		queryset = Member.objects.all()
		flavor = self.request.query_params.get('flavor', None)
		if flavor is not None:
			queryset = queryset.filter(favorite_ice_cream=flavor)
			return queryset
		else:
			return HttpResponse(status=403)

def employee_list(request):
	if request.method == 'GET':
		employees = Member.objects.all()
		serializer = MemberSerializer(employees, many=True)
		return JSONResponse(serializer.data)

def employee_filter(request, name):
	
	try:
		employee = Member.objects.get(name__iexact=name)
	except Member.DoesNotExist:
		return HttpResponse(status=404)
	if request.method == 'GET':
		serializer = MemberSerializer(employee)
		return JSONResponse(serializer.data)
