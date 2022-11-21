# 准备
## 硬件
- 键盘模拟
  - promicro，基于ATmega32U4芯片
  - USB转TTL模块(如CH340g)
- 画面采集
  - USB采集卡
- 机箱电源按钮模拟
  - 同键盘模拟需要的配件
  - PC817光耦
  - 面包板一块
  - 1k ohm电阻若干
  - 杜邦线若干
## 软件
- Python3，安装PyGame和pySerial库，用于运行main.py
- Arduino IDE，用于写入kvm.ino程序到promicro
- 如果系统使用Gnu/Linux，需要安装指令v4l2-ctl  
比如Debian使用指令`sudo apt install v4l-utils`安装
## promicro连接示意图
<img src="https://github.com/evilwarrior/ip-kvm/blob/main/Sketch.png" width="50%">

# 说明
iKVM的半解决方案，能够将x86/arm设备转化为KVM设备  
只需要在设备上再安装桌面和远程桌面服务就能变成完整的iKVM  
kvm.ino是写入到promicro的程序，可以做到键盘模拟及机箱电源按钮模拟，同时允许原来的机箱按键生效  
main.py可以采集被控主机画面以及发送键盘指令和电源控制指令到promicro
