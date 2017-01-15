import os
import re
import sys

sys.path.append(os.path.abspath('..'))
from fromC import key as kodiKeyh
from toClasify import gui02 as xbmcgui

keyMap = dict((getattr(kodiKeyh, akey), akey) for akey in dir(kodiKeyh) if akey.startswith('ACTION_'))
_action = dict([('0x{:04x}'.format(ival), x) for x, ival in kodiKeyh.__dict__.items() if x.startswith('ACTION_')])

class Window(xbmcgui.Window):
    def __init__(self):
        super(Window, self).__init__()
        img = xbmcgui.ControlImage(20, 20, 920, 100, 'floor_button.png')
        self.addControl(img)
        lbls = [(40, 50, 100, 40, 'onAction', 'font14', 'yellow'),
                (160, 30, 300, 40, 'ActionID', 'font13', 'red'),
                (480, 30,100, 40, 'ButtonCode', 'font13', 'red'),
                (600, 30,100, 40, 'Amount1', 'font13', 'red'),
                (720, 30,100, 40, 'Amount2', 'font13', 'red'),
                (840, 30,100, 40, 'Number', 'font13', 'red')]
        for lbl in lbls:
            ctrl = xbmcgui.ControlLabel(*lbl)
            self.addControl(ctrl)

        lbls = [(160, 70, 300, 40, 'ActionID', 'font13', 'white'),
                (480, 70,100, 40, 'ButtonCode', 'font13', 'white'),
                (600, 70,100, 40, 'Amount1', 'font13', 'white'),
                (720, 70,100, 40, 'Amount2', 'font13', 'white'),
                (840, 70,100, 40, 'Number', 'font13', 'lime')]
        self.lblCtrls = []
        for lbl in lbls:
            ctrl = xbmcgui.ControlLabel(*lbl)
            self.addControl(ctrl)
            self.lblCtrls.append(ctrl)

        img = xbmcgui.ControlImage(960, 20, 260, 100, 'floor_button.png')
        self.addControl(img)
        lbls = [(980, 20, 260, 100, 'onControl', 'font14', 'yellow'),
                (980, 70, 260, 100, 'actionID', 'font13', 'lime')]
        for lbl in lbls:
            ctrl = xbmcgui.ControlLabel(*lbl)
            self.addControl(ctrl)
            self.lblCtrls.append(ctrl)

        self.addControl(xbmcgui.ControlImage(0, 120, 720, 576, 'background.png'))
        self.list = xbmcgui.ControlList(500, 150, 400, 300,
                                        textColor='yellow', selectedColor='green',
                                        _imageWidth=20, _imageHeight=20,
                                        buttonFocusTexture='floor_buttonFO.png',
                                        buttonTexture='floor_button.png',
                                        _space=10,
                                        _itemTextXOffset=0, _itemTextYOffset=0)

        self.addControl(self.list)

        self.button1 = xbmcgui.ControlButton(50, 270, 200, 30, "Button 1")
        self.button2 = xbmcgui.ControlButton(50, 320, 200, 30, "Button 2")
        self.chkbutton = xbmcgui.ControlCheckMark(50, 370, 200, 30, "Check Button")
        self.radiobutton = xbmcgui.ControlRadioButton(50, 420, 200, 50, "Radio Button")
        self.slider = xbmcgui.ControlSlider(50, 480, 200, 50)
        self.textbox = xbmcgui.ControlTextBox(500, 520, 200, 100)
        self.edit = xbmcgui.ControlEdit(500, 520, 200, 100, 'Esto es el Label',
                                        textColor='yellow', disabledColor='red')


        self.addControl(self.button1)
        self.addControl(self.button2)
        self.addControl(self.chkbutton)
        self.addControl(self.radiobutton)
        self.addControl(self.slider)
        self.addControl(self.textbox)
        self.addControl(self.edit)


        self.button1.controlDown(self.button2)
        self.button1.controlRight(self.list)
        self.button2.controlUp(self.button1)
        self.button2.controlRight(self.list)
        self.list.controlLeft(self.button1)

        self.slider.setPercent(80)
        self.textbox.setText('Lina1\nLinea2[CR]linea3')
        # self.edit.setLabel('Esto es LABEL')
        self.edit.setText('Esto es TEXTO')

        # add a few items to the list
        # xbmcgui.lock()

        for i in range(20):
            listitem = xbmcgui.ListItem('item' + str(i), iconImage='icon_home.png', thumbnailImage='icon_back.png')
            listitem.setLabel2('test')
            listitem.setInfo(type='video', infoLabels={'Title':'movie', 'playcount':2})
            listitem.select(True)
            self.list.addItem(listitem)
        # self.ctrlGrp1.addItem(xbmcgui.ControlLabel(0, 0, 300, 50, 'En CtrlGrp1', 'font13', '0xFFFFFFFF'))
        # xbmcgui.unlock()
        self.setFocus(self.button1)

    def getActionStr(self, aval, prefix='ACTION_'):
        actVal = '0x{:04x}'.format(aval)
        return _action.get(actVal, actVal)

    def onAction(self, action):
        actionID = action.getId()
        try:
            actionName = self.getActionStr(actionID)
        except:
            dlg = xbmcgui.Dialog()
            dlg.ok('Error en getActionStr', '\n'.join([str(action), type(action)]))
            return

        try: btCode = action.getButtonCode()
        except: btCode = 'ERROR'
        try: amnt1 = action.getAmount1()
        except: amnt1 = 'ERROR'
        try: amnt2 = action.getAmount2()
        except: amnt2 = 'ERROR'
        ctrl = self.lblCtrls[0]
        lstAction = ctrl.getLabel()
        if lstAction != actionName:
            number = 1
            self.list.removeItem(0)
            self.list.addItem(actionName)
        else:
            ctrl = self.lblCtrls[4]
            number = int(ctrl.getLabel() or '0') + 1
        toDisplay = map(str, [actionName, btCode, amnt1, amnt2, number])

        for k in range(5):
            try:
                ctrl = self.lblCtrls[k]
                ctrl.setLabel(toDisplay[k])
            except:
                msg = '\n'.join([str(k+1), toDisplay[k]])
                dlg = xbmcgui.Dialog()
                dlg.ok('getControl', msg)
                return


        key = action.getId()
        actionStr = keyMap[key]

    def onControl(self, control):
        self._onEvent('onControl', control)

    def onClick(self, control):
        """onClick method.

        This method will recieve all click events that the main program will send to this window.
        """
        self._onEvent('onClick', control)
        pass

    def onDoubleClick(self, control):
        self._onEvent('onDoubleClick', control)
        pass

    def onFocus(self, control):
        """onFocus method.

        This method will recieve all focus events that the main program will send to this window.
        """
        self._onEvent('onFocus', control)
        pass

    def _onEvent(self, strId, control):
        # self.list.removeItem(0)
        # self.list.addItem(strId)

        ctrl = self.lblCtrls[-2]
        ctrl.setLabel(strId)
        if control:
            if isinstance(control, int):
                control = self.getControl(control)
            tipo = re.search(r'Control[A-Z][a-z]+', str(type(control)))
            if tipo:
                tipo = tipo.group() + (' ' + str(control.getId()) if control.getId() else ' @NA')
        else:
            tipo = '@NA'
        ctrl = self.lblCtrls[-1]
        ctrl.setLabel(tipo)

if __name__ == '__main__':
    w = Window()
    w.doModal()
