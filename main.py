from game import *

if __name__ == "__main__":
    pygame.init()
    
    game = Game(100, 1)
    game.Run()

    pygame.quit()
