from Bubble import Bubble

DEFAULT_BUBBLES = 30

def setup():
    size(800, 800)
    Bubble.inst.clear()
    for _ in range(DEFAULT_BUBBLES):
        Bubble()

def draw():
    background(0)
    Bubble.update()
    Bubble.draw()

def keyPressed():
    if keyCode == ord(' '):
        Bubble()
    elif keyCode == ord('\b'):
        Bubble.inst.pop()
    elif keyCode == ord('R'):
        setup()
    elif keyCode == ord('Z'):
        Bubble.rainbow = not Bubble.rainbow
    elif keyCode == ord('X'):
        Bubble.srainbow = not Bubble.srainbow
    elif keyCode == ord('C'):
        Bubble.do_stroke = not Bubble.do_stroke
    elif keyCode == ord('B'):
        Bubble().R = 100
    print(len(Bubble.inst))

def mousePressed():
    Bubble.mousePressed(mouseX, mouseY)
    print(len(Bubble.inst))