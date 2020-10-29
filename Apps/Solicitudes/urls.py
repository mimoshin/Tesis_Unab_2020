from django.urls import path
from . import views

urlpatterns =[
    path('solicitudes',views.requests_view,name='requests_views'),#vista_principal
    path('solicitudes/revisar/<int:pk_id>',views.review_request,name='review_request'),#revisar_solicitud(admin)
    path('solicitudes/evento',views.new_event_request,name='new_event_request'),#nueva_solicitud_evento(cliente)
    path('solicitudes/info',views.New_info_request,name='new_info_request'),#nueva_solicitud_info(cliente)
]