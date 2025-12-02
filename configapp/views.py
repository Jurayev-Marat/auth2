from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Todo, User
from .serializers import TodoSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        todos = Todo.objects.filter(user=request.user, completed=True)
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        todos = Todo.objects.filter(user=request.user, completed=False)
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Todo.objects.filter(user=request.user).count()
        completed = Todo.objects.filter(user=request.user, completed=True).count()
        pending = Todo.objects.filter(user=request.user, completed=False).count()
        return Response({
            "total": total,
            "completed": completed,
            "pending": pending
        })
