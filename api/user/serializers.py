from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from user.models import Client

from trip import serializers as trip_serializers


# Serializer only for User class - No extra information included
class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Client
        fields = ['id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password']
        read_only_fields = ['created_at', 'updated_at']

        def create(self, validated_data):
            return Client.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance) #type: ignore

            return instance
