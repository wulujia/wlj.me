---
title: "创业笔记 329：我闹的一个 Github 双因素认证乌龙"
date: 2020-02-17T10:01:40+08:00
lastmod: 2020-02-17T10:01:40+08:00
author: "Luca"
tags: ["Startup"]
draft: false
slug: "startup-note-329"
summary: "因为安全的缘故，我打开了 Github 的双因素认证，每次在新设备登录时，需要 Google 的“身份验证器”验证一次性口令。但前段时间我犯了个错误： 切换主力手机时，在新手机上启用了“身份验证器”——这相当于重新配置了 Github 的双"
paywall: true
---

因为安全的缘故，我打开了 Github 的双因素认证，每次在新设备登录时，需要 Google 的“身份验证器”验证一次性口令。但前段时间我犯了个错误：

1. 切换主力手机时，在新手机上启用了“身份验证器”——这相当于重新配置了 Github 的双因素认证，但是在提示保存 recovery code 的时候，我想着之前保存过，就无视了；
2. 一周后觉得新手机不好用，重置了，没有备份“身份验证器”；
3. 恰好有同事因为远程办公没设备，我把自己用的笔记本电脑重置后寄给他——于是日常登录 Github 的便携设备也没了。

之后拿了一台老的 Linux，准备登录 Github 时，才发现原来手机上 Google 身份验证器的口令已经失效了（因为配置了新的，老的自动失效）——我的 Github 是公司 Github 的管理员和付费账户，挂了可有点麻烦。咨询过 Github 客服之后，得到的答复是：

Each time you disable and reconfigure 2FA, new recovery codes are generated. It’s possible you’re either using an older set of codes or you initiated the reconfiguration process, but didn't complete the setup. With either scenario, this could explain why you're running into this issue with your current recovery code file.

We can only accept the following secure verification methods, and they need to have been set up by the account owner prior to access being lost:
