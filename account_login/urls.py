
from django.urls import path
from account_login.views import Login, Logout , Register, Profile, ProfileUpdate

urlpatterns = [
	path('register/', Register.as_view(), name="register_url"),
	path('login/', Login.as_view(), name="login_url"),
	path('logout/', Logout.as_view(), name="logout_url"),
	path('profile/<str:username>/update/', ProfileUpdate.as_view(), name="profile_edit_url"),
	path('profile/<str:username>/', Profile.as_view(), name="profile_url"),
	]
	


