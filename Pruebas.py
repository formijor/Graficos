'''
Created on 2 abr. 2020

@author: jor_l
'''
import wx
#import wx.GCDC

def OnPaint(self, event):
        self.OnPaintDC(event)
        self.OnPaintGC(event)

def OnPaintDC(self, event):
    dc = wx.PaintDC(self)

    dc.SetPen(wx.GREEN_PEN)
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.DrawCircle(150.0, 50.0, 50.0)
    dc.DrawLine(100.0, 50.0, 200.0, 50.0)
    dc.DrawLine(150.0, 0.0, 150.0, 100.0)
    dc.DrawRectangle(125.0, 25.0, 50.0, 50.0)

def OnPaintGC(self, event):
    dc = wx.PaintDC(self)
    gc = wx.GraphicsContext.Create(dc)

    if gc:
        gc.SetPen(wx.RED_PEN)
        path = gc.CreatePath()
        path.AddCircle(50.0, 50.0, 50.0)
        path.MoveToPoint(0.0, 50.0)
        path.AddLineToPoint(100.0, 50.0)
        path.MoveToPoint(50.0, 0.0)
        path.AddLineToPoint(50.0, 100.0)
        path.CloseSubpath()
        path.AddRectangle(25.0, 25.0, 50.0, 50.0)
        gc.StrokePath(path)

        # Draw a Bézier curve
        gc.SetPen(wx.BLUE_PEN)
        path = gc.CreatePath()
        path.MoveToPoint(120.0, 160.0)
        path.AddCurveToPoint((35, 200), (220, 260), (220, 40))
        gc.StrokePath(path)