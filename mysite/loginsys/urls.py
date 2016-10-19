from django.conf.urls import url
from loginsys.views import (login,
                            logout,
                            register,
                            update,
                            delete,
                            # show_users
)
from django.contrib.auth import views as auth_views

app_name = 'loginsys'

urlpatterns = [
    # it`s for action in admin
    # url(r'^(?P<ct>[0-9]+)/(?P<ids>.*)/$', show_users, name='show_users'),

    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'password_reset_form.html',
                                                          'email_template_name': 'password_reset_email.html',
                                                          'subject_template_name': 'password_reset_subject.txt',
                                                          'post_reset_redirect': 'loginsys:password_reset_done'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'password_reset_done.html',
                                                                    'current_app': 'loginsys'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^update/$', update, name='update'),
    url(r'^(?P<id>[0-9]+)/delete/$', delete, name='delete'),
    ]

