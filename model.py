import subprocess,json
from typing import Any, Dict
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, QPersistentModelIndex, Qt, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.qt.searchmodel"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class SearchModel(QAbstractListModel):
    IdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    UploaderRole = Qt.ItemDataRole.UserRole +3
    DurationRole = Qt.ItemDataRole.UserRole +4

    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.query : str = ""
        self.videos : list[dict] = []
    
    def rowCount(self, 
                 parent: QModelIndex | QPersistentModelIndex= QModelIndex())  -> int:
        return len(self.videos)
        
    def roleNames(self) -> Dict[int, QByteArray]:
        default = super().roleNames()
        default[self.IdRole] = QByteArray(b'id')
        default[self.TitleRole] = QByteArray(b'title')
        default[self.UploaderRole] = QByteArray(b'uploader')
        default[self.DurationRole] = QByteArray(b'duration')
        return default
    
    def data(self, 
             index: QModelIndex | QPersistentModelIndex, /, 
             role: int = Qt.ItemDataRole.UserRole) -> Any:
        if not self.videos:
            ret = None
        elif not index.isValid():
            ret = None
        elif role == self.IdRole:
            ret = self.videos[index.row()]["id"]
        elif role == self.TitleRole:
            ret = self.videos[index.row()]["title"]
        elif role == self.UploaderRole:
            ret = self.videos[index.row()]["uploader"]
        elif role == self.DurationRole:
            ret = self.videos[index.row()]["duration_string"]
        else:
            ret  = None
        return ret
    
    @Slot(str, result=None)
    def setQuery(self, newQuery):
        self.query = newQuery

    @Slot()
    def searchYT(self):
        videos = subprocess.run(['yt-dlp', 
                                 f'ytsearch10:{self.query}', 
                                 '--flat-playlist', 
                                 '--print', 
                                 '%(.{uploader,title,duration_string,id})j'], 
                                 capture_output=True, text=True)

        auxList = []

        for line in videos.stdout.splitlines():
            video = json.loads(line)
            if "duration_string" in video:
                auxList.append(video)

        # Crucial!
        self.beginResetModel()
        self.videos = auxList 
        self.endResetModel()   

    @Slot(str, result=None)
    def downloadAudio(self, video_id: str):
        subprocess.Popen(['yt-dlp', 
                          '-x', 
                          '--audio-format', 'mp3', 
                          f'https://www.youtube.com/watch?v={video_id}',
                          '-o', f'{self.downloadLocation}/%(title)s - %(uploader)s.%(ext)s'])
        
    @Slot(str, result=None)
    def downloadVideo(self, video_id: str):
                          f'https://www.youtube.com/watch?v={video_id}',
                          '-o', f'{self.downloadLocation}/%(title)s - %(uploader)s.%(ext)s'])
                          f'https://www.youtube.com/watch?v={video_id}'])