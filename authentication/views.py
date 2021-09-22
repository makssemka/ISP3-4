from django.shortcuts import redirect, render
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
import logging
from .email_thread import EmailThread
from .models import SetPasswordForm, SendResetEmailForm, SignupForm
from django.http import HttpResponseRedirect
from django.views.generic import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)


class LoginView(View):
    """"""
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'registration/login.html', context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info("Logging was a success")
            return HttpResponseRedirect('/')
        else:
            logger.warning(f"Signup was not valid")
            messages.error(request, "Signup is not valid")

    form = SignupForm()
    context = dict(form=form)
    return render(request, 'authentication/signup.html', context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            logger.info("Password for was changed")
            return HttpResponseRedirect('/')
        else:
            logger.warning("Password change was not vaid")
            messages.error(request, "change password is not valid")

    form = PasswordChangeForm(request.user)
    return render(request, "authentication/change_password.html", dict(form=form))


def reset_password(request):
    context = dict(form=SendResetEmailForm())

    if request.method == "POST":
        form = SendResetEmailForm(request.POST)

        if not form.is_valid():
            logger.warning("Invalid email")
            messages.error(request, "Please, use valid email")
            return render(request, "authentication/reset_password.html", context)

        email = form.cleaned_data['email']

        try:
            validate_email(email)
        except ValidationError:
            logger.warning("Invalid email")
            messages.error(request, "Please, use valid email")
            return render(request, 'authentication/reset_password.html', context)

        current_site = get_current_site(request)

        user = User.objects.filter(email=email)

        if not user.exists():
            messages.error(request, "No users registered with this email")
            logger.warning(f"There was no user for {email}")
            render(request, 'authentication/reset_password.html', context)

        email_content = {
            "user": user[0],
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user[0].pk)),
            "token": PasswordResetTokenGenerator().make_token(user[0]),
        }

        link = reverse(
            'authentication:complete_password_reset',
            kwargs=dict(uidb64=email_content["uid"], token=email_content["token"]),
        )

        email_subject = "Password reset instructions"

        reset_url = f"http://{current_site.domain}{link}"

        email = EmailMessage(
            email_subject,
            f"Hi {user[0].username}, Please open the link below to reset your password \n{reset_url}",
            "noreply@semycolon.com",
            [email],
        )

        EmailThread(email).start()

        logger.info(f"Email was sent to {email}")
        messages.success(request, "We send you an email with reset")

    return render(request, "authentication/reset_password.html", context)


def complete_password_reset(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.info(request, "This link is invalid, request a new link")
            return redirect("index")
    except:
        logger.warning("Attempt of use of old link")
        messages.error(request, "Something went wrong, request another link")
        return redirect("index")

    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if not form.is_valid():
            logger.warning("Password change was invalid")
            messages.error(request, "Passwords do not match")
        else:
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            logger.info("Password reset via email successful")
            messages.success(request, "Password reset successful")
            return redirect('authentication:login')

    form = SetPasswordForm()
    context = dict(uidb64=uidb64, token=token, form=form)

    return render(request, "authentication/set_new_password.html", context)
