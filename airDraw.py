import Leap, sys
import pygame
from pygame.locals import *

#Map
pygame.init()
screen=pygame.display.set_mode((1024,718))
pygame.display.set_caption("Leap Motion Paint")
pygame.font.init()

#Initialize Background
background = pygame.Surface((1024,718))
#set_colorkey((100,100,100))
background.fill((255,255,255))

screen.blit(background,(0,0))

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
myfont = pygame.font.SysFont("comicsansms", 40)
clearText = myfont.render("Clear", 20, black)

points = []
colors = []
currentColor = black
current = -1
first = 1
def optimize_x(x):
    return int(5*x +500)

def optimize_y(y):
    return int(1050 - 5*y+100)

def canvas():
    for point in range(len(points)):
        #print points[point]
        #pygame.draw.lines(screen, (100,100,100), False, points[point], 5)
        pygame.draw.lines(screen, colors[point], False, points[point], 5)

    #palatte
    pygame.draw.rect(screen,(235,199,158),(0,618,1024,100),0)
    pygame.draw.rect(screen,black,(0,618,1024,100),5)
    #colors
    #red
    pygame.draw.rect(screen,red,(15,633,140,70),0)
    pygame.draw.rect(screen,black,(15,633,140,70),5)
    #green
    pygame.draw.rect(screen,green,(185,633,140,70),0)
    pygame.draw.rect(screen,black,(185,633,140,70),5)
    #blue
    pygame.draw.rect(screen,blue,(355,633,140,70),0)
    pygame.draw.rect(screen,black,(355,633,140,70),5)
    #black
    pygame.draw.rect(screen,black,(525,633,140,70),0)
    pygame.draw.rect(screen,black,(525,633,140,70),5)
    #white
    pygame.draw.rect(screen,white,(695,633,140,70),0)
    pygame.draw.rect(screen,black,(695,633,140,70),5)
    #clear
    pygame.draw.rect(screen,white,(865,633,140,70),0)
    pygame.draw.rect(screen,black,(865,633,140,70),5)
    screen.blit(clearText,(885,640))


def cursor(x,y,z):
    pygame.draw.circle(screen,(31, 68, 245), (x, y), int(4*1.01**z),2)

def add_points(coords):
    points[current].append(coords)
    
def add_list_to_points(c):
    global current
    current +=1
    points.append([])
    colors.append(c)


def on_plane(z):
    if z<0:
        return True
    else:
        return False
def checkColor(x,y,z):
    global currentColor
    #clear
    if on_plane(z) and x>865 and x<1005 and y>633 and y<703:
        for i in range(len(colors)):
            colors[i] = white
    #red
    elif on_plane(z) and x>15 and x<155 and y>633 and y<703:
        currentColor = red
    #green
    elif on_plane(z) and x>185 and x<325 and y>633 and y<703:
        currentColor = green
    #blue
    elif on_plane(z) and x>355 and x<495 and y>633 and y<703:
        currentColor = blue
    #black
    elif on_plane(z) and x>525 and x<665 and y>633 and y<703:
        currentColor = black
    #white
    elif on_plane(z) and x>695 and x<835 and y>633 and y<703:
        currentColor = white

def draw(x,y,z):
    checkColor(x,y,z)
    global first
    if on_plane(z):
        if first:
            first = 0
            add_list_to_points(currentColor)
            add_points((x,y))
            add_points((x,y))
            canvas()
            
        else:
            add_points((x,y))
        canvas()
        
        #print points
    if not on_plane(z):
        first = 1
        canvas()
        cursor(x,y,z)

class LeapEventListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);        
        controller.config.set("Gesture.Swipe.MinLength", 200.0)
        controller.config.save()


    def on_disconnect(self, controller):
        print "Disconnected"

    def on_frame(self, controller):
        print "Frame available"
        #screen.blit(background,(0,0)) 
        #pygame.draw.rect(screen,(255,255,255),Rect(192,39,640,640),3)
        frame = controller.frame()

        for hand in frame.hands:
            x = optimize_x(hand.pointables.frontmost.tip_position.x) 
            y = optimize_y(hand.pointables.frontmost.tip_position.y)
            z = hand.pointables.frontmost.tip_position.z
            screen.blit(background,(0,0))
            draw(x,y,z)



            pygame.display.update()
                

def main():
    listener = LeapEventListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()