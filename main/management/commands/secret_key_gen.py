from django.core.management import base, utils


class Command(base.BaseCommand):
    help = 'Generate an APIKey'

    def handle(self, *args, **kwargs):
        print('Add this to your .env file:\n\n')
        self.stdout.write(self.style.SUCCESS(f'SECRET_KEY={utils.get_random_secret_key()}'))
