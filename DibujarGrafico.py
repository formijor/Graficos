'''
Created on 23 mar. 2020

@author: jor_l
'''
import wx
import math
import random
import operator


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
        self.grafico = Grafico('Gastos sueldo', centro, self.get_radio(), datos, 0) 
        
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

'----------------------------------------------------------------------------'
         
class Grafico():
    def __init__(self, nombre, posicion, radio, datos, orientacion):
        self.nombre = nombre
        self.posicion = posicion
        self.radio = radio
        self.tipo_id = 0
        self.datos = datos
        self.lista_porciones = []        
        self.ancho_lineas = 0
        self.rotar = orientacion
        self.set_lista_colores()
        self.crear_tipos_graficos()
        self.set_tipo_grafico(self.tipo_id)
        self.crear_porciones()
            
    def get_nombre(self):
        return self.nombre
    
    def get_posicion(self):
        return self.posicion
    
    def get_tipo_grafico(self):
        return self.tipo_grafico
    
    def get_datos(self):
        return self.datos
    
    def get_ancho_lineas_divisorias(self):
        return self.tipo_grafico.get_ancho_lineas_divisorias()
        
    def get_variacion_radio(self):
        return self.tipo_grafico.get_variacion_radio()   
    
    def get_color_desactivado(self):
        return self.tipo_grafico.get_color_desactivado()     
    
    def get_porciones(self):
        return self.lista_porciones
    
    def get_color_lineas_divisorias(self):
        return self.tipo_grafico.get_color_lineas_divisorias()
    
    def get_operador(self):
        return self.tipo_grafico.get_operador()
    
    def get_tipo_grafico_nombre(self):
        return self.tipo_grafico.get_nombre()
    
    def set_datos(self, datos):
        self.datos = datos
        
    def set_radio(self, radio):
        self.radio = radio
        
    def cambiar_radio(self, radio):
        self.set_radio(radio)
        self.lista_porciones = []
        self.crear_porciones()
        
    def rotar_grafico(self, grados):
        self.rotar = grados
        
    def get_rotar_grafico(self):
        return self.rotar 
    
    def seleccionar_porcion(self, porcion_id):
        for porcion in self.lista_porciones:
            porcion.set_desactivado()
        self.lista_porciones[porcion_id].set_activado()
    
    def set_tipo_grafico(self, tipo_indice):
        self.tipo_grafico = self.tipos_graficos[tipo_indice]
    
    def cambiar_tipo_grafico(self, tipo_indice):
        self.set_tipo_grafico(tipo_indice)
        self.lista_porciones = [] #Hay que cambiarlo por un metodo de actualizacon
        self.crear_porciones()
    
    def set_lista_colores(self):
        self.lista_colores = [(0,255,0)
                                  ,(0,0,255)
                                  ,(255,0,0)
                                  ,(0,255,255)
                                  ,(255,255,0)
                                  ,(255,0,255)
                                  ,(255,128,0)                                  
                                  ,(255,247,0)
                                  ,(255,0,239)
                                  ,(0,255, 255)
                                  ,(215,170,0)
                                  ]
    
    def crear_tipos_graficos(self):
        '''Crea las opciones de cada tipo de grafico'''
        self.tipos_graficos = [TipoGrafico('Clasico', 
                                        False, (255,255,255), 2,
                                        False, (255,255,255), 2,
                                        True, (255,255,255), 3,
                                        (60,60,60), 0, None, 0),
                               TipoGrafico('Moderno',
                                          False, (255,255,255), 2,
                                          False, (255,255,255), 2,
                                          True, (255,255,255), 3,
                                          (60,60,60), 10, None, 0),
                               TipoGrafico('Medialuna',
                                          False, (255,255,255), 2,
                                          False, (255,255,255), 2,
                                          True, (255,255,255), 3,
                                          (60,60,60), 10, operator.truediv, 2),
                               TipoGrafico('Cuarto',
                                          False, (255,255,255), 2,
                                          False, (255,255,255), 2,
                                          True, (255,255,255), 3,
                                          (60,60,60), 10, operator.truediv, 4                                          
                                           )
                                         ]
        
    def seleccionar_color_relleno(self, indice):
        '''Selecciona el color de relleno de las porciones'''
        cantidad =  len(self.lista_colores)
        if indice <= cantidad:
            return self.lista_colores[indice]
        else:
            return self.lista_colores[random.randrange(0, cantidad, 1)]
        
    def crear_porciones(self):
        '''Crea las porciones que componen el grafico'''
        datos = self.get_datos()
        contador = 0
        radio = self.radio
        variacion = self.get_variacion_radio()
        operador = self.get_operador()
        if datos is not None:
            for dato in datos:
                radio = radio + variacion
                if operador[0] is not None:
                    dato = operador[0](dato, operador[1])
                porcion = Porcion(radio, self.posicion, dato, self.seleccionar_color_relleno(contador),
                                   self.get_color_lineas_divisorias(), 
                                   self.get_ancho_lineas_divisorias(), self.get_color_desactivado())
                self.lista_porciones.append(porcion)
                contador = contador + 1
                
    def dibujar_grafico(self, gc):
        '''Dibuja el grafico, porcion a porcion'''
        def calcular_rotacion(grados_final):
            if grados_final > 360:
                grados_final = abs(360 - grados_final)
            return grados_final
        
        porciones = self.get_porciones()
        rotar = self.get_rotar_grafico()
        a = 0 
        g_final = 0 + rotar       
        grados = 0 + rotar
        
        for porcion in porciones:
            a = porcion.get_grados()         
            g_final = g_final + a            
            g_final = calcular_rotacion(g_final)            
            self.dibujar_porcion(gc, grados, g_final, porcion)
            grados = g_final
    
    def calcular_grados_grafico(self, gc):
        '''Calcula la orientacion en grados inicial y final de cada porcion'''
        def calcular_rotacion(grados_final):
            if grados_final > 360:
                grados_final = abs(360 - grados_final)
            return grados_final
        
        porciones = self.get_porciones()
        rotar = self.get_rotar_grafico()
        a = 0 
        g_inicial = rotar
        g_final = rotar       
        
        for porcion in porciones:
            a = porcion.get_grados()         
            g_final = g_final + a            
            g_final = calcular_rotacion(g_final)
            porcion.set_grados_porcion(g_inicial, g_final)
            g_inicial = g_final            
    
    def set_grados_porcion(self, porcion, grados_inicial, grados_final):
        porcion.set_grados_inicial_final(grados_inicial, grados_final)    
    
    def actualizar_porcion(self, porcion_id, datos):
        porcion = self.lista_porciones[porcion_id]
        porcion.actualizar_datos()        
    

             
    def dibujar_porcion(self, gc, grados_inicial, grados_final, porcion):
        '''Dibuja una porcion'''
        centro = porcion.get_posicion()
        radio = porcion.get_radio()
        color_relleno = porcion.get_color_activo()
        color_lineas = porcion.get_color_lineas()
        ancho_lineas = porcion.get_ancho_lineas_divisorias()
        
        pen = gc.CreatePen(wx.Pen(color_lineas, ancho_lineas))
        gc.SetPen(pen)
        
        brush = gc.CreateBrush(wx.Brush(color_relleno))
        gc.SetBrush(brush)
    
        p = gc.CreatePath()
        p.MoveToPoint(centro)          
        p.AddArc((centro), radio, math.radians(grados_final), math.radians(grados_inicial), False)
        p.AddLineToPoint(centro)
        
        gc.FillPath(p)
        gc.StrokePath(p)       
    
    
    def dibujar_grafico2(self, gc):
        porciones = self.get_porciones()
        for porcion in porciones:
            self.dibujar_porcion(gc, porcion)
    
    def dibujar_porcion2(self, gc, porcion):
        '''Dibuja una porcion'''
        centro = porcion.get_posicion()
        radio = porcion.get_radio()
        grados_inicial = porcion.get_grados_inicial()
        grados_final = porcion.get_grados_final()
        color_relleno = porcion.get_color_activo()
        color_lineas = porcion.get_color_lineas()
        ancho_lineas = porcion.get_ancho_lineas_divisorias()
        
        pen = gc.CreatePen(wx.Pen(color_lineas, ancho_lineas))
        gc.SetPen(pen)
        
        brush = gc.CreateBrush(wx.Brush(color_relleno))
        gc.SetBrush(brush)
    
        p = gc.CreatePath()
        p.MoveToPoint(centro)          
        p.AddArc((centro), radio, math.radians(grados_final), math.radians(grados_inicial), False)
        p.AddLineToPoint(centro)
        
        gc.FillPath(p)
        gc.StrokePath(p)  
'----------------------------------------------------------------------------------'

class Porcion():
    def __init__(self, radio, posicion, grados, color_relleno, color_lineas, ancho_lineas, color_desactivado):
        self.radio = radio
        self.posicion = posicion
        self.grados = grados 
        self.grados_inicial = 0
        self.grados_final = 0
        self.color_relleno = color_relleno
        self.color_lineas = color_lineas
        self.ancho_lineas = ancho_lineas
        self.color_desactivado = color_desactivado
        self.desactivado = 0
        self.seleccionado = 0
        self.set_color_activo(self.color_relleno)
    
    def get_posicion(self):
        return self.posicion
    
    def get_radio(self):
        return self.radio
    
    def get_grados(self):
        return self.grados
    
    def get_color_relleno(self):
        return self.color_relleno
    
    def get_color_desactivado(self):
        return self.color_desactivado 
    
    def get_color_lineas(self):
        return self.color_lineas
    
    def get_color_activo(self):
        return self.color_activo
    
    def get_ancho_lineas_divisorias(self):
        return self.ancho_lineas
    
    def get_grados_inicial(self):
        return self.grados_inicial
    
    def get_grados_final(self):
        return self.grados_final    
    
    def set_color_activo(self, color):
        self.color_activo = color
    
    def set_grados_inicial(self, grados_inicial):
        self.grados_inicial = grados_inicial
        
    def set_grados_final(self, grados_final):
        self.grados_final = grados_final
        
    def set_grados_inicial_final(self, grados_inicial, grados_final):
        self.set_grados_inicial(grados_inicial)
        self.set_grados_final(grados_final)
    
    def set_desactivado(self):
        self.desactivado = 0
        self.set_color_activo(self.color_desactivado)
        
    def set_activado(self):
        self.desactivado = 1
        self.set_color_activo(self.color_relleno)        
        
    def is_activo(self):
        return self.desactivado
    
    def is_seleccionado(self):
        return self.seleccionado

'--------------------------------------------------------------------------------------------'

class TipoGrafico():
    def __init__(self, nombre, perimetro, color_perimetro, ancho_perimetro,
                  perimetro_interior, color_perimetro_interior, ancho_perimetro_interior,
                  lineas_divisorias, color_lineas_divisorias, ancho_lineas_divisorias, color_desactivado, variacion_radio
                  , operador, valor_operador):
        self.nombre = nombre
        self.perimetro = perimetro
        self.color_perimetro = color_perimetro
        self.ancho_perimetro = ancho_perimetro
        self.perimetro_interior = perimetro_interior
        self.color_perimetro_interior = color_perimetro_interior
        self.ancho_perimetro_interior = ancho_perimetro_interior
        self.lineas_divisorias = lineas_divisorias
        self.color_lineas_divisorias = color_lineas_divisorias
        self.ancho_lineas_divisorias = ancho_lineas_divisorias
        self.color_desactivado = color_desactivado
        self.variacion_radio = variacion_radio
        self.operacion = (operador, valor_operador)
        
    def get_nombre(self):
        return self.nombre
    
    def is_perimetro(self):
        return self.perimetro
    
    def get_color_perimetro(self):
        return self.color_perimetro
    
    def get_ancho_perimetro(self):
        return self.ancho_perimetro
    
    def is_perimetro_interior(self):
        return self.perimetro_interior
    
    def get_color_perimetro_interior(self):
        return self.color_perimetro_interior
    
    def get_ancho_perimetro_interior(self):
        return self.ancho_perimetro_interior
    
    def is_lineas_divisorias(self):
        return self.lineas_divisorias
    
    def get_color_lineas_divisorias(self):        
        return self.color_lineas_divisorias
    
    def get_ancho_lineas_divisorias(self):
        return self.ancho_lineas_divisorias
    
    def get_variacion_radio(self):
        return self.variacion_radio
    
    def get_color_desactivado(self):
        return self.color_desactivado
    
    def get_operador(self):
        return self.operacion

'---------------TEST---------------'
app = wx.App()
frame = GraficoDibujo(None)
frame.Show()
app.MainLoop()