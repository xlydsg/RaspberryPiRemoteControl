# pylint: disable=no-member
# -*- coding: utf-8 -*
# 上述注释能够忽略在vscode中出现 "Module * has no * member"的报错
# 但是该报错实际上并不会对运行造成影响

import sys
import cv2
import numpy as np
import pygame
import serial
import copy

import time
from py_class.button import Button
import ctrl_func

window_size = {}
window_size['window_W'] = 1280
# 临时更改了窗口高度，适应电脑分辨率，原值为720
window_size['window_L'] = 620
# 设置控制栏高度
window_size['control_L'] = 100

window_W = window_size['window_W']
window_L = window_size['window_L']
control_L = window_size['control_L']

def main():
    """
    主要函数，设置窗口参数，并包含大循环
    """


    # 初始化pygame，所有和pygame相关的内容清放在该部分之后，以免因为未初始化而报错
    pygame.init()

    # 将VideoCapture参数改为0能够在没有视频输入的时候使用笔记本摄像头，从而避免报错
    # 正常使用过程中参数为2
    camera = cv2.VideoCapture(0)
    camera.set(3, window_W)
    camera.set(4, window_L)
    
    
    # pygame参数设置
    screen = pygame.display.set_mode((window_W, window_L + control_L))
    pygame.display.set_caption("HDMICapture")
    pygame.event.set_grab(False)

    ### gui设置
    # 初始化按键
    manager_button = Button(screen, 'Hello World', 32, keyvalue = 0x05, modvalue = 0x4c)
    ###


    while True:
        for event in pygame.event.get():
            
            # pygame检测到退出
            if event.type == pygame.QUIT:
                sys.exit(0)

            # pygame检测到键盘按下
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.set_grab(not(pygame.event.get_grab()))

                # 在终端打印串口发送的信息
                if event.key != pygame.K_LSHIFT:
                    print(bytes.fromhex(ctrl_func.ch9329_kbencode(pygkey_to_code(event.key),0)))
                    # ser.write(bytes.fromhex(ch9329_kbencode(pygkey_to_code(event.key),0)))

            # pygame检测到按键抬起
            elif event.type == pygame.KEYUP:
                pass
                # ser.write(bytes.fromhex("57AB00020800000000000000000C"))
                # ser.write("57AB00020800000000000000000C" )

            # pygame检测鼠标位置
            elif event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                print('Mouse position: (' + str(event.pos[0]) + ', ' + str(event.pos[1]) + ')')

                pos_str = ctrl_func.ch9329_msencode(event.pos[0], event.pos[1], window_size)
                # ser.write(bytes.fromhex(pos_str))
                print(pos_str)
                # if pygame.event.get_grab():
                #     pygame.mouse.set_pos(window_W/2,window_W/2)

            # pygame检测鼠标按键按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标按下的位置是否在manager_button之中
                ctrl_func.check_button(manager_button, mouse_x, mouse_y)
                if manager_button.stats:
                    comb_kb_data = ctrl_func.ch9329_kbencode(manager_button.keyvalue, manager_button.modvalue)
                    print(comb_kb_data)
                    # 需要将stats改为False以便下一次检测
                    manager_button.stats = False

                if event.button == 1:
                    print("You pressed the left mouse button")
                    # ser.write(bytes.fromhex("57ab00050501010000000E"))
                elif event.button == 2:
                    print("You pressed the middle mouse button")
                    # ser.write(bytes.fromhex("57ab000505010400000011"))
                elif event.button == 3:
                    print("You pressed the right mouse button")
                    # ser.write(bytes.fromhex("57ab00050501020000000f"))
                elif event.button == 4:
                    print("You up")
                    # ser.write(bytes.fromhex("57ab00050501000000010E"))
                elif event.button == 5:
                    print("You down")
                    # ser.write(bytes.fromhex("57ab00050501000000ff0c"))
            elif event.type == pygame.MOUSEBUTTONUP:
                # print("57ab00050501000000000D")
                # ser.write(bytes.fromhex("57ab00050501000000000D"))
                if event.button == 1:
                    print("You released the left mouse button")
                elif event.button == 2:
                    print("You released the middle mouse button")
                elif event.button == 3:
                    print("You released the right mouse button")
                elif event.button == 4:
                    print("You up")
                elif event.button == 5:
                    print("You down")
        
        ### 交互界面相关操作
        manager_button.draw_button()
        # ctrl_func.check_button(manager_button.stats, manager_button, mouse_x, mouse_y)
        # if manager_button.stats:
        #     print("Hello World")
        #     manager_button.stats = False
        ###
        
        ret, frame = camera.read()
        del ret
        # ret有实际的用途吗？必须存在两个参数吗？
        # 如果必须存在两个参数但是又没有使用到的话，通过del删除该变量

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0,1)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
        pygame.display.flip()
        
        # 时间暂停一段时间，限制刷新率
        time.sleep(0.3)

        # count = ser.inWaiting()
        # if count != 0:
        #     recv = ser.read(count)
        #     print(recv)
        # ser.flushInput()

        # ser.write(bytes.fromhex("57ab00050501020000000F"))
        # ser.write(bytes.fromhex("57ab00050501000000000D"))

def pygkey_mod(mod):
    """
    组合键
    """
    modvalue = {
        pygame.KMOD_NONE     :0,
        pygame.KMOD_LSHIFT   :0x02,
        pygame.KMOD_RSHIFT   :0x20,
        pygame.KMOD_SHIFT    :0x02,
        pygame.KMOD_LCTRL    :0x01,
        pygame.KMOD_RCTRL    :0x10,
        pygame.KMOD_CTRL     :0x01,
        pygame.KMOD_LALT     :0x04,
        pygame.KMOD_RALT     :0x40,
        pygame.KMOD_ALT      :0x04,
        pygame.KMOD_LMETA    :0x80,
        pygame.KMOD_RMETA    :0x08,
        pygame.KMOD_META     :0x08,
        pygame.KMOD_CAPS     :0x02,
        pygame.KMOD_NUM      :0x00,
        pygame.KMOD_MODE     :0x00
    }

    return modvalue.get(mod,0)

def pygkey_to_code(key):
    """
    将除控制键之外的普通按键进行映射
    """

    # 将一般按键映射到对应的按键，用于获得按下了什么按键
    keyvalue = {
        pygame.K_BACKSPACE  :'back_space',   
        pygame.K_TAB        :'tab',
        pygame.K_CLEAR      :'',
        pygame.K_RETURN     :'',
        pygame.K_PAUSE      :'pause',
        pygame.K_ESCAPE     :'esc',
        pygame.K_SPACE       :'space',       
        pygame.K_EXCLAIM     :'',
        pygame.K_QUOTEDBL   :'',
        pygame.K_HASH       :'',
        pygame.K_DOLLAR     :'',
        pygame.K_AMPERSAND :'',
        pygame.K_QUOTE        :"'",   
        pygame.K_LEFTPAREN  :'',
        pygame.K_RIGHTPAREN  :'',
        pygame.K_ASTERISK    :'',
        pygame.K_PLUS      :'',
        pygame.K_COMMA      :',',
        pygame.K_MINUS      :'-',
        pygame.K_PERIOD     :'.',
        pygame.K_SLASH     :'/',
        pygame.K_0          :'0',
        pygame.K_1          :'1',
        pygame.K_2          :'2',
        pygame.K_3           :'3',
        pygame.K_4          :'4',
        pygame.K_5        :'5',
        pygame.K_6          :'6',
        pygame.K_7          :'7',
        pygame.K_8          :'8',
        pygame.K_9          :'9',
        pygame.K_COLON      :'',
        pygame.K_SEMICOLON   :';',
        pygame.K_LESS        :'',
        pygame.K_EQUALS      :'=',
        pygame.K_GREATER    :'',
        pygame.K_QUESTION   :'',
        pygame.K_AT         :'',
        pygame.K_LEFTBRACKET :'[',
        pygame.K_BACKSLASH   :'keycode_29',
        pygame.K_RIGHTBRACKET :']',
        pygame.K_CARET       :'',
        pygame.K_UNDERSCORE  :'',
        pygame.K_BACKQUOTE   :"`",
        pygame.K_a          :'a',
        pygame.K_b          :'b',
        pygame.K_c          :'c',
        pygame.K_d           :'d',
        pygame.K_e           :'e',
        pygame.K_f          :'f',
        pygame.K_g           :'g',
        pygame.K_h          :'h',
        pygame.K_i         :'i',
        pygame.K_j         :'j',
        pygame.K_k          :'k',
        pygame.K_l           :'l',
        pygame.K_m          :'m',
        pygame.K_n           :'n',
        pygame.K_o          :'o',
        pygame.K_p          :'p',
        pygame.K_q          :'q',
        pygame.K_r         :'r',
        pygame.K_s          :'s',
        pygame.K_t          :'t',
        pygame.K_u         :'u',
        pygame.K_v         :'v',
        pygame.K_w           :'w',
        pygame.K_x          :'x',
        pygame.K_y          :'y',
        pygame.K_z          :'z',
        pygame.K_DELETE         :'delete',    
        pygame.K_KP0                :'pad_0', 
        pygame.K_KP1               :'pad_1',
        pygame.K_KP2                :'pad_2',
        pygame.K_KP3                :'pad_3',
        pygame.K_KP4                :'pad_4',
        pygame.K_KP5                :'pad_5',
        pygame.K_KP6                 :'pad_6',
        pygame.K_KP7                :'pad_7',
        pygame.K_KP8                :'pad_8',
        pygame.K_KP9                :'pad_9',
        pygame.K_KP_PERIOD   :'pad_.',
        pygame.K_KP_DIVIDE   :'pad_/',
        pygame.K_KP_MULTIPLY :'pad_*',
        pygame.K_KP_MINUS   :'pad_-',
        pygame.K_KP_PLUS   :'pad_+',
        pygame.K_KP_ENTER   :'enter_r',
        pygame.K_KP_EQUALS  :'=',
        pygame.K_UP             :'up_arrow',    
        pygame.K_DOWN             :'down_arrow',
        pygame.K_RIGHT            :'right_arrow',
        pygame.K_LEFT              :'left_arrow',
        pygame.K_INSERT              :'insert',
        pygame.K_HOME                :'home',
        pygame.K_END               :'end',
        pygame.K_PAGEUP            :'page_up',
        pygame.K_PAGEDOWN           :'page_down',
        pygame.K_F1                :'f1',
        pygame.K_F2                 :'f2',
        pygame.K_F3               :'f3',
        pygame.K_F4                 :'f4',
        pygame.K_F5                 :'f5',
        pygame.K_F6                :'f6',
        pygame.K_F7                 :'f7',
        pygame.K_F8               :'f8',
        pygame.K_F9                  :'f9',
        pygame.K_F10                :'f10',
        pygame.K_F11                 :'f11',
        pygame.K_F12                :'f12',
        pygame.K_F13                 :'f13',
        pygame.K_F14                :'f14',
        pygame.K_F15              :'f15',
        pygame.K_NUMLOCK           :'num_lock',
        pygame.K_CAPSLOCK            :'caps_lock',
        pygame.K_SCROLLOCK        :'scroll_lock',
        pygame.K_RSHIFT           :'shift_r',
        pygame.K_LSHIFT           :'shift_l',
        pygame.K_RCTRL            :'ctrl_r',
        pygame.K_LCTRL               :'ctrl_l',
        pygame.K_RALT               :'alt_r',
        pygame.K_LALT             :'alt_l',
        pygame.K_RMETA              :'',
        pygame.K_LMETA            :'',
        pygame.K_LSUPER             :'l_win',
        pygame.K_RSUPER            :'r_win',
        pygame.K_MODE              :'',
        pygame.K_HELP                :'',
        pygame.K_PRINT             :'print_screen',
        pygame.K_SYSREQ            :'',
        pygame.K_BREAK            :'',
        pygame.K_MENU             :'',
        pygame.K_POWER        :'',
        pygame.K_EURO             :'',
    }
    # 将按键进行映射，得到对应的编码
    key_map = {
        '`' : 0x35,
        '1' : 0x1E,
        '2' : 0x1F,
        '3' : 0x20,
        '4' : 0x21,
        '5' : 0x22,
        '6' : 0x23,
        '7' : 0x24,
        '8' : 0x25,
        '9' : 0x26,
        '0' : 0x27,
        '-' : 0x2D,
        '=' : 0x2E,
        'keycode_14' : 0x89,
        'back_space' : 0x2A,
        'tab' : 0x2B,
        'q' : 0x14,
        'w' : 0x1A,
        'e' : 0x08,
        'r' : 0x15,
        't' : 0x17,
        'y' : 0x1C,
        'u' : 0x18,
        'i' : 0x0C,
        'o' : 0x12,
        'p' : 0x13,
        '[' : 0x2F,
        ']' : 0x30,
        'keycode_29' : 0x31,
        'caps_lock' : 0x39,
        'a' : 0x04,
        's' : 0x16,
        'd' : 0x07,
        'f' : 0x09,
        'g' : 0x0A,
        'h' : 0x0B,
        'j' : 0x0D,
        'k' : 0x0E,
        'l' : 0x0f,
        ';' : 0x33,
        "'" : 0x34,
        'keycode_42' : 0x32,
        'enter_l' : 0x28,
        'shift_l' : 0xE1,
        'keycode_45' : 0x64,
        'z' : 0x1D,
        'x' : 0x1B,
        'c' : 0x06,
        'v' : 0x19,
        'b' : 0x05,
        'n' : 0x11,
        'm' : 0x10,
        ',' : 0x36,
        '.' : 0x37,
        '/' : 0x38,
        'keycode_56' : 0x87,
        'shift_r' : 0xE5,
        'ctrl_l' : 0xE0,
        'alt_l' : 0xE2,
        'space' : 0x2C,
        'alt_r' : 0xE6,
        'ctrl_r' : 0xE4,
        'insert' : 0x49,
        'delete' : 0x4C,
        'left_arrow' : 0x50,
        'right_arrow' : 0x4F,
        'home' : 0x4A,
        'end' : 0x4D,
        'up_arrow' : 0x52,
        'down_arrow' : 0x51,
        'page_up' : 0x4B,
        'page_down' : 0x4E,
        'num_lock' : 0x53,
        'pad_7' : 0x5F,
        'pad_4' : 0x5C,
        'pad_1' : 0x59,
        'pad_8' : 0x60,
        'pad_2' : 0x5A,
        'pad_0' : 0x62,
        'pad_9' : 0x61,
        'pad_6' : 0x5E,
        'pad_3' : 0x5B,
        'pad_.' : 0x63,
        'pad_/' : 0x54,
        'pad_5' : 0x5D,
        'pad_*' : 0x55,
        'pad_-' : 0x56,
        'pad_+' : 0x57,
        'keycode_107' : 0x85,
        'enter_r' : 0x58,
        'esc' : 0x29,
        'f1' : 0x3A,
        'f2' : 0x3B,
        'f3' : 0x3C,
        'f4' : 0x3D,
        'f5' : 0x3E,
        'f6' : 0x3F,
        'f7' : 0x40,
        'f8' : 0x41,
        'f9' : 0x42,
        'f10' : 0x43,
        'f11' : 0x44,
        'f12' : 0x45,
        'print_screen' : 0x56,
        'scroll_lock' : 0x57,
        'pause' : 0x58,
        'l_win' : 0xE3,
        'r_win' : 0xE7,
        'app' : 0x65,
    }

    return key_map.get(keyvalue.get(key,0),0)

if __name__ == '__main__':
    try:
        # ser = serial.Serial('/dev/ttyAMA0', 9600)
        # if ser.isOpen == False:
        #     ser.open()
        #ser.write(bytes.fromhex("57ab00050501020000000F"))
        main()
    except KeyboardInterrupt:
        print(KeyboardInterrupt)
        # if ser != None:
        #     ser.close()