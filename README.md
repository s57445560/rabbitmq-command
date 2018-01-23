# 练习
----
作者：孙杨<br>
工具名称:mq队列执行命令<br>
<br>
<br>
程序使用模块介绍:<br>
   json            复杂数据传输<br>
   pika            mq的操作api模块<br>
   threading       创建监听线程模块<br>



# 使用说明
---

首先要按1 看一下当前 连接上 服务端的客户端ip<br>
执行1需要等待3秒<br>

按2是创建组与主机的关系， 组名字 服务器ip  多ip的情况加逗号<br>
例子:<br>
sun 192.168.2.111,192.168.2.121<br>

按3是远程执行命令  组或者是ip 加命令<br>
例子:<br>
sun ifconfig<br>
192.168.2.111,192.168.2.121 ifconfig<br>
<br>

客户端启动   （运行在linux上）<br>
python3.5 bin/Clent_start.py<br>
<br>

服务端启动<br>
bin/Server_start.py<br>

配置文件<br>
conf/settings.py            （配置rabbitmq的ip地址）<br>
