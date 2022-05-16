import os
import datetime
import sys

time = 3600
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
endTime = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
print(now)
print(endTime)


def writeToLog(data):
    with open('log.txt', 'w') as log:
        log.write(data)
        log.close()


def shutdown(_time):
    res = os.popen(f'shutdown -s -t {_time}')
    if len(res.read().format()) != '':
        print("已设置关机")
        sys.exit(0)
    print(format(res.read()))


def restart(_time):
    res = os.popen(f'shutdown -r -t {_time}')
    print(res.read().format())


def cancel():
    res = os.popen('shutdown -a')
    print(res.read().format())


shutdown(time)
sys.exit(0)
