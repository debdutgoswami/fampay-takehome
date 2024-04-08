from celery import Task, states
from datetime import datetime, timedelta

from core.handlers import YTHandler
from youtube.celery import app


class FetchYTVideoPeriodicTask(Task):
    name = "core.tasks.FetchYTVideoPeriodicTask"
    run_every = 10

    def run(self, *args, **kwargs):
        from core.models import YTDataV3Credentials, YTMetadata
        from django_celery_results.models import TaskResult

        tr: TaskResult = (
            TaskResult.objects.filter(
                periodic_task_name=self.name, status=states.SUCCESS
            )
            .order_by("-date_created")
            .first()
        )
        if tr is None:
            published_after = datetime.now() - timedelta(hours=24)
        else:
            published_after = tr.date_created

        data = YTHandler(
            keys=YTDataV3Credentials.objects.all().values_list(
                "encrypted_text", flat=True
            )
        ).get_all_data(published_after)
        YTMetadata.objects.bulk_create(
            [YTMetadata(**item) for item in data], ignore_conflicts=True
        )


app.register_task(FetchYTVideoPeriodicTask())
