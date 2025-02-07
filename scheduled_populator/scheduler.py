from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from main import news_pipeline
from logging_config import logger


def scheduled_news_process_pipeline():
    try:
        logger.info(f'Scheduled start at {datetime.now()}')
        news_pipeline()
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    logger.info('Starting scheduler...')
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_news_process_pipeline, 'interval', minutes=30)
    scheduler.start()
