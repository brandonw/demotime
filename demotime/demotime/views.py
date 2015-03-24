from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from demotime import forms, models


def index(request):
    return render(request, 'demotime/index.html', {})


class ReviewDetail(DetailView):
    template_name = 'demotime/review.html'
    model = models.Review


class CreateReviewView(TemplateView):
    template_name = 'demotime/create_review.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateReviewView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.review_inst = models.Review(creator=self.request.user)
        self.review_form = forms.ReviewForm(
            user=self.request.user,
            instance=self.review_inst,
            data=request.POST
        )
        AttachmentFormSet = formset_factory(forms.AttachmentForm, extra=4, max_num=5)
        self.attachment_forms = AttachmentFormSet(data=request.POST, files=request.FILES)
        if self.review_form.is_valid() and self.attachment_forms.is_valid():
            data = self.review_form.cleaned_data
            data['creator'] = request.user
            data['attachments'] = []
            for form in self.attachment_forms.forms:
                if form.cleaned_data:
                    data['attachments'].append({
                        'attachment': form.cleaned_data['attachment'],
                        'attachment_type': form.cleaned_data['attachment_type'],
                    })

            models.Review.create_review(**data)

            return redirect('index')
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.review_inst = models.Review(creator=self.request.user)
        self.review_form = forms.ReviewForm(
            user=self.request.user,
            instance=self.review_inst
        )
        AttachmentFormSet = formset_factory(forms.AttachmentForm, extra=4, max_num=5)
        self.attachment_forms = AttachmentFormSet()
        return super(CreateReviewView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateReviewView, self).get_context_data(**kwargs)
        context.update({
            'review_form': self.review_form,
            'review_inst': self.review_inst,
            'attachment_forms': self.attachment_forms
        })
        return context


review_form_view = CreateReviewView.as_view()
review_detail = ReviewDetail.as_view()
