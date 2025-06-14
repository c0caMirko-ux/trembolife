from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    direccion = Column(String(150))
    telefono = Column(String(20))
    es_empleado = Column(Boolean, default=False)

    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete-orphan")
    carrito = relationship("Carrito", uselist=False, back_populates="usuario", cascade="all, delete-orphan")
    empleado = relationship("Empleado", uselist=False, back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(nombre={self.nombre}, correo={self.correo})>"

class Empleado(Base):
    __tablename__ = 'empleado'
    idempleado = Column(Integer, primary_key=True)
    rol = Column(String(50))  # Ej: admin, vendedor

    id = Column(Integer, ForeignKey('usuario.id'), unique=True)
    usuario = relationship("Usuario", back_populates="empleado")

    def __repr__(self):
        return f"<Empleado(nombre={self.usuario.nombre}, rol={self.rol})>"

class Categoria(Base):
    __tablename__ = 'categoria'
    idcategoria = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)  # Evita duplicados

    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Categoria({self.nombre})>"

class Producto(Base):
    __tablename__ = 'producto'
    idproducto = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(300))
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    imagen_url = Column(String(200))

    idcategoria = Column(Integer, ForeignKey('categoria.idcategoria'))
    categoria = relationship("Categoria", back_populates="productos")

    detalles_carrito = relationship("CarritoDetalle", back_populates="producto", cascade="all, delete-orphan")
    detalles_pedido = relationship("DetallePedido", back_populates="producto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Producto({self.nombre}, ${self.precio})>"

class Carrito(Base):
    __tablename__ = 'carrito'
    idcarrito = Column(Integer, primary_key=True)

    id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", back_populates="carrito")

    detalles = relationship("CarritoDetalle", back_populates="carrito", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Carrito(usuario={self.usuario.nombre})>"

class CarritoDetalle(Base):
    __tablename__ = 'carrito_detalle'
    iddetalle = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)

    idcarrito = Column(Integer, ForeignKey('carrito.idcarrito'))
    carrito = relationship("Carrito", back_populates="detalles")

    idproducto = Column(Integer, ForeignKey('producto.idproducto'))
    producto = relationship("Producto", back_populates="detalles_carrito")

    def __repr__(self):
        return f"<CarritoDetalle(producto={self.producto.nombre}, cantidad={self.cantidad})>"

class MetodoPago(Base):
    __tablename__ = 'metodo_pago'
    idmetodo = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)  # Ej: "Tarjeta", "Efectivo"

    pedidos = relationship("Pedido", back_populates="metodo_pago")

    def __repr__(self):
        return f"<MetodoPago({self.tipo})>"

class Pedido(Base):
    __tablename__ = 'pedido'
    idpedido = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    estado = Column(String(50), default="pendiente")  # Ej: pendiente, enviado, completado

    id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", back_populates="pedidos")

    idmetodo = Column(Integer, ForeignKey('metodo_pago.idmetodo'))
    metodo_pago = relationship("MetodoPago", back_populates="pedidos")

    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pedido(id={self.idpedido}, usuario={self.usuario.nombre}, total={self.total})>"

class DetallePedido(Base):
    __tablename__ = 'detalle_pedido'
    iddetalle = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    idpedido = Column(Integer, ForeignKey('pedido.idpedido'))
    pedido = relationship("Pedido", back_populates="detalles")

    idproducto = Column(Integer, ForeignKey('producto.idproducto'))
    producto = relationship("Producto", back_populates="detalles_pedido")

    def __repr__(self):
        return f"<DetallePedido(producto={self.producto.nombre}, cantidad={self.cantidad})>"
