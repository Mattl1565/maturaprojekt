import pygame as pg

def init():
    pg.init()
    win = pg.display.set_mode((500, 500))

def getKey(keyName):
    ans = False
    for eve in pg.event.get(): pass
    keyInput = pg.key.get_pressed()
    myKey = getattr(pg, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pg.display.update()
    return ans

def main():
    if getKey('LEFT'):
        print('Left key pressed')
    if getKey('RIGHT'):
        print('Right key pressed')

if __name__ == '__main__':
    init()
    while True:
        main()