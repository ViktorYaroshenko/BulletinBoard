from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', AdList.as_view(), name = 'ads'),
    path('<int:pk>', AdDetail.as_view(), name = 'ad'),
    path('create_ad/', CreateAdView.as_view(), name='create_ad'),
    path('<int:pk>/edit/', AdEdit.as_view(), name='edit_ad'),
    path('responses/', ResponseList.as_view(), name='responses'),
    path('responses/accept/<int:response_id>/', views.accept_response, name='accept_response'),
    path('responses/reject/<int:response_id>/', views.reject_response, name='reject_response'),
    path('mailing/', mailing, name='mailing'),
]
