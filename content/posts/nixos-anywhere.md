---
title: "nixos-anywhere：一条命令把远程 Linux 装成 NixOS"
date: 2026-08-25T17:18:44+08:00
lastmod: 2026-08-25T17:18:44+08:00
author: "Luca"
tags: ["Tools","Ops","NixOS"]
draft: false
slug: "nixos-anywhere"
---

装 NixOS 通常要做安装 U 盘，进安装环境，手动分区，手动装。云主机更麻烦，很多厂商没有 NixOS 镜像，只给 Debian、Ubuntu。

nixos-anywhere 解决的就是这件事。只要一台机器能 SSH 登录，它就能远程把机器上的 Linux 换成 NixOS。不用 U 盘，不用控制台，不用厂商支持。

## 它怎么做到的

靠的是 Linux 的 kexec。kexec 能跳过硬件重启，直接把内存里正在跑的内核换成另一个。nixos-anywhere 用它做四步：

1. SSH 登进目标机器，下载一个很小的 NixOS 安装环境，用 kexec 切换过去。原来的系统被踢出内存，机器现在跑在一个纯内存的 NixOS 安装盘里。
2. 按你写的分区文件给硬盘分区、格式化、挂载。这一步交给 disko 做，disko 是一个用配置文件描述磁盘布局的工具。
3. 把你定义好的 NixOS 系统传到机器上，装进硬盘。
4. 重启。机器起来就是 NixOS。

## 要准备什么

本机：

- 装了 Nix，开了 flakes
- 一个 flake，里面定义了目标机器的 NixOS 配置
- 一个 disko 分区文件

目标机器：

- 跑着任意 Linux，x86_64 或 aarch64
- 能用 root 或免密 sudo 的用户 SSH 登录
- 内存 1GB 以上，安装环境要在内存里跑
- 支持 kexec。多数虚拟机和物理机都支持，OpenVZ、LXC 这类容器不支持

## 一个完整的例子

flake.nix：

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    disko.url = "github:nix-community/disko";
    disko.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { nixpkgs, disko, ... }: {
    nixosConfigurations.web = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        disko.nixosModules.disko
        ./disk-config.nix
        ./configuration.nix
      ];
    };
  };
}
```

disk-config.nix，一块盘，一个启动分区加一个根分区：

```nix
{
  disko.devices.disk.main = {
    device = "/dev/sda";
    type = "disk";
    content = {
      type = "gpt";
      partitions = {
        ESP = {
          size = "500M";
          type = "EF00";
          content = {
            type = "filesystem";
            format = "vfat";
            mountpoint = "/boot";
            mountOptions = [ "umask=0077" ];
          };
        };
        root = {
          size = "100%";
          content = {
            type = "filesystem";
            format = "ext4";
            mountpoint = "/";
          };
        };
      };
    };
  };
}
```

configuration.nix 至少要写引导程序，加一条装完能拿到 root 的路。最简单的是把 SSH 公钥配在 root 下：

```nix
{
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  services.openssh.enable = true;
  users.users.root.openssh.authorizedKeys.keys = [
    "ssh-ed25519 AAAA... you@laptop"
  ];
  system.stateVersion = "26.05";
}
```

如果你想用普通用户登录、sudo 提权，那这个用户要进 `wheel` 组，并且要么给他设密码，要么让 sudo 免密：

```nix
{
  users.users.luca = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    openssh.authorizedKeys.keys = [ "ssh-ed25519 AAAA... you@laptop" ];
  };
  security.sudo.wheelNeedsPassword = false;
}
```

然后一条命令：

```bash
nix run github:nix-community/nixos-anywhere -- \
  --flake .#web \
  --target-host root@1.2.3.4
```

装完后目标机器的 SSH 主机密钥变了，再登录会报错。把 `~/.ssh/known_hosts` 里那台机器的旧记录删掉就行。

## 常用开关

物理机装之前先生成硬件配置，不然网卡、显卡驱动可能缺：

```bash
--generate-hardware-config nixos-generate-config ./hardware-configuration.nix
```

先在本地虚拟机里试一遍分区和系统能不能起来，不碰真机：

```bash
--vm-test
```

目标机器配置低，系统在本机编译好再传过去：

```bash
--build-on local
```

内存只有 1GB 左右的机器，少传一些分区工具的依赖，省内存：

```bash
--no-disko-deps
```

装完后往新系统里放文件，比如 SSH 主机密钥、密钥文件：

```bash
--extra-files ./files
```

保留目标机器原来的 SSH 主机密钥，省掉改 known_hosts：

```bash
--copy-host-keys
```

系统配坏了想重装但不动数据，分区模式改成只挂载不格式化：

```bash
--disko-mode mount
```

## 坑

- 分区文件里的 `device` 写错盘，会把错的盘格掉。先 `lsblk` 看清楚，或者用 `/dev/disk/by-id/` 下的名字。
- 装完要能提权。普通用户只配了公钥、没设密码，sudo 默认要密码，root 又没配公钥——这台机器上就没人能变成 root，sudo、su、passwd 全都过不去。要么公钥配给 root，要么 `security.sudo.wheelNeedsPassword = false`，要么给用户设密码。装完第一条命令先跑 `sudo whoami`。
- 已经锁死了的救法：重启进引导菜单按 `e`，内核参数加 `init=/bin/sh`，进去后 `mount -o remount,rw /`，`passwd 用户名`。这条路要求控制台在手。
- 安装环境跑在内存里，内存小的机器传大系统会内存不足。先试 `--build-on local` 和 `--no-disko-deps`。
- 改了分区文件，先跑 `--vm-test`，比在真机上格错盘便宜。
