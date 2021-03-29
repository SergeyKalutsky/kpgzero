"""Names for constants returned by Pygame."""
from enum import IntEnum
import pygame.locals
import pygame


KEYS = {'AC_BACK': 1073742094,
        'UNKNOWN': 0,
        'BACKSPACE': 8,
        'TAB': 9,
        'CLEAR': 107374198,
        'RETURN': 13,
        'PAUSE': 1073741896,
        'ESCAPE': 27,
        'SPACE': 32,
        'QUOTE': 39,
        'COMMA': 44,
        'MINUS': 45,
        'PERIOD': 46,
        'SLASH': 47,
        'K_0': 48,
        'K_1': 49,
        'K_2': 50,
        'K_3': 51,
        'K_4': 52,
        'K_5': 53,
        'K_6': 54,
        'K_7': 55,
        'K_8': 56,
        'K_9': 57,
        'SEMICOLON': 59,
        'EQUALS': 61,
        'LEFTBRACKET': 91,
        'BACKSLASH': 92,
        'RIGHTBRACKET': 93,
        'BACKQUOTE': 96,
        'A': 97,
        'B': 98,
        'C': 99,
        'D': 100,
        'E': 101,
        'F': 102,
        'G': 103,
        'H': 104, 
        'I': 105, 'J': 106, 'K': 107, 
        'L': 108, 'M': 109, 'N': 110, 
        'O': 111, 'P': 112, 'Q': 113, 
        'R': 114, 'S': 115, 'T': 116, 
        'U': 117, 'V': 118, 'W': 119, 
        'X': 120, 'Y': 121, 'Z': 122, 
        'DELETE': 127, 'KP_0': 1073741922, 
        'KP_1': 1073741913, 'KP_2': 1073741914, 
        'KP_3': 1073741915, 'KP_4': 1073741916, 
        'KP_5': 1073741917, 'KP_6': 1073741918, 
        'KP_7': 1073741919, 'KP_8': 1073741920, 
        'KP_9': 1073741921, 'KP_PERIOD': 1073741923, 
        'KP_DIVIDE': 1073741908, 'KP_MULTIPLY': 1073741909, 
        'KP_MINUS': 1073741910, 'KP_PLUS': 1073741911, 
        'KP_ENTER': 1073741912, 'KP_EQUALS': 1073741927, 'UP': 1073741906,
        'DOWN': 1073741905, 'RIGHT': 1073741903, 'LEFT': 1073741904, 
        'INSERT': 1073741897, 'HOME': 1073741898, 'END': 1073741901, 
        'PAGEUP': 1073741899, 'PAGEDOWN': 1073741902, 'F1': 1073741882, 
        'F2': 1073741883, 'F3': 1073741884, 'F4': 1073741885, 'F5': 1073741886, 
        'F6': 1073741887, 'F7': 1073741888, 'F8': 1073741889, 'F9': 1073741890, 
        'F10': 1073741891, 'F11': 1073741892, 'F12': 1073741893, 'F13': 1073741928, 
        'F14': 1073741929, 'F15': 1073741930, 'NUMLOCKCLEAR': 1073741907, 
        'CAPSLOCK': 1073741881, 'SCROLLLOCK': 1073741895, 'RSHIFT': 1073742053, 
        'LSHIFT': 1073742049, 'RCTRL': 1073742052, 'LCTRL': 1073742048, 
        'RALT': 1073742054, 'LALT': 1073742050, 'RGUI': 1073742055, 
        'LGUI': 1073742051, 'MODE': 1073742081, 'HELP': 1073741941, 
        'PRINTSCREEN': 1073741894, 'SYSREQ': 1073741978, 'MENU': 1073741942, 
        'POWER': 1073741926, 'CURRENCYUNIT': 1073742004, 'CURRENCYSUBUNIT': 1073742005, 
        'EXCLAIM': 33, 'QUOTEDBL': 34, 'HASH': 35, 'DOLLAR': 36, 
        'AMPERSAND': 38, 'PERCENT': 37, 'LEFTPAREN': 40, 'RIGHTPAREN': 41, 
        'ASTERISK': 42, 'PLUS': 43, 'COLON': 58, 'LESS': 60, 
        'GREATER': 62, 'QUESTION': 63, 'AT': 64, 'CARET': 94, 'UNDERSCORE': 95}


class Keyboard:
    """The current state of the keyboard.
    Each attribute represents a key. For example, ::
        keyboard.a
    is True if the 'A' key is depressed, and False otherwise.
    """
    # The current key state. This may as well be a class attribute - there's
    # only one keyboard.
    _pressed = set()

    def __getattr__(self, kname):
        # return is a reserved word, so alias enter to return
        if kname == 'enter':
            kname = 'return'
        try:
            key = KEYS[kname.upper()]
        except AttributeError:
            raise AttributeError('The key "%s" does not exist' % key)
        return key in self._pressed

    def _press(self, key):
        """Called by Game to mark the key as pressed."""
        self._pressed.add(key)

    def _release(self, key):
        """Called by Game to mark the key as released."""
        self._pressed.discard(key)

    def __getitem__(self, k):
        return getattr(self, k)

    def __repr__(self):
        return "<Keyboard pressed={}>".format(self._pressed)


keyboard = Keyboard()
def exit(e):
    if e.type == pygame.QUIT:
        pygame.quit()


def init():
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption('TITLE')
    clock = pygame.time.Clock()
    return screen, clock

screen, clock_pg = init()

FPS = 60
while True:
    for event in pygame.event.get():
        exit(event)

        if event.type == pygame.KEYDOWN:
            keyboard._press(event.key)

        elif event.type == pygame.KEYUP:
            keyboard._release(event.key)

    print(keyboard.a)
    
    pygame.display.update()
    clock_pg.tick(FPS)
