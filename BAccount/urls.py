from django.urls import path
from .views import index, MFALoginView, MFALogoutView, ChangeUserInfoView
from .views import profile, BAccountPasswordChangeView, RegisterUserView, RegisterDoneView
from .views import user_activate, DeleteUserView

app_name = 'BAccount'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/password/change', BAccountPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/login/', MFALoginView.as_view(), name='login'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/logout/', MFALogoutView.as_view(), name='logout'),
    path('', index, name='index'),
]
