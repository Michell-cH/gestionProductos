from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto a una clave secreta más segura

@app.route('/')
def index():
    # Asegurarse de que la sesión tenga un diccionario de productos
    if 'productos' not in session:
        session['productos'] = []

    return render_template('index.html', productos=session['productos'])

@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        id_producto = request.form['id']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        # Comprobar si el ID es único
        if any(prod['id'] == id_producto for prod in session['productos']):
            flash("El ID ya existe. Por favor, elige otro.", "error")
            return redirect(url_for('nuevo_producto'))

        # Crear el nuevo producto
        nuevo_prod = {
            'id': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        # Agregar el producto a la sesión
        session['productos'].append(nuevo_prod)
        session.modified = True  # Marcar la sesión como modificada

        return redirect(url_for('index'))

    return render_template('nuevo_producto.html')

@app.route('/editar_producto/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = next((prod for prod in session['productos'] if prod['id'] == id), None)

    if request.method == 'POST':
        # Actualizar los datos del producto
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']

        session.modified = True
        return redirect(url_for('index'))

    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<id>')
def eliminar_producto(id):
    session['productos'] = [prod for prod in session['productos'] if prod['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
