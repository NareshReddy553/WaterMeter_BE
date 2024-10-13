from django.db import models

from account.models import Flat, UserProfile



# Water Consumption Model
class WaterConsumption(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    kiloliters = models.DecimalField(max_digits=10, decimal_places=2)  # Consumption in kiloliters
    recorded_at = models.DateTimeField(auto_now_add=True)
    created_datetime= models.DateTimeField(auto_now_add=True)
    modify_datetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("scan_meter", "Can scan the meter to get Readings"),
        ]

    def __str__(self):
        return f"Consumption for Flat {self.flat.flat_number}: {self.kiloliters} KL on {self.recorded_at}"

