// output from tools/make_base.py

class aewl_basics {
    colorBackground[] = {
        0,
        0,
        0,
        0
    };
    colorText[] = {
        1,
        1,
        1,
        1
    };
    colorShadow[] = {
        0,
        0,
        0,
        0.5
    };
    tooltipColorText[] = {
        1,
        1,
        1,
        1
    };
    tooltipColorBox[] = {
        1,
        1,
        1,
        1
    };
    tooltipColorShade[] = {
        0,
        0,
        0,
        0.65
    };
    shadow = 0;
    text = "";
    fixedWidth = 0;
    font = "RobotoCondensed";
    linespacing = 1;
    deletable = 0;
    fade = 0;
    access = 0;
    x = 0;
    y = 0;
    w = 0.3;
    h = 0.3;
    idc = -1;
    default = 0;
    blinkingPeriod = 0;
    moving = 0;
};
class aewl_text2 : aewl_basics {
    type = 0;
    style = "0x00 + 				0x10";
    sizeEx = "GUI_GRID_CENTER_H";
    autoplay = 0;
    loops = 0;
    tileW = 1;
    tileH = 1;
    onCanDestroy = "";
    onDestroy = "";
    onMouseEnter = "";
    onMouseExit = "";
    onSetFocus = "";
    onKillFocus = "";
    onKeyDown = "";
    onKeyUp = "";
    onMouseButtonDown = "";
    onMouseButtonUp = "";
    onMouseButtonClick = "";
    onMouseButtonDblClick = "";
    onMouseZChanged = "";
    onMouseMoving = "";
    onMouseHolding = "";
    onVideoStopped = "";
};
class aewl_text : aewl_basics {
    type = 0;
    style = "0x00 + 				0x10";
    SizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
};
class structuredtextattr {
    color = "#ffffff";
    colorLink = "#D09B43";
    align = "left";
};
class aewl_structuredtext : aewl_basics {
    type = 13;
    style = 0;
    class Attributes : structuredtextattr {
        
    };
    size = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
};
class aewl_picture : aewl_basics {
    type = 0;
    style = 48;
    sizeEx = 0;
};
class aewl_edit : aewl_basics {
    type = 2;
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorSelection[] = {
        "(profilenamespace getvariable ['GUI_BCG_RGB_R',0.13])",
        "(profilenamespace getvariable ['GUI_BCG_RGB_G',0.54])",
        "(profilenamespace getvariable ['GUI_BCG_RGB_B',0.21])",
        1
    };
    autocomplete = "";
    size = 0.2;
    style = "0x00 + 0x40";
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    canModify = 1;
};
class aewl_combo : aewl_basics {
    type = 4;
    colorSelect[] = {
        0,
        0,
        0,
        1
    };
    colorScrollbar[] = {
        1,
        0,
        0,
        1
    };
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorPicture[] = {
        1,
        1,
        1,
        1
    };
    colorPictureSelected[] = {
        1,
        1,
        1,
        1
    };
    colorPictureDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorPictureRight[] = {
        1,
        1,
        1,
        1
    };
    colorPictureRightSelected[] = {
        1,
        1,
        1,
        1
    };
    colorPictureRightDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorTextRight[] = {
        1,
        1,
        1,
        1
    };
    colorSelectRight[] = {
        0,
        0,
        0,
        1
    };
    colorSelect2Right[] = {
        0,
        0,
        0,
        1
    };
    soundSelect[] = {
        "\A3\ui_f\data\sound\RscCombo\soundSelect",
        0.1,
        1
    };
    soundExpand[] = {
        "\A3\ui_f\data\sound\RscCombo\soundExpand",
        0.1,
        1
    };
    soundCollapse[] = {
        "\A3\ui_f\data\sound\RscCombo\soundCollapse",
        0.1,
        1
    };
    maxHistoryDelay = 1;
    class ComboScrollBar {
        color[] = {
            1,
            1,
            1,
            1
        };
    };
    colorSelectBackground[] = {
        1,
        1,
        1,
        0.7
    };
    colorActive[] = {
        1,
        0,
        0,
        1
    };
    style = "0x10 + 0x200";
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    arrowEmpty = "\A3\ui_f\data\GUI\RscCommon\rsccombo\arrow_combo_ca.paa";
    arrowFull = "\A3\ui_f\data\GUI\RscCommon\rsccombo\arrow_combo_active_ca.paa";
    wholeHeight = 0.45;
};
class aewl_listbox : aewl_basics {
    type = 5;
    rowHeight = 0;
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorScrollbar[] = {
        1,
        0,
        0,
        0
    };
    colorSelect[] = {
        0,
        0,
        0,
        1
    };
    colorSelect2[] = {
        0,
        0,
        0,
        1
    };
    colorSelectBackground[] = {
        0.95,
        0.95,
        0.95,
        1
    };
    colorSelectBackground2[] = {
        1,
        1,
        1,
        0.5
    };
    soundSelect[] = {
        "\A3\ui_f\data\sound\RscListbox\soundSelect",
        0.09,
        1
    };
    autoScrollSpeed = -1;
    autoScrollDelay = 5;
    autoScrollRewind = 0;
    arrowEmpty = "#(argb,8,8,3)color(1,1,1,1)";
    arrowFull = "#(argb,8,8,3)color(1,1,1,1)";
    colorPicture[] = {
        1,
        1,
        1,
        1
    };
    colorPictureSelected[] = {
        1,
        1,
        1,
        1
    };
    colorPictureDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorPictureRight[] = {
        1,
        1,
        1,
        1
    };
    colorPictureRightSelected[] = {
        1,
        1,
        1,
        1
    };
    colorPictureRightDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorTextRight[] = {
        1,
        1,
        1,
        1
    };
    colorSelectRight[] = {
        0,
        0,
        0,
        1
    };
    colorSelect2Right[] = {
        0,
        0,
        0,
        1
    };
    class ListScrollBar {
        color[] = {
            1,
            1,
            1,
            1
        };
        autoScrollEnabled = 1;
    };
    style = 16;
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    period = 1.2;
    maxHistoryDelay = 1;
};
class aewl_button : aewl_basics {
    type = 1;
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorBackgroundDisabled[] = {
        0,
        0,
        0,
        0.5
    };
    colorBackgroundActive[] = {
        0,
        0,
        0,
        1
    };
    colorFocused[] = {
        0,
        0,
        0,
        1
    };
    colorBorder[] = {
        0,
        0,
        0,
        1
    };
    soundEnter[] = {
        "\A3\ui_f\data\sound\RscButton\soundEnter",
        0.09,
        1
    };
    soundPush[] = {
        "\A3\ui_f\data\sound\RscButton\soundPush",
        0.09,
        1
    };
    soundClick[] = {
        "\A3\ui_f\data\sound\RscButton\soundClick",
        0.09,
        1
    };
    soundEscape[] = {
        "\A3\ui_f\data\sound\RscButton\soundEscape",
        0.09,
        1
    };
    style = 2;
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    url = "";
    offsetX = 0;
    offsetY = 0;
    offsetPressedX = 0;
    offsetPressedY = 0;
    borderSize = 0;
};
class aewl_shortcutbutton : aewl_basics {
    type = 16;
    class HitZone {
        left = 0;
        top = 0;
        right = 0;
        bottom = 0;
    };
    class ShortcutPos {
        left = 0;
        top = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 20) - (((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)) / 2";
        w = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1) * (3/4)";
        h = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    };
    class TextPos {
        left = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1) * (3/4)";
        top = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 20) - (((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)) / 2";
        right = 0.005;
        bottom = 0;
    };
    shortcuts[] = {};
    textureNoShortcut = "#(argb,8,8,3)color(0,0,0,0)";
    color[] = {
        1,
        1,
        1,
        1
    };
    colorFocused[] = {
        1,
        1,
        1,
        1
    };
    color2[] = {
        0.95,
        0.95,
        0.95,
        1
    };
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorBackgroundFocused[] = {
        "(profilenamespace getvariable ['GUI_BCG_RGB_R',0.13])",
        "(profilenamespace getvariable ['GUI_BCG_RGB_G',0.54])",
        "(profilenamespace getvariable ['GUI_BCG_RGB_B',0.21])",
        1
    };
    colorBackground2[] = {
        1,
        1,
        1,
        1
    };
    soundEnter[] = {
        "\A3\ui_f\data\sound\RscButton\soundEnter",
        0.09,
        1
    };
    soundPush[] = {
        "\A3\ui_f\data\sound\RscButton\soundPush",
        0.09,
        1
    };
    soundClick[] = {
        "\A3\ui_f\data\sound\RscButton\soundClick",
        0.09,
        1
    };
    soundEscape[] = {
        "\A3\ui_f\data\sound\RscButton\soundEscape",
        0.09,
        1
    };
    class Attributes {
        font = "RobotoCondensed";
        color = "#E5E5E5";
        align = "left";
        shadow = 1;
    };
    colorSecondary[] = {
        1,
        1,
        1,
        1
    };
    colorFocusedSecondary[] = {
        1,
        1,
        1,
        1
    };
    color2Secondary[] = {
        0.95,
        0.95,
        0.95,
        1
    };
    colorDisabledSecondary[] = {
        1,
        1,
        1,
        0.25
    };
    class AttributesImage {
        font = "RobotoCondensed";
        color = "#E5E5E5";
        align = "left";
    };
    style = 0;
    textSecondary = "";
    sizeExSecondary = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    fontSecondary = "RobotoCondensed";
    animTextureDefault = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButton\normal_ca.paa";
    animTextureNormal = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButton\normal_ca.paa";
    animTextureDisabled = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButton\normal_ca.paa";
    animTextureOver = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButton\over_ca.paa";
    animTextureFocused = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButton\focus_ca.paa";
    animTexturePressed = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButton\down_ca.paa";
    periodFocus = 1.2;
    periodOver = 0.8;
    period = 0.4;
    size = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    url = "";
    action = "";
};
class aewl_shortcutbuttonmain {
    color[] = {
        1,
        1,
        1,
        1
    };
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    class HitZone {
        left = 0;
        top = 0;
        right = 0;
        bottom = 0;
    };
    class ShortcutPos {
        left = 0.0145;
        top = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 20) - (((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1.2)) / 2";
        w = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1.2) * (3/4)";
        h = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1.2)";
    };
    class TextPos {
        left = "(((safezoneW / safezoneH) min 1.2) / 32) * 1.5";
        top = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 20)*2 - (((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1.2)) / 2";
        right = 0.005;
        bottom = 0;
    };
    class Attributes {
        font = "RobotoCondensed";
        color = "#E5E5E5";
        align = "left";
        shadow = 0;
    };
    class AttributesImage {
        font = "RobotoCondensed";
        color = "#E5E5E5";
        align = 0;
    };
    style = 0;
    animTextureNormal = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButtonMain\normal_ca.paa";
    animTextureDisabled = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButtonMain\disabled_ca.paa";
    animTextureOver = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButtonMain\over_ca.paa";
    animTextureFocused = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButtonMain\focus_ca.paa";
    animTexturePressed = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButtonMain\down_ca.paa";
    animTextureDefault = "\A3\ui_f\data\GUI\RscCommon\RscShortcutButtonMain\normal_ca.paa";
    period = 0.5;
    size = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1.2)";
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1.2)";
    action = "";
};
class aewl_frame : aewl_basics {
    type = 0;
    style = 64;
    sizeEx = 0.02;
};
class aewl_slider : aewl_basics {
    type = 3;
    style = 1024;
    color[] = {
        1,
        1,
        1,
        0.8
    };
    colorActive[] = {
        1,
        1,
        1,
        1
    };
};
class iguiback : aewl_basics {
    type = 0;
    style = 128;
    sizeEx = 0;
};
class aewl_checkbox : aewl_basics {
    color[] = {
        1,
        1,
        1,
        0.7
    };
    colorFocused[] = {
        1,
        1,
        1,
        1
    };
    colorHover[] = {
        1,
        1,
        1,
        1
    };
    colorPressed[] = {
        1,
        1,
        1,
        1
    };
    colorDisabled[] = {
        1,
        1,
        1,
        0.2
    };
    colorBackgroundFocused[] = {
        0,
        0,
        0,
        0
    };
    colorBackgroundHover[] = {
        0,
        0,
        0,
        0
    };
    colorBackgroundPressed[] = {
        0,
        0,
        0,
        0
    };
    colorBackgroundDisabled[] = {
        0,
        0,
        0,
        0
    };
    soundEnter[] = {
        0.1,
        1
    };
    soundPush[] = {
        0.1,
        1
    };
    soundClick[] = {
        0.1,
        1
    };
    soundEscape[] = {
        0.1,
        1
    };
    type = 77;
    style = 0;
    checked = 0;
    textureChecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_checked_ca.paa";
    textureUnchecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_unchecked_ca.paa";
    textureFocusedChecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_checked_ca.paa";
    textureFocusedUnchecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_unchecked_ca.paa";
    textureHoverChecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_checked_ca.paa";
    textureHoverUnchecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_unchecked_ca.paa";
    texturePressedChecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_checked_ca.paa";
    texturePressedUnchecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_unchecked_ca.paa";
    textureDisabledChecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_checked_ca.paa";
    textureDisabledUnchecked = "A3\Ui_f\data\GUI\RscCommon\RscCheckBox\CheckBox_unchecked_ca.paa";
};
class aewl_textcheckbox : aewl_basics {
    color[] = {
        0,
        0,
        0,
        0
    };
    colorTextSelect[] = {
        0,
        0.8,
        0,
        1
    };
    colorSelectedBg[] = {
        "(profilenamespace getvariable ['GUI_BCG_RGB_R',0.13])",
        "(profilenamespace getvariable ['GUI_BCG_RGB_G',0.54])",
        "(profilenamespace getvariable ['GUI_BCG_RGB_B',0.21])",
        1
    };
    colorSelect[] = {
        0,
        0,
        0,
        1
    };
    colorTextDisable[] = {
        0.4,
        0.4,
        0.4,
        1
    };
    colorDisable[] = {
        0.4,
        0.4,
        0.4,
        1
    };
    strings[] = {
        "UNCHECKED"
    };
    checked_strings[] = {
        "CHECKED"
    };
    type = 7;
    style = 0;
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 0.8)";
    rows = 1;
    columns = 1;
};
class aewl_buttonmenu : aewl_basics {
    colorBackgroundFocused[] = {
        1,
        1,
        1,
        1
    };
    colorBackground2[] = {
        0.75,
        0.75,
        0.75,
        1
    };
    color[] = {
        1,
        1,
        1,
        1
    };
    colorFocused[] = {
        0,
        0,
        0,
        1
    };
    color2[] = {
        0,
        0,
        0,
        1
    };
    colorDisabled[] = {
        1,
        1,
        1,
        0.25
    };
    colorSecondary[] = {
        1,
        1,
        1,
        1
    };
    colorFocusedSecondary[] = {
        0,
        0,
        0,
        1
    };
    color2Secondary[] = {
        0,
        0,
        0,
        1
    };
    colorDisabledSecondary[] = {
        1,
        1,
        1,
        0.25
    };
    class TextPos {
        left = "0.25 * (((safezoneW / safezoneH) min 1.2) / 40)";
        top = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) - (((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)) / 2";
        right = 0.005;
        bottom = 0;
    };
    class Attributes {
        font = "PuristaLight";
        color = "#E5E5E5";
        align = "left";
        shadow = 0;
    };
    class ShortcutPos {
        left = "5.25 * (((safezoneW / safezoneH) min 1.2) / 40)";
        top = 0;
        w = "1 * (((safezoneW / safezoneH) min 1.2) / 40)";
        h = "1 * ((((safezoneW / safezoneH) min 1.2) / 1.2) / 25)";
    };
    soundEnter[] = {
        "\A3\ui_f\data\sound\RscButtonMenu\soundEnter",
        0.09,
        1
    };
    soundPush[] = {
        "\A3\ui_f\data\sound\RscButtonMenu\soundPush",
        0.09,
        1
    };
    soundClick[] = {
        "\A3\ui_f\data\sound\RscButtonMenu\soundClick",
        0.09,
        1
    };
    soundEscape[] = {
        "\A3\ui_f\data\sound\RscButtonMenu\soundEscape",
        0.09,
        1
    };
    type = 16;
    style = "0x02 + 0xC0";
    animTextureNormal = "#(argb,8,8,3)color(1,1,1,1)";
    animTextureDisabled = "#(argb,8,8,3)color(1,1,1,1)";
    animTextureOver = "#(argb,8,8,3)color(1,1,1,1)";
    animTextureFocused = "#(argb,8,8,3)color(1,1,1,1)";
    animTexturePressed = "#(argb,8,8,3)color(1,1,1,1)";
    animTextureDefault = "#(argb,8,8,3)color(1,1,1,1)";
    textSecondary = "";
    sizeExSecondary = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    fontSecondary = "PuristaLight";
    period = 1.2;
    periodFocus = 1.2;
    periodOver = 1.2;
    size = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
    sizeEx = "(((((safezoneW / safezoneH) min 1.2) / 1.2) / 25) * 1)";
};
class aewl_buttonmenuok {
    shortcuts[] = {
        "0x00050000 + 0",
        28,
        57,
        156
    };
    soundPush[] = {
        "\A3\ui_f\data\sound\RscButtonMenuOK\soundPush",
        0.09,
        1
    };
};
class aewl_buttonmenucancel {
    shortcuts[] = {
        "0x00050000 + 1"
    };
};
class aewl_controlsgroup : aewl_basics {
    class VScrollbar {
        color[] = {
            1,
            1,
            1,
            1
        };
        width = 0.021;
        autoScrollEnabled = 1;
    };
    class HScrollbar {
        color[] = {
            1,
            1,
            1,
            1
        };
        height = 0.028;
    };
    class Controls {
        
    };
    type = 15;
    style = 16;
};
class aewl_controlsgroupnohscroll : aewl_controlsgroup {
    class HScrollbar {
        
    };
};
class aewl_controlsgroupnovscroll : aewl_controlsgroup {
    class VScrollbar {
        
    };
};
class aewl_controlsgroupnoscroll : aewl_controlsgroupnovscroll {
    class HScrollbar {
        
    };
};
class aewl_progress : aewl_basics {
    type = 8;
    style = "0x00";
    texture = "";
    colorFrame[] = {
        0,
        0,
        0,
        1
    };
    colorBar[] = {
        0,
        0,
        0,
        1
    };
};