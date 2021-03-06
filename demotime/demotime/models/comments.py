from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from .attachments import Attachment
from .base import BaseModel
from .messages import Message
from .users import UserReviewStatus


class CommentThread(BaseModel):

    review_revision = models.ForeignKey('ReviewRevision')

    def __unicode__(self):
        return u'Comment Thread for Review: {}'.format(self.review_revision)

    @classmethod
    def create_comment_thread(cls, review_revision):
        return cls.objects.create(review_revision=review_revision)

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']


class Comment(BaseModel):

    commenter = models.ForeignKey('auth.User')
    comment = models.TextField()
    thread = models.ForeignKey('CommentThread')
    attachments = GenericRelation('Attachment')

    def __unicode__(self):
        return u'Comment by {} on Review: {}'.format(
            self.commenter.username, self.thread.review_revision.review.title
        )

    @classmethod
    def create_comment(cls, commenter, comment, review,
                       thread=None, attachment=None, attachment_type=None,
                       description=None):
        if not thread:
            thread = CommentThread.create_comment_thread(review)

        obj = cls.objects.create(
            commenter=commenter,
            comment=comment,
            thread=thread
        )
        if attachment or attachment_type:
            Attachment.objects.create(
                attachment=attachment,
                attachment_type=attachment_type,
                description=description,
                content_object=obj,
            )

        system_user = User.objects.get(username='demotime_sys')
        users = list(review.review.reviewers.all())
        users.append(review.review.creator)
        for reviewer in users:
            if reviewer == commenter:
                continue

            UserReviewStatus.objects.filter(
                review=review.review,
                user=reviewer,
            ).update(read=False)

            context = {
                'receipient': reviewer,
                'sender': system_user,
                'comment': obj,
                'url': review.get_absolute_url(),
                'title': review.review.title,
            }
            Message.send_system_message(
                'New Comment on {}'.format(review.review.title),
                'demotime/messages/new_comment.html',
                context,
                reviewer,
                revision=review,
                thread=thread,
            )

        return obj

    class Meta:
        ordering = ['created']
