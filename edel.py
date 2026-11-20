class Cliente:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion 
    def validar_datos(self):
        if self.nombre != "" and self.telefono != "":
            return True 
        else:
            return False 
class DetallePedido:
    def __init__(self, pedido, producto, cantidad):
        self.pedido = pedido
        self.producto = producto
        self.cantidad = cantidad 
        self.precio = producto.calcular_precio()
        self.subtotal = self.precio * cantidad 
    def calcular_subtotal(self):
        

