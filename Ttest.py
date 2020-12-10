from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from rpi_ws281x import *
import argparse


# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
cycleChekerMode= True
html = '''<html>
              <head>
              <meta charset="utf-8">
              <title>Стили</title>
              <link rel="stylesheet" href="mainst.css">
              </head>
              <script type="text/javascript" charset="utf-8">
                    function httpGetAsync(method, callback) {
                        var xmlHttp = new XMLHttpRequest();
                        xmlHttp.onreadystatechange = function() {
                            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                                callback(xmlHttp.responseText);
                        }
                        xmlHttp.open("GET", window.location.href + method, true);
                        xmlHttp.send(null);
                    }
                    function rainbow() {
                        console.log("Rainbow");
                        httpGetAsync("rainbow/on", function(){ console.log("rainbowDone"); });
					}	
					function chaserainbowrainbow() {
                        console.log("ChaseRainbow");
                        httpGetAsync("chaserainbow/on", function(){ console.log("ChaseRainbowDone"); });
					}	
					function theaterchase() {
                        console.log("theaterChase");
                        httpGetAsync("theaterchase/on", function(){ console.log("theaterChaseDone"); });
					}
                    function ledOff() {
                        console.log("Led OFF...");
                        httpGetAsync("led/off", function(){ console.log("Done"); });
                    }
              </script>
              <body>
				 <br></br>
				 <br></br>
                 <h1>HAPPY NEW YEAR 2020!<h1>
				 <br></br>
				 <p><button class="button button_led" onclick="Rainbow();">Rainbow</button></p>
				 <p><button class="button button_led" onclick="ChaseRainbow();">Chase Rainbow</button></p>
				 <p><button class="button button_led" onclick="theaterChase()">theater Chase</button></p>
				 <p><button class="button button_led" onclick="ledOff();">Led OFF</button></p
              </body>
            </html>'''

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
       # if self.path == "/":
       #     self.send_response(200)
       #     self.send_header('Content-type', 'text/html')
       #     self.end_headers()
       #     self.wfile.write(html.encode('utf-8'))
       # else:
       #     self.send_error(404, "Page Not Found {}".format(self.path))

      # print("GET request, Path:", self.path)
      # if self.path == "/" or self.path.endswith("/led/on") or self.path.endswith("/led/off"):
      #     if self.path.endswith("/led/on"):
      #         rainbow(strip)
      #     if self.path.endswith("/led/off"):
      #         colorWipe(strip, Color(0,0,0), 10)
      #    self.send_response(200)
      #     self.send_header('Content-type', 'text/html')
      #     self.end_headers()
      #     self.wfile.write(html.encode('utf-8'))
      # else:
      #     self.send_error(404, "Page Not Found {}".format(self.path))
      # Create NeoPixel object with appropriate configuration.
       strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
       strip.begin()

       print("GET request, path:", self.path)
       if self.path == "/":
           self.send_response(200)
           self.send_header('Content-type', 'text/html')
           self.end_headers()
           self.wfile.write(html.encode('utf-8'))
       elif self.path == "rainbow/on":
           self.send_response(200)
           self.send_header('Content-type', 'text/plain')
           self.end_headers()
           rainbow(strip)
           #cycleCheker(strip)
           #cycleChekerMode = True
           self.wfile.write("OK")
       elif self.path == "chaserainbow/on":
           self.send_response(200)
           self.send_header('Content-type', 'text/plain')
           self.end_headers()
           theaterChaseRainbow(strip)
           #cycleCheker(strip)
           #cycleChekerMode = True
           self.wfile.write("OK")
       elif self.path == "theaterchase/on":
           self.send_response(200)
           self.send_header('Content-type', 'text/plain')
           self.end_headers()
           theaterChase(strip, Color(100,100,100))
           #cycleCheker(strip)
           #cycleChekerMode = True
           self.wfile.write("OK")
       elif self.path == "/led/off":
           self.send_response(200)
           self.send_header('Content-type', 'text/plain')
           self.end_headers()
           #cycleCheker(strip)
           #cycleChekerMode = False
           colorWipe(strip, Color(0,0,0), 10)
           self.wfile.write("OK")
       else:
           self.send_error(404, "Page Not Found {}".format(self.path))
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)



def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)
#def rasperrypi_pinout(strip, value: bool):
#   print("LED ON" if value else "LED OFF")
#    try:
#        rainbow(strip)
#    except:
#        pass

def rasperrypi_cleanup():
    try:
        GPIO.cleanup()
    except:
        pass
def cycleCheker (strip):
    while cycleChekerMode:
        rainbow(strip)
#def raspberrypi_on():
#    try:
# colorWipe()
#    except:
#        pass

def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
       # while cycleCheker:
       #     rainbowCycle(strip)
    except KeyboardInterrupt:
        pass
    httpd.server_close()




if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
   # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
   # strip.begin()

   # try:
   #    while cycleChekerMode:
   #          rainbowCycle(strip)
   #          Print("OK")
   # except:
   #     print("Something went wrong")
   # else:
   #     print("Nothing went wrong")
