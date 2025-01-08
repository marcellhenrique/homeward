from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    brokerage_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.brokerage_name}"
