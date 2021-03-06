#!/usr/bin/env python3

import os
import time
from datetime import datetime 
from typing import List

from inky.inky_uc8159 import Inky
# To simulate:
#from inky.mock import InkyMockImpression as Inky
from inky.auto import auto

from font_source_sans_pro import SourceSansProLight
from font_source_sans_pro import SourceSansPro
from font_source_sans_pro import SourceSansProSemibold
from PIL import Image, ImageDraw, ImageFont

from events import Events
from gcal import Google_Calendar 

inky = Inky()
light_font = ImageFont.truetype(SourceSansProLight, 14)
normal_font = ImageFont.truetype(SourceSansPro, 14)
semibold_font = ImageFont.truetype(SourceSansProSemibold, 14)

BLACK=(0,0,0)
WHITE=(255, 255, 255)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
RED=(255, 0, 0)
YELLOW=(255, 255, 0)
ORANGE=(255, 140, 0)
CLEAR=(255, 255, 255)

DESATURATED_PALETTE = [
    (0, 0, 0),
    (255, 255, 255),
    (0, 255, 0),
    (0, 0, 255),
    (255, 0, 0),
    (255, 255, 0),
    (255, 140, 0),
    (255, 255, 255)
]

SATURATED_PALETTE = [
    (57, 48, 57),       #   BLACK
    (255, 255, 255),    #   WHITE
    (58, 91, 70),       #   GREEN?
    (61, 59, 94),       #   BLUE?
    (156, 72, 75),      #   YELLOW?
    (208, 190, 71),     #   ORANGE?
    (177, 106, 73),     #   RED?
    (255, 255, 255)     #   CLEAR
]

colors = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']

PATH = os.path.dirname(__file__)

img = Image.open(os.path.join(PATH, "resources/backdrop.png")).resize(inky.resolution)
draw = ImageDraw.Draw(img)

def draw_day_headers(box_width:int):
    draw.rectangle((1, 1, 600, 20), fill=BLUE)
    draw.text(((box_width*0)+30,2), "MON" , WHITE, font=semibold_font)
    draw.text(((box_width*1)+30,2), "TUE" , WHITE, font=semibold_font)
    draw.text(((box_width*2)+30,2), "WED" , WHITE, font=semibold_font)
    draw.text(((box_width*3)+30,2), "THU" , WHITE, font=semibold_font)
    draw.text(((box_width*4)+30,2), "FRI" , WHITE, font=semibold_font)
    draw.text(((box_width*5)+30,2), "SAT" , WHITE, font=semibold_font)
    draw.text(((box_width*6)+30,2), "SUN" , WHITE, font=semibold_font)

def draw_day(x:int, y:int, box_width:int, box_height:int, today_string:str, events:List[str], today=False):
    date_box_height = 15
    # draw date background
    colour = RED
    if today:
        colour = GREEN
    draw.rectangle((x, y, x+box_width, y+date_box_height), 
                    fill=colour)
    draw.rectangle((x, y+date_box_height, x+box_width, y+box_height), 
                    fill=WHITE)

    # write date
    center_start_pos = 0
    if len(today_string) == 6:
        center_start_pos = 22
    elif len(today_string) == 5:
        center_start_pos = 27

    # date header
    draw.text((x + center_start_pos, y-2), today_string , WHITE, font=semibold_font)

    # general y offset
    offset_y = y + (date_box_height -2)

    # event strings
    if len(events) > 0:
        event_y = offset_y
        event_x = x + 2
        event_count = 0
        for event in events:
            if event_count < 20:
                friendly_time = event.start.strftime("%H:%M")
                if event.end:
                    friendly_time_end = event.end.strftime("%H:%M")
                    friendly_time = str("%s - %s" % (friendly_time, friendly_time_end))
                    draw.text((event_x, event_y), event.title[:13] , BLUE, font=normal_font)
                    draw.text((event_x, event_y+13), friendly_time , GREEN, font=normal_font)
                
                event_y = event_y + 30
                event_count = event_count +1

    # draw containing box
    right_edge = x+box_width
    if right_edge > 598:
        right_edge = 598
        
    draw.line((x, offset_y, right_edge, offset_y), colour)
    draw.line((x, offset_y, x, offset_y+box_height), colour)
    

calendar_data = Google_Calendar()

x = 1
x_max = 600
y = 21
y_max = 488
day_count = 0
box_width = 86
box_height = 93
today = calendar_data.events.get_day_from_dt(datetime.now())
draw_day_headers(box_width)
for day in calendar_data.events.dates:
    events = calendar_data.events.find_events_by_day(day)

    datetime_day = None
    friendly_day = calendar_data.events.remove_year_from_friendly_date(day)
    if day_count < 28:
        todays_the_day = False
        if today == day:
            todays_the_day = True
        draw_day(x, y, box_width, box_height, friendly_day, events, todays_the_day)
        day_count = day_count + 1
    if x < x_max - 150:
        x = x + box_width
    else:
        x = 1
        y = y + box_height + 15

# right and bottom edges
draw.line((598,0,598,446), RED)
draw.line((0,446,598,446), RED)

inky.set_image(img, saturation=1)
inky.show()
# To simulate:
#inky.wait_for_window_close()
