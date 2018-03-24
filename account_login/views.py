from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from account_login.forms import SignUpForm, ProfileUpdateForm, ProfilePictureUpdateForm
from django.contrib import messages
from account_login.models import Profile

User = get_user_model()

class Register(View):
	template_name = "register.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			return redirect('/account_login/login/')
		else:
			errors = form.errors.get_json_data()
			for every_error in errors:
				for error in errors[every_error]:
					messages.add_message(request, messages.ERROR, error["message"])
			return redirect('/account_login/register/')


class Login(View):
	template_name = "login.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
	
	def post(self, request, *args, **kwargs):
		username = request.POST.get("username")
		password = request.POST.get("password")
		try:
			user = User.objects.get(username=username)
			auth_user = authenticate(username = user.username, password = password)
			if auth_user is not None:
				login(request, user)
				return redirect("/account_login/profile/{}".format(user.username))
			else:
				messages.add_message(request, messages.ERROR, 'Incorrect Credentials')
				return redirect("/account_login/login/")	
		except Exception as e:
			messages.add_message(request, messages.ERROR, 'Incorrect Credentials')
			return redirect("/account_login/login/")

class Logout(View):
	
	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect("/account_login/login/")

class Profile(View):
	template_name = "profile.html"

	def get(self, request, username, *args, **kwargs):
		try:
			user = User.objects.get(username=username)
			if user and user!=request.user:
				following_flag = request.user.profile.check_connection(user)
			else:
				following_flag = None
		except Exception as e:
			print(e)
			user = None
		return render(request, self.template_name, {"user" : user, "following_flag" : following_flag})


class ProfileUpdate(View):
	
	def post(self, request, *args, **kwargs):
		form = ProfileUpdateForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['email'] is not '':
				request.user.profile.email=form.cleaned_data['email']
			if form.cleaned_data['internship1'] is not '':
				request.user.profile.internship1=form.cleaned_data['internship1']
			if form.cleaned_data['internship2'] is not '':
				request.user.profile.internship2=form.cleaned_data['internship2']
			if form.cleaned_data['internship3'] is not '':
				request.user.profile.internship3=form.cleaned_data['internship3']
			if form.cleaned_data['internship4'] is not '':
				request.user.profile.internship4=form.cleaned_data['internship4']
			if request.FILES:
				profile_picture_form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=request.user.profile)
				if profile_picture_form.is_valid():
					profile_picture_form.save()
			request.user.save()
		else:
			errors = form.errors.get_json_data()
			for every_error in errors:
				for error in errors[every_error]:
					messages.add_message(request, messages.ERROR, error["message"])
		return redirect("/account_login/profile/{}".format(request.user.username))




def temp_home(request):
	return redirect("/account_login/login/{}".format(request.user.username))
