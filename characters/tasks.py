from celery import shared_task

from characters.scrapper import sync_characters_with_api


@shared_task
def run_sync_with_api():
    sync_characters_with_api()
