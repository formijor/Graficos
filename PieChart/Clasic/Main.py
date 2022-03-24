'''
Created on 24 mar. 2022

@author: jor_l
'''

import wx
import math
import random
import operator
from Type import TipoGrafico
from Segments.Portion import Porcion

class ClassicPie():
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
        self.lista_porciones = [] #Hay que cambiarlo por un metodo de actualizacion
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