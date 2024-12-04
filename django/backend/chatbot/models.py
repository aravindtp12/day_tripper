from django.db import models

class TravelPlan(models.Model):
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip to {self.destination}"
