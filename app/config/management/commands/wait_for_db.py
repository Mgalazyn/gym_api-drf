#Command for django to wait for the database
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    #Waiting for db

    def handle(self, *args, **kwargs):
        self.stdout.write('Wait for db..')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Waiting for db... ')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Db up!!!'))
        
        
    