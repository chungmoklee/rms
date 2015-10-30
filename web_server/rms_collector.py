__author__ = 'cmlee'


from gevent import monkey
monkey.patch_all()
#monkey.patch_sys(stdin=True, stdout=False, stderr=False)
import gevent
from influxdb import InfluxDBClient
import time
import random




dbname = 'rms'

measurement = 'rms'
device = 'RE001'
region = 'Hanaro'

client = InfluxDBClient(host='172.16.87.132', port=8086, database='rms')

while True:

    data_point = '%s,device=%s,region=%s value=%f %d000000000' % \
                 (measurement,
                  device,
                  region,
                  random.uniform(0, 100),
                  int(time.time()))
    client.write(data_point)
    gevent.sleep(5)
