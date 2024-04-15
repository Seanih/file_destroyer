from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

# Qt is a positioning module
from PyQt6.QtCore import Qt
from pathlib import Path


def open_files():
    # print(str(window.width()) + " " + str(window.height()))
    global filenames
    filenames, _ = QFileDialog.getOpenFileNames(window, "Select Files")
    # format file names
    formatted_names = [file.split("/")[-1] for file in filenames]
    message_area.setText("\n".join(formatted_names))
    if len(formatted_names) > 0:
        clear_btn.setVisible(True)
        destroy_btn.setDisabled(False)


def show_confirmation_dialog():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(
        "Are you sure you want to delete the selected file(s)? This action cannot be undone."
    )
    msg.setWindowTitle("Confirmation")
    msg.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    choice = msg.exec()
    return choice == QMessageBox.StandardButton.Yes


def destroy_files():
    try:
        if len(filenames) > 0:
            confirm = show_confirmation_dialog()
            if confirm:
                for filename in filenames:
                    path = Path(filename)
                    with open(path, "wb") as file:
                        file.write(b"overwritten once")
                    with open(path, "wb") as file:
                        file.write(b"overwritten twice")
                    with open(path, "wb") as file:
                        file.write(b"overwritten thrice")
                    path.unlink()
                message_area.setText("Destruction Successful")
                # Update clear_btn visibility
                clear_btn.setVisible(False)
                destroy_btn.setDisabled(True)

    except Exception:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Must choose file(s) to be deleted")
        msg.exec()


def clear_selection():
    filenames.clear()
    # Update clear_btn visibility
    message_area.setText("")
    clear_btn.setVisible(False)
    window.adjustSize()
    destroy_btn.setDisabled(True)


app = QApplication([])
window = QWidget()
window.setWindowTitle("File Destroyer")
layout = QVBoxLayout()

# create and add description
description = QLabel(
    'Select the files you want destroyed. The files will be <font color="red">permanently</font> deleted.'
)
layout.addWidget(description)

# create and add widgets with positioning
open_btn = QPushButton("Select File(s)")
open_btn.setToolTip("choose the file(s) you want to delete")
open_btn.setFixedWidth(100)
layout.addWidget(open_btn, alignment=Qt.AlignmentFlag.AlignCenter)
open_btn.clicked.connect(open_files)

clear_btn = QPushButton("Clear Selection")
clear_btn.setToolTip("clear the selected file(s)")
clear_btn.setFixedWidth(120)
clear_btn.clicked.connect(clear_selection)
layout.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignCenter)
clear_btn.setVisible(False)

message_area = QLabel("")
layout.addWidget(message_area, alignment=Qt.AlignmentFlag.AlignCenter)

destroy_btn = QPushButton("Destroy")
destroy_btn.setToolTip("delete the selected file(s)")
destroy_btn.setFixedWidth(100)
layout.addWidget(destroy_btn, alignment=Qt.AlignmentFlag.AlignCenter)
destroy_btn.clicked.connect(destroy_files)
destroy_btn.setDisabled(True)

window.setLayout(layout)
window.move(650, 400)

if __name__ == "__main__":
    window.show()
    app.exec()
