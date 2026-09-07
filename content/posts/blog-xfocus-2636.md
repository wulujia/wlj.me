---
title: "警惕：Norton杀毒软件严重误报，大量用户无法开机"
date: 2007-05-18T00:00:00+08:00
tags: ["Startup"]
draft: false
slug: "blog-xfocus-2636"
---

一、事件分析：
                

今日，超级巡警团队接受到大量用户求助，因为安装Norton杀毒软件，升级到最新特征定义后，导致将系统杀坏，无法开机。
                

杀软报警截图如下：

                  

                

经过分析，这是该杀软对系统正常文件的误报，鉴于Norton杀毒软件在国际上有庞大的装机量，将会有大批用户遭遇无法开机现象。
                

关于被报文件netapi32.dll：
                

文件说明：

                  netapi32.dll 名称为：Microsoft LAN Manager DLL，它是Windows网络应用程序接口，用于支持访问微软网络。
                

经过我们分析，该文件可以正常通过微软数字签名认证，从而证实了该杀软误报。
                

该
杀软为什么会误报该文件呢？经过我们追踪分析，netapi32.dll曾经跟近年几个重要的漏洞有关，其中04年的Lsasrv.dll
漏洞，它是从系统Netapi32.dll中找到DsRolepEncryptPasswordStart函数，在第一个参数过长导致了溢出。由于
Netapi32.dll中的DsRoleUpgradeDownlevelServer函数是一个客户端函数，该漏洞只能在本机触发，所以黑客会修改
Netapi32.dll，将请求发送给本机的变量地址改为黑客制定指定的IP地址，从而远程利用该漏洞。此外还有其它的漏洞出现在
Netapi32.dll本身，由于杀软会检测该文件是否被修改利用，从而就造成了特征提取错误，误报了系统中原本正常的文件。
                

二、解决方案：
                
                
                  
                    
                  
                
                

在该杀毒软件报警后，不要重启动系统，会造成无法启动。

                  1、在病毒服务器的系统中心将病毒库恢复到17日以前的版本。

                    2、对于已经更新病毒定义的客户端，千万不要重新启动电脑，关掉symantec antivirus 服务，从隔离区里面恢复被隔离的两个文件。

                  3、使用该杀软的信任列表和目录，将该文件临时加入到信任列表中，并及时关注官方最新升级特征。

                4、紧急停用该杀软。

                5、如果系统已经无法启动，可以使用windows 安装光盘启动系统，执行如下命令恢复被杀除的文件：

                 expand G:\I386\netapi32.dl_ c:\windows\system32\netapi32.dll

                expand G:\I386\netapi32.dl_ c:\windows\system32\dllcache\netapi32.dll

                expand G:\I386\lsasrv.dl_ c:\windows\system32\lsasrv.dll

                  expand G:\I386\lsasrv.dl_ c:\windows\system32\dllcache\lsasrv.dll 

超级巡警：彻底查杀各种木马，全面保护系统安全。

                  更多免费工具下载：[http://www.dswlab.com](http://www.dswlab.com/)

                  专业的桌面与内容安全产品：[http://www.unnoo.com ](http://www.unnoo.com%20/)
