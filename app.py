from apscheduler.schedulers.blocking import BlockingScheduler
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urlencode
# import SynopticChartReader

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=25)
def timed_job():
    result = urlopen("https://meteohub-bot.herokuapp.com/ping").read()
    print("I'm working...")
    # SynopticChartReader.Run();

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()