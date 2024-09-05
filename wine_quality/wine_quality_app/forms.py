#wine_quality/forms.py
from django import forms
    
class white_wine_qualityForm(forms.Form):
    volatile_acidity = forms.FloatField(label="acidité volatile")
    chlorides = forms.FloatField(label="chlorides")
    total_sulfur_dioxide = forms.FloatField(label="dioxyde de soufre total")
    density = forms.FloatField(label="densité")
    alcohol = forms.FloatField(label="alcohol")

class red_wine_qualityForm(forms.Form):
    volatile_acidity = forms.FloatField(label="acidité volatile")
    citric_acid = forms.FloatField(label="acide citric")
    total_sulfur_dioxide = forms.FloatField(label="dioxyde de soufre total")
    sulphates = forms.FloatField(label="sulphates")
    alcohol = forms.FloatField(label="alcohol")

    

    
