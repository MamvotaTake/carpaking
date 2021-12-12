from django.db import models


# Create your models here.


class ChoiceManager(models.Manager):
    def a(self):
        return super(ChoiceManager, self).filter(choice_category='a', is_active=True)

    def b(self):
        return super(ChoiceManager, self).filter(choice_category='b', is_active=True)


parking_choice = (
    ('A', 'A'),
    ('B', 'B'),
)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    actual_entry_time = models.TimeField(auto_now_add=False, null=True)
    number_plate = models.CharField(max_length=50)
    choice_category = models.CharField(max_length=100, choices=parking_choice)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
