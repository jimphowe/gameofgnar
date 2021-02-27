from django.urls import path, include

from . import views
from django.conf import settings

from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
        path('', views.index, name="index"),
        path('climbs/<int:climb_id>', views.climb_by_id, name='climb_by_id'),
        path('addson/<int:game_id>', views.add_on_by_id, name='game_id'),
        path('add_climb', views.add_climb, name="add_climb"),
        path('gnar_leaderboard', views.gnar_leaderboard, name="gnar_leaderboard"),
        path('trivia', views.trivia_home, name="trivia"),
        path('accounts/', include('django.contrib.auth.urls')),
        path('accounts/signup', views.signup, name='signup'),
        path('loggedincheck', views.loggedincheck, name='loggedincheck'),
        path('view_climbs', views.view_climbs, name='view_climbs'),
        path('profile', views.profile, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
