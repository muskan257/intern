
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from account_login.models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)
	email = forms.EmailField(max_length=254, required=True)
	mobile_number=forms.CharField(max_length=10,required=True)

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
			raise  ValidationError("Email already exists")
		return email

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileUpdateForm(forms.Form):
	
	email=forms.EmailField(max_length=100, required=False)
	internship1= forms.CharField(max_length=500, required=False)
	internship2= forms.CharField(max_length=500, required=False)
	internship3= forms.CharField(max_length=500, required=False)
	internship4= forms.CharField(max_length=500, required=False)
	




class ProfilePictureUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('profile_picture', )