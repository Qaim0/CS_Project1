import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)






#ccentricity
# orbit incl : between 2.4 and 180.0
# long - asc node : between 4.8 and 360.0
# long - perihelion : between 4.8 and 360.0
# eccentric anomaly :

adjustables = ['Eccentricity', 'Orbit Inclination', 'Longitude of Ascending node',
               'Longitude of Perihelion', 'Eccentric Anomaly']





class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.y = y
        self.clicked_on_option = False

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect, 0, 19)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 1, 19)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False


        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active: # if optionbox clicked on
                    self.draw_menu = not self.draw_menu
                    self.clicked_on_option = False
                    print('ee')

                elif self.draw_menu and self.active_option >= 0: # if optionbox option clicked on
                    print('aaaaaaaaaaaaaaaaaaaaaaaaa')
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.clicked_on_option = True
                    return self.active_option
        return -1



def create_widgets(win, solar_system):
    lables = ['Select mass', 'semi-major axis', 'Eccentricity']


    planets = OptionBox(
        1750, 300, 160, 40, (150, 150, 150), 'orange', pygame.font.SysFont(None, 30),
        ["Mercury", "Venus", "Earth", "Mars", "Jupiter"])
    themes = OptionBox(
        1700, 300, 160, 40, (150, 150, 150), 'orange', pygame.font.SysFont(None, 30),
        ["Dark Standard", "Dark blue", "light"])


    slider1 = Slider(win, 1650, 410, 150, 10, min=0.02, max=5, step=0.01)  # for semi major axis
    slider2 = Slider(win, 1650, 510, 150, 10, min=0.00000001, max=0.989, step=0.001)  # for eccentricity


    output1 = TextBox(win, 1820, 400, 85, 30, fontSize=20, borderThickness=0)
    output2 = TextBox(win, 1820, 500, 85, 30, fontSize=20, borderThickness=0)

    fps_box = TextBox(win, 1750, 400, 150, 45, textColour='black', fontSize=25, colour='grey', borderThickness=0, font=pygame.font.SysFont('Consolas', int(20)))
    date_textbox = TextBox(win, 10, 0, 700, 45, textColour=solar_system.txt_colour, fontSize=25, borderThickness=0, font=pygame.font.SysFont('Consolas', int(20)))



    # graph optionboxes


    graph_type = OptionBox(1560, 300, 160, 40, (150, 150, 150), 'orange', pygame.font.SysFont(None, 30),
        ["Distance", "Venus", "Earth", "Mars", "Jupiter"])
    planet1 = OptionBox(1450, 400, 160, 40, (150, 150, 150), 'orange', pygame.font.SysFont(None, 30),
        ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
    planet2 = OptionBox(1650, 400, 160, 40, (150, 150, 150), 'orange', pygame.font.SysFont(None, 30),
        ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])


    outputs = [output1, output2]

    sliders = [slider1, slider2]


    return date_textbox, sliders, planets, themes, lables, outputs, fps_box, graph_type, planet1, planet2
    # lists = comboboxes

