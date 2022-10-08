# 准备

硬件

promicro，基于ATmega32U4芯片

PC817光耦

USB转TTL模块(如CH340g)

1k ohm电阻若干

杜邦线若干

软件

Python3，安装PyGame和pySerial库，用于运行main.py

Arduino IDE，用于写入kvm.ino程序到promicro

![promicro连接示意图](https://github.com/evilwarrior/ip-kvm/blob/main/Sketch.png)

# 说明

kvm.ino是写入到promicro的程序，可以做到键盘模拟及ATX电源按键模拟，同时允许原来的电源按键生效

main.py可以采集被控主机画面以及发送键盘指令和电源控制指令到promicro
