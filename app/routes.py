from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash)
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from .models import Usuario, Activo, Amenaza, Riesgo, Salvaguarda
from .risk import resumen_riesgos

main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(
            username=request.form['username']).first()
        if user and check_password_hash(user.password,
                                        request.form['password']):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/')
@login_required
def dashboard():
    activos  = Activo.query.all()
    riesgos  = Riesgo.query.all()
    resumen  = resumen_riesgos(riesgos)
    return render_template('dashboard.html',
                           activos=activos,
                           riesgos=riesgos,
                           resumen=resumen)


@main.route('/activos')
@login_required
def lista_activos():
    activos = Activo.query.all()
    return render_template('activos.html', activos=activos)


@main.route('/activos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_activo():
    if request.method == 'POST':
        activo = Activo(
            nombre           = request.form['nombre'],
            categoria        = request.form['categoria'],
            disponibilidad   = int(request.form['disponibilidad']),
            confidencialidad = int(request.form['confidencialidad']),
            integridad       = int(request.form['integridad']),
            autenticidad     = int(request.form['autenticidad']),
            trazabilidad     = int(request.form['trazabilidad']),
            descripcion      = request.form.get('descripcion', '')
        )
        db.session.add(activo)
        db.session.commit()
        flash('Activo registrado correctamente.', 'success')
        return redirect(url_for('main.lista_activos'))
    return render_template('nuevo_activo.html')


@main.route('/riesgos')
@login_required
def lista_riesgos():
    riesgos  = Riesgo.query.all()
    activos  = Activo.query.all()
    amenazas = Amenaza.query.all()
    return render_template('riesgos.html',
                           riesgos=riesgos,
                           activos=activos,
                           amenazas=amenazas)


@main.route('/riesgos/calcular', methods=['POST'])
@login_required
def calcular_riesgo():
    riesgo = Riesgo(
        activo_id  = int(request.form['activo_id']),
        amenaza_id = int(request.form['amenaza_id']),
        impacto    = int(request.form['impacto'])
    )
    db.session.add(riesgo)
    db.session.commit()
    flash(f'Riesgo calculado: {riesgo.nivel_riesgo} '
          f'(inherente: {riesgo.riesgo_inherente} | '
          f'residual: {riesgo.riesgo_residual})', 'info')
    return redirect(url_for('main.lista_riesgos'))


@main.route('/salvaguardas/nueva', methods=['POST'])
@login_required
def nueva_salvaguarda():
    salvaguarda = Salvaguarda(
        nombre      = request.form['nombre'],
        tipo        = request.form['tipo'],
        eficacia    = int(request.form['eficacia']),
        activo_id   = int(request.form['activo_id']),
        descripcion = request.form.get('descripcion', '')
    )
    db.session.add(salvaguarda)
    db.session.commit()
    flash('Salvaguarda registrada correctamente.', 'success')
    return redirect(url_for('main.lista_activos'))
