import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1

import io.qt.textproperties 1.0

ApplicationWindow {
    id: page
    width: 800
    height: 400
    visible: true

    Bridge {
        id: bridge
    }

    RowLayout {
        // Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        TextInput {
            id: searchBox
            font.pixelSize: 20
            text: ""
            focus: true
            onTextChanged: {
                bridge.setQuery(text);
            }
            Text {
                id: placeholderText
                text: "Enter text here..."
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
            onClicked: {
                bridge.searchYT();
            }
        }
    }
}
