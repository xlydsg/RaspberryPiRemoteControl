import pygame.font

class Button():
    def __init__(self, screen, prop):
        """
        初始化按钮的属性

        :param screen: 要在哪个窗口显示
        :param prop: 使用字典传递Button属性
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font_size = prop['font_size']
        self.modvalue = prop['modvalue']
        self.keyvalue = prop['keyvalue']
        self.order = prop['order']
        self.stats = False

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 150, 40
        self.space = 30
        self.button_color = (127, 127, 127)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont("fonts/Times_New_Roman.ttf", self.font_size)

        #创建按钮的rect对象，并使其位于左下角
        # self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottom = self.screen_rect.bottom
        self.rect.left = (self.order - 1) * (self.width + self.space)
        # self.rect.bottomleft = self.screen_rect.bottomleft
        
        # 按钮的标签只需创建一次
        self.prep_msg(prop['msg'])

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