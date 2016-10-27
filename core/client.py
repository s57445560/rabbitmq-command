#!/usr/bin/env python
# coding:utf-8
# Author: Sun Yang

import pika
import os, sys
import threading
import socket
import subprocess
import json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings

mq_ip = settings.MQ_IP


class Client:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=mq_ip))
        self.channel = self.connection.channel()
        self.localIP = socket.gethostbyname(socket.gethostname())
        self.running()

    def monitor(self):
        self.channel.exchange_declare(exchange='command',
                                      type='fanout')

        self.result = self.channel.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

        self.channel.queue_bind(exchange='command',
                                queue=self.queue_name)
        self.channel.basic_consume(self.callback,
                              queue=self.queue_name,
                              no_ack=True)
        self.channel.start_consuming()

    def reply_register(self):
        channel_r = self.connection.channel()
        result = channel_r.queue_declare(queue='register')
        channel_r.basic_publish(exchange='',
                              routing_key='register',
                              body=self.localIP)
        print("[+] 发送本地ip 注册信息")
        channel_r.close()

    def reply_command(self,msg):
        channel_r2 = self.connection.channel()
        result = channel_r2.queue_declare(queue='return_info')
        channel_r2.basic_publish(exchange='',
                              routing_key='return_info',
                              body=msg)
        print("[+] 发送命令返回信息")
        channel_r2.close()

    def callback(self, ch, method, properties, body):
        msg = str(body, encoding='utf8')
        if msg == 'register_info':
            self.reply_register()
        else:
            msg = json.loads(msg,encoding='utf8')
            if self.localIP in msg['ip']:
                ret = subprocess.Popen(msg['command'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                ret = ret.stdout.read()+ ret.stderr.read()
                return_msg = {
                    'msg':str(ret,encoding='utf8'),
                    'ip':self.localIP
                }
                msg = json.dumps(return_msg)
                self.reply_command(msg)
    def running(self):
        f1 = threading.Thread(target=self.monitor, args=())
        print('[+] 队列监听线程开启')
        f1.start()


# a = Client()
