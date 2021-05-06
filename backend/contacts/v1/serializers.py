from rest_framework import serializers

from backend.accounts.v1.serializers import UserSerializer
from backend.accounts.models import User

class ContactGroupSerializer(serializers.Serializer):

    all_contacts = UserSerializer(source='contacts', many=True)
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        if obj.role == 0:
            return 'Administrador'
        else:
            return 'Jefe de Zona'

    class Meta:
        model = User
        fields = ['email', "given_name", "family_name", "picture", 'role', 'all_contacts']
        

    
    
