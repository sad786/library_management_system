from flask import Blueprint, request, jsonify, make_response,render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Book, BorrowRequest, BorrowHistory
import csv

user_bp = Blueprint('user', __name__)

@user_bp.route('/user_dashboard')
def user_dashboard():
    return render_template('user.html')

@user_bp.route('/')
def user():
    user_dashboard()

@user_bp.route('/search',methods=['GET'])
def search_book():
    query = request.args.get('query')

    #Login to handle search request
    return f"Request for '{query}'"


@user_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'available': book.available
    } for book in books])

@user_bp.route('/borrow_history/download', methods=['GET'])
@jwt_required()
def download_borrow_history():
    current_user = get_jwt_identity()
    borrow_history = BorrowHistory.query.filter_by(user_id=current_user['id']).all()
    if not borrow_history:
        return jsonify({'message': 'No borrow history available'}), 404

    output = []
    for record in borrow_history:
        book = Book.query.get(record.book_id)
        output.append({
            'Book Title': book.title,
            'Author': book.author,
            'Borrowed Date': record.borrowed_date,
            'Returned Date': record.returned_date or 'Not Returned'
        })

    response = make_response()
    writer = csv.DictWriter(response, fieldnames=output[0].keys())
    writer.writeheader()
    writer.writerows(output)

    response.headers['Content-Disposition'] = 'attachment; filename=borrow_history.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response
