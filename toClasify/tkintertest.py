import Tkinter as tk
import os
import re
import sys
import ttk

import ImageTk
import xbmcaddon
from KodiAddonIDE.KodiStubs.xbmcModules import xbmc
from PIL import ImageFont
from PIL import ImageGrab

import controlXml


class Window(tk.Toplevel, object):

    rescode = ['1080i', '720p', '480p 4:3', '480p 16:9', 'NTSC 4:3',
               'NTSC 16:9', 'PAL 4:3', 'PAL 16:9', 'PAL60 4:3', 'PAL60 16:9']

    resolution = {'1080i': (1920, 1080), '720p': (720, 480),
                  '480p 4:3': (720, 480), '480p 16:9': (720, 480),
                  'NTSC 4:3': (720, 480), 'NTSC 16:9': (720, 480),
                  'PAL 4:3': (720, 576), 'PAL 16:9': (720, 576),
                  'PAL60 4:3': (720, 480), 'PAL60 16:9': (720, 480)
                  }
    defRes = '720p'


    """Create a new Window to draw on."""

    def __init__(self, windowId=-1):
        """
        Create a new Window to draw on.

        Specify an id to use an existing window.

        Raises:
        ValueError: If supplied window Id does not exist.
        Exception: If more then 200 windows are created.

        Deleting this window will activate the old window that was active
        and resets (not delete) all controls that are associated with this window.
        """
        root = controlXml.AppWindow()
        tk.Toplevel.__init__(self, root)
        self.attributes('-fullscreen', True)
        self.overrideredirect(True)

        self.windowId = windowId
        if windowId != -1:
            self.window = windowId
        # else:
        #     self.window = tk.Frame()
        self.xorg = 0
        self.yorg = 0
        self.res = self.defRes
        self.controls = {}
        self.properties = {}
        pass

    def show(self):
        """Show this window.

        Shows this window by activating it, calling close() after it wil activate the current window again.

        Note:
            If your script ends this window will be closed to. To show it forever,
            make a loop at the end of your script and use doModal() instead.
        """
        # self.window.pack()
        pass

    def close(self):
        """Closes this window.

        Closes this window by activating the old window.
        The window is not deleted with this method.
        """
        self.removeControls(self.controls.values())
        self.window.destroy()
        pass

    def onAction(self, action):
        """onAction method.

        This method will recieve all actions that the main program will send to this window.
        By default, only the PREVIOUS_MENU action is handled.
        Overwrite this method to let your script handle all actions.
        Don't forget to capture ACTION_PREVIOUS_MENU, else the user can't close this window.
        """

        pass

    def onClick(self, control):
        """onClick method.

        This method will recieve all click events that the main program will send to this window.
        """
        pass

    def onDoubleClick(self):
        pass

    def onControl(self, control):
        """
        onControl method.
        This method will recieve all control events that the main program will send to this window.
        'control' is an instance of a Control object.
        """
        pass

    def onFocus(self, control):
        """onFocus method.

        This method will recieve all focus events that the main program will send to this window.
        """
        pass

    def onInit(self):
        """onInit method.

        This method will be called to initialize the window.
        """
        pass

    def doModal(self):
        """Display this window until close() is called."""
        parent = self.winfo_parent()
        parent = self.nametowidget(parent)
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
        pass

    def addControl(self, control):
        """Add a Control to this window.

        Raises:
            TypeError: If supplied argument is not a Control type.
            ReferenceError: If control is already used in another window.
            RuntimeError: Should not happen :-)

        The next controls can be added to a window atm:
            ControlLabel
            ControlFadeLabel
            ControlTextBox
            ControlButton
            ControlCheckMark
            ControlList
            ControlGroup
            ControlImage
            ControlRadioButton
            ControlProgress
        """
        if not isinstance(control, Control): raise TypeError('Not a Control type')
        if control.isAdded(): raise ReferenceError('the control is already used in another window')
        id  = control.getId()
        if id is not None:
            id = str(id)
            self.controls[id] = str(control)
        xraw, yraw = control.getPosition()
        dbaseX, dbaseY = self.resolution[self.defRes]
        rbaseX, rbaseY = self.resolution[self.res]
        xmult, ymult = (1.0*rbaseX)/dbaseX, (1.0*rbaseY)/dbaseY
        xpos = self.xorg + int(xraw*xmult)
        ypos = self.yorg + int(yraw*ymult)
        control._createControl(self)
        control.place(in_=self, x=xpos, y=ypos)
        pass

    def addControls(self, controls):
        """
        addControls(self, List)--Add a list of Controls to this window.

        *Throws:
        - TypeError, if supplied argument is not ofList type, or a control is not ofControl type
        - ReferenceError, if control is already used in another window
        - RuntimeError, should not happen :-)
        """
        k = 0
        for control in controls:
            self.addControl(control)
            print k, len(controls), str(control)
            k += 1
        pass

    def getControl(self, controlId):
        """Get's the control from this window.

        Raises:
            Exception: If Control doesn't exist

        controlId doesn't have to be a python control, it can be a control id
        from a xbmc window too (you can find id's in the xml files).

        Note:
            Not python controls are not completely usable yet.
            You can only use the Control functions.
        """
        if controlId not in self.controls: raise Exception('Not a valid controlId')
        return self.controls[controlId]

    def setFocus(self, control):
        """Give the supplied control focus.

        Raises:
            TypeError: If supplied argument is not a Control type.
            SystemError: On Internal error.
            RuntimeError: If control is not added to a window.
        """
        if not isinstance(control, Control): raise TypeError('Not a Control type')
        control.focus_force()
        pass

    def setFocusId(self, controlId):
        """Gives the control with the supplied focus.

        Raises:
            SystemError: On Internal error.
            RuntimeError: If control is not added to a window.
        """
        control = self.getControl(str(controlId))
        self.setFocus(control)
        pass

    def getFocus(self):
        """Returns the control which is focused.

        Raises:
            SystemError: On Internal error.
            RuntimeError: If no control has focus.
        """
        return self.focus_lastfor()

    def getFocusId(self):
        """Returns the id of the control which is focused.

        Raises:
            SystemError: On Internal error.
            RuntimeError: If no control has focus.
        """
        control = self.getFocus()
        return long(control.getId())

    def removeControl(self, control):
        """Removes the control from this window.

        Raises:
            TypeError: If supplied argument is not a Control type.
            RuntimeError: If control is not added to this window.

        This will not delete the control. It is only removed from the window.
        """
        if not isinstance(control, Control): raise TypeError('Not a Control type')
        controlId = str(control.getId())
        self.controls.pop(controlId)
        control.place_forget()
        pass

    def removeControls(self, controls):
        for control in controls:
            self.removeControl(control)
        pass

    def getHeight(self):
        """Returns the height of this screen."""
        return self.winfo_screenheight()

    def getWidth(self):
        """Returns the width of this screen."""
        return self.winfo_screenwidth()

    def getResolution(self):
        """Returns the resolution of the screen.

        The returned value is one of the following:
            0 - 1080i      (1920x1080)
            1 - 720p       (1280x720)
            2 - 480p 4:3   (720x480)
            3 - 480p 16:9  (720x480)
            4 - NTSC 4:3   (720x480)
            5 - NTSC 16:9  (720x480)
            6 - PAL 4:3    (720x576)
            7 - PAL 16:9   (720x576)
            8 - PAL60 4:3  (720x480)
            9 - PAL60 16:9 (720x480)
        Note: this info is outdated. XBMC 12+ returns different vaulues.
        """
        res = self.res
        return long(self.rescode.index(res))


    def setCoordinateResolution(self, resolution):
        """Sets the resolution that the coordinates of all controls are defined in.

        Allows XBMC to scale control positions and width/heights to whatever resolution
        XBMC is currently using.

        resolution is one of the following:
            0 - 1080i      (1920x1080)
            1 - 720p       (1280x720)
            2 - 480p 4:3   (720x480)
            3 - 480p 16:9  (720x480)
            4 - NTSC 4:3   (720x480)
            5 - NTSC 16:9  (720x480)
            6 - PAL 4:3    (720x576)
            7 - PAL 16:9   (720x576)
            8 - PAL60 4:3  (720x480)
            9 - PAL60 16:9 (720x480)

        Note: default is 720p (1280x720)
        Note 2: this is not an actual display resulution. This is the resolution of the coordinate grid
        all controls are placed on.
        """
        self.res = self.rescode[resolution]
        pass

    def setProperty(self, key, value):
        """Sets a window property, similar to an infolabel.

        key: string - property name.
        value: string or unicode - value of property.

        Note:
            key is NOT case sensitive. Setting value to an empty string is equivalent to clearProperty(key).

        Example:
            win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
            win.setProperty('Category', 'Newest')
        """
        self.properties[key] = value
        pass

    def getProperty(self, key):
        """Returns a window property as a string, similar to an infolabel.

        key: string - property name.

        Note:
            key is NOT case sensitive.

        Example:
            win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
            category = win.getProperty('Category')
        """
        return self.properties[key]

    def clearProperty(self, key):
        """Clears the specific window property.

        key: string - property name.

        Note:
            key is NOT case sensitive. Equivalent to setProperty(key,'').

        Example:
            win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
            win.clearProperty('Category')
        """
        self.properties.pop(key)
        pass

    def clearProperties(self):
        """Clears all window properties.

        Example:
            win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
            win.clearProperties()
        """
        for key in self.properties:
            self.clearProperty(key)
        pass

    # noinspection PyUnusedLocal
class WindowDialog(Window):
    """
    Create a new WindowDialog with transparent background, unlike Window.
    WindowDialog always stays on top of XBMC UI.
    """

    def __init__(self):
        Window.__init__(self)
        canvas = tk.Canvas(self, bg='black', borderwidth=0)
        canvas.place(relwidth=1.0, relheight=1.0)

        bgimg = ImageGrab.grab()
        self.photo = photo = ImageTk.PhotoImage(bgimg)
        canvas.create_image(0, 0, image=photo, anchor='nw')
        # focusId = self.focus_lastfor()
        # self.lift(focusId)
        pass

# noinspection PyUnusedLocal
class WindowXML(Window):
    """Create a new WindowXML script."""

    def __init__(self, xmlFilename, scriptPath, defaultSkin='Default', defaultRes='720p'):
        """
        xmlFilename: string - the name of the xml file to look for.
        scriptPath: string - path to script. used to fallback to if the xml doesn't exist in the current skin.
        (eg os.getcwd())
        defaultSkin: string - name of the folder in the skins path to look in for the xml.
        defaultRes: string - default skins resolution.

        Note:
        Skin folder structure is eg(resources/skins/Default/720p).

        Example:
        ui = GUI('script-Lyrics-main.xml', os.getcwd(), 'LCARS', 'PAL')
        ui.doModal()
        del ui
        """
        Window.__init__(self)
        self.windowname = os.path.splitext(xmlFilename)[0]
        self.scriptPath = scriptPath
        self.defaultSkin =  defaultSkin
        self.defaultRes = defaultRes

    def setGUI(self):
        window, controls = controlXml.getRoots(self.windowname + '.xml', self.scriptPath, self.defaultSkin, self.defaultRes)
        wndList = controlXml.processRoot(window)
        wndMap = {}
        for elem in wndList:
            key = elem.pop('elem_tag')
            wndMap[key] = elem
        coord = wndMap['coordinates']
        self.xorg = int(coord.get('left', 0))
        self.yorg = int(coord.get('top', 0))
        resId = int(coord.get('system', 1))
        self.res = self.rescode[resId]

        ctrList = controlXml.processRoot(controls)

        controls = []
        for k in range(len(ctrList)):
            genTags, args, kwargs, navTags = controlXml.mapArgsKwargs(ctrList, k)
            ctrClassName = genTags['ctrClass']
            ctrClass = getattr(sys.modules[__name__], ctrClassName)
            control = ctrClass(*args, **kwargs)
            if genTags.has_key('id'):
                control.getId = lambda : int(genTags.get('id'))
            controls.append(control)
        self.addControls(controls)
        pass

    def doModal(self):
        self.setGUI()
        # Window.doModal(self)
        self.show()

    def removeItem(self, position):
        """Removes a specified item based on position, from the Window List.

        position: integer - position of item to remove.
        """
        control = self.items.pop(position)
        pass

    def addItem(self, item, position=32767):
        """Add a new item to this Window List.

        item: string, unicode or ListItem - item to add.
        position: integer - position of item to add. (NO Int = Adds to bottom,0 adds to top, 1 adds to one below from top,-1 adds to one above from bottom etc etc)
                  If integer positions are greater than list size, negative positions will add to top of list, positive positions will add to bottom of list.
        Example:
            self.addItem('Reboot XBMC', 0)
        """
        self.items.insert(position, item)
        pass

    def clearList(self):
        """Clear the Window List."""
        while self.items:
            self.items.pop()
        pass

    def setCurrentListPosition(self, position):
        """Set the current position in the Window List.

        position: integer - position of item to set.
        """
        self.currItem = long(position)
        pass

    def getCurrentListPosition(self):
        """Gets the current position in the Window List."""
        return self.currItem

    def getListItem(self, position):
        """Returns a given ListItem in this Window List.

        position: integer - position of item to return.
        """
        lenItem = self.getListSize()
        position = max(-lenItem, min(lenItem, position))
        return self.items[position]

    def getListSize(self):
        """Returns the number of items in this Window List."""
        return long(len(self.items))

    def setProperty(self, key, value):
        """Sets a container property, similar to an infolabel.

        key: string - property name.
        value: string or unicode - value of property.

        Note:
            Key is NOT case sensitive.

        Example:
            self.setProperty('Category', 'Newest')
        """
        self.properties[key] = value
        pass

# noinspection PyUnusedLocal
class WindowXMLDialog(WindowXML):
    """Create a new WindowXMLDialog script."""

    def __init__(self, xmlFilename, scriptPath, defaultSkin="Default", defaultRes="720p"):
        """
        xmlFilename: string - the name of the xml file to look for.
        scriptPath: string - path to script. used to fallback to if the xml doesn't exist in the current skin. (eg os.getcwd())
        defaultSkin: string - name of the folder in the skins path to look in for the xml.
        defaultRes: string - default skins resolution.

        Note:
        Skin folder structure is eg(resources/skins/Default/720p).

        Example:
        ui = GUI('script-Lyrics-main.xml', os.getcwd(), 'LCARS', 'PAL')
        ui.doModal()
        del ui
        """
        WindowXML.__init__(self, xmlFilename, scriptPath, defaultSkin, defaultRes)
        canvas = tk.Canvas(self, bg='black', borderwidth=0)
        canvas.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        bgimg = ImageGrab.grab()
        self.photo = photo = ImageTk.PhotoImage(bgimg)
        canvas.create_image(0, 0, image=photo, anchor='nw')
        self.focus_set()
        self.lift()
        pass


#noinspection PyUnusedLocal
class Control(object):
    """
    Parent for control classes. The problem here is that Python uses references to this class in a dynamic typing way.
    For example, you will find this type of python code frequently:
    window.getControl( 100 ).setLabel( "Stupid Dynamic Type")
    Notice that the 'getControl' call returns a 'Control ' object.
    In a dynamically typed language, the subsequent call to setLabel works if the specific type of control has the method.
    The script writer is often in a position to know more than the code about the specificControl type
    (in the example, that control id 100 is a 'ControlLabel ') where the C++ code is not.
    SWIG doesn't support this type of dynamic typing. The 'Control ' wrapper that's returned will wrap aControlLabel
    but will not have the 'setLabel' method on it. The only way to handle this is to add all possible subclass methods
    to the parent class. This is ugly but the alternative is nearly as ugly.
    It's particularly ugly here because the majority of the methods are unique to the particular subclass.
    If anyone thinks they have a solution then let me know. The alternative would be to have a set of 'getContol'
    methods, each one coresponding to a type so that the downcast can be done in the native code.
    IOW rather than a simple 'getControl' there would be a 'getControlLabel', 'getControlRadioButton',
    'getControlButton', etc.
    TODO:This later solution should be implemented for future scripting languages
    while the former will remain as deprecated functionality for Python.
    """
    def addItem(self):
        pass

    def addItems(self):
        pass

    def canAcceptMessages(self):
        pass

    def controlDown(self, control=None):
        """
        controlDown(control)--Set's the controls down navigation.
        control : control object - control to navigate to on down.
        *Note, You can also usesetNavigation() . Set to self to disable navigation.

        Throws:
         - TypeError, if one of the supplied arguments is not a control type.
         - ReferenceError, if one of the controls is not added to a window.
        example:
         - self.button.controlDown(self.button1)
        """
        self.down = control
        pass

    def controlLeft(self, control=None):
        """
        controlLeft(control)--Set's the controls left navigation.

        control : control object - control to navigate to on left.

        *Note, You can also usesetNavigation() . Set to self to disable navigation.

        Throws:
        - TypeError, if one of the supplied arguments is not a control type.
        - ReferenceError, if one of the controls is not added to a window.


        example:
        - self.button.controlLeft(self.button1)
        """
        self.left = control
        pass

    def controlRight(self, control=None):
        """
        controlRight(control)--Set's the controls right navigation.

        control : control object - control to navigate to on right.

        *Note, You can also usesetNavigation() . Set to self to disable navigation.

        Throws:
        - TypeError, if one of the supplied arguments is not a control type.
        - ReferenceError, if one of the controls is not added to a window.

        example:
        - self.button.controlRight(self.button1)
        """
        self.right = control
        pass

    def controlUp(self, control=None):
        """
        controlUp(control)--Set's the controls up navigation.

        control : control object - control to navigate to on up.

        *Note, You can also usesetNavigation() . Set to self to disable navigation.

        Throws:
        - TypeError, if one of the supplied arguments is not a control type.
        - ReferenceError, if one of the controls is not added to a window.
        example:
         - self.button.controlUp(self.button1)
         """
        self.up = control
        pass

    def getHeight(self):
        """
        getHeight() --Returns the control's current height as an integer.

        example:
        - height = self.button.getHeight()
        """
        return self.height

    def getId(self):
        """
        getId() --Returns the control's current id as an integer.

        example:
        - id = self.button.getId()
        """
        return None

    def getPosition(self):
        """
        getPosition() --Returns the control's current position as a x,y integer tuple.

        example:
        - pos = self.button.getPosition()
        """
        return (self.getX(), self.getY())

    def getWidth(self):
        """
        getWidth() --Returns the control's current width as an integer.

        example:
        - width = self.button.getWidth()
        """
        return self.width

    def getX(self):
        """
        Get X coordinate of a control as an integer.
        """
        return self.x

    def getY(self):
        """
        Get Y coordinate of a control as an integer.
        """
        return self.y

    def setAnimations(self, event_attr=[()]):
        """
        setAnimations([(event, attr,)*])--Set's the control's animations.

        [(event,attr,)*] : list - A list of tuples consisting of event and attributes pairs.
        - event : string - The event to animate.
        - attr : string - The whole attribute string separated by spaces.


        Animating your skin -http://wiki.xbmc.org/?title=Animating_Your_Skin

        example:
        - self.button.setAnimations([('focus', 'effect=zoom end=90,247,220,56 time=0',)])
        """
        pass

    def setEnableCondition(self, enable):
        """
        setEnableCondition(enable)--Set's the control's enabled condition.
        Allows XBMC to control the enabled status of the control.

        enable : string - Enable condition.

        List of Conditions -http://wiki.xbmc.org/index.php?title=List_of_Boolean_Conditions

        example:
        - self.button.setEnableCondition('System.InternetState')
        """
        pass

    def setEnabled(self, enabled=True):
        """
        setEnabled(enabled)--Set's the control's enabled/disabled state.

        enabled : bool - True=enabled / False=disabled.

        example:
        - self.button.setEnabled(False)
        """
        pass

    def setHeight(self, height):
        """
        setHeight(height)--Set's the controls height.

        height : integer - height of control.

        example:
        - self.image.setHeight(100)
        """
        self.height = height
        pass

    def setNavigation(self, up=None, down=None, left=None, right=None):
        """
        setNavigation(up, down, left, right)--Set's the controls navigation.

        up : control object - control to navigate to on up.
        down : control object - control to navigate to on down.
        left : control object - control to navigate to on left.
        right : control object - control to navigate to on right.

        *Note, Same ascontrolUp() ,controlDown() ,controlLeft() ,controlRight() . Set to self to disable navigation for that direction.

        Throws:
        - TypeError, if one of the supplied arguments is not a control type.
        - ReferenceError, if one of the controls is not added to a window.


        example:
        - self.button.setNavigation(self.button1, self.button2, self.button3, self.button4)
        """
        if up: self.controlUp(up)
        if down: self.controlDown(down)
        if left: self.controlLeft(left)
        if right: self.controlRight(right)
        pass

    def setPosition(self, x, y):
        """
        setPosition(x, y)--Set's the controls position.

        x : integer - x coordinate of control.
        y : integer - y coordinate of control.

        *Note, You may use negative integers. (e.g sliding a control into view)

        example:
        - self.button.setPosition(100, 250)
        """
        self.x = x
        self.y = y
        pass

    def setVisible(self, visible):
        """
        setVisible(visible)--Set's the control's visible/hidden state.

        visible : bool - True=visible / False=hidden.

        example:
        - self.button.setVisible(False)
        """
        if visible: self.pack()
        else:
            self.pack_forget()
        pass

    def setVisibleCondition(self, condition, allowHiddenFocus=False):
        """
        setVisibleCondition(visible[,allowHiddenFocus])--Set's the control's visible condition.
        Allows XBMC to control the visible status of the control.

        visible : string - Visible condition.
        allowHiddenFocus : bool - True=gains focus even if hidden.

        List of Conditions -http://wiki.xbmc.org/index.php?title=List_of_Boolean_Conditions

        example:
        - self.button.setVisibleCondition('[Control.IsVisible(41) + !Control.IsVisible(12)]', True)
        """
        pass

    def setWidth(self, width):
        """
        setWidth(width)--Set's the controls width.

        width : integer - width of control.

        example:
        - self.image.setWidth(100)
        """
        self.width = width
        pass


#noinspection PyUnusedLocal
class ControlBase:

    def __init__(self):
        self.Frame = None
        self.widget = None
        self._type = ''
        self._args = []
        self._kwargs = {}
        self._binds = []
        # ttk.Frame.__init__(self, root, width=width, height=height)

    def isAdded(self):
        return self.Frame is not None

    def pack(self, *args, **kwargs):
        if not self.isAdded(): return
        self.Frame.pack(self, *args, **kwargs)
        self.Frame.pack_propagate(False)

    def grid(self, *args, **kwargs):
        if not self.isAdded(): return
        self.Frame.grid(self, *args, **kwargs)
        self.Frame.grid_propagate(False)

    def _createControl(self, master):
        width, height = self.getWidth(), self.getHeight()
        self.Frame = ttk.Frame(master, width=width, height=height)
        self.Frame.pack_propagate(False)
        try:
            wfunc = getattr(ttk, self._type)
        except:
            wfunc = getattr(tk, self._type)
        self.widget = wfunc(self.Frame, **self._kwargs)
        self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        for bind in self._binds:
            mname, args = bind[0], bind[1:]
            try:
                method = getattr(self.widget, mname)
            except:
                method = getattr(self, mname)
            method(*args)
        self.widget.pack(fill=tk.BOTH, expand=tk.YES)

    def __getattr__(self, item):
        if self.isAdded():
            return getattr(self.Frame, item)


    def _eqTkFont(self, fontname, fontset='Default', res='720p'):
        pathName, skinDir = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
        fontXml = os.path.join(pathName, skinDir, res, 'Font.xml')
        fonts = xbmcaddon.Addon._parseXml(fontXml)
        fontset = fonts.find('.//fontset[@id="%s"]' % fontset)
        font = fontset.find('.//font[name="%s"]' % fontname)
        attrib = {}
        if font:
            for child in font.getchildren():
                attrib[child.tag] = child.text
            filename = attrib['filename']
            filename = os.path.join(pathName, skinDir, 'Fonts', filename)
            if os.path.exists(filename):
                font = ImageFont.truetype(filename)
                attrib['family'] = font.font.family
                if font.font.style != 'Regular': attrib['style'] = font.font.style
        family = attrib.get('family', 'Roman')
        size = attrib.get('size', 10)
        weight = attrib.get('style', 'normal')
        return (family, size, weight)

    def _getThemeColour(self, *args):
        pathName, skinDir = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
        colorXml = skinDir.split('.', 1)[1] + '.xml'
        colorXml = os.path.join(pathName, skinDir, 'Colors', colorXml)
        defaultXml = os.path.join(pathName, skinDir, 'Colors', 'defaults.xml')
        colorsRoot = []
        for fileName in [colorXml, defaultXml]:
            if not os.path.exists(fileName): continue
            colorsRoot.append(xbmcaddon.Addon._parseXml(fileName))
        codes = list(args)
        for k in range(len(codes)):
            srchcolor = codes[k]
            if not re.match('[0-9ABCDEF]{8}\Z', srchcolor.upper()):
                for colors in colorsRoot:
                    color = colors.find('.//color[@name="%s"]' % srchcolor)
                    if color is None: continue
                    color = '#' + color.text[2:]
                    break
                else:
                    color = None
            else:
                color = '#' + srchcolor[2:]
            codes[k] = color
        return codes[0] if len(codes) == 1 else codes



    def _fltKw(self, kw):
        for key in kw.keys():
            vList = kw[key]
            if isinstance(vList, list):
                vList = [elem for elem in vList if elem[-1]]
            if vList:
                kw[key] = vList
            else:
                kw.pop(key)
        return kw


    def _setTexture(self, filename):
        from PIL import Image
        import ImageTk
        width, height = self.getWidth(), self.getHeight()
        image = Image.open(filename)
        self.imagetk = ImageTk.PhotoImage(image.mode, (width, height))
        imagetk = image.resize((width, height))
        self.imagetk.paste(imagetk, (0, 0, width, height))
        self.widget.configure(image=self.imagetk)
        pass

    def _setAlignment(self, _alignment):
        xbfont_left = 0x00000000
        xbfont_right = 0x00000001
        xbfont_center_x = 0x00000002
        xbfont_center_y = 0x00000004
        xbfont_truncated = 0x00000008
        self._yalignment = tk.NSEW if _alignment and 0x00000004 & _alignment else tk.NW
        index = 0x00000003 & (_alignment or xbfont_left)
        self._xalignment = (tk.LEFT, tk.RIGHT, tk.CENTER, tk.LEFT) [index]

    def _setLabelAlignment(self, labelsize):
        # import tkFont
        widget = self.widget
        width, height = self.cget('width'), self.cget('height')
        labelwidth, labelheight = labelsize
        pckKwargs = {'x': 0, 'y': 0}
        if self._alignment == tk.RIGHT:
            pckKwargs['x'] = width - labelwidth
        elif self._alignment == tk.CENTER:
            pckKwargs['x'] = (width - labelwidth) / 2
        if self._anchor == tk.CENTER:
            pckKwargs['y'] = (height - labelheight) / 2
        widget.place_forget()
        self.widget.place(**pckKwargs)

    def _getLabelSize(self, label):
        import tkFont
        if not self.isAdded(): return
        widget = self.widget
        width, height = self.cget('width'), self.cget('height')
        styleName = widget.cget('style')
        s = ttk.Style()
        fontstr = s.lookup(styleName, 'font')
        if fontstr in tkFont.names():
            tkfont = tkFont.nametofont(fontstr)
        else:
            pattern = '\{*(?P<family>[^-0-9}]+)\}* (?P<size>[-0-9]+) (?P<weight>[a-z]+)' \
                      '(?:.+?(?P<slant>[a-z]+).+?(?P<underline>[01]+).+?(?P<overstrike>[01]+))*'
            if not re.match(pattern, fontstr):
                kwargs = {'family':'Roman', 'size':'16'}
            else:
                kwargs = re.match(pattern, fontstr).groupdict()
            for key in kwargs.keys():
                if not kwargs[key]: kwargs.pop(key)
            tkfont = tkFont.Font(**kwargs)
        labelwidth = tkfont.measure(label)
        labelheight = tkfont.cget('size')
        if labelheight < 0:
            labelheight = -labelheight
        else:
            labelheight = int(labelheight*widget.winfo_fpixels('1i')/72.0)
        return (labelwidth, labelheight)

    def _getId(self):
        return str(self)


#noinspection PyUnusedLocal
class ControlLabel(ControlBase, Control):

    """
    ControlLabel class.
    Creates a text label.
    """

    def __init__(self, x, y, width, height, label, font=None, textColor=None, disabledColor=None, _alignment=None,
                 hasPath=None, angle=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        label: string or unicode - text string.
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled label's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled label's label. (e.g. '0xFFFF3300')
        alignment: integer - alignment of label - *Note, see xbfont.h
        hasPath: bool - True=stores a path / False=no path.
        angle: integer - angle of control. (+ rotates CCW, - rotates CW)"

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.label = xbmcgui.ControlLabel(100, 250, 125, 75, 'Status', angle=45)
        """
        ControlBase.__init__(self)
        self._labelVar = lblvar = tk.StringVar()
        self.hasPath = hasPath
        self._setAlignment(_alignment)

        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        self._type = 'Label'
        s = ttk.Style()
        styleName = self._getId() + '.TLabel'
        kw = dict(anchor=self._yalignment, justify=self._xalignment,font=font, foreground=textColor)
        kw = self._fltKw(kw)
        s.configure(styleName, **kw)
        kw = dict(foreground=[('disabled', disabledColor)])
        kw = self._fltKw(kw)
        if kw: s.map(styleName, **kw)
        self._kwargs = dict(textvariable=lblvar, style=styleName)
        self._bind = ['setLabel', label]
        pass

    def setLabel(self, label):
        """Set's text for this label.

        label: string or unicode - text string.
        """
        if self.isAdded():
            self.label = xlabel = label
            labelsize = self._getLabelSize(xlabel)
            if self.hasPath and labelsize[0] > self.width:
                xlabel = os.path.join(os.path.splitdrive(label)[0], os.sep, '..', os.path.basename(label))
                labelsize = self._getLabelSize(xlabel)
            self._labelVar.set(xlabel)
        else:
            self._bind = [['setLabel', label]]
        pass

    def getLabel(self):
        """Returns the text value for this label."""
        if self.isAdded(): return self.label
        return self._bind[0][1]


#noinspection PyUnusedLocal
class ControlTextBox(ControlBase, Control):

    """
    ControlTextBox class.
    Creates a box for multi-line text.
    """

    def __init__(self, x, y, width, height, font=None, textColor=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        font: string - font used for text. (e.g. 'font13')
        textColor: hexstring - color of textbox's text. (e.g. '0xFFFFFFFF')

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.textbox = xbmcgui.ControlTextBox(100, 250, 300, 300, textColor='0xFFFFFFFF')
        """
        ControlBase.__init__(self)
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)
        # self.pack_propagate(False)
        self._type = 'Text'
        self._kwargs = dict(foreground=textColor, font=font, state=tk.DISABLED, )
        # self.widget = tk.Text(self, foreground=textColor, font=font, state=tk.DISABLED)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        pass

    def setText(self, text):
        """Set's the text for this textbox.

        text: string or unicode - text string.
        """
        if self.isAdded():
            self.widget.configure(state=tk.NORMAL)
            self.reset()
            self.widget.insert('1.0', text)
            self.widget.configure(state=tk.DISABLED)
        else:
            self._binds = [['insert', '1.0', text]]
        pass

    def scroll(self, position):
        """Scrolls to the given position.

        id: integer - position to scroll to.
        """
        if not self.isAdded(): return
        oldState = self.widget.cget('state')
        self.widget.configure(state=tk.NORMAL)
        self.widget.yview_scroll(position, tk.UNITS)
        self.widget.configure(state=oldState)
        pass

    def reset(self):
        """Clear's this textbox."""
        if self.isAdded():
            oldState = self.widget.cget('state')
            self.widget.configure(state=tk.NORMAL)
            self.widget.delete('1.0', tk.END)
            self.widget.configure(state=oldState)
        else:
            self._binds = [['insert', '1.0', '']]
        pass

#noinspection PyUnusedLocal
class ControlButton(ControlBase, Control):

    """
    ControlButton class.
    Creates a clickable button.
    """

    def __init__(self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, textOffsetX=None,
                 textOffsetY=None, alignment=None, font=None, textColor=None, disabledColor=None, angle=None,
                 shadowColor=None, focusedColor=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        label: string or unicode - text string.
        focusTexture: string - filename for focus texture.
        noFocusTexture: string - filename for no focus texture.
        textOffsetX: integer - x offset of label.
        textOffsetY: integer - y offset of label.
        alignment: integer - alignment of label - *Note, see xbfont.h
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled button's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled button's label. (e.g. '0xFFFF3300')
        angle: integer - angle of control. (+ rotates CCW, - rotates CW)
        shadowColor: hexstring - color of button's label's shadow. (e.g. '0xFF000000')
        focusedColor: hexstring - color of focused button's label. (e.g. '0xFF00FFFF')

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.button = xbmcgui.ControlButton(100, 250, 200, 50, 'Status', font='font14')
        """
        ControlBase.__init__(self)

        self._labelVar = lblvar = tk.StringVar()
        self._setAlignment(alignment)
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        width, height = self.getWidth(), self.getHeight()
        '''
        Falta por integerar
        angle = None,
        shadowColor = None,:
        '''

        # ControlBase.__init__(self, width=width, height=height)
        # self.pack_propagate(False)

        styleName = self._getId() + '.TButton'
        s = ttk.Style()
        kw = self._fltKw(dict(padding=(textOffsetX or 0, textOffsetY or 0),
                              anchor=self._yalignment,
                              justify=self._xalignment,
                              relief=tk.FLAT))
        s.configure(styleName, **kw)
        self._type = 'Button'
        self._kwargs = dict(textvariable=lblvar, style=styleName, compound=tk.BOTTOM)
        # self.widget = ttk.Button(self, textvariable=lblvar, style=styleName, compound=tk.BOTTOM)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        if noFocusTexture:
            self._binds.append(['bind', '<Leave>', lambda x: self._setTexture(noFocusTexture)])
            # self.widget.bind('<Leave>', lambda x: self._setTexture(noFocusTexture))
        if focusTexture:
            self._binds.append(['bind', '<Enter>', lambda x: self._setTexture(focusTexture)])
            # self.widget.bind('<Enter>', lambda x: self._setTexture(focusTexture))

        self._binds.append(['setLabel', label, font, textColor, disabledColor, shadowColor, focusedColor])
        # self.setLabel(label, font, textColor, disabledColor, shadowColor, focusedColor)

        pass

    def setDisabledColor(self, disabledColor):
        """Set's this buttons disabled color.

        disabledColor: hexstring - color of disabled button's label. (e.g. '0xFFFF3300')
        """
        if self.isAdded():
            styleName = self.widget.cget('style')
            s = ttk.Style()
            changes = [elem for elem in s.map(styleName, 'foreground') if not (elem[0] == 'disable' and len(elem) == 2)]
            changes.append(('disabled', disabledColor))
            s.map(styleName, foreground=changes)
        else:
            self._binds.append('setDisabledColor', disabledColor)
        pass

    def setLabel(self, label=None, font=None, textColor=None, disabledColor=None, shadowColor=None, focusedColor=None):
        """Set's this buttons text attributes.

        label: string or unicode - text string.
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled button's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled button's label. (e.g. '0xFFFF3300')
        shadowColor: hexstring - color of button's label's shadow. (e.g. '0xFF000000')
        focusedColor: hexstring - color of focused button's label. (e.g. '0xFFFFFF00')
        label2: string or unicode - text string.

        Example:
            self.button.setLabel('Status', 'font14', '0xFFFFFFFF', '0xFFFF3300', '0xFF000000')
        """
        if self.isAdded():
            styleName = self.widget.cget('style')
            kw = self._fltKw(dict(font=font, foreground=textColor))
            s = ttk.Style()
            s.configure(styleName,**kw)
            kw = self._fltKw(dict(foreground=[('focus', focusedColor), ('disabled', disabledColor), ('!active', disabledColor)]))
            if kw: s.map(styleName, **kw)
            self._labelVar.set(label)
        else:
            self._binds.append(['setLabel', label, font, textColor, disabledColor, shadowColor, focusedColor])
        pass

    def getLabel(self):
        """Returns the buttons label as a unicode string."""
        if self.isAdded():
            return self.widget.cget('text')
        else:
            for elem in self._binds:
                if not elem[0] == 'setLabel': continue
                label = elem[1]
            else:
                label = ''
            return label

    def getLabel2(self):
        """Returns the buttons label2 as a unicode string."""
        return unicode


#noinspection PyUnusedLocal
class ControlCheckMark(ControlBase, Control):

    """
    ControlCheckMark class.
    Creates a checkmark with 2 states.
    """

    def __init__(self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, checkWidth=None,
                 checkHeight=None, _alignment=None, font=None, textColor=None, disabledColor=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        label: string or unicode - text string.

        focusTexture: string - filename for focus texture.
        noFocusTexture: string - filename for no focus texture.
        checkWidth: integer - width of checkmark.
        checkHeight: integer - height of checkmark.
        _alignment: integer - alignment of label - *Note, see xbfont.h
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled checkmark's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled checkmark's label. (e.g. '0xFFFF3300')

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.checkmark = xbmcgui.ControlCheckMark(100, 250, 200, 50, 'Status', font='font14')
        """
        ControlBase.__init__(self)

        '''
        not implemented
        label, f checkWidth=None,
                 checkHeight=None, font=None, textColor=None, disabledColor=None
        '''

        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)
        self._setAlignment(_alignment)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)

        self.intvar = intvar = tk.IntVar()
        styleName = self._getId() + '.TCheckbutton'
        s = ttk.Style()
        s.configure(styleName,
                    anchor=self._yalignment,
                    justify=self._xalignment)
        self._type = 'Checkbutton'
        self._kwargs = dict(variable=intvar, style=styleName)
        # self.widget = ttk.Checkbutton(self, variable=intvar, style=styleName)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        self._binds.append(['instate', 'focus', self._setTexture, focusTexture])
        self._binds.append(['instate', '!focus', self._setTexture, noFocusTexture])
        # self.widget.instate('focus', self._setTexture, focusTexture)
        # self.widget.instate('!focus', self._setTexture, noFocusTexture)

        # self.setLabel(label, font, textColor, disabledColor)
        self._binds(['setLabel', label, font, textColor, disabledColor])
        pass

    def setDisabledColor(self, disabledColor):
        """Set's this controls disabled color.

        disabledColor: hexstring - color of disabled checkmark's label. (e.g. '0xFFFF3300')
        """
        if self.isAdded():
            self.widget.config(disabledforeground=disabledColor)
        else:
            self._binds.append(['setDisabledColor', disabledColor])
        pass

    def setLabel(self, label, font=None, textColor=None, disabledColor=None):
        """Set's this controls text attributes.

        label: string or unicode - text string.
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled checkmark's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled checkmark's label. (e.g. '0xFFFF3300')

        Example:
            self.checkmark.setLabel('Status', 'font14', '0xFFFFFFFF', '0xFFFF3300')
        """
        if self.isAdded():
            styleName = self.widget.cget('style')
            s = ttk.Style()
            s.configure(styleName,
                        font=font,
                        foreground=textColor)
            s.map(styleName,
                  foreground=[('disabled', disabledColor)])
            self.widget.configure(text=label)
        else:
            self._binds.append(['setLabel', label, font, textColor, disabledColor])
        pass

    def getSelected(self):
        """Returns the selected status for this checkmark as a bool."""
        return bool(self.intvar.get())

    def setSelected(self, isOn):
        """Sets this checkmark status to on or off.

        isOn: bool - True=selected (on) / False=not selected (off)
        """
        self.intvar.set(int(isOn))
        pass

# noinspection PyUnusedLocal
class ControlRadioButton(tk.Radiobutton, Control):
    """
    ControlRadioButton class.
    Creates a radio-button with 2 states.
    """

    def __init__(self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, textOffsetX=None,
                 textOffsetY=None, _alignment=None, font=None, textColor=None, disabledColor=None, angle=None,
                 shadowColor=None, focusedColor=None, focusOnTexture=None, noFocusOnTexture=None,
                 focusOffTexture=None, noFocusOffTexture=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        label: string or unicode - text string.
        focusTexture: string - filename for focus texture.
        noFocusTexture: string - filename for no focus texture.
        textOffsetX: integer - x offset of label.
        textOffsetY: integer - y offset of label.
        _alignment: integer - alignment of label - *Note, see xbfont.h
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled radio button's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled radio button's label. (e.g. '0xFFFF3300')
        angle: integer - angle of control. (+ rotates CCW, - rotates CW)
        shadowColor: hexstring - color of radio button's label's shadow. (e.g. '0xFF000000')
        focusedColor: hexstring - color of focused radio button's label. (e.g. '0xFF00FFFF')
        focusOnTexture: string - filename for radio focused/checked texture.
        noFocusOnTexture: string - filename for radio not focused/checked texture.
        focusOffTexture: string - filename for radio focused/unchecked texture.
        noFocusOffTexture: string - filename for radio not focused/unchecked texture.
        Note: To customize RadioButton all 4 abovementioned textures need to be provided.
        focus and noFocus textures can be the same.

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.radiobutton = xbmcgui.ControlRadioButton(100, 250, 200, 50, 'Status', font='font14')
        """
        ControlBase.__init__(self)

        '''
        x, y, width, height, label, focusTexture=None, noFocusTexture=None, textOffsetX=None,
                 textOffsetY=None, _alignment=None, font=None, textColor=None, disabledColor=None, angle=None,
                 shadowColor=None, focusedColor=None, focusOnTexture=None, noFocusOnTexture=None,
                 focusOffTexture=None, noFocusOffTexture=None
        '''
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)
        self._setAlignment(_alignment)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)

        self.intvar = intvar = tk.IntVar()

        styleName = self._getId() + '.TRadiobutton'
        s = ttk.Style()
        s.configure(styleName,
                    anchor=self._yalignment,
                    justify=self._xalignment)

        self._type = 'RadioButton'
        self._kwargs = dict(variable=intvar, style=styleName)
        self._binds.append(['instate', 'focus', self._setTexture, focusTexture])
        self._binds.append(['instate', '!focus', self._setTexture, noFocusTexture])

        # self.widget = ttk.Radiobutton(self, variable=intvar, style=styleName)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        # self.widget.instate('focus', self._setTexture, focusTexture)
        # self.widget.instate('!focus', self._setTexture, noFocusTexture)

        # self.setLabel(label, font, textColor, disabledColor, shadowColor, focusedColor)
        self._binds.append(['setLabel', label, font, textColor, disabledColor, shadowColor, focusedColor])

        pass

    def setSelected(self, selected):
        """Sets the radio buttons's selected status.

        selected: bool - True=selected (on) / False=not selected (off)
        """
        self.intvar.set(int(selected))
        pass


    def isSelected(self):
        """Returns the radio buttons's selected status."""
        return bool(self.intvar.get())

    def setLabel(self, label, font=None, textColor=None, disabledColor=None, shadowColor=None, focusedColor=None):
        """Set's the radio buttons text attributes.

        label: string or unicode - text string.
        font: string - font used for label text. (e.g. 'font13')
        textColor: hexstring - color of enabled radio button's label. (e.g. '0xFFFFFFFF')
        disabledColor: hexstring - color of disabled radio button's label. (e.g. '0xFFFF3300')
        shadowColor: hexstring - color of radio button's label's shadow. (e.g. '0xFF000000')
        focusedColor: hexstring - color of focused radio button's label. (e.g. '0xFFFFFF00')

        Example:
            self.radiobutton.setLabel('Status', 'font14', '0xFFFFFFFF', '0xFFFF3300', '0xFF000000')
        """
        if self.isAdded():
            styleName = self.widget.cget('style')
            s = ttk.Style()
            s.configure(styleName,
                        font=font,
                        foreground=textColor)
            s.map(styleName,
                  foreground=[('disabled', disabledColor), ('focus', focusedColor)])
            self.widget.configure(text=label)
        else:
            self._binds.append(['setLabel', label, font, textColor, disabledColor, shadowColor, focusedColor])
        pass

    def setRadioDimension(self, x, y, width, height):
        """Sets the radio buttons's radio texture's position and size.

        x: integer - x coordinate of radio texture.
        y: integer - y coordinate of radio texture.
        width: integer - width of radio texture.
        height: integer - height of radio texture.

        Example:
            self.radiobutton.setRadioDimension(x=100, y=5, width=20, height=20)
        """
        pass

#noinspection PyUnusedLocal
class ControlImage(ControlBase, Control):

    """
    ControlImage class.
    Displays an image from a file.
    """

    def __init__(self, x, y, width, height, filename, colorKey=None, aspectRatio=None, colorDiffuse=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        filename: string - image filename.
        colorKey: hexString - (example, '0xFFFF3300')
        aspectRatio: integer - (values 0 = stretch (default), 1 = scale up (crops), 2 = scale down (black bars)
        colorDiffuse: hexString - (example, '0xC0FF0000' (red tint)).

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.image = xbmcgui.ControlImage(100, 250, 125, 75, aspectRatio=2)
        """
        ControlBase.__init__(self)
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)
        self.colorKey = colorKey
        self.aspectRatio = aspectRatio or 0
        self.setColorDiffuse(colorDiffuse)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)

        styleName = self._getId() + '.TLabel'
        s = ttk.Style()
        s.configure(styleName)

        self._type = 'Label'
        self._kwargs = dict(style=styleName)
        # self.widget = ttk.Label(self, style=styleName)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)

        # self.setImage(filename)
        self._binds.append(['setImage', filename])
        pass

    def setImage(self, filename):
        """Changes the image.

        filename: string - image filename.
        """
        if not self.isAdded():
            self._binds.append(['setImage', filename])
            return
        from PIL import Image
        import ImageTk
        width, height = self.getWidth(), self.getHeight()
        self.image = image = Image.open(filename)
        self.imagetk = ImageTk.PhotoImage(image.mode, (width, height))
        if self.aspectRatio == 0:           # stretch
            imagetk = image.resize((width, height))
        elif self.aspectRatio == 1:         # crop
            imagetk = image.crop((0, 0, width, height))
        else:                               # scale down
            image.thumbnail((width, height))
            imagetk = image
        self.image = imagetk
        self.imagetk.paste(imagetk, (0, 0, width, height))

        styleName = self.widget.cget('style')
        s = ttk.Style()
        s.configure(styleName,
                    image=self.imagetk)
        pass

    def setColorDiffuse(self, colorDiffuse):
        """Changes the images color.

        colorDiffuse: hexString - (example, '0xC0FF0000' (red tint)).
        """
        self.ColorDiffuse = colorDiffuse
        pass

#noinspection PyUnusedLocal
class ControlProgress(ControlBase, Control):

    """
    ControlProgress class.
    """

    def __init__(self, x, y, width, height, texturebg=None, textureleft=None, texturemid=None, textureright=None,
                 textureoverlay=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        texturebg: string - image filename.
        textureleft: string - image filename.
        texturemid: string - image filename.
        textureright: string - image filename.
        textureoverlay: string - image filename.

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.progress = xbmcgui.ControlProgress(100, 250, 125, 75)
        """
        ControlBase.__init__(self)

        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)

        self.dblvar = dblvar = tk.DoubleVar()

        styleName = self._getId() + '.Horizontal.TProgressbar'
        s = ttk.Style()
        s.configure(styleName)
        self._type = 'Progressbar'
        self._kwargs = dict(variable=dblvar, mode='determinate', orient=tk.HORIZONTAL, style=styleName)
        # self.widget = ttk.Progressbar(self, variable=dblvar, mode='determinate', orient=tk.HORIZONTAL, style=styleName)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        pass

    def setPercent(self, percent):
        """Sets the percentage of the progressbar to show.

        percent: float - percentage of the bar to show.

        Note:
            Valid range for percent is 0-100.
        """
        if not self.isAdded():
            self._binds.append(['setPercent', percent])
            return
        lstPercent = self.getPercent()
        delta = percent - lstPercent
        self.widget.step(delta)
        pass

    def getPercent(self):
        """Returns a float of the percent of the progress."""
        return self.dblvar.get()

#noinspection PyUnusedLocal
class ControlGroup(ControlBase, Control):

    """ControlGroup class."""

    def __init__(self, x, y, width, height):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.

        Example:
        self.group = xbmcgui.ControlGroup(100, 250, 125, 75)
        """
        ControlBase.__init__(self)

        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)

        self._type = 'LabelFrame'
        self._kwargs = dict(borderwidth=2)
        # self.widget = ttk.LabelFrame(borderwidth=2)
        pass

#noinspection PyUnusedLocal
class ControlSlider(Control):

    """
    ControlSlider class.
    Creates a slider.
    """

    def __init__(self, x, y, width, height, textureback=None, texture=None, texturefocus=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        textureback: string - image filename.
        texture: string - image filename.
        texturefocus: string - image filename.

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.slider = xbmcgui.ControlSlider(100, 250, 350, 40)
        """
        ControlBase.__init__(self)

        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        # width, height = self.getWidth(), self.getHeight()
        # ControlBase.__init__(self, width=width, height=height)

        self.dblvar = dblvar = tk.DoubleVar()

        styleName = self._getId() + '.Horizontal.TScale'
        s = ttk.Style()
        s.configure(styleName)

        self._type = 'Scale'
        self._kwargs = dict(from_=0.0, to=100.0, length=300, variable=dblvar, orient=tk.HORIZONTAL, style=styleName)
        # self.widget = ttk.Scale(self, from_=0.0, to=100.0, length=300, variable=dblvar, orient=tk.HORIZONTAL, style=styleName)
        # self.widget.pack(fill=tk.BOTH, expand=tk.YES)
        pass

    def getPercent(self):
        """Returns a float of the percent of the slider."""
        return self.dblvar.get()

    def setPercent(self, percent):
        """Sets the percent of the slider."""
        self.dblvar.set(percent)
        pass

#noinspection PyUnusedLocal
class ControlList(Control):

    """
    ControlList class.
    Creates a list of items.
    """

    def __init__(self, x, y, width, height, font=None, textColor=None, buttonTexture=None, buttonFocusTexture=None,
                 selectedColor=None, _imageWidth=None, _imageHeight=None, _itemTextXOffset=None, _itemTextYOffset=None,
                 _itemHeight=None, _space=None, _alignmentY=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.
        font: string - font used for items label. (e.g. 'font13')
        textColor: hexstring - color of items label. (e.g. '0xFFFFFFFF')
        buttonTexture: string - filename for no focus texture.
        buttonFocusTexture: string - filename for focus texture.
        selectedColor: integer - x offset of label.
        _imageWidth: integer - width of items icon or thumbnail.
        _imageHeight: integer - height of items icon or thumbnail.
        _itemTextXOffset: integer - x offset of items label.
        _itemTextYOffset: integer - y offset of items label.
        _itemHeight: integer - height of items.
        _space: integer - space between items.
        _alignmentY: integer - Y-axis alignment of items label - *Note, see xbfont.h

        Note:
            After you create the control, you need to add it to the window with addControl().

        Example:
            self.cList = xbmcgui.ControlList(100, 250, 200, 250, 'font14', space=5)
        """
        pass

    def addItem(self, item):
        """Add a new item to this list control.

        item: string, unicode or ListItem - item to add.
        """
        pass

    def addItems(self, items):
        """Adds a list of listitems or strings to this list control.

        items: List - list of strings, unicode objects or ListItems to add.
        """
        pass

    def selectItem(self, item):
        """Select an item by index number.

        item: integer - index number of the item to select.
        """
        pass

    def reset(self):
        """Clear all ListItems in this control list."""
        pass

    def getSpinControl(self):
        """Returns the associated ControlSpin object.

        Note:
            Not working completely yet -
            After adding this control list to a window it is not possible to change
            the settings of this spin control.
        """
        return object

    def setImageDimensions(self, imageWidth=None, imageHeight=None):
        """Sets the width/height of items icon or thumbnail.

        imageWidth: integer - width of items icon or thumbnail.
        imageHeight: integer - height of items icon or thumbnail.
        """
        pass

    def setItemHeight(self, itemHeight):
        """Sets the height of items.

        itemHeight: integer - height of items.
        """
        pass

    def setPageControlVisible(self, visible):
        """Sets the spin control's visible/hidden state.

        visible: boolean - True=visible / False=hidden.
        """
        pass

    def setSpace(self, space=None):
        """Set's the space between items.

        space: integer - space between items.
        """
        pass

    def getSelectedPosition(self):
        """Returns the position of the selected item as an integer.

        Note:
            Returns -1 for empty lists.
        """
        return int

    def getSelectedItem(self):
        """Returns the selected item as a ListItem object.

        Note:
            Same as getSelectedPosition(), but instead of an integer a ListItem object is returned. Returns None for empty lists.
            See windowexample.py on how to use this.
        """
        return              #ListItem

    def size(self):
        """Returns the total number of items in this list control as an integer."""
        return long

    def getListItem(self, index):
        """Returns a given ListItem in this List.

        index: integer - index number of item to return.

        Raises:
            ValueError: If index is out of range.
        """
        return              #ListItem

    def getItemHeight(self):
        """Returns the control's current item height as an integer."""
        return long

    def getSpace(self):
        """Returns the control's space between items as an integer."""
        return long

    def setStaticContent(self, items):
        """Fills a static list with a list of listitems.

        items: List - list of listitems to add.
        """
        pass

    def removeItem(self, index):
        """
        Remove an item by index number.
        index : integer - index number of the item to remove.
        example:
        my_list.removeItem(12)
        """
        pass


from xbmcConstants import getActionStr

class mytestWindowXML(WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.pf = open('c:/testFiles/wndTestOut.txt', 'w')
        self.pf.write('\n' + '__init__: ' + str(args) + ' ' + str(kwargs))
        WindowXMLDialog.__init__(self, *args, **kwargs)
        pass

    def addControl(self, control):
        ctrClass = control.__class__
        ctrlId = control.getId()
        self.pf.write('\naddControl: Control: %s CtrlClass: %s CtrlId: %s' % (str(control), ctrClass, ctrlId))
        WindowXMLDialog.addControl(self, control)

    def setFocus(self, ctrlId):
        control = self.getControl(ctrlId)
        ctrClass = control.__class__
        self.pf.write('\n' + 'setFocus: ' + str(ctrlId))
        WindowXMLDialog.setFocus(self, ctrlId)

    def onClose(self):
        self.pf.close()
        self.close()

    def onAction(self, action):
        actionID = action.getId()
        actionName = getActionStr(actionID)
        btCode = action.getButtonCode()
        self.pf.write('\nonActionId: %s Action: %s ButtonCode: %s' % (actionID, actionName, btCode))
        if actionName in ['ACTION_PARENT_DIR', 'ACTION_PREVIOUS_MENU', 'ACTION_NAV_BACK', 'ACTION_X']:
            self.onClose()
        elif actionName in ['ACTION_MOVE_UP', 'ACTION_MOVE_RIGHT', 'ACTION_MOVE_DOWN', 'ACTION_MOVE_LEFT']:
            try:
                ctrl = self.getFocus()
            except Exception as e:
                self.pf.write('\nActionName: %s ButtonCode: %s ErrMsg: %s ' % (actionName, btCode, str(e)))
            else:
                ctrlId = ctrl.getId()
                self.pf.write('\nActionName: %s ButtonCode: %s CtrlClass: %s CtrlId: %s' % (actionName, btCode, ctrl.__class__, ctrlId))

    def onClick(self, ctrlId):
        control = self.getControl(ctrlId)
        ctrClass = control.__class__
        self.pf.write('\nOnClick: Control: %s CtrlClass: %s CtrlId: %s' % (str(control), ctrClass, ctrlId))

        pass

    def onDoubleClick(self, *args, **kwargs):
        self.pf.write('\n' + 'onDoubleClick: ' + str(args) + ' ' + str(kwargs))
        pass

    def onControl(self, control):
        ctrClass = control.__class__
        ctrlId = control.getId()
        self.pf.write('\nOnControl: Control: %s CtrlClass: %s CtrlId: %s' % (str(control), ctrClass, ctrlId))
        pass

    def onFocus(self, ctrlId):
        control = self.getControl(ctrlId)
        ctrClass = control.__class__
        self.pf.write('\nOnFocus: Control: %s CtrlClass: %s CtrlId: %s' % (str(control), ctrClass, ctrlId))
        pass

    def onInit(self, *args, **kwargs):
        self.pf.write('\n' + 'onInit: ' + str(args) + ' ' + str(kwargs))
        pass




if __name__ == '__main__':
    _path = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons\plugin.video.xbmcmodule'
    root = controlXml.AppWindow()
    root.title('AppWindow')
    # root.withdraw()
    wnd = mytestWindowXML('DialogOK.xml', _path)
    wnd.doModal()
    root.mainloop()

    # '''
    #     xbfont_left = 0x00000000
    #     xbfont_right = 0x00000001
    #     xbfont_center_x = 0x00000002
    #     xbfont_center_y = 0x00000004
    # '''
    # import time
    # root = tk.Tk()
    # frame=tk.Frame(height=45, width=45, bg='black').place(x=5, y=300)
    # folder = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons\plugin.image.comicstrips\resources\skins\Default\media'
    # test = ControlButton(5, 670, 45, 45, 'ST',
    #                      textColor = 'black', disabledColor = 'white',
    #                      alignment = 0x00000002 | 0x00000004,
    #                      focusTexture=folder + '/' + 'floor_buttonFO.png',
    #                      noFocusTexture=folder + '/' + 'floor_button.png',
    #                      font='Times 12 bold')
    # test.place(x=5, y=370)

    # label = ControlLabel(0, 0, 400, 40, 'Este es un label (izquierda)', textColor='blue')
    # setattr(label, 'getId', lambda x=23:x)
    # print label.getId()
    # label.place(x=0,y=0)
    # label = ControlLabel(0, 0, 400, 40, 'Este es un label (derechaxx)', font=('Times', -20, 'bold'), textColor='green', _alignment=1)
    # label.place(x=0, y=40)
    # label = ControlLabel(0, 0, 400, 40, 'Este es un label (centroxxx)', font=('Poor Richard', -20, 'bold'), _alignment=2)
    # label.place(x=0, y=80)
    # label = ControlLabel(0, 0, 400, 40, 'Este es un label (centroxyx)', _alignment=6, textColor='red')
    # label.place(x=0, y=120)
    # label = ControlLabel(0, 0, 400, 40, 'c:/uno/dos/tres/cuatro/cinco/seis/siete/ocho/nueve/diez/once/doce.xml', _alignment=6, font=('Times', -20, 'bold'), hasPath=True, textColor='red')
    # label.place(x=0, y=160)
    # text = ControlTextBox(0,0, 200, 40)
    # text.setText('Esto es un texto que estoy escribiendo en este momento para probar que esto fucnciona')
    # text.place(x=0, y=200)
    #
    # check = ControlCheckMark(0, 0, 200, 40, 'checkbutton')
    # check.place(x=0, y=240)
    # # radio = ControlRadioButton(40, 60, 80, 3, 'pruebaradio')
    # # radio.place(x=0, y=0)
    # filename = r'c:\testFiles\headerVeoCineX.png'
    # image = ControlImage(0, 0, 400, 200, filename, aspectRatio=0)
    # image.place(x = 400, y=0)

    # '''
    # Prueba del ControlButton
    # '''
    # root = tk.Tk()
    #
    # folder = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons\plugin.image.comicstrips\resources\skins\Default\media'
    # param = [('focusTexture', folder + '/' + 'floor_buttonFO.png'),
    #          ('noFocusTexture', folder + '/' + 'floor_button.png'),
    #          ('disabledColor', 'grey'),
    #          ('textColor', 'green'),
    #          # ('textOffsetX', 50),
    #          # ('textOffsetY', 40),
    #          ('alignment', 0x00000004 | 0x00000001),
    #          ('font', 'Roman 20 bold'),
    #          ('angle', 45),
    #          ('shadowColor', 'FFFFFF'),
    #          ('focusedColor', '32CD32')
    #          ]
    #
    # for k in range(len(param)):
    #     kw = dict(param[:k])
    #     x = 5 + 100 * (k / 8)
    #     y = 5 + 85 * (k % 8)
    #     boton = ControlButton(x, y, 100, 80, 'Status' + str(k), **kw)
    #     boton.place(x=x, y=y)
    #
    # root.mainloop()