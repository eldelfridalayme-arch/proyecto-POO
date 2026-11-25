from datetime import datetime
from Pedido import Pedido, EN_PREPARACION, ENTREGADO
from variante import (ENVIO_GRATIS_DESDE, ENVIO_GRATIS_SOLO_CERCADO,
                      PEDIDO_MINIMO_DELIVERY, ZONAS_ENVIO, MINUTOS_RETRASO)


class PedidoDelivery(Pedido):
    def __init__(self, cliente, zona, fecha=None):
        super().__init__(cliente, "Delivery", fecha)
        self.zona = zona
        self._retraso = False

    @property
    def zona(self):
        return self._zona

    @zona.setter
    def zona(self, valor):
        if valor not in ZONAS_ENVIO:
            raise ValueError("Zona de delivery no valida")
        self._zona = valor

    @property
    def retraso(self):
        return self._retraso

    def calcular_cargos(self):
        envio = ZONAS_ENVIO[self._zona]
        if ENVIO_GRATIS_DESDE is not None and self.calcular_subtotal() >= ENVIO_GRATIS_DESDE:
            if self._zona == "Cercado" or not ENVIO_GRATIS_SOLO_CERCADO:
                envio = 0
        return envio

    # se agregan dos reglas del delivery al cambio de estado
    def cambiar_estado(self, nuevo):
        if nuevo == EN_PREPARACION and self.calcular_subtotal() < PEDIDO_MINIMO_DELIVERY:
            raise ValueError(f"El pedido minimo para delivery es Bs {PEDIDO_MINIMO_DELIVERY}")
        super().cambiar_estado(nuevo)
        # PENDIENTE: la regla 9 (retraso) se completa cuando el docente responda
        if nuevo == ENTREGADO and MINUTOS_RETRASO is not None:
            minutos = (datetime.now() - self._fecha).total_seconds() / 60
            self._retraso = minutos > MINUTOS_RETRASO

    # el delivery solo acepta efectivo o QR
    def pagar(self, metodo):
        if metodo.tipo == "Tarjeta":
            raise ValueError("El delivery solo acepta efectivo o QR")
        super().pagar(metodo)
