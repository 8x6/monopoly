BOARD = [
  ['GO', 'Go',],
  ['Mediterranean', 'Ave',],
  ['Community', 'Chest',],
  ['Baltic', 'Ave',],
  ['Income', 'Tax',],
  ['Reading', 'Railroad',],
  ['Oriental', 'Ave',],
  ['Chance', 'Chance', ],
  ['Vermont', 'Ave',],
  ['Connecticut', 'Ave',],

  ['Just', 'Visiting',],
  ['St. Charles', 'Place',],
  ['Electric', 'Company',],
  ['States', 'Ave',],
  ['Virginia', 'Ave',],
  ['Pennsylvania', 'Railroad',],
  ['St. James', 'Place', ],
  ['Community', 'Chest',],
  ['Tennessee', 'Ave',],
  ['New York', 'Ave',],

  ['Free', 'Parking',],
  ['Kentucky', 'Ave',],
  ['Chance', 'Chance',],
  ['Indiana', 'Ave',],
  ['Illinois', 'Ave',],
  ['B. & O.', 'Railroad',],
  ['Atlantic', 'Ave',],
  ['Ventnor', 'Ave',],
  ['Water', 'Works',],
  ['Marvin', 'Gardens',],

  ['Go', 'To Jail',],
  ['Pacific', 'Ave',],
  ['North Carolina', 'Ave',], 
  ['Community', 'Chest',],
  ['Pennsylvania', 'Ave',],
  ['Short Line', 'Railroad',],
  ['Chance', 'Chance', ],
  ['Park', 'Place', ],
  ['Luxury', 'Tax',],
  ['Boardwalk', 'Boardwalk'],
]

import random


class Player:
    position = 0
    turns_left_in_jail = None

    def advance(self, spaces):
        self.position += spaces
        self.position = self.position % 40
        Rules().apply(self)

    def advance_to(self, new_position):
        if self.position > new_position:
            self.pass_go()
        self.position = new_position
        Rules().apply(self)

    def pass_go(self):
        pass

    def go_to_jail(self):
        # TODO: do not collect $200
        # TODO: Jail
        self.advance_to(10)

    def tell(self, num):
        print(' '.join(["Position %02d:" % self.position] + BOARD[self.position] + ["(roll: %d)" % num]))
   

class CardDeck:

    cards = None
    current = None

    def __init__(self):
        raise(NotImplementedError)

    def go_back_three_spaces(self, player):
        player.advance(-3)

    def go_to_jail(self, player):
        player.go_to_jail()

    def advance_to_st_charles_place(self, player):
        player.advance_to(11)

    def advance_to_boardwalk(self, player):
        player.advance_to(39)

    def advance_to_reading_railroad(self, player):
        player.advance_to(5)

    def advance_to_go(self, player):
        player.advance_to(0)

    def advance_to_illinois_ave(self, player):
        player.advance_to(24)

    def advance_to_nearest_railroad(self, player):
        if player.position < 5:
            player.advance_to(5)
        elif player.position < 15:
            player.advance_to(15)
        elif player.position < 25:
            player.advance_to(25)
        elif player.position < 35:
            player.advance_to(35)
        else:
            player.advance_to(5)

    def advance_to_nearest_utility(self, player):
        if player.position < 12:
            player.advance_to(12)
        elif player.position < 28:
            player.advance_to(28)
        else:
            player.advance_to(12)

    def pas(self, player):
        pass

    def draw(self, player):
        if self.current is None:
            self.current = 0
        else:
            self.current += 1
            if self.current >= len(self.cards):
                self.current = 0
        card = self.cards[self.current]
        print(' '.join((card[0], card[1])))
        rule_fn = card[2]
        rule_fn(player)


class ChanceDeck(CardDeck):

    def __init__(self):
        self.cards = [
            ['Pay', '15', self.pas],
            ['Get', 'out of jail free', self.pas],
            ['Advance', 'to Reading Railroad', self.advance_to_reading_railroad],
            ['Advance', 'to the nearest Utility', self.advance_to_nearest_utility],
            ['Go', 'To Jail', self.go_to_jail],
            ['Advance', 'to Boardwalk', self.advance_to_boardwalk],
            ['Pay', 'each player 50', self.pas],
            ['Advance', 'to Go', self.advance_to_go],
            ['Advance', 'to Illinoin Ave', self.advance_to_illinois_ave],
            ['Advance', 'to St. Charles Place', self.advance_to_st_charles_place],
            ['Collect', '150', self.pas],
            ['Advance', 'to the nearest Railroad', self.advance_to_nearest_railroad],
            ['Collect', '50', self.pas],
            ['Advance', 'to the nearest Railroad', self.advance_to_nearest_railroad],
            ['Go', 'back three spaces', self.go_back_three_spaces],
            ['Pay', 'General Repairs', self.pas],
        ]
        random.shuffle(self.cards)


class CommunityChestDeck(CardDeck):

    def __init__(self):
        self.cards = [
            ['Collect', '100', self.pas],
            ['Advance', 'to Go', self.advance_to_go],
            ['Pay', '100', self.pas],
            ['Collect', '100', self.pas],
            ['Pay', 'General Repairs', self.pas],
            ['Collect', '10', self.pas],
            ['Get', 'out of jail free', self.pas],
            ['Collect', '200', self.pas],
            ['Pay', '50', self.pas],
            ['Collect', '25', self.pas],
            ['Collect', '50', self.pas],
            ['Collect', '10 from each player', self.pas],
            ['Collect', '20', self.pas],
            ['Pay', '50', self.pas],
            ['Go', 'To Jail', self.go_to_jail],
            ['Collect', '100', self.pas],
        ]
        random.shuffle(self.cards)


CHANCE_DECK = ChanceDeck()
COMMUNITY_CHEST_DECK = CommunityChestDeck()

class Rules:

    def land_on_property(self, player, spot):
        pass

    def apply(self, player):
        spot = BOARD[player.position]
        type = spot[1]
        if type in ('Go', 'Visiting', 'Parking'):
            pass
        elif type == 'Tax':
            pass
        elif type in ('Ave', 'Place', 'Railroad', 'Company', 'Works', 'Gardens', 'Boardwalk'):
            self.land_on_property(player, spot)
        elif type == 'Chest':
            COMMUNITY_CHEST_DECK.draw(player)
        elif type == 'Chance':
            CHANCE_DECK.draw(player)
        elif type == 'To Jail':
            player.go_to_jail()
        else:
            raise ValueError(type)


class Game:
    def roll(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def demo_1(self):
        for ix in range(100):
            print self.roll()

        for ix in (0, 10, 20, 30):
            print(BOARD[ix])

    def test_1(self):
        for ix in range(100):
            roll = self.roll()
            assert roll >= 2
            assert roll <= 12

    def take_turn(self, player):
        roll = self.roll()
        player.advance(roll)
        player.tell(roll)
        Rules().apply(player)

    def test_2(self):
        p = Player()
        for ix in range(10000):
            self.take_turn(p)

    def test_3(self):
        counts = [0] * 40
        p = Player()
        for ix in range(1000000):
            self.take_turn(p)
            counts[p.position] += 1
        for ix in range(40):
            print("\t".join([str(counts[ix])] + BOARD[ix]))

Game().test_3()
