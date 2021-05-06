from rest_framework import serializers
from backend.accounts.serializers import UserSerializer

class ContactGroupSerializer(serializers.Serializer):

    all_contacts = UserSerilizer(source='contacts', many=True)
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        if obj.role == 0:
            return 'Administrador'
        else:
            return 'Jefe de Zona'

    class Meta:
        model = User
        fields = ['email', "given_name", "family_name", "picture", 'role']
        

    
    
