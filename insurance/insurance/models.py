from django.db import models


class InsuranceForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')],
        blank=False,
        default='male'
    )
    age = models.IntegerField()
    marital_status = models.CharField(
        max_length=10, 
        choices=[('single', 'Single'), ('married', 'Married')],
        blank=False,
        default='single'
    )
    children = models.IntegerField(blank=False, default=0)
    income = models.IntegerField()
    employment = models.CharField(
        max_length=15, 
        choices=[('unemployed', 'Unemployed'), ('employed', 'Employed')],
        blank=False,
        default='unemployed'
    )
    disability = models.BooleanField(default=False)

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=20)
    engine_power = models.IntegerField(null=True, blank=True)
    body_type = models.CharField(max_length=50)
    engine_volume = models.DecimalField(max_digits=6, decimal_places=2)

    driving_experience = models.IntegerField()
    vehicles_in_family = models.IntegerField()
    accidents = models.IntegerField()

    mileage = models.IntegerField()
    vehicle_accidents = models.IntegerField()
    market_value = models.DecimalField(max_digits=10, decimal_places=2)
    total_owners = models.IntegerField()
    dashcam = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Insurance Form"
