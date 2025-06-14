from ORM import Usuario, Empleado, Categoria, Producto, Carrito, CarritoDetalle, MetodoPago, Pedido, DetallePedido
from datetime import datetime

def agregar_datos(session):
    # Crear categorías
    cat1 = Categoria(nombre="Proteínas")
    cat2 = Categoria(nombre="Ropa Deportiva Mujer")
    cat3 = Categoria(nombre="Ropa Deportiva Hombre")
    cat4 = Categoria(nombre="Accesorios de Gym")
    cat5 = Categoria(nombre="Vitaminas")
    cat6 = Categoria(nombre="PreEntrenos")
    cat7 = Categoria(nombre="Creainas")

    session.add_all([cat1, cat2 ,cat3, cat4, cat5, cat6, cat7])
    session.commit()

    # Crear productos
    prod1 = Producto(nombre="Proteína Whey", descripcion="Proteína de suero 2lb", precio=120.50, stock=30, imagen_url="https://example.com/proteina.jpg", categoria=cat1)
    prod2 = Producto(nombre="Creatina Monohidratada", descripcion="Creatina pura 300g", precio=60.00, stock=50, imagen_url="https://example.com/creatina.jpg", categoria=cat7)
    prod3 = Producto(nombre="Camiseta Dry-Fit", descripcion="Camiseta deportiva", precio=25.00, stock=100, imagen_url="https://example.com/camiseta.jpg", categoria=cat3)
    prod4 = Producto(nombre="Short Deportivo", descripcion="Short cómodo para entrenamiento", precio=28.00, stock=30, imagen_url="https://example.com/short.jpg", categoria=cat3)
    prod5 = Producto(nombre="Pantalones Deportivos", descripcion="Pantalones deportivos", precio=25.00, stock=20, imagen_url="https://example.com/pantalones.jpg", categoria=cat3)
    prod6 = Producto(nombre="Guantes de entrenamiento", descripcion="Antideslizantes", precio=20.00, stock=50, imagen_url="https://example.com/guantes.jpg", categoria=cat4)
    prod7 = Producto(nombre="Cinturón de levantamiento", descripcion="Soporte lumbar", precio=45.00, stock=15, imagen_url="https://example.com/cinturon.jpg", categoria=cat4)
    prod8 = Producto(nombre="Botellón de Agua 2L", descripcion="Botella resistente", precio=15.00, stock=60, imagen_url="https://example.com/botellon.jpg", categoria=cat4)
    prod9 = Producto(nombre="Straps de entrenamiento", descripcion="Antideslizantes", precio=20.00, stock=50, imagen_url="https://example.com/straps.jpg", categoria=cat4)
    prod10 = Producto(nombre="Camiseta DryFit Hombre", descripcion="Camiseta deportiva negra", precio=35.00, stock=25, imagen_url="https://example.com/camiseta_hombre.jpg", categoria=cat3)
    prod11 = Producto(nombre="Short Deportivo Hombre", descripcion="Short cómodo para entrenamiento", precio=28.00, stock=30, imagen_url="https://example.com/short_hombre.jpg", categoria=cat3)
    prod12 = Producto(nombre="Pantalones Deportivos Hombre", descripcion="Pantalones deportivos", precio=25.00, stock=20, imagen_url="https://example.com/pantalones_hombre.jpg", categoria=cat3)
    prod13 = Producto(nombre="Top Deportivo Mujer", descripcion="Top ajustado con soporte", precio=30.00, stock=30, imagen_url="https://example.com/top_mujer.jpg", categoria=cat2)
    prod14 = Producto(nombre="Leggings Mujer", descripcion="Leggings de compresión", precio=40.00, stock=20, imagen_url="https://example.com/leggings.jpg", categoria=cat2)
    prod15 = Producto(nombre="Pantalones Deportivos Mujer", descripcion="Pantalones deportivos", precio=25.00, stock=20, imagen_url="https://example.com/pantalones_mujer.jpg", categoria=cat2)


    session.add_all([prod1, prod2, prod3, prod4, prod5, prod6, prod7, prod8, prod9, prod10, prod11, prod12, prod13, prod14, prod15])
    session.commit()

    # Crear métodos de pago
    mp1 = MetodoPago(tipo="Tarjeta")
    mp2 = MetodoPago(tipo="Efectivo")
    session.add_all([mp1, mp2])
    session.commit()

    # Crear usuarios
    user1 = Usuario(nombre="Mirko Coca", correo="cocaponcemirko335@gmail", contrasena="123456", direccion="Av. Central 123", telefono="70001234")
    user2 = Usuario(nombre="Carlos Pérez", correo="carlos@gmail.com", contrasena="123456", direccion="Av. Central 123", telefono="70001234")
    user3 = Usuario(nombre="Laura Gómez", correo="laura@gmail.com", contrasena="abcdef", direccion="Calle 12 #45", telefono="78945612", es_empleado=True)
    session.add_all([user1, user2, user3])
    session.commit()

    # Crear empleado asociado a user2
    empleado1 = Empleado(rol="admin", usuario=user1)
    empleado2 = Empleado(rol="admin", usuario=user2)
    session.add(empleado1, empleado2)
    session.commit()

    # Crear carritos
    carrito1 = Carrito(usuario=user1)
    session.add(carrito1)
    session.commit()

    # Agregar detalles al carrito
    detalle1 = CarritoDetalle(carrito=carrito1, producto=prod1, cantidad=2)
    detalle2 = CarritoDetalle(carrito=carrito1, producto=prod3, cantidad=1)
    session.add_all([detalle1, detalle2])
    session.commit()

    # Crear pedidos
    pedido1 = Pedido(usuario=user1, metodo_pago=mp1, total=166.00, estado="pendiente")
    session.add(pedido1)
    session.commit()

    # Agregar detalles al pedido
    detalle_pedido1 = DetallePedido(pedido=pedido1, producto=prod1, cantidad=2, precio_unitario=120.50)
    detalle_pedido2 = DetallePedido(pedido=pedido1, producto=prod3, cantidad=1, precio_unitario=25.00)
    session.add_all([detalle_pedido1, detalle_pedido2])
    session.commit()


    print("✅ Datos de prueba agregados correctamente.")

