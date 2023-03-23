import datetime
import pygame
import pygame_widgets
from pygame.locals import *
from button_class import Button
from graphs import *
from authentication import user_has_access
from calculations import *
from sim_data import *
from widgets import *
import matplotlib.animation as animation
import ptext
# fonts = pygame.font.get_fonts()
#     main window colour \ overlay colour / text colour
font = pygame.font.SysFont('Consolas', 20)
pygame.init()

window = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF)
sunImg = pygame.image.load("planet images/sun.png").convert_alpha()
mercuryImg = pygame.image.load('planet images/mercury.png').convert_alpha()
venusImg = pygame.image.load('planet images/venus.png').convert_alpha()
earthImg = pygame.image.load('planet images/earth.png').convert_alpha()
marsImg = pygame.image.load('planet images/mars.png').convert_alpha()
jupiterImg = pygame.image.load('planet images/jupiter.png').convert_alpha()
saturnImg = pygame.image.load('planet images/saturn.png').convert_alpha()
uranusImg = pygame.image.load('planet images/uranus.png').convert_alpha()
neptuneImg = pygame.image.load('planet images/neptune.png').convert_alpha()
solarSystemImg = pygame.image.load(
    'planet images/solar_system.jpg').convert_alpha()
solarSystemImg = pygame.transform.scale(solarSystemImg, (400, 150))

imgs = [sunImg, mercuryImg, venusImg, earthImg, marsImg, jupiterImg, saturnImg, uranusImg,
        neptuneImg]

logo = pygame.image.load("sim logo2.png").convert_alpha()
# WIDTH = pygame.display.get_surface().
# ---------GRAPHS-----



for x in range(len(imgs)):
    imgs[x] = pygame.transform.scale(imgs[x], (325, 170))


colour_dict = {
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'orange': (255, 165, 0),
    'white': (238, 137, 104, 1)
}

planet_lst = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
setting_labels = ['Background colour', 'FPS', 'Graph figure colour', 'Graph line colour',
                  'Accent colour', 'Distance Metric']
graphTab_labels = ['GRAPH TYPE', 'PLANET 1', 'PLANET 2']

distance_graphImg = pygame.image.load(
    'graph images/distance_graph.png').convert_alpha()
anomaly_graphImg = pygame.image.load(
    'graph images/anomaly_graph.png').convert_alpha()

#  NAME, X-LABEL, Y-LABEL
distance_graph = Graph('distance_graph', 'Time since graph creation (S)',
                       'Distance between Planets (AU)')
anomaly_graph = Graph('anomaly_graph', 'Time since graph creation (S)',
                      'True anomaly of the planet (°)')
# List of graphs
graphs = [distance_graph, anomaly_graph]





class Sim:
    def __init__(self):
        self.instances = []  # planets and the sun
        self.scale = 1.0
        self.speed_multiplier = 2.5
        self.menu_colour = dark_blue_colours[1]
        self.window_colour = dark_blue_colours[0]
        self.date_edited = False
        self.shiftx = 240
        self.shifty = 0
        self.drawline = True
        self.orbit_ticks = 0  # number of frames when planet orbits are reset
        self.sim_accent_colour = 'orange'
        self.sim_running = True
        self.distance_metric = 'AU'
        self.user_access = True  # to check if users access has changed while sim running
        self.year = 2000
        self.day = 1
        self.month = 1

    def update_scale(self, scale_multiplier):
        # updates scale of the simulation
        for instances in self.instances:
            instances.radius *= scale_multiplier
        self.scale *= round(scale_multiplier, 2)

    def zoom_out(self):
        if self.scale > 0.05: # checks if max zoom out limit reached
            solar_system.update_scale(0.75)
            Body.SCALE *= 0.75


    def zoom_in(self):
        if self.scale < 9: # checks if max zoom in limit reached
            solar_system.update_scale(1.25)
            Body.SCALE *= 1.25

    def change_theme(self, option):
        if option == 0:
            self.menu_colour = dark_grey_colours[1]
            self.window_colour = dark_grey_colours[0]
        elif option == 1:
            self.menu_colour = dark_blue_colours[1]
            self.window_colour = dark_blue_colours[0]
        else:
            self.menu_colour = light_grey_colours[1]
            self.window_colour = light_grey_colours[0]

    def increase_speed(self):
        if self.speed_multiplier < 12:
            self.speed_multiplier += 0.15

    def decrease_speed(self):
        if self.speed_multiplier > 0.1:
            self.speed_multiplier -= 0.15


class Body:
    SCALE = 150

    def __init__(self, name, colour, radius):
        self.name = name

        self.__x = 0
        self.__y = 0
        self.orbital_points = []
        self.colour = colour
        self.radius = radius
        self.clicked_on = False
        self.circleRect = 0
        self.current_Rectx = 0
        self.prev_shiftx = 0
        self.stats = []
        self.enableTxt = False
        self.enableDistanceTxt = False
        self.radius_vector = 0.0
        self.default_vals = True
        self.true_anomaly = 0.0

        # starting coordinates of the planet
        self.startx = 0
        self.starty = 0
        # if the point should be appended to the orbit list
        self.append_orbit = True
        # if the planet has completed a full orbit
        self.rotated_once = False
        self.same_pos = False  # if planet hasnt moved on screen (slower planets)

        # ------Modifiable planet elements-----#
        self.__semi_major = 0.0
        self.__eccentricity = 0.0

    def generate(self, planet, jul_centuries):
        # calculate elements
        self.__semi_major, self.__eccentricity, orbit_incl, long_asc, long_peri, \
        self.true_anomaly, self.radius_vector = calculate_elements(self.name,
        self.__semi_major, self.__eccentricity, self.default_vals, jul_centuries)

        # calculate co-ordinates

        self.__x, self.__y = calculate_coords(self.radius_vector, long_asc,
              self.true_anomaly, long_peri, orbit_incl)


        solar_system.instances[0].draw()

        point = (self.__x, self.__y)

        # append to list of orbit points if append orbit = True
        if self.append_orbit:
            self.orbital_points.append(point)


        if not self.rotated_once: # if planet has not done one full orbit yet
            self.append_orbit = True
            if self.check_fully_rotated(): # check if planet has done an orbit
                self.rotated_once = True
                self.append_orbit = False # stop adding to orbit list

        # draw the body
        self.draw()

    def generate_stats(self, body):
        i = solar_system.instances.index(body)
        planet_dict = body_stats[i]
        self.stats.append(self.name)
        for key, value in planet_dict.items():
            self.stats.append(str(key) + ": " + str(value))

    def display_body_txt(self, y, move_y):
        label = []
        y_val = 20

        distance = self.radius_vector
        # convert to KM if it is the current distance metric
        if solar_system.distance_metric == 'KM':
            distance = convert_to_km(distance)
        distance = round(distance, 3)
        # automatically set as AU by above function#
        # only show distance  (clicked twice)
        if self.enableDistanceTxt:
            blit_line(f'Distance from the sun: {distance} {solar_system.distance_metric}',
                      self.circleRect.topright[0] + 100, y + y_val + move_y, 'white')
            return
        # show all stats (clicked once)
        if self.enableTxt:
            for i in range(1, len(self.stats)): # miss index 0: the planet name (already displayed)
                blit_line(self.stats[i], self.circleRect.topright[0] + 100, y + y_val + move_y, 'white')
                y_val += 20
            blit_line(f'Distance from the sun: {distance} {solar_system.distance_metric}',
                      self.circleRect.topright[0] + 100, y + y_val + move_y, 'white')

    def setx(self, xvalue):
        self.__x = xvalue

    def getx(self):
        return self.__x

    def sety(self, yvalue):
        self.__y = yvalue

    def gety(self):
        return self.__y

    def set_semi_major(self, s):
        self.__semi_major = s

    def get_semi_major(self):
        return self.__semi_major

    def set_eccentricity(self, e):
        self.__eccentricity = e

    def get_eccentricity(self):
        return self.__eccentricity

    def draw(self):
        # Scale x and y values
        x = self.__x * self.SCALE + SIM_WIDTH / 2
        y = -self.__y * self.SCALE + SIM_HEIGHT / 2


        if len(self.orbital_points) > 2:
            updated_points = []


            for point in self.orbital_points:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.SCALE + SIM_WIDTH / 2
                orbit_y = -orbit_y * self.SCALE + SIM_HEIGHT / 2
                updated_points.append((orbit_x + solar_system.shiftx, orbit_y +
                                            solar_system.shifty))

            if solar_system.drawline:
                points = updated_points
                pygame.draw.aalines(window, self.colour, False, points, 1)

        self.circleRect = pygame.draw.circle(window, self.colour, (x + solar_system.shiftx,
                                            y + solar_system.shifty), self.radius)

        if self.name == 'Saturn' or self.name == 'Jupiter' or self.name == 'Uranus' or self.name == 'Neptune':
            if round(self.__x, 2) == round((self.current_Rectx - self.prev_shiftx) + solar_system.shiftx, 2):
                self.append_orbit = False
                self.same_pos = True
            else:
                self.current_Rectx = self.__x
                self.prev_shiftx = solar_system.shiftx
                self.append_orbit = True
                self.same_pos = False

        if self.circleRect.collidepoint(pygame.mouse.get_pos()) or self.clicked_on:
            outer_circle_rect = pygame.draw.circle(window, 'white',
            (x + solar_system.shiftx, y + solar_system.shifty), self.radius + 5, width=1)

            line_endx = outer_circle_rect.midright[0] + 100
            pygame.draw.line(window, 'white', (x + solar_system.shiftx, y + solar_system.shifty),
                             (line_endx, y + solar_system.shifty))
            name_txt = font.render(self.name, True, self.colour)
            window.blit(name_txt, (line_endx + 10, y - 5 + solar_system.shifty))
            # display the statistics
            self.display_body_txt(y, solar_system.shifty)

    def check_fully_rotated(self):
        thresh = 0.001 # threshold
        # get the difference in x and y between start position and current position
        x_diff = abs(round((self.startx * solar_system.scale) - (self.__x * solar_system.scale),
                           3)) # 3 DP
        y_diff = abs(round((self.starty * solar_system.scale) - (self.__y * solar_system.scale),
                           3))

        ticks = pygame.time.get_ticks() # num of frames

        # speed up simulation to reduce length of orbit lists
        if ticks < 6000:
            solar_system.speed_multiplier = 2.7
        # return to normal speed
        if 12000 >= ticks <= 12500:
            solar_system.speed_multiplier = 1

        if x_diff <= thresh and y_diff <= thresh: # if completed an orbit
            if self.name == 'Neptune' or self.name == 'Uranus':
                if self.same_pos: # if not moved on screen
                    return # dont stop drawing orbit line

            if ticks > 2500 and (ticks - solar_system.orbit_ticks > 2000):
                return True
    def set_start_pos(self):
        self.startx = self.__x
        self.starty = self.__y





def create_solarSystem():
    global solar_system
    solar_system = Sim()
    sun = Body('Sun', 'yellow', 20)  # sun position is centre of the screen
    solar_system.sun = sun
    sun.x = 0
    sun.y = 0
    mercury = Body('Mercury', 'grey', 2)
    venus = Body('Venus', '#D8BE8E', 6)
    earth = Body('Earth', 'blue', 6)
    mars = Body('Mars', 'red', 4)
    jupiter = Body('Jupiter', '#F6F0E3', 10)
    saturn = Body('Saturn', '#F3CE89', 9)
    uranus = Body('Uranus', '#2BC7B4', 16)
    neptune = Body('Neptune', 'dark blue', 14)

    space_entites = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    for entity in space_entites:
        solar_system.instances.append(entity)
        entity.generate_stats(entity)

def blit_text(surface, text, pos, color, font=pygame.font.SysFont('Consolas', 15)):
    words = [word.split(' ') for word in text.splitlines()] # 2D array: each row is list of words.
    space = font.size(' ')[0] # space width
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= 1920:
                x = pos[0]  # Reset the x
                y += word_height  # Start on new row (if end of screen reached)
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x
        y += word_height  # Start on new row for each line


def show_body_info():
    for i in range(len(solar_system.instances)):
        if solar_system.instances[i].clicked_on: # if a body has been clicked
            blit_text(window, body_info[i], (1360, 350), 'white') # display the body info
            window.blit(imgs[i], (1470, 170)) # display the body image
            return # dont display solar system image & info if a body has been clicked
    blit_text(window, system_info, (1360, 350), 'white') # display solar system info
    window.blit(solarSystemImg, (1450, 200)) # display solar system image


def blit_line(text, x, y, colour):
    line = font.render(text, True, colour)
    window.blit(line, (x, y))

def show_controls():
    left_labels_y = 50
    left_side_tips = [f"SPEED: {round(solar_system.speed_multiplier, 2)}X",
                      "S: ENABLE / DISABLE ORBIT LINES", "ARROW KEYS: MOVE SCREEN",
                      "RIGHT CLICK: ENABLE / DISABLE PLANET INFO",
                      "C: CENTRE SCREEN"]

    for i in left_side_tips:
        blit_line(i, 20, left_labels_y, 'white')
        left_labels_y += 30


def set_elements(dropdown, sliders):
    planet = solar_system.instances[dropdown.selected + 1]

    print(dropdown.selected_an_option)

    if planet.default_vals:
        sliders[0].setValue(planet.get_semi_major())
        sliders[1].setValue(planet.get_eccentricity())
    else:
        planet.append_orbit = True
        if dropdown.selected_an_option:  # if a dropdown option changed
            sliders[0].setValue(planet.get_semi_major())
            sliders[1].setValue(planet.get_eccentricity())

        planet.set_semi_major(sliders[0].getValue())
        planet.set_eccentricity(sliders[1].getValue())

        for slider in sliders:
            if slider.selected:
                planet.set_start_pos() # set the start position of orbit
                planet.orbital_points = []







def btn_clicked(selected_btn, buttons):
    selected_btn.active = True
    # make all non-selected buttons inactive
    for btn in buttons:
        if btn.active:
            btn.active = False
            btn.active_colour = '#333333' # default colour
            return True



def main(id):

    global SIM_WIDTH, SIM_HEIGHT, distance_graphImg, anomaly_graphImg
    count = 0
    frame_count = 0

    first_run = True
    show_menu = False

    window = pygame.display.set_mode((1920, 1080), FULLSCREEN | DOUBLEBUF)

    leftwidth = window.get_width() * 0.7
    rightwidth = leftwidth
    leftheight = window.get_height() * 0.95

    SIM_WIDTH, SIM_HEIGHT = leftwidth, leftheight

    height = window.get_height()

    # rectangle for the menu
    rightrect = (leftwidth, 0, rightwidth, height)

    right_surf = pygame.Surface(pygame.Rect(rightrect).size, pygame.SRCALPHA)

    paused_text_x = 850

    create_solarSystem()

    body_info_btn = Button(1450, 100, 90, 22, 'INFO')
    physics_btn = Button(1700, 100, 130, 22, 'PLANET EDITOR')
    settings_btn = Button(1650, 140, 90, 22, 'SETTINGS')
    instructions_btn = Button(1560, 100, 120, 22, 'INSTRUCTIONS')
    submit_btn = Button(1520, 1000, 250, 22, 'SUBMIT')
    default_vals_btn = Button(1420, 800, 120, 22, 'DEFAULT VALS')
    custom_vals_btn = Button(1720, 800, 120, 22, 'CUSTOM VALS')
    reset_all_vals = Button(1570, 800, 120, 22, 'RESET VALS')
    graph_btn = Button(1500, 140, 120, 22, 'GRAPHS')

    reset_all_vals.active = True
    #   placing at the far right of the window
    collapse_expand_btn = Button(pygame.display.get_surface().get_width() - 10, 540, 3, 120, '')
    # adding collapse button to list of buttons
    buttons = [body_info_btn, physics_btn, settings_btn, instructions_btn,
               submit_btn, default_vals_btn, custom_vals_btn, reset_all_vals,
               graph_btn, collapse_expand_btn]

    body_info_btn.active = True

    fps = 60
    # --------------------------CREATING WIDGETS----------------------------------------------------#

    date_textbox, sliders, planet_dropdown, val_outputs, side_labels, graphType_dropdown, \
    body1_dropdown, body2_dropdown, theme_dropdown, \
    graphbg_dropdown, graph_line_dropdown, accents_dropdown, \
    metric_dropdown, fps_dropdown = create_widgets(window, solar_system.sim_accent_colour,
                                                   solar_system.menu_colour, font)
    # ----------------------------- fi------------------------------------------------------------------#
    # graph optionbox1 : backgroundgure colour, graph optionbox 2 graph line colour
    clock = pygame.time.Clock()
    while solar_system.user_access:
        element_labels_y = 310
        if count > 100:
            if not user_has_access(id):
                solar_system.user_access = False
            count = 0
        count += 1

        clock.tick(fps)

        shift_distance = 10

        window.fill(solar_system.window_colour)
        rgb = solar_system.menu_colour + (200,)
        graphImgs = [distance_graphImg, anomaly_graphImg]

        # window.blit(space_backgroundImg, (0, 0))

        blit_line(f'FPS: {round(clock.get_fps())}', 20, 200, 'white')
        jul_century = gregorian_to_julian(solar_system.day, solar_system.month, solar_system.year)

        for i in range(1, len(solar_system.instances)):
            solar_system.instances[i].generate(solar_system.instances[i], jul_century)



        show_controls()

        if solar_system.date_edited:
            for planet in solar_system.instances:
                solar_system.orbit_ticks = pygame.time.get_ticks()
                planet.set_start_pos()
                planet.rotated_once = False

        if solar_system.sim_running:
            solar_system.date_edited = False
            solar_system.day, solar_system.month, solar_system.year \
                = increment_date(solar_system.day, solar_system.month, solar_system.year)

            date_textbox.setText(f'{solar_system.year}-{solar_system.month}'
                                 f'-{round(solar_system.day)}')
            date_textbox.colour = solar_system.window_colour


            solar_system.day += 0.4 * round(solar_system.speed_multiplier, 2)
            solar_system.day = round(solar_system.day, 2)

        else:
            blit_line('SIMULATION PAUSED', paused_text_x, 1050, solar_system.sim_accent_colour)

            if date_textbox.selected:
                date_textbox.textColour = 'grey'
                solar_system.date_edited = True

                try:
                    new_date = date_textbox.getText()
                    date_lst = new_date.split('-')

                    new_year = int(date_lst[0])

                    new_month = int(date_lst[1])

                    new_day = float(date_lst[2])
                    new_day = int(new_day)
                    # see if the entered values make a valid date
                    datetime.datetime(year=new_year, month=new_month, day=new_day)

                except:
                    blit_line('Date has to be in format yyyy-m-d', 190, 20,
                              solar_system.sim_accent_colour)



                else:
                    solar_system.year = int(date_lst[0])

                    solar_system.month = int(date_lst[1])

                    solar_system.day = float(date_lst[2])
                    solar_system.day = int(solar_system.day)



                    for planet in solar_system.instances:
                        planet.orbital_points = []

            else:
                date_textbox.textColour = solar_system.sim_accent_colour
                solar_system.date_edited = False

        # -----------------------EVENTS SECTION--------------------------

        events = pygame.event.get()

        for event in events:
            pos = pygame.mouse.get_pos()

            if not solar_system.user_access or event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            # pause or play simulation
            elif event.type == pygame.KEYDOWN:  # if key pressed
                if event.key == pygame.K_SPACE: # if spacebar pressed
                    if solar_system.sim_running:
                        solar_system.sim_running = False
                    else:
                        solar_system.sim_running = True
                # increase or decrease speed
                elif event.key == pygame.K_a: # if A key pressed
                    solar_system.decrease_speed()
                elif event.key == pygame.K_d: # if D key pressed
                    solar_system.increase_speed()
                # enable or disable orbit lines
                elif event.key == pygame.K_s: # if S key pressed
                    if solar_system.drawline:
                        solar_system.drawline = False
                    else:
                        solar_system.drawline = True



                elif event.key == pygame.K_c: # if C key pressed
                    if show_menu:
                        solar_system.shiftx, solar_system.shifty = 0, 0
                    else:
                        solar_system.shiftx = 240
                        solar_system.shifty = 0




            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # scroll down: zoom out
                    solar_system.zoom_out()

                elif event.button == 4:  # scroll up: zoom in
                    solar_system.zoom_in()



                elif event.button == 1:  # left mouse button pressed
                    if collapse_expand_btn.isOver(pos):
                        if show_menu:  # close menu
                            # button placed at far right of the screen
                            collapse_expand_btn.x = pygame.display.get_surface().get_width() - 10
                            show_menu = False
                        else: # open menu
                            # button placed just slightly left of the menu
                            collapse_expand_btn.x = 1340
                            show_menu = True
                    for body in solar_system.instances:
                        if body.circleRect.collidepoint(pygame.mouse.get_pos()):
                            if body.clicked_on:
                                body.clicked_on = False
                            else:
                                body.clicked_on = True

                    if submit_btn.isOver(pos): # submit button clicked
                        if submit_btn.active:
                            submit_btn.active = False
                        else:
                            submit_btn.active = True
                        # reset frame count and clear graph values
                        frame_count = 0
                        distance_graph.clear_graph()
                        anomaly_graph.clear_graph()

                    if body_info_btn.isOver(pos):  # INFO button clicked
                        btn_clicked(body_info_btn, (physics_btn, settings_btn, instructions_btn,
                                                      graph_btn))

                    elif physics_btn.isOver(pos):  # PLANET EDITOR BUTTON CLICKED
                        btn_clicked(physics_btn, (body_info_btn, settings_btn, instructions_btn,
                                                  graph_btn))


                    elif settings_btn.isOver(pos):  # SETTINGS BUTTONS CLICKED
                        btn_clicked(settings_btn, (body_info_btn, physics_btn, instructions_btn,
                                                   graph_btn))

                    elif instructions_btn.isOver(pos): # INSTRUCTIONS BUTTON CLICKED
                        btn_clicked(instructions_btn, (body_info_btn, settings_btn, physics_btn,
                                                       graph_btn))

                    elif graph_btn.isOver(pos): # GRAPHS BUTTON CLICKED
                        btn_clicked(graph_btn, (body_info_btn, settings_btn, physics_btn,
                                                instructions_btn))

                    if custom_vals_btn.isOver(pos):
                        planet = solar_system.instances[planet_dropdown.selected + 1]
                        btn_clicked(custom_vals_btn, (default_vals_btn, reset_all_vals))
                        planet.default_vals = False


                    elif default_vals_btn.isOver(pos):
                        planet = solar_system.instances[planet_dropdown.selected + 1]
                        btn_clicked(default_vals_btn, (custom_vals_btn, reset_all_vals))
                        planet.orbital_points = []
                        planet.default_vals = True
                        # reset bools
                        planet.append_orbit = True
                        planet.rotated_once = False
                        planet.set_start_pos()





                    elif reset_all_vals.isOver(pos):
                        btn_clicked(reset_all_vals, (default_vals_btn, custom_vals_btn))
                        for planet in solar_system.instances:
                            planet.orbital_points = []
                            planet.default_vals = True
                            # reset bools
                            planet.append_orbit = True
                            planet.rotated_once = False
                            planet.set_start_pos()

                        reset_all_vals.active = False
                        custom_vals_btn.active = False
                        default_vals_btn.active = True




                elif event.button == 3: # right click
                    for body in solar_system.instances:
                        if body.circleRect.collidepoint(pygame.mouse.get_pos()):
                            if not body.enableTxt:  # if no stats shown
                                body.enableTxt = True # enable stats
                            else:
                                if body.enableDistanceTxt: # if only distance shown
                                    body.enableDistanceTxt = False # disable distance
                                else:
                                    body.enableDistanceTxt = True # enable distance only
                                body.enableTxt = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: # shift left
            solar_system.shiftx += shift_distance
        elif keys[pygame.K_RIGHT]: # shift right
            solar_system.shiftx -= shift_distance
        elif keys[pygame.K_UP]: # shift up
            solar_system.shifty += shift_distance
        elif keys[pygame.K_DOWN]: # shift down
            solar_system.shifty -= shift_distance

        date_textbox.draw()



        # # ------------------------------------------------------------#
        #
        planet_dropdown.update(events)
        pygame_widgets.update(events)
        pygame_widgets.update(events)
        graphType_dropdown.update(events)
        body1_dropdown.update(events)
        body2_dropdown.update(events)
        theme_dropdown.update(events)
        graphbg_dropdown.update(events)
        graph_line_dropdown.update(events)
        accents_dropdown.update(events)
        fps_dropdown.update(events)
        metric_dropdown.update(events)

        for i in range(len(sliders)):
            # hide sliders and textboxes
            sliders[i].hide()
            val_outputs[i].hide()


        if show_menu:
            rgb = solar_system.menu_colour + (100,)

            # Semi transparent menu
            pygame.draw.rect(right_surf, rgb, right_surf.get_rect(), 0, 32)
            pygame.draw.rect(right_surf, solar_system.sim_accent_colour,
                             right_surf.get_rect(), 2, 32)
            window.blit(right_surf, rightrect)

            window.blit(logo, (1530, 10))

            body_info_btn.draw(window)
            physics_btn.draw(window)
            settings_btn.draw(window)
            instructions_btn.draw(window)
            graph_btn.draw(window)

            if body_info_btn.active:
                show_body_info()
            elif instructions_btn.active:
                blit_text(window, instructions, (1400, 190), 'white')
                blit_line('Instructions', 1560, 200, solar_system.sim_accent_colour)

            elif physics_btn.active: # physics editor open
                for i in range(len(sliders)):
                    # initialise  values and display
                    sliders[i].handleColour = colour_dict[solar_system.sim_accent_colour]
                    sliders[i].draw()
                    sliders[i].show()
                    val_outputs[i].draw()
                    val_outputs[i].show()
                    val_outputs[i].setText(round(sliders[i].getValue(), 2))
                # display the side labels
                for i in range(3):
                    blit_line(side_labels[i], 1370, element_labels_y, 'white')
                    element_labels_y += 100
                # draw planet editor buttons
                default_vals_btn.draw(window)
                custom_vals_btn.draw(window)
                planet_dropdown.draw(window)
                reset_all_vals.draw(window)
                blit_line('Planet Editor', 1550, 200, solar_system.sim_accent_colour)





                set_elements(planet_dropdown, sliders)
                #
                if solar_system.instances[planet_dropdown.selected + 1].default_vals:
                    default_vals_btn.active = True
                    custom_vals_btn.active = False
                else:
                    default_vals_btn.active = False
                    custom_vals_btn.active = True

            if not physics_btn.active: # if physics editor not being used:
                for i in range(len(sliders)):
                    # hide sliders and textboxes
                    sliders[i].hide()
                    val_outputs[i].hide()

            if graph_btn.active:
                min, max = 0, 3  # ensure correct number of lables are shown
                blit_line('GRAPHS', 1600, 200, solar_system.sim_accent_colour)
                graph_labels_y = 320
                graphType_dropdown.draw(window)

                if graphType_dropdown.selected == 0: # DISTANCE GRAPH SELECTED
                    body2_dropdown.draw(window)
                    body1_dropdown.draw(window)

                elif graphType_dropdown.selected == 1:  # TRUE ANOMALY GRAPH SELECTED
                    body1_dropdown.draw(window)
                    max = 2 # show only 2 lables (only 2 dropdowns needed)

                graphType_dropdown.draw(window)

                for i in range(min, max):
                    blit_line(graphTab_labels[i], 1400, graph_labels_y, 'white')
                    graph_labels_y += 100
                submit_btn.draw(window)

                if submit_btn.active:
                    if solar_system.sim_running:
                        frame_count += 1
                        if frame_count > 20: # only update the graph every 20 frames
                            if graphType_dropdown.selected == 0: # DISTANCE GRAPH
                                body_1, body_2 = solar_system.instances[body1_dropdown.selected+1],  \
                                        solar_system.instances[body2_dropdown.selected]
                                planet_distance = calculate_distance(body_1.getx(), body_1.gety(),
                                                                     body_2.getx(), body_2.gety())

                                if solar_system.distance_metric == 'KM':
                                    planet_distance = convert_to_km(planet_distance)
                                distance_graph.values.append(planet_distance)
                                # plot the graph
                                distance_graph.plot()
                                distance_graphImg = pygame.image.load('distance_graph.png').\
                                    convert_alpha()



                            elif graphType_dropdown.selected == 1: # TRUE ANOMALY GRAPH
                                planet = solar_system.instances[body1_dropdown.selected + 1]

                                anomaly_graph.values.append(planet.true_anomaly)
                                # plot the graph
                                anomaly_graph.plot()
                                anomaly_graphImg = pygame.image.load('anomaly_graph.png').\
                                    convert_alpha()

                            frame_count = 0
                    # display the graph image in the pygame window
                    window.blit(graphImgs[graphType_dropdown.selected], (1400, 600))
                #
                #     # true anomaly



            #



            #
            elif settings_btn.active:
                blit_line('SETTINGS', 1570, 200, solar_system.sim_accent_colour)
                side_labels_y = 320

                # draw
                metric_dropdown.draw(window)
                accents_dropdown.draw(window)
                graph_line_dropdown.draw(window)
                submit_btn.draw(window)
                graphbg_dropdown.draw(window)
                fps_dropdown.draw(window)
                theme_dropdown.draw(window)


                # display labels
                for label in setting_labels:
                    blit_line(label, 1400, side_labels_y, 'white')
                    side_labels_y += 100

                # if submit button pressed
                if submit_btn.active:
                    submit_btn.active = False
                    accent_colour = accents_dropdown.option_list[accents_dropdown.selected]

                    # SET DATE TEXTBOX AND WINDOW COLOURS
                    date_textbox.colour = solar_system.window_colour
                    date_textbox.textColour = accent_colour
                    solar_system.change_theme(theme_dropdown.selected)


                    # SET BUTTON COLOURS

                    for btn in buttons:
                        btn.given_colour = accent_colour
                    solar_system.sim_accent_colour = accent_colour

                    # SET FPS
                    fps = float(fps_dropdown.option_list[fps_dropdown.selected])


                    # SET DROPDOWN COLOURS

                    for dropdown in [planet_dropdown, graphType_dropdown, metric_dropdown,
                    body1_dropdown, fps_dropdown, body2_dropdown, graphbg_dropdown,
                    graph_line_dropdown, accents_dropdown, theme_dropdown]:

                        dropdown.active_colour = solar_system.sim_accent_colour
                        dropdown.color = solar_system.menu_colour

                    # SET DISTANCE METRIC
                    solar_system.distance_metric = \
                        metric_dropdown.option_list[metric_dropdown.selected]

                    # SET GRAPH COLOURS AND LABELS
                    for graph in graphs:
                        # graph.bg_color = graphbg_dropdown.option_list[graphbg_dropdown.selected]
                        graph.bg_color = graph.colours[graphbg_dropdown.selected]
                        graph.line_color = \
                            graph_line_dropdown.option_list[graph_line_dropdown.selected]

                    distance_graph.ylabel_txt = f'Distance between Planets ' \
                    f'({solar_system.distance_metric}' \
                    f'{" * 10M" if solar_system.distance_metric == "KM" else print()})'

            #



            #


        #
        #
        #
        # else:

        #
        # # if pygame.display.get_surface().get_width() == 1920 and pygame.display.get_surface().get_height() == 1080:
        collapse_expand_btn.draw(window)
        #
        if first_run:
            first_run = False



        pygame.display.update()

    pygame.quit()

    # window = Tk()
    # window.withdraw()
    # messagebox.showerror(message='You no longer have access! Closing simulation...')
    # window.destroy()s
    # window.mainloop()



if __name__ == '__main__':
    pass
main('PyAdmin727')
