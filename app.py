import os
import base64
from datetime import datetime
from bson.objectid import ObjectId
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, abort
)
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import config

app = Flask(__name__)
app.config['MONGO_URI'] = config.MONGO_URI
app.config['SECRET_KEY'] = config.SECRET_KEY

mongo = PyMongo(app)

# --- Auth setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, uid, username, role):
        self.id = uid
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    return User(str(u['_id']), u['username'], u.get('role', 'user'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def role_required(role):
    def decorator(f):
        from functools import wraps

        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


# --- Public routes (register/login simplified) ---
@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role == 'user':
        return redirect(url_for('report'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Username and password required', 'danger')
            return redirect(request.url)
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists', 'danger')
            return redirect(request.url)
        user = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'role': 'user'
        }
        mongo.db.users.insert_one(user)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = mongo.db.users.find_one({'username': username})
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid credentials', 'danger')
            return redirect(request.url)
        user_obj = User(str(user['_id']),
                        user['username'], user.get('role', 'user'))
        login_user(user_obj)
        flash('Logged in successfully', 'success')
        if user_obj.role == 'pwd':
            return redirect(url_for('pwd_dashboard'))
        return redirect(url_for('my_reports'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('login'))


# --- User submit report ---
@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if current_user.role != 'user':
        flash('Only registered users can submit reports', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        image = request.files.get('image')
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')
        description = request.form.get('description', '').strip()

        if not image or image.filename == '' or not allowed_file(image.filename):
            flash('Please upload a valid image', 'danger')
            return redirect(request.url)
        if not lat or not lon:
            flash('Location required', 'danger')
            return redirect(request.url)

        # Convert image to Base64
        image_data = base64.b64encode(image.read()).decode('utf-8')
        mime_type = f"image/{image.filename.rsplit('.', 1)[1].lower()}"

        doc = {
            'image_data': image_data,
            'image_mime': mime_type,
            'image_filename': secure_filename(image.filename),
            'latitude': float(lat),
            'longitude': float(lon),
            'description': description,
            'timestamp': datetime.utcnow(),
            'status': 'Pending',
            'reported_by': ObjectId(current_user.id),
            'comments': []
        }
        res = mongo.db.potholes.insert_one(doc)
        return redirect(url_for('thank_you', report_id=str(res.inserted_id)))

    return render_template('report_user.html')


@app.route('/thank-you')
@login_required
def thank_you():
    rid = request.args.get('report_id')
    return render_template('thank_you.html', report_id=rid)


@app.route('/my-reports')
@login_required
def my_reports():
    if current_user.role != 'user':
        flash('Only normal users can view this page', 'danger')
        return redirect(url_for('index'))
    docs = list(mongo.db.potholes.find(
        {'reported_by': ObjectId(current_user.id)}).sort('timestamp', -1))
    for d in docs:
        d['_id'] = str(d['_id'])
        d['timestamp'] = d['timestamp'].isoformat()
        d['image_url'] = f"data:{d['image_mime']};base64,{d['image_data']}"
    return render_template('my_reports.html', reports=docs)


# --- PWD dashboard ---
@app.route('/pwd/dashboard')
@login_required
@role_required('pwd')
def pwd_dashboard():
    docs = list(mongo.db.potholes.find().sort('timestamp', -1))
    for d in docs:
        d['_id'] = str(d['_id'])
        d['timestamp'] = d['timestamp'].isoformat()
        d['image_url'] = f"data:{d['image_mime']};base64,{d['image_data']}"
        if isinstance(d.get('reported_by'), ObjectId):
            d['reported_by'] = str(d['reported_by'])
        if d.get('reported_by'):
            u = mongo.db.users.find_one({'_id': ObjectId(d['reported_by'])})
            d['reported_by_username'] = u['username'] if u else None
    return render_template('pwd_dashboard.html', reports=docs)


@app.route('/api/reports')
@login_required
@role_required('pwd')
def api_reports():
    status = request.args.get('status')
    q = {}
    if status:
        q['status'] = status
    docs = list(mongo.db.potholes.find(q).sort('timestamp', -1))
    for d in docs:
        d['_id'] = str(d['_id'])
        d['timestamp'] = d['timestamp'].isoformat()
        d['image_url'] = f"data:{d['image_mime']};base64,{d['image_data']}"
        if isinstance(d.get('reported_by'), ObjectId):
            d['reported_by'] = str(d['reported_by'])
        if d.get('reported_by'):
            u = mongo.db.users.find_one({'_id': ObjectId(d['reported_by'])})
            d['reported_by_username'] = u['username'] if u else None
    return jsonify(docs)


@app.route('/pwd/update_status', methods=['POST'])
@login_required
@role_required('pwd')
def update_status():
    data = request.get_json()
    report_id = data.get('report_id')
    new_status = data.get('status')
    comment = data.get('comment', '').strip()

    if new_status not in ('Pending', 'In Progress', 'Resolved'):
        return jsonify({'ok': False, 'error': 'invalid status'}), 400
    try:
        oid = ObjectId(report_id)
    except:
        return jsonify({'ok': False, 'error': 'bad id'}), 400

    update = {'$set': {'status': new_status}}
    if comment:
        update['$push'] = {'comments': {
            'text': comment, 'when': datetime.utcnow()}}
    res = mongo.db.potholes.update_one({'_id': oid}, update)
    if res.matched_count == 0:
        return jsonify({'ok': False, 'error': 'not found'}), 404
    return jsonify({'ok': True})


@app.route('/report/<report_id>')
def view_report(report_id):
    try:
        d = mongo.db.potholes.find_one({'_id': ObjectId(report_id)})
    except:
        d = None
    if not d:
        abort(404)
    d['_id'] = str(d['_id'])
    d['timestamp'] = d['timestamp'].isoformat()
    d['image_url'] = f"data:{d['image_mime']};base64,{d['image_data']}"
    if d.get('reported_by'):
        u = mongo.db.users.find_one({'_id': d['reported_by']})
        d['reported_by_username'] = u['username'] if u else None
    return render_template('view_report.html', report=d)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
