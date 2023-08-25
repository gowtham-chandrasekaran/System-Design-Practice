from enum import Enum

class Suit(Enum):
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'
    HEARTS = 'hearts'
    SPADES = 'spades'

class Card:
    def __init__(self,suit,value):
        self._suit = suit
        self._value = value

    def getSuit(self):
        return self._suit
    
    def getValue(self):
        return self._value
    
    def print(self):
        print(self.getValue(), self.getSuit())


import random

class Deck:
    def __init__(self):
        self._cards = []
        for suit in Suit:
            for value in range(1,14):
                self._cards.append(Card(suit,min(value,10)))
                                  
    def print(self):
        for card in self._cards:
            card.print()

    def draw(self):
        return self._cards.pop()

    def shuffle(self):
        for i in range(len(self._cards)):
            j = random.randint(0,51)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

class Hand:
    def __init__(self):
        self._score = 0
        self._cards = []

    def addCard(self,card):
        self._cards.append(card)
        # For Ace, add 11 if score <= 21, otherwise add 1
        if card.getValue() == 1:
            if self._score + 11 <= 21:
                self._score += 11
            else:
                self._score += 1
        else:
            self._score += card.getValue()
        print('Score: ' + str(self._score))

    def getScore(self):
        return self._score
    
    def getCards(self):
        return self._cards
    
    def print(self):
        for card in self._cards:
            print(card.getValue(), card.getSuit())


from abc import ABC, abstractmethod

class Player:
    def __init__(self,hand):
        self._hand = hand

    def getHand(self):
        return self._hand
    
    def clearHand(self):
        self._hand = Hand()

    def addCard(self,card):
        self._hand.addCard(card)

    # Will be implemented by subclasses
    @abstractmethod
    def makeMove(self):
        pass

class UserPlayer(Player):
    def __init__(self,balance,hand):
        super().__init__(hand)
        self._balance = balance 

    def getBalance(self):
        return self._balance
    
    def placeBet(self, amount):
        if amount > self._balance:
            raise ValueError('Insufficient funds')
            
        else:
            self._balance -= amount
            return amount

    def receiveWinnings(self, amount):
        self._balance += amount

    def makeMove(self):
        if self.getHand().getScore() > 21:
            return False
        move = input('Draw a card? (y/n): ')
        return move == 'y'


class Dealer(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self._targetScore = 17

    def updateTargetScore(self, score):
        self._targetScore = score

# return true if score is less than target score and make move else return false and dont make move
    def makeMove(self):
        return self.getHand().getScore() < self._targetScore
    
class GameRound:
    def __init__(self,player,dealer,deck):
        self._deck = deck
        self._player = player
        self._dealer = dealer

    def getBetUser(self):
        amount = int(input('Enter bet amount: '))
        return amount
    
    def cleanupRound(self):
        self._player.clearHand()
        self._dealer.clearHand()
        print('Player balance: ', self._player.getBalance())
    
    def play(self):
        self._deck.shuffle()

        if self._player.getBalance() <= 0:
            print('Insufficient funds for Player')
            return
        userBet = self.getBetUser()
        self._player.placeBet(userBet)

        self.dealInitialCards()

    # user makes move
        while self._player.makeMove():
            drawnCard = self._deck.draw()
            print('Player draws', drawnCard.getSuit(), drawnCard.getValue())
            self._player.addCard(drawnCard)
            print('Player Score: ', self._player.getHand().getScore())

        if self._player.getHand().getScore() > 21:
            print('Player Busts')
            self.cleanupRound()
            return

    # dealer makes move
        while self._dealer.makeMove():
            self._dealer.addCard(self._deck.draw())

    # Determine winner
        if self._dealer.getHand().getScore() > 21:
            print('Player wins')
            self._player.receiveWinnings(userBet * 2)
        elif self._dealer.getHand().getScore() > self._player.getHand().getScore():
            print('Player loses')
        else:
            print('Game is a draw')
            self._player.receiveWinnings(userBet)
        

    def dealInitialCards(self):
        for i in range(2):
            self._player.addCard(self._deck.draw())
            self._dealer.addCard(self._deck.draw())
        print('Player Hand: ')
        self._player.getHand().print()
        dealerCard = self._dealer.getHand().getCards()[0]
        print("Dealer's first card: ")
        dealerCard.print()

# Initally player has 1000 dollars.
player = UserPlayer(1000, Hand())
dealer = Dealer(Hand())

while player.getBalance() > 0:
    gameRound = GameRound(player, dealer, Deck()).play()
