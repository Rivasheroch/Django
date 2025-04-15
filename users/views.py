from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(user, request):
    """Sends a verification email to the user."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"
    subject = 'Activate Your Account'

    message = render_to_string('users/email_confirmation_message.html', {
        'user': user,
        'activate_url': activation_link,
        'current_site': current_site,
    })

    try:
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        email.content_subtype = "html"
        email.send()
    except Exception as e:
        messages.error(request, f"Error sending verification email: {e}")
        print(f"Error sending verification email: {e}")


def home(request):
    """Handles both user registration and login on the same page."""
    signup_form = CustomUserCreationForm()  # Initialize signup form

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = False  # User is inactive until email verification
                user.save()
                send_verification_email(user, request)
                messages.success(request, 'Please confirm your email to complete the registration.')
                return redirect('home')  # Redirect to home or a "check email" page
            else:
                # Display form errors
                for field, errors in signup_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:  # Check if the user is active
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is not active. Please check your email for the activation link.')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'users/home.html', {'signup_form': signup_form})



def activate(request, uidb64, token):
    """Activates the user's account upon email verification."""
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated! You are now logged in.')
        return redirect('dashboard')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')


def logout_view(request):
    """Logs the user out."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """Displays the user's dashboard (requires login)."""
    return render(request, 'myapp/dashboard.html')

