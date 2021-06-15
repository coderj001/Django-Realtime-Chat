import base64
import json
import logging
import os

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core import files
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from account.forms import AccountAuthForm, AccountUpdateForm, RegistrationForm
from account.models import Account

logger = logging.getLogger(__name__)

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_redirect_if_exists(request):
    redirect = None
    if request.method == 'GET':
        next = request.GET.get('next')
        if next:
            redirect = str(next)
    logger.info('Rederict after login or registration.')
    return redirect


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        logger.warn(f"Auth User {user.email} trying to view register page.")
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
        else:
            context['login_form'] = form

    else:
        form = AccountAuthForm()
        context['login_form'] = form

    return render(request, 'account/login.html', context=context)


def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get('id')
    try:
        if not cache.has_key(
            reverse(
                'account:account_view',
                kwargs={
                    'id': user_id
                }
            )
        ):
            account = Account.objects.get(id=user_id)
            cache.set(
                reverse(
                    'account:account_view',
                    kwargs={
                        'id': user_id
                    }
                ),
                account,
                CACHE_TTL
            )
        else:
            account = cache.get(
                reverse(
                    'account:account_view',
                    kwargs={
                        'id': user_id
                    }
                )
            )
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


def account_search_view(request, *args, **kwargs):
    context = {}

    if request.method == 'GET':
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_result = Account.objects.filter(Q(email__icontains=search_query) | Q(
                username__icontains=search_query)).distinct()
            accounts = list()
            if search_result:
                accounts = [(q, False) for q in search_result]

            context['accounts'] = accounts

    return render(request, "account/search_result.html", context=context)


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('account:login_view')
    user_id = kwargs.get('id')
    try:
        account = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return HttpResponse("That user dosn't exist.")

    if account.id != request.user.id:
        return HttpResponse("You Can't edit others profile.")

    context = {}

    if request.method == 'POST':
        form = AccountUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            cache.delete(reverse(
                'account:account_view',
                kwargs={
                    'id': user_id
                }
            )
            )
            logger.info(f"Updated user {account.username}")
            return redirect('account:account_view', id=account.id)
        else:
            form = AccountUpdateForm(
                request.POST,
                instance=request.user,
                initial={
                    "id": account.id,
                    "email": account.email,
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email
                }
            )
            context['form'] = form
    else:
        form = AccountUpdateForm(initial={
            "id": account.id,
            "email": account.email,
            "username": account.username,
            "profile_image": account.profile_image,
            "hide_email": account.hide_email
        })
        context['form'] = form

    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_account.html", context=context)


def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect Padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(f"{settings.TEMP}/{str(user.id)}"):
            os.mkdir(f"{settings.TEMP}/{str(user.id)}")
        url = os.path.join(
            f"{settings.TEMP}/{str(user.id)}",
            TEMP_PROFILE_IMAGE_NAME
        )
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as des:
            des.write(image)
        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "="*((4-len(imageString) % 4) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
    return None


@csrf_exempt
def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.method == 'POST' and user.is_authenticated:
        try:
            imageString = request.POST.get('image')
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = Image.open(url)
            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeigth = int(float(str(request.POST.get("cropHeigth"))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            left = cropX
            top = cropY+cropHeigth
            right = cropX+cropWidth
            bottom = cropY

            crop_img = img.crop((left, top, right, bottom))
            user.profile_image.delete()
            user.profile_image.save(files.File(open(url, "rb")))

            payload['result'] = "success"
            payload['cropped_profile_image'] = user.profile_image.url
            os.remove(url)
        except Exception as e:
            payload['result'] = "Error"
            payload['exception'] = str(e)
            logger.debug(str(e))
    return HttpResponse(json.dumps(payload), content_type="application/json")
