# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.management.base import BaseCommand

from oneanddone.tasks.models import TaskAttempt


class Command(BaseCommand):
    help = 'Cleans up status of tasks and attempts based on task data'

    def handle(self, *args, **options):
        qs = TaskAttempt.objects.values('id', 'created', 'modified', 'task__id', 'task__name', 'user__id', 'state')
        self.dump(qs, 'task_attempts.csv')
        print 'Done!'

    def dump(self, qs, outfile_path):
        import csv

        writer = csv.writer(open(outfile_path, 'w'))

        headers = []
        obj = qs[0]
        for key, value in obj.items():
            headers.append(key)
        writer.writerow(headers)

        for obj in qs:
            row = []
            for key, value in obj.items():
                row.append(value)
            writer.writerow(row)
