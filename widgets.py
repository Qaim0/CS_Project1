import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from button_class import Dropdown






#ccentricity
# orbit incl : between 2.4 and 180.0
# long - asc node : between 4.8 and 360.0
# long - perihelion : between 4.8 and 360.0
# eccentric anomaly :

def create_widgets(win, accent_colour, colour, font):
    date_textbox = TextBox(win, 10, 0, 170, 45, textColour=accent_colour,
                           fontSize=25, borderThickness=0, font=font, colour=colour)

    lables = ['Select mass', 'semi-major axis', 'Eccentricity']
    planets = Dropdown(
        1750, 300, 160, 40, colour, accent_colour, font,
        ["Mercury", "Venus", "Earth", "Mars", "Jupiter"])

    # for semi major axis
    slider1 = Slider(win, 1620, 410, 150, 10, min=0.02, max=5, step=0.01, initial=0.2)
    output1 = TextBox(win, 1800, 400, 85, 30, fontSize=20, borderThickness=0)

    # for eccentricity
    slider2 = Slider(win, 1620, 510, 150, 10, min=0.00000001, max=0.989, step=0.001,
                     initial=0.02)
    output2 = TextBox(win, 1800, 500, 85, 30, fontSize=20, borderThickness=0)

    outputs = [output1, output2]
    sliders = [slider1, slider2]

    # FOR GRAPHS

    graph_type = Dropdown(1750, 300, 160, 40, colour, accent_colour, font,
                          ["Distance", "True Anomaly"])
    planet1 = Dropdown(1750, 400, 160, 40, colour, accent_colour, font,
                       ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",
                        "Neptune"])
    planet2 = Dropdown(1750, 500, 160, 40, colour, accent_colour, font,
                       ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn",
                        "Uranus", "Neptune"])

    themes = Dropdown(
        1750, 300, 160, 40, colour, accent_colour, font,
        ["Dark Standard", "Dark blue", "light"])
    themes.selected = 1  # set to dark blue

    # Graph background colours
    graph_bg = Dropdown(1750, 500, 150, 45, colour, accent_colour, font,
                        ['Grey', 'dark blue', 'white'])
    # graph line colours
    graph_line = Dropdown(1750, 600, 150, 45, colour, accent_colour, font,
                          ['red', 'blue', 'green'])
    # simulation accent colours
    accent_colours = Dropdown(1750, 700, 150, 45, colour, accent_colour, font,
                              ['red', 'yellow', 'blue', 'orange', 'white'])
    # metric options
    metric = Dropdown(1750, 800, 150, 45, colour, 'orange', font, ['KM', 'AU'])
    # fps options
    fps = Dropdown(1750, 400, 150, 45, colour, 'orange', font, ['60', '120', '144'])

    return date_textbox, sliders, planets, outputs, lables, graph_type, \
           planet1, planet2, themes, graph_bg, graph_line, accent_colours, metric, fps
    # lists = comboboxes



#
#
# def create_widgets(win, accent_colour, colour, font):
#     lables = ['Select mass', 'semi-major axis', 'Eccentricity']
#     planets = Dropdown(
#         1750, 300, 160, 40, colour, accent_colour, font,
#         ["Mercury", "Venus", "Earth", "Mars", "Jupiter"])
#
#     themes = Dropdown(
#         1750, 300, 160, 40, colour, accent_colour, font,
#         ["Dark Standard", "Dark blue", "light"])
#     themes.selected = 1 # set to dark blue
#
#     graph_background = Dropdown(1750, 500, 150, 45, colour, 'orange', font, ['Grey', 'dark blue', 'white'])
#     graph_line = Dropdown(1750, 600, 150, 45, colour, 'orange', font, ['red', 'blue', 'green'])
#     accent_colours = Dropdown(1750, 700, 150, 45, colour, 'orange', font, ['red', 'yellow', 'blue', 'orange', 'white'])
#
#     slider1 = Slider(win, 1620, 410, 150, 10, min=0.02, max=5, step=0.01)  # for semi major axis
#     slider2 = Slider(win, 1620, 510, 150, 10, min=0.00000001, max=0.989, step=0.001)  # for eccentricity
#
#
#     output1 = TextBox(win, 1800, 400, 85, 30, fontSize=20, borderThickness=0)
#     output2 = TextBox(win, 1800, 500, 85, 30, fontSize=20, borderThickness=0)
#     metric =  Dropdown(1750, 800, 150, 45, colour, 'orange', font, ['KM', 'AU'])
#
#     fps = Dropdown(1750, 400, 150, 45, colour, 'orange', font, ['60', '120', '144'])
#     metric =  Dropdown(1750, 800, 150, 45, colour, 'orange', font, ['KM', 'AU'])
#
#     date_textbox = TextBox(win, 10, 0, 170, 45, textColour=colour, fontSize=25, borderThickness=0, font=font)
#
#     # graph optionboxes
#
#
#     graph_type = Dropdown(1750, 300, 160, 40, colour, 'orange', font,
#                           ["Distance", "True Anomaly"])
#     planet1 = Dropdown(1750, 400, 160, 40, colour, 'orange', font,
#                        ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
#     planet2 = Dropdown(1750, 500, 160, 40, colour, 'orange', font,
#                        ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
#
#     outputs = [output1, output2]
#     sliders = [slider1, slider2]
#     return date_textbox, sliders, planets, themes, lables, outputs, fps, graph_type, planet1, planet2, graph_background, graph_line, accent_colours, metric
#     # lists = comboboxes

#ccentricity
# orbit incl : between 2.4 and 180.0
# long - asc node : between 4.8 and 360.0
# long - perihelion : between 4.8 and 360.0
# eccentric anomaly :



# def create_widgets(win, solar_system):
#     lables = ['Select mass', 'semi-major axis', 'Eccentricity']
#     planets = Dropdown(
#         1750, 300, 160, 40, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30),
#         ["Mercury", "Venus", "Earth", "Mars", "Jupiter"])
#     themes = Dropdown(
#         1750, 300, 160, 40, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30),
#         ["Dark Standard", "Dark blue", "light"])
#     themes.selected = 1 # set to dark blue
#
#     graph_background = Dropdown(1750, 500, 150, 45, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30), ['Grey', 'dark blue', 'white'])
#     graph_line = Dropdown(1750, 600, 150, 45, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30), ['red', 'blue', 'green'])
#     accent_colours = Dropdown(1750, 700, 150, 45, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30), ['red', 'yellow', 'blue', 'orange', 'white'])
#
#     slider1 = Slider(win, 1620, 410, 150, 10, min=0.02, max=5, step=0.01)  # for semi major axis
#     slider2 = Slider(win, 1620, 510, 150, 10, min=0.00000001, max=0.989, step=0.001)  # for eccentricity
#
#
#     output1 = TextBox(win, 1800, 400, 85, 30, fontSize=20, borderThickness=0)
#     output2 = TextBox(win, 1800, 500, 85, 30, fontSize=20, borderThickness=0)
#     metric =  Dropdown(1750, 800, 150, 45, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30), ['KM', 'AU'])
#
#     fps = Dropdown(1750, 400, 150, 45, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30), ['60', '120', '144'])
#
#     date_textbox = TextBox(win, 10, 0, 170, 45, textColour=solar_system.sim_accent_colour, fontSize=25, borderThickness=0, font=pygame.font.SysFont('Consolas', int(20)))
#
#     # graph optionboxes
#
#
#     graph_type = Dropdown(1750, 300, 160, 40, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30),
#                           ["Distance", "True Anomaly"])
#     planet1 = Dropdown(1750, 400, 160, 40, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30),
#                        ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
#     planet2 = Dropdown(1750, 500, 160, 40, solar_system.overlay_colour, 'orange', pygame.font.SysFont(None, 30),
#                        ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
#
#     outputs = [output1, output2]
#     sliders = [slider1, slider2]
#     return date_textbox, sliders, planets, themes, lables, outputs, fps, graph_type, planet1, planet2, graph_background, graph_line, accent_colours, metric
    # lists = comboboxes
