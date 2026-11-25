from Pedido import Pedido
from variante import ENVASE_POR_PLATO


class PedidoParaLlevar(Pedido):
    def __init__(self, cliente, fecha=None):
        super().__init__(cliente, "Para llevar", fecha)
        self._envases = 0

    @property
    def envases(self):
        return self._envases

    # un envase por cada plato (tambien los que van dentro de un combo)
    def calcular_cargos(self):
        platos = 0
        for d in self._detalles:
            platos += d.producto.contar_platos() * d.cantidad
        self._envases = platos
        return round(platos * ENVASE_POR_PLATO, 2)
