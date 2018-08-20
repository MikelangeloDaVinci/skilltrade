from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from website import views
from website.forms import LoginForm
from website.views import SignUpView, IndexView, LogoutView, UserSettingsView, api_cities_json_view, ProfilePictureView, \
    EditSkillsView, EditSkillView, api_skills_json_view, EditNeedsView, EditNeedView

urlpatterns = [
    url(r'^login/$', auth_views.login, {'authentication_form': LoginForm}, name='login'),
    url(r'^sign-up/$', SignUpView.as_view(), name='sign_up'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^user-settings/$', UserSettingsView.as_view(), name='user_settings'),
    url(r'^profile-picture/$', ProfilePictureView.as_view(), name='profile_picture'),
    url(r'^edit-skills/$', EditSkillsView.as_view(), name='edit_skills'),
    url(r'^skill/update/$', EditSkillView.as_view(), name='edit_skill'),
    url(r'^edit-needs/$', EditNeedsView.as_view(), name='edit_needs'),
    url(r'^need/update/$', EditNeedView.as_view(), name='edit_need'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/public/cities.json$', api_cities_json_view, name='api_cities_json_view'),
    url(r'^api/public/skills.json$', api_skills_json_view, name='api_skills_json_view'),
    url(r'^password/change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password/change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password/reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password/reset/\
            (?P<uidb64>[0-9A-Za-z_\-]+)/\
            (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)