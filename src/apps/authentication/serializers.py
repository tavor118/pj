from dj_rest_auth.serializers import PasswordResetSerializer


class MyPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {"email_template_name": "password_reset_email.html"}
