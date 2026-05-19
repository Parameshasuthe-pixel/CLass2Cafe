from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def reminder_job():
    print("Sending snack reminders...")


def start_scheduler():
    scheduler.add_job(reminder_job, 'interval', minutes=30)
    scheduler.start()