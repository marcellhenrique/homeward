from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from agents.services import AgentService

class CustomerAgentView(APIView):
    def get(self, request, *args, **kwargs):
        data = AgentService.get_agent_details(kwargs["customer_id"])
        if not data:
            raise NotFound(detail="Customer or agent not found.")
        return Response(data)

class AgentsByLocationView(APIView):
    def get(self, request, *args, **kwargs):
        location = request.query_params.get("location")
        if not location:
            return Response({"error": "Location query parameter is required."}, status=400)
        data = AgentService.get_agents_by_location(location)
        if not data:
            raise NotFound(detail="No agents found in the specified location.")
        return Response(data)
