#Formulario creado a partir del modelo
from django import forms

from newspaper2.news.models import News

class NewsForm(forms.ModelForm):

	class Meta:
		model = News
		fields = '__all__'
