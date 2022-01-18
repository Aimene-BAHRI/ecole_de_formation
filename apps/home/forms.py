from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.home.models import Facture, Fils, Magazin, Matiere, Parant

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
	nom_parent = forms.CharField(required=True, label='Le nom du parant',
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
	prenom_parent = forms.CharField(required=True, label='Le prenom du parant',
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
	telephone = forms.CharField(required=True, label='Le numero de telephone du parant',
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
	class Meta:
		model = Parant
		fields = ('nom_parent', 'prenom_parent', 'telephone')

class StudentForm(forms.ModelForm):
	GENDER_CHOICES = (
		("homme", "Homme"), 
		("femme", "Femme")
	)
	NIVEAU_CHOICES = (
		("prescolaire", "Prescolaire"),
		("preparatoire", "Preparatoire"), 
		("primaire", "Primaire"),
		("moyenne", "Moyenne"),
		("lycéenne", "Lycéenne")
	)
	parant = forms.ModelChoiceField(queryset=Parant.objects.all(),
					required=True, label='Le nom du parant',
					widget=forms.Select(attrs={
					'class': 'form-control'}))
	prenom_fils = forms.CharField(required=True, label="Le prenom d'etudiant",
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
	gender = forms.ChoiceField(choices=GENDER_CHOICES, 
					required=True, label='Le sexe',
					widget=forms.Select(attrs={
					'class': 'form-control'}))
	date_of_birth = forms.DateField(required=True, label="La date de naisssance",
					input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
					widget=forms.DateInput(attrs={
						'class': 'form-control',
						'id' : 'birthday',
						'type': 'text',
						'placeholder':"date/mois/annee",
						'data-datepicker':""}))

	niveau_etude = forms.ChoiceField(choices=NIVEAU_CHOICES,
					required=True, label="Niveau d'etude",
					widget=forms.Select(attrs={
					'class': 'form-control'}))
	class Meta:
		model = Fils
		fields = ('parant', 'prenom_fils', 'gender', 'date_of_birth', 'niveau_etude')

class MagazinForm(forms.ModelForm):
	nom_magazin = forms.CharField(required=True, label='Le nom du magazin',
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
	caisse = forms.CharField(required=True, label='La caisse',
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
	
	class Meta:
		model = Magazin
		fields = ('nom_magazin', 'caisse')

class FactureForm(forms.ModelForm):
	Operration_ch = (
					("entrée", "entrée"),
					("sortie" , "sortie"))
	magazin = forms.ModelChoiceField(queryset=Magazin.objects.all(),
					required=True, label='Le nom du magazin',
					widget=forms.Select(attrs={
					'class': 'form-control'}))

	operateur = forms.ModelChoiceField(queryset=User.objects.all(),
					required=True, label="L'operateur",
					widget=forms.Select(attrs={
					'class': 'form-control'}))

	type_operation = forms.ChoiceField(choices=Operration_ch,
					required=True, label="Le type d'operation",
					widget=forms.Select(attrs={
					'class': 'form-control'}))

	somme_operation = forms.DecimalField(max_digits=100, decimal_places=2,
						required=True, label="Le frais d'operation",
						widget=forms.NumberInput(attrs={
						'class': 'form-control'}))

	description = forms.CharField(required=True, label="Description",
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))
					
	date_de_creation = forms.DateField(
					required=True, label="La date de creation du facture",
					input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
					widget=forms.DateInput(attrs={
						'class': 'form-control',
						'id' : 'birthday',
						'type': 'text',
						'placeholder':"",
						'data-datepicker':""}))

	status = forms.ChoiceField(
					choices=[("validée et payée", "Validée Et Payée"), ("pas encore", "Pas Encore")],
					required=True, label="L'etat de facture",
					widget=forms.Select(attrs={
					'class': 'form-control'}))
	class Meta:
		model = Facture
		fields = '__all__'


