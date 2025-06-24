from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile

        # fields = '__all__'.

        exclude =['password']

        read_only_fields = ['role', 'username']