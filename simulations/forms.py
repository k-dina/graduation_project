from django import forms


class SimulationForm(forms.Form):
    field_fertility = forms.IntegerField(min_value=1, max_value=10)
    vitality = forms.IntegerField(min_value=1, max_value=100)
    charisma = forms.IntegerField(min_value=1, max_value=100)

class NameSimulationForm(forms.Form):
    simulation_id = forms.CharField()
    name = forms.CharField()
