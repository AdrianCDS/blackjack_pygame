from menus import *


class Game:
    def __init__(self, balance, modifier):
        pygame.display.set_caption("Blackjack")
        self.isRunning = False
        self.windowWidth = 1280
        self.windowHeight = 720
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("Assets/Images/background.jpg")
        self.currentMenu = "main_menu"
        self.mainMenu = MainMenu(self)
        self.playingScreen = PlayingScreen(self)
        self.resultScreen = ResultScreen(self)
        self.wager = 0.0
        self.balance = balance
        self.modifier = modifier
        self.player = Player(self)
        self.player.GetInitialCards()
        self.dealer = Dealer(self)
        self.dealer.GetInitialCards()
        pygame.mixer.music.load("Assets/Sounds/music.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        self.sound = pygame.mixer.Sound("Assets/Sounds/select.wav")
        self.sound.set_volume(0.25)
    
    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                
            if self.currentMenu == "main_menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.wager != 0:
                            self.sound.play()
                            self.currentMenu = "play_screen"
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.mainMenu.decreaseWager.IsHovered() and self.wager > 0:
                        self.sound.play()
                        self.wager -= self.modifier
                        self.balance += self.modifier
                    elif self.mainMenu.increaseWager.IsHovered() and self.balance > 0:
                        self.sound.play()
                        self.wager += self.modifier
                        self.balance -= self.modifier
                        
            elif self.currentMenu == "play_screen":
                if not self.player.blackjack:
                    self.player.CheckBlackjack()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.playingScreen.hit.IsHovered() and self.player.isPlaying:
                        self.sound.play()
                        self.player.Hit()
                    elif self.playingScreen.stand.IsHovered() and self.player.isPlaying:
                        self.sound.play()
                        self.player.Stand()

            elif self.currentMenu == "result_screen":
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.resultScreen.quit.IsHovered():
                        self.isRunning = False
                    if self.resultScreen.playAgain.IsHovered():
                        self.sound.play()
                        self.player.Reset()
                        self.dealer.Reset()
                        self.currentMenu = "main_menu"
            
    def Draw(self):
        self.window.blit(self.background, (0, 0))
        
        if self.currentMenu == "main_menu":
            self.mainMenu.Draw()
        elif self.currentMenu == "play_screen":
            self.playingScreen.Draw()
        elif self.currentMenu == "result_screen":
            self.resultScreen.Draw()

    def Update(self):
        pygame.display.update()
        self.clock.tick(self.fps)
        
    def Run(self):
        self.isRunning = True
        while self.isRunning:
            self.CheckEvents()
            self.Draw()
            self.Update()
            