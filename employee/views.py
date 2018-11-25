from django.contrib.auth.models import User
from rest_framework import viewsets

from employee.serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer



