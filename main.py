
import sys
from urllib.request import urlopen
from PyQt5.QtCore import QRunnable,QTimer, QThreadPool
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton
from time import sleep
from Song_title import song_data
from Stream import stream



url = 'http://stream.rockradio.si:9034/'
url_photo = 'https://www.rockradio.si/'
default_photo = 'https://www.rockradio.si/Public/assets/dist/1486812949460/img/icon-rock-sign-grey.svg'

class Worker(QRunnable):

    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn

    def run(self):
        try:
            self.fn()
        except:
            pass

class Ui(QtWidgets.QMainWindow):

    def __init__(self,*args, **kwargs):

        super(Ui, self).__init__(*args, **kwargs) # Call the inherited classes __init__ method
        uic.loadUi('Rock_radio_Qt_UI.ui', self) # Load the .ui file

        #play_button
        self.button = self.findChild(QPushButton, 'pushButton')
        self.button.clicked.connect(self.pushButtonPressed)
        #stop_button
        self.button2 = self.findChild(QPushButton, 'pushButton_2')
        self.button2.clicked.connect(self.pushButton_2Pressed)
        self.button2.setEnabled(False)

        self.setWindowTitle('Rock player')

        self.timer = QTimer()

        self.threadpool = QThreadPool()

        self.timer.timeout.connect(self.work)

        self.show()
        self.player = None


    def work(self):
        worker = Worker(self.update_song_info)
        self.threadpool.start(worker)

    def default_photo(self):
        sleep(0.5)
        self.label.setPixmap(QtGui.QPixmap(None))
        self.titleL.setText('Click PLAY')

    def update_song_info(self):
        try:
            song = song_data(url, url_photo,default_photo)
            self.titleL.setText(song.title)

            try:
                data = urlopen(song.photo).read()
            except:  # če slike ne more naložiti 404

                track_cover = default_photo
                data = urlopen(track_cover).read()

            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.label.setPixmap(QtGui.QPixmap(pixmap))

        except:

            self.titleL.setText('No Stream!')#Če ni povezave
            self.label.setPixmap(QtGui.QPixmap(None))

    def pushButtonPressed(self):

        try:
            self.player = stream(url)
        except:
            self.titleL.setText('No Stream!')


        self.button.setEnabled(False)
        self.button2.setEnabled(True)

        self.work()

        self.timer.start(3000)

    def pushButton_2Pressed(self):

        self.player.stop()
        self.timer.stop()

        self.button.setEnabled(True)
        self.button2.setEnabled(False)

        worker= Worker(self.default_photo)
        self.threadpool.start(worker)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Ui()
    window.show()
    sys.exit(app.exec_())