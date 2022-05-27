import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Ortusa')
        panel = wx.Panel(self)
        VBOX = wx.BoxSizer(wx.VERTICAL)
        HBOX= wx.BoxSizer(wx.HORIZONTAL )

        self.text_table = wx.TextCtrl(panel,style=wx.TE_MULTILINE)
        self.text_input = wx.TextCtrl(panel)

        VBOX.Add(self.text_table, 1, wx.ALL | wx.EXPAND, 5)




        HBOX.Add(self.text_input, 80, 1)


        my_btn = wx.Button(panel, label='Send Message')
        HBOX.Add(my_btn, 10 , 15)

        VBOX.Add(HBOX)




        panel.SetSizer(VBOX)
        self.Show()


    def scale_bitmap(self,bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()