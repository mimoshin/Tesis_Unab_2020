from django.urls import path
from . import views

urlpatterns =[
    path('',views.requests_view,name='requests_views'),#vista_principal
    path('revisar/<int:pk_id>/<int:r_type>',views.review_request,name='review_request'),#revisar_solicitud(admin)
    path('evento',views.new_event_request,name='new_event_request'),#nueva_solicitud_evento(cliente)
    path('info',views.new_info_request,name='new_info_request'),#nueva_solicitud_info(cliente)
    path('ver/<int:pk_id>/<int:r_type>',views.client_review,name='client_review'),#revisar_solicitud(cliente)
    path('modificar/<str:r_type>/<int:pk_id>',views.modify_request,name='modify_request'),#modificar_solicitud(cliente)
    path('question/reviews',views.question_reviews,name='question_revs'),#consultar revisiones
]