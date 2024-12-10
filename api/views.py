import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Author, Book, Borrow
from .serializers import AuthorSerializer, BookSerializer, BorrowSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def borrow_book(request):
    book_id = request.data.get('book_id')
    user = request.user  # Assume user is authenticated
    try:
        book = Book.objects.get(id=book_id, copies_available__gt=0)
    except Book.DoesNotExist:
        return Response({"error": "Book not available"}, status=status.HTTP_404_NOT_FOUND)

    borrow = Borrow.objects.create(book=book, user=user)
    book.copies_available -= 1
    book.save()
    serializer = BorrowSerializer(borrow)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def return_book(request, pk):
    try:
        borrow = Borrow.objects.get(id=pk, user=request.user, is_returned=False)
    except Borrow.DoesNotExist:
        return Response({"error": "Borrow record not found"}, status=status.HTTP_404_NOT_FOUND)
    
    #borrow
    borrow.is_returned = True
    borrow.return_date = datetime.date.today()
    borrow.save()
    
    book = borrow.book
    book.copies_available += 1
    book.save()
    return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)