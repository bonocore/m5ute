import wx
import wx.adv
import soundControl
import bleConnection

TRAY_ICON_ON = 'microphone.png'
TRAY_ICON_OFF = 'microphone-off.png'

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.myapp_frame = frame
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        is_muted = soundControl.is_default_muted()
        self.refresh_icon(is_muted)

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, "M5 Mute utility")

    def CreatePopupMenu(self):
        self.menu = wx.Menu()
        self.create_menu_item(self.menu, "About", -1, self.on_about)
        self.menu.AppendSeparator()
        self.create_menu_item(self.menu, "Exit", -1, self.on_exit)
        return self.menu

    @staticmethod
    def create_menu_item(menu, label, id, func):
        item = wx.MenuItem(menu, id, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def on_left_down(self,event):
        is_muted = soundControl.is_default_muted()
        if(is_muted):
          soundControl.unmute()
        else:
          soundControl.mute()

        self.refresh_icon(is_muted)

    def refresh_icon(self,is_muted):
        #print("refresh_icon")
        if(is_muted):
           self.set_icon(TRAY_ICON_OFF)
           bitmap = wx.Bitmap('microphone-off-osd.png', wx.BITMAP_TYPE_PNG)
           splash = wx.adv.SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,300, None, -1)
        else:
           self.set_icon(TRAY_ICON_ON)
           bitmap = wx.Bitmap('microphone-osd.png', wx.BITMAP_TYPE_PNG)
           splash = wx.adv.SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,300, None, -1)
    def on_about(self, event):
        print("on_about")

    def on_exit(self, event):
        print("exit")
        self.myapp_frame.Close()


class MyApplication(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1, 1))
        soundControl.EVT_RESULT(self,self.updateStatus)
        self.soundControl=soundControl.SoundControl(self)
        self.soundControl.start()
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.m5BleConnection=bleConnection.BleConnection(self)
        self.m5BleConnection.start()


    def on_close(self, event):
        print("destroy app")
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()

    def updateStatus(self, evt):
        #print("updateMicStatus")
        is_muted=soundControl.is_default_muted()
        self.myapp.refresh_icon(is_muted)
        self.m5BleConnection.update_mute_status(is_muted);

MyApp = wx.App()
MyApplication()
MyApp.MainLoop()
