from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .serializers import UserSerializer

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            verification_url = f"http://localhost:8000/users/verify-email/{refresh.access_token}/"

            send_mail(
                "Verify Your Email",
                f"Click the link to verify: {verification_url}",
                "no-reply@mysite.com",
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "User created. Check email for verification."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
