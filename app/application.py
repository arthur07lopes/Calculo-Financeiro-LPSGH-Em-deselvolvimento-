import wx

from app.config import APP_NAME, MIN_SIZE, WINDOW_SIZE
from app.services.storage import StorageService
from app.ui.main_frame import MainFrame


class FinanceApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_NAME)
        self.SetVendorName("LPSGH")
        self.SetClassName("LPSGHFinancas")
        self.frame = MainFrame(
            storage=StorageService(),
            title=APP_NAME,
            size=WINDOW_SIZE,
            min_size=MIN_SIZE,
        )
        self.frame.Centre()
        self.frame.show_with_fade()
        return True

    def run(self):
        self.MainLoop()
