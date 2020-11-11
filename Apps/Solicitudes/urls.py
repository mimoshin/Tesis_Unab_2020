from django.urls import path
from . import views

urlpatterns =[
    path('solicitudes',views.requests_view,name='requests_views'),#vista_principal
    path('solicitudes/revisar/<int:pk_id>/<int:r_type>',views.review_request,name='review_request'),#revisar_solicitud(admin)
    path('solicitudes/evento',views.new_event_request,name='new_event_request'),#nueva_solicitud_evento(cliente)
    path('solicitudes/info',views.new_info_request,name='new_info_request'),#nueva_solicitud_info(cliente)
    path('solicitudes/ver/<int:pk_id>/<int:r_type>',views.client_review,name='client_review'),#revisar_solicitud(cliente)
    path('solicitudes/modificar/<int:pk_id>',views.modify_request,name='modify_request'),#modificar_solicitud(cliente)
]