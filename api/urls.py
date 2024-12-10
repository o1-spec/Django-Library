from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
]
