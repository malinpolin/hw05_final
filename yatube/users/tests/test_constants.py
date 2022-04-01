from django.urls import reverse

USERNAME = 'TestUser'

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
PASSWORD_CHANGE_URL = reverse('users:password_change')
PASSWORD_CHANGE_DONE_URL = reverse('users:password_change_done')
PASSWORD_RESET_URL = reverse('users:password_reset')
PASSWORD_RESET_DONE_URL = reverse('users:password_reset_done')
PASSWORD_RESET_COMPLETE_URL = reverse('users:password_reset_complete')

LOGIN_TEMPLATE = 'users/login.html'
LOGOUT_TEMPLATE = 'users/logged_out.html'
SIGNUP_TEMPLATE = 'users/signup.html'
PASSWORD_CHANGE_TEMPLATE = 'users/password_change_form.html'
PASSWORD_CHANGE_DONE_TEMPLATE = 'users/password_change_done.html'
PASSWORD_RESET_TEMPLATE = 'users/password_reset_form.html'
PASSWORD_RESET_DONE_TEMPLATE = 'users/password_reset_done.html'
PASSWORD_RESET_COMPLETE_TEMPLATE = 'users/password_reset_complete.html'
PASSWORD_RESET_CONFIRM_TEMPLATE = 'users/password_reset_confirm.html'
