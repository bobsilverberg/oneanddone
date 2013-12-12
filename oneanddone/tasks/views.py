# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from django_filters.views import FilterView
from tower import ugettext as _

from oneanddone.base.util import get_object_or_none
from oneanddone.users.mixins import UserProfileRequiredMixin
from oneanddone.tasks.filters import AvailableTasksFilterSet
from oneanddone.tasks.forms import FeedbackForm
from oneanddone.tasks.mixins import TaskMustBePublishedMixin
from oneanddone.tasks.models import Feedback, Task, TaskAttempt


class AvailableTasksView(TaskMustBePublishedMixin, FilterView):
    queryset = Task.objects.order_by('-execution_time')
    context_object_name = 'available_tasks'
    template_name = 'tasks/available.html'
    paginate_by = 10
    filterset_class = AvailableTasksFilterSet


class TaskDetailView(TaskMustBePublishedMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    allow_expired_tasks = True

    def get_context_data(self, *args, **kwargs):
        ctx = super(TaskDetailView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated():
            ctx['attempt'] = get_object_or_none(TaskAttempt, user=self.request.user,
                                                task=self.object, state=TaskAttempt.STARTED)
        return ctx


class StartTaskView(UserProfileRequiredMixin, TaskMustBePublishedMixin,
                    generic.detail.SingleObjectMixin, generic.View):
    model = Task

    def post(self, *args, **kwargs):
        task = self.get_object()
        if not task.is_available:
            messages.error(self.request, _('That task is unavailable at this time.'))
            return redirect('tasks.available')

        attempt, created = TaskAttempt.objects.get_or_create(user=self.request.user, task=task,
                                                             state=TaskAttempt.STARTED)
        return redirect(task)


class AbandonTaskView(UserProfileRequiredMixin, TaskMustBePublishedMixin,
                      generic.detail.SingleObjectMixin, generic.View):
    model = TaskAttempt

    def post(self, *args, **kwargs):
        attempt = get_object_or_404(TaskAttempt, pk=kwargs['pk'],
                                    state=TaskAttempt.STARTED)
        attempt.state = TaskAttempt.ABANDONED
        attempt.save()

        return redirect('tasks.feedback', attempt.pk)


class FinishTaskView(UserProfileRequiredMixin, TaskMustBePublishedMixin,
                     generic.detail.SingleObjectMixin, generic.View):
    model = TaskAttempt

    def post(self, *args, **kwargs):
        attempt = get_object_or_404(TaskAttempt, pk=kwargs['pk'],
                                    state=TaskAttempt.STARTED)
        attempt.state = TaskAttempt.FINISHED
        attempt.save()

        return redirect('tasks.feedback', attempt.pk)


class CreateFeedbackView(UserProfileRequiredMixin, TaskMustBePublishedMixin, generic.CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'tasks/feedback.html'

    def dispatch(self, request, *args, **kwargs):
        self.attempt = get_object_or_404(TaskAttempt, pk=kwargs['pk'],
                                         state__in=[TaskAttempt.FINISHED, TaskAttempt.ABANDONED])
        return super(CreateFeedbackView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(CreateFeedbackView, self).get_context_data(*args, **kwargs)
        ctx['attempt'] = self.attempt
        return ctx

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.attempt = self.attempt
        feedback.save()

        messages.success(self.request, _('Your feedback has been submitted. Thanks!'))
        return redirect('users.profile.detail')
