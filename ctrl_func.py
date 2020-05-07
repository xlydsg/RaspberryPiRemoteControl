def check_button(button, mouse_x, mouse_y):
    """
    检测鼠标点击时，是否处在button的矩形框中
    :param button: 定义的button
    :param mouse_x: 鼠标位置横坐标
    :param mouse_y: 鼠标位置纵坐标
    """
    if mouse_x < button.rect.right and mouse_x >= button.rect.left:
        if mouse_y > button.rect.top and mouse_y <= button.rect.bottom:
            button.stats = True

def ch9329_kbencode(keyvalue,modvalue):
    """
    拼接串口需要发送的键盘按键数据包，支持最多8个控制按键和1个普通按键

    :param keyvalue: 按下的普通按键
    :param modvalue: 按下的组合键
    :returns: 返回串口需要发送的数据包
    """
    str_head = "57AB000208"
    str_tail = "%02x"%((0x0C+keyvalue+modvalue)&0xff)
    # mod = "%02x"%(modvalue)
    key = "%02x"%(keyvalue)
    str_a = str_head + '00' + '00'  + key + '0000000000'  + str_tail
    # str_a = str_head + mod + '00'  + key + '0000000000'  + str_tail

    return str_a

def ch9329_msencode(mouse_x, mouse_y, window_size):
    """
    组合串口发送的鼠标位置信息

    :param x: 鼠标位置的横坐标
    :param y: 鼠标位置的纵坐标
    """
    str_head = "57AB0004070200" 
    x = int(mouse_x * 4096/window_size['window_W'])
    y = int(mouse_y * 4096/window_size['window_L'])

    x_str1 = "%02x"%(x&0xff) 
    x_str2 = "%02x"%((x>>8)&0xff)
    y_str1 = "%02x"%(y&0xff) 
    y_str2 = "%02x"%((y>>8)&0xff) 

    str_tail = 0x57+0xAB+4+7+2+ int(y&0xff) +  int((y>>8)&0xff) + int(x&0xff) +  int((x>>8)&0xff)

    str = str_head + x_str1 +x_str2 + y_str1 + y_str2 + '00' + "%02x"%(str_tail&0xff)
    return str