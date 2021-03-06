from django.conf.urls import url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import (
    login,
    logout_then_login,
    password_reset,
    password_reset_complete,
    password_reset_confirm,
    password_reset_done,
)

from demotime.views import (
    index_view,
    reviews,
    reviewers,
    messages,
    users
)


# General
urlpatterns = [
    url('^$', index_view, name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^addons/$', TemplateView.as_view(template_name='addons.html'), name='addons'),
    url(r'^markdown/$', TemplateView.as_view(template_name='markdown.html'), name='markdown'),
]

# Reviews
urlpatterns += [
    url(r'^create/$', reviews.review_form_view, name='create-review'),
    url(r'^review/(?P<pk>[\d]+)/$', reviews.review_detail, name='review-detail'),
    url(
        r'^review/(?P<pk>[\d]+)/rev/(?P<rev_pk>[\d]+)/$',
        reviews.review_detail,
        name='review-rev-detail'
    ),
    url(r'^review/(?P<pk>[\d]+)/edit/$', reviews.review_form_view, name='edit-review'),
    url(
        r'^review/(?P<review_pk>[\d]+)/reviewer-status/(?P<reviewer_pk>[\d]+)/$',
        reviews.reviewer_status_view,
        name='update-reviewer-status',
    ),
    url(r'review/(?P<pk>[\d]+)/update-state/$', reviews.review_state_view, name='update-review-state'),
    url(r'comment/update/(?P<pk>[\d]+)/$', reviews.update_comment_view, name='update-comment'),
    url(r'review/(?P<pk>[\d]+)/reviewer-finder/$', reviewers.reviewer_finder, name='reviewer-finder'),
    url(r'review/(?P<pk>[\d]+)/add-reviewer/$', reviewers.add_reviewer, name='add-reviewer'),
    url(r'review/(?P<pk>[\d]+)/delete-reviewer/$', reviewers.delete_reviewer, name='delete-reviewer'),
    url(
        r'comment/(?P<comment_pk>[\d]+)/attachment/(?P<attachment_pk>[\d]+)/update/$',
        reviews.delete_comment_attachment_view,
        name='update-comment-attachment'
    ),
    url(r'review/list/$', reviews.review_list_view, name='review-list'),
]

# Messages
urlpatterns += [
    url(r'^inbox/$', messages.inbox_view, name='inbox'),
    url(r'^message/(?P<pk>[\d]+)/$', messages.msg_detail_view, name='message-detail'),
]

# Accounts
urlpatterns += [
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^accounts/profile/(?P<pk>[\d]+)/$', users.profile_view, name='profile'),
    url(r'^accounts/profile/(?P<pk>[\d]+)/edit/$', users.edit_profile_view, name='edit-profile'),
    url(
        r'^accounts/password/reset/$',
        password_reset,
        {
            'template_name': 'registration/password_reset_request.html',
            'post_reset_redirect': reverse_lazy('password_reset_done'),
        },
        name='password-reset'
    ),
    url(
        r'^accounts/password/reset/done/$',
        password_reset_done,
        {'template_name': 'registration/password_reset_submitted.html'},
        name='password_reset_done'
    ),
    url(
        r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'registration/password_reset_confirmation.html'},
        name='password_reset_confirm'
    ),
    url(
        r'^accounts/password/reset/complete/$',
        password_reset_complete,
        {'template_name': 'registration/password_reset_completed.html'},
        name='password_reset_complete'
    ),
]
