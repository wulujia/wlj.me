---
title: "对 365kit 的疑问和建议"
date: 2005-07-26T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1148"
---

[365kit ](http://www.365kit.com/)是号称是一个自动更新的通讯录，其实我对这个功能并不怎么看好，原因是：

1、通讯录里有大量个人隐私和商业数据，备份在别人那里，实在不放心；
2、自动更新的意义有多大？首先它需要用户都填写自己的真实信息，其次需要你有大量的朋友用 365kit ，事实上，我至少有 2/3 的朋友很少甚至不上网。

对 365kit 现在的实现方式，还多一个不看好：outlook 究竟有多少人用？个人认为，国内并不多。

他有隐私协议，仔细看看，觉得未能给我完全的信心，如下：

协议：未经用户同意，365KIT不会向任何个人或机构透露用户个人资料信息，除非要求查看者拥有中华人民共和国宪法和法律认可的有关部门书面授权。
wlj：这条就不需要注解了 :)

协议：用户关键资料经由高度加密，除非破坏数据库，否则入侵者无法获取这些资料。
wlj：这段话是有问题的，入侵者要获取资料，绝对不会破坏数据库，条条大路通罗马。

协议：365KIT拥有严格的共享级别限制体系，只有得到你授权的用户，才能共享你指定的联系人信息。
wlj：能授权共享就一定可能被“越权共享”，至少这是我的经验。

仔细想想，它究竟安全吗？试一试吧，花了将近半个小时玩瞎子摸象：

1、365kit 走的是 HTTP 协议，所有数据传送全部明文，局域网内容易被人窃听密码和数据（例如，[这样](http://blog.xfocus.net/resserver.php?blogId=1&resource=365kit3.png)就是访问我建的一个用户数据，并不需要客户端）。没有验证码，容易被人暴力猜测口令；
2、在通讯薄填入[超长用户名](http://blog.xfocus.net/resserver.php?blogId=1&resource=365kit2.png)（我测试的是 255 位），点击同步时，可能导致 365kit & outlook 崩溃，那么至少恶意好友能够利用网络更新的机会溢出你的机器。
3、在安装目录下存在365kit.dat文件，默认保存登陆信息（启动 outlook 后并不需要每次输入密码，除非每次手工注销），如果被窃取可能导致数据泄露；
4、部份 web 程序还存在问题，利用得当，说不定也能获取更多信息，比如点[这里](http://211.161.159.167/servlet/UserN2C?username=hongbo%40donews.com&password=test&invite=1&nuserlist=%3Cnamecards%3E%3Cnamecard%3E%3Cnid+v=%22X83CCCCA2-A825-4CF5-9BF6-D509EF3A625BX%22%2F%3E%3Clastname+v=%22XXX%22%2F%3E%3Cfirstname+v=%22%E9%B2%81%E5%8A%A0%22%2F%3E%3Cfullname+v=%22XXX%22%2F%3E%3Chometelephonenumber+v=%22aaaaa%22%2F%3E%3Cmobiletelephonenumber+v=%228888888888%22%2F%3E%3Ctags+nid=%22X83CCCCA2-A825-4CF5-9BF6-D509EF3A625BX%22+v=%22%2C%22+%2F%3E%3C%2Fnamecard%3E%3Cnamecard%3E%3Cnid+v=%22X21F226C0-1172-44E8-AB87-FF71813B0CEBX%22%2F%3E%3Clastname+v=%22%E5%BC%A0%22%2F%3E%3Cfirstname+v=%22%E4%B8%89%22%2F%3E%3Cfullname+v=%22%E5%BC%A0%E4%B8%89%22%2F%3E%3Cmobiletelephonenumber+v=%221111111%22%2F%3E%3Ctags+nid=%22X21F226C0-1172-44E8-AB87-FF71813B0CEBX%22+v=%22%2C%22+%2F%3E%3C%2Fnamecard%3E%3Ccusertags%3E%3C%2Fcusertags%3E%3C%2Fnamecards%3E)会出现[500错误](http://blog.xfocus.net/resserver.php?blogId=1&resource=365kit.PNG)。
5、可以暴力猜测目标的注册邮箱，比如我猜刘韧用是[liuren@donews.com](https://web.archive.org/web/20071014204604/mailto:liuren@donews.com)邮箱注册的，而洪波用的则是[keso.hb@gmail.com](https://web.archive.org/web/20071014204604/mailto:keso.hb@gmail.com) ;)

一些不足和建议，供参考：

1、当前似乎没有办法在服务器删除数据，也就是说，只增不减；
2、数据同步不够智能化，比如我在本机删除一条信息后同步，应该考虑将服务器信息也同样删除；
3、没有办法选择同步方向；
4、密码已经保存在 365kit.dat 后修改密码，此时按同步，实际上已经登陆错误，但没有提示；
5、web 上帐户设定处密码没有用星号隐藏；
6、应该要有 PDA 上的客户端；
7、询问是否邀请其它用户加入的时间过早，至少等人用了个把星期，积累了一定数量的通讯录后再取数据啊 ;)

前两年和 [glacier](http://blog.xfocus.net/index.php?blogId=15) 玩 pda 的时候，就觉得如果能服务器备份数据，并且能够进行知识管理就酷了，后来想想，毕竟不是我们所擅长，就算了。所以，不管看好不看好，毕竟它是我们也曾经构想过的一个应用，一路走好罢。
