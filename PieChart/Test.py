'''
Created on 24 mar. 2022

@author: jor_l
'''

import wx
import math
import random
import operator

from Clasic.Main import ClassicPie


class GraficoDibujo(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.parent = parent
        self.SetMinSize((900, 600))
        self.SetBackgroundColour(wx.WHITE)
        self.panel= wx.Panel(self)
        self.panel.SetDoubleBuffered(True)
        self.mdc = None
        self.centro_pos = (300, 300)
        self.radio = 100       
        
        self.panel.Bind(wx.EVT_SIZE, self.on_resize)
        self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.capturar_erase_background)        
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.crear_grafico(0)
        self.crear_boton_rotar()
        self.crear_boton_seleccionar_porcion()
        self.crear_boton_seleccionar_grafico()
        self.crear_boton_seleccionar_radio()
    
    def capturar_erase_background(self, event):
        '''No hacer nada'''
        pass
    
    def crear_boton_rotar(self):
        self.text = wx.TextCtrl(self.panel, pos= (750, 300), value='0')
        self.spin = wx.SpinButton(self.panel, pos = (750,350), style=wx.SP_VERTICAL)
        self.spin.SetRange(0,360)
        self.spin.SetValue(0)
        self.spin.Bind(wx.EVT_SPIN, self.cambiar_orientacion)
    
    def crear_boton_seleccionar_porcion(self):
        self.text2 = wx.TextCtrl(self.panel, pos= (600, 300), value='-1')
        self.spin2 = wx.SpinButton(self.panel, pos = (600,350), style=wx.SP_VERTICAL)
        self.spin2.SetRange(-1, 6)
        self.spin2.SetValue(-1)
        self.spin2.Bind(wx.EVT_SPIN, self.seleccionar_porcion)    
        
    def crear_boton_seleccionar_grafico(self):
        self.text3 = wx.TextCtrl(self.panel, pos= (600, 150), value='Clasico')
        self.spin3 = wx.SpinButton(self.panel, pos = (600,200), style=wx.SP_VERTICAL)
        self.spin3.SetRange(0, 3)
        self.spin3.SetValue(0)
        self.spin3.Bind(wx.EVT_SPIN, self.seleccionar_grafico)
        
    def crear_boton_seleccionar_radio(self):
        self.text4 = wx.TextCtrl(self.panel, pos= (750, 150), value=str(self.get_radio()))
        self.spin4 = wx.SpinButton(self.panel, pos = (750,200), style=wx.SP_VERTICAL)
        self.spin4.SetRange(0, 150)
        self.spin4.SetValue(self.get_radio())
        self.spin4.Bind(wx.EVT_SPIN, self.set_radio)
        
    def cambiar_orientacion(self, event):
        '''Cambia la orientacion seteando el grado inicial distinto de 0'''
        grado = int(self.spin.GetValue())
        if grado == 360:
            grado = 0
            self.spin.SetValue(0)
        self.text.SetValue(str(grado))
        self.grafico.rotar_grafico(grado)
        self.on_resize(None)    
        
    def seleccionar_porcion(self, event):
        '''Desactiva porcion'''
        porcion_id = self.spin2.GetValue() 
        self.grafico.seleccionar_porcion(porcion_id)
        self.text2.SetValue(str(porcion_id))
        self.on_resize(None)
        
    def seleccionar_grafico(self, event):
        '''Selecciona el tipo de grafico'''
        grafico_id = self.spin3.GetValue()
        
        self.grafico.cambiar_tipo_grafico(grafico_id)
        self.on_resize(None)
        nombre = self.grafico.get_tipo_grafico_nombre()
        self.text3.SetValue(str(nombre))  
    
    def set_radio(self, event):
        '''Setea el radio del grafico'''
        radio = self.spin4.GetValue()
        self.radio = radio
        self.text4.SetValue(str(radio))
        self.grafico.cambiar_radio(radio)
        self.on_resize(None)
    
    def get_radio(self):
        return self.radio
    
    def get_centro(self):
        return self.centro_pos
    
    def get_datos(self, datos):
        pass
    
    def set_datos(self):
        pass
    
    def actualizar(self):
        pass
    
    def dibujar_circulo(self):
        pass
    
    def obtener_tamanio_frame(self):
        w, h = self.panel.GetClientSize()
        return w, h
    
    def on_resize(self, event):
        w, h= self.obtener_tamanio_frame()
        self.panel.SetSize(0, 0, w, h)
        self.mdc = wx.MemoryDC(wx.Bitmap(w, h))
        
        #self.redibujar()
        #self.redibujar_gdc()
        self.dibujar_grafico()
        self.Refresh()
        
    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self.panel)
        
        if not self.mdc:
            return
        w, h = self.mdc.GetSize()
        dc.Blit(0, 0, w, h, self.mdc, 0, 0)
        
    #-------------------------------------------------------------------
    
    def generar_datos(self):
        lista_porcentajes = [(115) 
                             ,(90)
                             ,(72)
                             ,(28)
                             ,(20)
                             ,(20)
                             ,(15)]
        return lista_porcentajes      
    
    def dibujar_grafico(self):
        dc = self.mdc
        gcdc = wx.GCDC(dc)
        gc = gcdc.GetGraphicsContext()
        dc.Clear()        
        self.grafico.dibujar_grafico(gc)
        
    def crear_grafico(self, tipo):
        centro = self.get_centro()
        datos = self.generar_datos()
        self.grafico = ClassicPie('Gastos sueldo', centro, self.get_radio(), datos, 0) 
        
    def porcion(self, r, a, c, dc, x, y, xc, yc, color, grados, gc):
        x2, y2 = self.definir_triangulo(r,grados, c)
        x2 = c[0] + x2
        y2 = c[1] - y2
        x2 = round(x2)
        y2 = round(y2)
        #self.dibujar_triangulo(r, grados, dc)
        dc.SetPen(wx.Pen(wx.WHITE, 2))
        dc.SetBrush(wx.Brush(wx.Colour(color)))        
        dc.DrawArc(x, y, x2, y2, c[0], c[1])
        return x2, y2
            
    def rotar(self, grados, rotacion):
        return grados + rotacion
        
    def dibujar_linea_divisoria(self,dc, x, y, x2, y2):
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.DrawLine(x, y, x2, y2)
    
    def dibujar_perimetro_interior_gcdc(self, x, y, r, gc, color, width):
        pen = wx.Pen(color)
        pen.SetWidth(width)
        gc.SetPen(gc.CreatePen(pen))
        
        p = gc.CreatePath()
        p.MoveToPoint(x,y)          
        p.AddCircle(x, y, r)
        gc.StrokePath(p)
            
    def relleno_anillo_interior_gcdc(self, x, y, r, gc, color):
        brush = gc.CreateBrush(wx.Brush(color))
        gc.SetBrush(brush)
        
        p = gc.CreatePath()
        p.MoveToPoint(x,y)          
        p.AddCircle(x, y, r)
        gc.FillPath(p)
        
    def dibujar_perimetro_gcdc(self, x, y, r, gc, color):
        pn = wx.Pen(color)
        pn.SetWidth(2)
        pen = gc.CreatePen(pn)
        gc.SetPen(pen)

        p = gc.CreatePath()
        p.MoveToPoint(x,y)          
        p.AddCircle(x, y, r)
        gc.StrokePath(p)
    
    def dibujar_perimetro(self,x, y, r, dc, color):
        dc.SetPen(wx.Pen(wx.WHITE))
        dc.SetBrush(wx.Brush(color))
        dc.DrawCircle(x, y, r)    
        
    def dibujar_triangulo(self, r, a, dc):
        c = 500, 500
        d = 500
        x, y = self.definir_triangulo(r, a, c) 
        dc.SetPen(wx.Pen(wx.RED))
        dc.DrawLine(c[0], c[1], x +d, c[1])
        dc.SetPen(wx.Pen(wx.BLUE))
        dc.DrawLine(x+d, c[1], x+d, d-y)
        dc.SetPen(wx.Pen(wx.GREEN))
        dc.DrawLine(c[0], c[1], x+d, d-y)
        
    def calcular_perimetro(self, radio):
        return 2*math.pi*radio
        
    def calcular_perimetro_porcion(self, radio, angulo):
        return (2*math.pi*radio*angulo) / 360
        
    def definir_triangulo(self, hipotenusa, angulo, centro):
        '''obtiene la medida de los catetos'''
        angulo = math.radians(angulo)
        x = math.cos(angulo) * hipotenusa 
        y = math.sin(angulo) * hipotenusa
        c= x, y
        return c
    
    
app = wx.App()
frame = GraficoDibujo(None)
frame.Show()
app.MainLoop()