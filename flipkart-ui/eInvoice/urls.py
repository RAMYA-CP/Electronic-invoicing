from .import views
from django.urls import path
urlpatterns=[
    path('',views.upload,name='homepage'),
    path('download/', views.download,name='download'),
    path('analyze/', views.analyze,name='analyze')
]