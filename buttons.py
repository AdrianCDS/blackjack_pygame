import pygame


class Button:
    def __init__(self, game, isDecision):
        self.game = game
        self.isDecision = isDecision
        self.disabled = False
        if self.isDecision:
            self.color = (180, 196, 36)
        else:
            self.color = (255, 255, 255)
        self.buttonRect = None
        
    def DrawButton(self, text, size, x, y, orientation):
        font = pygame.font.Font("Assets/Fonts/default.ttf", size)
        text = font.render(text, True, self.color)
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
        self.buttonRect = textRect

        if self.IsHovered():
            if self.isDecision:
                self.color = (210, 4, 45)
            else:
                self.color = (125, 125, 125)
        else:
            if self.isDecision:
                self.color = (180, 196, 36)
            else:
                self.color = (255, 255, 255)
        
    def IsHovered(self):
        mousePos = pygame.mouse.get_pos()
        return self.buttonRect.collidepoint(mousePos)
    