from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from agents.models import Agent
from integrations.external_api import ExternalAPIService
from unittest.mock import patch

class AgentViewsTest(APITestCase):
    def setUp(self):

        self.agent = Agent.objects.create(
            name="Dana Agent",
            contact_info="dana.agent@example.com",
            brokerage_name="Super Realty",
            location="Austin, TX"
        )

        self.mock_customer_data = {
            "customers": [
                {
                    "id": 1,
                    "name": "Cynthia Hart",
                    "email": "c.hart@sample.com",
                    "phone_number": "111-123-1234",
                    "current_address": "908 Test St. Austin, TX 78749"
                }
            ]
        }

        self.mock_application_data = {
            "applications": [
                {
                    "customer_id": 1,
                    "purchasing_address": "111 Purchase St. Austin, TX 78739",
                    "application_approved": False,
                    "agent_name": "Dana Agent"
                }
            ]
        }

    def test_get_customer_agent_view(self):
        with patch.object(ExternalAPIService, 'fetch_applications', return_value=self.mock_application_data), \
             patch.object(ExternalAPIService, 'fetch_customers', return_value=self.mock_customer_data):
            
            url = reverse('customer-agent', kwargs={'customer_id': 1})
            response = self.client.get(url, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['customer']['id'], 1)
            self.assertEqual(response.data['agent']['name'], "Dana Agent")
            self.assertEqual(response.data['agent']['contact_info'], "dana.agent@example.com")
            self.assertEqual(response.data['agent']['brokerage_name'], "Super Realty")
            self.assertEqual(response.data['agent']['location'], "Austin, TX")

    def test_fail_get_customer_agent_view_not_found(self):
        with patch.object(ExternalAPIService, 'fetch_applications', return_value=self.mock_application_data), \
             patch.object(ExternalAPIService, 'fetch_customers', return_value=self.mock_customer_data):
            
            url = reverse('customer-agent', kwargs={'customer_id': 2})
            response = self.client.get(url, format='json')

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['detail'], "Customer or agent not found.")

    def test_get_agents_by_location_view(self):
        url = reverse('agents-by-location')
        response = self.client.get(f'{url}?location=Austin, TX', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Dana Agent")
        self.assertEqual(response.data[0]['location'], "Austin, TX")

    def test_fail_get_agents_by_location_view_without_queryparams(self):
        url = reverse('agents-by-location')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Location query parameter is required.")

    def test_fail_get_agents_by_location_view_unregistered_location(self):
        url = reverse('agents-by-location')
        response = self.client.get(f'{url}?location=Houston, TX', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "No agents found in the specified location.")
