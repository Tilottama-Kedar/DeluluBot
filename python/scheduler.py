from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def morning_news_job():
    print("Morning job ran at:", datetime.now())

def evening_quiz_job():
    print("Evening job ran at:", datetime.now())

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        morning_news_job,
        trigger='cron',
        hour=7,
        minute=0
    )

    scheduler.add_job(
        evening_quiz_job,
        trigger='cron',
        hour=19,
        minute=0
    )

    scheduler.start()
    print("Scheduler started")
