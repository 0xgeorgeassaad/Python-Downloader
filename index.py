
__author__ = "George Assad"




### required libraries
### PyQt >> installtion : pip3 install pyqt5
### pafy >> installtion : pip3 install pafy
### youtube-dl is required for pafy to run properly >> installtion : pip3 install youtube-dl

# PyQt website :  http://pyqt.sourceforge.net/Docs/PyQt5/installation.html
# Pafy website :  http://pythonhosted.org/Pafy/

#### Testing whether PyQt is installed or not


# print("Qt version:", QT_VERSION_STR)
# print("SIP version:", SIP_VERSION_STR)
# print("PyQt version:", PYQT_VERSION_STR)




#PyQT5 Import

from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import os
from os import path
import humanize
import sys
import pafy
import urllib.request

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UIEdits()
        self.Handle_Buttons()


    def Handle_UIEdits(self):
        self.setWindowTitle('CS50 Downloader')
        self.setFixedSize(672,360)


    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)
        self.pushButton_9.clicked.connect(self.get_YoutubeVideo)
        self.pushButton_6.clicked.connect(self.download_YoutubeVideo)
        self.pushButton_5.clicked.connect(self.youtubeVideo_browse)
        self.pushButton_7.clicked.connect(self.youtubeVideo_browse)
        self.pushButton_8.clicked.connect(self.youtubePlaylist_download)



    def Handle_Browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All File(*.*)" )
        save_loc_str = str(save_location)
        saveFiltered = (save_loc_str[2:].split(",")[0].replace("'", ""))
        self.lineEdit_2.setText(saveFiltered)


    def Handle_ProgessBar(self , blocknum , blocksize , totalsize):
        read = blocknum * blocksize

        if totalsize > 0:
            percentage = (read / totalsize) * 100
            self.progressBar.setValue(percentage)
            QApplication.processEvents()




    def Download(self):
        # url - save location
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        try:
            urllib.request.urlretrieve(url ,save_location , self.Handle_ProgessBar)
        except Exception:
            QMessageBox.warning(self, "Download Error", "The download failed")
            return


        QMessageBox.information(self , "Download completed" , "The download finished" )
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    #### Youtube Video Download ###

    def youtubeVideo_browse(self):
        youtubeSaveLocation = QFileDialog.getExistingDirectory(self, "Select Download Location")
        self.lineEdit_7.setText(youtubeSaveLocation)
        self.lineEdit_8.setText(youtubeSaveLocation)


    def download_YoutubeVideo(self):
        video_URL = self.lineEdit_3.text()
        v = pafy.new(video_URL)
        st = v.allstreams
        quality_index = self.comboBox.currentIndex()
        save_location = self.lineEdit_7.text()

        down = st[quality_index].download(filepath=save_location)

        QMessageBox.information(self, "Download completed", "The youtube video download finished")

    ###### Youtube Playlist Download ####

    def youtubePlaylist_download(self):
        playlist_URL = self.lineEdit_9.text()
        save_location = self.lineEdit_8.text()
        playlist = pafy.get_playlist(playlist_URL)
        playlist_videos = playlist['items']


        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        for video in playlist_videos:
            pVideo = video['pafy']
            bestVideos = pVideo.getbest(preftype='mp4')
            bestVideos.download()


    def get_YoutubeVideo(self):
        video_URL = self.lineEdit_3.text()
        v = pafy.new(video_URL)
        # print(v.title)
        # print(v.duration)
        # print(v.rating)
        # print(v.author)
        # print(v.length)
        # print(v.keywords)
        # print(v.thumb)
        # print(v.videoid)
        # print(v.viewcount)
        # You could use v.allstreams to get A list of all available streams
        st = v.videostreams
        #print(st)
        #print(type(st))
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = '{} {} {} {}'.format(s.mediatype, s.extension, s.quality, size)
            self.comboBox.addItem(data)

            



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_() #infinite loop

if __name__ == '__main__':
    main()





