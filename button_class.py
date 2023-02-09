import pygame

pygame.init()

class Button():
    def __init__(self, x, y, w, h, text, font = pygame.font.SysFont('Gotham', 18, 'bold', ),
                 accent_colour = 'red'):
        self.colour = '#333333'
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.button_clicked = False
        self.given_bd_colour = accent_colour
        self.accent_colour = accent_colour
        self.highlight_btn = False
        self.font = font
    def highlight_button(self):
        self.highlight_btn = True

    def draw(self, win, outline=True):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, self.accent_colour, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0, 10)

        self.buttonRect = pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0, 8)

        if self.buttonRect.collidepoint(pygame.mouse.get_pos()) or self.button_clicked:
            self.accent_colour = self.given_bd_colour
        else:
            self.accent_colour = (12, 15, 26)


        if self.buttonRect.collidepoint(pygame.mouse.get_pos()) or self.button_clicked or self.highlight_btn:
            self.accent_colour = self.given_bd_colour
        else:
            self.accent_colour = (12, 15, 26)


        text = self.font.render(self.text, True, self.accent_colour)
        win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Dropdown(Button):
    def __init__(self, x, y, w, h, colour, accent_colour, font, option_list, selected=0):
        super().__init__(x, y, w, h, colour, font, accent_colour)
        self.rect = pygame.Rect(x, y, w, h)
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.show_options = False
        self.active_option = -1
        # self.y = y
        self.txt_colour = 'white'

    def draw(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2, 19)
        pygame.draw.rect(surf, self.accent_colour if self.show_options else self.colour, self.rect, 1, 19) # If hovered over
        msg = self.font.render(self.option_list[self.selected], 1, 'white')
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.accent_colour if i == self.active_option else self.colour, rect, 0)
                msg = self.font.render(text, 1, (self.txt_colour))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            # pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.show_options = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.show_options and self.active_option == -1:
            self.draw_menu = False


        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_options: # if optionbox clicked on
                    self.draw_menu = not self.draw_menu
                    self.button_clicked = False
                    # print('ee')

                elif self.draw_menu and self.active_option >= 0: # if optionbox option clicked on
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.button_clicked = True
                    return self.active_option
        return -1

