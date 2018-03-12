from crontab import CronTab

cron = CronTab(user='murachpersad')  
job = cron.new(command='python /app/WeatherStation.py')  
job.minute.every(1)

for item in cron:  
    print(item)

cron.remove_all()

for item in cron:  
    print(item)

cron.write()