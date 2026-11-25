from abc import ABC, abstractmethod
from datetime import datetime
from DetallePedido import DetallePedido
from variante import DIAS

REGISTRADO = "REGISTRADO"
EN_PREPARACION = "EN_PREPARACION"
LISTO = "LISTO"
ENTREGADO = "ENTREGADO"
CANCELADO = "CANCELADO"

# a que estados se puede pasar desde cada estado
TRANSICIONES = {
    REGISTRADO: [EN_PREPARACION, CANCELADO],
    EN_PREPARACION: [LISTO],
    LISTO: [ENTREGADO],
    ENTREGADO: [],
    CANCELADO: [],
}


class Pedido(ABC):
    def __init__(self, cliente, tipo, fecha=None):
        if cliente is None:
            raise ValueError("El pedido necesita un cliente")
        if fecha is None:
            fecha = datetime.now()
        self._cliente = cliente
        self._tipo = tipo
        self._estado = REGISTRADO
        self._fecha = fecha
        self._total = 0
        self._detalles = []         # relacion con DetallePedido
        self._metodo_pago = None    # relacion con MetodoPago

    @property
    def cliente(self):
        return self._cliente

    @property
    def tipo(self):
        return self._tipo

    @property
    def estado(self):
        return self._estado

    @property
    def fecha(self):
        return self._fecha

    @property
    def total(self):
        return self.calcular_total()

    @property
    def detalles(self):
        return list(self._detalles)       # copia: desde fuera no se puede modificar

    @property
    def metodo_pago(self):
        return self._metodo_pago

    def agregar_producto(self, producto, cantidad=1):
        if self._estado != REGISTRADO:
            raise ValueError("Solo se agregan productos en estado REGISTRADO")
        if self._metodo_pago is not None:
            raise ValueError("El pedido ya esta pagado")
        dia = DIAS[self._fecha.weekday()]
        if not producto.esta_disponible(dia):
            raise ValueError(producto.nombre + " no esta disponible el " + dia)
        # si el producto ya estaba, se suma la cantidad
        for i in range(len(self._detalles)):
            if self._detalles[i].producto is producto:
                cantidad = cantidad + self._detalles[i].cantidad
                self._detalles[i] = DetallePedido(self, producto, cantidad)
                return
        self._detalles.append(DetallePedido(self, producto, cantidad))

    def quitar_producto(self, producto):
        if self._estado != REGISTRADO:
            raise ValueError("Solo se quitan productos en estado REGISTRADO")
        if self._metodo_pago is not None:
            raise ValueError("El pedido ya esta pagado")
        for i in range(len(self._detalles)):
            if self._detalles[i].producto is producto:
                del self._detalles[i]
                return
        raise ValueError("El producto no esta en el pedido")

    # agregado: suma de los detalles, sin cargos
    def calcular_subtotal(self):
        total = 0
        for d in self._detalles:
            total += d.subtotal
        return round(total, 2)

    # agregado por el documento: cada tipo de pedido calcula sus cargos distinto
    @abstractmethod
    def calcular_cargos(self):
        pass

    def calcular_total(self):
        self._total = round(self.calcular_subtotal() + self.calcular_cargos(), 2)
        return self._total

    def cambiar_estado(self, nuevo):
        if nuevo not in TRANSICIONES[self._estado]:
            raise ValueError("No se puede pasar de " + self._estado + " a " + nuevo)
        if nuevo == EN_PREPARACION and len(self._detalles) == 0:
            raise ValueError("El pedido no tiene productos")
        self._estado = nuevo

    # agregado: cobra el pedido con el metodo de pago elegido
    def pagar(self, metodo):
        if self._estado == CANCELADO:
            raise ValueError("No se puede cobrar un pedido cancelado")
        if self._metodo_pago is not None:
            raise ValueError("El pedido ya esta pagado")
        if len(self._detalles) == 0:
            raise ValueError("El pedido no tiene productos")
        metodo.procesar_pago(self.calcular_total())
        self._metodo_pago = metodo

    # agregado: muestra el detalle (subtotal, descuentos, cargos y total)
    def mostrar_detalle(self):
        descuentos = 0
        for d in self._detalles:
            descuentos += d.producto.calcular_descuento() * d.cantidad
        print("Pedido", self._tipo, "-", self._estado)
        print("Cliente:", self._cliente.nombre, "-", self._cliente.telefono)
        print("Fecha:", self._fecha.strftime("%d/%m/%Y %H:%M"))
        print("-" * 40)
        for d in self._detalles:
            print(f"{d.cantidad} x {d.producto.nombre}  Bs {d.precio:.2f} = Bs {d.subtotal:.2f}")
        print("-" * 40)
        print(f"Subtotal sin descuentos: Bs {self.calcular_subtotal() + descuentos:.2f}")
        print(f"Descuentos: Bs {descuentos:.2f}")
        print(f"Subtotal: Bs {self.calcular_subtotal():.2f}")
        print(f"Cargos (envases o envio): Bs {self.calcular_cargos():.2f}")
        print(f"TOTAL: Bs {self.calcular_total():.2f}")
