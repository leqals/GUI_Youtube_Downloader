# GUI_Youtube_Downloader
This application made with Kivy/KivyMD and PyTube downloads Youtube videos of different qualities

## MODULES USED 
The following Modules where used 
1. Kivy/KivyMD: Kivy and KivyMD where used to create the User Interface and also make it interactive. 
2. PyTube: PyTube was used to get the Thumbnail image, the youtube video's information and also download.
3. OS: The OS module was used to create folders, get file paths and check if a folder exist.
4. JSON: The json module was used to read and write to a .json file.
5. DateTime: was used to get, compare and make the UI interactive according the time reading.

## MAJOR FILES
The App has 4 major files which include:
1. Main.py: Contains all the logic of the app. It is where the link of the video is gotten from the UI and used to grab information for updating the UI and downloading the video.
2. Main.kv: It is where the User Interface is defined. It defines the app as an MDScreen and consist of a fixed top bar and scrollable content.
3. recent_d.py: This is where the attributes of the Recent download such as Title, Thumbnail and time are defined. 
4. recent_d.kv: Here the UI of the recent download is created.
