from django.views import generic
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
import re

User = get_user_model()


# UsernameValidationView
@method_decorator(never_cache, name='dispatch')
class UsernameValidationView(generic.View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()

            # Check if username is alphanumeric
            if not isinstance(username, str) or not re.match(r'^[a-zA-Z0-9]+$', username):
                return JsonResponse({'username_error': 'Username should only contain letters and numbers.'}, status=400)

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'username_error': 'Sorry, this username is already taken.'}, status=400)

            return JsonResponse({'username_valid': True}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


# EmailValidationView
@method_decorator(never_cache, name='dispatch')
class EmailValidationView(generic.View):
    def post(self, request):    
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'email_error': 'Email is invalid'}, status=400)
                    
            # Check if email already exists
            if User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'email_error': 'Sorry, this email is already in use. Choose another one.'}, status=400)

            return JsonResponse({'email_valid': True}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


# PasswordValidationView
@method_decorator(never_cache, name='dispatch')
class PasswordValidationView(generic.View):
    def post(self, request):   
        try:
            data = json.loads(request.body)
            password = data.get('password', '').strip()
            password2 = data.get('password2', '').strip()

            if password != password2:
                return JsonResponse({'password_error': 'Passwords do not match!'}, status=400)

            if len(password) < 8:
                return JsonResponse({'password_error': 'Your password must be at least 8 characters long.'}, status=400)

            return JsonResponse({'password_valid': True})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
