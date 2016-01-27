# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from nose.tools import eq_, assert_true

from oneanddone.users.tests import UserFactory
from oneanddone.tasks.tests import (TaskFactory, TaskProjectFactory, TaskTeamFactory,
                                    TaskTypeFactory, TaskAttemptFactory)


class APITests(APITestCase):

    def assert_response_status(self, response, expected_status):
        eq_(response.status_code, expected_status,
            "Test Failed, got response status: %s, expected status: %s" %
            (response.status_code, expected_status))

    def create_task(self, creator):
        team = TaskTeamFactory.create()
        project = TaskProjectFactory.create()
        type = TaskTypeFactory.create()

        return TaskFactory.create(team=team, project=project, type=type,
                                  creator=creator, owner=creator)

    def setUp(self):
        self.client_user = UserFactory.create()

        # Give all permissions to the client user
        self.client_user.is_superuser = True
        self.client_user.save()

        self.token = Token.objects.create(user=self.client_user)
        self.uri = '/api/v1/task/'

    def test_get_task_details(self):
        """
        Test GET details of a task with particular id for authenticated user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        user = UserFactory.create()

        test_task = self.create_task(user)
        TaskAttemptFactory.create(user=user, task=test_task)
        task_uri = self.uri + str(test_task.id) + '/'

        task_data = {"id": test_task.id,
                     "name": test_task.name,
                     "short_description": test_task.short_description,
                     "instructions": test_task.instructions,
                     "prerequisites": test_task.prerequisites,
                     "execution_time": test_task.execution_time,
                     "is_draft": test_task.is_draft,
                     "is_invalid": test_task.is_invalid,
                     "project": test_task.project.name,
                     "team": test_task.team.name,
                     "type": test_task.type.name,
                     "repeatable": test_task.repeatable,
                     "start_date": test_task.start_date,
                     "end_date": test_task.end_date,
                     "difficulty": test_task.difficulty,
                     "why_this_matters": test_task.why_this_matters,
                     "keyword_set": [
                         {"name": keyword.name} for keyword in test_task.keyword_set.all()],
                     "edit_url": '',
                     "url": '/tasks/%s/' % test_task.id,
                     "owner": user.email}

        response = self.client.get(task_uri)
        self.assert_response_status(response, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        eq_(response_data, task_data)

    def test_get_task_list(self):
        """
        Test GET task list for authenticated user
        """
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        user = UserFactory.create()

        test_task = self.create_task(user)
        TaskAttemptFactory.create(user=user, task=test_task)
        task_data = {"id": test_task.id,
                     "name": test_task.name,
                     "short_description": test_task.short_description,
                     "instructions": test_task.instructions,
                     "prerequisites": test_task.prerequisites,
                     "execution_time": test_task.execution_time,
                     "is_draft": test_task.is_draft,
                     "is_invalid": test_task.is_invalid,
                     "project": test_task.project.name,
                     "team": test_task.team.name,
                     "type": test_task.type.name,
                     "repeatable": test_task.repeatable,
                     "start_date": test_task.start_date,
                     "end_date": test_task.end_date,
                     "difficulty": test_task.difficulty,
                     "why_this_matters": test_task.why_this_matters,
                     "keyword_set": [
                         {"name": keyword.name} for keyword in test_task.keyword_set.all()],
                     "owner": user.email,
                     "edit_url": '',
                     "url": '/tasks/%s/' % test_task.id}

        response = self.client.get(reverse('api-task'), {}, **header)
        self.assert_response_status(response, status.HTTP_200_OK)
        response_data = json.loads(response.content)['results']
        assert_true(task_data in response_data)
