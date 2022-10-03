#!/usr/bin/env python3
# coding: utf-8
import pygame

py_map = {
    pygame.K_LCTRL:"KEY_LEFT_CTRL",
    pygame.K_LSHIFT:"KEY_LEFT_SHIFT",
    pygame.K_LALT:"KEY_LEFT_ALT",
    pygame.K_LSUPER:"KEY_LEFT_GUI",
    pygame.K_RCTRL:"KEY_RIGHT_CTRL",
    pygame.K_RSHIFT:"KEY_RIGHT_SHIFT",
    pygame.K_RALT:"KEY_RIGHT_ALT",
    pygame.K_RSUPER:"KEY_RIGHT_GUI",
    pygame.K_UP:"KEY_UP_ARROW",
    pygame.K_DOWN:"KEY_DOWN_ARROW",
    pygame.K_LEFT:"KEY_LEFT_ARROW",
    pygame.K_RIGHT:"KEY_RIGHT_ARROW",
    pygame.K_BACKSPACE:"KEY_BACKSPACE",
    pygame.K_TAB:"KEY_TAB",
    pygame.K_RETURN:"KEY_RETURN",
    pygame.K_PAUSE:"KEY_PAUSE",
    pygame.K_ESCAPE:"KEY_ESC",
    pygame.K_INSERT:"KEY_INSERT",
    pygame.K_DELETE:"KEY_DELETE",
    pygame.K_PAGEUP:"KEY_PAGE_UP",
    pygame.K_PAGEDOWN:"KEY_PAGE_DOWN",
    pygame.K_HOME:"KEY_HOME",
    pygame.K_END:"KEY_END",
    pygame.K_NUMLOCK:"KEY_NUM_LOCK",
    pygame.K_CAPSLOCK:"KEY_CAPS_LOCK",
    pygame.K_SCROLLOCK:"KEY_SCROLL_LOCK",
    pygame.K_PRINT:"KEY_PRINT_SCREEN",
    pygame.K_F1:"KEY_F1",
    pygame.K_F2:"KEY_F2",
    pygame.K_F3:"KEY_F3",
    pygame.K_F4:"KEY_F4",
    pygame.K_F5:"KEY_F5",
    pygame.K_F6:"KEY_F6",
    pygame.K_F7:"KEY_F7",
    pygame.K_F8:"KEY_F8",
    pygame.K_F9:"KEY_F9",
    pygame.K_F10:"KEY_F10",
    pygame.K_F11:"KEY_F11",
    pygame.K_F12:"KEY_F12",
    pygame.K_KP0:"KEY_KP_0",
    pygame.K_KP1:"KEY_KP_1",
    pygame.K_KP2:"KEY_KP_2",
    pygame.K_KP3:"KEY_KP_3",
    pygame.K_KP4:"KEY_KP_4",
    pygame.K_KP5:"KEY_KP_5",
    pygame.K_KP6:"KEY_KP_6",
    pygame.K_KP7:"KEY_KP_7",
    pygame.K_KP8:"KEY_KP_8",
    pygame.K_KP9:"KEY_KP_9",
    pygame.K_KP_PERIOD:"KEY_KP_DOT",
    pygame.K_KP_DIVIDE:"KEY_KP_SLASH",
    pygame.K_KP_MULTIPLY:"KEY_KP_ASTERISK",
    pygame.K_KP_MINUS:"KEY_KP_MINUS",
    pygame.K_KP_PLUS:"KEY_KP_PLUS",
    pygame.K_KP_ENTER:"KEY_KP_ENTER",
    pygame.K_MENU:"KEY_MENU",
    1073741925:"KEY_MENU",
    }
orig_map = {"KEY_LEFT_CTRL":128,
            "KEY_LEFT_SHIFT":129,
            "KEY_LEFT_ALT":130,
            "KEY_LEFT_GUI":131,
            "KEY_RIGHT_CTRL":132,
            "KEY_RIGHT_SHIFT":133,
            "KEY_RIGHT_ALT":134,
            "KEY_RIGHT_GUI":135,
            "KEY_UP_ARROW":218,
            "KEY_DOWN_ARROW":217,
            "KEY_LEFT_ARROW":216,
            "KEY_RIGHT_ARROW":215,
            "KEY_BACKSPACE":178,
            "KEY_TAB":179,
            "KEY_RETURN":176,
            "KEY_PAUSE":208,
            "KEY_ESC":177,
            "KEY_INSERT":209,
            "KEY_DELETE":212,
            "KEY_PAGE_UP":211,
            "KEY_PAGE_DOWN":214,
            "KEY_HOME":210,
            "KEY_END":213,
            "KEY_NUM_LOCK":219,
            "KEY_CAPS_LOCK":193,
            "KEY_SCROLL_LOCK":207,
            "KEY_PRINT_SCREEN":206,
            "KEY_F1":194,
            "KEY_F2":195,
            "KEY_F3":196,
            "KEY_F4":197,
            "KEY_F5":198,
            "KEY_F6":199,
            "KEY_F7":200,
            "KEY_F8":201,
            "KEY_F9":202,
            "KEY_F10":203,
            "KEY_F11":204,
            "KEY_F12":205,
            "KEY_KP_0":234,
            "KEY_KP_1":225,
            "KEY_KP_2":226,
            "KEY_KP_3":227,
            "KEY_KP_4":228,
            "KEY_KP_5":229,
            "KEY_KP_6":230,
            "KEY_KP_7":231,
            "KEY_KP_8":232,
            "KEY_KP_9":233,
            "KEY_KP_DOT":235,
            "KEY_KP_SLASH":220,
            "KEY_KP_ASTERISK":221,
            "KEY_KP_MINUS":222,
            "KEY_KP_PLUS":223,
            "KEY_KP_ENTER":224,
            "KEY_MENU":237
            }

if __name__ == "__main__":
    import pygame.camera as camera
    from struct import pack
    import serial
    import serial.tools.list_ports as list_ports
    from copy import deepcopy as copy

    ''' Open Serial '''
    uart_port = None
    for port in list_ports.comports():
        if 'USB VID:PID=1A86:7523' in port[2]:
            uart_port = port[0]
            break
    if uart_port is None:
        print('Please insert usb-serial device!')
        exit()
    uart = serial.Serial(uart_port, 9600)
    print('Serial port', uart_port, 'opened')

    ''' Settings of PyGame '''
    pygame.init()
    pygame.display.set_caption('IP-KVM GUI')

    ''' Settings of Video Capture Device '''
    camera.init()
    cap_res_sel = 0
    cap_res     = [(800, 600), (1280, 720)]
    cap_sel     = 0
    cap_list    = copy(camera.list_cameras())
    cap_width, cap_height = cap_res[0]
    ## remove invalid devices on GNU/Linux
    from platform import system
    if system().lower() == 'linux':
        from subprocess import run
        for cap in copy(cap_list):
            dev_cap = run('v4l2-ctl -D -d {} | grep -A1 "Device Caps" |\
                    sed -n "2p" | xargs'.format(cap), capture_output=True,
                    shell=True).stdout
            if dev_cap != b'Video Capture\n':
                cap_list.remove(cap)
    if not cap_list:
        print('Please insert usb video capture device!')
        camera.quit()
        pygame.quit()
        exit()
    best_res = cap_res[dict(zip(map(lambda x: x[1], cap_res),
        range(len(cap_res))))[max(*map(lambda x: x[1], cap_res))]]
    capture = camera.Camera(cap_list[0], best_res)
    capture.start()
    print('Video capture device "(0) %s" starting' %cap_list[0])

    ''' Screen Style '''
    base_width, base_height = 240, 120
    resolution = width, height = (cap_width+base_width,
            base_height if cap_height<base_height else cap_height)
    screen = pygame.display.set_mode(resolution)
    screen.fill((40, 40, 40))

    ''' Button Style '''
    btn_color       = (51, 255, 51)
    btn_color_light = (100, 149, 104)
    btn_color_dark  = (43, 83, 41)
    width_scale     = 0.8
    height_scale    = 0.5
    btn_num         = 6
    btn_width       = base_width*width_scale
    btn_height      = height/btn_num*height_scale
    shift           = (base_width-btn_width)/2
    merge           = height/btn_num*(1-height_scale)/2

    btn_pos = {'res':    (cap_width+shift, merge),
               'cap':    (cap_width+shift, height/btn_num+merge),
               'pwr':    (cap_width+shift, 2*height/btn_num+merge),
               'rst':    (cap_width+shift, 3*height/btn_num+merge),
               'lpwr':   (cap_width+shift, 4*height/btn_num+merge),
               'c_a_del':(cap_width+shift, 5*height/btn_num+merge)}

    ''' Text Style '''
    txt = {'res':'{}x{}'.format(*cap_res[0]),
           'cap':'Alt Video',
           'pwr':'Short Power',
           'rst': 'Reset',
           'lpwr': 'Long Power',
           'c_a_del':'Ctrl+Alt+Del'}
    txt_scale = 0.26
    txt_size = int(btn_height*txt_scale)

    font = pygame.font.SysFont('serif', txt_size)
    res_text     = font.render(txt['res'], True, btn_color)
    cap_text     = font.render(txt['cap'], True, btn_color)
    pwr_text     = font.render(txt['pwr'], True, btn_color)
    rst_text     = font.render(txt['rst'], True, btn_color)
    lpwr_text    = font.render(txt['lpwr'], True, btn_color)
    c_a_del_text = font.render(txt['c_a_del'], True, btn_color)

    txt_merge = (btn_height-font.size(txt['pwr'])[1])/2

    txt_pos = {
    'res':
       (cap_width+shift+(btn_width-font.size(txt['res'])[0])/2,
        merge+txt_merge),
    'cap':
       (cap_width+shift+(btn_width-font.size(txt['cap'])[0])/2,
        height/btn_num+merge+txt_merge),
    'pwr':
       (cap_width+shift+(btn_width-font.size(txt['pwr'])[0])/2,
        2*height/btn_num+merge+txt_merge),
    'rst':
       (cap_width+shift+(btn_width-font.size(txt['rst'])[0])/2,
        3*height/btn_num+merge+txt_merge),
    'lpwr':
       (cap_width+shift+(btn_width-font.size(txt['lpwr'])[0])/2,
        4*height/btn_num+merge+txt_merge),
    'c_a_del':
       (cap_width+shift+(btn_width-font.size(txt['c_a_del'])[0])/2,
        5*height/btn_num+merge+txt_merge)}

    while True:
        mouse = pygame.mouse.get_pos()

        ''' Refresh Screen '''
        if (    btn_pos['res'][0] <= mouse[0] <= btn_pos['res'][0]+btn_width and
                btn_pos['res'][1] <= mouse[1] <= btn_pos['res'][1]+btn_height):
            pygame.draw.rect(screen, btn_color_light,
                    [btn_pos['res'][0], btn_pos['res'][1], btn_width, btn_height])
        else:
            pygame.draw.rect(screen, btn_color_dark,
                    [btn_pos['res'][0], btn_pos['res'][1], btn_width, btn_height])

        if (    btn_pos['cap'][0] <= mouse[0] <= btn_pos['cap'][0]+btn_width and
                btn_pos['cap'][1] <= mouse[1] <= btn_pos['cap'][1]+btn_height):
            pygame.draw.rect(screen, btn_color_light,
                    [btn_pos['cap'][0], btn_pos['cap'][1], btn_width, btn_height])
        else:
            pygame.draw.rect(screen, btn_color_dark,
                    [btn_pos['cap'][0], btn_pos['cap'][1], btn_width, btn_height])

        if (    btn_pos['pwr'][0] <= mouse[0] <= btn_pos['pwr'][0]+btn_width and
                btn_pos['pwr'][1] <= mouse[1] <= btn_pos['pwr'][1]+btn_height):
            pygame.draw.rect(screen, btn_color_light,
                    [btn_pos['pwr'][0], btn_pos['pwr'][1], btn_width, btn_height])
        else:
            pygame.draw.rect(screen, btn_color_dark,
                    [btn_pos['pwr'][0], btn_pos['pwr'][1], btn_width, btn_height])

        if (    btn_pos['rst'][0] <= mouse[0] <= btn_pos['rst'][0]+btn_width and
                btn_pos['rst'][1] <= mouse[1] <= btn_pos['rst'][1]+btn_height):
            pygame.draw.rect(screen, btn_color_light,
                    [btn_pos['rst'][0], btn_pos['rst'][1], btn_width, btn_height])
        else:
            pygame.draw.rect(screen, btn_color_dark,
                    [btn_pos['rst'][0], btn_pos['rst'][1], btn_width, btn_height])

        if (    btn_pos['lpwr'][0] <= mouse[0] <= btn_pos['lpwr'][0]+btn_width and
                btn_pos['lpwr'][1] <= mouse[1] <= btn_pos['lpwr'][1]+btn_height):
            pygame.draw.rect(screen, btn_color_light,
                    [btn_pos['lpwr'][0], btn_pos['lpwr'][1], btn_width, btn_height])
        else:
            pygame.draw.rect(screen, btn_color_dark,
                    [btn_pos['lpwr'][0], btn_pos['lpwr'][1], btn_width, btn_height])

        if (    btn_pos['c_a_del'][0] <= mouse[0] <= btn_pos['c_a_del'][0]+btn_width and
                btn_pos['c_a_del'][1] <= mouse[1] <= btn_pos['c_a_del'][1]+btn_height):
            pygame.draw.rect(screen, btn_color_light,
                    [btn_pos['c_a_del'][0], btn_pos['c_a_del'][1], btn_width, btn_height])
        else:
            pygame.draw.rect(screen, btn_color_dark,
                    [btn_pos['c_a_del'][0], btn_pos['c_a_del'][1], btn_width, btn_height])

        screen.blit(res_text, (txt_pos['res'][0], txt_pos['res'][1]))
        screen.blit(cap_text, (txt_pos['cap'][0], txt_pos['cap'][1]))
        screen.blit(pwr_text, (txt_pos['pwr'][0], txt_pos['pwr'][1]))
        screen.blit(rst_text, (txt_pos['rst'][0], txt_pos['rst'][1]))
        screen.blit(lpwr_text, (txt_pos['lpwr'][0], txt_pos['lpwr'][1]))
        screen.blit(c_a_del_text, (txt_pos['c_a_del'][0], txt_pos['c_a_del'][1]))

        cap_img = pygame.transform.scale(capture.get_image(), cap_res[cap_res_sel])
        screen.blit(cap_img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            ''' Close Window '''
            if event.type == pygame.QUIT:
                capture.stop()
                camera.quit()
                pygame.quit()
                exit()

            ''' Button Trigger '''
            if event.type == pygame.MOUSEBUTTONDOWN:
                ''' Resize GUI to preset resolution '''
                if (    btn_pos['res'][0] <= mouse[0] <= btn_pos['res'][0]+btn_width and
                        btn_pos['res'][1] <= mouse[1] <= btn_pos['res'][1]+btn_height):
                    cap_res_sel = (cap_res_sel + 1) % len(cap_res)
                    cap_width, cap_height = cap_res[cap_res_sel]
                    resolution = width, height = (cap_width+base_width,
                            base_height if cap_height<base_height else cap_height)
                    screen = pygame.display.set_mode(resolution)
                    screen.fill((40, 40, 40))
                    btn_pos = {'res':    (cap_width+shift, merge),
                               'cap':    (cap_width+shift, height/btn_num+merge),
                               'pwr':    (cap_width+shift, 2*height/btn_num+merge),
                               'rst':    (cap_width+shift, 3*height/btn_num+merge),
                               'lpwr':   (cap_width+shift, 4*height/btn_num+merge),
                               'c_a_del':(cap_width+shift, 5*height/btn_num+merge)}
                    txt_pos = {
                    'res':
                       (cap_width+shift+(btn_width-font.size(txt['res'])[0])/2,
                        merge+txt_merge),
                    'cap':
                       (cap_width+shift+(btn_width-font.size(txt['cap'])[0])/2,
                        height/btn_num+merge+txt_merge),
                    'pwr':
                       (cap_width+shift+(btn_width-font.size(txt['pwr'])[0])/2,
                        2*height/btn_num+merge+txt_merge),
                    'rst':
                       (cap_width+shift+(btn_width-font.size(txt['rst'])[0])/2,
                        3*height/btn_num+merge+txt_merge),
                    'lpwr':
                       (cap_width+shift+(btn_width-font.size(txt['lpwr'])[0])/2,
                        4*height/btn_num+merge+txt_merge),
                    'c_a_del':
                       (cap_width+shift+(btn_width-font.size(txt['c_a_del'])[0])/2,
                        5*height/btn_num+merge+txt_merge)}
                    txt['res'] = '{}x{}'.format(*cap_res[cap_res_sel])
                    res_text = font.render(txt['res'], True, btn_color)

                ## Alternates video capture device
                elif (  btn_pos['cap'][0] <= mouse[0] <= btn_pos['cap'][0]+btn_width and
                        btn_pos['cap'][1] <= mouse[1] <= btn_pos['cap'][1]+btn_height):
                    capture.stop()
                    cap_sel = (cap_sel + 1) % len(cap_list)
                    capture = camera.Camera(cap_list[cap_sel], best_res)
                    capture.start()
                    print('Change to "({}) {}" Video capture device'.format(cap_sel, cap_list[cap_sel]))

                ### Send short power command to promicro
                elif (  btn_pos['pwr'][0] <= mouse[0] <= btn_pos['pwr'][0]+btn_width and
                        btn_pos['pwr'][1] <= mouse[1] <= btn_pos['pwr'][1]+btn_height):
                    print("trigger short power button")
                    uart.write(b'\xfd')

                ## Send reset command to promicro
                elif (  btn_pos['rst'][0] <= mouse[0] <= btn_pos['rst'][0]+btn_width and
                        btn_pos['rst'][1] <= mouse[1] <= btn_pos['rst'][1]+btn_height):
                    print("trigger reset button")
                    uart.write(b'\xfe')

                ## Send long power command to promicro
                elif (  btn_pos['lpwr'][0] <= mouse[0] <= btn_pos['lpwr'][0]+btn_width and
                        btn_pos['lpwr'][1] <= mouse[1] <= btn_pos['lpwr'][1]+btn_height):
                    print("trigger long power button")
                    uart.write(b'\xff')

                ## Send Ctrl+Alt+Delete keyboard command to promicro
                elif (  btn_pos['c_a_del'][0] <= mouse[0] <= btn_pos['c_a_del'][0]+btn_width and
                        btn_pos['c_a_del'][1] <= mouse[1] <= btn_pos['c_a_del'][1]+btn_height):
                    print("Send Ctrl+Alt+Delete command")
                    uart.write(pack("!BBBBBBBBBBBB",
                        1, orig_map['KEY_LEFT_CTRL'],
                        1, orig_map['KEY_LEFT_ALT'],
                        1, orig_map['KEY_DELETE'],
                        0, orig_map['KEY_LEFT_CTRL'],
                        0, orig_map['KEY_LEFT_ALT'],
                        0, orig_map['KEY_DELETE']))


            ''' KeyBoard Emulator '''
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                if event.type == pygame.KEYUP:
                    press = False
                else:
                    press = True

                if event.key in py_map:
                    key = orig_map[py_map[event.key]]
                    print("{} {} ({})".format("Pressed" if press else "Released", py_map[event.key], key))
                elif event.key in range(0, 256):
                    key = event.key
                    print("{} {} ({})".format("Pressed" if press else "Released", chr(key), key))
                else:
                    print("{} an invalid key {}".format("Pressed" if press else "Released", event.key))
                    continue

                uart.write(pack("!BB", 1 if press else 0, key))
