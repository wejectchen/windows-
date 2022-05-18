import datetime
import json
import os

time = 3600
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
endTime = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
data = {
    'startTime': now,
    'endTime': endTime,
    'cmd': ''
}

message = {
    200: '计划成功',
    201: '你已取消操作',
    300: '你已设置了关机计划',
    301: f'设置计划关机成功，你的计算机将于{endTime}关机',
    400: '尚无正在运行的计划，无法取消'
}


def readLog():
    with open('./data.json', 'r') as log:
        return json.load(log)


def writeLog(_data):
    with open('./data.json', 'w') as log:
        json.dump(_data, log)
        log.close()


def shutdown(_time):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_Time = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
    res = os.popen(f'shutdown -s -t {_time}')
    if len(res.read()) != 0:
        return 300
    data['startTime'] = now_time
    data['endTime'] = end_Time
    data['cmd'] = f'shutdown -s -t {_time}'
    writeLog(data)
    return 301


def restart(_time):
    res = os.popen(f'shutdown -r -t {_time}')
    if res.read() != '':
        print('你已设置了重启计划')
        return
    data['cmd'] = f'shutdown -s -t {_time}'
    writeLog(data)


def cancel():
    if readLog()['cmd'] == '':
        return 400
    os.popen('shutdown -a')
    data['startTime'] = ''
    data['endTime'] = ''
    data['cmd'] = ''
    writeLog(data)
    return 201
