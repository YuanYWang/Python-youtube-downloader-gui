import MyYoutubeDownload
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

wlist = []  # widget list, to be diabled and enabled
ytds = {}  # MyYoutubeDownload in a dict with youtube title as key
currentURL = ''


def checkYoutube():
    statusBar.showMessage('')
    global currentURL
    currentURL = urlInput.text()
    if currentURL == '':
        statusBar.showMessage('Please enter video url')
        return
    disableAllWidget()
    try:

        ytd = MyYoutubeDownload.MyYoutubeDownload(currentURL)
        ytds[ytd.videoURL] = ytd
        avB.setChecked(True)
        mvideoAudioStreams()
        avideoStream()
        aaudioStream()
        enableAllWidget()
    except Exception as e:
        statusBar.showMessage(str(e))


def mvideoAudioStreams():
    manualSelection.clear()
    manualSelection.addItems(ytds[currentURL].videoaudioStream())


def mpureVideoStreams():
    manualSelection.clear()
    manualSelection.addItems(ytds[currentURL].videoOnlyStream())


def mpureAudioStreams(ytd):
    manualSelection.clear()
    manualSelection.addItems(ytds[currentURL].audioOnlyStream())


def avideoStream():
    autoVSelection.clear()
    autoVSelection.addItems(ytds[currentURL].videoOnlyStream())
    autoVSelection.addItems(ytds[currentURL].videoaudioStream())


def aaudioStream():
    autoASelection.clear()
    autoASelection.addItems(ytds[currentURL].audioOnlyStream())
    autoASelection.addItems(ytds[currentURL].videoaudioStream())


def disableAllWidget():
    for w in wlist:
        w.setEnabled(False)


def enableAllWidget():
    for w in wlist:
        w.setEnabled(True)


def manualDownloadYouTube():
    disableAllWidget()
    statusBar.showMessage('')
    if dir.text() == '':
        statusBar.showMessage('Please choose a directory to download to')
        return
    try:
        s = manualSelection.currentText()
        i = s.find(':')
        tag = s[:i]
        ytds[currentURL].yt.register_on_progress_callback(progress_function)
        progessBar.reset()
        ytds[currentURL].downloadStream(tag, dir.text())
        downloadedFileName = ytds[currentURL].downloadedFileName
        if mmp3CheckBox.isChecked():
            ytds[currentURL].makeMp3(downloadedFileName, dir.text())
        statusBar.showMessage(ytds[currentURL].title + ' download finished')
    except Exception as e:
        statusBar.showMessage(str(e))
    enableAllWidget()


def autoDownloadYouTube():
    disableAllWidget()
    statusBar.showMessage('')
    if dir.text() == '':
        statusBar.showMessage('Please choose a directory to download to')
        return
    try:
        s = autoVSelection.currentText()
        i = s.find(':')
        tag1 = s[:i]
        ytds[currentURL].yt.register_on_progress_callback(progress_function)
        progessBar.reset()
        ytds[currentURL].downloadStream(tag1, dir.text())
        downloadedFileName1 = ytds[currentURL].downloadedFileName
        s = autoASelection.currentText()
        i = s.find(':')
        tag2 = s[:i]
        progessBar.reset()
        ytds[currentURL].downloadStream(tag2, dir.text())
        downloadedFileName2 = ytds[currentURL].downloadedFileName
        ytds[currentURL].processStreams(downloadedFileName1, downloadedFileName2, dir.text())
        if amp3CheckBox.isChecked():
            ytds[currentURL].makeMp3(downloadedFileName2, dir.text())
        statusBar.showMessage('download finished')
    except Exception as e:
        statusBar.showMessage(str(e))
    enableAllWidget()


def openDirSelect():
    dir.setText(QFileDialog.getExistingDirectory())


def progress_function(stream, chunk, file_handle, bytes_remaining):
    progessBar.setValue(round((1 - bytes_remaining / stream.filesize) * 100, 3))


app = QApplication([])
newFont = QFont("Times", 15)
window = QWidget()
window.setFixedSize(850, 500)
layout = QGridLayout()

layout.addWidget(QLabel('Youtube URL:'), 0, 0)
# youtube url input
urlInput = QLineEdit()
urlInput.setFont(newFont)
wlist.append(urlInput)
layout.addWidget(urlInput, 2, 0)

checkURLButton = QPushButton('Check URL')
wlist.append(checkURLButton)
checkURLButton.clicked.connect(checkYoutube)
layout.addWidget(checkURLButton, 2, 1)

tabs = QTabWidget()
manualTab = QWidget()
autoTab = QWidget()
tabs.resize(850, 250)
tabs.addTab(autoTab, 'combine multi stream')
tabs.addTab(manualTab, 'single stream')
# single stream download setup, can pick AV, A or V stream to download
avB = QRadioButton("Video Audio")
videoB = QRadioButton("Video only")
audioB = QRadioButton("Audio only")
avB.clicked.connect(mvideoAudioStreams)
videoB.clicked.connect(mpureVideoStreams)
audioB.clicked.connect(mpureAudioStreams)
avB.setChecked(True)
mmp3CheckBox = QCheckBox('MP3')
mDownloadButton = QPushButton('download')
wlist.append(avB)
wlist.append(videoB)
wlist.append(audioB)
wlist.append(mmp3CheckBox)
mhbl = QHBoxLayout()
mhbl.addWidget(avB)
mhbl.addWidget(videoB)
mhbl.addWidget(audioB)
mhbl.addWidget(mmp3CheckBox)
mhbl.addWidget(mDownloadButton)
mDownloadButton.clicked.connect(manualDownloadYouTube)
manualTabLayout = QVBoxLayout()
manualTabLayout.addLayout(mhbl)
manualSelection = QComboBox()
manualSelection.setFont(newFont)
wlist.append(manualSelection)
manualTabLayout.addWidget(manualSelection)
manualTab.setLayout(manualTabLayout)
# multi stream download page tab, pick a video steam and audio stream, use ffmpeg to combine
autoVSelection = QComboBox()
autoASelection = QComboBox()
autoVSelection.setFont(newFont)
autoASelection.setFont(newFont)
aDownloadButton = QPushButton('download')
aDownloadButton.clicked.connect(autoDownloadYouTube)
amp3CheckBox = QCheckBox('MP3')
wlist.append(autoVSelection)
wlist.append(autoASelection)
wlist.append(aDownloadButton)
wlist.append(amp3CheckBox)
autoTabLayout = QGridLayout()
autoTabLayout.addWidget(QLabel('Select Video:'), 0, 0, 1, 2)
autoTabLayout.addWidget(autoVSelection, 1, 0, 4, 5)
autoTabLayout.addWidget(QLabel('Select Audio:'), 5, 0, 1, 2)
autoTabLayout.addWidget(autoASelection, 6, 0, 4, 5)
autoTabLayout.addWidget(amp3CheckBox, 10, 0)
autoTabLayout.addWidget(aDownloadButton, 10, 2)
autoTab.setLayout(autoTabLayout)

layout.addWidget(tabs, 3, 0, 1, 2)
# where to save the downloaded video and audio
dirLabel = QLabel('Download Youtube Video to:')
dir = QLabel()
dir.setText('D:\\youtube audio video')
dir.setFont(newFont)

chooseDirButton = QPushButton('download dir')
wlist.append(chooseDirButton)
chooseDirButton.clicked.connect(openDirSelect)
qhl2 = QHBoxLayout()
qhl2.addWidget(dirLabel)
qhl2.addWidget(dir)
layout.addLayout(qhl2, 5, 0)
layout.addWidget(chooseDirButton, 5, 1)

progessBar = QProgressBar()
layout.addWidget(progessBar, 6, 0)

statusBar = QStatusBar()
statusBar.setFont(newFont)
layout.addWidget(statusBar, 7, 0)

window.setLayout(layout)
window.show()
app.exec_()
