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


class PollListView(generics.GenericAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin
                   ):
    # mandatory variables
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'

    # if get api require id based searching
    # def get(self, request, id=None):
    #     if id:
    #         return self.retrieve(request, id)
    #     else:
    #         return self.list(request)
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    # this is called after last line of post
    def perform_create(self, serializer):
        # this need X-CSRFToken as header field which in cookie for user login
        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def delete(self, request, id=None):
        return self.destroy(request, id)


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
