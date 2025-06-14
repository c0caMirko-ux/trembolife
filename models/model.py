from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

# ------------------ Usuario ------------------
class Usuario(Base, UserMixin):
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

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

# ------------------ Empleado ------------------
class Empleado(Base):
    __tablename__ = 'empleado'
    idempleado = Column(Integer, primary_key=True)
    rol = Column(String(50))
    id = Column(Integer, ForeignKey('usuario.id'), unique=True)

    usuario = relationship("Usuario", back_populates="empleado")

# ------------------ Categoría ------------------
class Categoria(Base):
    __tablename__ = 'categoria'
    idcategoria = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)

    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")

# ------------------ Producto ------------------
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

# ------------------ Carrito ------------------
class Carrito(Base):
    __tablename__ = 'carrito'
    idcarrito = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship("Usuario", back_populates="carrito")
    detalles = relationship("CarritoDetalle", back_populates="carrito", cascade="all, delete-orphan")

# ------------------ Detalle Carrito ------------------
class CarritoDetalle(Base):
    __tablename__ = 'carrito_detalle'
    iddetalle = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    idcarrito = Column(Integer, ForeignKey('carrito.idcarrito'))
    idproducto = Column(Integer, ForeignKey('producto.idproducto'))

    carrito = relationship("Carrito", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_carrito")

# ------------------ Método de Pago ------------------
class MetodoPago(Base):
    __tablename__ = 'metodo_pago'
    idmetodo = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)

    pedidos = relationship("Pedido", back_populates="metodo_pago")

# ------------------ Pedido ------------------
class Pedido(Base):
    __tablename__ = 'pedido'
    idpedido = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    estado = Column(String(50), default="pendiente")
    id = Column(Integer, ForeignKey('usuario.id'))
    idmetodo = Column(Integer, ForeignKey('metodo_pago.idmetodo'))

    usuario = relationship("Usuario", back_populates="pedidos")
    metodo_pago = relationship("MetodoPago", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")

# ------------------ Detalle Pedido ------------------
class DetallePedido(Base):
    __tablename__ = 'detalle_pedido'
    iddetalle = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    idpedido = Column(Integer, ForeignKey('pedido.idpedido'))
    idproducto = Column(Integer, ForeignKey('producto.idproducto'))

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_pedido")
