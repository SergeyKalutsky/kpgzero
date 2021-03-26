"""Names for constants returned by Pygame."""
from enum import IntEnum
import pygame.locals


# Event type indicating the end of a music track
MUSIC_END = 99


class mouse(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


# Use a code generation approach to copy Pygame's key constants out into
# a Python 3.4 IntEnum, stripping prefixes where possible
srclines = ["class keys(IntEnum):"]
for k, v in vars(pygame.locals).items():
    if k.startswith('K_'):
        if k[2].isalpha():
            k = k[2:]
        srclines.append("    %s = %d" % (k.upper(), v))

srclines.append("class keymods(IntEnum):")
for k, v in vars(pygame.locals).items():
    if k.startswith('KMOD_'):
        srclines.append("    %s = %d" % (k[5:].upper(), v))

exec('\n'.join(srclines), globals())
enum_list = list(map(int, keys))
print(enum_list)

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
            key = keys[kname.upper()]
        except AttributeError:
            raise AttributeError('The key "%s" does not exist' % key)
        return key.value in self._pressed

    def _press(self, key):
        """Called by Game to mark the key as pressed."""
        self._pressed.add(key)

    def _release(self, key):
        """Called by Game to mark the key as released."""
        self._pressed.discard(key)

    def __getitem__(self, k):
        if isinstance(k, keys):
            return k.value in self._pressed
        else:
            print(
                "String lookup in keyboard (eg. keyboard[%r]) is deprecated.")
            return getattr(self, k)

    def __repr__(self):
        return "<Keyboard pressed={}>".format(self._pressed)


keyboard = Keyboard()
# print(keyboard.keyboard)