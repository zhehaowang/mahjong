#!/usr/bin/env python3

import sys
import random

class Game():
    """
    Game state is a tuple of ([Hand], Tile, [Tile]), where
    
    Hand is an array of [Tile], typically 13 in length, representing the hands
    of all current players.
    
    Tile is a tuple (type, value). In a Game [Tile] stores the remaining tiles
    to be drawn, and a single Tile stores the currently discarded Tile.

    Game state transitions through a Move to the next State. A Move
    (Int, Action) defines a player's action (e.g. (1, Chow)). Legal Moves are
    ordered by precedence, and should none of the Moves be taken, Game continues
    with the ordinary flow of having the next player draw and discard one Tile.
    """
    SIZE_HAND = 13
    TILE_SIMPLE_DOT    = 'simple-dot'
    TILE_SIMPLE_BAMBOO = 'simple-bamboo'
    TILE_SIMPLE_CHAR   = 'simple-char'
    TILE_HONOR_WIND    = 'honor-wind'
    TILE_HONOR_DRAGON  = 'honor-dragon'
    TILE_BONUS_FLOWER  = 'bonus-flower'
    TILE_BONUS_SEASON  = 'bonus-season'

    SIZE_KONG = 4
    SIZE_PONG = 3
    SIZE_EYE  = 2
    
    SIZE_SIMPLE       = 9
    SIZE_HONOR_DRAGON = 3
    SIZE_HONOR_WIND   = 4

    SIZE_EYE_NEEDED   = 1
    SIZE_MELD_NEEDED  = 4

    PLAYER_NUM = 4

    def __init__(self):
        self.hands = [[] for i in range(Game.PLAYER_NUM)]
        self.tiles = []
        self.discarded_tile = None
        self.turn_owner = 0

        self.init_tiles()
        self.is_running = False
        return

    #########################
    # Game actions
    #########################
    def init_tiles(self):
        """
        Initialize the 144 tiles
        """
        for simple in [Game.TILE_SIMPLE_DOT, Game.TILE_SIMPLE_BAMBOO, Game.TILE_SIMPLE_CHAR]:
            for value in range(Game.SIZE_SIMPLE):
                self.tiles += [(simple, value) for i in range(4)]

        for value in ['east', 'west', 'north', 'south']:
            self.tiles += [(Game.TILE_HONOR_WIND, value) for i in range(4)]
            self.tiles += [(Game.TILE_BONUS_FLOWER, value)]
            self.tiles += [(Game.TILE_BONUS_SEASON, value)]

        for value in ['red', 'green', 'white']:
            self.tiles += [(Game.TILE_HONOR_DRAGON, value) for i in range(4)]

        random.shuffle(self.tiles)
        return

    def draw(self, idx, num):
        """
        Draw num tiles for player idx
        @param  idx int the player index
        @param  num int the number of tiles to draw
        """
        if num > len(self.tiles):
            raise RuntimeError('not enough tiles left')
        self.hands[idx] += self.tiles[:num]
        del self.tiles[:num]
        return

    def discard(self, player_idx, tile_idx):
        """
        Draw num tiles for player idx
        @param  player_idx int the player index
        @param  tile_idx   int the index of tile to be discarded
        """
        if tile_idx > len(self.hands[player_idx]) or tile_idx < 0:
            raise RuntimeError('invalid index')
        self.discarded_tile = self.hands[player_idx][tile_idx]
        del self.hands[player_idx][tile_idx]
        return

    def start(self):
        """
        Bootstrap a game
        """
        self.is_running = True
        for i in range(Game.PLAYER_NUM):
            self.draw(i, Game.SIZE_HAND)
        return

    def action(self, player_idx, action):
        """
        After obtaining the list of legal actions, take one from the list
        according to player decision, then move the game to the next
        'draw-discard'

        @param  player_idx int player index
        @param  action     str the action to take (one of 'declare-victory',
                pong, kong, or chow)
        """
        raise RuntimeError('not implemented')
        return

    #########################
    # Checks and helpers
    #########################
    @staticmethod
    def determine_legal_actions(self):
        """
        Determines the ordered set of legal actions.
          Any player picks up the discarded tile and declares victory ->
          Any player picks up the discarded tile by Pong or Kong -->
          Next player picks up the discarded tile by Chow
        """
        raise RuntimeError('not implemented')
        return

    @staticmethod
    def is_won(player_hand):
        """
        Check if a given hand has won
        @param  player_hand [Tile] unsorted array of tiles representing a
                player's entire hand. including flowers and kongs
        @return True if the hand has won, False if otherwise. The state of how
                it's won is also kept
        """
        if len(player_hand) < Game.SIZE_HAND + 1:
            return False

        # filter out Kongs and Bonuses
        hand, bonus, kongs = Game.filter_hand(player_hand)

        ret, state = Game.reduce(hand)
        return ret

    @staticmethod
    def reduce(hand):
        """
        Recursive call wrapper to decide if a player's hand has won
        @param  hand <type, <value, cnt>> a player's hand as represented by
                how many of each type of tile he has
        @return (bool, [Tile, [Tile, Tile, Tile]]) with first element indicating
                if the hand has won, and if so, the second element indicating
                how: which two tiles are used to form the eyes, and which four
                groups of three are used to form the melds (sequences or
                three-of-a-kind).
        """
        def helper(hand, state, simple, idxs):
            """
            Given a hand (of the same simple type) and indexes of tiles to take
            out, take them out and check if the remaining hand can be further
            divided. Keep trying if so, pop and backtrack if not.

            @param  hand <value, cnt> of the same simple type, how many of which
                    we have.
            @param  state [Tile, [Tile, Tile, Tile]], what we have taken out so
                    far (the pair and then three-of-a-kind or
                    three-of-a-sequence)
            @param  simple str indicating which simple type we are currently
                    reducing
            @param  idxs [int, int] or [int, int, int] indicating the indexes of
                    elements to be taken out in this call
            """
            if len(idxs) == 3:
                state[1].append([(simple, idxs[0]), (simple, idxs[1]), (simple, idxs[2])])
            elif len(idxs) == 2:
                state[0] = (simple, idxs[0])

            for i in idxs:
                hand[i] -= 1
                if hand[i] == 0:
                    del hand[i]
            if judge(hand, state, simple):
                return True
            else:
                if len(idxs) == 3:
                    state[1].pop()
                else:
                    state[0] = None
                for i in idxs:
                    if i in hand:
                        hand[i] += 1
                    else:
                        hand[i] = 1
            return False

        def judge(hand, state, simple):
            """
            Given a hand try (in sequence) pattern match it with
             - two-of-a-kind (eye) if a pair of eyes is not already present,
             - three-of-a-kind, and
             - sequence-of-three
            Call backtracking function suggesting which pattern is applied,
            backtracking function applies the reduction and in turn, recursively
            calls this to then match with a reduced hand.

            @param  hand <value, cnt> of the same simple type, how many of which
                    we have.
            @param  state [Tile, [Tile, Tile, Tile]], what we have taken out so
                    far (the pair and then three-of-a-kind or
                    three-of-a-sequence)
            @param  simple str indicating which simple type we are currently
                    reducing
            @return True with state modified if the given hand can eventually
                    be divided into at most one pair and any number of
                    three-of-a-kind or three-of-a-sequence.
            """
            if not hand:
                return True
            key = next(iter(hand.keys()))

            if hand[key] >= Game.SIZE_EYE and state[0] is None:
                if helper(hand, state, simple, [key, key]):
                    return True
            if hand[key] == Game.SIZE_PONG:
                if helper(hand, state, simple, [key, key, key]):
                    return True
            if key - 1 in hand and key - 2 in hand:
                if helper(hand, state, simple, [key - 2, key - 1, key]):
                    return True
            if key - 1 in hand and key + 1 in hand:
                if helper(hand, state, simple, [key - 1, key, key + 1]):
                    return True
            if key + 1 in hand and key + 2 in hand:
                if helper(hand, state, simple, [key, key + 1, key + 2]):
                    return True

            return False

        state = [None, []]
        # First handle the honor tiles whose only patterns are two or three
        # of a kind
        for honor in [Game.TILE_HONOR_WIND, Game.TILE_HONOR_DRAGON]:
            for key in hand[honor]:
                if hand[honor][key] == Game.SIZE_EYE:
                    state[0] = (honor, key)
                elif hand[honor][key] == Game.SIZE_PONG:
                    state[1].append([(honor, key), (honor, key), (honor, key)])
                else:
                    return False, None

        # Then handle the simple tiles
        for simple in [Game.TILE_SIMPLE_DOT, Game.TILE_SIMPLE_CHAR, Game.TILE_SIMPLE_BAMBOO]:
            if not judge(hand[simple], state, simple):
                return False, None
        
        if state[0] and len(state[1]) == Game.SIZE_MELD_NEEDED:
            return True, state
        else:
            return False, None

    @staticmethod
    def filter_hand(hand):
        """
        Filter out unused Kong pieces and Bonuses given a hand
        @param  hand [Tile], the unsorted hand to be filtered
        @return ({...}, [Tile], [Tile]), the first is the filtered hand,
                second is bonuses formed, and last is unused kong pieces
        """
        same_cnt = 1
        last_piece = None
        
        result = {
            Game.TILE_SIMPLE_DOT:    {},
            Game.TILE_SIMPLE_CHAR:   {},
            Game.TILE_SIMPLE_BAMBOO: {},

            Game.TILE_HONOR_DRAGON:  {},
            Game.TILE_HONOR_WIND:    {}
        }
        bonus  = []
        kongs  = []

        for tile in sorted(hand):
            if tile[0].startswith('bonus'):
                bonus.append(tile)
                last_piece = None
                same_cnt = 1
                continue
            if tile == last_piece:
                same_cnt += 1
                if same_cnt == Game.SIZE_KONG:
                    kongs.append(tile)
                    last_piece = None
                    same_cnt = 1
                    continue
            else:
                same_cnt = 1
            last_piece = tile
            if tile[1] in result[tile[0]]:
                result[tile[0]][tile[1]] += 1
            else:
                result[tile[0]][tile[1]] = 1
        return result, bonus, kongs