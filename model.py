import subprocess,json
from typing import Any, Dict
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, QPersistentModelIndex, Qt, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.qt.searchmodel"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class SearchModel(QAbstractListModel):
    IdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.DisplayRole + 2
    query : str = ""
    videos : list[dict] = []

    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.videos = []
    
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex= QModelIndex())  -> int:
        return len(self.videos)
        
    def roleNames(self) -> Dict[int, QByteArray]:
        default = super().roleNames()
        default[self.IdRole] = QByteArray(b'videoId')
        default[self.TitleRole] = QByteArray(b'videoTitle')
        return default
    
    def data(self, index: QModelIndex | QPersistentModelIndex, /, role: int = Qt.ItemDataRole.UserRole) -> Any:
        if not self.videos:
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.ItemDataRole.DisplayRole:
            ret = self.videos[index.row()]["title"]
        elif role == Qt.ItemDataRole.UserRole:
            ret = self.videos[index.row()]["id"]
        else:
            ret  = None
        return ret
    
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