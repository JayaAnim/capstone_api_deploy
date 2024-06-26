from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from user.models import Client

class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    has_preferences = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password', 'has_preferences']
        read_only_fields = ['created_at', 'updated_at', 'has_preferences']

    def get_has_preferences(self, obj):
        return hasattr(obj, 'preference')

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
