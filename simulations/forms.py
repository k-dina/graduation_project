from django import forms


class SimulationForm(forms.Form):
    resource_availability = forms.IntegerField(min_value=1, max_value=10)
    vitality = forms.IntegerField(min_value=1, max_value=100)
    charisma = forms.IntegerField(min_value=1, max_value=100)