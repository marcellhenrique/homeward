from integrations.external_api import ExternalAPIService
from agents.models import Agent

class AgentService:
    @staticmethod
    def get_agent_details(customer_id):
        applications = ExternalAPIService.fetch_applications()
        customers = ExternalAPIService.fetch_customers()

        application = next((app for app in applications["applications"] if app["customer_id"] == customer_id), None)
        customer = next((cust for cust in customers["customers"] if cust["id"] == customer_id), None)

        if not application or not customer:
            return None

        agent_name = application["agent_name"]
        agent = Agent.objects.filter(name=agent_name).first()

        return {
            "customer": {
                "id": customer["id"],
                "name": customer["name"],
                "email": customer["email"],
                "phone": customer["phone_number"],
                "current_address": customer["current_address"],
            },
            "agent": {
                "name": agent.name if agent else agent_name,
                "contact_info": agent.contact_info if agent else None,
                "brokerage_name": agent.brokerage_name if agent else None,
                "location": agent.location if agent else None,
            },
        }

    @staticmethod
    def get_agents_by_location(location):
        agents = Agent.objects.filter(location__icontains=location)
        return [
            {
                "name": agent.name,
                "contact_info": agent.contact_info,
                "brokerage_name": agent.brokerage_name,
                "location": agent.location,
            }
            for agent in agents
        ]
