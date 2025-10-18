from django.db import models
from django.core.exceptions import ValidationError
import requests


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.breed:
            try:
                response = requests.get('https://api.thecatapi.com/v1/breeds')
                if response.status_code == 200:
                    breeds = response.json()
                    breed_names = [breed['name'].lower() for breed in breeds]
                    if self.breed.lower() not in breed_names:
                        raise ValidationError(f"Breed '{self.breed}' is not valid. Please check TheCatAPI for valid breeds.")
                else:
                    raise ValidationError("Unable to validate breed. Please try again later.")
            except requests.RequestException:
                raise ValidationError("Unable to validate breed. Please check your internet connection.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        ordering = ['name']



