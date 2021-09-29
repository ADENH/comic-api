from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'comics', views.ComicViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('popular-comic/',views.popular_comic ,name="popular_comic"),
    path('detail-comic/',views.detail_comic ,name="detail_comic"),
    path('read-comic/', views.read_comic, name="read_comic"),
    path('list-comic/', views.list_comic, name="list_comic"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]