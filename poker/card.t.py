#!/usr/bin/env python3

import unittest
from card import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        pass

    ###### Const definitions #####
    def test_verifyScoreValidity(self):
        self.assertEqual(True, Card.STRAIGHT + Card.FLUSH               >
                               Card.FOUR_OF_A_KIND + Card.NUM_KINDS)
        self.assertEqual(True, Card.FOUR_OF_A_KIND                      >
                               Card.THREE_OF_A_KIND + Card.ONE_PAIR
                                                    + Card.NUM_KINDS)
        self.assertEqual(True, Card.THREE_OF_A_KIND + Card.ONE_PAIR     >
                               Card.FLUSH + Card.NUM_KINDS)
        self.assertEqual(True, Card.FLUSH                               >
                               Card.STRAIGHT + Card.NUM_KINDS)
        self.assertEqual(True, Card.STRAIGHT                            >
                               Card.THREE_OF_A_KIND + Card.NUM_KINDS)
        self.assertEqual(True, Card.THREE_OF_A_KIND                     >
                               Card.ONE_PAIR * 2 + Card.NUM_KINDS * 2)
        self.assertEqual(True, Card.ONE_PAIR * 2                        >
                               Card.ONE_PAIR + Card.NUM_KINDS)
        self.assertEqual(True, Card.ONE_PAIR                            >
                               Card.NUM_KINDS * 5)

    ###### Score types #######
    def test_scoreTypeHighCard(self):
        hand1 = [Card(1, 0), Card(3, 0), Card(5, 1), Card(7, 2), Card(9, 3)]
        self.assertEqual("high_card", Card.getScore(hand1)[1])

    def test_scoreTypeOnePair(self):
        hand1 = [Card(1, 0), Card(3, 0), Card(5, 1), Card(5, 2), Card(9, 3)]
        self.assertEqual("one_pair", Card.getScore(hand1)[1])

    def test_scoreTypeTwoPairs(self):
        hand1 = [Card(1, 0), Card(9, 0), Card(5, 1), Card(5, 2), Card(9, 3)]
        self.assertEqual("two_pairs", Card.getScore(hand1)[1])

    def test_scoreTypeThreeOfAKind(self):
        hand1 = [Card(1, 0), Card(5, 0), Card(5, 1), Card(7, 2), Card(5, 3)]
        self.assertEqual("three_of_a_kind", Card.getScore(hand1)[1])

    def test_scoreTypeStraight(self):
        hand1 = [Card(1, 0), Card(3, 0), Card(2, 1), Card(4, 2), Card(5, 3)]
        self.assertEqual("straight", Card.getScore(hand1)[1])

    def test_scoreTypeFlush(self):
        hand1 = [Card(1, 0), Card(3, 0), Card(5, 0), Card(6, 0), Card(7, 0)]
        self.assertEqual("flush", Card.getScore(hand1)[1])

    def test_scoreTypeFullHouse(self):
        hand1 = [Card(4, 0), Card(2, 0), Card(2, 1), Card(4, 2), Card(4, 3)]
        self.assertEqual("full_house", Card.getScore(hand1)[1])

    def test_scoreTypeFourOfAKind(self):
        hand1 = [Card(1, 0), Card(3, 0), Card(1, 1), Card(1, 2), Card(1, 3)]
        self.assertEqual("four_of_a_kind", Card.getScore(hand1)[1])

    def test_scoreTypeStraightFlush(self):
        hand1 = [Card(1, 0), Card(3, 0), Card(2, 0), Card(4, 0), Card(5, 0)]
        self.assertEqual("straight_flush", Card.getScore(hand1)[1])

    ####### Comparisons ######
    def test_straightFlushIsBetterThanFourOfAKind(self):
        hand1 = [Card(1, 0), Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0)]
        hand2 = [Card(1, 0), Card(1, 1), Card(1, 2), Card(1, 3), Card(10, 0)]
        self.assertEqual(True, Card.isBetterThan(hand1, hand2))

    def test_highCard(self):
        hand1 = [Card(1, 1), Card(2, 1), Card(4, 2), Card(11, 0), Card(9, 0),
                 Card(5, 0), Card(7, 0)]
        hand2 = [Card(1, 1), Card(2, 1), Card(4, 2), Card(11, 0), Card(9, 0),
                 Card(3, 0), Card(7, 0)]
        self.assertEqual(True, Card.isBetterThan(hand1, hand2),
                         "High card: failed when highest two cards from " +
                         "common pool")

if __name__ == '__main__':
    unittest.main()
