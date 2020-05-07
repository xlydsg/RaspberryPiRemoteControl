import pygame.font

class Button():
    def __init__(self, screen, msg, font_size, keyvalue, modvalue):
        """
        初始化按钮的属性

        :param screen: 要在哪个窗口显示
        :param msg: 按钮中显示的消息
        :param font_size: 显示消息的字体大小
        :param value: 该按钮对应的发送到串口的数据
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font_size = font_size
        self.keyvalue = keyvalue
        self.modvalue = modvalue
        self.stats = False

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (127, 127, 127)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont("fonts/Times_New_Roman.ttf", self.font_size)

        #创建按钮的rect对象，并使其位于左下角
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomleft = self.screen_rect.bottomleft
        
        # 按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """
        将msg渲染为图像，并使其在按钮上居中
        """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
        绘制一个用颜色填充的按钮，再绘制文本
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)