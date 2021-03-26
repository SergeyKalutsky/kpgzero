
from types import MethodType
import re
import pygame
import time
from math import radians, sin, cos, atan2, degrees, sqrt, ceil

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
            import os
            print(path)
            try:
                res = pygame.image.load(path).convert_alpha()
                print(res)
                break
            except:
                pass

        if res is not None:
            return res
        else:
            raise ValueError('Image ' + name + ' not found')


images = ImageLoader()


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


RECT_CLASSES = (pygame.rect.Rect, ZRect)

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
        else:
            return object.__getattribute__(self, attr)

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

        setter_name, position = symbolic_pos_dict.popitem()
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
        ow, oh = self._orig_surf.get_size()
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
        w, h = self._orig_surf.get_size()

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
        self._surface_cache.clear()  # Clear out old image's cache.
        self._update_pos()

    def _update_pos(self):
        p = self.pos
        self.width, self.height = self._orig_surf.get_size()
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


def exit(e):
    if e.type == pygame.QUIT:
        pygame.quit()


def draw():
    pass


def update(dt):
    pass


def on_mouse_down(button, pos):
    pass


def init():
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    screen = Screen(screen)
    pygame.display.set_caption('TITLE')
    clock = pygame.time.Clock()
    return screen, clock


screen, clock_pg = init()

# ========================================= TESTING AREA ==============================================================
alien = Actor('alien1')

TITLE = "Alien walk"
WIDTH = 500
HEIGHT = alien.height + 20


# The initial position of the alien
alien.topright = 0, 10


def draw():
    """Clear the screen and draw the alien."""
    screen.clear()
    alien.draw()


def update():
    """Move the alien by one pixel."""
    alien.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien.left > WIDTH:
        alien.right = 0

# ========================================== MAIN LOOP ==================================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = Screen(screen)
pygame.display.set_caption(TITLE)

GRAY = (200, 200, 200)
FPS = 60
while True:
    # dt = 1
    for e in pygame.event.get():
        exit(e)
        if e.type == pygame.MOUSEBUTTONDOWN:
            # Button press handler
            pos = pygame.mouse.get_pos()
            on_mouse_down(e.button, pos)

    update()
    draw()
    pygame.display.update()
    clock_pg.tick(FPS)
