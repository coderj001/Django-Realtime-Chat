from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings

from account.forms import RegistrationForm, AccountAuthForm
from account.models import Account


def get_redirect_if_exists(request):
    redirect = None
    if request.method == 'GET':
        next = request.GET.get('next')
        if next:
            redirect = str(next)
    return redirect


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(
            f"You are already authenticated as {user.email}."
        )

    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            else:
                return redirect("core:home_view")
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context=context)


def logout_view(request):
    logout(request)
    return redirect("core:home_view")


# ERROR:  <10-06-21, coderj001> # Form err not showing
def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('core:home_view')

    if request.method == 'POST':
        form = AccountAuthForm(request.POST or None)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                else:
                    return redirect("core:home_view")
        context['login_form'] = form
    else:
        form = AccountAuthForm()
        context['login_form'] = form

    return render(request, 'account/login.html', context=context)


def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get('id')
    try:
        account = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return HttpResponse("That user dosn't exist.")

    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

    return render(request, 'account/account.html', context=context)
