import json, asyncio
from typing import Any, Dict
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QPersistentModelIndex, Qt, Slot, Signal, Property
from qasync import asyncSlot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.qt.searchmodel"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class SearchModel(QAbstractListModel):
    IdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    UploaderRole = Qt.ItemDataRole.UserRole +3
    DurationRole = Qt.ItemDataRole.UserRole +4
    processingRequestSignal = Signal()

    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.query : str = ""
        self.videos : list[dict] = []
        self.downloadLocation : str = "~/Downloads"
        self._processingRequest : bool = False
    
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
   
    def getProcessingRequest(self):
        return self._processingRequest
    
    def setProcessingRequest(self, value : bool):
        self._processingRequest = value
        self.processingRequestSignal.emit()

    processingRequest = Property(bool, fget=getProcessingRequest, fset=setProcessingRequest, notify=processingRequestSignal)
    
    @Slot(str, result=None)
    def setQuery(self, newQuery):
        if not self._processingRequest:
            self.query = newQuery
    
    @asyncSlot()
    async def searchYT(self):
        self._processingRequest = True
        self.processingRequestSignal.emit()
        
        process = await asyncio.create_subprocess_exec(
                'yt-dlp', 
                f'ytsearch10:{self.query}', 
                '--flat-playlist',
                '--print',
                '%(.{uploader,title,duration_string,id})j',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stderr:
            print(f'[Error] {stderr.decode()}')
        elif stdout:
            auxList = []

            for line in stdout.splitlines():
                video = json.loads(line)
                if "duration_string" in video:
                    auxList.append(video)

            # Crucial!
            self.beginResetModel()
            self.videos = auxList 
            self.endResetModel()

        self._processingRequest = False
        self.processingRequestSignal.emit()

    @asyncSlot(str, result=None)
    async def downloadAudio(self, video_id: str):
        self._processingRequest = True
        self.processingRequestSignal.emit()
        process = await asyncio.create_subprocess_exec(
            'yt-dlp', 
            '-x', 
            '--audio-format', 'mp3', 
            f'https://www.youtube.com/watch?v={video_id}',
            '-o', f'{self.downloadLocation}/%(title)s - %(uploader)s.%(ext)s',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        _, stderr = await process.communicate()

        if stderr:
            print(f'[Error] {stderr.decode()}')

        self._processingRequest = False
        self.processingRequestSignal.emit()
        
    @asyncSlot(str, result=None)
    async def downloadVideo(self, video_id: str):
        self._processingRequest = True
        self.processingRequestSignal.emit()
        process = await asyncio.create_subprocess_exec(
            'yt-dlp', 
            f'https://www.youtube.com/watch?v={video_id}',
            '-o', f'{self.downloadLocation}/%(title)s - %(uploader)s.%(ext)s',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if stderr:
            print(f'[Error] {stderr.decode()}')

        self._processingRequest = False
        self.processingRequestSignal.emit()