# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from rest_framework import serializers

from django.contrib.auth.models import User

from oneanddone.tasks.models import (Task, TaskAttempt, TaskKeyword,
                                     TaskProject, TaskTeam, TaskType)


class TaskAttemptSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.SlugRelatedField(
        many=False,
        queryset=User.objects.all(),
        slug_field='email')

    class Meta:
        model = TaskAttempt
        fields = ('user', 'state')


class TaskKeywordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaskKeyword
        fields = ('name',)


class TaskProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaskProject
        fields = ('id', 'name',)


class TaskTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaskType
        fields = ('id', 'name',)


class TaskTeamSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = TaskTeam
        fields = ('id', 'name', 'description', 'url')


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    keyword_set = TaskKeywordSerializer(
        many=True,
        read_only=True,
        required=False)
    project = serializers.SlugRelatedField(
        many=False,
        queryset=TaskProject.objects.all(),
        slug_field='name')
    team = serializers.SlugRelatedField(
        many=False,
        queryset=TaskTeam.objects.all(),
        slug_field='name')
    type = serializers.SlugRelatedField(
        many=False,
        queryset=TaskType.objects.all(),
        slug_field='name')
    owner = serializers.SlugRelatedField(
        many=False,
        queryset=User.objects.all(),
        slug_field='email')
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    edit_url = serializers.SerializerMethodField('edit_url_if_staff')

    class Meta:
        model = Task
        fields = ('id', 'name', 'short_description', 'instructions', 'owner',
                  'prerequisites', 'execution_time', 'start_date', 'end_date',
                  'is_draft', 'is_invalid', 'project', 'team', 'type', 'repeatable',
                  'difficulty', 'why_this_matters', 'keyword_set', 'url', 'edit_url')

    def edit_url_if_staff(self, obj):
        user = self.context['request'].user
        if user.is_staff:
            return obj.get_edit_url()
        return ''
