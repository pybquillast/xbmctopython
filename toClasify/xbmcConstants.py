import sys

KEY_BUTTON_A                      = 256
KEY_BUTTON_B                      = 257
KEY_BUTTON_X                      = 258
KEY_BUTTON_Y                      = 259
KEY_BUTTON_BLACK                  = 260
KEY_BUTTON_WHITE                  = 261
KEY_BUTTON_LEFT_TRIGGER           = 262
KEY_BUTTON_RIGHT_TRIGGER          = 263

KEY_BUTTON_LEFT_THUMB_STICK       = 264
KEY_BUTTON_RIGHT_THUMB_STICK      = 265

KEY_BUTTON_RIGHT_THUMB_STICK_UP   = 266 # right thumb stick directions
KEY_BUTTON_RIGHT_THUMB_STICK_DOWN = 267 # for defining different actions per direction
KEY_BUTTON_RIGHT_THUMB_STICK_LEFT = 268
KEY_BUTTON_RIGHT_THUMB_STICK_RIGHT = 269

''' Digital - don't change order '''
KEY_BUTTON_DPAD_UP                = 270
KEY_BUTTON_DPAD_DOWN              = 271
KEY_BUTTON_DPAD_LEFT              = 272
KEY_BUTTON_DPAD_RIGHT             = 273

KEY_BUTTON_START                  = 274
KEY_BUTTON_BACK                   = 275

KEY_BUTTON_LEFT_THUMB_BUTTON      = 276
KEY_BUTTON_RIGHT_THUMB_BUTTON     = 277

KEY_BUTTON_LEFT_ANALOG_TRIGGER    = 278
KEY_BUTTON_RIGHT_ANALOG_TRIGGER   = 279

KEY_BUTTON_LEFT_THUMB_STICK_UP    = 280 # left thumb stick directions
KEY_BUTTON_LEFT_THUMB_STICK_DOWN  = 281 # for defining different actions per direction
KEY_BUTTON_LEFT_THUMB_STICK_LEFT  = 282
KEY_BUTTON_LEFT_THUMB_STICK_RIGHT = 283

# 0xF000 -> 0xF200 is reserved for the keyboard; a keyboard press is either
KEY_VKEY          = 0xF000 # a virtual key/functional key e.g. cursor left
KEY_ASCII         = 0xF100 # a printable character in the range of TRUE ASCII (from 0 to 127) # FIXME make it clean and pure unicode! remove the need for KEY_ASCII
KEY_UNICODE       = 0xF200 # another printable character whose range is not included in this KEY code

# 0xE000 -> 0xEFFF is reserved for mouse actions
KEY_VMOUSE        = 0xEFFF

KEY_MOUSE_START          = 0xE000
KEY_MOUSE_CLICK          = 0xE000
KEY_MOUSE_RIGHTCLICK     = 0xE001
KEY_MOUSE_MIDDLECLICK    = 0xE002
KEY_MOUSE_DOUBLE_CLICK   = 0xE010
KEY_MOUSE_LONG_CLICK     = 0xE020
KEY_MOUSE_WHEEL_UP       = 0xE101
KEY_MOUSE_WHEEL_DOWN     = 0xE102
KEY_MOUSE_MOVE           = 0xE103
KEY_MOUSE_DRAG           = 0xE104
KEY_MOUSE_DRAG_START     = 0xE105
KEY_MOUSE_DRAG_END       = 0xE106
KEY_MOUSE_RDRAG          = 0xE107
KEY_MOUSE_RDRAG_START    = 0xE108
KEY_MOUSE_RDRAG_END      = 0xE109
KEY_MOUSE_NOOP           = 0xEFFF
KEY_MOUSE_END            = 0xEFFF

# 0xD000 -> 0xD0FF is reserved for WM_APPCOMMAND messages
KEY_APPCOMMAND    = 0xD000

# 0xF000 -> 0xF0FF is reserved for mouse actions
KEY_TOUCH         = 0xF000

KEY_INVALID       = 0xFFFF

# actions that we have defined...
ACTION_NONE                  = 0
ACTION_MOVE_LEFT             = 1
ACTION_MOVE_RIGHT            = 2
ACTION_MOVE_UP               = 3
ACTION_MOVE_DOWN             = 4
ACTION_PAGE_UP               = 5
ACTION_PAGE_DOWN             = 6
ACTION_SELECT_ITEM           = 7
ACTION_HIGHLIGHT_ITEM        = 8
ACTION_PARENT_DIR            = 9
ACTION_PREVIOUS_MENU        = 10
ACTION_SHOW_INFO            = 11

ACTION_PAUSE                = 12
ACTION_STOP                 = 13
ACTION_NEXT_ITEM            = 14
ACTION_PREV_ITEM            = 15
ACTION_FORWARD              = 16 # Can be used to specify specific action in a window, Playback control is handled in ACTION_PLAYER_*
ACTION_REWIND               = 17 # Can be used to specify specific action in a window, Playback control is handled in ACTION_PLAYER_*

ACTION_SHOW_GUI             = 18 # toggle between GUI and movie or GUI and visualisation.
ACTION_ASPECT_RATIO         = 19 # toggle quick-access zoom modes. Can b used in videoFullScreen.zml window id=2005
ACTION_STEP_FORWARD         = 20 # seek +1% in the movie. Can b used in videoFullScreen.xml window id=2005
ACTION_STEP_BACK            = 21 # seek -1% in the movie. Can b used in videoFullScreen.xml window id=2005
ACTION_BIG_STEP_FORWARD     = 22 # seek +10% in the movie. Can b used in videoFullScreen.xml window id=2005
ACTION_BIG_STEP_BACK        = 23 # seek -10% in the movie. Can b used in videoFullScreen.xml window id=2005
ACTION_SHOW_OSD             = 24 # show/hide OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_SHOW_SUBTITLES       = 25 # turn subtitles on/off. Can b used in videoFullScreen.xml window id=2005
ACTION_NEXT_SUBTITLE        = 26 # switch to next subtitle of movie. Can b used in videoFullScreen.xml window id=2005
ACTION_SHOW_CODEC           = 27 # show information about file. Can b used in videoFullScreen.xml window id=2005 and in slideshow.xml window id=2007
ACTION_NEXT_PICTURE         = 28 # show next picture of slideshow. Can b used in slideshow.xml window id=2007
ACTION_PREV_PICTURE         = 29 # show previous picture of slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_OUT             = 30 # zoom in picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_IN              = 31 # zoom out picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_TOGGLE_SOURCE_DEST   = 32 # used to toggle between source view and destination view. Can be used in myfiles.xml window id=3
ACTION_SHOW_PLAYLIST        = 33 # used to toggle between current view and playlist view. Can b used in all mymusic xml files
ACTION_QUEUE_ITEM           = 34 # used to queue a item to the playlist. Can b used in all mymusic xml files
ACTION_REMOVE_ITEM          = 35 # not used anymore
ACTION_SHOW_FULLSCREEN      = 36 # not used anymore
ACTION_ZOOM_LEVEL_NORMAL    = 37 # zoom 1x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_1         = 38 # zoom 2x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_2         = 39 # zoom 3x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_3         = 40 # zoom 4x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_4         = 41 # zoom 5x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_5         = 42 # zoom 6x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_6         = 43 # zoom 7x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_7         = 44 # zoom 8x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_8         = 45 # zoom 9x picture during slideshow. Can b used in slideshow.xml window id=2007
ACTION_ZOOM_LEVEL_9         = 46 # zoom 10x picture during slideshow. Can b used in slideshow.xml window id=2007

ACTION_CALIBRATE_SWAP_ARROWS = 47 # select next arrow. Can b used in: settingsScreenCalibration.xml windowid=11
ACTION_CALIBRATE_RESET      = 48 # reset calibration to defaults. Can b used in: settingsScreenCalibration.xml windowid=11/settingsUICalibration.xml windowid=10
ACTION_ANALOG_MOVE          = 49 # analog thumbstick move. Can b used in: slideshow.xml window id=2007/settingsScreenCalibration.xml windowid=11/settingsUICalibration.xml windowid=10
# see also ACTION_ANALOG_MOVE_X, ACTION_ANALOG_MOVE_Y
ACTION_ROTATE_PICTURE_CW    = 50 # rotate current picture clockwise during slideshow. Can be used in slideshow.xml window id=2007
ACTION_ROTATE_PICTURE_CCW   = 51 # rotate current picture counterclockwise during slideshow. Can be used in slideshow.xml window id=2007

ACTION_SUBTITLE_DELAY_MIN   = 52 # Decrease subtitle/movie Delay.  Can b used in videoFullScreen.xml window id=2005
ACTION_SUBTITLE_DELAY_PLUS  = 53 # Increase subtitle/movie Delay.  Can b used in videoFullScreen.xml window id=2005
ACTION_AUDIO_DELAY_MIN      = 54 # Increase avsync delay.  Can b used in videoFullScreen.xml window id=2005
ACTION_AUDIO_DELAY_PLUS     = 55 # Decrease avsync delay.  Can b used in videoFullScreen.xml window id=2005
ACTION_AUDIO_NEXT_LANGUAGE  = 56 # Select next language in movie.  Can b used in videoFullScreen.xml window id=2005
ACTION_CHANGE_RESOLUTION    = 57 # switch 2 next resolution. Can b used during screen calibration settingsScreenCalibration.xml windowid=11

REMOTE_0                  = 58  # remote keys 0-9. are used by multiple windows
REMOTE_1                  = 59  # for example in videoFullScreen.xml window id=2005 you can
REMOTE_2                  = 60  # enter time (mmss) to jump to particular point in the movie
REMOTE_3                  = 61
REMOTE_4                  = 62  # with spincontrols you can enter 3digit number to quickly set
REMOTE_5                  = 63  # spincontrol to desired value
REMOTE_6                  = 64
REMOTE_7                  = 65
REMOTE_8                  = 66
REMOTE_9                  = 67

ACTION_PLAY               = 68  # Unused at the moment
ACTION_OSD_SHOW_LEFT      = 69  # Move left in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_OSD_SHOW_RIGHT     = 70  # Move right in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_OSD_SHOW_UP        = 71  # Move up in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_OSD_SHOW_DOWN      = 72  # Move down in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_OSD_SHOW_SELECT    = 73  # toggle/select option in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_OSD_SHOW_VALUE_PLUS = 74  # increase value of current option in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_OSD_SHOW_VALUE_MIN = 75  # decrease value of current option in OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_SMALL_STEP_BACK    = 76  # jumps a few seconds back during playback of movie. Can b used in videoFullScreen.xml window id=2005

ACTION_PLAYER_FORWARD      = 77  # FF in current file played. global action, can be used anywhere
ACTION_PLAYER_REWIND       = 78  # RW in current file played. global action, can be used anywhere
ACTION_PLAYER_PLAY         = 79  # Play current song. Unpauses song and sets playspeed to 1x. global action, can be used anywhere

ACTION_DELETE_ITEM        = 80  # delete current selected item. Can be used in myfiles.xml window id=3 and in myvideoTitle.xml window id=25
ACTION_COPY_ITEM          = 81  # copy current selected item. Can be used in myfiles.xml window id=3
ACTION_MOVE_ITEM          = 82  # move current selected item. Can be used in myfiles.xml window id=3
ACTION_SHOW_MPLAYER_OSD   = 83  # toggles mplayers OSD. Can be used in videofullscreen.xml window id=2005
ACTION_OSD_HIDESUBMENU    = 84  # removes an OSD sub menu. Can be used in videoOSD.xml window id=2901
ACTION_TAKE_SCREENSHOT    = 85  # take a screenshot
ACTION_RENAME_ITEM        = 87  # rename item

ACTION_VOLUME_UP          = 88
ACTION_VOLUME_DOWN        = 89
ACTION_VOLAMP             = 90
ACTION_MUTE               = 91
ACTION_NAV_BACK           = 92
ACTION_VOLAMP_UP          = 93
ACTION_VOLAMP_DOWN        = 94

ACTION_CREATE_EPISODE_BOOKMARK = 95 #Creates an episode bookmark on the currently playing video file containing more than one episode
ACTION_CREATE_BOOKMARK       = 96 #Creates a bookmark of the currently playing video file

ACTION_CHAPTER_OR_BIG_STEP_FORWARD     = 97 # Goto the next chapter, if not available perform a big step forward
ACTION_CHAPTER_OR_BIG_STEP_BACK        = 98 # Goto the previous chapter, if not available perform a big step back

ACTION_CYCLE_SUBTITLE       = 99 # switch to next subtitle of movie, but will not enable/disable the subtitles. Can be used in videoFullScreen.xml window id=2005

ACTION_MOUSE_START          = 100
ACTION_MOUSE_LEFT_CLICK     = 100
ACTION_MOUSE_RIGHT_CLICK    = 101
ACTION_MOUSE_MIDDLE_CLICK   = 102
ACTION_MOUSE_DOUBLE_CLICK   = 103
ACTION_MOUSE_WHEEL_UP       = 104
ACTION_MOUSE_WHEEL_DOWN     = 105
ACTION_MOUSE_DRAG           = 106
ACTION_MOUSE_MOVE           = 107
ACTION_MOUSE_LONG_CLICK     = 108
ACTION_MOUSE_END            = 109

ACTION_BACKSPACE        = 110
ACTION_SCROLL_UP        = 111
ACTION_SCROLL_DOWN      = 112
ACTION_ANALOG_FORWARD   = 113
ACTION_ANALOG_REWIND    = 114

ACTION_MOVE_ITEM_UP     = 115  # move item up in playlist
ACTION_MOVE_ITEM_DOWN   = 116  # move item down in playlist
ACTION_CONTEXT_MENU     = 117  # pops up the context menu


# stuff for virtual keyboard shortcuts
ACTION_SHIFT            = 118
ACTION_SYMBOLS          = 119
ACTION_CURSOR_LEFT      = 120
ACTION_CURSOR_RIGHT     = 121

ACTION_BUILT_IN_FUNCTION = 122

ACTION_SHOW_OSD_TIME    = 123 # displays current time, can be used in videoFullScreen.xml window id=2005
ACTION_ANALOG_SEEK_FORWARD = 124 # seeks forward, and displays the seek bar.
ACTION_ANALOG_SEEK_BACK   = 125 # seeks backward, and displays the seek bar.

ACTION_VIS_PRESET_SHOW      = 126
ACTION_VIS_PRESET_NEXT      = 128
ACTION_VIS_PRESET_PREV      = 129
ACTION_VIS_PRESET_LOCK      = 130
ACTION_VIS_PRESET_RANDOM    = 131
ACTION_VIS_RATE_PRESET_PLUS = 132
ACTION_VIS_RATE_PRESET_MINUS = 133

ACTION_SHOW_VIDEOMENU       = 134
ACTION_ENTER                = 135

ACTION_INCREASE_RATING      = 136
ACTION_DECREASE_RATING      = 137

ACTION_NEXT_SCENE           = 138 # switch to next scene/cutpoint in movie
ACTION_PREV_SCENE           = 139 # switch to previous scene/cutpoint in movie

ACTION_NEXT_LETTER          = 140 # jump through a list or container by letter
ACTION_PREV_LETTER          = 141

ACTION_JUMP_SMS2            = 142 # jump direct to a particular letter using SMS-style input
ACTION_JUMP_SMS3            = 143
ACTION_JUMP_SMS4            = 144
ACTION_JUMP_SMS5            = 145
ACTION_JUMP_SMS6            = 146
ACTION_JUMP_SMS7            = 147
ACTION_JUMP_SMS8            = 148
ACTION_JUMP_SMS9            = 149

ACTION_FILTER_CLEAR         = 150
ACTION_FILTER_SMS2          = 151
ACTION_FILTER_SMS3          = 152
ACTION_FILTER_SMS4          = 153
ACTION_FILTER_SMS5          = 154
ACTION_FILTER_SMS6          = 155
ACTION_FILTER_SMS7          = 156
ACTION_FILTER_SMS8          = 157
ACTION_FILTER_SMS9          = 158

ACTION_FIRST_PAGE           = 159
ACTION_LAST_PAGE            = 160

ACTION_AUDIO_DELAY          = 161
ACTION_SUBTITLE_DELAY       = 162
ACTION_MENU                 = 163
ACTION_SET_RATING           = 164
ACTION_RECORD               = 170

ACTION_PASTE                = 180
ACTION_NEXT_CONTROL         = 181
ACTION_PREV_CONTROL         = 182
ACTION_CHANNEL_SWITCH       = 183
ACTION_CHANNEL_UP           = 184
ACTION_CHANNEL_DOWN         = 185
ACTION_NEXT_CHANNELGROUP    = 186
ACTION_PREVIOUS_CHANNELGROUP = 187
ACTION_PVR_PLAY             = 188
ACTION_PVR_PLAY_TV          = 189
ACTION_PVR_PLAY_RADIO       = 190
ACTION_PVR_SHOW_TIMER_RULE  = 191
ACTION_TOGGLE_FULLSCREEN    = 199 # switch 2 desktop resolution
ACTION_TOGGLE_WATCHED       = 200 # Toggle watched status (videos)
ACTION_SCAN_ITEM            = 201 # scan item
ACTION_TOGGLE_DIGITAL_ANALOG = 202 # switch digital <-> analog
ACTION_RELOAD_KEYMAPS       = 203 # reloads CButtonTranslator's keymaps
ACTION_GUIPROFILE_BEGIN     = 204 # start the GUIControlProfiler running

ACTION_TELETEXT_RED         = 215 # Teletext Color buttons to control TopText
ACTION_TELETEXT_GREEN       = 216 #    "       "      "    "     "       "
ACTION_TELETEXT_YELLOW      = 217 #    "       "      "    "     "       "
ACTION_TELETEXT_BLUE        = 218 #    "       "      "    "     "       "

ACTION_INCREASE_PAR         = 219
ACTION_DECREASE_PAR         = 220

ACTION_VSHIFT_UP            = 227 # shift up video image in DVDPlayer
ACTION_VSHIFT_DOWN          = 228 # shift down video image in DVDPlayer

ACTION_PLAYER_PLAYPAUSE     = 229 # Play/pause. If playing it pauses, if paused it plays.

ACTION_SUBTITLE_VSHIFT_UP   = 230 # shift up subtitles in DVDPlayer
ACTION_SUBTITLE_VSHIFT_DOWN = 231 # shift down subtitles in DVDPlayer
ACTION_SUBTITLE_ALIGN       = 232 # toggle vertical alignment of subtitles

ACTION_FILTER               = 233

ACTION_SWITCH_PLAYER        = 234

ACTION_STEREOMODE_NEXT      = 235
ACTION_STEREOMODE_PREVIOUS  = 236
ACTION_STEREOMODE_TOGGLE    = 237 # turns 3d mode on/off
ACTION_STEREOMODE_SELECT    = 238
ACTION_STEREOMODE_TOMONO    = 239
ACTION_STEREOMODE_SET       = 240

ACTION_SETTINGS_RESET       = 241
ACTION_SETTINGS_LEVEL_CHANGE = 242

ACTION_TRIGGER_OSD          = 243 # show autoclosing OSD. Can b used in videoFullScreen.xml window id=2005
ACTION_INPUT_TEXT           = 244
ACTION_VOLUME_SET           = 245
ACTION_TOGGLE_COMMSKIP      = 246

# touch actions
ACTION_TOUCH_TAP            = 401
ACTION_TOUCH_TAP_TEN        = 410
ACTION_TOUCH_LONGPRESS      = 411
ACTION_TOUCH_LONGPRESS_TEN  = 420

ACTION_GESTURE_NOTIFY       = 500
ACTION_GESTURE_BEGIN        = 501
ACTION_GESTURE_ZOOM         = 502 #sendaction with point and currentPinchScale (fingers together < 1.0 -> fingers apart > 1.0)
ACTION_GESTURE_ROTATE       = 503
ACTION_GESTURE_PAN          = 504

ACTION_GESTURE_SWIPE_LEFT     = 511
ACTION_GESTURE_SWIPE_LEFT_TEN = 520
ACTION_GESTURE_SWIPE_RIGHT    = 521
ACTION_GESTURE_SWIPE_RIGHT_TEN = 530
ACTION_GESTURE_SWIPE_UP       = 531
ACTION_GESTURE_SWIPE_UP_TEN   = 540
ACTION_GESTURE_SWIPE_DOWN     = 541
ACTION_GESTURE_SWIPE_DOWN_TEN = 550
# 5xx is reserved for additional gesture actions
ACTION_GESTURE_END          = 599

# other, non-gesture actions
ACTION_ANALOG_MOVE_X          = 601 # analog thumbstick move, horizontal axis; see ACTION_ANALOG_MOVE
ACTION_ANALOG_MOVE_Y          = 602 # analog thumbstick move, vertical axis; see ACTION_ANALOG_MOVE


# The NOOP action can be specified to disable an input event. This is
# useful in user keyboard.xml etc to disable actions specified in the
# system mappings. ERROR action is used to play an error sound
ACTION_ERROR                = 998
ACTION_NOOP                 = 999

ICON_TYPE_NONE        = 101
ICON_TYPE_PROGRAMS    = 102
ICON_TYPE_MUSIC       = 103
ICON_TYPE_PICTURES    = 104
ICON_TYPE_VIDEOS      = 105
ICON_TYPE_FILES       = 106
ICON_TYPE_WEATHER     = 107
ICON_TYPE_SETTINGS    = 109

def getActionStr(aval, prefix='ACTION_'):
    _action = dict( [('0x{:04x}'.format(ival), x) for x, ival in sys.modules[__name__].__dict__.items() if x.startswith(prefix)])
    actVal = '0x{:04x}'.format(aval)
    return _action.get(actVal, actVal)

kbdEquiv = {
            65362:'up',
            65364:'down',
            65361:'left',
            65363:'right',
            65365:'pageup',
            65366:'pagedown',
            65360:'home',
            65367:'end',
            65293:'return',
            65288:'backspace',
            65307:'escape',
            65479:'f10',
            65478:'f9',
            65477:'f8',
            32   :'space',
            46   :'period',
            44   :'comma',
            65289:'tab',
            65377:'printscreen',
            45   :'minus',
            43   :'plus',
            61   :'equals',
            48   :'zero',
            49   :'one',
            50   :'two',
            51   :'three',
            52   :'four',
            53   :'five',
            54   :'six',
            55   :'seven',
            56   :'eight',
            57   :'nine',
            65451:'numpadplus',
            65453:'numpadminus',
            65438:'numpadzero',
            65436:'numpadone',
            65433:'numpadtwo',
            65435:'numpadthree',
            65430:'numpadfour',
            65437:'numpadfive',
            65432:'numpadsix',
            65429:'numpadseven',
            65431:'numpadeight',
            65434:'numpadnine',



}

actionIds = {
                "left"                    : ACTION_MOVE_LEFT,
                "right"                   : ACTION_MOVE_RIGHT,
                "up"                      : ACTION_MOVE_UP,
                "down"                    : ACTION_MOVE_DOWN,
                "pageup"                  : ACTION_PAGE_UP,
                "pagedown"                : ACTION_PAGE_DOWN,
                "select"                  : ACTION_SELECT_ITEM,
                "highlight"               : ACTION_HIGHLIGHT_ITEM,
                "parentdir"               : ACTION_NAV_BACK,
                "parentfolder"            : ACTION_PARENT_DIR,
                "back"                    : ACTION_NAV_BACK,
                "menu"                    : ACTION_MENU,
                "previousmenu"            : ACTION_PREVIOUS_MENU,
                "info"                    : ACTION_SHOW_INFO,
                "pause"                   : ACTION_PAUSE,
                "stop"                    : ACTION_STOP,
                "skipnext"                : ACTION_NEXT_ITEM,
                "skipprevious"            : ACTION_PREV_ITEM,
                "fullscreen"              : ACTION_SHOW_GUI,
                "aspectratio"             : ACTION_ASPECT_RATIO,
                "stepforward"             : ACTION_STEP_FORWARD,
                "stepback"                : ACTION_STEP_BACK,
                "bigstepforward"          : ACTION_BIG_STEP_FORWARD,
                "bigstepback"             : ACTION_BIG_STEP_BACK,
                "chapterorbigstepforward" : ACTION_CHAPTER_OR_BIG_STEP_FORWARD,
                "chapterorbigstepback"    : ACTION_CHAPTER_OR_BIG_STEP_BACK,
                "osd"                     : ACTION_SHOW_OSD,
                "showsubtitles"           : ACTION_SHOW_SUBTITLES,
                "nextsubtitle"            : ACTION_NEXT_SUBTITLE,
                "cyclesubtitle"           : ACTION_CYCLE_SUBTITLE,
                "codecinfo"               : ACTION_SHOW_CODEC,
                "nextpicture"             : ACTION_NEXT_PICTURE,
                "previouspicture"         : ACTION_PREV_PICTURE,
                "zoomout"                 : ACTION_ZOOM_OUT,
                "zoomin"                  : ACTION_ZOOM_IN,
                "playlist"                : ACTION_SHOW_PLAYLIST,
                "queue"                   : ACTION_QUEUE_ITEM,
                "zoomnormal"              : ACTION_ZOOM_LEVEL_NORMAL,
                "zoomlevel1"              : ACTION_ZOOM_LEVEL_1,
                "zoomlevel2"              : ACTION_ZOOM_LEVEL_2,
                "zoomlevel3"              : ACTION_ZOOM_LEVEL_3,
                "zoomlevel4"              : ACTION_ZOOM_LEVEL_4,
                "zoomlevel5"              : ACTION_ZOOM_LEVEL_5,
                "zoomlevel6"              : ACTION_ZOOM_LEVEL_6,
                "zoomlevel7"              : ACTION_ZOOM_LEVEL_7,
                "zoomlevel8"              : ACTION_ZOOM_LEVEL_8,
                "zoomlevel9"              : ACTION_ZOOM_LEVEL_9,
                "nextcalibration"         : ACTION_CALIBRATE_SWAP_ARROWS,
                "resetcalibration"        : ACTION_CALIBRATE_RESET,
                "analogmove"              : ACTION_ANALOG_MOVE,
                "analogmovex"             : ACTION_ANALOG_MOVE_X,
                "analogmovey"             : ACTION_ANALOG_MOVE_Y,
                "rotate"                  : ACTION_ROTATE_PICTURE_CW,
                "rotateccw"               : ACTION_ROTATE_PICTURE_CCW,
                "close"                   : ACTION_NAV_BACK,
                "subtitledelayminus"      : ACTION_SUBTITLE_DELAY_MIN,
                "subtitledelay"           : ACTION_SUBTITLE_DELAY,
                "subtitledelayplus"       : ACTION_SUBTITLE_DELAY_PLUS,
                "audiodelayminus"         : ACTION_AUDIO_DELAY_MIN,
                "audiodelay"              : ACTION_AUDIO_DELAY,
                "audiodelayplus"          : ACTION_AUDIO_DELAY_PLUS,
                "subtitleshiftup"         : ACTION_SUBTITLE_VSHIFT_UP,
                "subtitleshiftdown"       : ACTION_SUBTITLE_VSHIFT_DOWN,
                "subtitlealign"           : ACTION_SUBTITLE_ALIGN,
                "audionextlanguage"       : ACTION_AUDIO_NEXT_LANGUAGE,
                "verticalshiftup"         : ACTION_VSHIFT_UP,
                "verticalshiftdown"       : ACTION_VSHIFT_DOWN,
                "nextresolution"          : ACTION_CHANGE_RESOLUTION,
                "audiotoggledigital"      : ACTION_TOGGLE_DIGITAL_ANALOG,
                "number0"                 : REMOTE_0,
                "number1"                 : REMOTE_1,
                "number2"                 : REMOTE_2,
                "number3"                 : REMOTE_3,
                "number4"                 : REMOTE_4,
                "number5"                 : REMOTE_5,
                "number6"                 : REMOTE_6,
                "number7"                 : REMOTE_7,
                "number8"                 : REMOTE_8,
                "number9"                 : REMOTE_9,
                "smallstepback"           : ACTION_SMALL_STEP_BACK,
                "fastforward"             : ACTION_PLAYER_FORWARD,
                "rewind"                  : ACTION_PLAYER_REWIND,
                "play"                    : ACTION_PLAYER_PLAY,
                "playpause"               : ACTION_PLAYER_PLAYPAUSE,
                "switchplayer"            : ACTION_SWITCH_PLAYER,
                "delete"                  : ACTION_DELETE_ITEM,
                "copy"                    : ACTION_COPY_ITEM,
                "move"                    : ACTION_MOVE_ITEM,
                "screenshot"              : ACTION_TAKE_SCREENSHOT,
                "rename"                  : ACTION_RENAME_ITEM,
                "togglewatched"           : ACTION_TOGGLE_WATCHED,
                "scanitem"                : ACTION_SCAN_ITEM,
                "reloadkeymaps"           : ACTION_RELOAD_KEYMAPS,
                "volumeup"                : ACTION_VOLUME_UP,
                "volumedown"              : ACTION_VOLUME_DOWN,
                "mute"                    : ACTION_MUTE,
                "backspace"               : ACTION_BACKSPACE,
                "scrollup"                : ACTION_SCROLL_UP,
                "scrolldown"              : ACTION_SCROLL_DOWN,
                "analogfastforward"       : ACTION_ANALOG_FORWARD,
                "analogrewind"            : ACTION_ANALOG_REWIND,
                "moveitemup"              : ACTION_MOVE_ITEM_UP,
                "moveitemdown"            : ACTION_MOVE_ITEM_DOWN,
                "contextmenu"             : ACTION_CONTEXT_MENU,
                "shift"                   : ACTION_SHIFT,
                "symbols"                 : ACTION_SYMBOLS,
                "cursorleft"              : ACTION_CURSOR_LEFT,
                "cursorright"             : ACTION_CURSOR_RIGHT,
                "showtime"                : ACTION_SHOW_OSD_TIME,
                "analogseekforward"       : ACTION_ANALOG_SEEK_FORWARD,
                "analogseekback"          : ACTION_ANALOG_SEEK_BACK,
                "showpreset"              : ACTION_VIS_PRESET_SHOW,
                "nextpreset"              : ACTION_VIS_PRESET_NEXT,
                "previouspreset"          : ACTION_VIS_PRESET_PREV,
                "lockpreset"              : ACTION_VIS_PRESET_LOCK,
                "randompreset"            : ACTION_VIS_PRESET_RANDOM,
                "increasevisrating"       : ACTION_VIS_RATE_PRESET_PLUS,
                "decreasevisrating"       : ACTION_VIS_RATE_PRESET_MINUS,
                "showvideomenu"           : ACTION_SHOW_VIDEOMENU,
                "enter"                   : ACTION_ENTER,
                "increaserating"          : ACTION_INCREASE_RATING,
                "decreaserating"          : ACTION_DECREASE_RATING,
                "setrating"               : ACTION_SET_RATING,
                "togglefullscreen"        : ACTION_TOGGLE_FULLSCREEN,
                "nextscene"               : ACTION_NEXT_SCENE,
                "previousscene"           : ACTION_PREV_SCENE,
                "nextletter"              : ACTION_NEXT_LETTER,
                "prevletter"              : ACTION_PREV_LETTER,
                "jumpsms2"                : ACTION_JUMP_SMS2,
                "jumpsms3"                : ACTION_JUMP_SMS3,
                "jumpsms4"                : ACTION_JUMP_SMS4,
                "jumpsms5"                : ACTION_JUMP_SMS5,
                "jumpsms6"                : ACTION_JUMP_SMS6,
                "jumpsms7"                : ACTION_JUMP_SMS7,
                "jumpsms8"                : ACTION_JUMP_SMS8,
                "jumpsms9"                : ACTION_JUMP_SMS9,
                "filter"                  : ACTION_FILTER,
                "filterclear"             : ACTION_FILTER_CLEAR,
                "filtersms2"              : ACTION_FILTER_SMS2,
                "filtersms3"              : ACTION_FILTER_SMS3,
                "filtersms4"              : ACTION_FILTER_SMS4,
                "filtersms5"              : ACTION_FILTER_SMS5,
                "filtersms6"              : ACTION_FILTER_SMS6,
                "filtersms7"              : ACTION_FILTER_SMS7,
                "filtersms8"              : ACTION_FILTER_SMS8,
                "filtersms9"              : ACTION_FILTER_SMS9,
                "firstpage"               : ACTION_FIRST_PAGE,
                "lastpage"                : ACTION_LAST_PAGE,
                "guiprofile"              : ACTION_GUIPROFILE_BEGIN,
                "red"                     : ACTION_TELETEXT_RED,
                "green"                   : ACTION_TELETEXT_GREEN,
                "yellow"                  : ACTION_TELETEXT_YELLOW,
                "blue"                    : ACTION_TELETEXT_BLUE,
                "increasepar"             : ACTION_INCREASE_PAR,
                "decreasepar"             : ACTION_DECREASE_PAR,
                "volampup"                : ACTION_VOLAMP_UP,
                "volampdown"              : ACTION_VOLAMP_DOWN,
                "volumeamplification"     : ACTION_VOLAMP,
                "createbookmark"          : ACTION_CREATE_BOOKMARK,
                "createepisodebookmark"   : ACTION_CREATE_EPISODE_BOOKMARK,
                "settingsreset"           : ACTION_SETTINGS_RESET,
                "settingslevelchange"     : ACTION_SETTINGS_LEVEL_CHANGE,
                "stereomode"              : ACTION_STEREOMODE_SELECT,
                "nextstereomode"          : ACTION_STEREOMODE_NEXT,
                "previousstereomode"      : ACTION_STEREOMODE_PREVIOUS,
                "togglestereomode"        : ACTION_STEREOMODE_TOGGLE,
                "stereomodetomono"        : ACTION_STEREOMODE_TOMONO,
                "channelup"               : ACTION_CHANNEL_UP,
                "channeldown"             : ACTION_CHANNEL_DOWN,
                "previouschannelgroup"    : ACTION_PREVIOUS_CHANNELGROUP,
                "nextchannelgroup"        : ACTION_NEXT_CHANNELGROUP,
                "playpvr"                 : ACTION_PVR_PLAY,
                "playpvrtv"               : ACTION_PVR_PLAY_TV,
                "playpvrradio"            : ACTION_PVR_PLAY_RADIO,
                "record"                  : ACTION_RECORD,
                "togglecommskip"          : ACTION_TOGGLE_COMMSKIP,
                "showtimerrule"           : ACTION_PVR_SHOW_TIMER_RULE,
                "leftclick"               : ACTION_MOUSE_LEFT_CLICK,
                "rightclick"              : ACTION_MOUSE_RIGHT_CLICK,
                "middleclick"             : ACTION_MOUSE_MIDDLE_CLICK,
                "doubleclick"             : ACTION_MOUSE_DOUBLE_CLICK,
                "longclick"               : ACTION_MOUSE_LONG_CLICK,
                "wheelup"                 : ACTION_MOUSE_WHEEL_UP,
                "wheeldown"               : ACTION_MOUSE_WHEEL_DOWN,
                "mousedrag"               : ACTION_MOUSE_DRAG,
                "mousemove"               : ACTION_MOUSE_MOVE,
                "tap"                     : ACTION_TOUCH_TAP,
                "longpress"               : ACTION_TOUCH_LONGPRESS,
                "pangesture"              : ACTION_GESTURE_PAN,
                "zoomgesture"             : ACTION_GESTURE_ZOOM,
                "rotategesture"           : ACTION_GESTURE_ROTATE,
                "swipeleft"               : ACTION_GESTURE_SWIPE_LEFT,
                "swiperight"              : ACTION_GESTURE_SWIPE_RIGHT,
                "swipeup"                 : ACTION_GESTURE_SWIPE_UP,
                "swipedown"               : ACTION_GESTURE_SWIPE_DOWN,
                "error"                   : ACTION_ERROR,
                "noop"                    : ACTION_NOOP
}

''' WindowsID segun:
    https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/WindowIDs.h
'''
WINDOW_INVALID                       = 9999
WINDOW_HOME                          = 10000
WINDOW_PROGRAMS                      = 10001
WINDOW_PICTURES                      = 10002
WINDOW_FILES                         = 10003
WINDOW_SETTINGS_MENU                 = 10004
WINDOW_MUSIC                         = 10005
WINDOW_VIDEOS                        = 10006
WINDOW_SYSTEM_INFORMATION            = 10007
WINDOW_TEST_PATTERN                  = 10008
WINDOW_SCREEN_CALIBRATION            = 10011
WINDOW_SETTINGS_START                = 10016
WINDOW_SETTINGS_SYSTEM               = 10016
WINDOW_SETTINGS_SERVICE              = 10018
WINDOW_SCRIPTS                       = 10020
WINDOW_SETTINGS_MYPVR                = 10021
WINDOW_VIDEO_FILES                   = 10024
WINDOW_VIDEO_NAV                     = 10025
WINDOW_VIDEO_PLAYLIST                = 10028
WINDOW_LOGIN_SCREEN                  = 10029
WINDOW_SETTINGS_PLAYER               = 10030
WINDOW_SETTINGS_LIBRARY              = 10031
WINDOW_SETTINGS_INTERFACE            = 10032
WINDOW_SETTINGS_PROFILES             = 10034
WINDOW_SKIN_SETTINGS                 = 10035
WINDOW_ADDON_BROWSER                 = 10040
WINDOW_EVENT_LOG                     = 10050
WINDOW_SCREENSAVER_DIM               = 97
WINDOW_DEBUG_INFO                    = 98
WINDOW_DIALOG_POINTER                = 10099
WINDOW_DIALOG_YES_NO                 = 10100
WINDOW_DIALOG_PROGRESS               = 10101
WINDOW_DIALOG_KEYBOARD               = 10103
WINDOW_DIALOG_VOLUME_BAR             = 10104
WINDOW_DIALOG_SUB_MENU               = 10105
WINDOW_DIALOG_CONTEXT_MENU           = 10106
WINDOW_DIALOG_KAI_TOAST              = 10107
WINDOW_DIALOG_NUMERIC                = 10109
WINDOW_DIALOG_GAMEPAD                = 10110
WINDOW_DIALOG_BUTTON_MENU            = 10111
WINDOW_DIALOG_PLAYER_CONTROLS        = 10114
WINDOW_DIALOG_SEEK_BAR               = 10115
WINDOW_DIALOG_MUSIC_OSD              = 10120
WINDOW_DIALOG_VIS_SETTINGS           = 10121
WINDOW_DIALOG_VIS_PRESET_LIST        = 10122
WINDOW_DIALOG_VIDEO_OSD_SETTINGS     = 10123
WINDOW_DIALOG_AUDIO_OSD_SETTINGS     = 10124
WINDOW_DIALOG_VIDEO_BOOKMARKS        = 10125
WINDOW_DIALOG_FILE_BROWSER           = 10126
WINDOW_DIALOG_NETWORK_SETUP          = 10128
WINDOW_DIALOG_MEDIA_SOURCE           = 10129
WINDOW_DIALOG_PROFILE_SETTINGS       = 10130
WINDOW_DIALOG_LOCK_SETTINGS          = 10131
WINDOW_DIALOG_CONTENT_SETTINGS       = 10132
WINDOW_DIALOG_FAVOURITES             = 10134
WINDOW_DIALOG_SONG_INFO              = 10135
WINDOW_DIALOG_SMART_PLAYLIST_EDITOR  = 10136
WINDOW_DIALOG_SMART_PLAYLIST_RULE    = 10137
WINDOW_DIALOG_BUSY                   = 10138
WINDOW_DIALOG_PICTURE_INFO           = 10139
WINDOW_DIALOG_ADDON_SETTINGS         = 10140
WINDOW_DIALOG_ACCESS_POINTS          = 10141
WINDOW_DIALOG_FULLSCREEN_INFO        = 10142
WINDOW_DIALOG_SLIDER                 = 10145
WINDOW_DIALOG_ADDON_INFO             = 10146
WINDOW_DIALOG_TEXT_VIEWER            = 10147
WINDOW_DIALOG_PLAY_EJECT             = 10148
WINDOW_DIALOG_PERIPHERAL_SETTINGS    = 10150
WINDOW_DIALOG_EXT_PROGRESS           = 10151
WINDOW_DIALOG_MEDIA_FILTER           = 10152
WINDOW_DIALOG_SUBTITLES              = 10153
WINDOW_DIALOG_AUDIO_DSP_MANAGER      = 10154
WINDOW_DIALOG_AUDIO_DSP_OSD_SETTINGS = 10155
WINDOW_DIALOG_KEYBOARD_TOUCH         = 10156
WINDOW_MUSIC_PLAYLIST                = 10500
WINDOW_MUSIC_FILES                   = 10501
WINDOW_MUSIC_NAV                     = 10502
WINDOW_MUSIC_PLAYLIST_EDITOR         = 10503
WINDOW_DIALOG_OSD_TELETEXT           = 10550
WINDOW_DIALOG_PVR_ID_START           = 10600
WINDOW_DIALOG_PVR_GUIDE_INFO         = (WINDOW_DIALOG_PVR_ID_START)
WINDOW_DIALOG_PVR_RECORDING_INFO     = (WINDOW_DIALOG_PVR_ID_START+1)
WINDOW_DIALOG_PVR_TIMER_SETTING      = (WINDOW_DIALOG_PVR_ID_START+2)
WINDOW_DIALOG_PVR_GROUP_MANAGER      = (WINDOW_DIALOG_PVR_ID_START+3)
WINDOW_DIALOG_PVR_CHANNEL_MANAGER    = (WINDOW_DIALOG_PVR_ID_START+4)
WINDOW_DIALOG_PVR_GUIDE_SEARCH       = (WINDOW_DIALOG_PVR_ID_START+5)
WINDOW_DIALOG_PVR_CHANNEL_SCAN       = (WINDOW_DIALOG_PVR_ID_START+6)
WINDOW_DIALOG_PVR_UPDATE_PROGRESS    = (WINDOW_DIALOG_PVR_ID_START+7)
WINDOW_DIALOG_PVR_OSD_CHANNELS       = (WINDOW_DIALOG_PVR_ID_START+8)
WINDOW_DIALOG_PVR_OSD_GUIDE          = (WINDOW_DIALOG_PVR_ID_START+9)
WINDOW_DIALOG_PVR_RADIO_RDS_INFO     = (WINDOW_DIALOG_PVR_ID_START+10)
WINDOW_DIALOG_PVR_ID_END             = WINDOW_DIALOG_PVR_RADIO_RDS_INFO
WINDOW_PVR_ID_START                  = 10700
WINDOW_TV_CHANNELS                   = (WINDOW_PVR_ID_START)
WINDOW_TV_RECORDINGS                 = (WINDOW_PVR_ID_START+1)
WINDOW_TV_GUIDE                      = (WINDOW_PVR_ID_START+2)
WINDOW_TV_TIMERS                     = (WINDOW_PVR_ID_START+3)
WINDOW_TV_SEARCH                     = (WINDOW_PVR_ID_START+4)
WINDOW_RADIO_CHANNELS                = (WINDOW_PVR_ID_START+5)
WINDOW_RADIO_RECORDINGS              = (WINDOW_PVR_ID_START+6)
WINDOW_RADIO_GUIDE                   = (WINDOW_PVR_ID_START+7)
WINDOW_RADIO_TIMERS                  = (WINDOW_PVR_ID_START+8)
WINDOW_RADIO_SEARCH                  = (WINDOW_PVR_ID_START+9)
WINDOW_TV_TIMER_RULES                = (WINDOW_PVR_ID_START+10)
WINDOW_RADIO_TIMER_RULES             = (WINDOW_PVR_ID_START+11)
WINDOW_PVR_ID_END                    = WINDOW_RADIO_TIMER_RULES
WINDOW_FULLSCREEN_LIVETV             = 10800
WINDOW_FULLSCREEN_RADIO              = 10801
WINDOW_DIALOG_GAME_CONTROLLERS       = 10820
WINDOW_VIRTUAL_KEYBOARD              = 11000
WINDOW_DIALOG_SELECT                 = 12000
WINDOW_DIALOG_MUSIC_INFO             = 12001
WINDOW_DIALOG_OK                     = 12002
WINDOW_DIALOG_VIDEO_INFO             = 12003
WINDOW_FULLSCREEN_VIDEO              = 12005
WINDOW_VISUALISATION                 = 12006
WINDOW_SLIDESHOW                     = 12007
WINDOW_WEATHER                       = 12600
WINDOW_SCREENSAVER                   = 12900
WINDOW_DIALOG_VIDEO_OSD              = 12901
WINDOW_VIDEO_MENU                    = 12902
WINDOW_VIDEO_TIME_SEEK               = 12905
WINDOW_SPLASH                        = 12997
WINDOW_START                         = 12998
WINDOW_STARTUP_ANIM                  = 12999
WINDOW_PYTHON_START                  = 13000
WINDOW_PYTHON_END                    = 13099
WINDOW_ADDON_START                   = 14000
WINDOW_ADDON_END                     = 14099

windowsId = {
                "home"                    : WINDOW_HOME,
                "programs"                : WINDOW_PROGRAMS,
                "pictures"                : WINDOW_PICTURES,
                "filemanager"             : WINDOW_FILES,
                "files"                   : WINDOW_FILES,
                "settings"                : WINDOW_SETTINGS_MENU,
                "music"                   : WINDOW_MUSIC,
                "video"                   : WINDOW_VIDEOS,
                "videos"                  : WINDOW_VIDEO_NAV,
                "pvr"                     : WINDOW_TV_CHANNELS,
                "tvchannels"              : WINDOW_TV_CHANNELS,
                "tvrecordings"            : WINDOW_TV_RECORDINGS,
                "tvguide"                 : WINDOW_TV_GUIDE,
                "tvtimers"                : WINDOW_TV_TIMERS,
                "tvsearch"                : WINDOW_TV_SEARCH,
                "radiochannels"           : WINDOW_RADIO_CHANNELS,
                "radiorecordings"         : WINDOW_RADIO_RECORDINGS,
                "radioguide"              : WINDOW_RADIO_GUIDE,
                "radiotimers"             : WINDOW_RADIO_TIMERS,
                "radiosearch"             : WINDOW_RADIO_SEARCH,
                "gamecontrollers"         : WINDOW_DIALOG_GAME_CONTROLLERS,
                "pvrguideinfo"            : WINDOW_DIALOG_PVR_GUIDE_INFO,
                "pvrrecordinginfo"        : WINDOW_DIALOG_PVR_RECORDING_INFO,
                "pvrradiordsinfo"         : WINDOW_DIALOG_PVR_RADIO_RDS_INFO,
                "pvrtimersetting"         : WINDOW_DIALOG_PVR_TIMER_SETTING,
                "pvrgroupmanager"         : WINDOW_DIALOG_PVR_GROUP_MANAGER,
                "pvrchannelmanager"       : WINDOW_DIALOG_PVR_CHANNEL_MANAGER,
                "pvrguidesearch"          : WINDOW_DIALOG_PVR_GUIDE_SEARCH,
                "pvrchannelscan"          : WINDOW_DIALOG_PVR_CHANNEL_SCAN,
                "pvrupdateprogress"       : WINDOW_DIALOG_PVR_UPDATE_PROGRESS,
                "pvrosdchannels"          : WINDOW_DIALOG_PVR_OSD_CHANNELS,
                "pvrosdguide"             : WINDOW_DIALOG_PVR_OSD_GUIDE,
                "pvrosdteletext"          : WINDOW_DIALOG_OSD_TELETEXT,
                "systeminfo"              : WINDOW_SYSTEM_INFORMATION,
                "testpattern"             : WINDOW_TEST_PATTERN,
                "screencalibration"       : WINDOW_SCREEN_CALIBRATION,
                "guicalibration"          : WINDOW_SCREEN_CALIBRATION,
                "systemsettings"          : WINDOW_SETTINGS_SYSTEM,
                "servicesettings"         : WINDOW_SETTINGS_SERVICE,
                "networksettings"         : WINDOW_SETTINGS_SERVICE,
                "pvrsettings"             : WINDOW_SETTINGS_MYPVR,
                "tvsettings"              : WINDOW_SETTINGS_MYPVR,
                "playersettings"          : WINDOW_SETTINGS_PLAYER,
                "librarysettings"         : WINDOW_SETTINGS_LIBRARY,
                "interfacesettings"       : WINDOW_SETTINGS_INTERFACE,
                "scripts"                 : WINDOW_PROGRAMS,
                "videofiles"              : WINDOW_VIDEO_FILES,
                "videolibrary"            : WINDOW_VIDEO_NAV,
                "videoplaylist"           : WINDOW_VIDEO_PLAYLIST,
                "loginscreen"             : WINDOW_LOGIN_SCREEN,
                "profiles"                : WINDOW_SETTINGS_PROFILES,
                "skinsettings"            : WINDOW_SKIN_SETTINGS,
                "addonbrowser"            : WINDOW_ADDON_BROWSER,
                "yesnodialog"             : WINDOW_DIALOG_YES_NO,
                "progressdialog"          : WINDOW_DIALOG_PROGRESS,
                "virtualkeyboard"         : WINDOW_DIALOG_KEYBOARD,
                "volumebar"               : WINDOW_DIALOG_VOLUME_BAR,
                "submenu"                 : WINDOW_DIALOG_SUB_MENU,
                "favourites"              : WINDOW_DIALOG_FAVOURITES,
                "contextmenu"             : WINDOW_DIALOG_CONTEXT_MENU,
                "notification"            : WINDOW_DIALOG_KAI_TOAST,
                "infodialog"              : WINDOW_DIALOG_KAI_TOAST,
                "numericinput"            : WINDOW_DIALOG_NUMERIC,
                "gamepadinput"            : WINDOW_DIALOG_GAMEPAD,
                "shutdownmenu"            : WINDOW_DIALOG_BUTTON_MENU,
                "playercontrols"          : WINDOW_DIALOG_PLAYER_CONTROLS,
                "seekbar"                 : WINDOW_DIALOG_SEEK_BAR,
                "musicosd"                : WINDOW_DIALOG_MUSIC_OSD,
                "addonsettings"           : WINDOW_DIALOG_ADDON_SETTINGS,
                "visualisationsettings"   : WINDOW_DIALOG_ADDON_SETTINGS,
                "visualisationpresetlist" : WINDOW_DIALOG_VIS_PRESET_LIST,
                "osdvideosettings"        : WINDOW_DIALOG_VIDEO_OSD_SETTINGS,
                "osdaudiosettings"        : WINDOW_DIALOG_AUDIO_OSD_SETTINGS,
                "audiodspmanager"         : WINDOW_DIALOG_AUDIO_DSP_MANAGER,
                "osdaudiodspsettings"     : WINDOW_DIALOG_AUDIO_DSP_OSD_SETTINGS,
                "videobookmarks"          : WINDOW_DIALOG_VIDEO_BOOKMARKS,
                "filebrowser"             : WINDOW_DIALOG_FILE_BROWSER,
                "networksetup"            : WINDOW_DIALOG_NETWORK_SETUP,
                "mediasource"             : WINDOW_DIALOG_MEDIA_SOURCE,
                "profilesettings"         : WINDOW_DIALOG_PROFILE_SETTINGS,
                "locksettings"            : WINDOW_DIALOG_LOCK_SETTINGS,
                "contentsettings"         : WINDOW_DIALOG_CONTENT_SETTINGS,
                "songinformation"         : WINDOW_DIALOG_SONG_INFO,
                "smartplaylisteditor"     : WINDOW_DIALOG_SMART_PLAYLIST_EDITOR,
                "smartplaylistrule"       : WINDOW_DIALOG_SMART_PLAYLIST_RULE,
                "busydialog"              : WINDOW_DIALOG_BUSY,
                "pictureinfo"             : WINDOW_DIALOG_PICTURE_INFO,
                "accesspoints"            : WINDOW_DIALOG_ACCESS_POINTS,
                "fullscreeninfo"          : WINDOW_DIALOG_FULLSCREEN_INFO,
                "sliderdialog"            : WINDOW_DIALOG_SLIDER,
                "addoninformation"        : WINDOW_DIALOG_ADDON_INFO,
                "subtitlesearch"          : WINDOW_DIALOG_SUBTITLES,
                "musicplaylist"           : WINDOW_MUSIC_PLAYLIST,
                "musicfiles"              : WINDOW_MUSIC_FILES,
                "musiclibrary"            : WINDOW_MUSIC_NAV,
                "musicplaylisteditor"     : WINDOW_MUSIC_PLAYLIST_EDITOR,
                "teletext"                : WINDOW_DIALOG_OSD_TELETEXT,
                "selectdialog"            : WINDOW_DIALOG_SELECT,
                "musicinformation"        : WINDOW_DIALOG_MUSIC_INFO,
                "okdialog"                : WINDOW_DIALOG_OK,
                "movieinformation"        : WINDOW_DIALOG_VIDEO_INFO,
                "textviewer"              : WINDOW_DIALOG_TEXT_VIEWER,
                "fullscreenvideo"         : WINDOW_FULLSCREEN_VIDEO,
                "fullscreenlivetv"        : WINDOW_FULLSCREEN_LIVETV,
                "fullscreenradio"         : WINDOW_FULLSCREEN_RADIO,
                "visualisation"           : WINDOW_VISUALISATION,
                "slideshow"               : WINDOW_SLIDESHOW,
                "weather"                 : WINDOW_WEATHER,
                "screensaver"             : WINDOW_SCREENSAVER,
                "videoosd"                : WINDOW_DIALOG_VIDEO_OSD,
                "videomenu"               : WINDOW_VIDEO_MENU,
                "videotimeseek"           : WINDOW_VIDEO_TIME_SEEK,
                "startwindow"             : WINDOW_START,
                "startup"                 : WINDOW_STARTUP_ANIM,
                "peripheralsettings"      : WINDOW_DIALOG_PERIPHERAL_SETTINGS,
                "extendedprogressdialog"  : WINDOW_DIALOG_EXT_PROGRESS,
                "mediafilter"             : WINDOW_DIALOG_MEDIA_FILTER,
                "addon"                   : WINDOW_ADDON_START,
                "eventlog"                : WINDOW_EVENT_LOG,
                "tvtimerrules"            : WINDOW_TV_TIMER_RULES,
                "radiotimerrules"         : WINDOW_RADIO_TIMER_RULES
}

