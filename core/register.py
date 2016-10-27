#!/usr/bin/env python
# coding:utf-8
# Author: Sun Yang

import pika
import os, sys
import threading
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings

mq_ip = settings.MQ_IP



class Register:
    ip_list = []
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=mq_ip))
        self.channel_r = self.connection.channel()
        self.running()


    def send_request(self):
        self.channel_c = self.connection.channel()
        self.channel_c.exchange_declare(exchange='command',
                                 type='fanout')
        self.channel_c.basic_publish(exchange='command',
                              routing_key='',
                              body="register_info")
        self.channel_c.close()

    def receive(self):
        self.ip_list = []
        result = self.channel_r.queue_declare(queue='register')
        self.channel_r.basic_qos(prefetch_count=1)
        self.channel_r.basic_consume(self.callback,
                              queue='register',
                              no_ack=True)
        self.channel_r.start_consuming()

    def callback(self, ch, method, properties, body):
        # print(body)
        if str(body,encoding='utf8') not in self.ip_list:
            self.ip_list.append(str(body,encoding='utf8'))

    def running(self):
        f1 = threading.Thread(target=self.receive, args=())
        print('[+] 注册监听线程程序开启')
        f1.start()

# a = Register()
# a.send_request()
# a.running()
# time.sleep(3)
# print(a.ip_list)