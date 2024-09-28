from django.db import models

from account.models import Flat



# Water Consumption Model
class WaterConsumption(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    kiloliters = models.DecimalField(max_digits=10, decimal_places=2)  # Consumption in kiloliters
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consumption for Flat {self.flat.flat_number}: {self.kiloliters} KL on {self.recorded_at}"

