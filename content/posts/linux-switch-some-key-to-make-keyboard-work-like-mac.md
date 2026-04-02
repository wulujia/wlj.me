---
title: "Linux switch some key to make keyboard work like Mac"
date: 2024-05-23T22:43:00+08:00
tags: ["Tools"]
draft: false
slug: "linux-switch-some-key-to-make-keyboard-work-like-mac"
---

System -> Preferences -> Keyboard Shortcuts -> Custom

Ctrl + C / Ctrl + V / Ctrl + X / Ctrl + A, Change Ctrl to Alt

```
xte "keyup Alt_L" "keyup Alt_R" "keyup c" "keydown Control_L" "key c" "keyup Control_L"
xte "keyup Alt_L" "keyup Alt_R" "keyup v" "keydown Control_L" "key v" "keyup Control_L"
xte "keyup Alt_L" "keyup Alt_R" "keyup x" "keydown Control_L" "key x" "keyup Control_L"
xte "keyup Alt_L" "keyup Alt_R" "keyup a" "keydown Control_L" "key a" "keyup Control_L"
```

In Chrome, Ctrl + T / Ctrl + W / Ctrl + R / Ctrl + L, Change Ctrl to Alt

```
xte "keyup Alt_L" "keyup Alt_R" "keyup t" "keydown Control_L" "key t" "keyup Control_L"
xte "keyup Alt_L" "keyup Alt_R" "keyup w" "keydown Control_L" "key w" "keyup Control_L"
xte "keyup Alt_L" "keyup Alt_R" "keyup r" "keydown Control_L" "key r" "keyup Control_L"
xte "keyup Alt_L" "keyup Alt_R" "keyup l" "keydown Control_L" "key l" "keyup Control_L"
```

System -> Preferences -> Keyboard Shortcuts -> Typing

Switch language input from Meta + space to Ctrl + space
