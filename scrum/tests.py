from django.test import TestCase


from django.contrib.auth.models import User
# Create your tests here.
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import *


class ScrumTest(TestCase):

	def test_scrum(self):

		self.user = User.objects.create(username='olivier')
		self.user.set_password = 'aqw'
		self.user.save()

		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

		# création de sprint
		response = self.client.post('/api/sprint/', {'name':'Sprint de début','date_start':'2015-09-09','date_end':'2015-09-24'}, format='json' )
		self.assertEqual(response.status_code, 201)

		# Création de task 
		response = self.client.post('/api/task/', {'name': 'Tâche 1'}, format='json')
		self.assertEqual(response.status_code, 201)
		response = self.client.post('/api/task/', {'name': 'Tâche 2'}, format='json')
		self.assertEqual(response.status_code, 201)
		response = self.client.post('/api/task/', {'name': 'Tâche 3'}, format='json')
		self.assertEqual(response.status_code, 201)
		
		self.assertEqual(Task.objects.all().count(), 3)

		# Changement de priorité des taches
		reponse = self.client.post('/task/change_priority/1', {'positions' : '52:15:51:23:44:10:6:45:16:22:20:21:11:12'} )
		self.assertEqual(response.status_code, 201)
		
		# Changement de status 
		reponse = self.client.post('/task/change_status/1', {'status': '2'} )
		self.assertEqual(response.status_code, 201)

		# Vérification du changement de status
		self.assertEqual(Task.objects.get(pk=1).status, 2)

		# modification de task
		response = self.client.put('/api/task/1/', {'name' : 'Tâche modifiée'}, format='json')
		self.assertEqual(response.status_code, 200)	

		#modification de sprint
		reponse = self.client.put('/api/sprint/1/', {'name':'Sprint de debut'}, format='json' )
		self.assertEqual(response.status_code, 200)	

		# supression de task
		response = self.client.delete('/api/task/1/', {}, format='json')
		self.assertEqual(response.status_code, 204)

		# supression de sprint
		response = self.client.delete('/api/sprint/1/', {}, format='json')
		self.assertEqual(response.status_code, 204)