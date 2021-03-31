from types import MethodType
import re
import pygame
import time
from math import radians, sin, cos, atan2, degrees, sqrt, ceil, pi

PLATFORM = False
ANCHORS = {
    'x': {
        'left': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'right': 1.0,
    },
    'y': {
        'top': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'bottom': 1.0,
    }
}

SYMBOLIC_POSITIONS = set((
    "topleft", "bottomleft", "topright", "bottomright",
    "midtop", "midleft", "midbottom", "midright",
    "center"
))

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

KEYS_PLATFORM = {
        'UNKNOWN': 0,
        'BACKSPACE': 8,
        'TAB': 9,
        'RETURN': 13,
        'SPACE': 32,
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
        'A': 65,
        'B': 66,
        'C': 67,
        'D': 68,
        'E': 69,
        'F': 70,
        'G': 71,
        'H': 72, 
        'I': 73, 'J': 74, 'K': 75, 
        'L': 76, 'M': 77, 'N': 78, 
        'O': 79, 'P': 80, 'Q': 81, 
        'R': 82, 'S': 83, 'T': 84, 
        'U': 85, 'V': 86, 'W': 87, 
        'X': 88, 'Y': 89, 'Z': 90, 
        'DELETE': 127, 'KP_0': 1073741922, 
        'KP_1': 97, 'KP_2': 98, 
        'KP_3': 99, 'KP_4': 100, 
        'KP_5': 101, 'KP_6': 102, 
        'KP_7': 103, 'KP_8': 104, 
        'KP_9': 105, 'KP_PERIOD': 110, 
        'KP_DIVIDE': 111, 'KP_MULTIPLY': 106, 
        'KP_MINUS': 109, 'KP_PLUS': 107, 
        'UP': 273, 'DOWN': 274, 'RIGHT': 275, 'LEFT': 276, 
        'INSERT': 45, 'HOME': 36, 'END': 35, 
        'PAGEUP': 33, 'PAGEDOWN': 34, 'F1': 112, 
        'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 
        'F6': 117, 'F7': 118, 'F8': 119, 'F9': 120, 
        'F10': 121, 'F11': 122, 'F12': 123,  
        'NUMLOCKCLEAR': 144, 'CAPSLOCK': 20, 'LSHIFT': 16, 
        'RCTRL': 17, 'LCTRL': 17, 'RSHIFT': 16, 
        'RALT': 18, 'LALT': 18
}

# Provides more meaningful default-arguments e.g. for display in IDEs etc.
POS_TOPLEFT = None
ANCHOR_CENTER = None

MAX_ALPHA = 255  # Based on pygame's max alpha.

DEPRECATED_KEY_RE = re.compile(r'[A-Z]')
PREFIX_RE = re.compile(r'^K_(?!\d$)')

DEFAULT_FONT_SIZE = 24
REFERENCE_FONT_SIZE = 100
DEFAULT_LINE_HEIGHT = 1.0
DEFAULT_FONT_NAME = None
FONT_NAME_TEMPLATE = "%s.ttf "
DEFAULT_COLOR = "white"
DEFAULT_BACKGROUND = None
DEFAULT_OUTLINE_COLOR = "black"
DEFAULT_SHADOW_COLOR = "black"
OUTLINE_UNIT = 1 / 24
SHADOW_UNIT = 1 / 18
DEFAULT_ALIGN = "left"  # left, center, or right
DEFAULT_ANCHOR = 0, 0  # 0, 0 = top left ;  1, 1 = bottom right
DEFAULT_STRIP = True
ALPHA_RESOLUTION = 16
ANGLE_RESOLUTION_DEGREES = 3

AUTO_CLEAN = True
MEMORY_LIMIT_MB = 64
MEMORY_REDUCTION_FACTOR = 0.5

# ===================================== OPERATOR IMPLEMENTATION ==================================================================


class itemgetter:
    """
    Return a callable object that fetches the given item(s) from its operand.
    After f = itemgetter(2), the call f(r) returns r[2].
    After g = itemgetter(2, 5, 3), the call g(r) returns (r[2], r[5], r[3])
    """
    __slots__ = ('_items', '_call')

    def __init__(self, item):
        self._items = (item,)

        def func(obj):
            return obj[item]
        self._call = func

    def __call__(self, obj):
        return self._call(obj)

    def __repr__(self):
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__name__,
                              ', '.join(map(repr, self._items)))

    def __reduce__(self):
        return self.__class__, self._items


class attrgetter:
    """
    Return a callable object that fetches the given attribute(s) from its operand.
    After f = attrgetter('name'), the call f(r) returns r.name.
    After g = attrgetter('name', 'date'), the call g(r) returns (r.name, r.date).
    After h = attrgetter('name.first', 'name.last'), the call h(r) returns
    (r.name.first, r.name.last).
    """
    __slots__ = ('_attrs', '_call')

    def __init__(self, attr):
        if not isinstance(attr, str):
            raise TypeError('attribute name must be a string')
        self._attrs = (attr,)
        names = attr.split('.')

        def func(obj):
            for name in names:
                obj = getattr(obj, name)
            return obj
        self._call = func

    def __call__(self, obj):
        return self._call(obj)

    def __repr__(self):
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__qualname__,
                              ', '.join(map(repr, self._attrs)))

    def __reduce__(self):
        return self.__class__, self._attrs

# ===================================== HEAPQ PARTIAL IMPLEMENTATION ==============================================================


class HeapqPartial:
    # Код взят из https://github.com/python/cpython/blob/2d1cbe4193499914ccc9d217ea63eb17ff927c91/Lib/heapq.py#L258
    # Поскольку heapq не портирован в Sculpt
    def heapify(self, x):
        """Transform list into a heap, in-place, in O(len(x)) time."""
        n = len(x)
        # Transform bottom-up.  The largest index there's any point to looking at
        # is the largest with a child index in-range, so must have 2*i + 1 < n,
        # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
        # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
        # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
        # Выглядит уродливо, но reversed на платформе не работает
        for i in range((n//2)-1, -1, -1):
            self._siftup(x, i)

    def heappop(self, heap):
        """Pop the smallest item off the heap, maintaining the heap invariant."""
        lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
        if heap:
            returnitem = heap[0]
            heap[0] = lastelt
            self._siftup(heap, 0)
            return returnitem
        return lastelt

    def _siftup(self, heap, pos):
        endpos = len(heap)
        startpos = pos
        newitem = heap[pos]
        # Bubble up the smaller child until hitting a leaf.
        childpos = 2*pos + 1    # leftmost child position
        while childpos < endpos:
            # Set childpos to index of smaller child.
            rightpos = childpos + 1
            if rightpos < endpos and not heap[childpos] < heap[rightpos]:
                childpos = rightpos
            # Move the smaller child up.
            heap[pos] = heap[childpos]
            pos = childpos
            childpos = 2*pos + 1
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).
        heap[pos] = newitem
        self._siftdown(heap, startpos, pos)

    def _siftdown(self, heap, startpos, pos):
        newitem = heap[pos]
        # Follow the path to the root, moving parents down until finding a place
        # newitem fits.
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = heap[parentpos]
            if newitem < parent:
                heap[pos] = parent
                pos = parentpos
                continue
            break
        heap[pos] = newitem

    def heappush(self, heap, item):
        """Push item onto heap, maintaining the heap invariant."""
        heap.append(item)
        self._siftdown(heap, 0, len(heap)-1)


heapq = HeapqPartial()
# =================================================== IMAGE LOADER WRAPPER ====================================================================


class ImageLoader:

    def __init__(self):
        self._cache = {}

    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'image'

    def __repr__(self):
        return "<Images images={}>".format(self.__dir__())

    def cache_key(self, name, args, kwargs):
        kwpairs = sorted(kwargs.items())
        return (name, args, tuple(kwpairs))

    def unload(self, name, *args, **kwargs):
        key = self.cache_key(name, args, kwargs)
        if key in self._cache:
            del self._cache[key]

    def unload_all(self):
        self._cache.clear()

    def load(self, name, *args, **kwargs):
        key = self.cache_key(name, args, kwargs)
        if key in self._cache:
            return self._cache[key]

        res = None
        for ext in self.EXTNS:
            path = name + '.' + ext
            try:
                res = pygame.image.load(path).convert_alpha()
                break
            except:
                pass

        if res is not None:
            return res
        else:
            raise ValueError('Image ' + name + ' not found')


images = ImageLoader()

# ============================================== TEXT WRAPPAER ====================================================================================

_font_cache = {}

def getfont(fontname=None, fontsize=None, sysfontname=None,
            bold=None, italic=None, underline=None):
    if fontname is not None and sysfontname is not None:
        raise ValueError("Can't set both fontname and sysfontname")
    if fontname is None and sysfontname is None:
        fontname = DEFAULT_FONT_NAME
    if fontsize is None:
        fontsize = DEFAULT_FONT_SIZE
    key = fontname, fontsize, sysfontname, bold, italic, underline
    if key in _font_cache:
        return _font_cache[key]
    if sysfontname is not None:
        font = pygame.font.SysFont(
            sysfontname, fontsize, bold or False, italic or False)
    else:
        if fontname is not None:
            fontname = FONT_NAME_TEMPLATE % fontname
        try:
            font = pygame.font.Font(fontname, fontsize)
        except IOError:
            raise IOError("unable to read font filename: %s" % fontname)
    if bold is not None:
        font.set_bold(bold)
    if italic is not None:
        font.set_italic(italic)
    if underline is not None:
        font.set_underline(underline)
    _font_cache[key] = font
    return font


def _resolvecolor(color, default):
    if color is None:
        color = default
    if color is None:
        return None
    try:
        return tuple(make_color(color))
    except ValueError:
        return tuple(color)


_unrotated_size = {}
_tick = 0


class Ptext:
    def draw(self, text, pos=None,
            fontname=None, fontsize=None, sysfontname=None,
            antialias=True, bold=None, italic=None, underline=None,
            color=None, background=None,
            top=None, left=None, bottom=None, right=None,
            topleft=None, bottomleft=None, topright=None, bottomright=None,
            midtop=None, midleft=None, midbottom=None, midright=None,
            center=None, centerx=None, centery=None,
            align=None,
            shadow=None, scolor=None,
            alpha=1.0,
            anchor=None,
            angle=0,
            surf=None,
            cache=True):

        if topleft:
            left, top = topleft
        if bottomleft:
            left, bottom = bottomleft
        if topright:
            right, top = topright
        if bottomright:
            right, bottom = bottomright
        if midtop:
            centerx, top = midtop
        if midleft:
            left, centery = midleft
        if midbottom:
            centerx, bottom = midbottom
        if midright:
            right, centery = midright
        if center:
            centerx, centery = center

        x, y = pos or (None, None)
        hanchor, vanchor = anchor or (None, None)
        if left is not None:
            x, hanchor = left, 0
        if centerx is not None:
            x, hanchor = centerx, 0.5
        if right is not None:
            x, hanchor = right, 1
        if top is not None:
            y, vanchor = top, 0
        if centery is not None:
            y, vanchor = centery, 0.5
        if bottom is not None:
            y, vanchor = bottom, 1
        if x is None:
            raise ValueError("Unable to determine horizontal position")
        if y is None:
            raise ValueError("Unable to determine vertical position")

        if align is None:
            align = hanchor
        if hanchor is None:
            hanchor = DEFAULT_ANCHOR[0]
        if vanchor is None:
            vanchor = DEFAULT_ANCHOR[1]
        
        font = getfont(fontname, fontsize, sysfontname, bold, italic, underline)
        if background is not None:
            tsurf = font.render(text, antialias, _resolvecolor(color, 'white'), background)
        else:
            tsurf = font.render(text, antialias, _resolvecolor(color, 'white'))

        if angle:
            w0, h0 = _unrotated_size[(tsurf.get_size(), angle, text)]
            S, C = sin(radians(angle)), cos(radians(angle))
            dx, dy = (0.5 - hanchor) * w0, (0.5 - vanchor) * h0
            x += dx * C + dy * S - 0.5 * tsurf.get_width()
            y += -dx * S + dy * C - 0.5 * tsurf.get_height()
        else:
            x -= hanchor * tsurf.get_width()
            y -= vanchor * tsurf.get_height()
        x = int(round(x))
        y = int(round(y))

        surf.blit(tsurf, (x, y))

ptext = Ptext()

# ================================================= CALLBACK WRAPPER ===========================================================================


def mkref(o):
    return lambda: o


class Event:
    """An event scheduled for a future time.
    Events are ordered by their scheduled execution time.
    """

    def __init__(self, time, cb, repeat=None):
        self.time = time
        self.repeat = repeat
        self.cb = mkref(cb)
        self.name = str(cb)
        self.repeat = repeat

    def __lt__(self, ano):
        return self.time < ano.time

    def __eq__(self, ano):
        return self.time == ano.time

    @property
    def callback(self):
        return self.cb()


class Clock:
    """A clock used for event scheduling.
    When tick() is called, all events scheduled for before now will be called
    in order.
    tick() would typically be called from the game loop for the default clock.
    Additional clocks could be created - for example, a game clock that could
    be suspended in pause screens. Your code must take care of calling tick()
    or not. You could also run the clock at a different rate if desired, by
    scaling dt before passing it to tick().
    """

    def __init__(self):
        self.t = 0
        self.fired = False
        self.events = []
        self._each_tick = []

    def clear(self):
        """Remove all handlers from this clock."""
        self.events.clear()
        self._each_tick.clear()

    def schedule(self, callback, delay):
        """Schedule callback to be called once, at `delay` seconds from now.
        :param callback: A parameterless callable to be called.
        :param delay: The delay before the call (in clock time / seconds).
        """
        heapq.heappush(self.events, Event(self.t + delay, callback, None))

    def schedule_unique(self, callback, delay):
        """Schedule callback to be called once, at `delay` seconds from now.
        If it was already scheduled, postpone its firing.
        :param callback: A parameterless callable to be called.
        :param delay: The delay before the call (in clock time / seconds).
        """
        self.unschedule(callback)
        self.schedule(callback, delay)

    def schedule_interval(self, callback, delay):
        """Schedule callback to be called every `delay` seconds.
        The first occurrence will be after `delay` seconds.
        :param callback: A parameterless callable to be called.
        :param delay: The interval in seconds.
        """
        heapq.heappush(self.events, Event(self.t + delay, callback, delay))

    def unschedule(self, callback):
        """Unschedule the given callback.
        If scheduled multiple times all instances will be unscheduled.
        """
        self.events = [
            e for e in self.events
            if e.callback != callback
            if e.callback is not None
        ]
        heapq.heapify(self.events)
        self._each_tick = [e for e in self._each_tick if e() != callback]

    def each_tick(self, callback):
        """Schedule a callback to be called every tick.
        Unlike the standard scheduler functions, the callable is passed the
        elapsed clock time since the last call (the same value passed to tick).
        """
        self._each_tick.append(mkref(callback))

    def _fire_each_tick(self, dt):
        dead = [None]
        for r in self._each_tick:
            cb = r()
            if cb is not None:
                self.fired = True
                try:
                    cb(dt)
                except:
                    pass
        self._each_tick = [e for e in self._each_tick if e() not in dead]

    def tick(self, dt):
        """Update the clock time and fire all scheduled events.
        :param dt: The elapsed time in seconds.
        """
        self.fired = False
        self.t += float(dt)
        self._fire_each_tick(dt)
        while self.events and self.events[0].time <= self.t:
            ev = heapq.heappop(self.events)
            cb = ev.callback
            if not cb:
                continue

            if ev.repeat is not None:
                self.schedule_interval(cb, ev.repeat)

            self.fired = True
            try:
                cb()
            except Exception:
                self.unschedule(cb)

# ==================================================== SCREEN/SURFACE WRAPPERS ===================================================================

def round_pos(pos):
    """Round a tuple position so it can be used for drawing."""
    try:
        x, y = pos
    except TypeError:
        raise TypeError(
            "Coordinate must be a tuple (not {!r})".format(pos)) 
    try:
        return round(x), round(y)
    except TypeError:
        raise TypeError("Coordinate values must be numbers (not {!r})".format(pos)) 

COLORS = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'black': (0, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255,255,0),
    'blue': (0, 0, 255),
    'orange': (255, 69, 0)
}

def convert_hex_color(hex_color):
    h = hex_color.lstrip('#')
    rgb_color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb_color

def make_color(arg):
    if isinstance(arg, tuple):
        return arg
    if arg.lower() in COLORS:
        return COLORS[arg.lower()]
    elif arg.lower()[0] == '#':
        return convert_hex_color(arg.lower())
    else:
        raise AttributeError('The color "%s" does not exist' % arg.lower())


class SurfacePainter:
    """Interface to pygame.draw that is bound to a surface."""

    def __init__(self, screen):
        self._screen = screen

    @property
    def _surf(self):
        return self._screen.surface

    def line(self, start, end, color, width=1):
        """Draw a line from start to end."""
        start = round_pos(start)
        end = round_pos(end)
        pygame.draw.line(self._surf, make_color(color), start, end, width)

    def circle(self, pos, radius, color, width=1):
        """Draw a circle."""
        pos = round_pos(pos)
        pygame.draw.circle(self._surf, make_color(color), pos, radius, width)

    def filled_circle(self, pos, radius, color):
        """Draw a filled circle."""
        pos = round_pos(pos)
        pygame.draw.circle(self._surf, make_color(color), pos, radius, 0)

    def polygon(self, points, color):
        """Draw a polygon."""
        try:
            iter(points)
        except TypeError:
            raise TypeError("screen.draw.filled_polygon() requires an iterable of points to draw")   # noqa
        points = [round_pos(point) for point in points]
        pygame.draw.polygon(self._surf, make_color(color), points, 1)

    def filled_polygon(self, points, color):
        """Draw a filled polygon."""
        try:
            iter(points)
        except TypeError:
            raise TypeError("screen.draw.filled_polygon() requires an iterable of points to draw")   # noqa
        points = [round_pos(point) for point in points]
        pygame.draw.polygon(self._surf, make_color(color), points, 0)

    def rect(self, rect, color, width=1):
        """Draw a rectangle."""
        if not isinstance(rect, RECT_CLASSES):
            raise TypeError("screen.draw.rect() requires a rect to draw")
        pygame.draw.rect(self._surf, make_color(color), rect, width)

    def filled_rect(self, rect, color):
        """Draw a filled rectangle."""
        if not isinstance(rect, RECT_CLASSES):
            raise TypeError(
                "screen.draw.filled_rect() requires a rect to draw")
        pygame.draw.rect(self._surf, make_color(color), rect, rect.width)

    def text(self, *args, **kwargs):
        """Draw text to the screen."""
        # FIXME: expose ptext parameters, for autocompletion and autodoc
        ptext.draw(*args, surf=self._surf, **kwargs)

    def set_at(self, rect_points, color):
        # Метод set_at на платформе сломан
        rect = Rect(rect_points[0], rect_points[1], 1, 1)
        self.filled_rect(rect, make_color(color))


class Screen:
    """Interface to the screen."""

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

    def bounds(self):
        """Return a Rect representing the bounds of the screen."""
        return ZRect((0, 0), (self.width, self.height))

    def clear(self):
        """Clear the screen to black."""
        self.fill((0, 0, 0))

    def fill(self, color, gcolor=None):
        """Fill the screen with a colour."""
        self.surface.fill(make_color(color))

    def blit(self, image, pos):
        """Draw a sprite onto the screen.
        "blit" is an archaic name for this operation, but one that is is still
        frequently used, for example in Pygame. See the `Wikipedia article`__
        for more about the etymology of the term.
        .. __: http://en.wikipedia.org/wiki/Bit_blit
        :param image: A Surface or the name of an image object to load.
        :param pos: The coordinates at which the top-left corner of the sprite
                    will be positioned. This may be given as a pair of
                    coordinates or as a Rect. If a Rect is given the sprite
                    will be drawn at ``rect.topleft``.
        """
        if isinstance(image, str):
            image = images.load(image)
        self.surface.blit(image, pos)

    @property
    def draw(self):
        return SurfacePainter(self)

    def __repr__(self):
        return "<Screen width={} height={}>".format(self.width, self.height)


# ================================================= KEYBOARD/KEYS WRAPPER =======================================================

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
            key = KEYS[kname.upper()] if not PLATFORM else KEYS_PLATFORM[kname.upper()]
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


class Keys:
    def __getattr__(self, kname):
        if kname == 'enter':
            kname = 'return'
        try:
            key = KEYS[kname.upper()] if not PLATFORM else KEYS_PLATFORM[kname.upper()]
        except AttributeError:
            raise AttributeError('The key "%s" does not exist' % key)
        return key


keyboard = Keyboard()
keys = Keys()

# ================================================= ACTOR WRAPPER ===============================================================================

class Rect(pygame.Rect):
    __slots__ = ()

    # From Pygame docs
    VALID_ATTRIBUTES = """
        x y
        top  left  bottom  right
        topleft  bottomleft  topright  bottomright
        midtop  midleft  midbottom  midright
        center  centerx  centery
        size  width  height
        w h
    """.split()

    def __setattr__(self, key, value):
        try:
            pygame.Rect.__setattr__(self, key, value)
        except AttributeError as e:
            raise e


class ZRect:
    """ZRect
    This is a Python implementation of the pygame Rect class. Its raison
    d'être is to allow the coordinates to be floating point. All pygame
    functions which require a rect allow for an object with a "rect"
    attribute and whose coordinates will be converted to integers implictly.
    All functions which require a dict will use the flexible constructor
    to convert from: this (or a subclass); a Pygame Rect; a 4-tuple or a
    pair of 2-tuples. In addition, they'll recognise any object which has
    an (optionally callable) .rect attribute whose value will be used instead.
    """

    _item_mapping = dict(enumerate("xywh"))

    def __init__(self, *args):
        
        if len(args) == 1:
            args = tuple(self._handle_one_arg(args[0]))

        #
        # At this point we have one of:
        #
        # x, y, w, h
        # (x, y), (w, h)
        # (x, y, w, h),
        #
        if len(args) == 4:
            self.x, self.y, self.w, self.h = args
        elif len(args) == 2:
            (self.x, self.y), (self.w, self.h) = args
        elif len(args) == 1:
            self.x, self.y, self.w, self.h = args[0]
        else:
            raise TypeError(
                "%s should be called with one, two or four arguments"
                % (self.__class__.__name__)
            )
        
        self.rect = self
    
    def _handle_one_arg(self, arg):
        """Handle -- possibly recursively -- the case of one parameter
        Pygame -- and consequently pgzero -- is very accommodating when constructing
        a rect. You can pass four integers, two pairs of 2-tuples, or one 4-tuple.
        Also, you can pass an existing Rect-like object, or an object with a .rect
        attribute. The object named by the .rect attribute is either one of the above,
        or it's a callable object which returns one of the above.
        This is evidently a recursive solution where an object with a .rect
        attribute can yield an object with a .rect attribute, and so ad infinitum.
        """
        #
        # If the arg is an existing rect, return its elements
        #
        
        if isinstance(arg, RECT_CLASSES):
            return arg.x, arg.y, arg.w, arg.h
        #
        # If it's something with a .rect attribute, start again with
        # that attribute, calling it first if it's callable
        #
        if hasattr(arg, "rect"):
            rectobj = arg.rect
            if callable(rectobj):
                rectobj = rectobj()
            return self._handle_one_arg(rectobj)

        #
        # Otherwise, we assume it's an iterable of four elements
        #
        
        return arg

    def __repr__(self):
        return "<%s (x: %s, y: %s, w: %s, h: %s)>" % (
            self.__class__.__name__, self.x, self.y, self.w, self.h)

    def __reduce__(self):
        return self.__class__, (self.x, self.y, self.w, self.h)

    def copy(self):
        return self.__class__(self.x, self.y, self.w, self.h)
    __copy__ = copy

    def __len__(self):
        return 4

    def __getitem__(self, item):
        try:
            return getattr(self, self._item_mapping[item])
        except KeyError:
            raise IndexError

    def __setitem__(self, item, value):
        try:
            attribute = self._item_mapping[item]
        except KeyError:
            raise IndexError
        else:
            setattr(attribute, value)

    def __bool__(self):
        return self.w != 0 and self.h != 0

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h

    def __hash__(self):
        raise TypeError("ZRect instances may not be used as dictionary keys")

    def __eq__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) == (rect.x, rect.y, rect.w, rect.h)

    def __ne__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) != (rect.x, rect.y, rect.w, rect.h)

    def __lt__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) < (rect.x, rect.y, rect.w, rect.h)

    def __gt__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) > (rect.x, rect.y, rect.w, rect.h)

    def __le__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) <= (rect.x, rect.y, rect.w, rect.h)

    def __ge__(self, *other):
        rect = self.__class__(*other)
        return (self.x, self.y, self.w, self.h) >= (rect.x, rect.y, rect.w, rect.h)

    def __contains__(self, other):
        """Test whether a point (x, y) or another rectangle
        (anything accepted by ZRect) is contained within this ZRect
        """
        if len(other) == 2:
            return self.collidepoint(*other)
        else:
            return self.contains(*other)

    def _get_width(self):
        return self.w

    def _set_width(self, width):
        self.w = width
    width = property(_get_width, _set_width)

    def _get_height(self):
        return self.h

    def _set_height(self, height):
        self.h = height
    height = property(_get_height, _set_height)

    def _get_top(self):
        return self.y

    def _set_top(self, top):
        self.y = top
    top = property(_get_top, _set_top)

    def _get_left(self):
        return self.x

    def _set_left(self, left):
        self.x = left
    left = property(_get_left, _set_left)

    def _get_right(self):
        return self.x + self.w

    def _set_right(self, right):
        self.x = right - self.w
    right = property(_get_right, _set_right)

    def _get_bottom(self):
        return self.y + self.h

    def _set_bottom(self, bottom):
        self.y = bottom - self.h
    bottom = property(_get_bottom, _set_bottom)

    def _get_centerx(self):
        return self.x + (self.w / 2)

    def _set_centerx(self, centerx):
        self.x = centerx - (self.w / 2)
    centerx = property(_get_centerx, _set_centerx)

    def _get_centery(self):
        return self.y + (self.h / 2)

    def _set_centery(self, centery):
        self.y = centery - (self.h / 2)
    centery = property(_get_centery, _set_centery)

    def _get_topleft(self):
        return self.x, self.y

    def _set_topleft(self, topleft):
        self.x, self.y = topleft
    topleft = property(_get_topleft, _set_topleft)

    def _get_topright(self):
        return self.x + self.w, self.y

    def _set_topright(self, topright):
        x, y = topright
        self.x = x - self.w
        self.y = y
    topright = property(_get_topright, _set_topright)

    def _get_bottomleft(self):
        return self.x, self.y + self.h

    def _set_bottomleft(self, bottomleft):
        x, y = bottomleft
        self.x = x
        self.y = y - self.h
    bottomleft = property(_get_bottomleft, _set_bottomleft)

    def _get_bottomright(self):
        return self.x + self.w, self.y + self.h

    def _set_bottomright(self, bottomright):
        x, y = bottomright
        self.x = x - self.w
        self.y = y - self.h
    bottomright = property(_get_bottomright, _set_bottomright)

    def _get_midtop(self):
        return self.x + self.w / 2, self.y

    def _set_midtop(self, midtop):
        x, y = midtop
        self.x = x - self.w / 2
        self.y = y
    midtop = property(_get_midtop, _set_midtop)

    def _get_midleft(self):
        return self.x, self.y + self.h / 2

    def _set_midleft(self, midleft):
        x, y = midleft
        self.x = x
        self.y = y - self.h / 2
    midleft = property(_get_midleft, _set_midleft)

    def _get_midbottom(self):
        return self.x + self.w / 2, self.y + self.h

    def _set_midbottom(self, midbottom):
        x, y = midbottom
        self.x = x - self.w / 2
        self.y = y - self.h
    midbottom = property(_get_midbottom, _set_midbottom)

    def _get_midright(self):
        return self.x + self.w, self.y + self.h / 2

    def _set_midright(self, midright):
        x, y = midright
        self.x = x - self.w
        self.y = y - self.h / 2
    midright = property(_get_midright, _set_midright)

    def _get_center(self):
        return self.x + self.w / 2, self.y + self.h / 2

    def _set_center(self, center):
        x, y = center
        self.x = x - self.w / 2
        self.y = y - self.h / 2
    center = property(_get_center, _set_center)

    def _get_size(self):
        return self.w, self.h

    def _set_size(self, size):
        self.w, self.h = size
    size = property(_get_size, _set_size)

    def move(self, x, y):
        return self.__class__(self.x + x, self.y + y, self.w, self.h)

    def move_ip(self, x, y):
        self.x += x
        self.y += y

    def _inflated(self, x, y):
        return self.x - x / 2, self.y - y / 2, self.w + x, self.h + y

    def inflate(self, x, y):
        return self.__class__(*self._inflated(x, y))

    def inflate_ip(self, x, y):
        self.x, self.y, self.w, self.h = self._inflated(x, y)

    def _clamped(self, *other):
        rect = self.__class__(*other)

        if self.w >= rect.w:
            x = rect.x + rect.w / 2 - self.w / 2
        elif self.x < rect.x:
            x = rect.x
        elif self.x + self.w > rect.x + rect.w:
            x = rect.x + rect.w - self.w
        else:
            x = self.x

        if self.h >= rect.h:
            y = rect.y + rect.h / 2 - self.h / 2
        elif self.y < rect.y:
            y = rect.y
        elif self.y + self.h > rect.y + rect.h:
            y = rect.y + rect.h - self.h
        else:
            y = self.y

        return x, y

    def clamp(self, *other):
        rect = self.__class__(*other)
        x, y = self._clamped(rect)
        return self.__class__(x, y, self.w, self.h)

    def clamp_ip(self, *other):
        rect = self.__class__(*other)
        self.x, self.y = self._clamped(rect)

    def _clipped(self, *other):
        rect = self.__class__(*other)

        if self.x >= rect.x and self.x < (rect.x + rect.w):
            x = self.x
        elif rect.x >= self.x and rect.x < (self.x + self.w):
            x = rect.x
        else:
            raise 'NoIntersect'

        if (self.x + self.w) > rect.x and (self.x + self.w) <= (rect.x + rect.w):
            w = self.x + self.w - x
        elif (rect.x + rect.w) > self.x and (rect.x + rect.w) <= (self.x + self.w):
            w = rect.x + rect.w - x
        else:
            raise 'NoIntersect'

        if self.y >= rect.y and self.y < (rect.y + rect.h):
            y = self.y
        elif rect.y >= self.y and rect.y < (self.y + self.h):
            y = rect.y
        else:
            raise 'NoIntersect'

        if (self.y + self.h) > rect.y and (self.y + self.h) <= (rect.y + rect.h):
            h = self.y + self.h - y
        elif (rect.y + rect.h) > self.y and (rect.y + rect.h) <= (self.y + self.h):
            h = rect.y + rect.h - y
        else:
            raise 'NoIntersect'

        return x, y, w, h

    def clip(self, *other):
        rect = self.__class__(*other)
        try:
            x, y, w, h = self._clipped(rect)
        except:
            x, y, w, h = self.x, self.y, 0, 0
        return self.__class__(x, y, w, h)

    def clip_ip(self, *other):
        rect = self.__class__(*other)
        try:
            self.x, self.y, self.w, self.h = self._clipped(rect)
        except:
            self.x, self.y, self.w, self.h = self.x, self.y, 0, 0

    def _unioned(self, *other):
        rect = self.__class__(*other)
        x = min(self.x, rect.x)
        y = min(self.y, rect.y)
        w = max(self.x + self.w, rect.x + rect.w) - x
        h = max(self.y + self.h, rect.y + rect.h) - y
        return x, y, w, h

    def union(self, *other):
        rect = self.__class__(*other)
        return self.__class__(*self._unioned(rect))

    def union_ip(self, *other):
        rect = self.__class__(*other)
        self.x, self.y, self.w, self.h = self._unioned(rect)

    def _unionalled(self, others):
        allrects = [self] + [self.__class__(other) for other in others]
        x = min(r.x for r in allrects)
        y = min(r.y for r in allrects)
        w = max(r.x + r.w for r in allrects) - x
        h = max(r.y + r.h for r in allrects) - y
        return x, y, w, h

    def unionall(self, others):
        return self.__class__(*self._unionalled(others))

    def unionall_ip(self, others):
        self.x, self.y, self.w, self.h = self._unionalled(others)

    def fit(self, *other):
        rect = self.__class__(*other)
        ratio = max(self.w / rect.w, self.h / rect.h)
        w = self.w / ratio
        h = self.h / ratio
        x = rect.x + (rect.w - w) / 2
        y = rect.y + (rect.h - h) / 2
        return self.__class__(x, y, w, h)

    def normalize(self):
        if self.w < 0:
            self.x += self.w
            self.w = abs(self.w)
        if self.h < 0:
            self.y += self.h
            self.h = abs(self.h)

    def contains(self, *other):
        rect = self.__class__(*other)
        return (
            self.x <= rect.x and
            self.y <= rect.y and
            self.x + self.w >= rect.x + rect.w and
            self.y + self.h >= rect.y + rect.h and
            self.x + self.w > rect.x and
            self.y + self.h > rect.y
        )

    def collidepoint(self, *args):
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args
        return (
            self.x <= x < (self.x + self.w) and
            self.y <= y < (self.y + self.h)
        )

    def colliderect(self, *other):
        rect = self.__class__(*other)
        return (
            self.x < rect.x + rect.w and
            self.y < rect.y + rect.h and
            self.x + self.w > rect.x and
            self.y + self.h > rect.y
        )

    def collidelist(self, others):
        for n, other in enumerate(others):
            if self.colliderect(other):
                return n
        else:
            return -1

    def collidelistall(self, others):
        return [n for n, other in enumerate(others) if self.colliderect(other)]

    def collidedict(self, dict, use_values=True):
        for k, v in dict.items():
            if self.colliderect(v if use_values else k):
                return k, v

    def collidedictall(self, dict, use_values=True):
        val = itemgetter(1 if use_values else 0)
        return [i for i in dict.items() if self.colliderect(val(i))]


RECT_CLASSES = (pygame.Rect, ZRect)


def calculate_anchor(value, dim, total):
    if isinstance(value, str):
        try:
            return total * ANCHORS[dim][value]
        except KeyError:
            raise ValueError(
                '%r is not a valid %s-anchor name' % (value, dim)
            )
    return float(value)


def transform_anchor(ax, ay, w, h, angle):
    """Transform anchor based upon a rotation of a surface of size w x h."""
    theta = -radians(angle)

    sintheta = sin(theta)
    costheta = cos(theta)

    # Dims of the transformed rect
    tw = abs(w * costheta) + abs(h * sintheta)
    th = abs(w * sintheta) + abs(h * costheta)

    # Offset of the anchor from the center
    cax = ax - w * 0.5
    cay = ay - h * 0.5

    # Rotated offset of the anchor from the center
    rax = cax * costheta - cay * sintheta
    ray = cax * sintheta + cay * costheta

    return (
        tw * 0.5 + rax,
        th * 0.5 + ray
    )


def _set_angle(actor, current_surface):
    if actor._angle % 360 == 0:
        # No changes required for default angle.
        return current_surface
    return pygame.transform.rotate(current_surface, actor._angle)


def _set_opacity(actor, current_surface):
    alpha = int(actor.opacity * MAX_ALPHA + 0.5)  # +0.5 for rounding up.

    if alpha == MAX_ALPHA:
        # No changes required for fully opaque surfaces (corresponds to the
        # default opacity of the current_surface).
        return current_surface

    alpha_img = pygame.Surface(current_surface.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, alpha))
    alpha_img.blit(
        current_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )
    return alpha_img


class Actor:
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS
    DELEGATED_ATTRIBUTES = [
        a for a in dir(ZRect) if not a.startswith("_")
    ]

    function_order = [_set_opacity, _set_angle]
    _anchor = _anchor_value = (0, 0)
    _angle = 0.0
    _opacity = 1.0

    def _build_transformed_surf(self):
        cache_len = len(self._surface_cache)
        if cache_len == 0:
            last = self._orig_surf
        else:
            last = self._surface_cache[-1]
        for f in self.function_order[cache_len:]:
            new_surf = f(self, last)
            self._surface_cache.append(new_surf)
            last = new_surf
        return self._surface_cache[-1]

    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._handle_unexpected_kwargs(kwargs)

        self._surface_cache = []
        self.__dict__["_rect"] = ZRect((0, 0), (0, 0))
        # Initialise it at (0, 0) for size (0, 0).
        # We'll move it to the right place and resize it later

        self.image = image
        self._init_position(pos, anchor, **kwargs)
    

    def __getattr__(self, attr):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        elif attr in dir(self):
            return getattr(self._rect, attr)
        else:
            raise AttributeError('Attribute {} does not exist'.format(attr))

    def __setattr__(self, attr, value):
        """Assign rect attributes to the underlying rect."""
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return setattr(self._rect, attr, value)
        else:
            # Ensure data descriptors are set normally
            return object.__setattr__(self, attr, value)

    def __iter__(self):
        return iter(self._rect)

    def __repr__(self):
        return '<{} {!r} pos={!r}>'.format(
            type(self).__name__,
            self._image_name,
            self.pos
        )

    def __dir__(self):
        standard_attributes = [
            key
            for key in self.__dict__.keys()
            if not key.startswith("_")
        ]
        return standard_attributes + self.__class__.DELEGATED_ATTRIBUTES

    def _handle_unexpected_kwargs(self, kwargs):
        unexpected_kwargs = set(kwargs.keys()) - self.EXPECTED_INIT_KWARGS
        if not unexpected_kwargs:
            return
        raise TypeError("Unexpected keyword argument")

    def _init_position(self, pos, anchor, **kwargs):
        if anchor is None:
            anchor = ("center", "center")
        self.anchor = anchor

        symbolic_pos_args = {
            k: kwargs[k] for k in kwargs if k in SYMBOLIC_POSITIONS}

        if not pos and not symbolic_pos_args:
            # No positional information given, use sensible top-left default
            self.topleft = (0, 0)
        elif pos and symbolic_pos_args:
            raise TypeError(
                "'pos' argument cannot be mixed with 'topleft', "
                "'topright' etc. argument."
            )
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

    def _set_symbolic_pos(self, symbolic_pos_dict):
        if len(symbolic_pos_dict) == 0:
            raise TypeError(
                "No position-setting keyword arguments ('topleft', "
                "'topright' etc) found."
            )
        if len(symbolic_pos_dict) > 1:
            raise TypeError(
                "Only one 'topleft', 'topright' etc. argument is allowed."
            )

        setter_name, position = symbolic_pos_dict.popitem() if not PLATFORM else symbolic_pos_dict.items().pop()
        setattr(self, setter_name, position)

    def _update_transform(self, function):
        if function in self.function_order:
            i = self.function_order.index(function)
            del self._surface_cache[i:]
        else:
            raise IndexError(
                "function {!r} does not have a registered order."
                "".format(function))

    @property
    def anchor(self):
        return self._anchor_value

    @anchor.setter
    def anchor(self, val):
        self._anchor_value = val
        self._calc_anchor()

    def _calc_anchor(self):
        ax, ay = self._anchor_value
        ow, oh = list(map(int, self._orig_surf.get_size())) #По каким то причинам идет возврат str а не int
        ax = calculate_anchor(ax, 'x', ow)
        ay = calculate_anchor(ay, 'y', oh)
        self._untransformed_anchor = ax, ay
        if self._angle == 0.0:
            self._anchor = self._untransformed_anchor
        else:
            self._anchor = transform_anchor(ax, ay, ow, oh, self._angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        w, h = list(map(int, self._orig_surf.get_size()))#По каким то причинам идет возврат str а не int

        ra = radians(angle)
        sin_a = sin(ra)
        cos_a = cos(ra)
        self.height = abs(w * sin_a) + abs(h * cos_a)
        self.width = abs(w * cos_a) + abs(h * sin_a)
        ax, ay = self._untransformed_anchor
        p = self.pos
        self._anchor = transform_anchor(ax, ay, w, h, angle)
        self.pos = p
        self._update_transform(_set_angle)

    @property
    def opacity(self):
        """Get/set the current opacity value.
        The allowable range for opacity is any number between and including
        0.0 and 1.0. Values outside of this will be clamped to the range.
        * 0.0 makes the image completely transparent (i.e. invisible).
        * 1.0 makes the image completely opaque (i.e. fully viewable).
        Values between 0.0 and 1.0 will give varying levels of transparency.
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        # Clamp the opacity to the allowable range.
        self._opacity = min(1.0, max(0.0, opacity))
        self._update_transform(_set_opacity)

    @property
    def pos(self):
        px, py = self.topleft
        ax, ay = self._anchor
        return px + ax, py + ay

    @pos.setter
    def pos(self, pos):
        px, py = pos
        ax, ay = self._anchor
        self.topleft = px - ax, py - ay

    @property
    def x(self):
        ax = self._anchor[0]
        return self.left + ax

    @x.setter
    def x(self, px):
        self.left = px - self._anchor[0]

    @property
    def y(self):
        ay = self._anchor[1]
        return self.top + ay

    @y.setter
    def y(self, py):
        self.top = py - self._anchor[1]

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        self._orig_surf = images.load(image)
        del self._surface_cache[:]  # Clear out old image's cache.
        self._update_pos()

    def _update_pos(self):
        p = self.pos
        self.width, self.height = list(map(int, self._orig_surf.get_size()))
        self._calc_anchor()
        self.pos = p

    def draw(self):
        s = self._build_transformed_surf()
        screen.blit(s, self.topleft)

    def angle_to(self, target):
        """Return the angle from this actors position to target, in degrees."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = myy - ty   # y axis is inverted from mathematical y in Pygame
        return degrees(atan2(dy, dx))

    def distance_to(self, target):
        """Return the distance from this actor's pos to target, in pixels."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = ty - myy
        return sqrt(dx * dx + dy * dy)

    def unload_image(self):
        images.unload(self._image_name)

# ============================================================= ANIMATION ==============================================================

def linear(n):
    return n


def accelerate(n):
    return n * n


def decelerate(n):
    return -1.0 * n * (n - 2.0)


def accel_decel(n):
    p = n * 2
    if p < 1:
        return 0.5 * p * p
    p -= 1.0
    return -0.5 * (p * (p - 2.0) - 1.0)


def in_elastic(n):
    p = .3
    s = p / 4.0
    q = n
    if q == 1:
        return 1.0
    q -= 1.0
    return -(pow(2, 10 * q) * sin((q - s) * (2 * pi) / p))


def out_elastic(n):
    p = .3
    s = p / 4.0
    q = n
    if q == 1:
        return 1.0
    return pow(2, -10 * q) * sin((q - s) * (2 * pi) / p) + 1.0


def in_out_elastic(n):
    p = .3 * 1.5
    s = p / 4.0
    q = n * 2
    if q == 2:
        return 1.0
    if q < 1:
        q -= 1.0
        return -.5 * (pow(2, 10 * q) * sin((q - s) * (2.0 * pi) / p))
    else:
        q -= 1.0
        return pow(2, -10 * q) * sin((q - s) * (2.0 * pi) / p) * .5 + 1.0


def _out_bounce_internal(t, d):
    p = t / d
    if p < (1.0 / 2.75):
        return 7.5625 * p * p
    elif p < (2.0 / 2.75):
        p -= (1.5 / 2.75)
        return 7.5625 * p * p + .75
    elif p < (2.5 / 2.75):
        p -= (2.25 / 2.75)
        return 7.5625 * p * p + .9375
    else:
        p -= (2.625 / 2.75)
        return 7.5625 * p * p + .984375


def _in_bounce_internal(t, d):
    return 1.0 - _out_bounce_internal(d - t, d)


def bounce_end(n):
    return _out_bounce_internal(n, 1.)


def bounce_start(n):
    return _in_bounce_internal(n, 1.)


def bounce_start_end(n):
    p = n * 2.
    if p < 1.:
        return _in_bounce_internal(p, 1.) * .5
    return _out_bounce_internal(p - 1., 1.) * .5 + .5


def tween(n, start, end):
    return start + (end - start) * n


def tween_attr(n, start, end):
    if isinstance(start, tuple):
        return tuple(tween(n, a, b) for a, b in zip(start, end))
    elif isinstance(start, list):
        return [tween(n, a, b) for a, b in zip(start, end)]
    else:
        return tween(n, start, end)


TWEEN_FUNCTIONS = {
    'linear': linear,
    'accelerate': accelerate,
    'decelerate': decelerate,
    'accel_decel': accel_decel,
    'in_elastic': in_elastic,
    'out_elastic':out_elastic,
    'in_out_elastic': in_out_elastic,
    'bounce_end': bounce_end,
    'bounce_start': bounce_start,
    'bounce_start_end': bounce_start_end
}

class Animation:
    """An animation manager for object attribute animations.
    Each keyword argument given to the Animation on creation (except
    "type" and "duration") will be *tweened* from their current value
    on the object to the target value specified.
    If the value is a list or tuple, then each value inside that will
    be tweened.
    The update() method is automatically scheduled with the clock for
    the duration of the animation.
    """
    animations = []  # Stores strong references to objects being animated.

    # Animations are stored in _animation_dict under (object id, target
    # attribute) keys. Objects may not be hashable, so the id, rather than
    # the object itself, is needed.
    # Animations with multiple targets will appear here multiple times.
    # Newly scheduled animations will overwrite new ones. Once an animation
    # ends, it is removed from this dict.
    # Note that Animation keeps a reference to "its" object, so the id in the
    # key will be valid as long as the animation lives.
    _animation_dict = {}

    def __init__(self, object, tween='linear', duration=1, on_finished=None,
                 **targets):
        self.targets = targets
        try:
            self.function = TWEEN_FUNCTIONS[tween]
        except KeyError:
                raise KeyError('No tween called %s found.' % tween)
        self.duration = duration
        self.on_finished = on_finished
        self.t = 0
        self.object = object
        self.initial = {}
        self._running = True
        for k in self.targets:
            try:
                a = getattr(object, k)
            except AttributeError:
                raise ValueError(
                    'object %r has no attribute %s to animate' % (object, k)
                )
            self.initial[k] = a
            key = id(object), k
            previous_animation = self._animation_dict.get(key)
            if previous_animation is not None:
                previous_animation._remove_target(k)
            self._animation_dict[key] = self
        each_tick(self.update)
        self.animations.append(self)

    @property
    def running(self):
        """Running state of the animation.
        True if the animation is running.
        False if the duration has elapsed or the stop() method was called.
        """
        return self._running

    def update(self, dt):
        self.t += dt
        n = self.t / self.duration
        if n > 1:
            n = 1
            self.stop(complete=True)
            if self.on_finished is not None:
                self.on_finished()
            return
        n = self.function(n)
        for k in self.targets:
            v = tween_attr(n, self.initial[k], self.targets[k])
            setattr(self.object, k, v)

    def stop(self, complete=False):
        """Stop the animation, optionally completing the transition to the final
        property values.
        :param complete: If True, the object will have its targets
            set to their final values for the animation. If not, the
            targets will be set to some value between the start and
            end values.
        """
        if not self._running:
            # Don't do anything if already stopped.
            return

        self._running = False
        if complete:
            for k in self.targets:
                setattr(self.object, k, self.targets[k])
        for k in list(self.targets):
            self._remove_target(k, stop=False)
        unschedule(self.update)
        self.animations.remove(self)

    def _remove_target(self, target, stop=True):
        del self.targets[target]
        del self._animation_dict[id(self.object), target]
        if not self.targets and stop:
            self.stop()


def animate(object, tween='linear', duration=1, on_finished=None, **targets):
    return Animation(object, tween, duration, on_finished=on_finished,
                     **targets)


# ====================================================== GENERICS =============================================================

def exit(e):
    if e.type == pygame.QUIT:
        pygame.quit()


def draw():
    pass


def update(dt):
    pass


def on_mouse_down(button, pos):
    pass


def on_mouse_up(button, pos):
    pass


def on_mouse_move():
    pass


def on_key_down(key):
    pass


def on_key_up(key):
    pass


def init():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    screen = Screen(screen)
    clock = pygame.time.Clock()
    return screen, clock


TITLE = 'UNTITLED'
screen, clock_pg = init()
clock = Clock()
tick = clock.tick
schedule = clock.schedule
schedule_interval = clock.schedule_interval
schedule_unique = clock.schedule_unique
unschedule = clock.unschedule
each_tick = clock.each_tick
# ========================================= TESTING AREA ===================================================================
import random, math

"""
Pi Lander
 * A basic Lunar Lander style game in Pygame Zero
 * Run with 'pgzrun pi_lander.py', control with the LEFT, RIGHT and UP arrow keys
 * Author Tim Martin: www.Tim-Martin.co.uk
 * Licence: Creative Commons Attribution-ShareAlike 4.0 International
 * http://creativecommons.org/licenses/by-sa/4.0/
"""

WIDTH = 800 # Screen width
HEIGHT = 600 # Screen height

class LandingSpotClass:
    """ Each instance defines a landing spot by where it starts, how big it is and how many points it's worth """
    landing_spot_sizes = ["small", "medium", "large"]
    def __init__(self, starting_step):
        self.starting = starting_step
        random_size = random.choice(LandingSpotClass.landing_spot_sizes) # And randomly choose size
        if random_size == "small":
            self.size = 4
            self.bonus = 8
        elif random_size == "medium":
            self.size = 10
            self.bonus = 4
        else: # Large
            self.size = 20
            self.bonus = 2
    def get_within_landing_spot(self, step):
        if (step >= self.starting) and (step < self.starting + self.size):
            return True
        return False

class LandscapeClass:
    """ Stores and generates the landscape, landing spots and star field """
    step_size = 3 # Landscape is broken down into steps. Define number of pixels on the x axis per step.
    world_steps = int(WIDTH/step_size) # How many steps can we fit horizontally on the screen
    small_height_change = 3 # Controls how bumpy the landscape is
    large_height_change = 10 # Controls how steep the landscape is
    features = ["mountain","valley","field"] # What features to generate
    n_stars = 30 # How many stars to put in the background
    n_spots = 4 # Max number of landing spots to generate
    def __init__(self):
        self.world_height = [] # Holds the height of the landscape at each step
        self.star_locations = [] # Holds the x and y location of the stars
        self.landing_spots = [] # Holds the landing spots
    def get_within_landing_spot(self, step):
        """ Calculate if a given step is within any of the landing spots """
        for spot in self.landing_spots:
            if spot.get_within_landing_spot(step) == True:
                return True
        return False
    def get_landing_spot_bonus(self, step):
        for spot in self.landing_spots:
            if spot.get_within_landing_spot(step) == True:
                return spot.bonus
        return 0
    def reset(self):
        """ Generates a new landscape """
        # First: Choose which steps of the landscape will be landing spots
        del self.landing_spots[:] # Delete any previous LandingSpotClass objects
        next_spot_start = 0
        # Move from left to right adding new landing spots until either
        # n_spots spots have been placed or we run out of space in the world
        while len(self.landing_spots) < LandscapeClass.n_spots and next_spot_start < LandscapeClass.world_steps:
            next_spot_start += random.randint(10, 50) # Randomly choose location to start landing spot
            new_landing_spot = LandingSpotClass(next_spot_start) # Make a new landing object at this spot
            self.landing_spots.append( new_landing_spot ) # And store it in our list
            next_spot_start += new_landing_spot.size # Then take into account its size before choosing the next
        # Second: Randomise the world map
        del self.world_height[:] # Clear any previous world height data
        feature_steps = 0 # Keep track of how many steps we are into a feature
        self.world_height.append(random.randint(300, 500)) # Start the landscape between 300 and 500 pixels down
        for step in range(1, LandscapeClass.world_steps):
            # If feature_step is zero, we need to choose a new feature and how long it goes on for
            if feature_steps == 0:
                feature_steps = random.randint(25, 75)
                current_feature = random.choice(LandscapeClass.features)
            # Generate the world by setting the range of random numbers, must be flat if in a landing spot
            if self.get_within_landing_spot(step) == True:
                max_up = 0 # Flat
                max_down = 0 # Flat
            elif current_feature == "mountain":
                max_up = LandscapeClass.small_height_change
                max_down = -LandscapeClass.large_height_change
            elif current_feature == "valley":
                max_up = LandscapeClass.large_height_change
                max_down = -LandscapeClass.small_height_change
            elif current_feature == "field":
                max_up = LandscapeClass.small_height_change
                max_down = -LandscapeClass.small_height_change
            # Generate the next piece of the landscape
            current_height = self.world_height[step-1]
            next_height = current_height + random.randint(max_down, max_up)
            self.world_height.append(next_height)
            feature_steps -= 1
            # Stop mountains getting too high, or valleys too low
            if next_height > 570:
                current_feature = "mountain" # Too low! Force a mountain
            elif next_height < 200:
                current_feature = "valley" # Too high! Force a valley
        # Third: Randomise the star field
        del self.star_locations[:]
        for star in range(0, LandscapeClass.n_stars):
            star_step = random.randint(0, LandscapeClass.world_steps-1)
            star_x = star_step * LandscapeClass.step_size
            star_y = random.randint( 0, self.world_height[star_step] ) # Keep the stars above the landscape
            self.star_locations.append( (star_x, star_y) )

class ShipClass:
    """ Holds the state of the player's ship and handles movement """
    max_fuel = 1000 # How much fuel the player starts with
    booster_power = 0.05 # Power of the ship's thrusters
    rotate_speed = 10 # How fast the ship rotates in degrees per frame
    gravity = [0., 0.01] # Strength of gravity in the x and y directions
    def __init__(self):
        """ Create the variables which will describe the players ship """
        self.angle = 0 # The angle the ship is facing 0 - 360 degrees
        self.altitude = 0 # The number of pixels the ship is above the ground
        self.booster = False # True if the player is firing their booster
        self.fuel = 0 # Amount of fuel remaining
        self.position = [0,0] # The x and y coordinates of the players ship
        self.velocity = [0,0] # The x and y velocity of the players ship
        self.acceleration = [0,0] # The x and y acceleration of the players ship
    def reset(self):
        """ Set the ships position, velocity and angle to their new-game values """
        self.position = [750., 100.] # Always start at the same spot
        self.velocity = [ -random.random(), random.random() ] # But with some initial speed
        self.acceleration = [0., 0.] # No initial acceleration (except gravity of course)
        self.angle = random.randint(0, 360) # And pointing in a random direction
        self.fuel = ShipClass.max_fuel # Fill up fuel tanks
    def rotate(self, direction):
        """ Rotate the players ship and keep the angle within the range 0 - 360 degrees """
        if direction == "left":
            self.angle -= ShipClass.rotate_speed
        elif direction == "right":
            self.angle += ShipClass.rotate_speed
        if self.angle > 360: # Remember than adding or subtracting 360 degrees does not change the angle
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
    def booster_on(self):
        """ When booster is firing we accelerate in the opposite direction, 180 degrees, from the way the ship is facing """
        self.booster = True
        self.acceleration[0] = ShipClass.booster_power * math.sin( math.radians(self.angle + 180) )
        self.acceleration[1] = ShipClass.booster_power * math.cos( math.radians(self.angle + 180) )
        self.fuel -= 2
    def booster_off(self):
        """ When the booster is not firing we do not accelerate """
        self.booster = False
        self.acceleration[0] = 0.
        self.acceleration[1] = 0.
    def update_physics(self):
        """ Update ship physics in X and Y, apply acceleration (and gravity) to the velocity and velocity to the position """
        for axis in range(0,2):
            self.velocity[axis] += ShipClass.gravity[axis]
            self.velocity[axis] += self.acceleration[axis]
            self.position[axis] += self.velocity[axis]
        # Update player altitude. Note that (LanscapeClass.step_size * 3) is the length of the ship's legs
        ship_step = int(self.position[0]/LandscapeClass.step_size)
        if ship_step < LandscapeClass.world_steps:
            self.altitude = game.landscape.world_height[ship_step] - self.position[1] - (LandscapeClass.step_size * 3)
    def get_out_of_bounds(self):
        """ Check if the player has hit the ground or gone off the sides """
        if self.altitude <= 0 or self.position[0] <= 0 or self.position[0] >= WIDTH:
            return True
        return False

class GameClass:
    """ Holds main game data, including the ship and landscape objects. Checks for game-over """
    def __init__(self):
        self.time = 0. # Time spent playing in seconds
        self.score = 0 # Player's score
        self.game_speed = 30 # How fast the game should run in frames per second
        self.time_elapsed = 0. # Time since the last frame was changed
        self.blink = True # True if blinking text is to be shown
        self.n_frames = 0 # Number of frames processed
        self.game_on = False # True if the game is being played
        self.game_message = "PI   LANDER\nPRESS SPACE TO START" # Start of game message
        self.ship = ShipClass() # Make a object of the ShipClass type
        self.landscape = LandscapeClass()
        self.reset() # Start the game with a fresh landscape and ship
    def reset(self):
        self.time = 0.
        self.ship.reset()
        self.landscape.reset()
    def check_game_over(self):
        """ Check if the game is over and update the game state if so """
        if self.ship.get_out_of_bounds() == False:
            return # Game is not over
        self.game_on = False # Game has finished. But did we win or loose?
        # Check if the player looses. This is if the ship's angle is > 20 degrees
        # the ship is not over a landing site, is moving too fast or is off the side of the screen
        ship_step = int(self.ship.position[0]/LandscapeClass.step_size)
        if self.ship.position[0] <= 0 \
           or self.ship.position[0] >= WIDTH \
           or self.landscape.get_within_landing_spot(ship_step) == False \
           or abs(self.ship.velocity[0]) > .5 \
           or abs(self.ship.velocity[1]) > .5 \
           or (self.ship.angle > 20 and self.ship.angle < 340):
            self.game_message = "YOU JUST DESTROYED A 100 MEGABUCK LANDER\n\nLOOSE 250 POINTS\n\nPRESS SPACE TO RESTART"
            self.score -= 250
        else: # If the player has won! Update their score based on the amount of remaining fuel and the landing bonus
            points = self.ship.fuel / 10
            points *= self.landscape.get_landing_spot_bonus(ship_step)
            self.score += points
            self.game_message = "CONGRATULATIONS\nTHAT WAS A GREAT LANDING!\n\n" + str(round(points)) + " POINTS\n\nPRESS SPACE TO RESTART"

# Create the game object
game = GameClass()

def draw():
    """
    Draw the game window on the screen in the following order:
    start message, mountain range, bonus points, stars, statistics, player's ship
    """
    screen.fill("black")
    size = LandscapeClass.step_size

    if game.game_on == False:
        screen.draw.text(game.game_message, center=(WIDTH/2, HEIGHT/5), align="center")

    # Get the x and y coordinates of each step of the landscape and draw it as a straight line
    for step in range(0, game.landscape.world_steps - 1):
        x_start = size * step
        x_end   = size * (step + 1)
        y_start = game.landscape.world_height[step]
        y_end   = game.landscape.world_height[step + 1]
        screen.draw.line( (x_start, y_start), (x_end, y_end), "white" )
        # Every second we flash the landing spots with a thicker line by drawing a narrow rectangle
        if (game.blink == True or game.game_on == False) and game.landscape.get_within_landing_spot(step) == True:
            screen.draw.filled_rect( Rect(x_start-size, y_start-1, size, 3), "white" )

    # Draw the bonus point notifier
    if game.blink == True or game.game_on == False:
        for spot in game.landscape.landing_spots:
            x_text = spot.starting * size
            y_text = game.landscape.world_height[ spot.starting ] + 10 # The extra 10 pixels puts the text below the landscape
            screen.draw.text(str(spot.bonus) + "x", (x_text,y_text), color="white")

    # Draw the stars
    for star in game.landscape.star_locations:
        screen.draw.line( star, star, "white" )

    # Draw the stats
    screen.draw.text("SCORE: " + str(round(game.score)), (10,10), fontsize=14, color="white", background="black")
    screen.draw.text("TIME: " + str(round(game.time)), (10,25), fontsize=14, color="white", background="black")
    screen.draw.text("FUEL: " + str(game.ship.fuel), (10,40), fontsize=14, color="white", background="black")
    screen.draw.text("ALTITUDE: " + str(round(game.ship.altitude)), (WIDTH-230,10), fontsize=14, color="white", background="black")
    screen.draw.text("HORIZONTAL SPEED: {0:.2f}".format(game.ship.velocity[0]), (WIDTH-230,25), fontsize=14, color="white", background="black")
    screen.draw.text("VERTICAL SPEED: {0:.2f}".format(-game.ship.velocity[1]), (WIDTH-230,40), fontsize=14, color="white", background="black")

    screen.draw.circle( game.ship.position, size*2, "yellow" ) # Draw the player
    # Use sin and cosine functions to draw the ship legs and booster at the correct angle
    # Requires the values in radians (0 to 2*pi) rather than in degrees (0 to 360)
    sin_angle = math.sin( math.radians(game.ship.angle - 45) ) # Legs are drawn 45 degrees either side of the ship's angle
    cos_angle = math.cos( math.radians(game.ship.angle - 45) )
    screen.draw.line( game.ship.position, (game.ship.position[0] + (sin_angle*size*3), game.ship.position[1] + (cos_angle*size*3)), "yellow" )
    sin_angle = math.sin( math.radians(game.ship.angle + 45) )
    cos_angle = math.cos( math.radians(game.ship.angle + 45) )
    screen.draw.line( game.ship.position, (game.ship.position[0] + (sin_angle*size*3), game.ship.position[1] + (cos_angle*size*3)), "yellow" )
    if game.ship.booster == True:
        sin_angle = math.sin( math.radians(game.ship.angle) ) # Booster is drawn at the same angle as the ship, just under it
        cos_angle = math.cos( math.radians(game.ship.angle) )
        screen.draw.filled_circle( (game.ship.position[0] + (sin_angle*size*3), game.ship.position[1] + (cos_angle*size*3)), size, "orange" )

def update(detlatime):
    """ Updates the game physics 30 times every second  """
    game.time_elapsed += detlatime
    if game.time_elapsed < 1./game.game_speed:
        return # A 30th of a second has not passed yet
    game.time_elapsed -= 1./game.game_speed

    # New frame - do all the simulations
    game.n_frames += 1
    if game.n_frames % game.game_speed == 0: # If n_frames is an exact multiple of the game FPS: so once per second
        game.blink = not game.blink # Invert blink so True becomes False or False becomes True

    # Start the game if the player presses space when the game is not on
    if keyboard.space and game.game_on == False:
        game.game_on = True
        game.reset()
    elif game.game_on == False:
        return

    # If the game is on, update the movement and the physics
    if keyboard.left: # Change space ship rotation
        game.ship.rotate("left")
    elif keyboard.right:
        game.ship.rotate("right")

    if keyboard.up and game.ship.fuel > 0: # Fire boosters if the player has enough fuel
        game.ship.booster_on()
    else:
        game.ship.booster_off()

    game.time += detlatime
    game.ship.update_physics()
    game.check_game_over()
# ========================================== MAIN LOOP ========================================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = Screen(screen)
pygame.display.set_caption(TITLE)


FPS = 30

while True:
    dt = pygame.time.get_ticks() / 1000 - clock.t
    clock.tick(dt)
    for event in pygame.event.get():
        exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Button press handler
            pos = pygame.mouse.get_pos()
            on_mouse_down(event.button, pos)
            on_mouse_up(event.button, pos)

        if event.type == pygame.KEYDOWN:
            keyboard._press(event.key)
            on_key_down(event.key)

        elif event.type == pygame.KEYUP:
            keyboard._release(event.key)
            on_key_up(event.key)

    update(dt)
    draw()
    pygame.display.update()
    clock_pg.tick(FPS)
