from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import sessionmaker
from models.Base import engine
from models.model import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os

# Inicializar Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_fallback")

# Crear sesión SQLAlchemy
Session = sessionmaker(bind=engine)
db_session = Session()

# Configurar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))


# ======================
# Rutas públicas
# ======================

@app.route('/')
def home():
    return redirect(url_for('auth'))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form['action']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if action == 'register':
            if db_session.query(Usuario).filter_by(correo=correo).first():
                flash('El correo ya está registrado', 'danger')
            else:
                nuevo_usuario = Usuario(
                    nombre=request.form['nombre'],
                    correo=correo
                )
                nuevo_usuario.set_password(contrasena)
                db_session.add(nuevo_usuario)
                db_session.commit()
                flash('Registro exitoso. Inicia sesión.', 'success')
                return redirect(url_for('auth'))

        elif action == 'login':
            user = db_session.query(Usuario).filter_by(correo=correo).first()
            if user and user.check_password(contrasena):
                login_user(user)
                flash('Sesión iniciada correctamente', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Correo o contraseña incorrectos', 'danger')
                return redirect(url_for('auth'))

    return render_template('auth.html')


# ======================
# Dashboard
# ======================

@app.route('/dashboard')
@login_required
def dashboard():
    carrito = session.get('carrito', [])
    return render_template('dashboard.html', usuario=current_user, carrito_len=len(carrito))


# ======================
# Rutas para categorías
# ======================

@app.route('/ropa_hombre')
@login_required
def ropa_hombre():
    return render_template('ropa_hombre.html')

@app.route('/ropa_mujer')
@login_required
def ropa_mujer():
    return render_template('ropa_mujer.html')

@app.route('/suplementos')
@login_required
def suplementos():
    return render_template('suplementos.html')

@app.route('/accesorios')
@login_required
def accesorios():
    return render_template('accesorios.html')

@app.route('/carrito')
@login_required
def carrito():
    return render_template('carrito.html')


# ======================
# Logout
# ======================

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth'))


# ======================
# API futuras (ejemplo)
# ======================

@app.route('/api/productos')
def api_productos():
    return jsonify({"mensaje": "Aquí irá la lista de productos"})

# ======================
# API para carrito usando BD
# ======================

@app.route('/api/agregar_carrito', methods=['POST'])
@login_required
def api_agregar_carrito():
    data = request.get_json()
    idproducto = data.get('idproducto')
    cantidad = data.get('cantidad', 1)

    if not idproducto:
        return jsonify({"error": "Falta idproducto"}), 400

    producto = db_session.query(Producto).filter_by(idproducto=idproducto).first()  # Obtener producto
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    carrito = db_session.query(Carrito).filter_by(id=current_user.id).first()
    if not carrito:
        carrito = Carrito(id=current_user.id)
        db_session.add(carrito)
        db_session.commit()

    detalle = db_session.query(CarritoDetalle).filter_by(idcarrito=carrito.idcarrito, idproducto=idproducto).first()
    if detalle:
        detalle.cantidad += cantidad
    else:
        detalle = CarritoDetalle(idcarrito=carrito.idcarrito, idproducto=idproducto, cantidad=cantidad)
        db_session.add(detalle)

    db_session.commit()
    return jsonify({"mensaje": f'Producto "{producto.nombre}" agregado al carrito'})

@app.route('/api/obtener_carrito')
@login_required
def api_obtener_carrito():
    carrito = db_session.query(Carrito).options(joinedload(Carrito.detalles).joinedload(CarritoDetalle.producto)).filter_by(id=current_user.id).first()
    if not carrito or not carrito.detalles:
        return jsonify([])

    items = []
    for detalle in carrito.detalles:
        items.append({
            "idproducto": detalle.producto.idproducto,
            "nombre": detalle.producto.nombre,
            "precio": detalle.producto.precio,
            "cantidad": detalle.cantidad,
            "imagen_url": detalle.producto.imagen_url
        })
    return jsonify(items)

@app.route('/api/eliminar_carrito', methods=['POST'])
@login_required
def api_eliminar_carrito():
    data = request.get_json()
    idproducto = data.get('idproducto')

    if not idproducto:
        return jsonify({"error": "Falta idproducto"}), 400

    carrito = db_session.query(Carrito).filter_by(id=current_user.id).first()
    if not carrito:
        return jsonify({"error": "Carrito vacío"}), 400

    detalle = db_session.query(CarritoDetalle).filter_by(idcarrito=carrito.idcarrito, idproducto=idproducto).first()
    if detalle:
        db_session.delete(detalle)
        db_session.commit()
        return jsonify({"mensaje": "Producto eliminado del carrito"})
    else:
        return jsonify({"error": "Producto no encontrado en carrito"}), 404

@app.route('/api/finalizar_compra', methods=['POST'])
@login_required
def api_finalizar_compra():
    carrito = db_session.query(Carrito).options(joinedload(Carrito.detalles).joinedload(CarritoDetalle.producto)).filter_by(id=current_user.id).first()

    if not carrito or not carrito.detalles:
        return jsonify({"error": "Carrito vacío"}), 400

    total = sum(detalle.producto.precio * detalle.cantidad for detalle in carrito.detalles)

    nuevo_pedido = Pedido(
        id=current_user.id,
        total=total,
        estado='pendiente',
        fecha=datetime.utcnow(),
        idmetodo=None  # Aquí puedes manejar método de pago en otra implementación
    )
    db_session.add(nuevo_pedido)
    db_session.commit()  # Para obtener nuevo_pedido.idpedido

    for detalle_carrito in carrito.detalles:
        detalle_pedido = DetallePedido(
            idpedido=nuevo_pedido.idpedido,
            idproducto=detalle_carrito.idproducto,
            cantidad=detalle_carrito.cantidad,
            precio_unitario=detalle_carrito.producto.precio
        )
        db_session.add(detalle_pedido)

    # Vaciar carrito
    for detalle_carrito in carrito.detalles:
        db_session.delete(detalle_carrito)

    db_session.commit()
    return jsonify({"mensaje": "Compra finalizada correctamente", "idpedido": nuevo_pedido.idpedido})


# ======================
# Ejecutar app
# ======================

if __name__ == '__main__':
    app.run(debug=True)
