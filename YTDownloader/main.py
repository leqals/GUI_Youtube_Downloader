import os 
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.app import MDApp 
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from components.recent_d import RecentDownload
from pytube import YouTube
from datetime import datetime
import os
import json


Window.size = (320, 600)

PARENT_DIR = os.getcwd()
R_DOWNLOADS_PATH = os.path.join(PARENT_DIR, 'recent_thumbnails')
DOWNLOAD_PATH = os.path.join(PARENT_DIR, 'youtube_videos')
JSON_PATH = 'assets/data/recent.json'


# UTILITY FUNCTIONS

def timesince(dt, default="now"):
    now = datetime.now()
    dt = datetime.fromisoformat(dt)
    diff = now - dt
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default   


def write_json(data, filename = JSON_PATH):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)





# KIVY CLASSES

class Main(MDScreen):
    link = StringProperty('')
    thumbnail = StringProperty('assets/images/1.jpg')
    title = StringProperty('Lorem ipsum dolor sit amet')
    desc = StringProperty('Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, neque')
    author = StringProperty('Dev.Leqals')
    res = StringProperty('320p')
    
    yt = None
    
    # get link
    
    def get_link(self, widget):
        self.link = widget.text
        
        # With link get video thumnail, title, description and author
        try: 
            self.yt = YouTube(self.link)
            self.title = self.yt.title
            self.thumbnail = self.yt.thumbnail_url
            self.desc = self.yt.description
            self.author = self.yt.author
            
             # Shorten 
            self.title = ' '.join(self.title.split(' ')[:5])
            self.desc = ' '.join(self.desc.split(' ')[:9])
            
            res_list = [stream.resolution for stream in self.yt.streams.filter(progressive=True)]
            res_list = res_list[-2:]
            for resolution in res_list:
                self.ids.res.add_widget(MDFlatButton(
                    text = resolution,
                    font_size= '10',
                    md_bg_color = "#FCE4E4",
                    on_press= lambda x: self.set_res(x.text)
                ))
            
        except :
            self.title = 'Invalid Link'
            self.desc = 'Try something like "https://www.youtube.com/watch?v=GceNsojnMf0"'
        
    def set_res(self, res):
        self.res = res     
            
      
    def download(self):
        
        # OnDownloadclicked (isPath ? download to path and save_thumbnail()) : Create DownloadsPath and RecentPath then download
        if not os.path.exists(DOWNLOAD_PATH) or not os.path.exists(DOWNLOAD_PATH) : 
            os.mkdir(DOWNLOAD_PATH)
            os.mkdir(R_DOWNLOADS_PATH)
            
        if self.yt:
            with self.canvas.after:
                Color(1, 1, 1, 0.4)
                Rectangle(pos=self.pos, size=self.parent.size)
                
            self.download_video()
            self.add_recent()
       
            
    def add_recent(self):
        thumb_add = self.download_image(self.thumbnail)
        
        # isDone? time =  datetime.now, title = video_title, thumbnail = video_thumbnail.location
        recent = {
            'thumbnail': thumb_add,
            'title' : self.title,
            'time' : str(datetime.now())
            }
        
        
        # onDone: update_recent_downloads()
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
            temp = data['recent']
            temp.append(recent)
            
            write_json(data)
        
        self.get_json()
        
        self.desc = 'DOWNLOAD COMPLETE!!!'
        

    def download_video(self):
        self.yt.streams.filter(res= self.res).first().download(DOWNLOAD_PATH)
        
        
    def download_image(self, url):
        import requests # request img from web
        import shutil # save img locally

        res = requests.get(url, stream = True)
        thumb_add = ''
        
        if res.status_code == 200:
            file_name = f'{R_DOWNLOADS_PATH}/{self.title[:10]}_thumbnail.jpg'
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
                thumb_add = os.path.abspath(file_name)
                
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')
        
        return thumb_add
    
    
    def on_enter(self):
        self.get_json()
        
        
    def get_json(self):
        recentsWidgets = self.ids.recent.children
        if len(recentsWidgets) > 0:
            for child in recentsWidgets:
                self.ids.recent.remove_widget(child)
                
        with open('assets/data/recent.json', 'r') as r:
            data = json.loads(r.read())
            for recent in data['recent']:
                title = recent['title']
                tNail = recent['thumbnail']
                title = ' '.join(title.split(' ')[:6])
                time = recent['time']
                
                self.ids.recent.add_widget(RecentDownload(
                    rTitle = f'{title}...',
                    rThumbnail = tNail,
                    rTime = timesince(time)
                ))  
        
    
            
class YTDownloader(MDApp):
    def build(self):
        self.ld_kv_files()
        return Main()
    
    def ld_kv_files(self):
        Builder.load_file('components/recent_d.kv')
        Builder.load_file('components/Nav/nav.kv')
        Builder.load_file('main.kv')
        
    def on_start(self):
        self.root.dispatch('on_enter')

if  __name__ == '__main__': YTDownloader().run()