import os
import sqlite3
import pickle
import pprint
import xbmcaddon

''' Agregate Functions'''

class lista(object):
    def __init__(self):
        self.innList = []
    def step(self, *args):
        self.innList.append(args)
    def finalize(self, *args):
        return pickle.dumps(self.innList)

class diccio(object):
    def __init__(self):
        self.inndict = {}
    def step(self, key, value):
        self.inndict[key] = value
    def finalize(self, *args):
        return pickle.dumps([self.inndict])

'''Adapter functions'''

def adapter_func(obj):
    return pickle.dumps(obj)

def converter_func(data):
    return pickle.loads(data)


sqlite3.register_adapter(list, adapter_func)
sqlite3.register_converter('list', converter_func)


def initAddonDb(conn):
    addonsDir = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons'
    c = conn.cursor()
    sqlStr = 'create table enabled (id integer primary key, addonID text)'
    try:
        c.execute(sqlStr)
    except:
        sqlStr = 'delete from enabled'
        c.execute(sqlStr)
    sqlStr = 'select distinct addonID from addon'
    c.execute(sqlStr)

    answ = c.fetchall()
    answ = [elem[0] for elem in answ]
    enabledAdd = os.walk(addonsDir).next()[1]
    for addonID in enabledAdd:
        if addonID not in answ:
            xmlfile = os.path.join(addonsDir, addonID, 'addon.xml')
            if not os.path.exists(xmlfile): continue
            addon = xbmcaddon.Addon(addonID)
            keys = ['type', 'name', 'summary', 'description', 'stars', 'path', 'id', 'icon', 'version', 'changelog', 'fanart',
                    'language', 'provides','author', 'disclaimer']

            fldsVal = dict(zip(keys, map(addon.getAddonInfo, keys)))
            fldsVal['addonID'] = fldsVal.pop('id')
            fldsVal['stars'] = int(fldsVal['stars'])
            fldsVal['minversion'] = '0.0.0'
            keys = ['type', 'name', 'summary', 'description', 'stars', 'path', 'addonID', 'icon', 'version', 'changelog', 'fanart', 'author', 'disclaimer', 'minversion']
            sqlStr = 'insert into addon ({0}) values ({1})'.format(', '.join(keys), ':' + ', :'.join(keys))
            c.execute(sqlStr, fldsVal)
        sqlStr = 'insert into enabled (addonID) values ("{}")'
        c.execute(sqlStr.format(addonID))

    toInsert = [addonID for addonID in enabledAdd if addonID not in answ]
    pprint.pprint(toInsert)
    pass



def addonView(dbFile):
    conn.create_aggregate('diccio', 2, diccio)
    conn.create_aggregate('lista', 3, lista)
    # conn.row_factory = sqlite3.Row

    c = conn.cursor()
    viewExtra = 'create temp view extrainfoView as select id, value as content, diccio(key, value) as extrainfo from addonextra group by id'
    c.execute(viewExtra)

    viewDep = 'create temp view dependenciesView as select id, lista(addon, version, optional) as dependencies from dependencies group by id'
    c.execute(viewDep)

    viewAddon = 'create temp view addonView as ' \
                'select addon.addonID, type, name, version, summary, description, path, author, icon as thumbnail, ' \
                'disclaimer, fanart, stars as rating, dependencies, extrainfo, content, ' \
                'broken.id is not null as broken, enabled.id is not null as enabled ' \
                'from addon ' \
                'join dependenciesView on addon.id=dependenciesView.id ' \
                'join extrainfoView on addon.id=extrainfoView.id ' \
                'left outer join broken on addon.addonID=broken.addonID ' \
                'left outer join enabled on addon.addonID=enabled.addonID '

    c.execute(viewAddon)

    pass


if __name__ =='__main__':
    dbFile = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\userdata\Database\Addons19.db'
    with sqlite3.connect(dbFile, detect_types=sqlite3.PARSE_COLNAMES) as conn:
        initAddonDb(conn)
        addonView(conn)
        c = conn.cursor()
        # sqlStr = 'select addonID, type, dependencies as "dependencies [list]", extrainfo as "extrainfo [list]", ' \
        #          'rating, enabled, broken ' \
        #          'from addonView ' \
        #          'where content like "%video%" ' \
        #          'order by enabled desc ' \
        #          'limit 5'
        sqlStr = 'select * from enabled'


        # sqlStr = 'select addonID, type, enabled, broken ' \
        #          'from addonView ' \
        #          'where addonID like "plugin.video.%ide" ' \
        #          'order by addonID asc '

        c.execute(sqlStr)
        answ = c.fetchall()
        pprint.pprint(answ)

    pass
