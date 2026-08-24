---
title: "Brave 怎么确认我付过钱，又不知道我是谁"
date: 2026-08-24T16:26:04+08:00
lastmod: 2026-08-24T16:26:04+08:00
author: "Luca"
tags: ["security","tech"]
draft: false
slug: "brave-origin-blind-token"
---

Brave 6 月上线了 Origin，59.99 美元买断。Leo、News、Rewards、VPN、Wallet、Talk、Tor、Speedreader、Web Discovery 全部从二进制里编译掉，只留 Shields 和 Chromium 内核。Linux 免费。

我买了一个。翻文档的时候看到激活这一步的做法：Brave 的服务器没办法知道是谁在用这份授权。

它用的是盲签名。

## 常规做法是查表

付费解锁都要回答一个问题：这台设备凭什么证明自己付过钱。

一般是账号体系。你登录，服务器查表，这个 user_id 买过，放行。表里就记着某某邮箱在用 Origin、今天启动了几次。

盲签名把这张表去掉了。名字里的「盲」就是服务器闭着眼睛签——它签的时候不知道自己在签什么，签完也认不出来。

## 用数字走一遍

服务器手里有个只有它知道的私章，就当它是「乘以 7」。

我在自己电脑上随手生成一个 token，是 3。我要拿到「服务器给 3 盖过章」的证据，又不想让它知道 3 是多少。

- 我再挑一个随机数 5，把 3 乘上去：3 × 5 = 15。把 15 发过去
- 服务器盖章：15 × 7 = 105。把 105 还给我
- 我把 5 除掉：105 ÷ 5 = 21。21 正好是 3 × 7

现在我手上有一对数 (3, 21)。以后要用 premium 功能，把这两个数交出去，服务器算一下 3 × 7 是不是 21，对上了就放行。

服务器从头到尾只见过 15 和 105，没见过 3，也没见过 21。等我拿 (3, 21) 来的时候，它没办法把这次和当初签名那次对上——15 可以是任何人的 token 乘任何一个随机数得来的。

那个随机数 5 是全部的关键。它只存在我这台机器上，签完就扔。服务器少了它，就没法从 15 倒推回 3。

普通乘法当然撑不住：我拿 105 除以 15 就把 7 算出来了，之后自己在家就能给任意数字盖章。真实实现把乘法换成椭圆曲线上的运算，这个方向上除不回去。步骤一模一样。

## 二十行代码

Chaum 1982 年那版用的是 RSA，能直接跑：

```python
import random
from math import gcd

# 服务器的密钥对（教学用小素数，真实场景是 2048 位）
p, q = 1000003, 1000033
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))    # 私钥，只有服务器手里有

# 1. 浏览器在本地生成一个随机 token
token = random.randrange(2, n)

# 2. 挑一个随机数当信封，把 token 蒙起来
r = random.randrange(2, n)
while gcd(r, n) != 1:
    r = random.randrange(2, n)
blinded = token * pow(r, e, n) % n

# 3. 服务器签名。它看到的只有 blinded
blinded_sig = pow(blinded, d, n)

# 4. 浏览器把信封拆掉
sig = blinded_sig * pow(r, -1, n) % n

# 5. 之后拿 (token, sig) 去验证
print("token       =", token)
print("服务器看到的 =", blinded)
print("拆出来的签名 =", sig)
print("验证通过:", pow(sig, e, n) == token)
```

跑出来：

```
token       = 99230956405
服务器看到的 = 191161851496
拆出来的签名 = 366511550198
验证通过: True
```

`pow(r, e, n)` 是上面那个「乘以 5」，`pow(r, -1, n)` 是「除以 5」。服务器那一行只碰得到 `blinded`。

Brave 用的是椭圆曲线版本（VOPRF，可验证的不经意伪随机函数），走自家的 challenge-bypass-ristretto 库。数学换了，这五步一步不差。

## Brave 的实际流程

1. 你在 Stripe / App Store / Play Store 付款
2. 浏览器在本地生成一批随机 token
3. 盲化之后发出去，订阅服务转给 Brave 的 Challenge Bypass Server（CBR）签名，CBR 从没见过原始 token
4. CBR 返回签好的 token，附一份 DLEQ 证明
5. 浏览器验证证明，在本地解盲，得到可用的凭证

第 4 步那份证明是防一手阴的：服务器要是给每个人发不同的私章，光看章就能把人分出来，盲签名就白做了。DLEQ 证明用来说明这批签名和公开的那把公钥是同一把私钥出的，没有掉包。

凭证里只有三样东西：token 本身、一个 HMAC、一个有效期窗口。没有账号 ID，没有邮箱，没有支付信息。HMAC 把 token 绑到具体的发行方和商品上（比如 `brave.com?sku=leo-monthly`），你没法拿 Origin 的凭证去解锁 Leo。

各方看到的东西是切开的。支付方知道某某付了 59.99；订阅服务有订单数据，但看不到原始 token；CBR 看得到签发和兑换这两类事件，但连不起来。

官方文档里的说法是 decouple payment identity from service usage。

## 这套东西是 1982 年的

David Chaum 1982 年提出盲签名，比 Web 还早。他当时想做数字现金：银行能确认这张钞票是自己发的、没被花过两次，但不知道是谁在哪家店花的。

让它铺开的是 Privacy Pass。最早是 Cloudflare 的研究者推的，解决一个很具体的烦恼——Tor 和 VPN 用户老被 CAPTCHA 反复拦，因为服务器认不出他们刚刚才通过验证。Privacy Pass 让你验证一次拿到一批匿名 token，之后直接兑换通行，服务器无法把这些 token 关联到同一个人。

现在它是 IETF 标准，RFC 9576 / 9577 / 9578。Apple 叫 Private Access Tokens，Google 叫 Private State Tokens，Edge 里也有。

## 代价：他们自己也数不清设备

传统授权能做设备管理，因为服务器认得出「这是老王的第 4 台设备」。盲签名把这个能力砍掉了。Brave 分不清是你在 5 台设备上激活，还是你把购买 ID 发到群里被 50 个人用。

服务器端只剩防重放：CBR 记下已经兑换过的 token，同一个 token 换个绑定再来就返回 409 拒掉，完全相同的重放当幂等操作接受。

剩下的约束是激活的月度频率限制。设备数没有硬上限，撞到频率限制就去 account.brave.com 自助申请提额。

这只是摩擦力。你把购买 ID 发到群里，前几个人能激活，后面的等下个月。

换机器的时候没有「解绑旧设备」这一步，因为压根不存在绑定。重新激活一次就行。
