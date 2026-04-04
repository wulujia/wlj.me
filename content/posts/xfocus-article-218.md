---
title: "如何使用SSH的Port Forwarding加密不安全的服务"
date: 2001-07-08T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-218"
---

(inburst_at_263.net)

如何使用SSH的Port Forwarding加密不安全的服务


吴阿亭 Jephe


      一。简介： 


      大多数人知道SSH是用来替代R命令集，是用于加密的远程登录，文件传输，甚至加密的

      FTP(SSH2内置)， 因此SSH成为使用极广的服务之一，不仅如此，SSH还有另一项非常有

      用的功能，就是它的端口转发隧道功能，利用此功能，让一些不安全的服务象POP3，

      SMTP，FTP，LDAP等等通过SSH的加密隧道传输，然后，既然这些服务本身是不安全的，

      密码和内容是明文传送的，现在其它中间媒介也没无监听了。 


      二。图示： 


      SSH的加密隧道保护的只是中间传输的安全性，使得任何通常的嗅探工具软件无法获取发

      送内容。如下图： 

      假设客户机和服务器都运行Linux，且以POP3为例。 


           C (pop3 server: S)              S 

        _______                         ________                

        |     |                         |      |

        |     |________POP3___________ >|      |

        |_____|                         |______|

                  (图一：正常的POP3)


      (图一：正常的POP3) 


           C (pop3 server:C)               S (pop3 client: S) 

        _______                         ________                

        |     |                         |      |

        |     |--------SSH连接--------->|      |

        |_____|                         |______|

        

        

      (图二：SSH隧道后的POP3) 

      


      如图一： 正常的POP3连接是客户C向服务器S进行连接，C的设置是POP3服务器为S。 

      如图二： 用SSH隧道的话，客户C设置pop3服务器为自己(localhost)，然后设置SSH加密

      隧道 

      ，如果设置在同样的端口110听取C的请求，则对C来说，pop3服务器是自己本身，端口也

      是110 对S来说，看到的pop3请求地址不是来自C，而也是自己本身，因为有了SSH隧道。


      三。SSH隧道设置 


      1. 首先必须在C和S上安装SSH，确保SSH首先能工作。 

      2. 我们用简单的一个命令如下： 


      # ssh -C -P -f sshaccount@S -L 110:S:110 sleep 7200 


      解释如下： 

      -C 使用压缩功能，是可选的，加快速度。 


      -P 用一个非特权端口进行出去的连接。 


      -f 一旦SSH完成认证并建立port forwarding，则转入后台运行。 


      sshaccount 客户C在服务器S上的SSH连接帐号 


      -L 110:S:110 转发C对本地端口110的连接到远程服务器S的110端口。 

      也可以用高端端口(普通用户使用，因为普通用户不能在低于1024的端口上建立SSH隧道) 

      如果用高端端口，如：-L 1110:S:110,这样任何用户都可建立这种加密隧道。 


      sleep 7200 一般用于script,必须给一个命令，我们给一个sleep等待空 命令，这里为

      2小时，你可以 

      设为更长用于保持整个连接过程, 如 sleep 100000000 。 


      四。检验 


      设置后你就可以在客户C上用 # telnet localhost 110 命令而连到 S 上收取email，

      而整个过程也被加密。 


      五。其它常见问题： 


      1. 每次启动该命令时需要输入密码以验证SSH连接，你也可以用RSA键对的方法自动化

      SSH连接。 

      看文章荟萃中的另一篇文章《如何在两台linux服务器之间用RSA键对的方法SSH/SCP不需

      密码》 


      2. 如果你希望上面的命令永远保持运行状态，你可以用如下的scripts. 

      #!/bin/sh 

      while [ 1 ] ; do 

      ssh -C -P -f sshaccount@S -L 110:S:110 sleep 7200 

      sleep 1 

      done 


      3. 你可以在一个命令中用多个L 参数 ,如 -L 1110:S:110 -L 225:S:25 -L

      389:S:389 


      4. 一些windows客户端软件，象netscape mail,不能改变pop3端口号，被强迫到110，

      则你只能指定110 


      5. Linux下的fetchmail常用来自动接收邮件，可在.fetchmailrc中利用 

      preconnect参数预连接 ，指定上面的命令行。 


      6. 如果客户端是windows, 则可用tera Term pro,参考 

      [http://www.phys.washington.edu/Computing/winftpssh.html](http://www.phys.washington.edu/Computing/winftpssh.html) 


      吴阿亭 

      END
