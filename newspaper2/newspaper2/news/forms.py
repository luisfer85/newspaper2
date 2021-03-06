#Formulario creado a partir del modelo
from django import forms

from newspaper2.news.models import News, Event

from tinymce.widgets import TinyMCE

class NewsForm(forms.ModelForm):

    description = forms.CharField(widget=TinyMCE(), required=False)
    # Evitar el uso de caracteres especificos
    def clean_title(self):
        if ';' in self.cleaned_data['title']:
            raise forms.ValidationError("Error: Title no puede contener ;")
        return self.cleaned_data['title']

    class Meta:
        model = News
        fields = '__all__' # Podemos seleccionar los campos que queremos ej: ('title', 'publish_date',)

class EventForm(forms.ModelForm):

    description = forms.CharField(widget=TinyMCE(), required=False)
    # Evitar el uso de caracteres especificos
    def clean_title(self):
        if ';' in self.cleaned_data['title']:
            raise forms.ValidationError("Error: Title no puede contener ;")
        return self.cleaned_data['title']

    class Meta:
        model = Event
        fields = '__all__' # Podemos seleccionar los campos que queremos ej: ('title', 'publish_date',)
