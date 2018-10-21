#!/usr/bin/env python3

import unittest
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        return

    def test_game_tiles_filter(self):
        return

    def test_game_tiles_match(self):
        self.assertEqual(144, Game.SIZE_SIMPLE * 3 * 4 + Game.SIZE_HONOR_DRAGON * 4 + Game.SIZE_HONOR_WIND * 4 + 8, 'expect 144 mahjong tiles')
        return

    def test_game_win_condition(self):
        hand1 = [(Game.TILE_SIMPLE_DOT, 1)]
        self.assertEqual(False, Game.is_won(hand1))

        # Expect triples of the same to succeed
        hand2 = [(Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 1),
                 (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3),
                 (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2),
                 (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2),
                 (Game.TILE_HONOR_WIND, 1), (Game.TILE_HONOR_WIND, 1)]
        self.assertEqual(True, Game.is_won(hand2))

        # Expect simple tiles to match
        hand3 = [(Game.TILE_SIMPLE_CHAR, 1), (Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 1),
                 (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3),
                 (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2),
                 (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2),
                 (Game.TILE_HONOR_WIND, 1), (Game.TILE_HONOR_WIND, 1)]
        self.assertEqual(False, Game.is_won(hand3))

        # Expect simple sequence of three to succeed
        hand4 = [(Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 2), (Game.TILE_SIMPLE_DOT, 3),
                 (Game.TILE_SIMPLE_DOT, 4), (Game.TILE_SIMPLE_DOT, 4), (Game.TILE_SIMPLE_DOT, 4),
                 (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2),
                 (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2),
                 (Game.TILE_HONOR_WIND, 1), (Game.TILE_HONOR_WIND, 1)]
        self.assertEqual(True, Game.is_won(hand4))

        # Expect with Kong to succeed
        hand5 = [(Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 1),
                 (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3),
                 (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2),
                 (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2),
                 (Game.TILE_HONOR_WIND, 1), (Game.TILE_HONOR_WIND, 1)]
        self.assertEqual(True, Game.is_won(hand5))

        # Expect sequence of three to succeed even in kong's situation?
        # hand6 = [(Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 2), (Game.TILE_SIMPLE_DOT, 3),
        #          (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3), (Game.TILE_SIMPLE_DOT, 3),
        #          (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2), (Game.TILE_SIMPLE_CHAR, 2),
        #          (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2), (Game.TILE_SIMPLE_BAMBOO, 2),
        #          (Game.TILE_HONOR_WIND, 1), (Game.TILE_HONOR_WIND, 1)]
        # self.assertEqual(True, Game.is_won(hand6))

        # Expect breaking up of a kong to be handled correctly
        hand7 = [(Game.TILE_SIMPLE_DOT, 2), (Game.TILE_SIMPLE_DOT, 2),
                 (Game.TILE_SIMPLE_DOT, 1), (Game.TILE_SIMPLE_DOT, 2), (Game.TILE_SIMPLE_DOT, 3),
                 (Game.TILE_SIMPLE_DOT, 4), (Game.TILE_SIMPLE_DOT, 5), (Game.TILE_SIMPLE_DOT, 6),
                 (Game.TILE_SIMPLE_DOT, 7), (Game.TILE_SIMPLE_DOT, 8), (Game.TILE_SIMPLE_DOT, 9),
                 (Game.TILE_SIMPLE_DOT, 7), (Game.TILE_SIMPLE_DOT, 8), (Game.TILE_SIMPLE_DOT, 9)]
        self.assertEqual(True, Game.is_won(hand7))
        return

if __name__ == '__main__':
    unittest.main()
