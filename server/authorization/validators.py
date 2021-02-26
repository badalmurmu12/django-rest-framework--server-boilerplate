from oauth2_provider.oauth2_validators import OAuth2Validator
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Validator(OAuth2Validator):
    def validate_user(self, username, password, client, request, *args, **kwargs):
        if request.otp == 'True':
            # checking for otp validator
            try:
                user = User.objects.get(mobile=username)
                if user is not None and user.is_active:
                    passcode = int(password)

                    return True
            except User.DoesNotExist:
                return False
        else:
            return super().validate_user(username, password, client, request, *args, **kwargs)
        return False
