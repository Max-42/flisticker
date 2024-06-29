

import os
from flask import Flask, flash, json, make_response, redirect, render_template, request, send_file, url_for

from flask import Flask, render_template_string
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageDraw

from lib.auth import is_admin, token_required

from requests.exceptions import Timeout

import threading


from flask import Flask



app = Flask(__name__)






@app.route('/')
def index():
	return redirect(url_for('bild'))

@app.route('/embed')
def embed():

    one = 1534789 #italy_switzerland_id
    two = 1534788 #deutschland_denenmark_id
    
    return render_template('frame.html', matchid=two)



#async deamon that fetches screenshots from /embed



# def run_scheduler():
#     schedule.every(2).seconds.do(job)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#         print("Scheduler running")


def background_task():
    options = webdriver.FirefoxOptions()
    #options.add_argument('--headless')
    
    #options.add_argument("start-maximized")
    #options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.headless = True  # Set the browser to headless mode
    profile = webdriver.FirefoxProfile()

    # Set the gfx.font_rendering.cleartype_params.rendering_mode preference to 1
    profile.set_preference('gfx.font_rendering.cleartype_params.rendering_mode', 1)
    # Disable anti-aliasing
    
    # Specify the driver version manually if needed
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get("http://127.0.0.1:40406/embed")
        

        while True:
            time.sleep(2)  # Wait for the page to load completely
            # Locate the element and get its location and size
            element = driver.find_element(By.ID, "screenshot-area")
            location = element.location
            size = element.size

            # Take a full page screenshot
            driver.save_screenshot("full_screenshot.png")

            # Open the full screenshot and crop the desired area
            image = Image.open("full_screenshot.png")
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save("stage-01.png")
            print("Screenshot taken and saved as screenshot_area.png")
            crop_screenshot()
            color_patch()
            round_corners()
            
    finally:
        driver.quit()


def crop_screenshot():
    with Image.open("stage-01.png") as img:
        left = 0
        top = 100
        right = 500
        bottom = 250
        img = img.crop((left, top, right, bottom))
        img.save("stage-02.png")



def color_patch():
    """"
    Replace all Black pixels within 0,0,50,50 with green

    """
    left = 0
    top = 120
    right = 500
    bottom = 140
    with Image.open("stage-02.png") as img:
#        for x in range(left, right):
#            for y in range(top, bottom):
#                #r, g, b, a = img.getpixel((x, y))
#                r, g, b, a = img.getpixel((x, y))
#                #img.putpixel((x, y), (0, 255, 0)) #todo remove
#                if r == 26 and g == 25 and b == 25:
#                    #print("Found black pixel at", x, y)
#
#                    img.putpixel((x, y), (0, 255, 0, a))
#                    #img.putpixel((x, y), (0, 255, 0))
        img.save("stage-03.png")

def round_corners():
    with Image.open("stage-03.png") as img:
        rad = 30  # Amount of rounding
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', img.size, 255)
        w, h = img.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        img.putalpha(alpha)
        img.save("stage-04.png")


@app.route('/screenshot')
def screenshot():
    try:
        return send_file("stage-04.png", mimetype='image/png')
    except FileNotFoundError:
        try:
            return send_file("wait.png", mimetype='image/png')
        except FileNotFoundError:
            return "No screenshot available", 404

@app.route('/bild')
def bild():
    return render_template('bild.html')

def cleanup():
    try:
        os.remove("full_screenshot.png")
        os.remove("stage-01.png")
        os.remove("stage-02.png")
        os.remove("stage-03.png")
        os.remove("stage-04.png")
    except FileNotFoundError:
        pass

if __name__ == '__main__':

    cleanup()

    bg_task = threading.Thread(target=background_task)
    #bg_task.daemon = True

    # Start the thread
    bg_task.start()

    # try:
    #     app.run(host="0.0.0.0", port=5050, debug=True)
    # except KeyboardInterrupt:
    #     pass

    app.run(host="0.0.0.0", port=40406, debug=False)

    bg_task.join() #will never be reached lol
    