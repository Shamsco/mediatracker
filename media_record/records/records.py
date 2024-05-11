from flask import Blueprint, flash, render_template, request, url_for, redirect, session, g
from media_record.db_manager import get_user, get_user_by_id, db_session
from media_record.auth.auth import login_required
from media_record.models import Record
blp = Blueprint('records', __name__)

@blp.before_request
@login_required
def before_request():
    pass

@blp.get('/')
def index():
    records = g.user.records
    return render_template('records.html', records=records)

@blp.get('/create')
def create_get():
    return render_template('create.html')

@blp.post('/create')
def create_post():
    name = request.form['name']
    media_type = request.form['media_type']
    current_episode_non_season = request.form['current_episode_non_season']
    full_episode_non_season = request.form['full_episode_non_season']
    error = None
    if not name or not media_type or not current_episode_non_season or not full_episode_non_season:
        error = 'Missing data'
    
    if error is None:
        try:
            g.user.records.append(Record(name, media_type, current_episode_non_season, full_episode_non_season))
            db_session.add(g.user)
            db_session.commit()
        except Exception as e:
            error = "Something is wrong: " + str(e)
        else:
            return redirect(url_for('records.index'))
    
    flash(error)
    return redirect(url_for('records.create_get'))

@blp.get('/update/<int:id>')
def update_get(id):
    if not session['user_id']:
        return 404
    record = db_session.query(Record).filter(Record.record_id == id).first()
    

    if record:
        if record.user_id != session['user_id']:
            return 'Not Allowed', 403
        else:
            return render_template('update.html', record=record)
    else:
        return 'Not Found', 404

@blp.post('/update/<int:id>')
def update_post(id):
    name = request.form['name']
    media_type = request.form['media_type']
    current_episode_non_season = request.form['current_episode_non_season']
    full_episode_non_season = request.form['full_episode_non_season']
    error = None
    if not name or not media_type or not current_episode_non_season or not full_episode_non_season:
        error = 'Missing data'
    
    if error is None:
        try:
            record = db_session.query(Record).filter(Record.record_id == id, Record.user_id == session['user_id']).first()
            if record:
                record.name = name
                record.media_type = media_type
                record.current_episode_non_season = current_episode_non_season
                record.full_episode_non_season = full_episode_non_season
                db_session.add(record)
                db_session.commit()
        except Exception as e:
            error = "Something is wrong: " + str(e)
        else:
            return redirect(url_for('records.index'))
    
    flash(error)
    return redirect(url_for('records.update_get', id=id))

@blp.post('/delete/<int:id>')
def delete_post(id):
    record =  db_session.query(Record).filter(Record.record_id == id, Record.user_id == session['user_id']).first()
    error = None
    try:
        db_session.delete(record)
        db_session.commit()
    except Exception as e:
        error = "Something is wrong:" + str(e)
    else:
        return redirect(url_for('records.index'))
    
    flash(error)
    return redirect(url_for('records.update_get', id=id))