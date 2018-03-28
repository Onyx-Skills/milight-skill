# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.extensions import db
from milight_skill.index import mi_light
from flask.ext.login import login_required
from flask import render_template , redirect , request , url_for , flash
from onyxbabel import gettext
from onyx.api.exceptions import *
from milight_skill.api import *
from onyx.api.assets import Json

json = Json()
devices = Light()

@mi_light.route('/' , methods=['GET','POST'])
@login_required
def index():
    json.json = devices.get()
    return render_template('index.html', devices=json.decode())

@mi_light.route('/add', methods=['POST'])
@login_required
def add_device():
    try:
        devices.name = request.form['name']
        devices.identifier = request.form['identifier']
        devices.color = request.form['color']
        try:
            devices.protocol = int(request.form['protocol'])
        except ValueError:
            flash(gettext('Protocol is not a number !'), 'error')
            return redirect(url_for('mi_light.index'))
        devices.room = request.form['room']
        devices.add()
        flash(gettext('Devices Add'), 'success')
        return redirect(url_for('mi_light.index'))
    except DevicesException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('mi_light.index'))


@mi_light.route('/delete/<int:id>')
@login_required
def delete_device(id):
    try:
        devices.id = id
        devices.delete()
        flash(gettext('Devices Deleted'), 'success')
        return redirect(url_for('mi_light.index'))
    except DevicesException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('mi_light.index'))

@mi_light.route('/change_state', methods=['POST'])
@login_required
def change_state():
    try:
        devices.id = request.form['id']
        devices.state = str(request.form['state'])

        return devices.change_state()
    except DevicesException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('mi_light.index'))

@mi_light.route('/change_color', methods=['POST'])
@login_required
def change_color():
    try:
        devices.id = request.form['id']
        devices.color = request.form['color_'+request.form['id']]
        devices.change_color()

        flash(gettext('Devices Modified'), 'success')
        return redirect(url_for('mi_light.index'))
    except DevicesException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('mi_light.index'))

@mi_light.route('/widget')
@login_required
def widget():
    json.json = devices.get()
    return render_template('widget.html', devices=json.decode())

@mi_light.route('/get')
@login_required
def get_lamp():
    return devices.get()

@mi_light.route('/open')
def action_open(kwargs):

    devices.id = kwargs[0]
    devices.state = "true"

    devices.change_state()
    return json.encode({"status":"success", "label":"open_lamp"})

@mi_light.route('/close')
def action_close(kwargs):

    devices.id = kwargs[0]
    devices.state = "false"

    devices.change_state()
    return json.encode({"status":"success", "label":"close_lamp"})
