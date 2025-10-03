import subprocess, json

from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement


QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Bridge(QObject):
    query : str = ""
    videos : list[dict] = []

    @Slot(str, result=None)
    def setQuery(self, newQuery):
        self.query = newQuery

    @Slot()
    def searchYT(self):
        videos = subprocess.run(['yt-dlp', f'ytsearch5:{self.query}', '--flat-playlist', '--print', '%(.{uploader,title,duration_string,id})j'], capture_output=True, text=True)

        print(videos.stdout)

        for line in videos.stdout.splitlines():
            video = json.loads(line)
            self.videos.append(video)