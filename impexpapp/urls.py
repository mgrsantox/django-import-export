from django.urls import path
from .views import *
app_name = 'impexpapp'
urlpatterns = [

    path('', BulkStudentImportView.as_view(), name='upload'),
    path('export/', BulkStudentExportView.as_view(), name='export'),
]
