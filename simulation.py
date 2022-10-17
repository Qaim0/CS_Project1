import pygame

# fonts = pygame.font.get_fonts()
# print(fonts)
#     main window colour \ overlay colour / text colour

import pygame_widgets
from planet_stats_dicts import *
from planet_calculations import *
from create_button import button, btn_clicked
from tools import generate_menu
from pygame_widgets.textbox import TextBox
import datetime
from planet_info import solar_system_info, instructions, system_info
dark_grey_colours = ['black',  (20, 20, 20), 'white']
light_colours = ['#dedfe0', (30, 203, 225), 'black']
dark_blue_colours = ['#05070f',  (12, 15, 26), 'white']

font = pygame.font.SysFont('Consolas', int(20), )
pygame.init()


window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)


info_flag = True
display_menu = False
show_settings = False
show_instructions = False

# -----------IMAGES-------------

sunImg = pygame.image.load('sun.png').convert_alpha()
mercuryImg = pygame.image.load('mercury.png').convert_alpha()
venusImg = pygame.image.load('venus.png').convert_alpha()
earthImg = pygame.image.load('earth.png').convert_alpha()
marsImg = pygame.image.load('mars.png').convert_alpha()
jupiterImg = pygame.image.load('jupiter.png').convert_alpha()
saturnImg = pygame.image.load('saturn.png').convert_alpha()
uranusImg = pygame.image.load('uranus.png').convert_alpha()
neptuneImg = pygame.image.load('neptune.png').convert_alpha()
solarSystemImg = pygame.image.load('solar_system.jpg').convert_alpha()
solarSystemImg = pygame.transform.scale(solarSystemImg, (400, 150))

imgs = [sunImg, mercuryImg, venusImg, earthImg, marsImg, jupiterImg, saturnImg, uranusImg, neptuneImg]
for x in range(len(imgs)):
    imgs[x] = pygame.transform.scale(imgs[x], (325, 170))


# RATES: a, e, i, mean longitude (L), longitude of perihelion, longitude of ascending node

planet_lst = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


class Solarsystem:
    def __init__(self, speed_multiplier):
        self.instances = []
        self.scale = 1
        self.speed_multiplier = speed_multiplier
        self.default_vals = True
        self.theme = 0
        self.overlay_colour = dark_grey_colours[1]
        self.txt_colour = dark_grey_colours[2]
        self.window_colour = dark_grey_colours[0]




    def update_scale(self, scale_multiplier):
        for instances in self.instances:
            instances.radius *= scale_multiplier
    def check_theme(self, combobox):
        if self.theme == 0:
            self.overlay_colour = dark_grey_colours[1]
            self.txt_colour = dark_grey_colours[2]
            self.window_colour = dark_grey_colours[0]
        elif self.theme == 1:
            self.overlay_colour = dark_blue_colours[1]
            self.txt_colour = dark_blue_colours[2]
            self.window_colour = dark_blue_colours[0]

        else:
            self.overlay_colour = light_colours[1]
            self.txt_colour = light_colours[2]
            self.window_colour = light_colours[0]





class Planet:
    SCALE = 150

    def __init__(self, name, colour, mass, radius):
        self.name = name
        self.startx = 0
        self.starty = 0
        self.x = 0
        self.y = 0
        self.orbit = []
        self.colour = colour
        self.mass = mass
        self.radius = radius
        self.clicked_on = False
        self.circleRect = 0
        self.text = []
        self.enableTxt = False
        self.AU = 0
        self.radius_vector = 0
        self.full_rotation_points = []
        self.rotated = False
        self.default_vals = True

    # ------Modifiable planet elements-----#
        self.eccentricity = 0
        self.orbit_incl = 0
        self.long_asc_node = 0
        self.long_perihelion = 0

    def get_planet_elements(self, planet, jul_centuries):

        global k, long_perihelion, long_asc_node, orbit_incl
        k = 0

        i = planet_lst.index(planet)

        planet_elements = all_planetElements[i]
        planet_rates = all_planetRates[i]

        if solar_system.instances[i+1].default_vals:
            self.AU = planet_elements[0] + (planet_rates[0] * jul_centuries)  # AU (CONSTANT) aGen
            self.eccentricity = planet_elements[1] + (planet_rates[1] * jul_centuries)  # CONSTANT eGen
        else:
            print(self.name)

        orbit_incl = planet_elements[2] + (planet_rates[2] * jul_centuries)  # ORBIT INCLINCATION: CONSTANT iGen
        self.orbit_incl = orbit_incl % 360
        long_asc_node = planet_elements[5] + (
                planet_rates[5] * jul_centuries)  # LONGITUDE OF ASCENDING NODE (CONSTANT) WGen
        self.long_asc_node = long_asc_node % 360

        long_perihelion = planet_elements[4] + (planet_rates[4] * jul_centuries)  # LONGITUDE OF PERIHELION wGen
        self.long_perihelion = long_perihelion % 360
        if self.long_perihelion < 0:
            self.long_perihelion = 360 + self.long_perihelion

        orbit_pos = planet_elements[3] + (planet_rates[3] * jul_centuries)  # LGen
        orbit_pos = orbit_pos % 360

        if orbit_pos < 0:
            orbit_pos = 360 + orbit_pos
        mean_anomaly = orbit_pos - self.long_perihelion

        if mean_anomaly < 0:
            mean_anomaly = 360 + mean_anomaly
        k = math.pi / 180.0

        eccentric_anomaly = calc_ecc_anomaly(self.eccentricity, mean_anomaly, 6, k)
        anomaly_arg = (math.sqrt((1 + self.eccentricity) / (1 - self.eccentricity))) * (
            math.tan(to_radians(eccentric_anomaly) / 2))

        if anomaly_arg < 0:
            true_anomaly = 2 * (math.atan(anomaly_arg) / k + 180)  # atan = inverse tan
        else:
            true_anomaly = 2 * (math.atan(anomaly_arg) / k)

        self.radius_vector = self.AU * (1 - (self.eccentricity * (math.cos(to_radians(eccentric_anomaly)))))  # rGen

        planet_x = self.radius_vector * (math.cos(to_radians(self.long_asc_node))
                                    * math.cos(to_radians(true_anomaly + self.long_perihelion - self.long_asc_node))
                                    - math.sin(to_radians(self.long_asc_node))
                                    * math.sin(to_radians(true_anomaly + self.long_perihelion - self.long_asc_node))
                                    * math.cos(to_radians(self.orbit_incl)))
        planet_y = self.radius_vector * (math.sin(to_radians(self.long_asc_node))
                                    * math.cos(to_radians(true_anomaly + self.long_perihelion - self.long_asc_node))
                                    + math.cos(to_radians(self.long_asc_node))
                                    * math.sin(to_radians(true_anomaly + self.long_perihelion - self.long_asc_node))
                                    * math.cos(to_radians(self.orbit_incl)))

        return planet_x, planet_y

    def generate_mini_info(self, planet):
        dict_lst = [sun_facts, mercury_stats, venus_stats, earth_stats, mars_stats, jupiter_stats, saturn_stats,
                    uranus_stats, neptune_stats]
        i = solar_system.instances.index(planet)
        planet_dict = dict_lst[i]
        self.text.append(self.name)
        for key, value in planet_dict.items():
            self.text.append(str(key) + ": " + str(value))

    def display_planet_txt(self, y, move_y):
        label = []
        y_val = 20
        if self.enableTxt:
            for line in range(1, len(self.text)):
                label.append(font.render(self.text[line], True, solar_system.txt_colour))
            for line in label:
                window.blit(line, (self.circleRect.topright[0] + 100, y + y_val + move_y))
                y_val += 20
            blit_line(f'Distance from the sun: {round(self.radius_vector, 3)} AU', self.circleRect.topright[0] + 100, y + y_val + move_y, 20)

    def draw(self, draw_line, shift_x, shift_y):  # radius scale
        global line_endx
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = -y * self.SCALE + HEIGHT / 2
                updated_points.append((x + shift_x, y + shift_y))
            if draw_line:
                pygame.draw.lines(window, self.colour, False, updated_points, 1)
        self.circleRect = pygame.draw.circle(window, self.colour, (x + shift_x, y + shift_y), self.radius)

        if self.circleRect.collidepoint(pygame.mouse.get_pos()) or self.clicked_on:
            outer_circle_rect = pygame.draw.circle(window, solar_system.txt_colour, (x + shift_x, y + shift_y), self.radius + 5, width=1)
            line_endx = outer_circle_rect.midright[0] + 100
            pygame.draw.line(window, solar_system.txt_colour, (x + shift_x, y + shift_y), (line_endx, y + shift_y))
            name_txt = font.render(self.name, True, self.colour)
            window.blit(name_txt, (line_endx + 10, y - 5 + shift_y))
            self.display_planet_txt(y, shift_y)

    def update_scale(self, scale):
        self.radius *= scale

    def check_fully_rotated(self):
        dp = 12
        count = 0
        # if round(self.x, dp) == round(self.startx, dp):
        #     if round(self.y, dp) == round(self.starty, dp):

        x_diff = abs(-self.startx + self.circleRect.x)
        y_diff = abs(-self.starty + self.circleRect.y)
        ticks = pygame.time.get_ticks()






        if y_diff == 120:
                print('sdad')
                self.rotated = True

        # print([self.circleRect.x, self.startx])
        # print([self.circleRect.y, self.starty])


def hex_to_rgb(value):
    rgb = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def create_sub_windows(leftwidth, leftheight, rightwidth, height):
    rgb = solar_system.overlay_colour
    rgb = rgb + (200,)
    draw_rect_alpha(window, rgb, (leftwidth, 0, leftwidth, height))





def create_planets():
    global solar_system, sun
    solar_system = Solarsystem(1)
    sun = Planet('Sun', 'yellow', 8, 20)  # sun position is centre of the screen
    sun.x = 0
    sun.y = 0
    mercury = Planet('Mercury', 'grey', 0.330, 2)
    venus = Planet('Venus', '#D8BE8E', 4.87, 6)
    earth = Planet('Earth', 'blue', 5.97, 6)
    mars = Planet('Mars', 'red', 0.642, 4)
    jupiter = Planet('Jupiter', '#F6F0E3', 1898, 10)
    saturn = Planet('Saturn', '#F3CE89', 568, 9)
    uranus = Planet('Uranus', '#2BC7B4', 86.8, 8)
    neptune = Planet('Neptune', 'dark blue', 102, 8)

    space_entites = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    for entity in space_entites:
        solar_system.instances.append(entity)
        entity.generate_mini_info(entity)


def get_planet_coords(century, boolean, move_x, move_y, disable_movement, first_run):
    solar_system.instances[0].draw(boolean, move_x, move_y)
    if not disable_movement:
        mercury_x, mercury_y = solar_system.instances[1].get_planet_elements('Mercury', century)
        venus_x, venus_y = solar_system.instances[2].get_planet_elements('Venus', century)
        earth_x, earth_y = solar_system.instances[3].get_planet_elements('Earth', century)
        mars_x, mars_y = solar_system.instances[4].get_planet_elements("Mars", century)

        jupiter_x, jupiter_y = solar_system.instances[5].get_planet_elements('Jupiter', century)
        saturn_x, saturn_y = solar_system.instances[6].get_planet_elements('Saturn', century)
        uranus_x, uranus_y = solar_system.instances[7].get_planet_elements('Uranus', century)
        neptune_x, neptune_y = solar_system.instances[8].get_planet_elements('Neptune', century)

        planetxvals = [mercury_x, venus_x, earth_x, mars_x, jupiter_x, saturn_x, uranus_x, neptune_x]
        planetyvals = [mercury_y, venus_y, earth_y, mars_y, jupiter_y, saturn_y, uranus_y, neptune_y]

        for i in range(1, len(solar_system.instances)):  # to miss out the sun
            solar_system.instances[i].x = planetxvals[i - 1]
            solar_system.instances[i].y = planetyvals[i - 1]
            solar_system.instances[i].draw(boolean, move_x, move_y)
            if first_run:
                solar_system.instances[i].startx = solar_system.instances[i].circleRect.x
                solar_system.instances[i].starty = solar_system.instances[i].circleRect.y




            point = (solar_system.instances[i].x, solar_system.instances[i].y)


            # if len(solar_system.instances[1].orbit) > 300:
            #     solar_system.instances[1].orbit = []


            solar_system.instances[i].orbit.append(point)

            if solar_system.instances[i].rotated == False:
                solar_system.instances[i].full_rotation_points.append(point)



            solar_system.instances[i].orbit.append(point)
            # print(solar_system.instances[i].rotated)


            # print(len(solar_system.instances[1].full_rotation_points))
        solar_system.instances[1].check_fully_rotated()



    else:
        for i in range(len(solar_system.instances)):
            solar_system.instances[i].draw(boolean, move_x, move_y)


def show_planet_info():
    for i in range(len(solar_system.instances)):
        if solar_system.instances[i].clicked_on:
            blit_text(window, solar_system_info[i], (1395, 350), solar_system.txt_colour)
            window.blit(imgs[i], (1470, 150))

            return
    blit_text(window, system_info, (1370, 350), solar_system.txt_colour)
    window.blit(solarSystemImg, (1450, 200))


def blit_line(text, x, y, size):
    font = pygame.font.SysFont('Consolas', size)
    line = font.render(text, True, solar_system.txt_colour)
    window.blit(line, (x, y))


def show_controls():
    left_labels_y = 50
    left_side_tips = [f"Speed: {solar_system.speed_multiplier}x",
                      "S: enable / disable orbit line", "Arrow keys:move screen",
                      "Mouse right-click: enable / disable planet info",
                      "C: Centre screen"]

    for i in left_side_tips:
        blit_line(i, 20, left_labels_y, 20)
        left_labels_y += 30


def change_page(settings_apply_bool, info_bool, instructions_bool, physics_bool, settings_bool):
    global info_flag, show_instructions, display_menu, show_settings
    info_flag = info_bool
    show_instructions = instructions_bool
    display_menu = physics_bool
    show_settings = settings_bool
    show_apply_btn = settings_apply_bool

def set_default_elements(index, sliders, combo_selected):
    planet = solar_system.instances[index+1]

    if planet.default_vals:
        sliders[0].setValue(planet.AU)
        sliders[1].setValue(planet.eccentricity)
    else:
        for slider in sliders:
            if slider.selected:
                planet.orbit = []
        if combo_selected:
            sliders[0].setValue(planet.AU)
            sliders[1].setValue(planet.eccentricity)
        planet.AU = sliders[0].getValue()
        planet.eccentricity = sliders[1].getValue()
        # planet.orbit_incl = sliders[2].getValue()
        # planet.long_asc_node = sliders[3].getValue()
        # planet.long_perihelion = sliders[4].getValue()


def blit_text(surface, text, pos, color, font=pygame.font.SysFont('Consolas', 15)):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def change_res(index):
    global window
    resolutions = ["Native fullscreen", "1920 x 1080", "1280 x 720", "2560 x 1440", "3840 x 2160"]
    chosen_res = resolutions[index]
    if index == 0:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        t = chosen_res.split('x')
        width = int(t[0])
        height = int(t[1])

        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)



def main():
    global WIDTH, HEIGHT, new_date, window
    count = 0

    drawline = True
    sim_running = True
    date_editing = False
    first_run = True
    reset_orbit = False


    leftwidth = window.get_width() * 0.7
    leftheight = window.get_height() * 0.95
    rightwidth = window.get_width() * 0.3
    topheight = window.get_height() * 0.05
    height = window.get_height()


    create_planets()




    planet_info_btn = button(1450, 100, 90, 22, 'INFO')
    physics_btn = button(1700, 100, 130, 22, 'ADJUST PHYSICS')
    settings_btn = button(1600, 1050, 90, 22, 'SETTINGS')
    instructions_btn = button(1560, 100, 120, 22, 'INSTRUCTIONS')
    submit_btn = button(1750, 900, 120, 22, 'SUBMIT')
    default_vals_btn = button(1750, 1000, 120, 22, 'DEFAULT VALS')
    custom_vals_btn = button(1750, 800, 120, 22, 'CUSTOM VALS')
    reset_planet_vals_btn = button(1750, 900, 120, 22, 'RESET PLANET VALS')

    planet_info_btn.button_clicked = True
    default_vals_btn.button_clicked = True



    shift_x = 0
    shift_y = 0
    year, day, month = 2000, 1, 1

    leftrect = pygame.Rect([0, topheight], [leftwidth, leftheight])
    leftsurf = window.subsurface(leftrect)
    WIDTH = leftsurf.get_width()    # main simulation width and height
    HEIGHT = leftsurf.get_height()



    julian_epoch = gregorian_to_julian(2000, 1, 1)  # initialise julian epoch
    jul_century_in_jul_days = 36525

    date_textbox, sliders, physics_combo_box, theme_comboBox, side_labels, val_outputs, fps_textbox, res_dropdown = generate_menu(window, solar_system)
    fps = 60

    fps_textbox.setText(text=str(fps))
    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)





        element_labels_y = 310
        shift_distance = 10

        window.fill(solar_system.window_colour)

        blit_text(window, f'FPS: {round(clock.get_fps())}',  (20, 200), 'white')


        jul_century = ((gregorian_to_julian(year, month, day) - julian_epoch) / jul_century_in_jul_days)
        get_planet_coords(jul_century, drawline, shift_x, shift_y, date_editing, first_run)

        show_controls()
        create_sub_windows(leftwidth, leftheight, rightwidth, height)

        if sim_running:

            year, month, day = increment_date(year, month, day)
            date_textbox.setText(f'{year}-{month}-{day}')

            day += 0.4 * solar_system.speed_multiplier
            day = round(day, 2)
        else:
            blit_line('SIMULATION PAUSED', 600, 1020, 30)

            try:
                date_editing = True
                new_date = date_textbox.getText()
                date_lst = new_date.split('-')


                new_year = int(date_lst[0])

                new_month = int(date_lst[1])

                new_day = float(date_lst[2])
                new_day = int(day)

                date = f'{new_year}-{new_month}-{new_day}'


                datetime.datetime(year=new_year, month=new_month, day=new_day)
            except:
                date_editing = False



            else:
                year = int(date_lst[0])

                month = int(date_lst[1])

                day = float(date_lst[2])
                day = int(day)

                date_editing = False

        planet_info_btn.redraw(window)
        physics_btn.redraw(window)
        settings_btn.redraw(window)
        instructions_btn.redraw(window)

        solar_system.speed_multiplier = round(solar_system.speed_multiplier, 2)

        # -----------------------EVENTS--------------------------

        events = pygame.event.get()

        for event in events:
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # scroll up
                    Planet.SCALE *= 0.75
                    solar_system.update_scale(0.75)
                elif event.button == 1:  # left mouse button pressed
                    if planet_info_btn.isOver(pos):
                        if btn_clicked(planet_info_btn, (physics_btn, settings_btn, instructions_btn,submit_btn)):
                            change_page(False, True, False, False, False)

                    elif physics_btn.isOver(pos):
                        btn_clicked(physics_btn, (planet_info_btn, settings_btn, instructions_btn,submit_btn))
                        change_page(False, False, False, True, False)


                    elif settings_btn.isOver(pos):
                        btn_clicked(settings_btn, (planet_info_btn, physics_btn, instructions_btn,submit_btn))
                        change_page(False, False, False, False, True)

                    elif instructions_btn.isOver(pos):
                        btn_clicked(instructions_btn, (planet_info_btn, settings_btn, physics_btn, submit_btn))
                        change_page(False, False, True, False, False)

                    if submit_btn.isOver(pos):
                        submit_btn.button_clicked = True
                    if custom_vals_btn.isOver(pos):
                        custom_vals_btn.button_clicked = True
                    if default_vals_btn.isOver(pos):
                        default_vals_btn.button_clicked = True

                    if reset_planet_vals_btn.isOver(pos):
                        reset_planet_vals_btn.button_clicked = True

                    for planet in solar_system.instances:
                        if planet.circleRect.collidepoint(pygame.mouse.get_pos()):
                            if planet.clicked_on:
                                planet.clicked_on = False
                            else:
                                planet.clicked_on = True

                elif event.button == 3:
                    for planet in solar_system.instances:
                        if planet.circleRect.collidepoint(pygame.mouse.get_pos()):
                            if not planet.enableTxt:
                                planet.enableTxt = True
                            else:
                                planet.enableTxt = False
                elif event.button == 4:  # scroll down
                    Planet.SCALE *= 1.25
                    for planet in solar_system.instances:
                        planet.update_scale(1.25)

            if event.type == pygame.KEYDOWN:  # if key pressed
                if event.key == pygame.K_s:
                    if drawline:
                        drawline = False
                    else:
                        drawline = True
                elif event.key == pygame.K_SPACE:
                    if sim_running:
                        sim_running = False
                    else:
                        sim_running = True
                elif event.key == pygame.K_a:
                    solar_system.speed_multiplier -= 0.15
                elif event.key == pygame.K_d:
                    solar_system.speed_multiplier += 0.15
                elif event.key == pygame.K_c:
                    shift_x, shift_y = -sun.x * sun.SCALE, -sun.y * sun.SCALE

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            shift_x += shift_distance
        elif keys[pygame.K_RIGHT]:
            shift_x -= shift_distance
        elif keys[pygame.K_UP]:
            shift_y += shift_distance
        elif keys[pygame.K_DOWN]:
            shift_y -= shift_distance




        # ------------------------------------------------------------#



        physics_combo_box.update(events)
        theme_comboBox.update(events)
        res_dropdown.update(events)
        pygame_widgets.update(events)





        if info_flag:
            show_planet_info()

        elif show_settings:
            fps_textbox.draw()

            fps_textbox.show()
            submit_btn.redraw(window)

            if submit_btn.button_clicked:
                solar_system.theme = theme_comboBox.selected
                change_res(res_dropdown.selected)
                submit_btn.button_clicked = False
                date_textbox.colour = solar_system.window_colour
                date_textbox.textColour = 'red'
                solar_system.check_theme(theme_comboBox)
                fps = float(fps_textbox.getText())

            theme_comboBox.draw(window)
            res_dropdown.draw(window)
            # print(res_dropdown.selected)

        if not show_settings:
            fps_textbox.hide()



        if display_menu:
            for i in range(len(sliders)):
                sliders[i].show()
                val_outputs[i].show()
                val_outputs[i].setText(round(sliders[i].getValue(), 9))

            blit_line('ADJUST PHYSICS', 1500, 230, 30)
            for i in side_labels:
                blit_line(i, 1370, element_labels_y, 20)
                element_labels_y += 100

            planet = solar_system.instances[(physics_combo_box.selected)+1]
            buttons = [custom_vals_btn, default_vals_btn, reset_planet_vals_btn]

            if custom_vals_btn.button_clicked:
                for btn in buttons:
                    btn.button_clicked = False
                    btn.highlight_btn = False
                custom_vals_btn.highlight_btn = True
                planet.default_vals = False

            elif default_vals_btn.button_clicked:
                for btn in buttons:
                    btn.button_clicked = False
                    btn.highlight_btn = False
                default_vals_btn.highlight_btn = True
                solar_system.default_vals = True
                planet.orbit = []
                planet.default_vals = True

            elif reset_planet_vals_btn.button_clicked:
                for btn in buttons:
                    btn.button_clicked = False
                    btn.highlight_btn = False
                planet.default_vals = True
                planet.orbit = []
                reset_planet_vals_btn.highlight_btn = True


            set_default_elements(physics_combo_box.selected, sliders, physics_combo_box.clicked_on_option)
            # set_val_bools(custom_vals_btn, default_vals_btn, physics_combo_box, count)







            default_vals_btn.redraw(window)
            custom_vals_btn.redraw(window)
            physics_combo_box.draw(window)
            reset_planet_vals_btn.redraw(window)

        elif not display_menu:
            for i in range(len(sliders)):
                sliders[i].hide()
                val_outputs[i].hide()
            if show_instructions:
                blit_text(window, instructions, (1400, 150), solar_system.txt_colour)
                blit_line('INSTRUCTIONS', 1550, 150, 30)
















        #pygame.draw.rect(window, 'red', pygame.Rect(0, 0, 60, 60), 2)

        if first_run:
            first_run = False




        pygame.display.update()

main()
# sdasdasd