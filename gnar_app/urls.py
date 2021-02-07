from django.urls import path, include

from . import views
from django.conf import settings

from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
        path('', views.index, name="index"),
        path('climbs/<int:climb_id>', views.climb_by_id, name='climb_by_id'),
        path('add_climb', views.add_climb, name="add_climb"),
        path('gnar_leaderboard', views.gnar_leaderboard, name="gnar_leaderboard"),
        path('trivia', views.trivia_home, name="trivia"),
        path('accounts/', include('django.contrib.auth.urls')),
        path('accounts/signup', views.signup, name='signup'),
        path('loggedincheck', views.loggedincheck, name='loggedincheck'),
        path('dump_climbs', views.dump_climbs, name='dump_climbs'),
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
