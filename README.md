# 练习
----
作者：孙杨
工具名称：mq队列执行命令


程序使用模块介绍：
    json            复杂数据传输
    pika            mq的操作api模块
    threading       创建监听线程模块



##################################使用说明


首先要按1 看一下当前 连接上 服务端的客户端ip
                执行1需要等待3秒

按2是创建组与主机的关系， 组名字 服务器ip  多ip的情况加逗号
                例子：
                    sun 192.168.2.111,192.168.2.121

按3是远程执行命令  组或者是ip 加命令
                例子：
                    sun ifconfig
                    192.168.2.111,192.168.2.121 ifconfig

客户端启动   （运行在linux上）
            python3.5 bin/Clent_start.py

服务端启动
            bin/Server_start.py

配置文件
            conf/settings.py            （配置rabbitmq的ip地址）