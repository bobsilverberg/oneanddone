from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from oneanddone.tasks import models
from oneanddone.tasks.forms import TaskModelForm


class TaskAreaAdmin(MPTTModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    form = TaskModelForm
    list_display = ('name', 'area_full_name', 'execution_time', 'is_available',
                    'start_date', 'end_date', 'is_draft')
    list_filter = ('area', 'is_draft')
    search_fields = ('name', 'area__name', 'short_description')
    fieldsets = (
        (None, {
            'fields': ('name', 'area', 'execution_time')
        }),
        ('Details', {
            'fields': ('short_description', 'instructions')
        }),
        ('Availability', {
            'fields': ('start_date', 'end_date', 'is_draft')
        })
    )

    def is_available(self, task):
        return task.is_available
    is_available.boolean = True

    def area_full_name(self, task):
        return task.area.full_name


class TaskAttemptAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'state')
    list_filter = ('state',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'state')
    search_fields = ('text',)

    def task(self, feedback):
        return feedback.attempt.task

    def user(self, feedback):
        return feedback.attempt.user

    def state(self, feedback):
        return feedback.attempt.state

admin.site.register(models.TaskArea, TaskAreaAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskAttempt, TaskAttemptAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)
