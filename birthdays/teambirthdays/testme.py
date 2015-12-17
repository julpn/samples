from rest_framework.test import APIRequestFactory
from teambirthdays.views import ViewEmployees
from rest_framework.test import APITestCase
from teambirthdays.models import Member

factory = APIRequestFactory()

class ResultTest(APITestCase):
	def setUp(self):
		print "test"
		self.new_employee = Member(name='Sally',email='test@test.com',\
			birthday = '2014-01-01',favorite_ice_cream = 'potato')
		self.new_employee.save()
	def test_record_add(self):
		view = ViewEmployees.as_view()
		request = factory.get('/birthdays/')
		response = view(request)
		response.render()
		print response
		self.assertEqual(response.content, '[{"name":"Sally","birthday":"2014-01-01","favorite_ice_cream":"potato"}]')
	def test_simple_filter(self):
		view = ViewEmployees.as_view()
                request = factory.get('/birthdays/?name=sally')
                response = view(request)
                response.render()
                print response
                self.assertEqual(response.content, '[{"name":"Sally","birthday":"2014-01-01","favorite_ice_cream":"potato"}]')
	def test_multiple_filters(self):
		view = ViewEmployees.as_view()
                request = factory.get('/birthdays/?name=sally&month=jan')
                response = view(request)
                response.render()
                print response
                self.assertEqual(response.content, '[{"name":"Sally","birthday":"2014-01-01","favorite_ice_cream":"potato"}]')
	def test_no_match(self):
		view = ViewEmployees.as_view()
                request = factory.get('/birthdays/?name=jacobjingleheimer')
                response = view(request)
                response.render()
                print response
                self.assertEqual(response.content, '[]')
