import Tkinter as tk
import copy
import os
import sys
import tkSimpleDialog

from fromC import ButtonTranslator
from fromC.Keytable import VK, NAME, lookup
from PIL import Image, ImageTk

import controlXml
import guiTop
from guiTop import WindowBase
from KodiAddonIDE.KodiStubs.fromC import WindowIDs
from KodiAddonIDE.KodiStubs.fromC.key import *
from KodiAddonIDE.KodiStubs.fromC.ButtonTranslator import windows
from KodiAddonIDE.KodiStubs.xbmcModules.xbmcgui import ListItem


class Window(WindowBase):

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
        root = guiTop.AppWindow()
        if windowId != -1:
            return root.getWindowFromId(windowId)
        super(Window, self).__init__()
        self.windowId = windowId
        self.wndfile = ''
        self._resolution = 1
        self.withIdControls = {}
        self.noIdControls = []
        root.mapWindow(self)
        self.wndId = windowId
        self._setGUI(root)
        self.clearProperties()
        pass

    def _mapControl(self, control):
        ctrlId = control.getId()
        if ctrlId:
            self.withIdControls[ctrlId] = control
        else:
            self.noIdControls.append(control)

    def _setGUI(self, root):
        # vbar = tk.Scrollbar(root)
        # hbar = tk.Scrollbar(root, orient='horizontal')
        # vbar.pack(side=tk.RIGHT, fill=tk.Y)
        # hbar.pack(side=tk.BOTTOM, fill=tk.X)
        w, h = self.getWidth(), self.getHeight()
        self.focus = grpRoot = ControlGroup(0, 0, w, h)
        grpRoot._isSelected = True
        grpRoot.master = self
        grpRoot._wdgID = 0
        self.wndTk = wndTk = tk.Toplevel(root)
        # self.wndTk.overrideredirect(1)
        self.wndTk.transient(root)
        # self.wndTk.attributes('-fullscreen', True)
        grpRoot.widget = canvas = tk.Canvas(wndTk, width=w, height=h, highlightthickness=0, bd=0, bg='black', takefocus=1, scrollregion=(0, 0, 10*w, 10*h))
        self._setWidgetBinds()
        canvas.pack()

    def show(self):
        """Show this window.

        Shows this window by activating it, calling close() after it wil activate the current window again.

        Note:
            If your script ends this window will be closed to. To show it forever,
            make a loop at the end of your script and use doModal() instead.
        """
        self.wndTk.grab_set()
        self.wndTk.focus_set()
        self.wndTk.mainloop()
        pass

    def close(self):
        """Closes this window.

        Closes this window by activating the old window.
        The window is not deleted with this method.
        """
        self.wndTk.destroy()
        pass

    def onAction(self, action):
        """onAction method.

        This method will recieve all actions that the main program will send to this window.
        By default, only the PREVIOUS_MENU action is handled.
        Overwrite this method to let your script handle all actions.
        Don't forget to capture ACTION_PREVIOUS_MENU, else the user can't close this window.
        """
        if action == ACTION_PREVIOUS_MENU:
            self.close()
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
        wndTk = self.wndTk
        wndTk.grab_set()
        wndTk.focus_set()
        wndTk.protocol("WM_DELETE_WINDOW", self.close)
        wndTk.wait_window(wndTk)
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
        self.addControls([control])
        pass

    def addControls(self, controls):
        """
        addControls(self, List)--Add a list of Controls to this window.

        *Throws:
        - TypeError, if supplied argument is not ofList type, or a control is not ofControl type
        - ReferenceError, if control is already used in another window
        - RuntimeError, should not happen :-)
        """
        if not isinstance(controls, list): raise TypeError('The argument supplied is not of List type')
        focusedWdg = self.getFocus()
        container = focusedWdg if isinstance(focusedWdg, ControlGroup) else focusedWdg.master
        for control in controls:
            self._registerControl(control)
            self._mapControl(control)

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
        control = self.withIdControls.get(controlId)
        if not control: raise RuntimeError('Control is not added to this window')
        return control

    def setFocus(self, control=None):
        """Give the supplied control focus.

        Raises:
            TypeError: If supplied argument is not a Control type.
            SystemError: On Internal error.
            RuntimeError: If control is not added to a window.
        """
        control = control or self.focus
        if not isinstance(control, Control): raise TypeError('The supplied control is not a Control type')
        if not control._wdgID: raise RuntimeError('The control is not added to a window')
        master = control.master
        self._onEnter(None, control)


    def setFocusId(self, id):
        """Gives the control with the supplied focus.

        Raises:
            SystemError: On Internal error.
            RuntimeError: If control is not added to a window.
        """
        control = self.getControl(id)
        if not control: raise RuntimeError('The control with the supplied id is not mapped in this window')
        self.setFocus(control)
        pass

    def getFocus(self):
        """Returns the control which is focused.

        Raises:
            SystemError: On Internal error.
            RuntimeError: If no control has focus.
        """
        focusWdg = self.focus
        while True:
            focus = focusWdg.focus
            if not focus or not focus._isSelected: break
            focusWdg = focus
            if not isinstance(focusWdg, ControlGroup): break
        return focusWdg

    def getFocusId(self):
        """Returns the id of the control which is focused.

        Raises:
            SystemError: On Internal error.
            RuntimeError: If no control has focus.
        """
        control = self.getFocus()
        return control.getId()

    def removeControl(self, control):
        """Removes the control from this window.

        Raises:
            TypeError: If supplied argument is not a Control type.
            RuntimeError: If control is not added to this window.

        This will not delete the control. It is only removed from the window.
        """
        self.removeControls([control])
        pass

    def removeControls(self, controls):
        for ctrl in controls:
            ctrlId = ctrl.getId()
            if ctrlId:
                self.withIdControls.pop(ctrlId)
            else:
                self.noIdControls.pop(ctrl)
        for ctrl in self.noIdControls + self.withIdControls.values():
            navMap = ctrl.navMap
            for key in navMap:
                if navMap[key] in controls: navMap.pop(key)
        for ctrl in controls:
            del ctrl
        pass

    def getHeight(self):
        """Returns the height of this screen."""
        root = guiTop.AppWindow()
        return root.winfo_screenheight()

    def getWidth(self):
        """Returns the width of this screen."""
        root = guiTop.AppWindow()
        return root.winfo_screenwidth()

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
        height = self.getHeight()
        width = self.getWidth()
        if width >= 1920 and height >= 1080: return 0
        if width >= 1280 and height >= 720: return 1
        if width == 720 and height == 480: return 2
        if width == 720 and height == 576: return 6
        if width == 720 and height == 480: return 8


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
        self._resolution = resolution
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
        return self.properties.get(key)

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
        self.properties= {}
        pass


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
        wndfile = os.path.splitext(xmlFilename.lower())[0]
        self.wndfile = wndfile
        if wndfile in windows.keys():
            self.windowId = windows[wndfile]
        window, controls = controlXml.getRoots(xmlFilename, scriptPath, defaultSkin, defaultRes)
        wndList = controlXml.processRoot(window)
        xorig = yorig = 0
        for elem in wndList:
            for key in ['CHILDREN', 'ID', 'MASTERID']:
                elem.pop(key, None)
            elem_tag = elem.pop('elem_tag')
            if elem_tag == 'window':
                self._window = elem
            elif elem_tag == 'coordinates':
                xorig = elem.get('left', 0)
                yorig = elem.get('top', 0)
        ctrList = controlXml.processRoot(controls)
        masterW, masterH = self.getWidth(), self.getHeight()
        scrResW, scrResH = controlXml.coordResolution[defaultRes or '720p']
        if (scrResW*masterH)/scrResH > masterW:
            h = (scrResH*masterW)/scrResW
            deltaX, deltaY = 0, (masterH - h)/2
            masterH = h
        else:
            w = (scrResW*masterH)/scrResH
            deltaX, deltaY = (masterW - w)/2, 0
            masterW = w

        width, height = controlXml.normControlMap(ctrList, scrResW, scrResH)

        cgrp = self.focus
        cgrp._xorig, cgrp._yorig = (masterW*xorig)/scrResW + deltaX, (masterH*yorig)/scrResH + deltaY
        width,            height = (masterW*width)/scrResW, (masterH*height)/scrResH

        controls = []
        for k in range(len(ctrList)):
            control = relationalTags = None
            if ctrList[k]['elem_tag'] == 'control':
                controlClass, args, kwargs, relationalTags = controlXml.mapControl(k, ctrList)
                for n in [0, 2]: args[n] = (masterW*args[n])/scrResW
                for n in [1, 3]: args[n] = (masterH*args[n])/scrResH
                masterPos = kwargs['_params'].pop('master')
                if masterPos is not None:
                    kwargs['_params']['master'] = controls[masterPos]
                controlClass = getattr(sys.modules[__name__], controlClass)
                control = controlClass(*args, **kwargs)
            controls.append(control)
            ctrList[k] = relationalTags
        self.addControls([ctrl for ctrl in controls if ctrl])
        for control, relationalTags in zip(controls, ctrList):
            if control is None: continue
            navtags = relationalTags['navtags'].items()
            for k in range(len(navtags)):
                key, ctrId = navtags[k]
                ctrId = self.getControl(ctrId)
                navtags[k] = (key[2:], ctrId)
            if navtags: control.setNavigation(**dict(navtags))
        pass

    def removeItem(self, position):
        """Removes a specified item based on position, from the Window List.

        position: integer - position of item to remove.
        """
        pass

    def addItem(self, item, position=32767):
        """Add a new item to this Window List.

        item: string, unicode or ListItem - item to add.
        position: integer - position of item to add. (NO Int = Adds to bottom,0 adds to top, 1 adds to one below from top,-1 adds to one above from bottom etc etc)
                  If integer positions are greater than list size, negative positions will add to top of list, positive positions will add to bottom of list.
        Example:
            self.addItem('Reboot XBMC', 0)
        """
        pass

    def clearList(self):
        """Clear the Window List."""
        pass

    def setCurrentListPosition(self, position):
        """Set the current position in the Window List.

        position: integer - position of item to set.
        """
        pass

    def getCurrentListPosition(self):
        """Gets the current position in the Window List."""
        return long

    def getListItem(self, position):
        """Returns a given ListItem in this Window List.

        position: integer - position of item to return.
        """
        return ListItem

    def getListSize(self):
        """Returns the number of items in this Window List."""
        return long

    def setProperty(self, key, value):
        """Sets a container property, similar to an infolabel.

        key: string - property name.
        value: string or unicode - value of property.

        Note:
            Key is NOT case sensitive.

        Example:
            self.setProperty('Category', 'Newest')
        """
        pass


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
    def __init__(self):
        self.ctrlType = 'widget'
        self._id = None
        self.master = None
        self.wdgImg = None
        self._imgCache  = False
        self._ctrlState = True
        self._isSelected = False
        self._counter = 0
        self._isFocusable = False
        self.navMap = {}
        litem = ListItem()
        self._wdgInfo = guiTop.ListItemWrapper(litem, None, self._setWdgImage)


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
        self._setNavigation('Down', control)
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
        self._setNavigation('Left', control)
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
        self._setNavigation('Right', control)
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
        self._setNavigation('Up', control)
        pass

    def getHeight(self):
        """
        getHeight() --Returns the control's current height as an integer.

        example:
        - height = self.button.getHeight()
        """
        return self._wdgInfo.getProperty('height')

    def getId(self):
        """
        getId() --Returns the control's current id as an integer.

        example:
        - id = self.button.getId()
        """
        return self._id

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
        return self._wdgInfo.getProperty('width')

    def getX(self):
        """
        Get X coordinate of a control as an integer.
        """
        return self._x

    def getY(self):
        """
        Get Y coordinate of a control as an integer.
        """
        return self._y

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
        self._ctrlState = enabled
        self._setWdgImage()
        pass

    def setHeight(self, height):
        """
        setHeight(height)--Set's the controls height.

        height : integer - height of control.

        example:
        - self.image.setHeight(100)
        """
        self._wdgInfo.setProperty('height', height)
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
        if up: self._setNavigation('Up', up)
        if down: self._setNavigation('Down', down)
        if left: self._setNavigation('Left', left)
        if right: self._setNavigation('Right', right)
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
        self._x = x
        self._y = y
        pass

    def setVisible(self, visible):
        """
        setVisible(visible)--Set's the control's visible/hidden state.

        visible : bool - True=visible / False=hidden.

        example:
        - self.button.setVisible(False)
        """
        # if visible: self.pack()
        # else:
        #     self.pack_forget()
        # pass

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
        self._wdgInfo.setProperty('width', width)
        pass

    def _setNavigation(self, key, control):
        if not isinstance(control, Control): raise TypeError('Not a Control type')
        if not hasattr(control, '_wdgID'): raise ReferenceError('Control not added to a window')
        self.navMap[key] = control

    def _getAlignment(self, _alignment):
        _alignment = _alignment or 0x00000000
        xbfont_left = 0x00000000
        xbfont_right = 0x00000001
        xbfont_center_x = 0x00000002
        xbfont_center_y = 0x00000004
        xbfont_truncated = 0x00000008
        _yalignment = 'center' if 0x00000004 & _alignment else 'top'
        index = 0x00000003 & (_alignment or xbfont_left)
        _xalignment = ('left', 'right', 'center', 'left') [index]
        return _xalignment, _yalignment

    def _getImgWidget(self, clIm, texture=None, photo=True):
        if texture == None:
            width, height = self.getWidth(), self.getHeight()
            texture = Image.new('RGBA', (width, height), (256, 256, 256, 0))
        width, height = texture.size
        w, h = clIm.size
        if self._xalign == 'left':
            xsrc = 0
            xdst = 0
            W = min(w, width)
        elif self._xalign == 'right':
            xsrc = max(0, w - width)
            xdst = max(0, width - w)
            W = min(w, width)
        elif self._xalign == 'center':
            xsrc = max(0, (w - width)/2)
            xdst = max(0, (width - w)/2)
            W = min(w, width)

        if self._yalign == 'top':
            ysrc = 0
            ydst = 0
            H = min(h, height)
        elif self._yalign == 'center':
            ysrc = max(0, (h - height)/2)
            ydst = max(0, (height - h)/2)
            H = min(h, height)

        region = clIm.crop((xsrc, ysrc, xsrc + W, ysrc + H))
        texture.paste(region, (xdst, ydst, xdst + W, ydst + H))
        if photo: texture = ImageTk.PhotoImage(texture)
        return texture

    # def setWdgImg(self):
    #     bFlag = self._isSelected or not self._isFocusable
    #     if bFlag:
    #         wdgImg = ImageTk.PhotoImage(self._wdgenabled)
    #     else:
    #         wdgImg =  ImageTk.PhotoImage(self._wdgdisabled)
    #     self.wdgImg = wdgImg
    #     return wdgImg

    def updateCanvas(self, enabled=None):
        if self._ctrlState:
            if enabled is not None: self._isSelected = enabled
            self._setWdgImage()


    def _setWdgImage(self):
        if not hasattr(self, '_wdgID'): return
        if not self._ctrlState:               # Disabled
            layout = self.disabledLayout or self.focusedLayout
        else:
            if self._isSelected:              # Normal
                layout = self.focusedLayout
            else:                                   # Focused
                layout = self.normalLayout or self.focusedLayout

        litem = self._wdgInfo
        pilImg = controlXml.getImageFromLayout(layout, litem, cache=self._imgCache)
        self.wdgImg = ImageTk.PhotoImage(pilImg)

        container = self.master
        canvas = container.widget
        canvas.itemconfigure(self._wdgID, image=self.wdgImg)
        pass


    # def _getEnabledImg(self):
    #     self.wdgImg = ImageTk.PhotoImage(self._wdgenabled)
    #     return self.wdgImg

    # def _getDisabledImg(self):
    #     self.wdgImg =  ImageTk.PhotoImage(self._wdgdisabled)
    #     return self.wdgImg


class ControlLabel(Control):

    """
    ControlLabel class.
    Creates a text label.
    """

    def __init__(self, x, y, width, height, label, font=None, textColor=None, disabledColor=None, _alignment=None,
                 hasPath=None, angle=None, _params=None):
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
        Control.__init__(self)
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        layout =    {u'align': 'center',
                     u'aligny': 'center',
                     u'angle': angle or 0,
                     u'font': font or 'font13',
                     u'haspath': hasPath or False,
                     u'label': 'item.label',
                     u'shadowcolor': None,
                     u'textcolor': 'selected',
                     u'type': 'label'}

        _params = _params or {}
        slfAttr = dict(master='master', id='_id')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        if _params.has_key('layout'): layout = _params.pop('layout')

        self._params = _params

        xalign, yalign = self._getAlignment(_alignment)
        ctrlParam = dict(align=xalign, aligny=yalign)
        layout.update((key, value) for key, value in ctrlParam.items() if value)

        self.focusedLayout = [layout]
        self.normalLayout = None
        self.disabledLayout = [layout.copy()]

        self.focusedLayout[0]['textcolor'] = textColor
        self.disabledLayout[0]['textcolor'] = disabledColor

        litem = self._wdgInfo
        litem.setTriggers(['label'])
        litem.setProperty('label', label)
        pass

    def setLabel(self, label):
        """Set's text for this label.

        label: string or unicode - text string.
        """
        label = label.replace('[CR]', '\n')
        litem = self._wdgInfo
        litem.setProperty('label', label)
        pass

    def getLabel(self):
        """Returns the text value for this label."""
        litem = self._wdgInfo
        return litem.getProperty('label')


class ControlTextBox(Control):

    """
    ControlTextBox class.
    Creates a box for multi-line text.
    """

    def __init__(self, x, y, width, height, font=None, textColor=None, _params=None):
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
        Control.__init__(self)
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        layout =    {u'align': 'left',
                     u'aligny': 'top',
                     u'font': font or 'font13',
                     u'label': 'item.label',
                     u'shadowcolor': None,
                     u'textcolor': textColor or 'white',
                     u'type': 'label',
                     u'wrapmultiline':True}

        _params = _params or {}
        slfAttr = dict(master='master', id='_id')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        if _params.has_key('layout'): layout = _params.pop('layout')

        self._params = _params

        self.focusedLayout = [layout]
        self.normalLayout = None
        self.disabledLayout = None

        litem = self._wdgInfo
        litem.setTriggers(['text'])
        text = _params.pop('text', '')
        self.setText(text)
        pass

    def setText(self, text):
        """Set's the text for this textbox.

        text: string or unicode - text string.
        """
        text = text.replace('[CR]', '\n')
        litem = self._wdgInfo
        litem.setProperty(text=text, position=0, label=text)
        pass

    def scroll(self, position):
        """Scrolls to the given position.

        id: integer - position to scroll to.
        """
        litem = self._wdgInfo
        text = litem.getProperty('text')
        litem.setProperty(position=position, label=text[position:])
        pass

    def reset(self):
        """Clear's this textbox."""
        litem = self._wdgInfo
        litem.setProperty(text='', position=0, label='')
        pass


class ControlEdit(Control):

    """
    ControlEdit class.
    ControlEdit(x, y, width, height, label[, font, textColor,
                                                    disabledColor, alignment, focusTexture, noFocusTexture])
    """

    def __init__(self, x, y, width, height, label, font=None, textColor=None, disabledColor=None, alignment=None,
                 focusTexture=None, noFocusTexture=None, _params=None):
        """
        x              : integer - x coordinate of control.
        y              : integer - y coordinate of control.
        width          : integer - width of control.
        height         : integer - height of control.
        label          : string or unicode - text string.
        font           : [opt] string - font used for label text. (e.g. 'font13')
        textColor      : [opt] hexstring - color of enabled label's label. (e.g. '0xFFFFFFFF')
        disabledColor  : [opt] hexstring - color of disabled label's label. (e.g. '0xFFFF3300')
        _alignment      : [opt] integer - alignment of label - *Note, see xbfont.h
        focusTexture   : [opt] string - filename for focus texture.
        noFocusTexture : [opt] string - filename for no focus texture.
        isPassword     : [opt] bool - if true, mask text value.

        *Note, You can use the above as keywords for arguments and skip certain optional arguments.
        Once you use a keyword, all following arguments require the keyword.
        After you create the control, you need to add it to the window with addControl().

        example:
        - self.edit = xbmcgui.ControlEdit(100, 250, 125, 75, 'Status')
        """
        pass
        Control.__init__(self)
        self._isFocusable = True
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        focusTxure = {   u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': focusTexture or 'button-focus.png'},
                         u'type': u'image'}

        nofocusTxure = { u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': noFocusTexture or 'button-nofocus.png'},
                         u'type': u'image'}

        lbllayout =    { u'align': 'left',
                         u'aligny': 'top',
                         u'font': font or 'font13',
                         u'label': 'item.label',
                         u'text':'item.text',
                         u'textcolor': textColor or 'white',
                         u'type': 'label',
                         u'width': width/2,
                         u'wrapmultiline':True}

        txtlayout =    { u'align': 'left',
                         u'aligny': 'top',
                         u'font': font or 'font13',
                         u'label': 'item.text',
                         u'left': width/2,
                         u'textcolor': textColor or 'white',
                         u'type': 'label',
                         u'width': width/2,
                         u'wrapmultiline':True}


        _params = _params or {}
        slfAttr = dict(master='master', id='_id', focusedlayout='focusedLayout', itemlayout='normalLayout', disabledlayout='disabledLayout')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))
        self._params = _params

        if alignment: xalign, yalign = self._getAlignment(alignment)
        else: xalign, yalign = 'right', 'top'
        ctrlParam = dict(align=xalign, aligny=yalign)
        lbllayout.update(ctrlParam)
        txtlayout.update(ctrlParam)


        self.focusedLayout = [focusTxure, lbllayout, txtlayout]
        self.normalLayout = [nofocusTxure, lbllayout.copy(), txtlayout.copy()]
        self.disabledLayout = [nofocusTxure.copy(), lbllayout.copy(), txtlayout.copy()]

        self.disabledLayout[1]['textcolor'] = disabledColor or 'grey3'
        self.disabledLayout[2]['textcolor'] = disabledColor or 'grey3'

        litem = self._wdgInfo
        litem.setTriggers(['label', 'text'])
        self.setLabel(label)
        pass

    def getLabel(self):
        """
        getLabel() -- Returns the text heading for this edit control.

        example:
        - label = self.edit.getLabel()
        """
        litem = self._wdgInfo
        return litem.getProperty('label')

    def getText(self):
        """
        getText() -- Returns the text value for this edit control.

        example:
        - value = self.edit.getText()
        """
        litem = self._wdgInfo
        return litem.getProperty('text')

    def setLabel(self, label):
        """
        setLabel(label) -- Set's text heading for this edit control.

        label          : string or unicode - text string.
        example:
        - self.edit.setLabel('Status')
        """
        litem = self._wdgInfo
        litem.setProperty(label=label)

    def setText(self, value):
        """
        setText(value) -- Set's text value for this edit control.

        value          : string or unicode - text string.
        example:
        - self.edit.setText('online')
        """
        litem = self._wdgInfo
        litem.setProperty(text=value)

    def _onClick(self, event):
        mess = self.getText()
        answ = tkSimpleDialog.askstring('Enter value', '', initialvalue=mess)
        self.setText(answ)


class ControlButton(Control):

    """
    ControlButton class.
    Creates a clickable button.
    """

    def __init__(self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, textOffsetX=None,
                 textOffsetY=None, alignment=None, font=None, textColor=None, disabledColor=None, angle=None,
                 shadowColor=None, focusedColor=None, _params=None):
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

        Control.__init__(self)
        self._imgCache  = True
        self._isFocusable = True
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        focusTxure = {   u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': 'item.focustexture'},
                         u'type': u'image'}

        nofocusTxure = { u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': 'item.nofocustexture'},
                         u'type': u'image'}

        lbllayout =    { u'align': 'center',
                         u'aligny': 'center',
                         u'angle': angle or 0,
                         u'font': 'item.font',
                         u'haspath': False,
                         u'label': 'item.label',
                         u'shadowcolor': 'item.shadowcolor',
                         u'textcolor': None,
                         u'type': 'label',
                         u'textoffsetx': textOffsetX or 0,
                         u'textoffsety': textOffsetY or 0}

        _params = _params or {}
        slfAttr = dict(master='master', id='_id')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        if _params.has_key('focusTxure'): focusTxure = _params.pop('focusTxure')
        if _params.has_key('nofocusTxure'): nofocusTxure = _params.pop('nofocusTxure')
        if _params.has_key('lbllayout'): lbllayout = _params.pop('lbllayout')

        self._params = _params

        if alignment is None: alignment = 0x00000002|0x00000004
        xalign, yalign = self._getAlignment(alignment)
        ctrlParam = dict(align=xalign, aligny=yalign)
        lbllayout.update(ctrlParam)

        self.focusedLayout = [focusTxure, lbllayout]
        self.normalLayout = [nofocusTxure, lbllayout.copy()]
        self.disabledLayout = [nofocusTxure.copy, lbllayout.copy()]

        self.focusedLayout[1]['textcolor'] = 'item.focusedcolor'
        self.normalLayout[1]['textcolor'] = 'item.textcolor'
        self.disabledLayout[1]['textcolor'] = 'item.disabledcolor'

        litem = self._wdgInfo
        triggers = ['label', 'font', 'textcolor', 'disabledcolor', 'focusedcolor', 'shadowcolor']
        litem.setTriggers(triggers)
        litem.setProperty(focustexture=focusTexture or 'button-focus.png', nofocustexture=noFocusTexture or 'button-nofocus.png')
        self.setLabel(label, font, textColor, disabledColor, shadowColor, focusedColor)
        pass


    def setDisabledColor(self, disabledColor):
        """Set's this buttons disabled color.

        disabledColor: hexstring - color of disabled button's label. (e.g. '0xFFFF3300')
        """
        litem = self._wdgInfo
        litem.setProperty('disabledcolor', disabledColor)
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
        ctrlParam = dict(label=label, font=font or 'font13', textcolor=textColor or 'white', disabledcolor=disabledColor or 'grey3', shadowcolor=shadowColor, focusedcolor=focusedColor or 'white')
        ctrlParam = dict((key, value) for key, value in ctrlParam.items() if value is not None)
        litem = self._wdgInfo
        litem.setProperty(**ctrlParam)
        pass

    def getLabel2(self):
        """Returns the buttons label2 as a unicode string."""
        return unicode


class ControlCheckMark(Control):

    """
    ControlCheckMark class.
    Creates a checkmark with 2 states.
    """

    def __init__(self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, checkWidth=None,
                 checkHeight=None, _alignment=None, font=None, textColor=None, disabledColor=None, _params=None):
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

        Control.__init__(self)
        self._imgCache  = True
        self._isFocusable = True
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        checkTexture = { u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': 'item.nofocustexture'},
                         u'type': u'image'}

        lbllayout =    { u'align': 'center',
                         u'aligny': 'center',
                         u'font': 'item.font',
                         u'label': 'item.label',
                         u'textcolor': None,
                         u'type': 'label',
                         u'textoffsetx': 0,
                         u'textoffsety': 0}

        _params = _params or {}
        slfAttr = dict(master='master', id='_id', focusedlayout='focusedLayout', itemlayout='normalLayout', disabledlayout='disabledLayout')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))
        self._params = _params

        ctrlParam = dict(centerleft=height/2, centertop=height/2, width=checkWidth or 20, height=checkHeight or 20)
        checkTexture.update(ctrlParam)

        if _alignment is None: _alignment = 0x00000002|0x00000004
        xalign, yalign = self._getAlignment(_alignment)
        ctrlParam = dict(left=height, align=xalign, aligny=yalign)
        lbllayout.update((key, value) for key, value in ctrlParam.items() if value)

        self.focusedLayout = [checkTexture, lbllayout]
        self.normalLayout = None
        self.disabledLayout = [checkTexture.copy(), lbllayout.copy()]

        self.focusedLayout[1]['textcolor'] = 'item.textcolor'
        self.disabledLayout[1]['textcolor'] = 'item.disabledcolor'

        litem = self._wdgInfo
        litem.setProperty(_isOn=False, focustexture=focusTexture or 'button-focus.png', nofocustexture=noFocusTexture or 'button-nofocus.png')
        triggers = ['_isOn', 'label', 'font', 'textcolor', 'disabledcolor']
        litem.setTriggers(triggers)
        # litem.setProperty(focustexture=focusTexture or 'button-focus.png', nofocustexture=noFocusTexture or 'button-nofocus.png')
        self.setLabel(label, font, textColor, disabledColor)
        pass

    def setDisabledColor(self, disabledColor):
        """Set's this controls disabled color.

        disabledColor: hexstring - color of disabled checkmark's label. (e.g. '0xFFFF3300')
        """
        litem = self._wdgInfo
        litem.setProperty('disabledcolor', disabledColor)
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
        ctrlParam = dict(label=label, font=font or 'font13', textcolor=textColor or 'white', disabledcolor=disabledColor or 'grey3')
        litem = self._wdgInfo
        litem.setProperty(**ctrlParam)
        pass

    def getSelected(self):
        """Returns the selected status for this checkmark as a bool."""
        litem = self._wdgInfo
        return litem.getProperty('_isOn')
        pass
        # return self._isOn

    def setSelected(self, isOn):
        """Sets this checkmark status to on or off.

        isOn: bool - True=selected (on) / False=not selected (off)
        """
        litem = self._wdgInfo
        texture = self.focusedLayout[0]['texture']
        if isOn:
            texture['value'] = 'item.focustexture'
            litem.setProperty('_isOn', True)
        else:
            texture['value'] = 'item.nofocustexture'
            litem.setProperty('_isOn', False)

    def _onClick(self, event):
        isOn = self.getSelected()
        self.setSelected(not isOn)


class ControlRadioButton(Control):
    """
    ControlRadioButton class.
    Creates a radio-button with 2 states.
    """

    def __init__(self, x, y, width, height, label, focusTexture=None, noFocusTexture=None, textOffsetX=None,
                 textOffsetY=None, _alignment=None, font=None, textColor=None, disabledColor=None, angle=None,
                 shadowColor=None, focusedColor=None, focusOnTexture=None, noFocusOnTexture=None,
                 focusOffTexture=None, noFocusOffTexture=None, _params=None):
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
        Control.__init__(self)
        self._imgCache  = True
        self._isFocusable = True
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        focusTxure = {   u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': focusTexture or 'button-focus.png'},
                         u'type': u'image'}

        nofocusTxure = { u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': noFocusTexture or 'button-nofocus.png'},
                         u'type': u'image'}

        checkTexture = { u'aspectratio': 'stretch',
                         u'texture': {u'border': 5, u'value': None},
                         u'type': u'image'}

        lbllayout =    {u'align': 'center',
                        u'aligny': 'center',
                         u'angle': 0,
                         u'font': 'font13',
                         u'label': 'item.label',
                         u'shadowcolor': None,
                         u'textcolor': 'selected',
                         u'type': 'label'}


        _params = _params or {}
        slfAttr = dict(master='master', id='_id')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        if _params.has_key('focusTxure'): focusTxure = _params.pop('focusTxure')
        if _params.has_key('nofocusTxure'): nofocusTxure = _params.pop('nofocusTxure')
        if _params.has_key('lbllayout'): lbllayout = _params.pop('lbllayout')

        self._params = _params

        if _alignment is None: _alignment = 0x00000002|0x00000004
        xalign, yalign = self._getAlignment(_alignment)
        ctrlParam = dict(align=xalign, aligny=yalign)
        lbllayout.update((key, value) for key, value in ctrlParam.items() if value)

        self.focusedLayout = [focusTxure, checkTexture, lbllayout]
        self.normalLayout = [nofocusTxure, checkTexture.copy(), lbllayout.copy()]
        self.disabledLayout = [nofocusTxure.copy(), checkTexture.copy(), lbllayout.copy()]

        self.focusedLayout[2]['textcolor'] = 'item.focusedcolor'
        self.normalLayout[2]['textcolor'] = 'item.textcolor'
        self.disabledLayout[2]['textcolor'] = 'item.disabledcolor'

        radioW = _params.get('radiowidth', 32)
        radioH = _params.get('radioheight', radioW)
        rx = width - radioW - _params.get('radioposx', 0)
        ry = height/2 - radioH/2 - _params.get('radioposy', 0)
        self.setRadioDimension(rx, ry, radioW, radioH)

        litem = self._wdgInfo
        litem.setProperty(focusontexture=focusOnTexture or 'radiobutton-focus.png', focusofftexture=focusOffTexture or 'radiobutton-nofocus.png')
        litem.setProperty(nofocusontexture=noFocusOnTexture or 'radiobutton-focus.png', nofocusofftexture=noFocusOffTexture or 'radiobutton-nofocus.png')
        litem.setProperty(_isOn=False)
        triggers = ['_isOn', 'label', 'font', 'textcolor', 'disabledcolor', 'focusedcolor', 'shadowcolor']
        litem.setTriggers(triggers)
        self.setLabel(label, font, textColor, disabledColor, shadowColor, focusedColor)
        pass

    def setSelected(self, selected):
        """Sets the radio buttons's selected status.

        selected: bool - True=selected (on) / False=not selected (off)
        """
        litem = self._wdgInfo
        focusRadioTexture = self.focusedLayout[1]['texture']
        noFocusRadioTexture = self.normalLayout[1]['texture']
        if selected:
            focusRadioTexture['value'] = 'item.focusontexture'
            noFocusRadioTexture['value'] = 'item.nofocusontexture'
        else:
            focusRadioTexture['value'] = 'item.focusofftexture'
            noFocusRadioTexture['value'] = 'item.nofocusofftexture'
        litem.setProperty('_isOn', selected)
        pass


    def isSelected(self):
        """Returns the radio buttons's selected status."""
        litem = self._wdgInfo
        return litem.getProperty('_isOn')

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
        ctrlParam = dict(label=label, font=font or 'font13', textcolor=textColor or 'white', disabledcolor=disabledColor or 'grey3', shadowcolor=shadowColor, focusedcolor=focusedColor or 'white')
        ctrlParam = dict((key, value) for key, value in ctrlParam.items() if value)
        litem = self._wdgInfo
        litem.setProperty(**ctrlParam)
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
        radioParams = dict(left=x, top=y, width=width, height=height)
        for elem in [self.focusedLayout, self.normalLayout, self.disabledLayout]:
            elem[1].update(radioParams)
            # elem[2]['width'] = x
        selected = self.isSelected()
        self.setSelected(selected)
        pass

    def _onClick(self, event):
        isOn = self.isSelected()
        self.setSelected(not isOn)


class ControlImage(Control):

    """
    ControlImage class.
    Displays an image from a file.
    """

    def __init__(self, x, y, width, height, filename, colorKey=None, aspectRatio=None, colorDiffuse=None, _params=None):
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
        Control.__init__(self)
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        layout = {   u'colorkey': colorKey,
                     u'aspectratio': 'stretch',
                     u'texture': {u'border': 0, u'value': 'item.texture'},
                     u'type': u'image',
                     u'colordiffuse': 'item.colordiffuse'}

        _params = _params or {}
        slfAttr = dict(master='master', id='_id')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        if _params.has_key('layout'): layout = _params.pop('layout')
        self._params = _params

        aspectratio = ['stretch', 'scale', 'keep'][aspectRatio or 0]
        ctrlParam = dict(colorkey=colorKey, aspectratio=aspectratio)
        layout.update((key, value) for key, value in ctrlParam.items() if value)

        self.focusedLayout = [layout]
        self.normalLayout = None
        self.disabledLayout = None

        litem = self._wdgInfo
        litem.setTriggers(['texture', 'colordiffuse'])
        litem.setProperty(texture=filename, colordiffuse=colorDiffuse)

        pass

    def setImage(self, filename):
        """Changes the image.

        filename: string - image filename.
        """
        litem = self._wdgInfo
        litem.setProperty('texture', filename)
        pass

    def setColorDiffuse(self, colorDiffuse):
        """Changes the images color.

        colorDiffuse: hexString - (example, '0xC0FF0000' (red tint)).
        """
        litem = self._wdgInfo
        litem.setProperty('colordiffuse', colorDiffuse)
        pass


class ControlGroup(Control):

    """ControlGroup class."""

    def __init__(self, x, y, width, height, _params=None):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.

        Example:
        self.group = xbmcgui.ControlGroup(100, 250, 125, 75)
        """
        Control.__init__(self)
        self.ctrlType = 'container'
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        self.master = None
        self._xorig = 0
        self._yorig = 0

        _params = _params or {}
        slfAttr = dict(master='master', id='_id', xorig='_xorig', yorig='_yorig')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        self._params = _params

        self.widget = None
        self.focus = None

        self._mouseX = 0
        self._mouseY = 0
        self._mouseT = 0
        self._mouseState = ''
        self.mouseStop = None
        pass

    def _getFocusedWidget(self):
        focusWdg = self.focus
        while self._isContainer(focusWdg) and focusWdg._isSelected:
            focusWdg = focusWdg.focus
        return focusWdg

    def _setFocusOn(self, control):
        ctrl = control
        while True:
            master = ctrl.master
            if master._isSelected: break
            master._isSelected = True
            master.focus = ctrl
            ctrl = master
        ctrlgrp = master.focus
        master.focus = ctrl

        if ctrlgrp:
            while hasattr(ctrlgrp, 'widget'):
                ctrlgrp._isSelected = False
                ctrlgrp = ctrlgrp.focus

            if ctrlgrp._isSelected: ctrlgrp.updateCanvas(False)
        if not control._isSelected: control.updateCanvas(True)

    def _onMotion(self, ctrl):
        if self.mouseStop:
            self._onLeave(None, ctrl)
            self._onEnter(None, self.mouseStop)
            self.mouseStop = None
        pass


class ControlList(Control):

    """
    ControlList class.
    Creates a list of items.
    """

    def __init__(self, x, y, width, height, font=None, textColor=None, buttonTexture=None, buttonFocusTexture=None,
                 selectedColor=None, _imageWidth=None, _imageHeight=None, _itemTextXOffset=None, _itemTextYOffset=None,
                 _itemHeight=None, _space=None, _alignmentY=None, _params=None):
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

        Control.__init__(self)
        self.ctrlType = 'compound'
        self._isFocusable = True
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        _params = _params or {}
        slfAttr = dict(master='master', id='_id')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))

        _itemHeight = _itemHeight or 42
        _space = _space or 0

        oFlag = _params.setdefault('orientation', 'vertical') == 'horizontal'

        focusTx    = {   u'aspectratio': 'stretch',
                         u'height': height if oFlag else _itemHeight,
                         u'texture': {u'border': 5, u'value': buttonFocusTexture or 'floor_buttonFO.png'},
                         u'type': u'image',
                         u'width': _itemHeight if oFlag else width}

        nofocusTx =  {   u'aspectratio': 'stretch',
                         u'height': height if oFlag else _itemHeight,
                         u'texture': {u'border': 5, u'value': buttonTexture or 'floor_button.png'},
                         u'type': u'image',
                         u'width': _itemHeight if oFlag else width}

        imageTexture = { u'aspectratio': 'stretch',
                         u'height': _imageHeight,
                         u'texture': {u'border': 5, u'value': 'item.thumbnailimage' or 'item.iconimage'},
                         u'type': u'image',
                         u'width': _imageWidth}

        yalign = self._getAlignment(_alignmentY or 0x00000004)[1]
        lbllayout =    { u'aligny': yalign,
                         u'height': height if oFlag else _itemHeight + _space,
                         u'font': font or 'font13',
                         u'label': 'item.label',
                         u'left': _imageWidth,
                         u'textcolor': 'selected',
                         u'type': 'label',
                         u'width': _itemHeight + _space if oFlag else width,
                         u'textoffsetx': _itemTextXOffset or 7,
                         u'textoffsety': _itemTextYOffset or 0}

        self.itmFocusedLayout = [focusTx, imageTexture, lbllayout]
        self.itmNormalLayout =  [nofocusTx, imageTexture.copy(), lbllayout.copy()]

        self.itmFocusedLayout[2]['textcolor'] = selectedColor or 'white'
        self.itmNormalLayout[2]['textcolor'] = textColor or 'white'

        if _params.has_key('focusedlayout'): self.itmFocusedLayout = _params.pop('focusedlayout')
        if _params.has_key('itemlayout'): self.itmNormalLayout = _params.pop('itemlayout')
        self._params = _params

        self.scrollList = self._params.pop('scrolllist', False)

        self.mouseFlag = True
        self.widget = None
        self.reset()
        self.setImageDimensions(_imageWidth, _imageHeight)
        self.setSpace(_space)
        self._setItemDim(_itemHeight or 42)
        pass

    def addItem(self, item):
        """Add a new item to this list control.

        item: string, unicode or ListItem - item to add.
        """
        if self.static: raise ValueError('Operation not allowed in static content')
        if not self.widget: return
        if isinstance(item, basestring):
            item = ListItem(item)
        oFlag = self._params['orientation'] == 'horizontal'
        w, h = self._getItemDim()
        if self.last:
            xpos, ypos = self.last.getPosition()
            xpos, ypos = (xpos + w, ypos) if oFlag else (xpos, ypos + h)
        else:
            xpos, ypos = 0, 0

        control = ControlImage(xpos, ypos, w, h, None)
        control.focusedLayout = copy.deepcopy(self.itmFocusedLayout)
        control.normalLayout = copy.deepcopy(self.itmNormalLayout)
        control._wdgInfo = guiTop.ListItemWrapper(item, ['label', 'thumbnailImage', 'iconImage'], control._setWdgImage)
        control._wdgInfo.setProperty(width=w, height=h)
        # control._setWdgImage()
        self._registerControl(control)

        if not self.frst:
            self.frst = self.last = self.focus = control
        else:
            dir1, dir2 = ('controlLeft', 'controlRight') if oFlag else ('controlUp', 'controlDown')
            last = self.last
            getattr(control, dir1)(last)
            getattr(control, dir2)(self.frst)
            getattr(self.frst, dir1)(control)
            getattr(last, dir2)(control)
            self.last = control
        return control

    def addItems(self, items):
        """Adds a list of listitems or strings to this list control.

        items: List - list of strings, unicode objects or ListItems to add.
        """
        for item in items:
            control = self.addItem(item)
        pass

    def selectItem(self, item):
        """Select an item by index number.

        item: integer - index number of the item to select.
        """
        selWdg = self._getItemControl(item)
        self._onEnter(None, selWdg)
        pass

    def reset(self):
        """Clear all ListItems in this control list."""
        if self.widget: self.widget.delete('item')
        self.focus = None
        self.frst = None
        self.last = None
        self.static = False
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
        if imageWidth: self._imgW = imageWidth
        if imageHeight: self._imgH = imageHeight
        pass

    def _setItemDim(self, itemD):
        itemD += self.getSpace()
        if self._params['orientation'] == 'horizontal':
            self._itemW, self._itemH = itemD, self.getHeight()
        else:
            self._itemW, self._itemH = self.getWidth(), itemD

    def _getItemDim(self):
        return self._itemW, self._itemH

    def setItemHeight(self, itemHeight):
        """Sets the height of items.

        itemHeight: integer - height of items.
        """
        self._itemH = itemHeight + self.getSpace()
        pass

    def getItemHeight(self):
        """Returns the control's current item height as an integer."""
        return self._itemH

    def setPageControlVisible(self, visible):
        """Sets the spin control's visible/hidden state.

        visible: boolean - True=visible / False=hidden.
        """
        pass

    def setSpace(self, space=None):
        """Set's the space between items.

        space: integer - space between items.
        """
        self._space = space or 0
        pass

    def getSpace(self):
        """Returns the control's space between items as an integer."""
        return self._space

    def getSelectedPosition(self):
        """Returns the position of the selected item as an integer.

        Note:
            Returns -1 for empty lists.
        """
        if not self.focus: return -1
        selWdg = self.focus
        ctrlPos = selWdg.getPosition()
        itemSize = self._getItemDim()
        oFlag = self._params['orientation'] == 'horizontal'
        ndx = 1 - oFlag
        return ctrlPos[ndx]/itemSize[ndx]

    def getSelectedItem(self):
        """Returns the selected item as a ListItem object.

        Note:
            Same as getSelectedPosition(), but instead of an integer a ListItem object is returned. Returns None for empty lists.
            See windowexample.py on how to use this.
        """
        selWdg = self.focus
        return selWdg._wdgInfo

    def size(self):
        """Returns the total number of items in this list control as an integer."""
        ctrl = self.last
        if not ctrl: return 0
        ctrlPos = ctrl.getPosition()
        itemDim = self._getItemDim()
        ndx = 0 if self._params['orientation'] == 'horizontal' else 1
        return ctrlPos[ndx]/itemDim[ndx] + 1

    def _getItemControl(self, index):
        if self.size() == 0 or index != max(0, min(index, self.size())):
            raise ValueError('Index is out of range')
        selPos = self.getSelectedPosition()
        if selPos == index: return self.getSelectedItem()
        deltaPos = index - selPos
        selWdg = self.focus
        oFlag = self._params['orientation'] == 'horizontal'
        dir1, dir2 = ('Right', 'Left') if oFlag else ('Down', 'Up')
        key = dir1 if deltaPos > 0 else dir2
        deltaPos = abs(deltaPos)
        for k in range(deltaPos):
            selWdg = selWdg.navMap[key]
        return selWdg

    def getListItem(self, index):
        """Returns a given ListItem in this List.

        index: integer - index number of item to return.

        Raises:
            ValueError: If index is out of range.
        """
        control = self._getItemControl(index)
        return  control.wdgInfo

    def setStaticContent(self, items):
        """Fills a static list with a list of listitems.

        items: List - list of listitems to add.
        """
        self.reset()
        self.addItems(items)
        self.static = True
        pass

    def removeItem(self, index):
        """
        Remove an item by index number.
        index : integer - index number of the item to remove.
        example:
        my_list.removeItem(12)
        """
        if self.static: raise ValueError('Operation not allowed in static content')
        if self.size() == 0 or index != max(0, min(index, self.size())):
            raise ValueError('Index is out of range')
        oFlag = self._params['orientation'] == 'horizontal'
        dir1, dir2 = ('Left', 'Right') if oFlag else ('Up', 'Down')
        selPos = self.getSelectedPosition()
        if index == selPos:
            control = self.focus
            self.focus = None
            key = dir1 if selPos == self.size() - 1 else dir2
            toFocus = control.navMap[key]
        else:
            control = self._getItemControl(index)

        Dir1 = control.navMap[dir1]
        Dir2 = control.navMap[dir2]
        getattr(Dir1, 'control' + dir2)(Dir2)
        getattr(Dir2, 'control' + dir1)(Dir1)

        lstX, lstY = self.last.getPosition()
        itemW, itemH = self._getItemDim()
        bottomRight = (lstX + itemW, lstY + itemH)
        itemW, itemH = (itemW, 0) if oFlag else (0, itemH)
        topLeft = (control.getX() + itemW, control.getY() + itemH)
        if index == 0: self.frst = Dir2
        elif index == (self.size() - 1): self.last = Dir1


        canvas = self.widget
        canvas.delete(control._wdgID)
        del control

        movbox = topLeft + bottomRight
        canvas.addtag_overlapping('tomove', *movbox)
        canvas.move('tomove', -itemW, -itemH)
        canvas.dtag('item', 'tomove')

        wdgToMove = Dir2
        for itemPos in range(index + 1, self.size()):
            xPos, yPos = wdgToMove.getPosition()
            wdgToMove.setPosition(xPos - itemW, yPos - itemH)
            wdgToMove = wdgToMove.navMap[dir2]
        if not self.focus and toFocus:
            self.focus = toFocus
            # self._onEnter(None, toFocus)
        pass

    def _registerControl(self, control):
        control.master = self
        wdg = self.widget
        xpos, ypos = control.getPosition()
        control._wdgID = wdgID = wdg.create_image(xpos, ypos)
        control._setWdgImage()
        wdg.itemconfigure(wdgID, image=control.wdgImg, anchor=tk.NW, tags='item')

        def onEnter(event, ctrl=control):
            return self._onEnter(event, ctrl)
        def onLeave(event, ctrl=control):
            return self._onLeave(event, ctrl)
        def onMotion(event, ctrl=control):
            return self._onMotion(ctrl, event)

        wdg.tag_bind(wdgID, '<Enter>', onEnter)
        wdg.tag_bind(wdgID, '<Leave>', onLeave)
        wdg.tag_bind(wdgID, '<Motion>', onMotion)

        if hasattr(control, '_onClick'):
            def onClick(event, ctrl=control):
                return self._onItemClick(event, ctrl)
            wdg.tag_bind(wdgID, '<Button-1>', onClick)

        self.focus = self.focus or control

    def _onEnter(self, event, ctrl):
        if event and not self.mouseFlag: return
        if not self._isSelected: self.master._setFocusOn(self)
        if self.focus != ctrl: self._onLeave(None, self.focus)
        oFlag = self._params['orientation'] == 'horizontal'
        dir1, dir2 = ('Left', 'Right') if oFlag else ('Up', 'Down')
        self.focus = ctrl
        wdg = self.widget
        wdgID = ctrl._wdgID
        ctrl._isSelected = True
        ctrl._setWdgImage()
        if self.last._wdgID != wdgID:
            wdg.tag_raise(wdgID, ctrl.navMap[dir2]._wdgID)
        self.widget.focus_set()

    def _onLeave(self, event, ctrl):
        if not self.focus._isSelected: return
        oFlag = self._params['orientation'] == 'horizontal'
        dir1, dir2 = ('Left', 'Right') if oFlag else ('Up', 'Down')
        wdg = self.widget
        wdgID = ctrl._wdgID
        ctrl._isSelected = False
        ctrl._setWdgImage()
        # wdg.itemconfigure(wdgID, image=ctrl._getDisabledImg())
        if self.last._wdgID != wdgID:
            wdg.tag_lower(wdgID, ctrl.navMap[dir2]._wdgID)

    def _onMotion(self, ctrl, event):
        if not self.mouseFlag:
            if (ctrl._wdgID != self.focus._wdgID):
                self._onLeave(None, self.focus)
                self._onEnter(None, ctrl)
            self.mouseFlag = True
        pass

    def _onItemClick(self, event, ctrl):
        ctrl._onClick()

    def updateCanvas(self, isSelected=None):
        if isSelected is None: return
        self._isSelected = isSelected
        focus = self.focus
        if not focus: return
        func = self._onEnter if isSelected else self._onLeave
        func(None, focus)

    def _setWidgetBinds(self):
        ctrlWdg = self.widget

        ctrlWdg.event_add('<<navigation>>', '<Up>', '<Down>', '<Left>', '<Right>', '<Home>', '<End>', '<Prior>', '<Next>')
        ctrlWdg.bind('<<navigation>>', self._onNavigation)

        ctrlWdg.event_add('<<itemSelection>>', '<Return>', '<ButtonRelease-1>')
        ctrlWdg.bind('<<itemSelection>>', self._onItemSelection)


        ctrlWdg.event_add('<<listscroll>>', '<ButtonRelease-4>', '<ButtonRelease-5>', '<MouseWheel>')
        ctrlWdg.bind('<<listscroll>>', self._onListScroll)


    def _onNavigation(self, event):
        key = event.keysym
        wdg = self.focus
        if key not in ['Up', 'Down', 'Left', 'Right', 'Home', 'End', 'Prior', 'Next']: return
        vwcoords=None
        oFlag = self._params['orientation'] == 'horizontal'
        if key in ['Up', 'Down', 'Left', 'Right']:
            dir1, dir2 = ('Left', 'Right') if oFlag else ('Up', 'Down')
            if self.scrollList and key in [dir1, dir2]:
                canvas = self.widget
                xy = (self.getWidth(), self.getHeight())
                itemSize = self._getItemDim()
                cnv = (self.last.getX() + itemSize[0], self.last.getY() + itemSize[1])
                spc = self.getSpace()
                ndx = 1- oFlag
                if key == dir1:
                    p1 = xy[ndx]/2 - (itemSize[ndx] - spc)/2
                    p1x, p1y = (canvas.canvasx((1 - ndx)*p1), canvas.canvasy(ndx*p1))
                    LimInf, LimSup = xy[ndx]/2 - (itemSize[ndx] - spc)/2, cnv[ndx] - xy[ndx]/2 + (itemSize[ndx] - spc)/2
                else:
                    p1x, p1y = (canvas.canvasx(0), canvas.canvasy(0))
                    LimInf, LimSup = 0, cnv[ndx] - xy[ndx]
                p = (p1x, p1y)
                p1 = p[ndx] + (itemSize[ndx] - spc)
                if LimInf <= p1 <= LimSup:
                    p2x, p2y = xy[0]/(2 - ndx) + (1 - ndx)*(itemSize[0] + spc)/2, xy[1]/(1 + ndx) + ndx*(itemSize[1] + spc)/2
                    vwcoords = p + (p1x + p2x, p1y + p2y)
            control = wdg.navMap.get(key, None)
            if control:
                ctrlgrp = self
            elif self.navMap.get(key, None):
                control = self.navMap[key]
                ctrlgrp = self.master
            if not control: return
            if isinstance(control, ControlGroup):
                self.checkScroll(ctrlgrp, control)
                ctrlgrp = control
                control = control.focus
        elif key in ['Home', 'End']:
            control = self.frst if key == 'Home' else self.last
            ctrlgrp = self
        elif key in ['Prior', 'Next']:
            ctrlgrp = self
            wdgSize = (self.getWidth(), self.getHeight())
            itemSize = self._getItemDim()
            oFlag = self._params['orientation'] == 'horizontal'
            ndx = 1 - oFlag
            deltaPos = wdgSize[ndx]/itemSize[ndx] * (1 if key == 'Next' else -1)

            selPos = self.getSelectedPosition()
            limINF, limSUP = 0, self.size() - 1
            nxtPos = max(limINF, min(selPos + deltaPos, limSUP))
            if limINF < nxtPos < limSUP:
                control = self._getItemControl(nxtPos)
                canvas = self.widget
                xW, yH = self.focus.getPosition()
                if nxtPos - selPos > 0:
                    vwcoords = (canvas.canvasx(0), canvas.canvasy(0)) + (xW + itemSize[0], yH + itemSize[1])
                else:
                    width, height = canvas.winfo_width(), canvas.winfo_height()
                    vwcoords = (xW, yH) + (canvas.canvasx(width), canvas.canvasy(height))
            else:
                control = self.frst if nxtPos == limINF else self.last

        self._onLeave(None, wdg)
        ctrlgrp._onEnter(None, control)
        self.checkScroll(ctrlgrp, control, vwcoords)
        self.mouseFlag = False



    def checkScroll(self, ctrlgrp, control, vwcoords=None):
        canvas = ctrlgrp.widget
        w, h = control.getWidth(), control.getHeight()
        xpos, ypos = control.getPosition()
        wdgcoords = (xpos, ypos) + (xpos + w, ypos + h)
        if not vwcoords:
            width, height = canvas.winfo_width(), canvas.winfo_height()
            vwcoords = (canvas.canvasx(0), canvas.canvasy(0)) + (canvas.canvasx(width), canvas.canvasy(height))
        deltax = min(wdgcoords[0], vwcoords[0]) - vwcoords[0] + max(wdgcoords[2], vwcoords[2]) - vwcoords[2]
        deltay = min(wdgcoords[1], vwcoords[1]) - vwcoords[1] + max(wdgcoords[3], vwcoords[3]) - vwcoords[3]
        if deltax != 0 or deltay != 0:
            dx, dy = int(deltax), int(deltay)
            p1 = (max(0, dx), max(0, dy))
            p2 = (-min(0, dx), -min(0, dy))
            canvas.scan_mark(*p1)
            canvas.scan_dragto(*p2, gain=1)
            canvas.update()
            pass

    def _onItemSelection(self, event):
        if event.keysym == 'Return':
            key, id, mod, device = ('enter', None, '', 'keyboard')
        else:
            key, id, mod, device = ('leftclick', None, '', 'mouse')
        root = guiTop.AppWindow()
        root.toNotify(self, key, id, mod, event, device)
        pass

    def _onListScroll(self, event):
        if event.type == '38': # MOUSEWHEEL
            key = 'wheelup' if event.delta > 0 else 'wheeldown'
        elif event.type == '5': # BUTTONRELEASE
            key = 'wheelup' if event.num == 4 else 'wheeldown'

        oFlag = self._params['orientation'] == 'horizontal'
        canvas = self.widget
        xy = (self.getWidth(), self.getHeight())
        itemSize = self._getItemDim()
        cnv = (self.last.getX() + itemSize[0], self.last.getY() + itemSize[1])
        ndx = 1 - oFlag

        if key == 'wheelup':
            p1 = (canvas.canvasx(0), canvas.canvasy(0))
            deltax = -(1 - ndx)*min(p1[ndx], itemSize[ndx])
            deltay = -ndx*min(p1[ndx], itemSize[ndx])
            dPos = -1
        elif key == 'wheeldown':
            deltax = (1 - ndx)*min(cnv[ndx] - canvas.canvasy(xy[ndx]), itemSize[ndx])
            deltay = ndx*min(cnv[ndx] - canvas.canvasy(xy[ndx]), itemSize[ndx])
            dPos = 1
        if deltax != 0 or deltay != 0:
            dx, dy = int(deltax), int(deltay)
            p1 = (max(0, dx), max(0, dy))
            p2 = (-min(0, dx), -min(0, dy))
            canvas.scan_mark(*p1)
            canvas.scan_dragto(*p2, gain=1)
            selPos = self.getSelectedPosition()
            self.selectItem(selPos + dPos)


class ControlSlider(Control):

    """
    ControlSlider class.
    Creates a slider.
    """

    def __init__(self, x, y, width, height, textureback=None, texture=None, texturefocus=None, _params=None):
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
        Control.__init__(self)
        self._isFocusable = True
        self.setPosition(x, y)
        self.setWidth(width)
        self.setHeight(height)

        textureback = textureback or 'osd_slider_bg_2.png'
        texture = texture or 'osd_slider_nibNF.png'
        texturefocus = texturefocus or 'osd_slider_nib.png'

        controloffsetx = 10
        controloffsety =  0
        posmin = controloffsetx - 5
        posmax = posmin +  width - 2*controloffsetx

        sliderbar = { u'aspectratio': 'stretch',
                      u'left': controloffsetx,
                      u'top': controloffsety,
                      u'width': width - 2*controloffsetx,
                      u'height': height - controloffsety,
                      u'texture': {u'border': 0, u'value': textureback},
                      u'type': u'image'}

        slidernib = { u'aspectratio': 'stretch',
                      u'left': 'item.intpercent',
                      u'top': controloffsety,
                      u'width': 10,
                      u'height': height - controloffsety,
                      u'texture': {u'border': 0, u'value': None},
                      u'type': u'image'}

        _params = _params or {}
        slfAttr = dict(master='master', id='_id', focusedlayout='focusedLayout', itemlayout='normalLayout', disabledlayout='disabledLayout')
        set_int = set(_params.keys()).intersection(slfAttr.keys())
        while set_int:
            key = set_int.pop()
            setattr(self, slfAttr[key], _params.pop(key))
        self._params = _params

        self.focusedLayout = [sliderbar, slidernib]
        self.normalLayout = [sliderbar, copy.deepcopy(slidernib)]
        self.disabledLayout = None

        self.focusedLayout[1]['texture']['value'] = texturefocus
        self.normalLayout [1]['texture']['value'] = texture

        litem = self._wdgInfo
        litem.setProperty(posmin=posmin, posmax=posmax, percent=0, intpercent=posmin)
        triggers = ['percent', 'intpercent']
        litem.setTriggers(triggers)
        self.setPercent(0)
        pass


    def getPercent(self):
        """Returns a float of the percent of the slider."""
        litem = self._wdgInfo
        return litem.getProperty('percent')

    def setPercent(self, percent):
        """Sets the percent of the slider."""
        litem = self._wdgInfo
        posmin, posmax = litem.getProperty('posmin'), litem.getProperty('posmax')
        intpercent = posmin + int((posmax - posmin)*percent/100)
        litem.setProperty(percent=percent, intpercent=intpercent)
        pass

    def _onClick(self, event):
        if event is None: return
        litem = self._wdgInfo
        newpos = event.x - (self.getX() + self.master._xorig) - litem.getProperty('posmin')
        self._moveSliderTo(newpos)
        pass

    _onDrag = _onClick

    def _onKey(self, event):
        keysym = event.keysym
        if keysym not in ['Left', 'Right']: return
        litem = self._wdgInfo
        actpos = litem.getProperty('intpercent')
        k = 1 if keysym == 'Right' else -1
        newpos = actpos + k
        self._moveSliderTo(newpos)

    def _moveSliderTo(self, newpos):
        litem = self._wdgInfo
        posmin, posmax = litem.getProperty('posmin'), litem.getProperty('posmax')
        if newpos != max(posmin, min(newpos, posmax)): return
        percent = (100.0 * (newpos - posmin))/(posmax - posmin)
        self.setPercent(percent)


class Dialog(object):

    def __init__(self):
        self._Window = _Window = Window()
        setattr(_Window, 'onAction', self.onAction)
        setattr(_Window, 'onClick', self.onClick)
        setattr(_Window, 'onDoubleClick', self.onDoubleClick)
        setattr(_Window, 'onControl', self.onControl)
        setattr(_Window, 'onFocus', self.onFocus)
        setattr(_Window, 'onInit', self.onInit)
        self.answ = None
        self.buffer = []
        self.ndx = 0
        self.strPane = None
        pass

    def browse(self, type, heading, s_shares, mask=None, useThumbs=False, treatAsFolder=False, default=None,
               enableMultiple=False):
        """Show a 'Browse' dialog.

        type: integer - the type of browse dialog.
        heading: string or unicode - dialog heading.
        s_shares: string or unicode - from sources.xml. (i.e. 'myprograms')
        mask: string or unicode - '|' separated file mask. (i.e. '.jpg|.png')
        useThumbs: boolean - if True autoswitch to Thumb view if files exist.
        treatAsFolder: boolean - if True playlists and archives act as folders.
        default: string - default path or file.
        enableMultiple: boolean - if True multiple file selection is enabled.

        Types:
            0: ShowAndGetDirectory
            1: ShowAndGetFile
            2: ShowAndGetImage
            3: ShowAndGetWriteableDirectory

        Note:
            If enableMultiple is False (default): returns filename and/or path as a string
            to the location of the highlighted item, if user pressed 'Ok' or a masked item
            was selected. Returns the default value if dialog was canceled.
            If enableMultiple is True: returns tuple of marked filenames as a string,
            if user pressed 'Ok' or a masked item was selected. Returns empty tuple if dialog was canceled.

            If type is 0 or 3 the enableMultiple parameter is ignored.

        Example:
            dialog = xbmcgui.Dialog()
            fn = dialog.browse(3, 'XBMC', 'files', '', False, False, False, 'special://masterprofile/script_data/XBMC Lyrics')
        """
        return

    def browseMultiple(self, type, heading, shares, mask=None, useThumbs=None, treatAsFolder=None, default=None):
        """
        browse(type, heading, shares[, mask, useThumbs, treatAsFolder, default])--Show a 'Browse' dialog.

        type : integer - the type of browse dialog.
        heading : string or unicode - dialog heading.
        shares : string or unicode - from sources.xml. (i.e. 'myprograms')
        mask : [opt] string or unicode - '|' separated file mask. (i.e. '.jpg|.png')
        useThumbs : [opt] boolean - if True autoswitch to Thumb view if files exist (default=false).
        treatAsFolder : [opt] boolean - if True playlists and archives act as folders (default=false).
        default : [opt] string - default path or file.

        Types:
        - 1 : ShowAndGetFile
        - 2 : ShowAndGetImage


        *Note,
        returns tuple of marked filenames as a string,"
        if user pressed 'Ok' or a masked item was selected. Returns empty tuple if dialog was canceled.

        example:

        - dialog = xbmcgui.Dialog()
        - fn = dialog.browseMultiple(2, 'XBMC', 'files', '', False, False, 'special://masterprofile/script_data/XBMC Lyrics')
        """
        return self.browse(self, type, heading, shares, mask=None, useThumbs=False, treatAsFolder=False, default=None,
               enableMultiple=True)

    def browseSingle(self, type, heading, shares, mask=None, useThumbs=None, treatAsFolder=None, default=None):
        """
        browse(type, heading, shares[, mask, useThumbs, treatAsFolder, default])--Show a 'Browse' dialog.

        type : integer - the type of browse dialog.
        heading : string or unicode - dialog heading.
        shares : string or unicode - from sources.xml. (i.e. 'myprograms')
        mask : [opt] string or unicode - '|' separated file mask. (i.e. '.jpg|.png')
        useThumbs : [opt] boolean - if True autoswitch to Thumb view if files exist (default=false).
        treatAsFolder : [opt] boolean - if True playlists and archives act as folders (default=false).
        default : [opt] string - default path or file.

        Types:

        - 0 : ShowAndGetDirectory
        - 1 : ShowAndGetFile
        - 2 : ShowAndGetImage
        - 3 : ShowAndGetWriteableDirectory
        *Note, Returns filename and/or path as a string to the location of the highlighted item,
        if user pressed 'Ok' or a masked item was selected.
        Returns the default value if dialog was canceled.

        example:

        - dialog = xbmcgui.Dialog()
        - fn = dialog.browse(3, 'XBMC', 'files', '', False, False, 'special://masterprofile/script_data/XBMC Lyrics')
        """
        return self.browse(self, type, heading, s_shares, mask=None, useThumbs=False, treatAsFolder=False, default=None,
               enableMultiple=False)

    def input(self, heading, default=None, type=0, option=None, autoclose=None):
        """
        input(heading[, default, type, option, autoclose])--Show an Input dialog.

        heading : string - dialog heading.
        default : [opt] string - default value. (default=empty string)
        type : [opt] integer - the type of keyboard dialog. (default=xbmcgui.INPUT_ALPHANUM)
        option : [opt] integer - option for the dialog. (see Options below)
        autoclose : [opt] integer - milliseconds to autoclose dialog. (default=do not autoclose)

        Types:
        - xbmcgui.INPUT_ALPHANUM (standard keyboard)
        - xbmcgui.INPUT_NUMERIC (format: #)
        - xbmcgui.INPUT_DATE (format: DD/MM/YYYY)
        - xbmcgui.INPUT_TIME (format: HH:MM)
        - xbmcgui.INPUT_IPADDRESS (format: #.#.#.#)
        - xbmcgui.INPUT_PASSWORD (return md5 hash of input, input is masked)


        Options PasswordDialog :

        - xbmcgui.PASSWORD_VERIFY (verifies an existing (default) md5 hashed password)
        Options AlphanumDialog :

        - xbmcgui.ALPHANUM_HIDE_INPUT (masks input)
        *Note, Returns the entered data as a string.
        Returns an empty string if dialog was canceled.

        Note:
            available since Gotham

        Example:
        - dialog = xbmcgui.Dialog()
        - d = dialog.input('Enter secret code', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        """
        pass

    def numeric(self, type, heading, default=None):
        """Show a 'Numeric' dialog.

        type: integer - the type of numeric dialog.
        heading: string or unicode - dialog heading.
        default: string - default value.

        Types:
            0: ShowAndGetNumber    (default format: #)
            1: ShowAndGetDate      (default format: DD/MM/YYYY)
            2: ShowAndGetTime      (default format: HH:MM)
            3: ShowAndGetIPAddress (default format: #.#.#.#)

        Note:
            Returns the entered data as a string.
            Returns the default value if dialog was canceled.

        Example:
            dialog = xbmcgui.Dialog()
            d = dialog.numeric(1, 'Enter date of birth')
        """
        self.format = [None, [2, 2, 4], [2, 2], [3, 2, 2, 2]][type]
        self.chrSep = ['', '/', ':', '.'][type]
        xmlfilename = 'DialogNumeric.xml'
        self._setDialogGui(xmlfilename)
        window = self._Window
        ctrl = window.getControl(1)
        ctrl.setLabel(heading)
        self.strPane = window.getControl(4)
        if default:
            self.buffer = list(default)
            self.ndx = len(default)
            self.answ = default
            self.strPane.setLabel(default)
        pass
        window.show()
        return self.answ

    def notification(self, heading, message, icon=None, time=None, sound=None):
        """
        notification(heading, message[, icon, time, sound])--Show a Notification alert.

        heading : string - dialog heading.
        message : string - dialog message.
        icon : [opt] string - icon to use. (default xbmcgui.NOTIFICATION_INFO)
        time : [opt] integer - time in milliseconds (default 5000)
        sound : [opt] bool - play notification sound (default True)

        Builtin Icons:

        - xbmcgui.NOTIFICATION_INFO
        - xbmcgui.NOTIFICATION_WARNING
        - xbmcgui.NOTIFICATION_ERROR
        example:
        - dialog = xbmcgui.Dialog()
        - dialog.notification('Movie Trailers', 'Finding Nemo download finished.', xbmcgui.NOTIFICATION_INFO, 5000)
        """
        pass

    def yesno(self, heading, line1, line2=None, line3=None, nolabel=None, yeslabel=None):
        """Show a dialog 'YES/NO'.

        heading: string or unicode - dialog heading.
        line1: string or unicode - line #1 text.
        line2: string or unicode - line #2 text.
        line3: string or unicode - line #3 text.
        nolabel: label to put on the no button.
        yeslabel: label to put on the yes button.

        Note:
            Returns True if 'Yes' was pressed, else False.

        Example:
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno('XBMC', 'Do you want to exit this script?')
        """
        xmlfilename = 'DialogYesNo.xml'
        self._setDialogGui(xmlfilename)
        window = self._Window
        ctrl = window.getControl(1)
        ctrl.setLabel(heading)
        line = '\n'.join(elem for elem in [line1, line2, line3] if elem)
        ctrl = window.getControl(9)
        ctrl.setText(line)
        if yeslabel:
            ctrl = window.getControl(11)
            ctrl.setLabel(yeslabel)
        if nolabel:
            ctrl = window.getControl(10)
            ctrl.setLabel(nolabel)
        window.show()
        return self.answ or 'no'
        pass

    def ok(self, heading, line1, line2=None, line3=None):
        """Show a dialog 'OK'.

        heading: string or unicode - dialog heading.
        line1: string or unicode - line #1 text.
        line2: string or unicode - line #2 text.
        line3: string or unicode - line #3 text.

        Note:
            Returns True if 'Ok' was pressed, else False.

        Example:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'There was an error.')
        """
        xmlfilename = 'DialogOk.xml'
        self._setDialogGui(xmlfilename)
        line = '\n'.join(elem for elem in [line1, line2, line3] if elem)
        window = self._Window
        ctrl = window.getControl(1)
        ctrl.setLabel(heading)
        ctrl = window.getControl(9)
        ctrl.setText(line)
        window.show()
        pass

    def select(self, heading, mlist, autoclose=0):
        """Show a select dialog.

        heading: string or unicode - dialog heading.
        mlist: string list - list of items.
        autoclose: integer - milliseconds to autoclose dialog.

        Note:
            autoclose = 0 - This disables autoclose.
            Returns the position of the highlighted item as an integer.

        Example:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Choose a playlist', ['Playlist #1', 'Playlist #2, 'Playlist #3'])
        """
        pass


    def onAction(self, action):
        """onAction method.

        This method will recieve all actions that the main program will send to this window.
        By default, only the PREVIOUS_MENU action is handled.
        Overwrite this method to let your script handle all actions.
        Don't forget to capture ACTION_PREVIOUS_MENU, else the user can't close this window.
        """
        if action == ACTION_PREVIOUS_MENU:
            self._Window.close()
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
        ctrlId = control.getId()
        if self._Window.wndId in [WindowIDs.WINDOW_DIALOG_YES_NO, WindowIDs.WINDOW_DIALOG_OK]:
            if ctrlId == 11:          #YES BUTTON
                self.answ = 'yes'
                ctrlId = ACTION_PREVIOUS_MENU

            if ctrlId == ACTION_PREVIOUS_MENU:
                self._Window.close()
        pass

        if 10 <= ctrlId <= 19:
            letra = str(ctrlId % 10)
            self.modOutStr(letra, self.format, self.chrSep)

        if ctrlId == 23:
            ndx = self.ndx
            if len(self.buffer) == ndx:
                ndx -= 1
                ndx = max(0, ndx)
                self.ndx = ndx

            if len(self.buffer[ndx]) == 1:
                if ndx == len(self.buffer):
                    self.buffer.pop()
                else:
                    self.buffer.pop(ndx)
                self.ndx -= 1
            else:
                self.buffer[ndx] = self.buffer[ndx][:-1]
            self.modOutStr(jnChar=self.chrSep)

        if ctrlId == 20:
            self.ndx = max(0, self.ndx - 1)
        if ctrlId == 22:
            self.ndx = min(len(self.buffer), self.ndx + 1)

        if ctrlId == 21:
            self.answ = self.strPane.getLabel()
            self._Window.close()



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


    def _setDialogGui(self, xmlFilename, defaultSkin='Default', defaultRes='720p'):
        _Window = self._Window
        _Window.wndId = ButtonTranslator.windows.get(xmlFilename.lower(), None)

        window, controls = controlXml.getRoots(xmlFilename, '', defaultSkin, defaultRes)
        wndList = controlXml.processRoot(window)
        xorig = yorig = 0
        for elem in wndList:
            for key in ['CHILDREN', 'ID', 'MASTERID']:
                elem.pop(key, None)
            elem_tag = elem.pop('elem_tag')
            if elem_tag == 'window':
                _Window._window = elem
            elif elem_tag == 'coordinates':
                xorig = elem.get('left', 0)
                yorig = elem.get('top', 0)
        ctrList = controlXml.processRoot(controls)
        masterW, masterH = _Window.getWidth(), _Window.getHeight()
        scrResW, scrResH = controlXml.coordResolution[defaultRes]
        if (scrResW*masterH)/scrResH > masterW:
            h = (scrResH*masterW)/scrResW
            deltaX, deltaY = 0, (masterH - h)/2
            masterH = h
        else:
            w = (scrResW*masterH)/scrResH
            deltaX, deltaY = (masterW - w)/2, 0
            masterW = w

        width, height = controlXml.normControlMap(ctrList, scrResW, scrResH)

        cgrp = _Window.focus
        deltaX, deltaY = -(masterW - width)/2, -(masterH - height)/2
        cgrp._xorig, cgrp._yorig = (masterW*xorig)/scrResW + deltaX, (masterH*yorig)/scrResH + deltaY
        width,            height = (masterW*width)/scrResW, (masterH*height)/scrResH
        # _Window.wndTk.attributes('-fullscreen', False)
        _Window.wndTk.geometry("%dx%d%+d%+d" % (width, height, (masterW - width)/2, (masterH - height)/2))
        # _Window.wndTk.overrideredirect(1)
        controls = []
        for k in range(len(ctrList)):
            control = relationalTags = None
            if ctrList[k]['elem_tag'] == 'control':
                controlClass, args, kwargs, relationalTags = controlXml.mapControl(k, ctrList)
                for n in [0, 2]: args[n] = (masterW*args[n])/scrResW
                for n in [1, 3]: args[n] = (masterH*args[n])/scrResH
                masterPos = kwargs['_params'].pop('master')
                if masterPos is not None:
                    kwargs['_params']['master'] = controls[masterPos]
                controlClass = getattr(sys.modules[__name__], controlClass)
                control = controlClass(*args, **kwargs)
            controls.append(control)
            ctrList[k] = relationalTags

        _Window.addControls([ctrl for ctrl in controls if ctrl])
        for control, relationalTags in zip(controls, ctrList):
            if control is None: continue
            navtags = relationalTags['navtags'].items()
            for k in range(len(navtags)):
                key, ctrId = navtags[k]
                ctrId = _Window.getControl(ctrId)
                navtags[k] = (key[2:], ctrId)
            if navtags: control.setNavigation(**dict(navtags))

    def modOutStr(self, letra=None, lenLetra=None, jnChar=''):
        if letra:
            ndx = self.ndx
            # numLetras = lenLetra[ndx] if lenLetra else 1
            # nPos = len(self.buffer[ndx]) if self.buffer else 0
            if ndx == len(self.buffer):
                self.buffer.append(letra)
            else:
                if not lenLetra:
                    self.buffer.insert(ndx, letra)
                else:
                    self.buffer[ndx] += letra
            if not lenLetra or  len(self.buffer[ndx]) == lenLetra[ndx]:
                self.ndx = min(len(self.buffer), ndx + 1)
        buffer = jnChar.join(self.buffer)
        self.strPane.setLabel(buffer)


class testWindow(Window):
    def __init__(self):
        Window.__init__(self)
        # self.addControl(ControlImage(0, 0, 720, 576, 'background.png'))
        self.listV = ControlList(800, 10, 400, 400,
                                        textColor='yellow', selectedColor='green',
                                        _imageWidth=20, _imageHeight=20,
                                        buttonFocusTexture='floor_buttonFO.png',
                                        buttonTexture='floor_button.png',
                                        _space=0,
                                        _params={'scrolllist':False})

        self.listH = ControlList(10, 450, 1200, 45,
                                        textColor='yellow', selectedColor='green',
                                        _imageWidth=20, _imageHeight=20,
                                        buttonFocusTexture='floor_buttonFO.png',
                                        buttonTexture='floor_button.png',
                                        _space=30, _itemHeight=200,
                                        _params={'orientation':'horizontal', 'scrolllist':True})

        filename = 'c:/testFiles/confluence/defaultvideo.png'
        img1 = ControlImage(10, 510, 256, 256, filename, colorDiffuse=None)


        self.strAction = ControlLabel(50, 100, 200, 20, 'action', 'font13', '0xFFFF3300')
        self.strButton = ControlLabel(50, 150, 200, 20, 'button', 'font13', '0xFFFFFFFF')

        self.addControl(img1)
        self.addControl(self.listV)
        self.addControl(self.listH)
        self.addControl(self.strAction)
        self.addControl(self.strButton)

        self.button1 = ControlButton(50, 200, 200, 30, "Button 1")
        self.button2 = ControlButton(50, 240, 200, 30, "Button 2")
        self.chkbutton = ControlCheckMark(50, 280, 200, 30, "Check Button")
        self.radiobutton = ControlRadioButton(50, 320, 200, 50, "Radio Button")
        self.textbox = ControlTextBox(400, 10, 300, 200)
        self.editbox = ControlEdit(400, 220, 300, 50, 'Search')
        self.slider = ControlSlider(400, 300, 300, 50)

        self.addControl(self.button1)
        self.addControl(self.button2)
        self.addControl(self.chkbutton)
        self.addControl(self.radiobutton)
        self.addControl(self.textbox)
        self.addControl(self.editbox)
        self.addControl(self.slider)

        self.button1.controlDown(self.button2)
        self.button1.controlRight(self.listV)
        self.button2.controlUp(self.button1)
        self.button2.controlRight(self.listV)
        self.button2.controlDown(self.radiobutton)
        self.radiobutton.controlUp(self.button2)
        self.radiobutton.controlDown(self.listH)
        self.listV.controlLeft(self.button1)
        self.listH.controlUp(self.radiobutton)
        self.listH.controlDown(self.button1)

        # add a few items to the list
        # xbmcgui.lock()

        self.textbox.setText('Esto es un texto[CR]con tres lineas[CR]por lo menos')
        self.editbox.setText('buscar')

        for i in range(50):
            listitem = ListItem('item' + str(i), iconImage='icon_home.png', thumbnailImage='icon_back.png')
            listitem.setLabel2('test')
            listitem.setInfo(type='video', infoLabels={'Title':'movie', 'playcount':2})
            listitem.select(True)
            self.listV.addItem(listitem)
            self.listH.addItem('ItemH%2d' % i)
        # xbmcgui.unlock()
        self.setFocus(self.button1)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            print('action recieved: previous')
            self.close()
        if action == ACTION_SHOW_INFO:
            self.strAction.setLabel('action recieved: show info')
        if action == ACTION_STOP:
            self.strAction.setLabel('action recieved: stop')
        if action == ACTION_PAUSE:
            self.strAction.setLabel('action recieved: pause')
            # dialog = xbmcgui.Dialog()
            # dialog.ok('action recieved', 'ACTION_PAUSE')

    def onControl(self, control):
        if control == self.button1:
            self.strButton.setLabel('button 1 clicked')
        elif control == self.button2:
            self.strButton.setLabel('button 2 clicked')
        elif isinstance(control, ControlList):
            item = control.getSelectedItem()
            self.strButton.setLabel('selected : ' + item.getLabel())
            item.setLabel(item.getLabel() + '1')
            control.focus.updateCanvas()


class KeyboardWnd(Window):
    def __init__(self):
        Window.__init__(self)
        btnKwds = dict(alignment=0x00000002|0x00000004,
                               focusTexture='KeyboardKey.png',
                               noFocusTexture='KeyboardKeyNF.png')

        rbtnKwds = dict(_alignment=0x00000002|0x00000004,
                               focusTexture='KeyboardKey.png',
                               noFocusTexture='KeyboardKeyNF.png')

        self.buffer = []
        self.ndx = 0
        self.strPane = ControlLabel(0, 0, 800, 50, '', 'font13', '0xFFFF3300', _alignment=0x00000002|0x00000004)

        self.grp1 = grp1 = ControlGroup(0, 50, 800, 50)
        btnKwds['_params'] = dict(master=grp1)
        self.btn309 = btn309 = ControlButton(0, 0, 200, 50, "Done", **btnKwds)

        self.grp2 = grp2 = ControlGroup(0, 100, 800, 50)
        rbtnKwds['_params'] = dict(master=grp2)
        self.btn302 = btn302 = ControlRadioButton(0, 0, 200, 50, 'Shift', **rbtnKwds)

        self.grp3 = grp3 = ControlGroup(0, 150, 800, 50)
        rbtnKwds['_params'] = dict(master=grp3)
        self.btn303 = btn303 = ControlRadioButton(0, 0, 200, 50, 'Caps Lock', **rbtnKwds)

        self.grp4 = grp4 = ControlGroup(0, 200, 800, 50)
        rbtnKwds['_params'] = dict(master=grp4)
        btnKwds['_params'] = dict(master=grp4)
        self.btn307 = btn307 = ControlButton(0, 0, 100, 50, 'IP', **btnKwds)
        self.btn304 = btn304 = ControlRadioButton(100, 0, 100, 50, '@#!*', **rbtnKwds)

        self.grp5 = grp5 = ControlGroup(0, 250, 800, 50)
        btnKwds['_params'] = dict(master=grp5)
        self.btn300 = btn300 = ControlButton(0, 0, 200, 50, "Done", **btnKwds)
        self.btn32 = btn32 = ControlButton(200, 0, 200, 50, 'Space', **btnKwds)
        self.btn8 = btn8 = ControlButton(400, 0, 200, 50, 'Backspace', **btnKwds)
        self.btn305 = btn305 = ControlButton(600, 0, 100, 50, '<', **btnKwds)
        self.btn306 = btn306 = ControlButton(700, 0, 100, 50, '>', **btnKwds)

        self.kb = kb = []
        grps = [grp1, grp2, grp3, grp4]
        for row in range(4):
            kbcol = []
            btnKwds['_params'] = dict(master=grps[row])
            for col in range(12):
                btn = ControlButton(200 + 50*col, 0, 50, 50, '', **btnKwds)
                kbcol.append(btn)
            kb.append(kbcol)

        # Registro
        btnKwds['_params'] = None
        self.addControl(ControlButton(0, 0, 800, 50, "", **btnKwds))
        self.addControl(self.strPane)

        self.addControl(self.grp1)
        self.addControl(btn309)
        self.addControls(kb[0][:])

        self.addControl(self.grp2)
        self.addControl(btn302)
        self.addControls(kb[1][:])

        self.addControl(self.grp3)
        self.addControl(btn303)
        self.addControls(kb[2][:])

        self.addControl(self.grp4)
        self.addControls([btn307, btn304])
        self.addControls(kb[3][:])

        self.addControl(self.grp5)
        self.addControls([btn300, btn32, btn8, btn305, btn306])

        # Navigation
        btn309.setNavigation(left=kb[0][11], right=kb[0][0], up=btn300, down=btn302)
        btn302.setNavigation(left=kb[1][11], right=kb[1][0], up=btn309, down=btn303)
        btn303.setNavigation(left=kb[2][11], right=kb[2][0], up=btn302, down=btn307)
        btn307.setNavigation(left=kb[3][11], right=btn304, up=btn303, down=btn300)
        btn304.setNavigation(left=btn307, right=kb[3][0], up=btn303, down=btn300)
        btn300.setNavigation(left=btn306, right=btn32, up=btn304, down=btn309)
        btn32.setNavigation(left=btn300, right=btn8, up=kb[3][0], down=kb[0][0])
        btn8.setNavigation(left=btn32, right=btn305, up=kb[3][4], down=kb[0][4])
        btn305.setNavigation(left=btn8, right=btn306, up=kb[3][8], down=kb[0][8])
        btn306.setNavigation(left=btn305, right=btn300, up=kb[3][10], down=kb[0][10])

        for col in range(12):
            for row in range(4):
                if col != 11:
                    kb[row][col].controlRight(kb[row][col + 1])
                    kb[row][11 - col].controlLeft(kb[row][10 - col])
                if row != 3:
                    kb[row][col].controlDown(kb[row + 1][col])
                    kb[3 - row][col].controlUp(kb[2 - row][col])

        kb[0][11].controlRight(btn309)
        kb[0][0].controlLeft(btn309)

        kb[1][11].controlRight(btn302)
        kb[1][0].controlLeft(btn302)

        kb[2][11].controlRight(btn303)
        kb[2][0].controlLeft(btn303)

        kb[3][11].controlRight(btn307)
        kb[3][0].controlLeft(btn304)

        for col in range(4):
            kb[0][col].controlUp(btn32)
            kb[3][col].controlDown(btn32)
            kb[0][col+4].controlUp(btn8)
            kb[3][col+4].controlDown(btn8)

        for col in range(2):
            kb[0][col+8].controlUp(btn305)
            kb[3][col+8].controlDown(btn305)
            kb[0][col+10].controlUp(btn306)
            kb[3][col+10].controlDown(btn306)
        self.onInit()
        pass

    def onInit(self):
        self.btn302.setSelected(False)
        self.btn303.setSelected(False)
        self.btn304.setSelected(False)

        self.strLbl = strLbl = ['1234567890', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        self.kbdLayout(strLbl)

        self.setFocus(self.btn300)

    def onAction(self, action):
        btnCode = action.getButtonCode()
        if btnCode < 256:
            letra = chr(btnCode)
            self.modOutStr(letra)

    def onControl(self, control):
        if control in [self.btn302, self.btn303, self.btn304]:
            if control.isSelected():
                for ctrl in [self.btn302, self.btn303, self.btn304]:
                    if ctrl == control:continue
                    ctrl.setSelected(False)
                if control in [self.btn302, self.btn303]:
                    self.strLbl = strLbl = ['1234567890', 'QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']
                else:
                    self.strLbl = strLbl = ['!"#$%&/()=', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
            else:
                self.strLbl = strLbl = ['1234567890', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
            self.kbdLayout(strLbl)
            return
        letra = None
        xpos, ypos = control.getX(), control.master.getY()
        if xpos >= 200 and ypos < 250:
            row = (ypos - 50)/50
            col = (xpos - 200)/50
            letra = self.strLbl[row][col]
        if control == self.btn32:
            letra = ' '
            self.modOutStr(letra)
        if control == self.btn8:
            if self.ndx == len(self.buffer):
                self.buffer.pop()
            else:
                self.buffer.pop(self.ndx)
            self.ndx -= 1
        if control == self.btn305:
            self.ndx = max(0, self.ndx - 1)
        if control == self.btn306:
            self.ndx = min(len(self.buffer), self.ndx + 1)
        self.modOutStr(letra)



    def modOutStr(self, letra=None):
        if letra:
            if self.ndx == len(self.buffer):
                self.buffer.append(letra)
            else:
                self.buffer.insert(self.ndx, letra)
            self.ndx = min(len(self.buffer), self.ndx + 1)
        buffer = ''.join(self.buffer)
        self.strPane.setLabel(buffer)
        if self.btn302.isSelected():
            self.btn302.setSelected(False)
            self.strLbl = strLbl = ['1234567890', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
            self.kbdLayout(strLbl)

    def kbdLayout(self, strLbl):
        kb = self.kb
        for row in range(4):
            lbl = strLbl[row]
            for col in range(len(lbl)):
                kb[row][col].setLabel(lbl[col])


if __name__ == '__main__':
    # root = tk.Tk()
    # # root.attributes('-fullscreen', True)
    # vbar = tk.Scrollbar(root)
    # hbar = tk.Scrollbar(root, orient='horizontal')
    # vbar.pack(side=tk.RIGHT, fill=tk.Y)
    # hbar.pack(side=tk.BOTTOM, fill=tk.X)
    # grpRoot = ControlGroup(0, 0, 100, 100)
    # grpRoot.widget = canvas = tk.Canvas(root, bg='black', takefocus=1)
    # canvas.bind('<Key>', grpRoot._onKey)
    # canvas.bind('<Button-1>', root.onMouseClick)
    # canvas.bind('<Motion>', root.onMouseMove)
    #
    # canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
    #
    # vbar.config(command=canvas.yview)
    # hbar.config(command=canvas.xview)
    # canvas.config(xscrollcommand=hbar.set)
    # canvas.config(yscrollcommand=vbar.set)
    # canvas.config(scrollregion=(0, 0, 2000, 2000))

    # rootWindow = Window()
    #
    #
    # lbl1 = ControlLabel(410, 350, 400, 200, 'Primer Label', font='font16',
    #                     textColor='yellow', disabledColor='green', _alignment=0x00000002|0x00000004)
    # rootWindow.addControl(lbl1)
    #
    # texturefocus = 'c:/testFiles/confluence/button-focus.png'
    # texturenofocus = 'c:/testFiles/confluence/button-nofocus.png'
    # btn1 = ControlButton(410, 10, 200, 40,'OK', focusTexture=texturefocus, noFocusTexture=texturenofocus,
    #                      alignment=0x00000002|0x00000004, font='font12_title',
    #                      focusedColor='white', disabledColor='grey3')
    # rootWindow.addControl(btn1)
    #
    # txtfocus = 'c:/testFiles/confluence/keyboardkey.png'
    # txtnofocus = 'c:/testFiles/confluence/keyboardkeyNF.png'
    # rtxtOn = 'c:/testFiles/confluence/radiobutton-focus.png'
    # rtxtOff = 'c:/testFiles/confluence/radiobutton-nofocus.png'
    #
    # rbtn1 = ControlRadioButton(410, 210, 200, 50, 'CAPS LOCK',
    #                            focusTexture=txtfocus, noFocusTexture=txtnofocus,
    #                            _alignment=0x00000002|0x00000004, font='font13',
    #                            disabledColor='white', focusedColor='black',
    #                            focusOnTexture=rtxtOn, noFocusOnTexture=rtxtOn,
    #                            focusOffTexture=rtxtOff, noFocusOffTexture=rtxtOff)
    # rootWindow.addControl(rbtn1)
    #
    # filename = 'c:/testFiles/confluence/defaultvideo.png'
    # img1 = ControlImage(610, 210, 256, 256, filename, colorDiffuse='C0FF0000')
    # rootWindow.addControl(img1)
    #
    # txtfocus = 'c:/testFiles/confluence/button-focus.png'
    # txtnofocus = 'c:/testFiles/confluence/button-nofocus.png'
    # chk1 = ControlCheckMark(410, 260, 200, 50, 'SCROLL LOCK',
    #                         focusTexture=txtfocus, noFocusTexture=txtnofocus,
    #                         checkWidth=30, checkHeight=30,
    #                         _alignment=0x00000002|0x00000004, font='font13',
    #                         disabledColor='white', textColor='green')
    #
    # rootWindow.addControl(chk1)
    #
    # # # grp1 = ControlGroup(410, 350, 200, 200)
    # # # grp1._registerControl(canvas)
    # #
    # # options = dict(font='font16', textColor='yellow', disabledColor='green')
    # # lbl11 = ControlLabel(0,   0, 200, 50, 'Item1', **options)
    # # lbl12 = ControlLabel(0,  50, 200, 50, 'Item2', **options)
    # # lbl13 = ControlLabel(0, 100, 200, 50, 'Item3', **options)
    # # lbl14 = ControlLabel(0, 150, 200, 50, 'Item4', **options)
    # # # for lbl in [lbl11, lbl12, lbl13, lbl14]:
    # # #     lbl._registerControl(grp1._canvas)
    #
    # # txtfocus = 'c:/testFiles/confluence/keyboardkey.png'
    # # txtnofocus = 'c:/testFiles/confluence/keyboardkeyNF.png'
    # # rtxtOn = 'c:/testFiles/confluence/radiobutton-focus.png'
    # # rtxtOff = 'c:/testFiles/confluence/radiobutton-nofocus.png'
    # #
    # # kmax = 12
    # # grpk = ControlGroup(10,10, 200, 200)
    # # rootWindow.addControl(grpk)
    # # rbtn = []
    # # for k in range(kmax):
    # #     rbtnx = ControlRadioButton(0, k*50, 200, 50, 'Radio' + str(k),
    # #                            focusTexture=txtfocus, noFocusTexture=txtnofocus,
    # #                            _alignment=0x00000002|0x00000004, font='font13',
    # #                            disabledColor='white', focusedColor='black',
    # #                            focusOnTexture=rtxtOn, noFocusOnTexture=rtxtOn,
    # #                            focusOffTexture=rtxtOff, noFocusOffTexture=rtxtOff)
    # #     grpk._registerControl(rbtnx)
    # #     rbtn.append(rbtnx)
    # #
    # #
    # #
    # # for k in range(1, kmax - 1):
    # #     rbtnx = rbtn[k]
    # #     rbtnx.setNavigation(up=rbtn[k-1], down=rbtn[k+1])
    # # rbtn[0].setNavigation(up=rbtn[-1], down=rbtn[1])
    # # rbtn[-1].setNavigation(up=rbtn[-2], down=rbtn[0])
    #
    # grpk = ControlList(10,10, 400, 400, textColor='yellow', selectedColor='white',
    #                     _imageWidth=20, _imageHeight=20,
    #                     buttonFocusTexture='keyboardkey.png',
    #                     buttonTexture='floor_button.png',
    #                     _space=10, _itemHeight=40, _alignmentY=0x00000004,
    #                     _itemTextXOffset=10, _itemTextYOffset=40)
    #
    # rootWindow.addControl(grpk)
    #
    # for i in range(50):
    #     listitem = ListItem('item' + str(i), iconImage='icon_home.png', thumbnailImage='icon_back.png')
    #     listitem.setLabel2('test')
    #     listitem.setInfo(type='video', infoLabels={'Title':'movie', 'playcount':2})
    #     listitem.select(True)
    #     grpk.addItem(listitem)
    #
    # grpk.setNavigation(right=btn1, left=btn1)
    # btn1.setNavigation(left=grpk, down=rbtn1)
    # rbtn1.setNavigation(up=btn1)
    # rootWindow.show()

    # rootWindow = KeyboardWnd()
    # rootWindow.show()

    rootWindow = testWindow()
    rootWindow.show()

    # class myWindowXml(WindowXML):
    #     def __init__(self, filename):
    #         WindowXML.__init__(self, filename, '')



    # filename = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons\plugin.video.xbmcmodule\resources\skins\Default\720p\testCase.xml'
    # rootWindow = myWindowXml(filename)
    # rootWindow.show()
    # dlg = Dialog()
    # dlg.ok('ESTO ES EL ENCABEZADO', 'Esta es la primera linea', 'Esta la segunda', 'Esta la tercera')
    # rta = dlg.yesno('DIALOGO YESNO', 'Esta es la primera linea', 'Esta la segunda', 'Esta la tercera', nolabel='CANCEL')
    # rta = dlg.numeric(3, 'Entre el numero de identificacion')
    # print rta



