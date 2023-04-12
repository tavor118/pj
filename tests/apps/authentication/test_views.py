from allauth.account.forms import default_token_generator
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from pytest import fixture
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def _generate_uid_and_token(user: User) -> dict[str, str]:
    uid = user_pk_to_url_str(user)
    token = default_token_generator.make_token(user)
    return {"uid": uid, "token": token}


class TestPasswordResetView:
    url = "/api/auth/password/reset/"

    def test_password_reset(
        self,
        client: APIClient,
        user: User,
        user_email: str,
        mailoutbox: list[EmailMessage],
    ):
        data = {"email": user_email}

        response = client.post(self.url, data=data)

        assert response.status_code == 200, response.data
        assert response.data == {"detail": "Password reset e-mail has been sent."}

        assert len(mailoutbox) == 1
        email = mailoutbox[0]
        assert email.subject == "[example.com] Password Reset E-mail"
        assert "example.com" in email.body


class TestPasswordResetConfirmView:
    url = "/api/auth/password/reset/confirm/"

    def test_password_reset_confirm(
        self, client: APIClient, user: User, user_email: str, user_password: str
    ):
        new_password = "new@password314"
        url_kwargs = _generate_uid_and_token(user)

        data = {
            "new_password1": new_password,
            "new_password2": new_password,
            "uid": url_kwargs["uid"],
            "token": url_kwargs["token"],
        }

        response = client.post(self.url, data=data)
        assert response.status_code == 200, response.data

        # check login with new password
        data = {"email": user_email, "password": new_password}

        login_url = "/api/auth/login/"
        response = client.post(login_url, data=data)

        assert response.status_code == 200, response.data
        assert response.data["access_token"] is not None


class TestLoginLogoutView:
    login_url = "/api/auth/login/"
    logout_url = "/api/auth/logout/"

    def test_login_and_logout(
        self, client: APIClient, user: User, user_email: str, user_password: str
    ):
        data = {"email": user_email, "password": user_password}

        response = client.post(self.login_url, data=data)

        assert response.status_code == 200, response.data
        assert response.data["access_token"] is not None

        # logout
        response = client.post(self.login_url, data=data)

        assert response.status_code == HTTP_200_OK, response.data


class TestPasswordChangeView:
    url = "/api/auth/password/change/"

    def test_password_change(
        self, client: APIClient, user: User, user_email: str, user_password: str
    ):
        client.force_authenticate(user)

        new_password = "new@password314"

        data = {
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = client.post(self.url, data=data)
        assert response.status_code == 200, response.data

        # check login with old password
        data = {"email": user_email, "password": user_password}

        login_url = "/api/auth/login/"
        response = client.post(login_url, data=data)

        assert response.status_code == 400, response.data

        # check login with new password
        data = {"email": user_email, "password": new_password}

        login_url = "/api/auth/login/"
        response = client.post(login_url, data=data)

        assert response.status_code == 200, response.data
        assert response.data["access_token"] is not None


class TestRegistrationView:
    registration_url = "/api/auth/registration/"
    confirm_email_url = "/api/auth/registration/verify-email/"

    def test_registration(
        self,
        client: APIClient,
        user_email: str,
        user_password: str,
        username: str,
        mailoutbox: list[EmailMessage],
    ):
        registration_data = {
            "username": username,
            "email": user_email,
            "password1": user_password,
            "password2": user_password,
        }

        response = client.post(self.registration_url, data=registration_data)

        assert response.status_code == HTTP_201_CREATED, response.data
        assert response.data == {"detail": "Verification e-mail sent."}

        user = User.objects.get(email=user_email)
        assert user.username == username

        assert len(mailoutbox) == 1
        email = mailoutbox[0]
        assert email.subject == "[example.com] Please Confirm Your E-mail Address"

        email_address = EmailAddress.objects.first()
        email_confirmation = EmailConfirmationHMAC(email_address)
        key = email_confirmation.key
        assert key in email.body

        # check email confirmation
        confirmation_data = {"key": key}

        response = client.post(self.confirm_email_url, data=confirmation_data)

        assert response.status_code == 200, response.data
        assert response.data == {"detail": "ok"}
