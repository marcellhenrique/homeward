from django.urls import path
from agents.views import CustomerAgentView, AgentsByLocationView

urlpatterns = [
    path('customers/<int:customer_id>/agent/', CustomerAgentView.as_view(), name='customer-agent'),
    path('agents/', AgentsByLocationView.as_view(), name='agents-by-location'),
]
