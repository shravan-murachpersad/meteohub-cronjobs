from crontab import CronTab

cron = CronTab(user='murachpersad')  
job = cron.new(command='python /app/WeatherStation.py')  
job.minute.every(15)

#cron.remove_all()

cron.write()