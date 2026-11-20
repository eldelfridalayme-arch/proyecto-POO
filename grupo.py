class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    def calcular_precio(self):
        pass
    def esta_disponible(self):
        pass
class Plato(Producto):
    def __init__(self, nombre, precio, dias_disponibles):
        super().__init__(nombre, precio)
        self.dias_disponibles = dias_disponibles
    def calcular_precio(self):
        return self.precio
    def esta_disponible(self):
        return True
class Bebida(Producto):
    def __init__(self, nombre, precio,tipo, tamaño):
        super().__init__(nombre, precio)
        
