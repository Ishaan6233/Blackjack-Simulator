'''
Project: Blackjack
Author: Ishaan Meena
'''

import os
import random


def display_game_rules():
    with open('blackjack_rules.txt', 'r') as file:
        rules = file.read().splitlines()
        for line in rules:
            print(line)
    print('GOOD LUCK!\n')


class Card:
    def __init__(self, card_face, value, symbol):
        self.card_face = card_face
        self.value = value
        self.symbol = symbol


def show_cards(cards, hidden):
    for row in range(9):
        line = ""
        for i, card in enumerate(cards):
            if row == 0:
                line += "\t ________________ "
            elif row == 1:
                line += "\t|                |"
            elif row == 2:
                if card.card_face in ['J', 'Q', 'K', 'A']:
                    line += f"\t|  {card.card_face}             |"
                elif card.value == 10:
                    line += f"\t|  {card.value}            |"
                else:
                    line += f"\t|  {card.value}             |"
            elif row in [3, 4, 5, 6]:
                line += "\t|                |"
            elif row == 7:
                line += f"\t|       {card.symbol}        |"
            elif row == 8:
                if card.card_face in ['J', 'Q', 'K', 'A']:
                    line += f"\t|            {card.card_face}   |"
                elif card.value == 10:
                    line += f"\t|           {card.value}   |"
                else:
                    line += f"\t|            {card.value}   |"
            elif row == 9:
                line += "\t|________________|"

            if hidden and i == len(cards) - 1:
                line = line[:-17] + "\t ________________ \t|                |"
                line += "\t|      * *       |" * 3 + "\t|    *     *     |" * 3
                line += "\t|   *       *    |" * 3 + "\t|   *       *    |" * 3
                line += "\t|          *     |" + "\t|         *      |" + "\t|        *       |" * 3
                line += "\t|                |" * 2 + "\t|                |"
                line += "\t|        *       |" + "\t|                |"
                line += "\t|________________|"
        print(line)
    print()


def deal_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card, deck


def play_blackjack(deck):
    player_cards = []
    dealer_cards = []
    player_score = 0
    dealer_score = 0

    while len(player_cards) < 2:
        player_card, deck = deal_card(deck)
        player_cards.append(player_card)
        player_score += player_card.value

        if len(player_cards) == 2:
            if player_cards[0].value == 11 and player_cards[1].value == 11:
                player_cards[0].value = 1
                player_score -= 10

        dealer_card, deck = deal_card(deck)
        dealer_cards.append(dealer_card)
        dealer_score += dealer_card.value

        if len(dealer_cards) == 2:
            if dealer_cards[0].value == 11 and dealer_cards[1].value == 11:
                dealer_cards[1].value = 1
                dealer_score -= 10

    print_game_state(player_cards, dealer_cards, player_score, dealer_score, True)

    while player_score < 21:
        choice = input('Enter H to Hit or S to Stand: ').upper()
        if choice == 'H':
            player_card, deck = deal_card(deck)
            player_cards.append(player_card)
            player_score += player_card.value

            adjust_ace(player_cards, player_score)

            if player_score > 21:
                break

            print_game_state(player_cards, dealer_cards, player_score, dealer_score, True)

        elif choice == 'S':
            break
        else:
            print('Invalid choice! Please enter H or S.')

    print_game_state(player_cards, dealer_cards, player_score, dealer_score, False)

    while dealer_score < 17:
        dealer_card, deck = deal_card(deck)
        dealer_cards.append(dealer_card)
        dealer_score += dealer_card.value

        adjust_ace(dealer_cards, dealer_score)

        if dealer_score > 21:
            break

        print_game_state(player_cards, dealer_cards, player_score, dealer_score, False)

    determine_winner(player_score, dealer_score)


def adjust_ace(cards, score):
    card_pos = 0
    while score > 21 and card_pos < len(cards):
        if cards[card_pos].value == 11:
            cards[card_pos].value = 1
            score -= 10
        card_pos += 1
    return score


def print_game_state(player_cards, dealer_cards, player_score, dealer_score, hide_dealer_card):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('PLAYER CARDS:')
    show_cards(player_cards, False)
    print(f'PLAYER SCORE = {player_score}\n')
    print('DEALER CARDS:')
    show_cards(dealer_cards, hide_dealer_card)
    if hide_dealer_card:
        print(f'DEALER SCORE = {dealer_score - dealer_cards[-1].value}')
    else:
        print(f'DEALER SCORE = {dealer_score}')
    print()


def determine_winner(player_score, dealer_score):
    if player_score > 21:
        print('PLAYER BUSTED! DEALER WINS!')
    elif dealer_score > 21:
        print('DEALER BUSTED! PLAYER WINS!')
    elif player_score == dealer_score:
        print('TIE GAME!')
    elif player_score == 21:
        print('PLAYER HAS A BLACKJACK! PLAYER WINS!')
    elif dealer_score == 21:
        print('DEALER HAS A BLACKJACK! DEALER WINS!')
    elif player_score > dealer_score:
        print('PLAYER WINS!')
    else:
        print('DEALER WINS!')


def init_deck():
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    suit_symbols = {'Hearts': '\u2661', 'Diamonds': '\u2662', 'Spades': '\u2664', 'Clubs': '\u2667'}
    cards = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10,
             'K': 10}
    deck = []
    for suit in suits:
        for card, value in cards.items():
            deck.append(Card(card, value, suit_symbols[suit]))
    return deck


if __name__ == '__main__':
    display_game_rules()
    deck = init_deck()
    while True:
        play_blackjack(deck)
        play_again = input('Do you want to play again? (Y/N): ').upper()
        if play_again != 'Y':
            break
        deck = init_deck()
