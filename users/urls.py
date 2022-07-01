from django.urls import path
from .views import UsersAPIList, UserAPICreate, UserAPIReadUpdateDelete

urlpatterns = [
    path('', UsersAPIList.as_view()),
    path('register', UserAPICreate.as_view()),
    path('<int:id>', UserAPIReadUpdateDelete.as_view()),
]
