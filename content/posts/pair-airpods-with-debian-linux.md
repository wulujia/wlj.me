---
title: "pair Airpods with Debian Linux"
date: 2024-01-01T00:00:00+08:00
tags: ["Tips"]
draft: false
slug: "pair-airpods-with-debian-linux"
---

If you can't pair Airpods 2 with Debian 12, try this:

1. install some software: pulseaudio, bluez

2. run in terminal:

```
bluetoothctl
scan on
```

find your Airpods Mac Address.

3. pair

in bluetoothctl, type:

```
pair <MAC address>
```

if need PIN, The default PIN for AirPods is 0000.
