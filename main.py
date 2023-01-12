import sys
import sqlite3

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLineEdit, QPushButton, QLabel, QDialog


class Library(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("books.db")
        self.cur = self.con.cursor()
        self.buttons = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Каталог библиотеки")
        self.setFont(QFont("sans-serif", 14))

        self.search_type = QComboBox(self)
        self.search_type.addItems(["Автор", "Название"])
        self.search_type.resize(200, 35)
        self.search_type.move(20, 30)

        self.search = QLineEdit(self)
        self.search.resize(200, 35)
        self.search.move(20, 95)

        self.button = QPushButton("Искать", self)
        self.button.resize(200, 100)
        self.button.move(250, 30)
        self.button.clicked.connect(self.finding)

        self.label = QLabel(self)
        self.label.resize(440, 350)
        self.label.move(20, 150)
        self.label.setStyleSheet("background-color: 'white';"
                                 "border: 1px solid grey")

    def finding(self):
        [button.close() for button in self.buttons]
        cur = self.search_type.currentText()
        result = list(self.cur.execute(f"SELECT * FROM books WHERE {'title' if cur == 'Название' else 'author'} "
                                       f"LIKE '%{self.search.text()}%' OR {'title' if cur == 'Название' else 'author'} "
                                       f"LIKE '%{self.search.text().capitalize()}%'"))
        self.buttons = []
        for i in range(len(result)):
            print(result[i])
            button = QPushButton(result[i][1], self)
            button.meta = result[i]
            button.resize(440, 50)
            button.move(20, 150 + 50 * i)
            button.clicked.connect(self.show_dlg)
            self.buttons.append(button)
            button.show()

    def show_dlg(self):
        self.dlg = QDialog(self)
        self.dlg.setFont(QFont("serif", 14))
        self.dlg.setWindowTitle("Добавить элемент")
        self.dlg.setFixedSize(400, 700)

        sender = self.sender()
        self.book = QLabel(self.dlg)
        self.book.move(125, 0)
        self.book.resize(150, 300)
        self.book.setPixmap(QPixmap(f"assets/{sender.meta[3] if sender.meta[3] else 'book.jpg'}").scaled(150, 200))

        self.title_lab = QLabel(self.dlg)
        self.title_lab.move(125, 310)
        self.title_lab.resize(150, 40)
        self.title_lab.setText("Название")
        self.title_lab.setFont(QFont("sans-serif", 16))

        self.title = QLabel(self.dlg)
        self.title.move(50, 360)
        self.title.resize(350, 30)
        self.title.setText(sender.meta[1])

        self.author_lab = QLabel(self.dlg)
        self.author_lab.move(125, 400)
        self.author_lab.resize(150, 30)
        self.author_lab.setText("Автор")
        self.author_lab.setFont(QFont("sans-serif", 16))

        self.author = QLabel(self.dlg)
        self.author.move(50, 450)
        self.author.resize(350, 30)
        self.author.setText(sender.meta[2])

        self.year_lab = QLabel(self.dlg)
        self.year_lab.move(125, 490)
        self.year_lab.resize(150, 30)
        self.year_lab.setText("Год")
        self.year_lab.setFont(QFont("sans-serif", 16))

        self.year = QLabel(self.dlg)
        self.year.move(50, 540)
        self.year.resize(350, 30)
        self.year.setText(str(sender.meta[4]))

        self.genre_lab = QLabel(self.dlg)
        self.genre_lab.move(125, 580)
        self.genre_lab.resize(150, 30)
        self.genre_lab.setText("Жанр")
        self.genre_lab.setFont(QFont("sans-serif", 16))

        self.genre = QLabel(self.dlg)
        self.genre.move(50, 630)
        self.genre.resize(350, 30)
        self.genre.setText(sender.meta[-1])

        self.dlg.exec()


def excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = Library()
    ex.show()
    sys.exit(app.exec())
