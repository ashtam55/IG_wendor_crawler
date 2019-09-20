def main(): 
    from crontab import CronTab

    cron = CronTab(user='True')

    job = cron.new(command='pip freeze')
    job.minute.on(1)

    cron.write()

if __name__ == "__main__":
  main()