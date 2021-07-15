from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    # ByPasses JWT auth
    permission_classes = [permissions.AllowAny]

    def post(self, request, **kwargs):
        """
        POST with "id_token"
        Send an id token as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["id_token"]
        return Response(data, status=status.HTTP_200_OK)
