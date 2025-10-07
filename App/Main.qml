import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1

import io.qt.searchmodel 1.0

ApplicationWindow {
    id: page
    width: 700
    height: 400
    minimumWidth: 700
    maximumWidth: 700
    minimumHeight: 400
    maximumHeight: 400
    visible: true
    title: "MOMYT Download"

    SearchModel {
        id: searchModel
    }

    ColumnLayout {
        id: column
        spacing: 10
        anchors.fill: parent
        RowLayout {
            id: searchRow
            spacing: 5
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop | Qt.AlignCenter

            Rectangle {
                id: searchBoxContainer
                border.color: "#000000"
                color: "#ffffff"
                border.width: 1
                height: 26
                Layout.fillWidth: true
                Layout.topMargin: 10
                Layout.leftMargin: 10

                TextInput {
                    id: searchBox
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: searchBoxContainer.left
                    anchors.leftMargin: 5
                    font.pixelSize: 16
                    text: ""
                    focus: true
                    onTextChanged: {
                        searchModel.setQuery(text);
                    }
                    onAccepted: {
                        searchModel.searchYT();
                    }
                    Text {
                        id: placeholderText
                        text: "Search video..."
                        color: "#aaaaaa"
                        font: searchBox.font
                        anchors.fill: parent
                        anchors.leftMargin: searchBox.leftPadding
                        anchors.topMargin: searchBox.topPadding
                        visible: !searchBox.text
                    }
                }
            }

            Button {
                id: searchButton
                text: "Search"
                Layout.fillWidth: true
                Layout.maximumWidth: 100
                Layout.minimumWidth: 100
                Layout.topMargin: 10
                Layout.rightMargin: 10
                onClicked: {
                    searchModel.searchYT();
                }
            }
        }

        Rectangle {
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            Layout.bottomMargin:10
            Layout.fillWidth: true 
            Layout.fillHeight: true
            border.color: "#000000"
            border.width: 1
            clip: true

            Component {
                id: videoDelegate
                RowLayout{
                    Rectangle {
                        width: 120
                        height: 90
                        Image {
                            anchors.fill: parent
                            source: "placeholder.jpg"
                        }

                        Rectangle {
                            color: "black"
                            opacity: 0.70
                            width: durationText.width + 2
                            height: durationText.height + 2
                            anchors.bottom: parent.bottom
                            anchors.right: parent.right
                            anchors.rightMargin: 3
                            anchors.bottomMargin: 3
                            radius: 3
                            Text {
                                id: durationText
                                anchors.centerIn: parent
                                color: "white"
                                font.bold: true
                                text: duration
                            }
                        }
                    }
                    
                    ColumnLayout{
                        Text {
                            text: title
                            font.bold: true
                        }
                        Text {
                            text: uploader
                        }
                        RowLayout{
                            Button {
                                text: "Download Audio"
                                onClicked: {
                                    searchModel.downloadAudio(id);
                                }
                            }
                            Button {
                                text: "Download Video"
                                onClicked: {
                                    searchModel.downloadVideo(id);
                                }
                            }
                        }
                    }
                }
            }

            ListView {
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                anchors.topMargin: 10
                anchors.bottomMargin: 10
                id: searchResults
                spacing: 3
                anchors.fill: parent
                model: searchModel
                delegate: videoDelegate
            }
        }
        
    }
}
