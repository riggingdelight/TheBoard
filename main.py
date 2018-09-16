import neopixel
import time
import board
import math
import random
import digitalio



pixpin = board.D2
numpix = 63


### Makes the list of different slots so later we can treat them as an object
#
# [ [Slot 0 Start Pixel, Slot 0 End Pixel], [Slot 1 Start Pixel, Slot 1 End Pixel], ... ]

slot=[[0,5],[6,11],[12,17],[18,23],[39,44],[45,50],[51,56],[57,62]]

strip = neopixel.NeoPixel(pixpin, numpix, brightness=1)



pullcord = digitalio.DigitalInOut(board.D0)
pullcord.direction = digitalio.Direction.INPUT
pullcord.pull = digitalio.Pull.DOWN


def MakeRainbow(incr, freq1, freq2, freq3, phase1, phase2, phase3, center, width):
    #Highly stolen from https://krazydad.com/tutorials/makecolors.php
    red = math.sin(freq1 * incr + phase1) * width + center
    green = math.sin(freq2 * incr + phase2) * width + center
    blue = math.sin(freq3 * incr + phase3) * width + center
    
    pixelcolour = (int(red),int(green),int(blue))
    
    return pixelcolour

def WaitRainbowSmile(timetowait,qty):
    endtimes = time.monotonic() + timetowait
    while time.monotonic() < endtimes:
        
        smile = [24,38]
        smilei = smile[0]
        
        for x in range(0,qty):

            strip[smilei] = MakeRainbow(x,.1,.2,.3,0,0,0,127,128)
            #print("x: "+ str(x/255) + " i: " + str(smilei) + " : " +  str(strip[i]))
            strip.write()
                
            if smilei < smile[1]:
                smilei += 1
            else:
                smilei = smile[0]
            time.sleep(.1)
            

def FillPixels(pxstart, pxend, pxcolour):
        for x in range(pxstart,pxend+1):
            strip[x] = pxcolour
            
def callback():
        FillPixels(0,62,(100,100,100))


while True:
        
    for i in range(0, numpix):
    #  strip[i] = (int(math.sin(i/5)*255),int(math.sin(i/32)*255),int(math.sin(i/10)*255))
    #   print(strip[i])
        strip[i] = MakeRainbow(i,.1,.2,.3,0,0,0,127,128)
        strip.write()
        time.sleep(.05)
     
        
    for i in range(0,numpix):
        strip[i] = (0,0,0)
        
    winner = random.randint(0,7)

    for i in range(slot[winner][0],slot[winner][1]):
        strip[i] = (0,255,0)
        print(strip[i])
    print("Winner: " + str(winner))
        
    strip.write()
    


    WaitRainbowSmile(1,100)
    
    while pullcord.value == False:
        
        FillPixels(24,38,(100,0,100))
        time.sleep(.02)
