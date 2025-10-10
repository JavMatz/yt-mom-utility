from __future__ import annotations

import sys, asyncio

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from qasync import QEventLoop
from model import SearchModel

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    app.setDesktopFileName("momyt") 
    # FOR MY NOTES: Integrate Qt loop into the asyncio loop
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])

    # when app is about to quit delete the engine
    app.aboutToQuit.connect(engine.deleteLater)
    # when the engine quits, quit the app
    engine.quit.connect(app.quit)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
   
    app_close_event = asyncio.Event()
    # when the app and engine quit set the event TODO: 
    # read more about Events
    app.aboutToQuit.connect(app_close_event.set)
    engine.quit.connect(app_close_event.set)

    engine.loadFromModule("App","Main")

    if not engine.rootObjects():
            sys.exit(-1)

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
