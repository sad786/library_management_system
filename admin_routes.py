from flask import Blueprint, request, jsonify,render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, BorrowRequest

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    print('Dashboard method is called.....')
    return render_template('admin.html')

@admin_bp.route('/')
def admin():
    admin_dashboard()

@admin_bp.route('/add_book',methods=['POST'])
def add_book():
    book_name = request.form.get('book')
    return f"Book '{book_name}' added successfully!"

@admin_bp.route('/create_user', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Incomplete data'}), 400

    new_user = User(email=data['email'], password=data['password'], role='user')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@admin_bp.route('/borrow_requests', methods=['GET'])
@jwt_required()
def view_borrow_requests():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    requests = BorrowRequest.query.all()
    return jsonify([{
        'id': r.id,
        'user_id': r.user_id,
        'book_id': r.book_id,
        'start_date': r.start_date,
        'end_date': r.end_date,
        'status': r.status
    } for r in requests])
