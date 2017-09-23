#Formulario creado a partir del modelo
from django import forms

from newspaper2.news.models import News

class NewsForm(forms.ModelForm):

    # Evitar el uso de caracteres especificos
    def clean_title(self):
        if ';' in self.cleaned_data['title']:
            raise forms.ValidationError("Error: Title no puede contener ;")
        return self.cleaned_data['title']

    class Meta:
        model = News
        fields = '__all__' # Podemos seleccionar los campos que queremos ej: ('title', 'publish_date',)
