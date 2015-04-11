from django import forms
from django.contrib.auth.models import User

from demotime import models


class ReviewForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5})
    )

    def __init__(self, user, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['reviewers'].queryset = User.objects.exclude(
            pk=user.pk).exclude(username='demotime_sys')

        for key, value in self.fields.iteritems():
            self.fields[key].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Review
        fields = (
            'reviewers', 'description', 'title',
            'case_link',
        )


class CommentForm(forms.ModelForm):

    thread = forms.ModelChoiceField(
        queryset=models.CommentThread.objects.none(),
        widget=forms.widgets.HiddenInput(),
        required=False
    )

    def __init__(self, thread=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        if thread:
            self.fields['thread'].queryset = models.CommentThread.objects.filter(
                pk=thread.pk
            )
            self.fields['thread'].required = True

        for key, value in self.fields.iteritems():
            self.fields[key].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Comment
        fields = (
            'comment',
        )


class AttachmentForm(forms.Form):

    attachment = forms.FileField(
        required=False,
        widget=forms.widgets.FileInput(
            attrs={'class': 'form-control'}
        )
    )
    attachment_type = forms.ChoiceField(
        choices=models.Attachment.ATTACHMENT_TYPE_CHOICES,
        widget=forms.Select
    )
    description = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'}),
        max_length=2048
    )


class ReviewerStatusForm(forms.Form):

    status = forms.ChoiceField(choices=models.Reviewer.STATUS_CHOICES)
    review = forms.ModelChoiceField(queryset=models.Review.objects.none)
    reviewer = forms.ModelChoiceField(queryset=models.Reviewer.objects.none)

    def __init__(self, reviewer, *args, **kwargs):
        super(ReviewerStatusForm, self).__init__(*args, **kwargs)
        self.fields['review'].queryset = models.Review.objects.filter(
            pk=reviewer.review.pk)
        self.fields['reviewer'].queryset = models.Reviewer.objects.filter(
            pk=reviewer.pk)
