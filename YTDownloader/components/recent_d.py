from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

class RecentDownload(MDBoxLayout):
    rTitle = StringProperty('Lorem ipsum dolor sit')
    rTime= StringProperty('1 year ago')
    rThumbnail = StringProperty('assets/images/3.jpg')