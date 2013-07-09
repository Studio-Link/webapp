from flask import Blueprint, render_template, redirect, request, url_for, flash

from app import db
from app.models.peers import Peer
from app.forms.peers import AddForm, CallForm
from app import tasks
from sqlalchemy.exc import IntegrityError

mod = Blueprint('peers', __name__, url_prefix='/peers')

@mod.route('/')
def index():
    peers = Peer.query.all()
    return render_template("peers/index.html", peers=peers)

@mod.route('/add/', methods=('GET', 'POST'))
def add():
    form = AddForm(request.form)
    if form.validate_on_submit():
        peer = Peer(name=form.name.data, host=form.host.data)
        db.session.add(peer)
        try:
            db.session.commit()
            #TODO: 
            #flash(tasks.add.delay(2,2).id)
            return redirect(url_for('peers.index'))
        except IntegrityError:
            flash(u'IPv6 address already exist', 'error')
    return render_template("peers/add.html", form=form)

@mod.route('/delete/<id>')
def delete(id):
    db.session.delete(Peer.query.get(id))
    db.session.commit()
    return redirect(url_for('peers.index'))

@mod.route('/call/')
def call():
    form = CallForm()
    return render_template("peers/call.html", form=form)
