'''
Created on 24 mar. 2022

@author: jor_l
'''


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