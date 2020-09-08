from django.urls import path
from . import views

urlpatterns =[
    path('solicitudes',views.requests_view,name='requests_views'),
    path('solicitudes/revisar/<int:pk_id>',views.review_request,name='review_request'),
    path('solicitudes/nueva',views.new_request,name='new_request'),
]