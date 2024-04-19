from django.urls import include, path
#from rest_framework import routers
from rest_framework_nested import routers
from django.views.generic import RedirectView

from user import views as user_views
from trip import views as trip_views
from location import views as location_views
from preferences import views as preferences_views

router = routers.DefaultRouter()
router.register(r'users', user_views.ClientViewSet)

router.register(r'trips', trip_views.TripViewSet, basename='trips')
trips_router = routers.NestedDefaultRouter(router, 'trips', lookup='trip')
trips_router.register(r'locations', location_views.LocationViewSet, basename='locations')

router.register(r'preferences', preferences_views.PreferenceViewSet, basename='preferences')
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(trips_router.urls)),
    path(r'login', user_views.LoginView.as_view(), name='account_login'),
    path(r'logout', user_views.LogoutView.as_view(), name='account_logout'),
]

urlpatterns += router.urls

