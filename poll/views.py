from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins


from poll.Serializers import QuestionSerializer
from poll.models import Question


# class PollListView(generics.GenericAPIView, mixins.ListModelMixin):
#     serializer_class = QuestionSerializer
#


class PollAPIView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            question = serializer.save()
            return JsonResponse(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PollDetailView(APIView):
    def get_object(self, id):
        try:
            return Question.objects.get(id=id)
        except Question.DoesNotExist as e:
            return Response({"error": "Given question object not found"}, status=404)

        def get(self, request, id=None):
            instance = self.get_object(id)
            serializer = QuestionSerializer(instance)
            return Response(serializer.data)


@csrf_exempt
def poll(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        json_parser = JSONParser
        data = json_parser.parse(request)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            question = serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def poll_details(request, id):
    # instance = get_object_or_404(Question, id=id)
    try:
        instance = Question.objects.get(id=id)
    except Question.DoesNotExist as e:
        return JsonResponse({"error": "Given question object not found"}, status=404)

    if request.method == "GET":
        serializer = QuestionSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        json_parser = JSONParser
        data = json_parser.parse(request)
        serializer = QuestionSerializer(data=data, many=True)
        if serializer.is_valid():
            question = serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        instance.delete()
        return HttpResponse(status=204)
