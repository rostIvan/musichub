from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from auth.tasks import send_email_account_activation
from auth.verification import EmailVerificationUUIDStorage
from musichub import fields


class SignUpSerializer(serializers.ModelSerializer):
    password = fields.PasswordField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        self.activation_request(user)
        return user

    def activation_request(self, user):
        uuid, email = EmailVerificationUUIDStorage.save(user.email)
        activation_link = self.get_full_activation_link(uuid)
        send_email_account_activation.delay(email, activation_link)

    def get_full_activation_link(self, uuid):
        request = self.context['request']
        sub_link = reverse('activate_account', args=(uuid,))
        return request.build_absolute_uri(sub_link)
