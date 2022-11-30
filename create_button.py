import pygame

pygame.init()

class button():
    def __init__(self, x, y, width, height, text=''):
        self.original_colour = '#333333'
        self.colour = '#333333'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button_clicked = False
        self.bd_colour = 'orange'
        self.highlight_btn = False
    def highlight_button(self):
        self.highlight_btn = True

    def draw(self, win, outline=True):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, self.bd_colour, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0, 4)

        self.buttonRect = pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

        if self.buttonRect.collidepoint(pygame.mouse.get_pos()) or self.button_clicked:
            self.bd_colour = 'orange'


        else:
            self.bd_colour = 'grey'



        if self.text != '':
            if self.buttonRect.collidepoint(pygame.mouse.get_pos()) or self.button_clicked or self.highlight_btn:
                self.bd_colour = 'orange'
            else:
                self.bd_colour = 'grey'

            font = pygame.font.SysFont('Gotham', 20, 'bold')
            text = font.render(self.text, 1, self.bd_colour)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def redraw(self, surf):
        self.draw(surf, (0, 0, 0))







#
#
# program_running = True
# while program_running:
#     mybutton.redraw(win)
#     pygame.display.update()
#
#     for event in pygame.event.get():
#         pos = pygame.mouse.get_pos()
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             program_running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if mybutton.isOver(pos):
#                 print('clicked')
#         if event.type == pygame.MOUSEMOTION:
#             if mybutton.isOver(pos):
#                 mybutton.color = ('dark green')
#             else:
#                 mybutton.color = '#0a95ad'