from django import forms

from employees.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'actual_entry_time', 'number_plate', 'choice_category']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['actual_entry_time'].widget.attrs['placeholder'] = '00:00'
        self.fields['number_plate'].widget.attrs['placeholder'] = 'Number plate'
        self.fields['choice_category'].widget.attrs['placeholder'] = 'parking space'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input100'
