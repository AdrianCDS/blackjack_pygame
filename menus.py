from buttons import *
from players import Player, Dealer
import random


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.decreaseWager = Button(self.game, False)
        self.increaseWager = Button(self.game, False)
    
    def Draw(self):
        self.DrawText("Welcome to BlackJack!", 90, self.game.windowWidth / 2, 60, "center")
        self.DrawText("Enter your wager", 75, self.game.windowWidth / 2, self.game.windowHeight / 2, "center")
        self.decreaseWager.DrawButton("<", 75, self.game.windowWidth / 2 - 90, self.game.windowHeight / 2 + 90, "center")
        self.increaseWager.DrawButton(">", 75, self.game.windowWidth / 2 + 90, self.game.windowHeight / 2 + 90, "center")
        self.DrawText(f"{self.game.wager}", 60, self.game.windowWidth / 2, self.game.windowHeight / 2 + 90, "center")
        self.DrawText(f"Balance: {self.game.balance}$", 50, 45, self.game.windowHeight - 60, "left")
        self.DrawText("Press 'space' to start playing.", 50, self.game.windowWidth - 45, self.game.windowHeight - 60, "right")
    
    def DrawText(self, text, size, x, y, orientation):
        font = pygame.font.Font("Assets/Fonts/default.ttf", size)
        text = font.render(text, True, (255, 255, 255))
        textRect = text.get_rect()
        
        if orientation == "center":
            textRect.center = (x, y)
        elif orientation == "left":
            textRect.left = x
            textRect.centery = y
        elif orientation == "right":
            textRect.right = x
            textRect.centery = y
            
        self.game.window.blit(text, textRect)
        
        
class PlayingScreen(MainMenu):
    def __init__(self, game):
        self.game = game
        self.hit = Button(self.game, True)
        self.stand = Button(self.game, True)
        self.double = Button(self.game, True)
        self.split = Button(self.game, True)
        self.deck = [] # A LIST OF (value, suit), 6 DECKS OF CARDS
        self.LoadDeck()
        self.cardImages = {} # HOLDS THE FORMAT (value, suit) : image
        self.LoadCardImages()
        self.hiddenCard = pygame.image.load("Assets/Images/back-card.png")
        self.buttonSurface = pygame.Surface((185, 80), pygame.SRCALPHA)
        pygame.draw.rect(self.buttonSurface, (255, 255, 255, 25), (0, 0, 185, 80), border_radius=20)
    
    def Draw(self):
        self.game.player.DrawPlayerCards()
        self.game.dealer.DrawPlayerCards()
        self.DrawText(f"Dealer: {self.game.dealer.score}", 50, self.game.windowWidth - 45, 45, "right")
        self.DrawText(f"You: {self.game.player.score}", 50, self.game.windowWidth - 45, self.game.windowHeight - 45*2, "right")
        self.DrawText(f"Wager: {self.game.wager}$", 50, self.game.windowWidth - 45, self.game.windowHeight - 45, "right")
        self.game.window.blit(self.buttonSurface, (self.game.windowWidth / 2 - 100, self.game.windowHeight / 2 - 40))
        self.stand.DrawButton("stand", 60, self.game.windowWidth / 2 - 45, self.game.windowHeight / 2, "center")
        self.hit.DrawButton("hit", 60, self.game.windowWidth / 2 + 45, self.game.windowHeight / 2, "center")
    
    def LoadDeck(self):
        suits = [0, 1, 2, 3] # INDEXES FOR SUITS IN THE PICTURE
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # INDEXES+1 FOR VALUES IN THE PICTURE
        deck = [(value, suit) for suit in suits for value in values] * 6
        random.shuffle(deck)
        self.deck = deck
    
    def LoadCardImages(self):
        spriteSheet = pygame.image.load("Assets/Images/cards.png")
        for value in range(1, 14):
            for suit in range(4):
                x = (value - 1) * (2179 / 13) # THE ONE ON THE RIGHT IS THE WIDTH OF A CARD
                y = suit * (1216 / 5) # THE ONE ON THE RIGHT IS THE HEIGHT OF A CARD
                rect = pygame.Rect(x, y, 2179 / 13, 1216 / 5)
                image = pygame.Surface(rect.size).convert_alpha()
                image.blit(spriteSheet, (0, 0), rect)
                self.cardImages[(value, suit)] = image
    
    def DrawCard(self, value, suit, x, y):
        card = self.cardImages[(value, suit)]
        self.game.window.blit(card, (x, y))
        
        
class ResultScreen(MainMenu):
    def __init__(self, game):
        self.game = game
        self.playAgain = Button(self.game, True)
        self.quit = Button(self.game, True)
        self.verdict = "Undefined"
        self.buttonSurface = pygame.Surface((290, 150), pygame.SRCALPHA)
        pygame.draw.rect(self.buttonSurface, (255, 255, 255, 25), (0, 0, 290, 150), border_radius=20)
        
    def Draw(self):
        self.game.player.DrawPlayerCards()
        self.game.dealer.DrawPlayerCards()
        self.DrawText(f"Dealer: {self.game.dealer.score}", 50, self.game.windowWidth - 45, 45, "right")
        self.DrawText(f"You: {self.game.player.score}", 50, self.game.windowWidth - 45, self.game.windowHeight - 45*2, "right")
        self.DrawText(f"Wager: {self.game.wager}$", 50, self.game.windowWidth - 45, self.game.windowHeight - 45, "right")
        self.DrawText(f"{self.verdict} {self.game.balance}$", 75, self.game.windowWidth / 2, self.game.windowHeight / 2, "center")
        self.game.window.blit(self.buttonSurface, (self.game.windowWidth - 225, 280))
        self.playAgain.DrawButton("Play Again", 60, self.game.windowWidth - 45, 45*5 + 19 + 75, "right")
        self.quit.DrawButton("Quit", 60, self.game.windowWidth - 45, 45*5 + 19 + 150, "right")
        