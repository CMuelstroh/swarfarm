from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from herders import views as herder_views
from herders.forms import CrispyAuthenticationForm, CrispyPasswordChangeForm, CrispyPasswordResetForm, CrispySetPasswordForm

urlpatterns = [
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    # url(r'^api/', include('api.urls')),
    url(r'^apiv2/', include('apiv2.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-auth/get-token/', obtain_jwt_token),
    url(r'^api-auth/refresh-token/', refresh_jwt_token),
    url(r'^api-auth/verify-token/', verify_jwt_token),

    # Bestiary
    url(r'^bestiary/', include('bestiary.urls', namespace='bestiary')),

    # SWARFARM app
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),
    url(r'^data/', include('sw_parser.urls', namespace='sw_parser')),
    url(r'^', include('herders.urls', namespace='herders')),
    url(r'^', include('news.urls', namespace='news')),

    # Django auth/admin stuff
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, {'authentication_form': CrispyAuthenticationForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'news:latest_news'}, name='logout'),
    url(r'^password_change/$', auth_views.password_change,
        {
            'password_change_form': CrispyPasswordChangeForm,
            'post_change_redirect': 'password_change_done',
        },
        name='password_change'),
    url(r'^password_change/done$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, {'password_reset_form': CrispyPasswordResetForm}, name='password_reset'),
    url(r'^password_reset/done$', auth_views.password_reset_done, name='password_reset_done'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'set_password_form': CrispySetPasswordForm},
        name='password_reset_confirm',
    ),
    url(
        r'^reset/done/$',
        auth_views.password_reset_complete,
        {'extra_context': {'form': CrispyAuthenticationForm}},
        name='password_reset_complete'
    ),
    url(r'^username_change/$', herder_views.change_username, name="username_change"),
    url(r'^username_change/done/$', herder_views.change_username_complete, name="username_change_complete"),
]
