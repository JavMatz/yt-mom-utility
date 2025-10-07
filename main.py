from __future__ import annotations

import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from model import SearchModel

if __name__ == '__main__':

    app = QGuiApplication(sys.argv)
    app.setDesktopFileName("momyt")
    engine = QQmlApplicationEngine()

    engine.addImportPath(sys.path[0])
    engine.loadFromModule("App","Main")
    if not engine.rootObjects():
            sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)
