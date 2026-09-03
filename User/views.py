from rest_framework.views import APIView
from rest_framework.response import Response
from.serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken # to create model object


class RegisterView(APIView):
    def post(self,request):
       serializer=RegisterSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({"message":"Account created!"},status=201)
       return Response(serializer.errors,status=400)

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
        })

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            RefreshToken(request.data['refresh']).blacklist()
        except Exception:
            return Response({'detail':"Bad Token"},status=400)
        return Response({"detail":"Logged Out Successfully"},status=205)    
