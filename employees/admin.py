from django.contrib import admin

# Register your models here.
from employees.models import Employee

admin.site.register(Employee)
