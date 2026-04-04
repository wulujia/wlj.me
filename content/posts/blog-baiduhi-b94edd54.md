---
title: "nagios监控系统安装(2)"
date: 2008-12-21T21:00:00+08:00
tags: ["Life"]
draft: false
slug: "blog-baiduhi-b94edd54"
---

6、设置监控报警

需要调整的文件包括：

/usr/local/nagios/etc/objects/contacts.cfg

/usr/local/nagios/etc/objects/commands.cfg

a./usr/local/nagios/etc/objects/contacts.cfg

这里面是联系人、分组的信息，简单配置contact项目如下：

define contact{

         contact_name                     nagiosadmin

         use                              generic-contact

         service_notification_period      24x7

         host_notification_period         24x7

         service_notification_options     w,u,c,r

         host_notification_options        d,u,r

         alias                            Nagios Admin

         service_notification_commands    notify-service-by-email,notify-service-by-sms

         host_notification_commands       notify-host-by-email,notify-host-by-sms

         email                            wulujia@gmail.com        ; <<***** CHANGE THIS TO YOUR EMAIL ADDRESS ******

         }

b./usr/local/nagios/etc/objects/commands.cfg

这里配置了各种plugins的用法、命令等，可以好好看看这份文件，在其中做的事情包括了，定义发sms和通过邮件发报警信息，其中sms信息的细节建议参见《libfetion短信通知与nagios整合》：

#host notify by sms

define command {

command_name     notify-host-by-sms

command_line     /usr/local/fetion/sms.sh "Host $HOSTSTATE$ alert for $HOSTNAME$! on '$DATETIME$'">/dev/null 2>&1

}

#service notify by sms

define command {

command_name     notify-service-by-sms

command_line     /usr/local/fetion/sms.sh "$HOSTADDRESS$ $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$">/dev/null 2>&1

}

# 'notify-host-by-email' command definition

define command{

         command_name     notify-host-by-email

         command_line     /usr/local/nagios/bin/mail_send.sh "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" "***** N

agios *****\n\nNotification Type: $NOTIFICATIONTYPE$\nHost: $HOSTNAME$\nState: $HOSTSTATE$\nAddress: $HOSTADDRESS$\nInfo: $HOSTOUTPU

T$\n\nDate/Time: $LONGDATETIME$\n" $CONTACTEMAIL$

         }

# 'notify-service-by-email' command definition

define command{

         command_name     notify-service-by-email

         command_line     /usr/local/nagios/bin/mail_send.sh "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVI

CESTATE$ **" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HO

STADDRESS$\nState: $SERVICESTATE$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$" $CONTACTEMAIL$

         }

顺便提一句：如果要检查非标准端口（比如，ftp开在了22222端口上），也是修改commands.cfg文件，对check_ftp的声明修改增加-p参数即可。

# 'check_ftp' command definition

define command{

         command_name     check_ftp

         command_line     $USER1$/check_ftp -H $HOSTADDRESS$ -p $ARG1$

         }

再把test.cfg中，对应服务的检测命令后面加一个端口号的参数：

define service {

host_name ...

...

check_command check_ftp!22222

}

这就可以对22222端口的FTP进行监控，要添加多个参数，也可以如法炮制。

其中用到的脚本mail_send.sh如下：

#!/bin/bash

cd /usr/local/nagios/bin

if [ $# -ne 4 ]; then

         Subject="$1"

         AlertInfo="$2"

         Touser="$3"

         /usr/bin/python /usr/local/nagios/bin/mail_send.py "$Subject" "$AlertInfo" "$Touser"

fi

# EOF :mail_send.sh

用到的mail_send.py脚本如下：

## below is the mail_send.py

## mail_send.py

----------------------------------------------------------

# -*- coding: utf-8 -*-

import sys,os,re,glob,sys

import os.path

import smtplib

import time,datetime

import base64

import random

import email

import mimetypes

from email.MIMEMultipart import MIMEMultipart

from email.MIMEText import MIMEText

from email.MIMEImage import MIMEImage

#from email import Encoders

#from email import Message

#os.sys.path.append('/webapp/_conf/nagios/')

#from nagios_conf import visit

#################################################################

##     vspMail                                                   ##

##     参数列表                                                  ##

##     smtp_server                 发邮件smtp服务器地址           ##

##     from_usr                    发件人地址                     ##

##     to_usr                      收件人地址                     ##

##     subject                       邮件标题                     ##

##     htmlText                         邮件内容                  ##

##     auth                        是否需要认证，1为是，0为否     ##

##     log_usr                     smtp用户名                     ##

##     log_passwd                  smtp密码                       ##

##                                                              ##

#################################################################

def nagiosMail(smtp_server,from_usr,to_usr,subject,plainText,htmlText,auth,log_usr,log_passwd):

         server = smtplib.SMTP(smtp_server)

         #server.set_debuglevel(1)

         if auth == 1:

                 server.login(log_usr,log_passwd)

         strFrom = from_usr

         strTo = to_usr

         subject="=?GB2312?B?%s?=" % (base64.encodestring(subject)[:-1])

#    msgRoot = MIMEMultipart('related')

         msgRoot = MIMEMultipart('alternative')

         msgRoot['Subject'] = subject

         msgRoot['From'] = strFrom

         msgRoot['To'] = strTo

         msgRoot.preamble = 'This is a multi-part message in MIME format.'

         msgAlternative = MIMEMultipart('alternative')

         msgAlternative.attach(msgAlternative)

         #设定纯文本信息

         msgText = MIMEText(plainText, 'plain', 'gbk')

         msgAlternative.attach(msgText)       # 隐藏文本

#    msgRoot.attach(msgText)

         #设定HTML信息

         msgText = MIMEText(htmlText, 'html', 'gbk')

         msgRoot.attach(msgText)

         #设定内置图片信息,可以考虑作为取日志的附件的方法

#    fp = open('test.jpg', 'rb')

#    msgImage = MIMEImage(fp.read())

#    fp.close()

#    msgImage.add_header('Content-ID', '<image1>')

#    msgRoot.attach(msgImage)

         server.sendmail(strFrom, strTo, msgRoot.as_string())

         server.quit()

class Logger(object):

         def __init__(self):

                 from time import strftime

                 pid = os.getpid()

                 logtime=strftime('%Y%m%d')

                 self.logfile = '/var/log/nagios/nagios-%s.log' % logtime

         def write(self, err):

                 logline = '%s|%s\n' % (time.asctime(), err)

                 f = file(self.logfile, 'a')

                 f.write(logline)

                 f.close()

#class mailsend(object,subject,htmlText):

def mailsend(*arguments):

         logger = Logger()

         subject=arguments[0]

         htmlText=arguments[1]

         plainText=arguments[1]

         touser=arguments[2]

         #print subject

         #print htmlText

         #print plainText

         #return True

         #flist=visit()

         ######################################################

         ##

         ##          以下为配置内容

         ##

         ######################################################

         #邮件发送服务器地址

         smtp_server = 'localhost'

         #smtp_server = 'smtp.163.com'

         #smtp_server = 'abc.com'

         #smtp_server = '192.168.0.220'

         #发一封歇息多久

         delay = 3

         #smtp服务器是否需要验证

         #需要验证为1不需要为0

         auth = 0

         #如果需要验证，请在下面输入用户名和密码

         log_usr="abcdef"

         log_passwd="123456"

         #发件人地址

         from_usr = 'nagios@abc.com'

         try:

                 tousr=touser.split(",")

                 for to_usr in tousr:

                         print to_usr

                         nagiosMail(smtp_server,from_usr,to_usr,subject,plainText, htmlText,auth,log_usr,log_passwd)

                         logger.write('''Email has been sent to: %s \n''' % (to_usr))

                         time.sleep(delay)

                 logger.write('''......The all logs for nagios has been Finished!!!\n''')

         except IOError:

                 logger.write("Can not open list file please place it in current directory and name it as 'addr-xxx.txt'\n")

if __name__ == '__main__':

         logger = Logger()

         argv = sys.argv

         subject=argv[1]

         htmlText=argv[2]

         touser=argv[3]

         #subject="**RECOVERY alert - 192.168.0.233/Partition_Webapp is OK **"

         #htmlText="***** Nagios *****\n\nNotification Type:RECOVERY\n\nService: Partition_Webapp\nHost:192.168.0.233\nAddress: 192.168.0.233\nState:OK\n\nDate/Time: Mon Jul 30 18:24:59 CST 2007\n\nAdditionalInfo:\n\nDISK OK - free space: /webapp 757 MB (54% inode=70%):"

         print argv

         try:

                 mailsend(subject,htmlText,touser)

         except:

                 logger.write('execution failure:' + str(sys.exc_info()[0]))

                 raise

测试：/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg

启动nagios配置文件：/etc/init.d/nagios start

7、登陆web访问：http://server/nagios/

输入在nagios.pw中定义的用户名和密码登陆，就可以看到对test服务器的监控情况了，如果停止其中的某个服务，会在检测4次失败后，短消息和邮件通知。

8、如果需要服务器使用mysql进行数据存储，需要安装NDOUtils

./configure --enable-mysql

make

Mysql中建立库、用户，并赋予权限：

mysqladmin -uroot -p create nagios

mysql -uroot -p

mysql> grant all privileges on nagios.* to m1@localhost identified by 'xfocusisbest';

mysql> flush privileges;

导入库：

cd db

./installdb –u user –p password –h localhost –d database

拷贝编译完成的文件：

cp src/ndomod-3x.o /usr/local/nagios/bin/ndomod.o

cp config/ndomod.cfg /usr/local/nagios/etc/

调整/usr/local/nagios/etc/nagios.cfg

broker_module=/usr/local/nagios/bin/ndomod.o config_file=/usr/local/nagios/etc/ndomod.cfg

event_broker_options=-1

安装NDO2DB DAEMON

cp src/ndo2db-3x /usr/local/nagios/bin/ndo2db

cp config/ndo2db.cfg /usr/local/nagios/etc/

运行ndo2db，并将之加入/etc/rc.local

/usr/local/nagios/bin/ndo2db -c /usr/local/nagios/etc/ndo2db.cfg

9、如果希望对Linux受监控端的机器进行更细粒度的监控，需要安装NRPE

在客户机（受监控端），解压后：

./configure --enable-ssl --enable-command-args

make all

make install

将下面命令行运行并加入/etc/rc.local：

/usr/sbin/nrpe -c /etc/nrpe.cfg -d

在服务器（监控端），解压后：

./configure --enable-ssl --enable-command-args

make all

make install

cp sample-config/nrpe.cfg /etc/

cp src/nrpe /usr/sbin/

cp src/check_nrpe /usr/local/nagios/libexec/

在 objects/commands.cfg 中定义 check_nrpe 使用的命令：

# 'check_nrpe' command definition

define command{

         command_name     check_nrpe

         command_line     $USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$

         }

之后调整server的配置，加入check_nrpe，并重载nagios.cfg，就可以使用nrpe的功能了。

再次说明，本文中的配置和脚本多数来自：http://www.linuxtone.org/viewthread.php?tid=514，不知道是否原始出处，记录。
