from rest_framework.urls import path
from . import views

urlpatterns = [
    path('admin/new/', view=views.RegisterAdminUserView.as_view(), name='register_admin_account')
]
