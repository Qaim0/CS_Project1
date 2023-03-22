import pygame

pygame.init()

class Button:
    def __init__(self, x, y, w, h, text, font = pygame.font.SysFont('Gotham', 18, 'bold', ),
                 accent_colour = 'orange'):
        self.colour = '#333333'
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.active = False
        self.given_colour = accent_colour
        self.active_colour = accent_colour
        self.font = font

    def draw(self, win):
        # Call this method to draw the button on the screen

        pygame.draw.rect(win, self.active_colour, (self.x - 2, self.y - 2, self.width + 4,
                                                   self.height + 4), 0, 10)
                                                    # pad dimensions to fit text

        self.buttonRect = pygame.draw.rect(win, self.colour, (self.x, self.y, self.width,
                                                              self.height), 0, 8)


        if self.isOver(pygame.mouse.get_pos()) or self.active:
            # highlight button
            self.active_colour = self.given_colour
        else:
            # default colour
            self.active_colour = (12, 15, 26)


        text = self.font.render(self.text, True, self.active_colour)
        win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y +
                        (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Dropdown(Button):
    def __init__(self, x, y, w, h, colour, accent_colour, font, option_list):
        # inherit x, y, width, height, colour, font, accent colour
        super().__init__(x, y, w, h, colour, font, accent_colour)
        self.rect = pygame.Rect(x, y, w, h)
        self.option_list = option_list
        self.selected = 0 # boolean
        self.draw_menu = False
        self.show_options = False
        self.active_option = -1
        self.selected_an_option = False
        self.txt_colour = 'white'

    def draw(self, surf):
        pygame.draw.rect(surf, self.active_colour if self.show_options else
        self.colour, self.rect, 1, 19) # If hovered over highlight

        msg = self.font.render(self.option_list[self.selected], 1, 'white')
        surf.blit(msg, msg.get_rect(center=self.rect.center)) # display dropdown text

        if self.draw_menu: # display options
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height # lower each option

                pygame.draw.rect(surf, self.active_colour if i == self.active_option
                else self.colour, rect, 0) # rect for the option


                msg = self.font.render(text, 1, (self.txt_colour))
                surf.blit(msg, msg.get_rect(center=rect.center)) # display option text


    def update(self, event_list):
        self.selected_an_option = False
        mpos = pygame.mouse.get_pos()
        # check mouse collision
        self.show_options = self.rect.collidepoint(mpos)
        self.active_option = -1

        for i in range(len(self.option_list)):
            rect = self.rect.copy() # rect of the hovered over option
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.show_options and self.active_option == -1:
            self.draw_menu = False


        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_options: # if dropdown clicked on
                    self.draw_menu = not self.draw_menu
                    self.button_clicked = False

                elif self.draw_menu and self.active_option >= 0: # if dropdown option clicked on
                    self.selected = self.active_option
                    self.draw_menu = False
                    self.selected_an_option = True
                    return self.active_option
        return -1 # dont do anything

