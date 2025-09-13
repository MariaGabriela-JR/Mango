from rest_framework import serializers
from .models import Scientist

class ScientistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scientist
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'scientist_id': {'read_only': True},
            'is_verified': {'read_only': True},
            'verification_token': {'read_only': True},
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True},
            'is_active': {'read_only': True}
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        user_permissions_data = validated_data.pop('user_permissions', [])
        
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        
        instance.save()

        if groups_data:
            instance.groups.set(groups_data)
        if user_permissions_data:
            instance.user_permissions.set(user_permissions_data)
        
        return instance
    
    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)

        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
            
        instance.save()

        if groups_data is not None:
            instance.groups.set(groups_data)
        if user_permissions_data is not None:
            instance.user_permissions.set(user_permissions_data)

        return instance