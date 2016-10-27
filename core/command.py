#!/usr/bin/env python
# coding:utf-8
# Author: Sun Yang

import pika
import os, sys
import threading
import time
import json



from conf import settings

mq_ip = settings.MQ_IP



class Command:
    ip_list = []
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=mq_ip))
        self.channel_r = self.connection.channel()
        self.running()


    def send_request(self,command):
        self.channel_c = self.connection.channel()
        self.channel_c.exchange_declare(exchange='command',
                                 type='fanout')
        self.channel_c.basic_publish(exchange='command',
                              routing_key='',
                              body=command)
        self.channel_c.close()

    def receive(self):
        self.ip_list = []
        result = self.channel_r.queue_declare(queue='return_info')
        self.channel_r.basic_qos(prefetch_count=1)
        self.channel_r.basic_consume(self.callback,
                              queue='return_info',
                              no_ack=True)
        self.channel_r.start_consuming()

    def callback(self, ch, method, properties, body):
        msg = json.loads(body.decode(),encoding='utf8')
        self.ip_list.append(msg)
        # print("################",msg['ip'])
        # print(msg['msg'])
        # print(type(str(body,encoding='utf8')))


    def running(self):
        f1 = threading.Thread(target=self.receive, args=())
        print('[+] 命令返回监听线程开启')
        f1.start()
