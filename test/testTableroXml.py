import os
import re
import sys

sys.path.append(os.path.abspath('..'))
from fromC import key as kodiKeyh
from toClasify import gui02 as xbmcgui

keyMap = dict((getattr(kodiKeyh, akey), akey) for akey in dir(kodiKeyh) if akey.startswith('ACTION_'))
_action = dict([('0x{:04x}'.format(ival), x) for x, ival in kodiKeyh.__dict__.items() if x.startswith('ACTION_')])


class testTablero(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self, *args, **kwargs)

    def getActionStr(self, aval, prefix='ACTION_'):
        actVal = '0x{:04x}'.format(aval)
        return _action.get(actVal, actVal)

    def onAction(self, action):
        actionID = action.getId()
        try:
            actionName = self.getActionStr(actionID)
        except:
            dlg = xbmcgui.Dialog()
            dlg.ok('Error en getActionStr', '\n'.join([str(action), str(type(action))]))
            return

        try: btCode = action.getButtonCode()
        except: btCode = 'ERROR'
        try: amnt1 = action.getAmount1()
        except: amnt1 = 'ERROR'
        try: amnt2 = action.getAmount2()
        except: amnt2 = 'ERROR'
        ctrl = self.getControl(100 + 10*1)
        lstAction = ctrl.getLabel()
        if lstAction != actionName:
            self.recAction()
            number = 1
            if self.getListSize() == 15:
                self.removeItem(14)
            self.addItem(xbmcgui.ListItem(label=actionName), position=0)
        else:
            ctrl = self.getControl(100 + 10*5)
            number = int(ctrl.getLabel() or '0') + 1

        toDisplay = map(str, [actionName, btCode, amnt1, amnt2, number])
        self.displayAction(*toDisplay)

        if actionName in ['ACTION_MOUSE_LEFT_CLICK', 'ACTION_SELECT_ITEM']:
            try:
                ctrl = self.getFocus()
            except:
                msg = 'No control in focus'
            else:
                msg = '\n'.join([str(ctrl.getId()), str(ctrl)])
            dlg = xbmcgui.Dialog()
            dlg.ok('Focused Control', msg)

        if actionName in ['ACTION_PARENT_DIR', 'ACTION_PREVIOUS_MENU', 'ACTION_NAV_BACK', 'ACTION_X']:
            self.onClose()

    def onControl(self, control):
        self._onEvent('onControl', control)

    def onClick(self, control):
        """onClick method.

        This method will recieve all click events that the main program will send to this window.
        """
        self._onEvent('onClick', control)

    def onDoubleClick(self, control):
        self._onEvent('onDoubleClick', control)

    def onFocus(self, control):
        """onFocus method.

        This method will recieve all focus events that the main program will send to this window.
        """
        self._onEvent('onFocus', control)

    def onClose(self):
        self.close()

    def _onEvent(self, strId, control):
        ctrl = self.getControl(200)
        ctrl.setLabel(strId)
        if control and isinstance(control, int):
            control = self.getControl(control)
            tipo = re.search(r'Control[A-Z][a-z]+', str(type(control)))
            if tipo:
                tipo = tipo.group() + (' ' + str(control.getId()) if control.getId() else ' @NA')
        else:
            tipo = '@NA'
        ctrl = self.getControl(210)
        ctrl.setLabel(tipo)

        self.recAction()

        if self.getListSize() == 15:
            self.removeItem(14)
        self.addItem(xbmcgui.ListItem(label='%s %s' % (strId, tipo)), position=0)

    def recAction(self):
        try:
            ctrl = self.getControl(100 + 10*5)
            number = int(ctrl.getLabel() or '0')
        except:
            number = 0
        if number == 0: return
        ctrl = self.getControl(100 + 10*1)
        lstAction = ctrl.getLabel()
        litem = self.getListItem(0)
        litem.setLabel('%s %s' % (lstAction, number))
        self.displayAction()


    def displayAction(self, actionName='', btCode='', amnt1='', amnt2='', number=''):
        toDisplay = (actionName, btCode, amnt1, amnt2, number)
        for k in range(5):
            ctrlId = 100 + 10*(k + 1)
            try:
                ctrl = self.getControl(ctrlId)
                ctrl.setLabel(toDisplay[k])
            except:
                msg = '\n'.join([str(k+1), toDisplay[k]])
                dlg = xbmcgui.Dialog()
                dlg.ok('getControl', msg)
                return

if __name__ == '__main__':
    w = testTablero('tablero.xml', '', defaultSkin='', defaultRes='')
    w.doModal()

