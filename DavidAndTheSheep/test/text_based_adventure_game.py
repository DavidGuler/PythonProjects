"""
"""

import tkinter
import random
from msvcrt import getch

class UnpossibleCoordinates(Exception): pass
class UnpossibleDirection(Exception): pass
class UnrecognizedBoardElementType(Exception): pass
class UnrecognizedDirection(Exception): pass
class OnBoardElement(Exception): pass

# Consts
BOARD_WIDTH = 20
BOARD_HEIGHT = 6
BOARD_INIT_X = 22
BOARD_INIT_Y = 22

BOARD_WIDTH_LIMIT = BOARD_INIT_X + BOARD_WIDTH
BOARD_HEIGHT_LIMIT = BOARD_INIT_Y + BOARD_HEIGHT


POSSIBLE_DIFFS = (-1, 0, 1)
KEYS_TO_DIRECTIONS = {'w': 'up',
                      's': 'down',
                      'a': 'left',
                      'd': 'right'}
DIRECTIONS = {'up':    [0,1],
              'down':  [0,-1],
              'right': [1,0],
              'left':  [-1,0]}

BOARD_ELEMENTS_TYPES = {'vertical_wall': '|',
                        'horizontal_wall': '_',
                        'david_character': '^',
                        'sheep_goal': '*',
                        'clean': ' '}

class pos():
    """
    pos() -> object

    A class which creates a position object.
    Its purpose is to hold a position of any board element.

    It has the following attributes:
    x  (int)    - An coordinate on the X axis.
    y  (int)    - An coordinate on the Y axis.

    It has the following methods:
    _validate_coordinates - A function which validates the received coordinates.
    """

    def __init__(self, x, y):
        """
        __init__(self, x, y) -> pos object

        Initiates the object.
        It will assign the x and y to a new object, and validate 
        them using _validate_coordinates method.
        """
        self.x = x
        self.y = y
        self._validate_coordinates()

    def _validate_coordinates(self):
        """
        _validate_coordinates(self)

        Validates the new attributes of the new pos object.
        """

        # Validates the type of the new values.
        if type(self.x) not int or type(self.y) not int:
            raise TypeError

        # Validates that the values are in limits 
        # (which are defined by BOARD_WIDTH_LIMIT and BOARD_HEIGHT_LIMIT)
        if self.x < 0 or self.x > BOARD_WIDTH_LIMIT or \
           self.y < 0 or self.y > BOARD_HEIGHT_LIMIT:
            raise UnpossibleCoordinates


class direction():
    """
    direction() -> object

    A class which creates a direction object.
    Its purpose is to presents the direction of the character in the game,
    by holding the diff between the current location of the character,
    and its next location. The diff is in in both coordinates (x and y).

    It has the following attributes:
    x_diff  (int) - The diff in the X axis
    y_diff  (int) - The diff in the Y axis

    It has the following methods:
    _validate_diffs - Validates the new received diffs.
    """

    def __init__(self, x_diff, y_diff):
        """
        __init__(self, x_diff, y_diff) -> direction object

        Initiates a direction object.
        It assigns the x_diff and y_diff to the object, and then validates
        them using the _validate_diffs method.
        """
        self.x_diff = x
        self.y_diff = y
        self._validate_diffs()

    def _validate_diffs(self):
        """
        _validate_diffs(self)

        Validates the attributes of the new object.
        """

        # Validates the type of the diffs (int)
        if type(self.x_diff) not int or type(self.y_diff) not int:
            raise TypeError

        # Validates that the diffs are possible.
        # All possible values for the diffs are stored in the POSSIBLE_DIFFS list.
        if self.x_diff not in POSSIBLE_DIFFS or self.y_diff not in POSSIBLE_DIFFS:
            raise UnpossibleDirection

class board_element():
    """
    board_element() -> object

    A class which creates an board_element object.
    The board_element purpose is to create an element which has a position, and 
    a unique id. This element will be stored in a list, and the game will handle all
    the objects from it.

    It has the following attributes:
    pos                 (pos) - The position of the element.
    _board_element_type (str) - A string which describes the type of the element.
                                all possible types are defined in BOARD_ELEMENTS_TYPES dict.
    _id                 (str) - A string presents the unique id of the element.
    _index              (int) - An index of the element in the list which holds all elements.

    It has the following methods:
    id(self)    - a getter method for the _id attribute.

    """
    def __init__(self, board_element_type, board_index, x, y):
        """
        __init__(self, board_element_type, board_index, x, y)

        Initiates a new board element object.
        It assigns the type, index the coordinates of the object.
        """

        # Define the board element position
        self.pos = pos(x, y)
        self.board_element_type = board_element_type
        self.index = board_index
        self.id = None

    @property.getter()
    def id(self):
        """
        id(self) -> str

        Returns the id of the object.
        """

        # Checks if the attribute is already defined, and returns it.
        return self._id

    @property.setter()
    def id(self, val):
        """
        id(self)

        Creates the id of the object.
        """
        self._id = str(self.pos.x) + str(self.pos.y) + str(self._index) + self.board_element_type

    @property.getter()
    def index(self):
        """
        index(self) -> int

        Returns the index of the board element.
        """
        return _index

    @property.setter()
    def index(self, index):
        if type(index) not int:
            raise TypeError
        else:
            self._index = index

    @property.getter():
    def board_element_type(self):
        return self._board_element_type

    @property.setter()
    def board_element_type(self, board_element_type):
        if type(self.board_element_type) not str:
            raise TypeError

        elif self._board_element_type not in BOARD_ELEMENTS_TYPES.keys():
            raise UnrecognizedBoardElementType

        else:
            self._board_element_type = BOARD_ELEMENTS_TYPES[board_element_type]

    def __repr__(self):
        return self.board_element_type

class board_animation(board_element):
    """
    """
    def __init__(self, dir, *args):
        super(board_animation, self).__init__(*args)
        self.prev_pos = pos
        self.dir = direction(0,0)

    def set_direction(self, movement):
        """
        """
        if movement not in DIRECTIONS:
            raise UnrecognizedDirection

        self.dir = direction(*DIRECTIONS[movement])

    def update_pos(self):
        self.prev_pos = self.pos
        self.pos = pos(self.pos.x + self.dir.x_diff, self.pos.y + self.dir.y_diff)
        self.id = None


class board():
    
    def __init__(self):
        self.all_board_elements = []
        self.animation = None
        self.board_index = 0

        self.init_board()

    def _create_board_element(self, element_type, *args):
        new_board_element = element_type(*args)
        self.all_board_elements.append(new_board_element)
        self.board_index += 1

    def move(self):
        try:
            animation.update_pos()
            self._is_on_board_element()

        except OnBoardElement:
            pass
        except UnpossibleCoordinates:
            #! Fill here an error handling function
            return

    def get_movement(self):
        key = getch()

        if key in KEYS_TO_DIRECTIONS.keys():
            self.animation.set_direction(KEYS_TO_DIRECTIONS[key])

    def _is_on_board_element(self, board_element):
        for new_board_element in self.all_board_elements:
            if board_element.id == new_board_element.id:
                raise OnBoardElement

    def print_element(self, new_board_element):
        print(colorama.Cursor.POS(new_board_element.pos.x, new_board_element.pos.y) + \
            BOARD_ELEMENTS_TYPES[new_board_element.board_element_type])

    def _clear_screen(self):
        print(colorama.ansi.clear_screen())

    def print_board(self):
        self._clear_screen()
        for new_board_element in self.all_board_elements:
            self.print_element(new_board_element)

    def play(self):
        while True:
            continue

    def init_board(self):
        #EXAMPLE
        ho_walls = [[i, BOARD_INIT_Y - 1] for i in range(BOARD_INIT_X, BOARD_INIT_X + BOARD_WIDTH)] + \
                   [[i, BOARD_INIT_Y + 5] for i in range(BOARD_INIT_X, BOARD_INIT_X + BOARD_WIDTH)]
        ve_walls = [[BOARD_INIT_X, i] for i in range(BOARD_INIT_Y, BOARD_INIT_Y + BOARD_HEIGHT)] + \
                   [[BOARD_INIT_X + 7, i] for i in range(BOARD_INIT_Y + 2, BOARD_INIT_Y + 4)] + \
                   [[BOARD_INIT_X + BOARD_WIDTH, BOARD_INIT_Y + 1]] + [[BOARD_INIT_X + BOARD_WIDTH, BOARD_INIT_Y + 3]]
        for wall in ho_walls:
            self._create_board_element(board_element, 'horizontal_wall', self.board_index, *wall)

        for wall in ve_walls:
            self._create_board_element(board_element, 'vertical_wall', self.board_index, *wall)

        david = self._create_board_element(board_animation, 'david_character', self.board_index, BOARD_INIT_X + 3,BOARD_INIT_Y + 3)
        print("begin")
        self.print_board()


def main():
    print("begin")

    new_board = board()
    new_board.play()

if __name__ == "__main__":
    main()
    """
    try:
        new_board.init_board()
        new_board.play()
    except Exception as e:
        print(e)
        #new_board.finish_game()
    """



"""
board_outline = []

win32api.SetCursorPos((BOARD_HEIGHT, BOARD_WIDTH))
print("*")

import pyautogui, sys
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
"""