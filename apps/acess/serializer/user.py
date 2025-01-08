from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse

from apps.acess.models.user import Address
from apps.common.serializers import AppWriteOnlyModelSerializer


class UserAddressSerializer(AppWriteOnlyModelSerializer):
    """This is CUD Serializer for UserAddress model..."""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Address
        fields = ["id", "tag", "address", "city", "state", "country", "pincode"]


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset"""

    def form_valid(self, form):
        """return True if password reset is valid"""

        form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            email_template_name="registration/password_reset_email.html",
        )
        return JsonResponse({"detail": "Password reset e-mail has been sent."})
