import os
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models


class LoginView(View):
    """ Login View Definition """

    def get(self, request):

        form = forms.LoginForms()

        return render(request, "users/login.html", {"form": form})

    def post(self, request):

        form = forms.LoginForms(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse("cores:home"))

        return render(request, "users/login.html", {"form": form})


def log_out(request):

    logout(request)
    return redirect(reverse("cores:home"))


class SignUpView(FormView):
    """ Sign Up View Definition """

    template_name = "users/signup.html"
    form_class = forms.SignUpForms
    success_url = reverse_lazy("cores:home")

    def form_valid(self, form):

        form.save()  # If the form is valid, gonna save
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            user.veify_email()
            login(self.request, user)
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("cores:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    """ Custom Exception """

    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            post_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            post_request_error = post_request.json().get("error", None)
            if post_request_error is not None:
                raise GithubException
            access_token = post_request.json().get("access_token")
            get_request = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                },
            )
            username = get_request.json().get("login")
            if username is not None:
                name = get_request.json().get("name")
                email = get_request.json().get("email")
                bio = get_request.json().get("bio")
                avatar_url = get_request.json().get("avatar_url")
                user = models.User.objects.get(email=email)
                try:
                    if avatar_url is not None:
                        get_photo = requests.get(avatar_url)
                        content_photo = get_photo.content
                        user.avatar.save(f"{name}-avatar", ContentFile(content_photo))
                    if user.auth != models.User.AUTH_GITHUB:
                        raise GithubException()
                except models.User.DoesNotExist:
                    # Not Using 'create_user' because in here, we're not taking care of passwords
                    user = models.User.objects.create(
                        username=email,
                        first_name=name,
                        bio=bio,
                        email=email,
                        email_verified=True,
                        auth=models.User.AUTH_GITHUB,
                    )
                    if avatar_url is not None:
                        get_photo = requests.get(avatar_url)
                        content_photo = get_photo.content
                        user.avatar.save(f"{name}-avatar", ContentFile(content_photo))
                    user.set_unusable_password()
                    user.save()
                finally:
                    login(request, user)
                    return redirect(reverse("cores:home"))
            else:
                print("Cannot get User info")
                raise GithubException()
        else:
            print("Empty Code")
            raise GithubException()
    except GithubException:
        messages.error(request, "Something went wrong.")
        return redirect(reverse("users:login"))


def kakao_login(request):
    app_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    """ Custom Exception """

    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("KAKAO_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        get_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        json_token_result = get_request.json()
        access_token = json_token_result.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_request = profile_request.json()
        kakao_account = profile_request.get("kakao_account")
        email = kakao_account.get("email", None)
        gender = kakao_account.get("gender", None)
        nickname = kakao_account.get("profile").get("nickname", None)
        if email is None:
            raise KakaoException()
        try:
            user = models.User.objects.get(email=email)
            if user.auth != models.User.AUTH_KAKAO:  # If user has kakao auth
                raise KakaoException()

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                first_name=nickname,
                email=email,
                gender=gender.lower(),
                email_verified=True,
                auth=models.User.AUTH_KAKAO,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)  # We are gonna log the user in
        return redirect(reverse("cores:home"))
    except Exception:
        """
        requests.post(
            "https://kapi.kakao.com/v1/user/unlink",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        """
        return redirect(reverse("users:login"))
