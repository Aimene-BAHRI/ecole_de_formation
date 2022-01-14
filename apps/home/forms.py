from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.home.models import Parant

class UserProfileForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Pseudo","class": "form-control"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "mot de passe","class": "form-control"}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Prenom","class": "form-control"}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nom","class": "form-control"}))
	email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email","class": "form-control"}))
	
	class Meta:
		model = User
		fields = '__all__'

from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
	error_css_class = 'has-error'
	error_messages = {'password_incorrect':
				"L'ancien mot de passe n'est pas correct. Essayer à nouveau ."}
	old_password = forms.CharField(required=True, label='ancien mot de passe',
					widget=forms.PasswordInput(attrs={
					'class': 'form-control'}),
					error_messages={
					'required': 'Le mot de passe ne peut pas être vide '})

	new_password1 = forms.CharField(required=True, label='nouvel mot de passe',
					widget=forms.PasswordInput(attrs={
					'class': 'form-control'}),
					error_messages={
					'required': 'Le mot de passe ne peut pas être vide '})
	new_password2 = forms.CharField(required=True, label='Confirmation du mot de passe',
					widget=forms.PasswordInput(attrs={
					'class': 'form-control'}),
					error_messages={
					'required': 'Le mot de passe ne peut pas être vide '})


class ParantForm(forms.ModelForm):
	user = UserCreationForm
	class Meta:
		model = Parant
		fields = '__all__'