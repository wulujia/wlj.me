---
title: "COOKIE欺骗"
date: 2001-03-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-119"
---

(quack_at_xfocus.org)

ＣＯＯＫＩＥ欺骗

来源：[http://sunviva.yeah.net](http://sunviva.yeah.net/)


现在有很多社区网为了方便网友浏览，都使用了cookie技术以避免多次输入密码（就如the9和vr），所以只要对服务器递交给用户的cookie进行改写就可以达到欺骗服务程序的目的。 


ＣＯＯＫＩＥ欺骗原理 

按照浏览器的约定，只有来自同一域名的cookie才可以读写，而cookie只是浏览器的，对通讯协议无影响，所以要进行cookie欺骗可以有多种途径： 

１、跳过浏览器，直接对通讯数据改写 

２、修改浏览器，让浏览器从本地可以读写任意域名cookie 

３、使用签名脚本，让浏览器从本地可以读写任意域名cookie（有安全问题） 

４、欺骗浏览器，让浏览器获得假的域名 

其中： 

方法１、２需要较专业的编程知识，对普通用户不太合适。 

方法３的实现有２种方法： 

１、直接使用签名脚本，不需要签名验证，但是产生很严重的安全问题，因为大家都要上网的，如果这样做你的硬盘文件就…… 

２、对脚本进行签名后再使用签名脚本，但是需要专用的数字签名工具，对普通用户也不合适。 

方法４看样子应该是最合适的了，域名欺骗很简单，也不需要什么工具（当然如果你的机器装有web服务器那更好了），下面我以the9为例，以这种方法为基础，阐述一下cookie欺骗的过程（下文中提到的任何服务端的bug，the9都已经做了改进，所以本文对the9无安全方面的影响）： 


注：我们讨论的cookie是那种不会在硬盘的cookie文件里留下踪迹的cookie，就是那种只在浏览器生存周期内（会话）产生的cookie，如果浏览器关闭（会话结束）那么这个cookie就被删了！　 


ＣＯＯＫＩＥ欺骗实战 

the9在登陆的时候会返回３个cookie（这可把浏览器的警告cookie选项打开时看到）： 

cgl_random（随即序列号）：登陆识别的记号 

cgl_loginname（登陆名）：身份的识别记号 

cgl_areaid（小区号）：你居住的小区号码 

只要把cgl_loginname填入正确的登陆名，再对cgl_random进行修改，就可以达到欺骗服务程序的目的。 


一般欺骗php程序的字符串为： 

1''or''1''=''1 

把这个填入cgl_random，服务程序就被欺骗了！ 

因为服务程序不太可能对cookie进行语法检查（the9现在改进了），那么把这个字符串填入，就可以成功的欺骗对方程序，而达到突破的目的了！ 


现在的问题是，如何使浏览器把这个我改过的cookie返回给the9？ 

看一看the9的域名吧：[http://www.the9.com/](http://www.the9.com/)，而浏览器的cookie警告已经告诉了我们这３个cookie会返回给有.the9.com这个域名的服务器，哎？我的机器上正好有web服务器，那么动手吧！ 

先编一个设置cookie的html，就叫cookie.htm吧，然后把这个cookie放进web目录，这样还不行，因为我的机器的域名没设，那么设置host的名字，可是如果在网络设置中进行设置的话，机器要重启动的，还是想想别的简单的办法吧！ 

然后我们应该编辑hosts文件，这个文件应该在windows目录下，你有可能找不到它，但是如果你找到了hosts.sam文件，那么把它后面的扩展名去掉，就是我们要的文件了！ 

编辑hosts文件，填入以下一行: 

127.0.0.1 www0.the9.com 

解释一下，127.0.0.1是本机的lo地址，可以用做web地址，而www0.the9.com就是我们欺骗产生的域名。 

然后在浏览器中输入[http://www0.the9.com/cookie.htm](http://www0.the9.com/cookie.htm)，看，页面出来了，快设置cookie吧！ 

直接访问http;//www.the9.com/main.htm看看，不错吧！ 


但是不是所有的网友都有自己的web服务器啊！那怎么办呢？ 

其实如果你有个人主页的话，也可以达到cookie欺骗的目的，比如某个个人主页的服务器的ip地址是1.2.3.4，先上传cookie.htm文件，再编辑hosts文件： 

1.2.3.4 www0.the9.com 

然后访问[http://www0.the9.com/](http://www0.the9.com/)***/cookie.htm，其中***是你个人主页的地址目录。 


对了我作了个工具在我的主页上，现在公开一下,[http://home.etang.com/fsl/9the/](http://home.etang.com/fsl/9the/)，大家知道该怎么做了吧？嘿嘿，不过你那样设置是没有用的，要这样编辑hosts： 

etang的ip [www.the9.com](http://www.the9.com/) 

the9的ip www0.the9.com 

为什么要这样呢？我等会会告诉大家的 


继续the9的cookie讨论，还有2个cookie： 

cgl_mainshowinfo（个人信息） 

cgl_showinfo_changed（意义不知） 

由于第二个cookie不知道是什么，所以就讨论第一个。 

第一个cookie存放着你在the9的名字、称号、居住的小区、街道、是否有工作、星级、门牌号等的信息（目前只知道这些，其余的信息不知其意义，具体格式就让给大家去分析了），但是中文都escape过了，如果你用的不是netscpae而是ie的话，不能用unescape得知其信息，因为ie对双字节采用unicode而不采用ascii，如果哪天the9也支持unicode就好了！：），但是其他网站站长注意了，你们可通过cgi的形式把这些the9居民信息抓过来实现数据共享！哈哈……，如果你们真要这么做，就只有使用签名脚本了，总不能让别人编辑hosts吧（不过得注意版权哦！）？ 


ie的cookie漏洞： 

如果你用的是ie的话，由于ie本身的漏洞，你大可不必编辑hosts，就可以同样做到读写别的域名的cookie，你可以使用以下的方法欺骗ie（具体的可以去[www.cookiecentral.com](http://www.cookiecentral.com/)看看）： 

假设你的主页文件为[http://a.com/cookie.htm](http://a.com/cookie.htm)， 

使用以下url： [http://a%2Ecom%2Fcookie%2Ehtm%3F.the9.com](http://a%2Ecom%2Fcookie%2Ehtm%3F.the9.com/) 

如果直接输在浏览器地址栏里不行，就作个script，把location的值设为这个就可以了！ 

这个地址转换后应该是这样的： [http://a.com/cookie.htm?.the9.com](http://a.com/cookie.htm?.the9.com) 

由于ie的bug，误把前面那个的域名以为是.the9.com了！ 


hosts文件解释 

hosts文件实际上可以看成一个本机的dns系统，它可以负责把域名解释成ip地址，它的优先权比dns服务器要高，它的具体实现是TCP/IP协议中的一部分。 

如果有这么一行： 

202.109.110.3 [www.the9.com](http://www.the9.com/) 

那么在输入[www.the9.com](http://www.the9.com/)时，网络协议会首先检查hosts文件找到匹配的，如果找不到再去dns查，这样你访问[www.the9.com](http://www.the9.com/)实际上是访问202.109.110.3，而不是通常的202.109.110.2。 

注：由于缓存的作用，如果开着浏览器编辑hosts的话，hosts里的内容有可能不会当场生效，你可以重新启动浏览器或等一会时间再试一下！ 


关于ＲＥＦＥＲＥＲ的欺骗（这个虽然不属于cookie欺骗，但是懒得再写一篇，就归在一起了） 

referer是http头，它的作用是签定用户是从何处引用连接的，在the9，服务程序就充分利用了这一点，如过你是手动输入url的话，那么referer不会设任何值，服务程序就返回什么“投机取巧”的字样！ 

由于我们前面对浏览器进行了域名欺骗，那么referer也被欺骗了，但是服务程序对referer是整个主机名检查，所以www0.the9.com的域名就欺骗不了服务器，所以得用[www.the9.com](http://www.the9.com/)欺骗，那么还得设一个域名方便我们访问the9，而且还得让cookie返回给这个真的the9，那么就用www0.the9.com吧！（这回知道前面访问我主页工具时要那样编辑hosts了吧？） 

如果你用了这个方法的话，那么你就不能直接点击the9的连接，而得用工具中的地址欺骗来进行访问，至于这样做的好处，大家自己找找吧，我就不想详细说了，太累了！ 


关于netvampire： 

这个下载工具大家都知道吧？那么它的3.3版大家用过吗？很棒的！因为它可以直接让大家改变下载连接的referer，而且它还能继承浏览器的cookie，把cookie返回给服务端（不过cookie不能改，如果能改的话，这个工具就太………………） 


后记 

好了关于cookie及referer就说到这了，在这个星期以前利用cookie欺骗的话the9的门户可是大开的（当然似乎还有通用密码什么的），不过the9虽然改进了，我不能保证其他社区网也改进了，当然本文只是探讨技术，不负什么法律责任。
