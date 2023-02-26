

class Player:
    def __init__(self, game):
        self.score = 0
        self.game = game
        self.cards = []
        self.isPlaying = True
        self.isBust = False
        self.blackjack = False

    def CheckBlackjack(self):
        if self.score == 21:
            self.blackjack = True
            self.game.balance += (2 * self.game.wager)
            self.game.resultScreen.verdict = "Blackjack! Your balance is now"
            self.game.currentMenu = "result_screen"

    def GetInitialCards(self):
        cardTuple1 = self.game.playingScreen.deck[0]
        cardTuple2 = self.game.playingScreen.deck[2]
        self.cards.append(cardTuple1)
        self.cards.append(cardTuple2)
        self.CalculateScore()
        del self.game.playingScreen.deck[0]
        del self.game.playingScreen.deck[1]

    def CalculateScore(self):
        self.score = 0
        numOfAces = 0

        for tuple in self.cards:
            if tuple[0] >= 10:
                self.score += 10
            elif tuple[0] == 1:
                numOfAces += 1
                self.score += 11
            else:
                self.score += tuple[0]

        while self.score > 21 and numOfAces > 0:
            self.score -= 10
            numOfAces -= 1

    def Stand(self):
        self.isPlaying = False
        self.game.dealer.isPlaying = True
        self.game.dealer.CalculateScore()
        if self.game.dealer.score <= 16:
            self.game.dealer.DoTurn()
        else:
            self.CompareScores()

    def Hit(self):
        newCardTuple = self.game.playingScreen.deck[0]
        self.cards.append(newCardTuple)
        self.CalculateScore()
        del self.game.playingScreen.deck[0]
        self.CheckBust()

    def DrawPlayerCards(self):
        x = 0
        for card in self.cards:
            self.game.playingScreen.DrawCard(card[0], card[1], 25 + x * 2179 / 26, self.game.windowHeight - 1216 / 5 - 25)
            x += 1

    def CompareScores(self):
        if self.score > self.game.dealer.score:
            self.game.balance += (2 * self.game.wager)
            self.game.resultScreen.verdict = "You win! Your balance is now"
            self.game.currentMenu = "result_screen"
        elif self.score < self.game.dealer.score:
            self.game.resultScreen.verdict = "You lost! Your balance is now"
            self.game.currentMenu = "result_screen"
        else:
            self.game.balance += self.game.wager
            self.game.resultScreen.verdict = "It's a push. Your balance is"
            self.game.currentMenu = "result_screen"

    def CheckBust(self):
        if self.score > 21:
            self.isBust = True
            self.game.currentMenu = "result_screen"
            self.game.resultScreen.verdict = "You busted! Your balance is now"

    def Reset(self):
        self.game.wager = 0.0
        self.isPlaying = True
        self.isBust = False
        self.blackjack = False
        self.cards = []
        self.GetInitialCards()


class Dealer(Player):
    def __init__(self, game):
        super().__init__(game)
        self.isPlaying = False

    def GetInitialCards(self):
        cardTuple1 = self.game.playingScreen.deck[1]
        self.cards.append(cardTuple1)
        self.CalculateScore()
        cardTuple2 = self.game.playingScreen.deck[3]
        self.cards.append(cardTuple2)
        del self.game.playingScreen.deck[1]
        del self.game.playingScreen.deck[3]

    def DrawPlayerCards(self):
        x = 0
        for card in self.cards:
            self.game.playingScreen.DrawCard(card[0], card[1], 25 + x * 2179 / 26, 25)
            x += 1
        if not self.isPlaying:
            self.game.window.blit(self.game.playingScreen.hiddenCard, (25 + 2179 / 26, 25))

    def CheckBust(self):
        if self.score > 21:
            self.isBust = True
            self.game.currentMenu = "result_screen"
            self.game.resultScreen.verdict = "Dealer busted! Your balance is now"
            self.game.balance += (2 * self.game.wager)

    def DoTurn(self):
        while self.score < 17:
            self.Hit()
        if not self.isBust:
            self.game.player.CompareScores()

    def Reset(self):
        self.isPlaying = False
        self.isBust = False
        self.cards = []
        self.GetInitialCards()
