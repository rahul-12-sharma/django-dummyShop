from django.contrib import admin
from django.urls import path, include
from products import views  # ✅ Import your view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup_view, name='signup'),  # ✅ Use the function here
]
