import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1

import io.qt.textproperties 1.0

ApplicationWindow {
    id: page
    width: 800
    height: 400
    visible: true

    Bridge {
        id: bridge
    }

    ColumnLayout {
        id: column
        spacing: 2
        anchors.fill: parent
        RowLayout {
            id: searchRow
            spacing: 2
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop | Qt.AlignCenter

            TextInput {
                id: searchBox
                Layout.fillWidth: true
                Layout.topMargin: 10
                Layout.leftMargin: 10
                font.pixelSize: 16
                text: ""
                focus: true
                onTextChanged: {
                    bridge.setQuery(text);
                }
                Text {
                    id: placeholderText
                    text: "Search video"
                    color: "#aaaaaa"
                    font: searchBox.font
                    anchors.fill: parent
                    anchors.leftMargin: searchBox.leftPadding
                    anchors.topMargin: searchBox.topPadding
                    visible: !searchBox.text
                    verticalAlignment: searchBox.verticalAlignment
                    horizontalAlignment: searchBox.horizontalAlignment
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
                    bridge.searchYT();
                }
            }
        }
    }
}
