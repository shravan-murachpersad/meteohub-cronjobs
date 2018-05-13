from crontab import CronTab

cron = CronTab(user='murachpersad')  
# job = cron.new(command='python /app/WeatherStation.py')  
# job.minute.every(15)

Synoptic_Reader = cron.new(command='python /app/Test.py')  
Synoptic_Reader.minute.every(1)

#cron.remove_all()

cron.write()