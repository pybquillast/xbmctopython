# xbmctopython
Porting XBMC modules to python. Following steps in xbmcstubs.

## Description

This project has 7 python modules

The basic modules are: xbmc.py, xbmcaddon.py, xbmcplugin.py, xbmcgui.py and xbmcvfs.py.

This modules are the XBMC (KODI) modules and contains python code of some/all the members in it. Check the files to verify the objects that are ported in this version

The complementary modules: 
- KodiScriptImporter.py: This module is used to install a hook in the python importer system that makes available the basic modules and the Kodi Script modules
- KodiServer.py: This module is used wih two purposes. The first, as a run module to test the KodiScriptImporter system with the video addons installed in your system. The second. as a debug module, to place breakpoints in the addon you are going to test and verify all you need.

## Requirements
This project has been tested in a system with the following characteristics:
- Windows Vista SP2
- Python 2.7.9
- Chrome Browser (For KodiServer client)

## Installation
- Clone the repository to a directory in your system
- Make the directory of the first step available throught python path.

## KodiScriptImporter Interactive Session Setup

If you clone the repository, for example, to the  directory **c:/modxbmcpy** in your system.

- Start an interactive session

- Make available **c:/modxbmcpy** to python trought python path
```
    >>> import sys
    >>> sys.path.append('c:/modxbmcpy')
```
- Create and install an importer instance
```
    >>> from KodiImporter import KodiScriptImporter as ksi
    >>> importer = ksi.KodiScriptImporter()       # For Win x86 users. See module for details
    >>> importer.install()                        # Installed as a metha path importer
```
- Verify the installation (optional)                      
```
    >>> import xbmc
    >>> xbmc.translatePath(**'special://home'**)
```
- If you have metahandler installed in your system you can try this:
```
    >>> import metahandler
    >>> from metahandler import metahandlers
    >>> md = metahandlers.MetaData()
    >>> md.get_meta('movie', 'mad max fury road', year='2015')
```    
- You will get something like this:

{'rating': 8.2, 'year': 2015, 'duration': u'7200', 
'plot': u"An apocalyptic story set in the furthest reaches of our planet, in a stark desert landscape where humanity is broken, and 
          most everyone is crazed fighting for the necessities of life. Within this world ...", 
'votes': u'370,371', 'title': 'mad max fury road', 'tagline': u'What a Lovely Day.', 
'writer': u'George Miller, Brendan McCarthy, Nick Lathouris', 'imgs_prepacked': u'false', 
'backdrop_url': u'http://image.tmdb.org/t/p/original/tbhdm8UJAb4ViCTsulYFL3lxMCd.jpg', 'tmdb_id': u'76341', 
'cover_url': u'http://image.tmdb.org/t/p/w342/kqjL17yufvn9OVLyXYpvtyrFfak.jpg', 'imdb_id': u'tt1392190', 
'director': u'George Miller', 'studio': u'', 'genre': u'Thriller / Action / Adventure', 'thumb_url': u'', 'overlay': 6, 
'premiered': u'2015-05-15', 
'cast': [(u'Tom Hardy', u'Max Rockatansky'), (u'Charlize Theron', u'Imperator Furiosa'), ...], 
'mpaa': u'R', 'playcount': 0, 'trailer_url': u'2h6IKpgFixg', 
'trailer': u'plugin://plugin.video.youtube/?action=play_video&videoid=2h6IKpgFixg'}

## KodiServer Interactive Session Setup

- Check the importer installation that you test in KodiScriptImporter Interactive Session Setup
```
    >>> import sys
    >>> sys.path.append('c:/modxbmcpy')
    >>> from KodiImporter import KodiServer as ks
    >>> httpd = ks.runServer()   # Here you must apply the same parameters that you use for KodiScriptImporter
```
- Now your default webbrowser must open in the address localhost:5000
- The webbrowser must show all your installed addons in groups: video, audio (music), image (picture) and executable (program)
- Click the addon you want to open. The audio and executable addons are based, specially when show the media, in the widgets defined in xbmcgui which are not ported yet
- For stop the server
```
    >>> httpd.shutdown()                     # Stop the server
    >>> httpd.server_close()                 # Close the socket
```



                          

