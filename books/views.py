from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from .models import Book
from .serializers import *
from .permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def check_availability(self, request, pk=None):
        if pk is None:
            return Response(
                {
                    "message": "Invalid request",
                    "message": status.HTTP_400_BAD_REQUEST
                }
            )
        book = get_object_or_404(Book, pk=pk)
        if book.availability:
            return Response(
                    {
                    'message': 'Book is available',
                     "status": status.HTTP_200_OK
                    }
            )
        else:
            return Response(
                    {
                        'message': 'Book is not available',
                     "status": status.HTTP_404_NOT_FOUND
                    }
            )
        

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()
        title = self.request.GET.get("title")
        author = self.request.GET.get("author")
        isbn = self.request.GET.get("isbn")
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn__icontains=isbn)

        return queryset
            