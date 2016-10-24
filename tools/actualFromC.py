import os
import sys
import shutil
import urllib2
import re

def actualKey():
    url = r'https://github.com/xbmc/xbmc/blob/master/xbmc/input/Key.h'
    pattern1 = r'class="pl-en">(?P<key>[A-Z_0-9]+)</span>.+?(?:class="pl-c1">)*(?P<value>[xXA-F0-9]+)(?:</span>)*'
    header = """'''
            Archivo generado desde: %s
'''
    """

    content = urllib2.urlopen(url).read()
    matchs = re.findall(pattern1, content)

    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'key.py')

    nchar = max(map(lambda  x: len(x[0]), matchs))
    strFmt = '\n{0:<%s} = {1}' % nchar

    with open(filename, 'w') as f:
        f.write(header % url)
        for key, value in matchs:
            f.write(strFmt.format(key, value))

def actualWindowIDs():
    url = r'https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/WindowIDs.h'
    pattern1 = r'class="pl-en">(?P<key>[A-Z_0-9]+)</span> +(?P<pfx>[(A-Z_0-9)+]*)(?:<span class="pl-c1">)*(?P<value>[0-9]*)(?:</span>)*(?P<sfx>\)*)'
    # pattern2 = r'class="pl-en">(?P<key>[A-Z_0-9]+)</span> +?(?P<pfx>[()A-Z_0-9+]+)</td>'
    # pattern3 = r'class="pl-en">(?P<key>[A-Z_0-9]+)</span> +?(?P<pfx>[(A-Z_0-9)+]+)<span class="pl-c1">(?P<value>[0-9]+)</span>(?P<sfx>\))'
    header = """'''
            Archivo generado desde: %s
'''
    """

    content = urllib2.urlopen(url).read()
    matchs = re.findall(pattern1, content)
    matchs = map(lambda x: (x[0], ''.join(x[1:])), matchs)

    # ext1   = re.findall(pattern2, content)
    # matchs.extend(ext1)
    #
    # ext2   = re.findall(pattern3, content)
    # ext2 = map(lambda x: (x[0], ''.join(x[1:])), ext2)
    # matchs.extend(ext2)

    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'WindowIDs.py')
    # filename = r'c:/testFiles/code.txt'

    nchar = max(map(lambda  x: len(x[0]), matchs))
    strFmt = '\n{0:<%s} = {1:>5}' % nchar

    # if os.path.exists(filename): shutil.copyfile(filename, filename + '.old')
    with open(filename, 'w') as f:
        f.write(header % url)
        for key, value in matchs:
            f.write(strFmt.format(key, value))

def actualKeysym():
    url = r'https://github.com/xbmc/xbmc/blob/master/xbmc/input/XBMC_keysym.h'
    pattern1 = r'js-file-line"> +(?P<key>X[A-Z_0-9a-z]+)[ =]+(?:<span class="pl-c1">)*(?P<value>[xXA-Fa-f0-9]+)(?:</span>)*'
    pattern2 = r'class="pl-en">(?P<key>[A-Z_0-9]+)</span> +(?P<value>\([A-Z_0-9 |]+\))</td>'
    # pattern3 = r'class="pl-en">(?P<key>[A-Z_0-9]+)</span> +?(?P<pfx>[(A-Z_0-9)+]+)<span class="pl-c1">(?P<value>[0-9]+)</span>(?P<sfx>\))'
    header = """'''
            Archivo generado desde: %s
'''
    """

    content = urllib2.urlopen(url).read()
    matchs = re.findall(pattern1, content)

    ext1   = re.findall(pattern2, content)
    matchs.extend(ext1)

    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'Keysym.py')
    # filename = r'c:/testFiles/code.txt'

    nchar = max(map(lambda  x: len(x[0]), matchs))
    strFmt = '\n{0:<%s} = {1:>6}' % nchar

    with open(filename, 'w') as f:
        f.write(header % url)
        for key, value in matchs:
            f.write(strFmt.format(key, value))

def actualVkeys():
    url = r'https://github.com/xbmc/xbmc/blob/master/xbmc/input/XBMC_vkeys.h'
    pattern1 = r'js-file-line"> +(?P<key>[A-Z_0-9]+)[ =]+(?:<span class="pl-c1">)*(?P<value>[xXA-F0-9]+)(?:</span>)*'
    header = """'''
            Archivo generado desde: %s
'''
    """

    content = urllib2.urlopen(url).read()
    matchs = re.findall(pattern1, content)

    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'Vkeys.py')

    nchar = max(map(lambda  x: len(x[0]), matchs))
    strFmt = '\n{0:<%s} = {1:>6}' % nchar

    with open(filename, 'w') as f:
        f.write(header % url)
        for key, value in matchs:
            f.write(strFmt.format(key, value))


def actualButtonTranslator():
    url = r'https://github.com/xbmc/xbmc/blob/master/xbmc/input/ButtonTranslator.cpp'
    pattern1 = r'&quot;</span>(?P<key>[a-z0-9]+)<span.+?>&quot;.+?, (?P<value>[A-Z_0-9]+)'
    pattern2 = r'ActionMapping (.+?)\[\]'
    header = """'''
            Archivo generado desde: %s
'''

from key import *
from WindowIDs import *
    """

    content = urllib2.urlopen(url).read()
    matchs  = re.findall(pattern1, content)
    mapobjs = re.findall(pattern2, content)

    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'ButtonTranslator.py')
    # filename = r'c:/testFiles/code.txt'

    nchar = max(map(lambda  x: len(x[0]), matchs)) + 2
    strFmt = '\n\t\t\t{0:<%s} : {1},' % nchar

    # if os.path.exists(filename): shutil.copyfile(filename, filename + '.old')
    splt = ''
    k = 0
    with open(filename, 'w') as f:
        f.write(header % url)
        for key, value in matchs:
            if value.split('_', 1)[0] != 'REMOTE' and splt != value.split('_', 1)[0]:
                splt = value.split('_', 1)[0]
                if k > 0:f.write('\n}')
                f.write(2*'\n' + mapobjs[k] + ' = {')
                k += 1
            f.write(strFmt.format(('# ' if splt == 'APPCOMMAND' else '') + "'" + key + "'", value))
        f.write('\n}')

def actualKeytable():
    url = r'https://github.com/xbmc/xbmc/blob/master/xbmc/input/XBMC_keytable.cpp'
    pattern1 = r'(?P<key1>X[A-Z_0-9a-z]+).+?(?P<key2>X[A-Z_0-9a-z]+).+?&quot;</span>(?P<key3>[A-Z_0-9a-z]+)<span class="pl-pds">&quot;'
    header = """'''
            Archivo generado desde: %s
'''

from Keysym import *
from Vkeys import *
from TkinterKeys import *

XBMCK,  VK,  XBMCVK,  NAME = range(4)
_xbmck, _vk, _xbmcvk, _name = [], [], [], []

_add = lambda a, b, c, d: (_xbmck.append(a), _vk.append(b), _xbmcvk.append(c), _name.append(d))

def lookup(lookup_value, indx):
	indx = max(0, min(3, indx))
	colValues = (_xbmck, _vk, _xbmcvk, _name)[indx]
	try:
		npos = colValues.index(lookup_value)
	except:
		return None
	return _xbmck[npos], _vk[npos], _xbmcvk[npos], _name[npos]

"""
    content = urllib2.urlopen(url).read()
    matchs = re.findall(pattern1, content)

    path = os.path.dirname(__file__)
    filename = os.path.join(path, 'Keytable.py')

    nchar = []
    for k in range(3):
        nchar.append(max(map(lambda  x: len(x[k]), matchs)))
    strFmt = '\n_add({0:>%s}, {1:>%s}, {2:>%s}, {3:>%s})' % (nchar[0], nchar[0] - 3, nchar[1], nchar[2] + 2)

    with open(filename, 'w') as f:
        f.write(header % url)
        for key1, key2, key3 in matchs:
            f.write(strFmt.format(key1, 'V' + key1[4:], key2, '"%s"' % key3))

if __name__ == '__main__':
    # actualKey()
    # actualWindowIDs()
    actualKeysym()
    # actualVkeys()
    # actualButtonTranslator()
    # actualKeytable()