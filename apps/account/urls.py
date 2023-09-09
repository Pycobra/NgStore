from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserLoginForm, PassResetForm, PassResetConfirmForm

app_name="account_"
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/<slug:id>/', views.users_dashboard, name="users_dashboard_"),
    #path ('', connection.new_user, name = 'new_user'),
    path('check-registration/', views.registration_check, name="registration_check"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('delete/', views.delete_account, name="delete_account"),
    path('delete_confirmation/', auth_views.TemplateView.as_view(
        template_name='account/user/delete_confirmation.html'), name="delete_confirmation"),

    #this here takes u to form where u enter email, then on click of button, to page saying u did it successfully
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/user/password_reset_form.html',
        success_url='password_reset_email_confirm',
        email_template_name='account/user/password_reset_email.html',
        form_class=PassResetForm),
        name="password_reset"),

    path('edit_login/', auth_views.PasswordResetView.as_view(
            template_name='account/user/password_reset_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='account/user/password_reset_email.html',
            form_class=PassResetForm),
            name="edit_login"),

    #d page saying u did it successfully
    path('password_reset/password_reset_email_confirm/', auth_views.TemplateView.as_view(
        template_name='account/user/reset_status.html'), name="password_reset_done"),

    #this appears in ur email, on click this takes u to password_reset_complete
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/user/password_reset_confirm.html',
        success_url='/account/password_reset_complete/',
        form_class=PassResetConfirmForm),
        name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.TemplateView.as_view(
        template_name='account/user/reset_status.html'), name="password_reset_complete"),
    path('register/', views.account_registration, name="register"),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activation,  name="activate_"),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name="logout"),
    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/set_default/", views.set_default, name="set_default"),
    #path("user_orders/", views.user_orders, name="user_orders"),
    path("", views.search_account, name="search_account"),
    path('dashboard_ajax/', views.dashboard_ajax, name="dashboard_ajax"),
    path("likes_and_wishlist/", views.likes_and_wishlist, name="likes_and_wishlist"),
    path("wishlist/wishlist_add_and_remove/<int:id>/", views.wishlist_add_and_remove, name="wishlist_add_and_remove"),
    path("wishlist/remove_from_wishlist/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("likes/remove_from_likes/", views.remove_from_likes, name="remove_from_likes"),
]
