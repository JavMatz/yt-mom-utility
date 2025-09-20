from __future__ import annotations

import subprocess
import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Bridge(QObject):
    query=""

    @Slot(str, result=None)
    def setQuery(self, newQuery):
        self.query = newQuery

    @Slot()
    def searchYT(self):
        videos = subprocess.run(['yt-dlp', f'ytsearch5:{self.query}', '--flat-playlist', '--print', '\"%(.{uploader,title,duration_string,id})j\"'], capture_output=True, text=True)

        print(videos.stdout)

if __name__ == '__main__':

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.addImportPath(sys.path[0])
    engine.loadFromModule("App","Main")
    if not engine.rootObjects():
            sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)
