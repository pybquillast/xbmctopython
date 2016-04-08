'''
Created on 9/05/2014

@author: pybquillast

This module has been ported from xbmcstubs:

__author__ = 'Team XBMC <http://xbmc.org>'
__credits__ = 'Team XBMC'
__date__ = 'Thu Apr 17 08:03:38 BST 2014'
__platform__ = 'ALL'
__version__ = '2.14.0'


'''
import sys
import os
import re
import time
import xbmcgui

# variables
special_xbmc = None
special_home = None
xbmcLoglevel = -1

#
#    CONSTANTS
#

CAPTURE_FLAG_CONTINUOUS = 1
CAPTURE_FLAG_IMMEDIATELY = 2
CAPTURE_STATE_DONE = 3
CAPTURE_STATE_FAILED = 4
CAPTURE_STATE_WORKING = 0
DRIVE_NOT_READY = 1
ENGLISH_NAME = 2
ISO_639_1 = 0
ISO_639_2 = 1

LOGDEBUG = 0
LOGINFO = 1
LOGNOTICE = 2
LOGWARNING = 3
LOGERROR = 4
LOGSEVERE = 5
LOGFATAL = 6
LOGNONE = 7
PLAYER_CORE_AUTO = 0
PLAYER_CORE_DVDPLAYER = 1
PLAYER_CORE_MPLAYER = 2
PLAYER_CORE_PAPLAYER = 3
PLAYLIST_MUSIC = 0
PLAYLIST_VIDEO = 1
SERVER_AIRPLAYSERVER = 2
SERVER_EVENTSERVER = 6
SERVER_JSONRPCSERVER = 3
SERVER_UPNPRENDERER = 4
SERVER_UPNPSERVER = 5
SERVER_WEBSERVER = 1
SERVER_ZEROCONF = 7
TRAY_CLOSED_MEDIA_PRESENT = 96
TRAY_CLOSED_NO_MEDIA = 64
TRAY_OPEN = 16
abortRequested = False

#
#    Class
#

class InfoTagMusic(object):
    '''
    Kodi's music info tag class.

    To get music info tag data of currently played source.

    Note
    Info tag load is only be possible from present player class.
    Example:

    1 ...
    2 tag = xbmc.Player().getMusicInfoTag()
    3
    4 title = tag.getTitle()
    5 url   = tag.getURL()
    6 ...
    '''
    def getAlbum(self):
        """
        --returns a string.
        """
        pass

    def getAlbumArtist(self):
        """
        --returns a string.
        """
        pass

    def getArtist(self):
        """
        --returns a string.
        """
        pass

    def getComment(self):
        """
        --returns a string.
        """
        pass

    def getDisc(self):
        """
        --returns a integer.
        """
        pass

    def getDuration(self):
        """
        --returns a integer.
        """
        pass

    def getGenre(self):
        """
        --returns a string.
        """
        pass

    def getLastPlayed(self):
        """
        --returns a string.
        """
        pass

    def getListeners(self):
        """
        --returns a integer.
        """
        pass

    def getLyrics(self):
        """
        --returns a string.
        """
        pass

    def getPlayCount(self):
        """
        --returns a integer.
        """
        pass

    def getReleaseDate(self):
        """
        --returns a string.
        """
        pass

    def getTitle(self):
        """
        --returns a string.
        """
        pass

    def getTrack(self):
        """
        --returns a integer.
        """
        pass

    def getURL(self):
        """
        --returns a string.
        """
        pass

class InfoTagVideo(object):
    '''
    Kodi's video info tag class.

    To get video info tag data of currently played source.

    Note
    Info tag load is only be possible from present player class.

    Example:

    1 ...
    2 tag = xbmc.Player().getVideoInfoTag()
    3
    4 title = tag.getTitle()
    5 file  = tag.getFile()
    6 ...

    '''

    def getCast(self):
        """
        --returns a string.
        """
        pass

    def getDirector(self):
        """
        --returns a string.
        """
        pass

    def getFile(self):
        """
        --returns a string.
        """
        pass

    def getFirstAired(self):
        """
        --returns a string.
        """
        pass

    def getGenre(self):
        """
        --returns a string.
        """
        pass

    def getIMDBNumber(self):
        """
        --returns a string.
        """
        pass

    def getLastPlayed(self):
        """
        --returns a string.
        """
        pass

    def getOriginalTitle(self):
        """
        --returns a string.
        """
        pass

    def getPath(self):
        """
        --returns a string.
        """
        pass

    def getPictureURL(self):
        """
        --returns a string.
        """
        pass

    def getPlayCount(self):
        """
        --returns a integer.
        """
        pass

    def getPlot(self):
        """
        --returns a string.
        """
        pass

    def getPlotOutline(self):
        """
        --returns a string.
        """
        pass

    def getPremiered(self):
        """
        --returns a string.
        """
        pass

    def getRating(self):
        """
        --returns a float (double where supported).
        """
        pass

    def getTagLine(self):
        """
        --returns a string.
        """
        pass

    def getTitle(self):
        """
        --returns a string.
        """
        pass

    def getVotes(self):
        """
        --returns a string.
        """
        pass

    def getWritingCredits(self):
        """
        --returns a string.
        """
        pass

    def getYear(self):
        """
        --returns a integer.
        """
        pass

class Keyboard(object):
    def __init__(self, default = '', heading = '', hidden = False):
        """
        --Creates a newKeyboard object with default text
        heading and hidden input flag if supplied.

        default : [opt] string - default text entry.
        heading : [opt] string - keyboard heading.
        hidden : [opt] boolean - True for hidden text entry.

        example:

            - kb =xbmc.Keyboard ('default', 'heading', True)
            - kb.setDefault('password') # optional
            - kb.setHeading('Enter password') # optional
            - kb.setHiddenInput(True) # optional
            - kb.doModal()
            - if (kb.isConfirmed()):
            - text = kb.getText()
        """
        self._default = default
        self._heading = heading
        self._hidden = hidden
        self._isConfirmed = False

    def doModal(self, autoclose = 0):
        """
        --Show keyboard and wait for user action.
        autoclose : [opt] integer - milliseconds to autoclose dialog. (default=do not autoclose)
        example:
            - kb.doModal(30000)
        """
        dialog = xbmcgui.Dialog()
        self._text = dialog.input(self._heading + ': ')
        # self._text = raw_input(self._heading + ': ')
        self._isConfirmed = True

    def getText(self):
        """
        --Returns the user input as a string.
        Note, This will always return the text entry even if you cancel the keyboard.
        Use theisConfirmed() method to check if user cancelled the keyboard.

        example:
            - text = kb.getText()
        """
        return self._text

    def isConfirmed(self):
        """
        --Returns False if the user cancelled the input.
        example:
            - if (kb.isConfirmed()):
        """
        return self._isConfirmed

    def setDefault(self, default):
        """
        --Set the default text entry.
        default : string - default text entry.
        Example:
            - kb.setDefault('password')
        """
        self._default = default

    def setHeading(self, heading):
        """
        --Set the keyboard heading.
        heading : string - keyboard heading.
        example:
            - kb.setHeading('Enter password')
        """
        self._heading = heading

    def setHiddenInput(self, hidden):
        """
        --Allows hidden text entry.
        hidden : boolean - True for hidden text entry.
        example:
            - kb.setHiddenInput(True)
        """
        self._hidden = hidden

class Monitor(object):
    def __init__(self):
        """
        --Creates a newMonitor to notify addon about changes.
        """
        pass

    def onAbortRequested(self):
        """
        --onAbortRequested method.
        Will be called when XBMC requests Abort
        """
        pass

    def onDatabaseScanStarted(self, database):
        """
        --onDatabaseScanStarted method.
        database : video/music as string
        Will be called when database update starts and return video or music to indicate which DB is being updated
        """
        pass

    def onDatabaseUpdated(self, database):
        """
        --onDatabaseUpdated method.
        database : video/music as string
        Will be called when database gets updated and return video or music to indicate which DB has been changed
        """
        pass

    def onNotification(self, sender, method, data):
        """
        --onNotification method.

        sender : sender of the notification
        method : name of the notification
        data : JSON-encoded data of the notification

        Will be called when XBMC receives or sends a notification
        """
        pass

    def onScreensaverActivated(self):
        """
        --onScreensaverActivated method.

        Will be called when screensaver kicks in
        """
        pass

    def onScreensaverDeactivated(self):
        """
        --onScreensaverDeactivated method.

        Will be called when screensaver goes off
        """
        pass

    def onSettingsChanged(self):
        """
        --onSettingsChanged method.

        Will be called when addon settings are changed
        """
        pass

class PlayList(object):
    def __init__(self, playlist):
        """
        Retrieve a reference from a valid xbmc playlist

        playlist: int - can be one of the next values:
            0: xbmc.PLAYLIST_MUSIC
            1: xbmc.PLAYLIST_VIDEO

        Use PlayList[int position] or __getitem__(int position) to get a PlayListItem.
        """
        pass
    def __getitem__(self):
        """
        x.__getitem__(y) <==> x[y]
        """
        pass

    def __len__(self):
        """
        x.__len__() <==> len(x)
        """
        pass

    def add(self, url, listitem = None, index = 0):
        """
        --Adds a new file to the playlist.

        url : string or unicode - filename or url to add.
        listitem : [opt] listitem - used with setInfo() to set different infolabels.
        index : [opt] integer - position to add playlist item. (default=end)

        *Note, You can use the above as keywords for arguments and skip certain optional arguments. Once you use a keyword, all following arguments require the keyword.

        example:
            - playlist =xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
            - video = 'F:\movies\Ironman.mov'
            - listitem =xbmcgui.ListItem ('Ironman', thumbnailImage='F:\movies\Ironman.tbn')
            - listitem.setInfo('video', {'Title': 'Ironman', 'Genre': 'Science Fiction'})
            - playlist.add(url=video, listitem=listitem, index=7)n
        """
        pass

    def clear(self):
        """
        --clear all items in the playlist.
        """
        pass

    def getPlayListId(self):
        """
         --returns an integer.
        """
        pass

    def getposition(self):
        """
         --returns the position of the current song in this playlist.
        """
        pass

    def load(self, filename):
        """
        --Load a playlist.

        clear current playlist and copy items from the file to this Playlist filename can be like .pls or .m3u ...
        returns False if unable to load playlist
        """
        pass

    def remove(self, filename):
        """
        --remove an item with this filename from the playlist.
        """
        pass


    def shuffle(self):
        """
        --shuffle the playlist.
        """
        pass

    def size(self):
        """
        --returns the total number of PlayListItems in this playlist.
        """
        pass

    def unshuffle(self):
        """
        --unshuffle the playlist.
        """
        pass


class Player(object):
    def __init__(self):
        """
        --Creates a newPlayer class.
        """
        pass

    def DisableSubtitles(self):
        """
        --disable subtitles
        """

    def getAvailableAudioStreams(self):
        """
        --get Audio stream names
        """
        pass

    def getAvailableSubtitleStreams(self):
        """
        --get Subtitle stream names
        """
        pass

    def getMusicInfoTag(self):
        """
        --returns the MusicInfoTag of the current playing 'Song'.
        Throws: Exception, if player is not playing a file or current file is not a music file.
        """
        pass


    def getPlayingFile(self):
        """
        --returns the current playing file as a string.
        Throws: Exception, if player is not playing a file.
        """
        pass

    def getSubtitles(self):
        """
        --get subtitle stream name
        """
        pass


    def getTime(self):
        """
        --Returns the current time of the current playing media as fractional seconds.
        Throws: Exception, if player is not playing a file.
        """
        pass

    def getTotalTime(self):
        """
        --Returns the total time of the current playing media in seconds. This is only accurate to the full second.
        *Throws: Exception, if player is not playing a file.
        """
        pass

    def getVideoInfoTag(self):
        """
        --returns the VideoInfoTag of the current playing Movie.
        Throws: Exception, if player is not playing a file or current file is not a movie file.
        """
        pass

    def isPlaying(self):
        """
        --returns True is xbmc is playing a file.
        """
        pass

    def isPlayingAudio(self):
        """
        --returns True is xbmc is playing an audio file.
        """
        pass

    def isPlayingVideo(self):
        """
        --returns True if xbmc is playing a video.
        """
        pass

    def onPlayBackEnded(self):
        """
        --onPlayBackEnded method.

        Will be called when xbmc stops playing a file
        """
        pass

    def onPlayBackPaused(self):
        """
        --onPlayBackPaused method.

        Will be called when user pauses a playing file
        """
        pass

    def onPlayBackResumed(self):
        """
        --onPlayBackResumed method.

        Will be called when user resumes a paused file
        """
        pass

    def onPlayBackSeek(self, time, seekOffset):
        """
        --onPlayBackSeek method.

        time : integer - time to seek to.
        seekOffset : integer - ?.

        Will be called when user seeks to a time
        """
        pass

    def onPlayBackSeekChapter(self, chapter):
        """
        --onPlayBackSeekChapter method.

        chapter : integer - chapter to seek to.

        Will be called when user performs a chapter seek
        """
        pass

    def onPlayBackSpeedChanged(self, speed):
        """
        --onPlayBackSpeedChanged method.

        speed : integer - current speed of player.

        *Note, negative speed means player is rewinding, 1 is normal playback speed.

        Will be called when players speed changes. (eg. user FF/RW)
        """
        pass

    def onPlayBackStarted(self):
        """
        --onPlayBackStarted method.

        Will be called when xbmc starts playing a file
        """
        pass

    def onPlayBackStopped(self):
        """
        --onPlayBackStopped method.

        Will be called when user stops xbmc playing a file
        """
        pass

    def onQueueNextItem(self):
        """
        --onQueueNextItem method.

        Will be called when user queues the next item
        """
        pass

    def pause(self):
        """
         --Pause playing.
        """
        pass

    def play(self, item = '', listitem = None, windowed = False, startpos = 0):
        """
        --Play this item.

        item : [opt] string - filename, url or playlist.
        listitem : [opt] listitem - used with setInfo() to set different infolabels.
        windowed : [opt] bool - true=play video windowed, false=play users preference.(default)
        startpos : [opt] int - starting position when playing a playlist. Default = -1

        *Note, If item is not given then thePlayer will try to play the current item
        in the current playlist.

        You can use the above as keywords for arguments and skip certain optional arguments.
        Once you use a keyword, all following arguments require the keyword.

        example:

            - listitem =xbmcgui.ListItem ('Ironman')

            - listitem.setInfo('video', {'Title': 'Ironman', 'Genre': 'Science Fiction'})

            - xbmc.Player().play(url, listitem, windowed)

            - xbmc.Player().play(playlist, listitem, windowed, startpos)
        """
        pass

    def playnext(self):
        """
        --Play next item in playlist.
        """
        pass

    def playprevious(self):
        """
        --Play previous item in playlist.
        """
        pass

    def playselected(self):
        """
        --Play a certain item from the current playlist.
        """
        pass

    def seekTime(self):
        """
        --Seeks the specified amount of time as fractional seconds. The time specified is relative to the beginning of the currently playing media file.

        Throws: Exception, if player is not playing a file.
        """
        pass

    def setAudioStream(self, stream):
        """
        --set Audio Stream.

        stream : int

        example:
            - setAudioStream(1)
        """
        pass

    def setSubtitleStream(self, stream):
        """
        --set Subtitle Stream

        stream : int

        example:
            - setSubtitleStream(1)
        """
        pass

    def setSubtitles(self):
        """
        --set subtitle file and enable subtitlesn
        """
        pass

    def showSubtitles(self, visible):
        """
        --enable/disable subtitles

        visible : boolean - True for visible subtitles.

        example:
            - xbmc.Player().showSubtitles(True)
        """
        pass

    def stop(self):
        """
        --Stop playing.
        """
        pass

class RenderCapture(object):
    def capture(self, width, height , flags = None):
        """
        --issue capture request.

        width : Width capture image should be rendered to
        height : Height capture image should should be rendered to
        flags : Optional. Flags that control the capture processing.

        The value for 'flags' could be or'ed from the following constants:
            - xbmc.CAPTURE_FLAG_CONTINUOUS : after a capture is done, issue a new capture request immediately
            - xbmc.CAPTURE_FLAG_IMMEDIATELY : read out immediately whencapture() is called, this can cause a busy wait
        """
        pass

    def getAspectRatio(self):
        """
        --returns aspect ratio of currently displayed video.
        """
        pass

    def getCaptureState(self):
        """
        --returns processing state of capture request.

        The returned value could be compared against the following constants:
            - xbmc.CAPTURE_STATE_WORKING : Capture request in progress.
            - xbmc.CAPTURE_STATE_DONE : Capture request done. The image could be retrieved withgetImage()
            - xbmc.CAPTURE_STATE_FAILED : Capture request failed.
        """
        pass

    def getHeight(self):
        """
        --returns height of captured image.
        """
        pass

    def getImage(self):
        """
        --returns captured image as a bytearray.

        The size of the image isgetWidth() *getHeight() * 4
        """
        pass

    def getImageFormat(self):
        """
        --returns format of captured image: 'BGRA' or 'RGBA'.
        """
        pass

    def getWidth(self):
        """
        --returns width of captured image.
        """
        pass

    def waitForCaptureStateChangeEvent(self, msecs = 0):
        """
        --wait for capture state change event.

        msecs : Milliseconds to wait. Waits forever if not specified.

        The method will return 1 if the Event was triggered. Otherwise it will return 0.
        """
        pass

#
#    Functions
#

def audioResume():
    """
    --Resume Audio engine.

    example: xbmc.audioResume()
    """
    pass

def audioSuspend():
    """
    --Suspend Audio engine.

    example:
        - xbmc.audioSuspend()
    """
    pass

def convertLanguage(language, lang_format):
    """
    --Returns the given language converted to the given format as a string.

    language: string either as name in English, two letter code (ISO 639-1), or three letter code (ISO 639-2/T(B)
    format: format of the returned language string
    xbmc.ISO_639_1: two letter code as defined in ISO 639-1
    xbmc.ISO_639_2: three letter code as defined in ISO 639-2/T or ISO 639-2/B
    xbmc.ENGLISH_NAME: full language name in English (default)

    example:
    - language = xbmc.convertLanguage(English, xbmc.ISO_639_2)

    """
    pass

def enableNavSounds(yesNo):
    """
    --Enables/Disables nav sounds

    yesNo : integer - enable (True) or disable (False) nav sounds

    example:
        - xbmc.enableNavSounds(True)
    """
    pass

def executeJSONRPC(jsonrpccommand):
    """
    --Execute an JSONRPC command.

    jsonrpccommand : string - jsonrpc command to execute.

    List of commands -

    example:
        - response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "id": 1 }')
    """
    pass

def executebuiltin(function):
    """
    --Execute a built in XBMC function.

    function : string - builtin function to execute.

    List of functions -http://wiki.xbmc.org/?title=List_of_Built_In_Functions

    example:
        - xbmc.executebuiltin('XBMC.RunXBE(c:\avalaunch.xbe)')
    """
    pass

def executehttpapi(httpcommand):
    """
    --Not implemented anymore.
    """
    pass

def executescript(script):
    """
    --Execute a python script.
    script : string - script filename to execute.
    example:
        - xbmc.executescript('special://home/scripts/update.py')

    """
    fileName = translatePath(script)
    execfile(fileName, globals())
    pass


def getCacheThumbName(path):
    """
    --Returns a thumb cache filename.

    path : string or unicode - path to file

    example:
        - thumb = xbmc.getCacheThumbName('f:\videos\movie.avi')
    """
    pass


def getCleanMovieTitle(path, usefoldername = False):
    """
    --Returns a clean movie title and year string if available.

    path : string or unicode - String to clean
    bool : [opt] bool - use folder names (defaults to false)

    example:
        - title, year = xbmc.getCleanMovieTitle('/path/to/moviefolder/test.avi', True)
    """
    pass

def getCondVisibility(condition):
    """
    --Returns True (1) or False (0) as a bool.

    condition : string - condition to check.

    List of Conditions -http://wiki.xbmc.org/?title=List_of_Boolean_Conditions

    *Note, You can combine two (or more) of the above settings by using "+" as an AND operator,
    "|" as an OR operator, "!" as a NOT operator, and "[" and "]" to bracket expressions.


    example:
        - visible = xbmc.getCondVisibility('[Control.IsVisible(41) + !Control.IsVisible(12)]')
    """
    pass

def getDVDState():
    """
    --Returns the dvd state as an integer.

    return values are:
        - 1 : xbmc.DRIVE_NOT_READY
        - 16 : xbmc.TRAY_OPEN
        - 64 : xbmc.TRAY_CLOSED_NO_MEDIA
        - 96 : xbmc.TRAY_CLOSED_MEDIA_PRESENT


    example:
        - dvdstate = xbmc.getDVDState()
    """
    pass

def getFreeMem():
    """
    --Returns the amount of free memory in MB as an integer.

    example:
        - freemem = xbmc.getFreeMem()
    """
    pass

def getGlobalIdleTime():
    """
    --Returns the elapsed idle time in seconds as an integer.

    example:
        - t = xbmc.getGlobalIdleTime()
    """
    pass

def getIPAddress():
    """
    --Returns the current ip address as a string.

    example:
        -
    """
    import socket
    return socket.gethostbyname(socket.gethostname())

def getInfoImage(infotag):
    """
    --Returns a filename including path to the InfoImage's thumbnail as a string.

    infotag : string - infotag for value you want returned.

    List of InfoTags -http://wiki.xbmc.org/?title=InfoLabels

    example:
        - filename = xbmc.getInfoImage('Weather.Conditions')
    """
    pass

def getRegion(setting_id):
    """
    --Returns your regions setting as a string for the specified id.

    setting_id : string - id of setting to return

    *Note, choices are (dateshort, datelong, time, meridiem, tempunit, speedunit)You can use the above as keywords for arguments.

    example:
        - date_long_format = xbmc.getRegion('datelong')
    """
    pass

def getInfoLabel(infotag):
    """
    --Returns an InfoLabel as a string.

    infotag : string - infoTag for value you want returned.

    List of InfoTags -http://wiki.xbmc.org/?title=InfoLabels

    example:
        - label = xbmc.getInfoLabel('Weather.Conditions')
    """
    return ''
    pass

def getLanguage(lang_format = None, region = None):
    """
    --Returns the active language as a string.

    lang_format: [opt] format of the returned language string
        - xbmc.ISO_639_1: two letter code as defined in ISO 639-1
        - xbmc.ISO_639_2: three letter code as defined in ISO 639-2/T or ISO 639-2/B
        - xbmc.ENGLISH_NAME: full language name in English (default)


    region: [opt] append the region delimited by "-" of the language (setting) to the returned language string

    example:
        - language = xbmc.getLanguage(xbmc.ENGLISH_NAME)
    """
    if lang_format == ISO_639_1: return 'en'
    elif lang_format == ISO_639_2: return 'eng'
    elif lang_format == ENGLISH_NAME: return 'English'
    return 'English'


def getLocalizedString(string_id):
    """
    --Returns a localized 'unicode string'.

    string_id : integer - id# for string you want to localize.

    *Note, See strings.xml in }\ for which id
    you need for a string.

    example:
        - locstr = xbmc.getLocalizedString(6)
    """
    addonId = sys.argv[0]
    langPath = 'special://home/addons/' + addonId
    langPath = translatePath(langPath)
    langPath = langPath + '\\resources\\language\\English\\strings.xml'
    if os.path.exists(langPath):
        with open(langPath, 'r') as langFile:
            langStr = langFile.read()
        strToSearch = '<string id="' + str(string_id) + '">'
        limInf = langStr.find(strToSearch)
        if limInf == -1: return 'not found'
        limInf += len(strToSearch)
        limSup = langStr.find('</string>', limInf)
        return langStr[limInf:limSup]
    return 'archivo lenguaje no existe'

def getSkinDir():
    """
    --Returns the active skin directory as a string.

    *Note, This is not the full path like 'special://home/addons/MediaCenter', but only 'MediaCenter'.

    example:
        - skindir = xbmc.getSkinDir()
    """
    return 'skin.confluence'
    pass

def getSupportedMedia(media):
    """
    --Returns the supported file types for the specific media as a string.

    media : string - media type

    *Note, media type can be (video, music, picture).The return value is a pipe separated string of filetypes (eg. '.mov|.avi').

       You can use the above as keywords for arguments.

    example:
        - mTypes = xbmc.getSupportedMedia('video')
    """
    pass

def log(msg, level = LOGNOTICE):
    """
    --Write a string to XBMC's log file and the debug window.
    msg : string - text to output.
    level : [opt] integer - log level to ouput at. (default=LOGNOTICE)

    *Note, You can use the above as keywords for arguments and skip certain optional arguments.
    Once you use a keyword, all following arguments require the keyword.

    Text is written to the log for the following conditions.
    XBMC loglevel == -1 (NONE, nothing at all is logged)
    XBMC loglevel == 0 (NORMAL, shows LOGNOTICE, LOGERROR, LOGSEVERE and LOGFATAL) XBMC loglevel == 1 (DEBUG, shows all)
    See pydocs for valid values for level.


    example:
        - xbmc.log(msg='This is a test string.', level=xbmc.LOGDEBUG));
    """
    logLst = ['LOGDEBUG', 'LOGINFO', 'LOGNOTICE', 'LOGWARNING',
               'LOGERROR', 'LOGSEVERE', 'LOGFATAL', 'LOGNONE']
    if xbmcLoglevel < 0 : return
    if xbmcLoglevel == 0 and level in [LOGDEBUG, LOGINFO]: return
    print >> sys.stderr, logLst[level] + ':  ' + msg

def makeLegalFilename(filename, fatX = True):
    """
    --Returns a legal filename or path as a string.

    filename : string or unicode - filename/path to make legal
    fatX : [opt] bool - True=Xbox file system(Default)


    *Note, If fatX is true you should pass a full path. If fatX is false only pass the basename of the path.

    You can use the above as keywords for arguments and skip
    certain optional arguments. Once you use a keyword,
    all following arguments require the keyword.

    example:
        - filename = xbmc.makeLegalFilename('F: Age: The Meltdown.avi')
    """
    if fatX: return validatePath(filename)
    return filename + '/'
    pass

def playSFX(filename, useCached = True):
    """
    --Plays a wav file by filename

    filename : string - filename of the wav file to play. useCached : [opt] bool - False = Dump any previously cached wav associated with filename

    example:
        - xbmc.playSFX('special://xbmc/scripts/dingdong.wav')

        - xbmc.playSFX('special://xbmc/scripts/dingdong.wav',False)
    """
    pass

def restart():
    """
    --Restart the htpc. example:
    - xbmc.restart()
    """
    pass

def Shutdown():
    """
    --Shutdown the htpc.

    example:
        - xbmc.shutdown()
    """
    pass

def skinHasImage(image):
    """
    --Returns True if the image file exists in the skin.

    image : string - image filename

    *Note, If the media resides in a subfolder include it. (eg. home-myfiles\home-myfiles2.png)You can use the above as keywords for arguments.

    example:
        - exists = xbmc.skinHasImage('ButtonFocusedTexture.png')
    """
    pass

def sleep(atime):
    """
    --Sleeps for 'time' msec.
    time : integer - number of msec to sleep.

    *Note, This is useful if you have for example aPlayer class that is waiting
    for onPlayBackEnded() calls.


    Throws: PyExc_TypeError, if time is not an integer.

    example:
        - xbmc.sleep(2000) # sleeps for 2 seconds
    """
    time.sleep(float(atime/1000.0))
    pass

def startServer(typ, bStart, bWait):
    """
    --start or stop a server.

    typ : integer - use SERVER_* constants
    bStart : bool - start (True) or stop (False) a server
    bWait : [opt] bool - wait on stop before returning (not supported by all servers)
    returnValue : bool - True or False


    example:
        - xbmc.startServer(xbmc.SERVER_AIRPLAYSERVER, False)
    """
    pass

def stopSFX():
    """
    --Stops wav file

    example:
        - xbmc.stopSFX()
    """
    pass

def translatePath(path):
    """
    --Returns the translated path.

    path : string or unicode - Path to format

    *Note, Only useful if you are coding for both Linux and Windows.
    e.g. Converts 'special://masterprofile/script_data' -> '/home/user/XBMC/UserData/script_data' on Linux.

    example:
        - fpath = xbmc.translatePath('special://masterprofile/script_data')
        :type path: string or unicode
    """
    specialProtocol = {
                       'special://temp':'special://home/cache',
                       'special://masterprofile':'special://home/userdata',
                       'special://profile':'special://masterprofile',
                       'special://userdata':'special://masterprofile',
                       'special://database':'special://masterprofile/Database',
                       'special://thumbnails':'special://masterprofile/Thumbnails',
                       'special://musicplaylists':'special://profile/playlists/music',
                       'special://videoplaylists':'special://profile/playlists/video',
                       'special://logpath':'special://home',
                       'special://skin':'special://xbmc/addons'
                       }

    if sys.platform[:3] == 'win':
        specialProtocol['special://xbmc'] = special_xbmc or os.path.join(os.path.expandvars("$PROGRAMFILES"), "Kodi")
        specialProtocol['special://home'] = special_home or os.path.join(os.path.expandvars("$APPDATA"), "Kodi")
    elif not (special_home or special_xbmc):
        raise Exception('You must define the vars xbmc.special_xbmc (special://xbmc) and xbmc.special_home (special://home)')
    else:
        specialProtocol['special://xbmc'] = special_xbmc
        specialProtocol['special://home'] = special_home

    pattern = 'special://[^\\\\/]+'
    oldPath = ''
    while oldPath != path:
        oldPath = path
        path = re.sub(pattern, lambda x: specialProtocol.get(x.group(), x.group()), oldPath)
    root = re.match(pattern, path)
    if not root: return validatePath(path)
    raise Exception(root.group() + ' is not a special path in KODI')



def validatePath(aPath):
    """
    --Returns the validated path.

    path : string or unicode - Path to format

    *Note, Only useful if you are coding for both Linux and Windows for fixing slash problems.
    e.g. Corrects 'Z://something' -> 'Z:'
    example:
        - fpath = xbmc.validatePath(somepath)
    """
    return os.path.normpath(aPath)

