import sys
import pygame
import serial

window_W = 100
window_L = 100

def run_capture():
    pygame.init()
    screen = pygame.display.set_mode((window_W,window_L))
    pygame.display.set_caption("keycapture")
    pygame.event.set_grab(True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.set_grab(not(pygame.event.get_grab()))
                print('0x%x'%pygkey_to_code(event.key))
                print(ch9329_kbencode(pygkey_to_code(event.key),pygkey_mod(event.mod)))
            elif event.type == pygame.KEYUP:
                print("\x57\xAB\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x00\x0C")
                #ser.write("\x57\xAB\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x00\x0C" )
            elif event.type == pygame.MOUSEMOTION:
                print(event.rel[0]) 
                print(event.rel[1])
                if pygame.event.get_grab():
                    pygame.mouse.set_pos(window_W/2,window_W/2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("You pressed the left mouse button")
                    print("\x57\xAB\x00\x05\x05\x01\x01\x00\x00\x00\x0E")
                elif event.button == 2:
                    print("You pressed the middle mouse button")
                    print("\x57\xAB\x00\x05\x05\x01\x03\x00\x00\x00\x10")
                elif event.button == 3:
                    print("You pressed the right mouse button")
                    print("\x57\xAB\x00\x05\x05\x01\x02\x00\x00\x00\x0F")
                elif event.button == 4:
                    print("You up")
                    print("\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0E") 
                elif event.button == 5:
                    print("You down")
                    print("\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0E") 
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print("You released the left mouse button")
                    print("\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0D")
                elif event.button == 2:
                    print("You released the middle mouse button")
                    print("\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0D")
                elif event.button == 3:
                    print("You released the right mouse button")
                    print("\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0D")
                elif event.button == 4:
                    print("You up")
                elif event.button == 5:
                    print("You down")



        pygame.display.flip()

def ch9329_msencode(x,y):
    return 0

def ch9329_kbencode(keyvalue,modvalue):
    str_head = "\x57\xAB\x00\x02\x08" 
    str_tail = chr((0x0C+keyvalue+modvalue)&0xff) 
    mod = chr(modvalue) 
    key = chr(keyvalue) 
    str_a = str_head + mod + '\x00'  + key + '\x00\x00\x00\x00\x00'  + str_tail

    return str_a

def pygkey_mod(mod):
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
        pygame.K_RIGHT            :'left_arrow',
        pygame.K_LEFT              :'right_arrow',
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

run_capture()

