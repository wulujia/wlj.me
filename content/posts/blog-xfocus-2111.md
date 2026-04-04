---
title: "Vista里的数据安全功能"
date: 2006-09-30T00:00:00+08:00
tags: ["Startup"]
draft: false
slug: "blog-xfocus-2111"
---

一直听人说将要发布的Vista中已经包含了较为完善的数据安全功能，也有几位朋友提醒过，在微软这个巨人将要介入的市场，千万要小心行事。以前装过一次Vista，测试了几天就卸载了，没太注意数据安全的功能，今天特地上微软的网上搜索一番。

> [Vista安全相关网址](http://www.microsoft.com/technet/windowsvista/security/default.mspx)
> 
>   [Microsoft? Windows Vista? Security Advancements](http://download.microsoft.com/download/c/2/9/c2935f83-1a10-4e4a-a137-c1db829637f5/WindowsVistaSecurityWP.doc)
其中提到了在数据安全方面微软采取的措施主要有四项：

> BitLocker Drive Encryption
> 
>   Integrated Rights Management Services Client
> 
>   Encrypting File System Enhancements
> 
>   USB Device Control
比较有影响是的第二项，微软在将RMS的客户端内置到Vista中，在一个已经预先全部部署过Vista系统的环境中，RMS的实施成本将大大降低……

> Many organizations are already using Microsoft’s Right
> Management Services (RMS) technology, which helps protect the security
> and integrity of sensitive information by making documents accessible
> only to authorized users, and by enforcing specific policies around
> forwarding, printing and sharing by those users.
> 
> Previous versions of Windows required the installation of additional
> components to enable this functionality. Windows Vista includes an
> integrated RMS client that helps further safeguard digital information.
> For businesses, this saves on deployment costs and ensures consistent
> application of usage policies. For end users, this means being able to
> work with RMS-protected documents without having to install or
> configure any additional software.
> 
> RMS also helps enterprise customers further control and protect their
> information by providing smart card integration and longer encryption
> key lengths. The Windows Server “Longhorn” release will introduce the
> integration of RMS with Active Directory Federation Services to support
> cross-company protected collaboration. This capability will allow
> companies to share sensitive information among themselves and with
> business partners, protected by the same mechanism that they now use to
> protect their internal information.
> 
> In addition, RMS is now integrated with the WinFX? APIs and the new XML
> Paper Specification (XPS) format — an open, cross-platform document
> format that helps customers effortlessly create, share, print, archive
> and protect rich digital documents. With a new print driver that
> outputs XPS, any application can produce XPS documents that can be
> protected with RMS. This basic functionality will significantly broaden
> the range of information that can be protected by RMS.
> 
> The 2007 Microsoft Office system provides even deeper integration with
> RMS through new developments in Microsoft SharePoint?. SharePoint
> administrators can set access policies for the SharePoint document
> libraries on a per-user basis that will be inherited by RMS policies.
> This means that users who have “view-only” rights to access the content
> will have that “view-only” access (no print, copy or paste) enforced by
> RMS, even when the document has been removed from the SharePoint site.
> Enterprise customers can set usage policies that are enforced not only
> when the document is at rest, but also when the information is outside
> the direct control of the enterprise.
不过还好，RMS和VISTA高昂的价格会令大多数人望而却步。尤其是在国内，盗版Office和Windows流行的环境下，一般企业要采用RMS，可能付出的代价，可能甚至会超过他们单位所有的网络/电脑硬件成本。
