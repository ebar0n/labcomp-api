from django.conf.urls import include, url
from django.contrib import admin
from lab_reservations.urls import router as reservations_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/reservations/', include(reservations_router.urls)),
]
