import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    args = '[days]'
    help = 'Deletes uploads older than specified days'

    def handle(self, *args, **options):
        from uploader.models import Upload

        try:
            days = int(args[0])
        except ValueError:
            raise CommandError('"%s" is not an integer' % args[0])
        if days <= 0:
            raise CommandError('"%s" must be a positive integer' % days)

        end_date = timezone.now() - datetime.timedelta(days=days)
        for upload in Upload.objects.filter(date_uploaded__lt=end_date):
            upload.delete()
