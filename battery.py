import psutil
import smtplib
from email.message import EmailMessage
import datetime

#  convert seconds to hour
def sec2hours(secs):
    mm,ss=divmod(secs,60)
    hh,mm=divmod(mm,60)
    return '%d:%02d:%02d' % (hh,mm,ss)
# psutil.sensors_battery create a tuuple with pecent,secsleft and power_plugged
battery=psutil.sensors_battery()

percent=str(battery.percent)
timeremaining=str(sec2hours(battery.secsleft))
plugged=str(battery.power_plugged)
# psutil.users() creates a list with the name of the current user and time the computer was on in second using epoch

Username=psutil.users()
Username=Username[0].name
timestarted=datetime.datetime.fromtimestamp(psutil.users()[0].started )
timestarted=timestarted.strftime('%Y %B %A %I:%M:%S %p') 
# checked if the laptop is charging
if plugged:
    plugged='Laptop is Charging'
plugged='Laptop is not Charging'


# send data to the email
msg=EmailMessage()
msg['subject']='Battery Remainder On Your Pc'
msg['From']='Your Email Address'
msg['To']='Receivers Email Address'
msg.set_content(f'Battery percent is:{percent}\nTime Remaining is:{timeremaining}\nBattery status:{plugged}')

msg.add_alternative(f'''\
<!DOCTYPE html>
<html lang="en">

<body>
     
    <h1>Hey {Username}</h1>
    <p>On {timestarted}</p>
    <h4>Battery percent is: {percent}</h4>
    <h4>Time Remaining is:  {timeremaining}</h4>
    <h4>Battery status: {plugged}</h4>
</body>
</html>

''',subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('Your Email Address','Your Password')

    smtp.send_message(msg)