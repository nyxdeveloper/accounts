# rest framework
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action

# django
from django.db import transaction

# локальные импорты
from .models import User
from .models import OTC
from .exceptions import InvalidOTC
from .serializers import UserSerializer
from .services import clean_phone
from .services import get_auth_payload
from .services import send_otc


class AuthenticationViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def phone_auth_autoreg(self, request):
        phone = request.data.get("phone")
        otc = request.data.get("otc")

        if not phone:
            return Response({"detail": "Укажите телефон"}, status=400)

        phone = clean_phone(phone)

        if otc:
            if OTC.objects.filter(key=phone, code=otc).exists():
                try:
                    return Response(get_auth_payload(self.get_queryset().get(phone=phone), request))
                except User.DoesNotExist:
                    return Response(get_auth_payload(User.objects.create(phone=phone), request))
            raise InvalidOTC
        return Response(send_otc(phone))

    def email_auth(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email:
            return Response({"detail": "Укажите email"}, status=400)
        if not password:
            return Response({"detail": "Укажите пароль"}, status=400)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                return Response(get_auth_payload(user, request), status=200)

        return Response({"detail": "Неверный логин или пароль"}, status=400)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def auth(self, request):
        auth_type = request.query_params.get("t")
        if auth_type == "phone_autoreg":
            return self.phone_auth_autoreg(request)
        if auth_type == "email":
            return self.email_auth(request)
        return Response({"detail": "Недоступный метод авторизации"}, status=400)
