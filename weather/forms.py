from django.forms import ModelForm,TextInput
from django.forms import widgets
from .models import City
class Cityform(ModelForm):
    class Meta:
        model=City
        fields=['name']
        widgets={'name':TextInput(attrs={'class':'input','placeholder':'City Name'})}