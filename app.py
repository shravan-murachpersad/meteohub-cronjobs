from apscheduler.schedulers.blocking import BlockingScheduler
import SynopticChartReader

sched = BlockingScheduler()

@sched.scheduled_job('interval', hour=5)
def timed_job():
    # SynopticChartReader.Run();

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()