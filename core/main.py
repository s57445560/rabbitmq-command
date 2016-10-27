#!/usr/bin/env python
# coding:utf-8
# Author: Sun Yang


import time,sys
import re, json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import register
import command

class Main:
    def __init__(self):
        self.master = register.Register()
        self.group_ip_dic = {}
        self.conn = command.Command()
    def function(self):
        while True:
            p_list = [(1,"刷新查看连接主机"),(2,"设置组信息"),(3,"执行命令")]
            for ind,val in p_list:
                print(ind,val)
            user_inp = input("请输入相应的序号：")
            if user_inp == "1":
                self.master.send_request()
                for num in [3,2,1]:
                    r1 = '\r[等待 %s]'%num
                    sys.stdout.write(r1)
                    sys.stdout.flush()
                    time.sleep(1)
                print()
                print("以下登陆的客户端ip如下！")
                for ip in self.master.ip_list:
                    print(ip)
                self.master.ip_list = []
            elif user_inp == '2':
                print('加入组之前需要先刷新一下主机信息 先按1')
                print('加入组的模式是，组名 ip 多ip用逗号分隔,每次只允许定义一组信息，如需多组请多次输入！')
                user_inp = input("请按照格式输入，<q>返回,请按照格式输入：")
                if user_inp == 'q':
                    continue
                else:
                    group = user_inp.strip().split()[0]
                    ip = user_inp.strip().split()[-1]
                    if group == ip:
                        print("输入有误，请重新输入！")
                        continue
                    ip_list = ip.split(',')
                    self.group_ip_dic[group] = ip_list
                    print(self.group_ip_dic)
                    print(group,"组设置成功！")
            elif user_inp == '3':
                print("格式如下 ip command,或者 组 command ，第一种多ip的情况逗号分隔")
                p = re.compile(r"^[a-zA-Z\.]+")
                user_inp = input("请输入对应格式 <q>退出：")
                group_ip = user_inp.strip().split()[0]
                commd = user_inp.strip().split()[-1]
                group_ip_list = group_ip.split(',')
                if p.search(group_ip):
                    if not self.group_ip_dic.get(group_ip):
                        print("输入的组信息有误！")
                        continue
                    else:
                        ip_list = self.group_ip_dic.get(group_ip)
                else:
                    ip_list = group_ip.split(',')
                msg ={
                    'command':commd,
                    'ip':ip_list
                }

                msg = json.dumps(msg)
                self.conn.send_request(msg)
                a=0
                while len(self.conn.ip_list) < len(ip_list):
                    time.sleep(0.1)
                    a+=1
                    if a == 30:
                        print("输入信息有误，检查逗号是否是正常逗号，没有返回数据的ip 请按1检查是否连接正常"
                              "数据超时3s!")
                        break
                for msg in self.conn.ip_list:
                    print("################", msg['ip'])
                    print(msg['msg'])
                self.conn.ip_list = []
                input("<<<<<<上面是执行结果，回车继续>>>>>")


a = Main()
a.function()