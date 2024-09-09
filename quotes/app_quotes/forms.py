from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Author, Quote, Tag
from django.forms import ModelForm, CharField, DateField, TextInput, ModelMultipleChoiceField, SelectMultiple,\
    ModelChoiceField


class AuthorForm(ModelForm):
    fullname = CharField()
    born_date = DateField()
    born_location = CharField()
    description = CharField()

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        

class QuoteForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('-id'), required=False, widget=SelectMultiple())
    quote = CharField()
    owner = ModelChoiceField(queryset=Author.objects.all().order_by('-id'))

    class Meta:
        model = Quote
        fields = ["quote", "owner", 'tags']
        

class TagForm(ModelForm):
    name = CharField()
    class Meta:
        model = Tag
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError("A tag with this name already exists.")
        return name