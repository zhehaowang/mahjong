#!/usr/bin/env python3

import os
import sys


# Assign the numbers such that (after being offset by highest cards (1 unit)
#   STRAIGHT + FLUSH           >
#   FOUR_OF_A_KIND             >
#   THREE_OF_A_KIND + ONE_PAIR >
#   FLUSH                      >
#   STRAIGHT                   >
#   THREE_OF_A_KIND            >
#   ONE_PAIR * 2               >
#   ONE_PAIR                   >
#   HIGH_CARD

# Design concern: decoupling Card representation from Total Ordering Rule
# representation

# TODO: store "score_type" in const

class Card:

    NUM_SUITS        = 4
    NUM_KINDS        = 13
    TOTAL_HAND_CARDS = 7

    FOUR_OF_A_KIND  = 400
    FLUSH           = 320
    STRAIGHT        = 280
    THREE_OF_A_KIND = 250
    ONE_PAIR        = 100

    def __init__(self, number, suit):
    # @param  int, int
    # Number: [0, 12]. '0' - 2, '11' - King, '12' - Ace
    # suit:   [0, 3] .
        self.number = number
        self.suit  = suit

    def __gt__(self, rhs):
    # @param Card
        return self.number < rhs.number

    def __eq__(self, rhs):
    # @param Card
        return self.number == rhs.number

    @staticmethod
    def isSamesuit(cards):
    # @param  [Card]
    # @return True if given cards are all of the same suit
        if len(cards) > 0:
            suit = cards[0].suit
            for card in cards[1:]:
                if card.suit != suit:
                    return False
        return True

    @staticmethod
    def isSequence(cards):
    # @param  [Card]
    # @return True if given cards are exactly a sequence
    # @note   A sequence that wraps around is not considered a sequence: 
    #         f(J, K, A) == True, f(A, 2, 3) == False
        if len(cards) > 0:
            sorted_cards = sorted(cards)
            value = sorted_cards[0].number
            for i in range(1, len(sorted_cards)):
                if sorted_cards[i].number - value != i:
                    return False
        return True

    @staticmethod
    def getScore(cards):
    # @param  [Card]
    # @return Int, String. Score and type of score
    # @note   https://en.wikipedia.org/wiki/List_of_poker_hands
    #         From high to low
    #           Five of a kind* (Four of a kind + Joker)
    #           Straight flush  (Five of the same suit + sequence)
    #           Four of a kind  (Four of the same number)
    #           Full house      (Three of a kind + A pair)
    #           Flush           (Five of the same suit, not sequence)
    #           Straight        (Five of a sequence, not same suit)
    #           Three of a kind (Three of the same number)
    #           Two pair        (Two pairs of the same number)
    #           One pair        (Two cards of the same number)
    #           High card       (Highest numbered card)
    #         These are not mutually exclusive and only the five cards that
    #         make the highest score matters. (One can have three of a kind and
    #         a straight / flush.
        assert len(cards) <= Card.TOTAL_HAND_CARDS
        # If this does not hold, the kind score comparison no longer holds and
        # this implementation is wrong

        score      = 0
        score_type = "high_card"

        matrix = [[0 for x in range(Card.NUM_KINDS)]
                     for y in range(Card.NUM_SUITS)]
        for card in cards:
            matrix[card.suit][card.number] = 1

        # With the current scoring system there is no need to store number of
        # cards in each suit yet
        suit_count = []
        for suit in range(Card.NUM_SUITS):
            num_cards = sum(matrix[suit])
            if num_cards > 4:
                temp = Card.getStraightScore(matrix[suit])
                if temp > 0:
                # Straight Flush
                    score      = max(Card.STRAIGHT + Card.FLUSH + temp, score)
                    score_type = "straight_flush"
                    return score, score_type
                else:
                # Flush
                    temp = Card.FLUSH + max(matrix[suit])
                    if temp > score:
                        score      = temp
                        score_type = "flush"
            suit_count.append(num_cards)

        kind_count = []
        # An additional variable is added to keep track of score generated by
        # pairs. This is to handle Full House.
        kind_score = 0

        # TODO: this high card impl is wrong, need to differentiate player
        # cards and pool cards in this case
        high_card  = 0
        for kind in range(Card.NUM_KINDS):
            num_cards = sum([matrix[i][kind] for i in range(Card.NUM_SUITS)])
            kind_count.append(num_cards)
            if num_cards > 3:
                # Four of a kind
                temp = Card.FOUR_OF_A_KIND + kind
                if temp > score:
                    score      = temp
                    score_type = "four_of_a_kind"
            elif num_cards > 2:
                # Three of a kind
                kind_score += Card.THREE_OF_A_KIND + kind
            elif num_cards > 1:
                # One pair
                kind_score += Card.ONE_PAIR + kind
            else:
                # High card
                high_card = kind

        temp = Card.getStraightScore(kind_count)
        if temp > 0:
            # Straight
            temp += Card.STRAIGHT
            if temp > score:
                score_type = "straight"
                score = temp

        if kind_score > score:
            score = kind_score
            if kind_score > Card.THREE_OF_A_KIND + Card.ONE_PAIR:
                # Full House
                score_type = "full_house"
            elif kind_score >= Card.THREE_OF_A_KIND:
                score_type = "three_of_a_kind"
            elif kind_score > Card.ONE_PAIR * 2:
                score_type = "two_pairs"
            else:
                score_type = "one_pair"

        if score_type == "":
            score_type = "high_card"
            score      = high_card

        return score, score_type

    @staticmethod
    def getStraightScore(row):
    # @param  [Int] of length NUM_KINDS
    # @return Int, 0 if not a straight, highest card num if otherwise
    # @TODO   handle wrap around if required
        assert len(row) == Card.NUM_KINDS

        curr_seq_len = 0
        start        = -1
        for idx in range(len(row)):
            if row[len(row) - idx - 1] != 0:
                if start < 0:
                    start = idx
                curr_seq_len += 1
                if curr_seq_len > 4:
                    return len(row) - start
            else:
                curr_seq_len = 0
                start = -1
        return 0

    @staticmethod
    def isBetterThan(lhs_cards, rhs_cards):
    # @param  [Card], [Card]
    # @return Boolean. True if lhs is better than rhs. False if otherwise
    #         __gt__ for [Cards]
        return Card.getScore(lhs_cards)[0] > Card.getScore(rhs_cards)[0]

    @staticmethod
    def isTheSame(lhs_cards, rhs_cards):
    # @param  [Card], [Card]
    # @return Boolean. True if lhs is the same as rhs. False if otherwise
    #         __eq__ for [Cards]
        return Card.getScore(lhs_cards)[0] == Card.getScore(rhs_cards)[0]