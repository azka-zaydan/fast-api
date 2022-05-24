from datetime import datetime
from time import sleep

while True:
    now = datetime.now()
    print(now.strftime("%H : %M : %S"))
    hour = int(now.strftime("%H")) * 3600
    minute = int(now.strftime("%M")) * 60
    second = int(now.strftime("%S"))
    total = hour + minute + second
    print(total)
    sleep(1)

# def conv_time(time):
#     hour = int(time.split(':')[0]) * 3600
#     minute = int(time.split(':')[1]) * 60
#     seconds = int(time.split(':')[2])
#     one_for_all = hour + minute + seconds
#     print(time)
#     print(one_for_all)
