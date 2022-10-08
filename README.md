# 准备

硬件

promicro，基于ATmega32U4芯片

PC817光耦

USB转TTL模块(如CH340g)

面包板一块

1k ohm电阻若干

杜邦线若干

软件

Python3，安装PyGame和pySerial库，用于运行main.py

Arduino IDE，用于写入kvm.ino程序到promicro

如果系统使用Gnu/Linux，需要安装指令v4l2-ctl

比如Debian使用下面的指令安装

`sudo apt install v4l-utils`

![promicro连接示意图](https://github.com/evilwarrior/ip-kvm/blob/main/Sketch.png)

# 说明

kvm.ino是写入到promicro的程序，可以做到键盘模拟及ATX电源按键模拟，同时允许原来的电源按键生效

main.py可以采集被控主机画面以及发送键盘指令和电源控制指令到promicro
