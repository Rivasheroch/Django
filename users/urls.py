

from django.urls import path, include
from .views import home, activate, logout_view
from .import views
urlpatterns = [
    path('', home, name='home'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('accounts/', include('allauth.urls')),
    path('logout/', logout_view, name='logout'),  # Add this line

]
