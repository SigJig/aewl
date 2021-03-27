
import enum
from ..utils import inheritors

class Gettable:
    @classmethod
    def get(cls, key):
        key = key.upper()

        try:
            return getattr(cls, key)
        except AttributeError:
            for child in inheritors(cls):
                st = getattr(child, key, None)

                if st is not None:
                    return st
            
            raise

class ControlTypes(Gettable):
    STATIC = 0
    BUTTON = 1
    EDIT = 2
    SLIDER = 3
    COMBO = 4
    LISTBOX = 5
    TOOLBOX = 6
    CHECKBOXES = 7
    PROGRESS = 8
    HTML = 9
    STATIC_SKEW = 10
    ACTIVETEXT = 11
    TREE = 12
    STRUCTURED_TEXT = 13
    CONTEXT_MENU = 14
    CONTROLS_GROUP = 15
    SHORTCUTBUTTON = 16
    HITZONES = 17
    VEHICLETOGGLES = 18
    CONTROLS_TABLE = 19
    XKEYDESC = 40
    XBUTTON = 41
    XLISTBOX = 42
    XSLIDER = 43
    XCOMBO = 44
    ANIMATED_TEXTURE = 45
    MENU = 46
    MENU_STRIP = 47
    CHECKBOX = 77
    OBJECT = 80
    OBJECT_ZOOM = 81
    OBJECT_CONTAINER = 82
    OBJECT_CONT_ANIM = 83
    LINEBREAK = 98
    USER = 99
    MAP = 100
    MAP_MAIN = 101
    LISTNBOX = 102
    ITEMSLOT = 103
    LISTNBOX_CHECKABLE = 104
    VEHICLE_DIRECTION = 105

class ControlStyles(Gettable):
    LEFT = 0x00
    RIGHT = 0x01
    CENTER = 0x02
    DOWN = 0x04
    UP = 0x08
    VCENTER = 0x0C
    SINGLE = 0x00
    MULTI = 0x10
    TITLE_BAR = 0x20
    PICTURE = 0x30
    FRAME = 0x40
    BACKGROUND = 0x50
    GROUP_BOX = 0x60
    GROUP_BOX2 = 0x70
    HUD_BACKGROUND = 0x80
    TILE_PICTURE = 0x90
    WITH_RECT = 0xA0
    LINE = 0xB0
    UPPERCASE = 0xC0
    LOWERCASE = 0xD0
    ADDITIONAL_INFO = 0x0F00
    SHADOW = 0x0100
    NO_RECT = 0x0200
    KEEP_ASPECT_RATIO = 0x0800
    TITLE = '0x20 + 0x02'
    VERTICAL = 0x01
    HORIZONTAL = 0

class SLControlStyles(ControlStyles):
    VERT = 0
    HORZ = 0x400
    TEXTURES = 0x10

class LBControlStyles(ControlStyles):
    TEXTURES = 0x10
    MULTI = 0x20

class TRControlStyles(ControlStyles):
    SHOWROOT = 1
    AUTOCOLLAPSE = 2
