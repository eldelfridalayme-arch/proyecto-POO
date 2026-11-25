from Pedido import Pedido
from variante import MESA_MIN, MESA_MAX


class PedidoLocal(Pedido):
    def __init__(self, cliente, mesa, fecha=None):
        super().__init__(cliente, "Local", fecha)
        self.mesa = mesa

    @property
    def mesa(self):
        return self._mesa

    @mesa.setter
    def mesa(self, valor):
        if valor < MESA_MIN or valor > MESA_MAX:
            raise ValueError("La mesa debe ser del 1 al 15")
        self._mesa = valor

    def calcular_cargos(self):
        return 0       # el pedido local no tiene cargos
