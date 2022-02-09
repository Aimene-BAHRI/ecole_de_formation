from random import choices
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.home.models import Activity, Cours_particulier, Abonement, Facture, Student, Magazin, Matiere, Parent, StudyLevel, Villa

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
	old_password = forms.CharField(  label='ancien mot de passe',
					widget=forms.PasswordInput(attrs={
					'class': 'form-control'}),
					error_messages={
					'required': 'Le mot de passe ne peut pas être vide '})

	new_password1 = forms.CharField(  label='nouvel mot de passe',
					widget=forms.PasswordInput(attrs={
					'class': 'form-control'}),
					error_messages={
					'required': 'Le mot de passe ne peut pas être vide '})
	new_password2 = forms.CharField(  label='Confirmation du mot de passe',
					widget=forms.PasswordInput(attrs={
					'class': 'form-control'}),
					error_messages={
					'required': 'Le mot de passe ne peut pas être vide '})

class ParentForm(forms.ModelForm):
	Plan_CHOICES = (
		("mentuelle", "Mentuelle"),
		("trimestrielle", "Trimestrielle"),
		("6_mois", "6 Mois"),
		("annuelle", "Annuelle"),
	)

	father_name = forms.CharField( label='Le nom du père',widget=forms.TextInput(attrs={'class': 'form-control'}))
	father_profession = forms.CharField(label="profession du père", widget=forms.TextInput(attrs={'class': 'form-control'}))
	father_phone = forms.CharField(label="numéro de téléphone du père", widget=forms.TextInput(attrs={'class': 'form-control'}))
	father_avatar = forms.ImageField(label="Image du père")
	mother_name = forms.CharField(label="nom et prénom de la mère", widget=forms.TextInput(attrs={'class': 'form-control'}))
	mother_profession = forms.CharField(label="profession de la mère", widget=forms.TextInput(attrs={'class': 'form-control'}))
	mother_phone = forms.CharField(label="numéro de téléphone de la mère", widget=forms.TextInput(attrs={'class': 'form-control'}))
	authorized_people = forms.TextInput(attrs={"label":"personnes autorisées à recuperer l'eleve",'class': 'form-control'})
	subscribed_plan = forms.ChoiceField(
		choices= Plan_CHOICES,
		label="le plan d'abonement",
		widget=forms.Select(attrs={
		'class': 'form-control form-select'}))
	class Meta:
		model = Parent
		fields = (
			"father_name",
			"father_profession",
			"father_phone",
			"father_avatar",
			"mother_name",
			"mother_profession",
			"mother_phone",
			"authorized_people",
			"subscribed_plan")

class StudyLevelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StudyLevelForm, self).__init__(*args, **kwargs)
		# you can iterate all fields here
		for fname, f in self.fields.items():
			f.widget.attrs['class'] = 'form-control form-select'
	class Meta:
		model = StudyLevel
		fields = '__all__'

class StudentForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StudentForm, self).__init__(*args, **kwargs)
		self.fields['student_firstname'].widget.attrs['class'] = 'form-control'
		self.fields['student_name'].widget.attrs['class'] = 'form-control'
		self.fields['place_of_birth'].widget.attrs['class'] = 'form-control'
		self.fields['address'].widget.attrs['class'] = 'form-control'
		self.fields['allergic'].widget.attrs['class'] = 'form-control'
		self.fields['chronical_sickness'].widget.attrs['class'] = 'form-control'
		self.fields['particular_handicap'].widget.attrs['class'] = 'form-control'
		self.fields['student_gender'].widget.attrs['class'] = 'form-control form-select'
		self.fields['student_avatar'].widget.attrs['class'] = 'form-control form-file-input'
		self.fields['scolar_year'].widget.attrs['class'] = 'form-control'
		self.fields['last_school_attended'].widget.attrs['class'] = 'form-control'

	parent = forms.ModelChoiceField(
		widget=forms.Select(attrs={
			'class' : "form-control form-select",
		}), queryset=Parent.objects.all()
	)
	date_of_birth = forms.DateField(
		label="La date de naissance de l'eleve",
		input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
		widget=forms.DateInput(attrs={
			'class': 'form-control',
			'id' : 'birthday',
			'type': 'text',
			'placeholder':"",
			'data-datepicker':""})
	)
	scolar_inscription_date = forms.DateField(
		label="La date d'inscription scolaire",
		input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
		widget=forms.DateInput(attrs={
			'class': 'form-control',
			'id' : 'birthday',
			'type': 'text',
			'placeholder':"",
			'data-datepicker':""})
	)

	pedagogic_inscription_date = forms.DateField(
		label="La date d'inscription pédagogique",
		input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
		widget=forms.DateInput(attrs={
			'class': 'form-control',
			'id' : 'birthday',
			'type': 'text',
			'placeholder':"",
			'data-datepicker':""})
	)

	activities = forms.ModelMultipleChoiceField(
		label="Les activités de l'éleve",
		widget=forms.CheckboxSelectMultiple(attrs={
			'class' : "form-check-input",
			'type' : "checkbox",
		}), queryset=Activity.objects.all()
	)
	class Meta:
		model = Student
		fields = (
			'parent',
			'student_firstname', 'student_name',
			'date_of_birth', 'place_of_birth',
			'address', 'allergic', 'chronical_sickness',
			'particular_handicap', 'student_gender', 'student_avatar',
			'scolar_inscription_date', 'pedagogic_inscription_date',
			'scolar_year', 'last_school_attended','activities',)

class MagazinForm(forms.ModelForm):
	nom_magazin = forms.CharField(
		label='Le nom du magazin',
		widget=forms.TextInput(attrs={'class': 'form-control'}))

	caisse = forms.CharField(
		label='La caisse initiale',
		widget=forms.TextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Magazin
		fields = ('nom_magazin', 'caisse')

class VillaForm(forms.ModelForm):
	nom_villa = forms.CharField(
		label='Le nom du villa',
		widget=forms.TextInput(attrs={'class': 'form-control'}))

	magazin = forms.ModelChoiceField(
		queryset=Magazin.objects.all(),
		label='Le nom du magazin',
		widget=forms.Select(attrs={
		'class': 'form-control form-select'}))

	class Meta:
		model = Villa
		fields = '__all__'



class FactureForm(forms.ModelForm):
	magazin = forms.ModelChoiceField(queryset=Magazin.objects.all(),
					  label='Le nom du magazin',
					widget=forms.Select(attrs={
					'class': 'form-control form-select'}))

	operateur = forms.ModelChoiceField(queryset=User.objects.all(),
					  label="L'operateur",
					widget=forms.Select(attrs={
					'class': 'form-control form-select'}))

	somme_operation = forms.DecimalField(
						  label="Le frais d'operation",
						widget=forms.NumberInput(attrs={
						'class': 'form-control'}))

	reste_a_paier = forms.DecimalField(
						label="Le reste à Paier",
						widget=forms.NumberInput(attrs={
						'class': 'form-control'}))

	description = forms.CharField(  label="Description",
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))

	date_de_creation = forms.DateField(
					  label="La date de creation du facture",
					input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
					widget=forms.DateInput(attrs={
						'class': 'form-control',
						'id' : 'birthday',
						'type': 'text',
						'placeholder':"",
						'data-datepicker':""}))

	status = forms.ChoiceField(
					choices=[("validée et payée", "Validée Et Payée"), ("pas encore", "Pas Encore")],
					  label="L'etat de facture",
					widget=forms.Select(attrs={
					'class': 'form-control form-select'}))
	class Meta:
		model = Facture
		fields = '__all__'


class AbonementForm(forms.ModelForm):
	magazin = forms.ModelChoiceField(queryset=Magazin.objects.all(),
					  label='Le nom du magazin',
					widget=forms.Select(attrs={
					'class': 'form-control form-select'}))

	operateur = forms.ModelChoiceField(queryset=Parent.objects.all(),
					  label="L'operateur",
					widget=forms.Select(attrs={
					'class': 'form-control form-select'}))

	somme_operation = forms.DecimalField(
						label="Le frais d'operation",
						widget=forms.NumberInput(attrs={
						'class': 'form-control'}))

	reste_a_paier = forms.DecimalField(
						label="Le reste à Paier",
						widget=forms.NumberInput(attrs={
						'class': 'form-control'}))

	description = forms.CharField(  label="Description",
					widget=forms.TextInput(attrs={
					'class': 'form-control'}))

	date_de_creation = forms.DateField(
					  label="La date de creation du facture",
					input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
					widget=forms.DateInput(attrs={
						'class': 'form-control',
						'id' : 'birthday',
						'type': 'text',
						'placeholder':"",
						'data-datepicker':""}))

	# status = forms.ChoiceField(
	# 				choices=[("validée et payée", "Validée Et Payée"), ("pas encore", "Pas Encore")],
	# 				  label="L'etat de facture",
	# 				widget=forms.Select(attrs={
	# 				'class': 'form-control'}))
	class Meta:
		model = Abonement
		fields = ('magazin', 'operateur', 'somme_operation', 'reste_a_paier', 'date_de_creation')
class MatiereForm(forms.ModelForm):
	nom_matiere = forms.CharField(
		label = "le nom de la matiere",
		widget=forms.TextInput(attrs={'class' : "form-control"}))

	class Meta:
		model = Matiere
		fields = '__all__'

from django.conf import settings
class Cours_particulierForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Cours_particulierForm, self).__init__(*args, **kwargs)
		self.fields['cours_type'].widget.attrs['class'] = 'form-control form-select'

	nom_etudiant = forms.CharField(label = "le nom de l'eleve",
		widget=forms.TextInput(attrs={'class' : "form-control"}))

	prenom_etudiant = forms.CharField(label = "le prenom de l'eleve",
		widget=forms.TextInput(attrs={'class' : "form-control"}))

	matiere = forms.ModelChoiceField(
		queryset=Matiere.objects.all(),
		label = "le nom de la matiere",
		widget=forms.Select(attrs={'class': 'form-control form-select'}))

	prix_matiere = forms.DecimalField(
		label = "le prix de la matiere",
		widget=forms.NumberInput(attrs={'class': 'form-control'}))

	date_de_creation = forms.DateField(
					  label="La date de creation du facture",
					input_formats=settings.DATE_INPUT_FORMATS,
					widget=forms.DateInput(attrs={
						'class': 'form-control',
						'type': 'text',
						'placeholder':"",
						'data-datepicker':""}))

	class Meta:
		model = Cours_particulier
		fields = ('nom_etudiant', 'prenom_etudiant', 'matiere', 'prix_matiere', 'cours_type', 'date_de_creation')

class ActivityForm(forms.ModelForm):
	activity_name = forms.CharField(
		label = "le nom de l'activité",
		widget=forms.TextInput(attrs={'class' : "form-control"}))

	activity_price = forms.DecimalField(
		label= "le prix de l'activité",
		widget=forms.NumberInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Activity
		fields = '__all__'

class ActivityForm(forms.ModelForm):
	activity_name = forms.CharField(
		label = "le nom de l'activité",
		widget=forms.TextInput(attrs={'class' : "form-control"}))

	activity_price = forms.DecimalField(
		label= "le prix de l'activité",
		widget=forms.NumberInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Activity
		fields = '__all__'