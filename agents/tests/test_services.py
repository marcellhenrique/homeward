from unittest.mock import patch
from django.test import TestCase
from agents.models import Agent
from agents.services import AgentService

class AgentServiceTest(TestCase):
    def setUp(self):
        Agent.objects.create(
            name="Dana Agent",
            contact_info="123-456-7890",
            brokerage_name="Best Brokers",
            location="Austin, TX"
        )

    @patch('integrations.external_api.ExternalAPIService.fetch_applications')
    @patch('integrations.external_api.ExternalAPIService.fetch_customers')
    def test_get_agent_details(self, mock_fetch_customers, mock_fetch_applications):
        mock_fetch_applications.return_value = {
            "applications": [
                {
                    "customer_id": 1,
                    "purchasing_address": "111 Purchase St. Austin, TX 78739",
                    "application_approved": False,
                    "agent_name": "Dana Agent"
                }
            ]
        }
        mock_fetch_customers.return_value = {
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

        customer_id = 1
        result = AgentService.get_agent_details(customer_id)

        self.assertIn("customer", result)
        self.assertIn("agent", result)
        self.assertEqual(result["agent"]["name"], "Dana Agent")
        self.assertEqual(result["customer"]["name"], "Cynthia Hart")

    @patch('integrations.external_api.ExternalAPIService.fetch_applications')
    @patch('integrations.external_api.ExternalAPIService.fetch_customers')
    def test_fail_get_agent_details_agent_not_found(self, mock_fetch_customers, mock_fetch_applications):
        mock_fetch_applications.return_value = {
            "applications": [
                {
                    "customer_id": 1,
                    "purchasing_address": "111 Purchase St. Austin, TX 78739",
                    "application_approved": False,
                    "agent_name": "Dana Agent"
                }
            ]
        }
        mock_fetch_customers.return_value = {
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

        customer_id = 99
        result = AgentService.get_agent_details(customer_id)
        self.assertIsNone(result)

    def test_get_agents_by_location(self):
        agents = AgentService.get_agents_by_location("Austin")
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["brokerage_name"], "Best Brokers")

    def test_fail_get_agents_by_unregistered_location(self):
        agents = AgentService.get_agents_by_location("Dallas")
        self.assertEqual(len(agents), 0)
