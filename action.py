import json
import os
import datetime

time = 3600
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
endTime = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
data = {
    'startTime': now,
    'endTime': endTime,
    'cmd': ''
}


def readLog():
    with open('data.json', 'r') as log:
        return json.load(log)


def writeLog(_data):
    with open('data.json', 'w') as log:
        json.dump(_data, log)
        log.close()


def shutdown(_time):
    res = os.popen(f'shutdown -s -t {_time}')
    if res != '':
        print('你已设置了关机计划')
        return
    data['cmd'] = f'shutdown -s -t {_time}'
    writeLog(data)
    print(format(res))


def restart(_time):
    res = os.popen(f'shutdown -r -t {_time}')
    if res != '':
        print('你已设置了重启计划')
        return
    data['cmd'] = f'shutdown -s -t {_time}'
    writeLog(data)
    print(res.read().format())


def cancel():
    res = os.popen('shutdown -a')
    if res != '':
        print('尚无正在运行的计划，无法取消')
        return
    data['startTime'] = ''
    data['endTime'] = ''
    data['cmd'] = ''
    writeLog(data)
    print('你已取消操作')
