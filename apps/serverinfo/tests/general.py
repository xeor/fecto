"""
General tests for the serverinfo apps that doesn't fit in its own file.
"""

from django.test import TestCase
from django.test.client import Client

from apps.serverinfo.models import Server

class SimpleTest(TestCase):
    fixtures = ['testing.json',]

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index(self):
        """
        Make sure that the basics are fine.
        """
        response = self.client.get('/serverinfo/')
        self.assertEqual(response.status_code, 200)

    def test_details(self):
        """
        Check if we can see server details and info in it
        """
        response = self.client.get('/serverinfo/details/1')
        self.assertContains(response, '10.0.0.2', 1) # One of the ip's

    def test_get_serverinfo(self):
        """
        Test that we have the testdb up and working
        """
        serverObj = Server.objects.all()[0]
        self.assertEqual(serverObj.name, 'server-0')
