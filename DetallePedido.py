from variante import CANTIDAD_MIN, CANTIDAD_MAX


class DetallePedido:
    def __init__(self, pedido, producto, cantidad):
        if cantidad < CANTIDAD_MIN or cantidad > CANTIDAD_MAX:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        self._pedido = pedido
        self._producto = producto
        self._cantidad = cantidad
        self._precio = producto.calcular_precio()     # precio del momento
        self._subtotal = self.calcular_subtotal()

    @property
    def pedido(self):
        return self._pedido

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio(self):
        return self._precio

    @property
    def subtotal(self):
        return self._subtotal

    def calcular_subtotal(self):
        return round(self._precio * self._cantidad, 2)
