from django import forms

class CreatePlayer(forms.Form):
    name = forms.CharField(label="Username", max_length=200)
