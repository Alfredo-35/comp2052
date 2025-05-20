from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import ItemForm, ChangePasswordForm
from app.models import db, User, Item

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')
            return render_template('cambiar_password.html', form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role and current_user.role.name == 'Student':
        items = Item.query.all()
    else:
        items = Item.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', items=items)

@main.route('/items', methods=['GET', 'POST'])
@login_required
def items():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            cantidad=form.cantidad.data,
            precio_estimado=form.precio_estimado.data,
            ubicacion=form.ubicacion.data,
            fecha_adquisicion=form.fecha_adquisicion.data,
            owner_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash("Item created successfully.")
        return redirect(url_for('main.dashboard'))
    return render_template('item_form.html', form=form)

@main.route('/items/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_item(id):
    item = Item.query.get_or_404(id)
    if not current_user.role or (current_user.role.name != 'Admin' and item.owner_id != current_user.id):
        flash('You do not have permission to edit this item.')
        return redirect(url_for('main.dashboard'))

    form = ItemForm(obj=item)
    form.id.data = item.id  # Establecer el ID en el formulario

    if form.validate_on_submit():
        item.nombre = form.nombre.data
        item.categoria = form.categoria.data
        item.cantidad = form.cantidad.data
        item.precio_estimado = form.precio_estimado.data
        item.ubicacion = form.ubicacion.data
        item.fecha_adquisicion = form.fecha_adquisicion.data
        db.session.commit()
        flash("Item updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('item_form.html', form=form)

@main.route('/items/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_item(id):
    item = Item.query.get_or_404(id)
    if not current_user.role or (current_user.role.name != 'Admin' and item.owner_id != current_user.id):
        flash('You do not have permission to delete this item.')
        return redirect(url_for('main.dashboard'))
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if not current_user.role or current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))
    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)
