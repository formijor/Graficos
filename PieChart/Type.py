'''
Created on 24 mar. 2022

@author: jor_l
'''

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