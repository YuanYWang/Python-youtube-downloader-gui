from pytube import YouTube
import os
from ffmpy3 import FFmpeg


class StreamInfo():
    def __str__(self):
        if self.videoaudio == 'a':  # pure audio stream
            return self.itag + ':' + self.mimeType + ':' + self.aop + ':abr:' + self.abr + ':' + str(
                int(self.fileSize / 1048576)) + 'MB' #convert from byte to mega byte
        elif self.videoaudio == 'v':  # pure video stream
            return self.itag + ':' + self.mimeType + ':' + self.aop + ':Res ' + self.resolution + ',' + str(
                self.fps) + 'fps,' + str(int(self.fileSize / 1048576)) + 'MB'
        elif self.videoaudio == 'va':  # video audio
            return self.itag + ':' + self.mimeType + ':' + self.aop + ':Res ' + self.resolution + ',' + str(
                self.fps) + 'fps,, abr:' + self.abr + ',' + str(int(self.fileSize / 1048576)) + 'MB'
        else:  # something is wrong
            return self.itag + ':something is wrong'


class MyYoutubeDownload():
    def __init__(self, videoURL):
        self.videoURL = videoURL
        self.yt = YouTube(self.videoURL)
        self.title = self.yt.title
        alls = self.yt.streams.all()
        self.steamInfoS = []
        for a in alls:
            si = StreamInfo()
            si.itag = a.itag
            if a.resolution != None:
                si.resolution = a.resolution
            else:
                si.resolution = ''
            if a.abr != None:
                si.abr = a.abr
            else:
                si.abr = ''
            if a.fps != None:
                si.fps = a.fps
            else:
                si.fps = ''
            try:
                if a.filesize != None and isinstance(a.filesize, int):
                    si.fileSize = a.filesize
                else:
                    si.fileSize = 0
            except Exception as e:
                si.fileSize = 0
            if a.is_adaptive:
                si.aop = 'A'
            elif a.is_progressive:
                si.aop = 'P'
            else:
                si.aop = ''
            if a.mime_type != None:
                si.mimeType = a.mime_type
            else:
                si.mimeType = ''
            if a.includes_video_track and a.includes_audio_track:
                si.videoaudio = 'va'
            elif a.includes_video_track and not a.includes_audio_track:
                si.videoaudio = 'v'
            elif not a.includes_video_track and a.includes_audio_track:
                si.videoaudio = 'a'
            else:
                si.videoaudio = ''
            self.steamInfoS.append(si)

    def videoOnlyStream(self):
        result = []
        for si in self.steamInfoS:
            if si.videoaudio == 'v':
                result.append(si.__str__())
        return result

    def audioOnlyStream(self):
        result = []
        for si in self.steamInfoS:
            if si.videoaudio == 'a':
                result.append(si.__str__())
        return result

    def videoaudioStream(self):
        result = []
        for si in self.steamInfoS:
            if si.videoaudio == 'va':
                result.append(si.__str__())
        return result

    def downloadStream(self, aTag, aDir):
        self.downloadDir = aDir
        ytd = self.yt.streams.get_by_itag(aTag)
        self.fname = ytd.default_filename
        self.downloadedFileName = str(aTag) + self.fname
        if not os.path.exists(aDir):
            os.makedirs(aDir)
        ytd.download(aDir)
        os.rename(aDir + '\\' + self.fname, aDir + '\\' + self.downloadedFileName)

    def processStreams(self, aFile1, aFile2, aDir):
        idx = self.fname.rfind('.')
        outFileName = self.fname[:idx]+'.mp4'
        ff = FFmpeg(
            inputs={aDir + '\\' + aFile1: None, aDir + '\\' + aFile2: None},
            outputs={aDir + '\\' + outFileName: None}
        )
        ff.run()

    def makeMp3(self, aFile, aDir):
        idx = self.fname.rfind('.')
        outFileName = self.fname[:idx] + '.mp3'
        ff = FFmpeg(
            inputs={aDir + '\\' + aFile: None},
            outputs={aDir + '\\' + outFileName: '-vn'}
        )
        ff.run()
