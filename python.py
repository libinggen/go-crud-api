from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="yourpassword"
    )
    return conn

@app.route('/books', methods=['GET'])
def get_books():
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, title, author, year FROM books")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(books)

@app.route('/books/<string:id>', methods=['GET'])
def get_book(id):
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, title, author, year FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    cur.close()
    conn.close()
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO books (id, title, author, year) VALUES (%s, %s, %s, %s)",
                    (new_book['id'], new_book['title'], new_book['author'], new_book['year']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(new_book), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/books/<string:id>', methods=['PUT'])
def update_book(id):
    updated_book = request.get_json()
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s",
                    (updated_book['title'], updated_book['author'], updated_book['year'], id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(updated_book)
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/books/<string:id>', methods=['DELETE'])
def delete_book(id):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM books WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"result": "success"}), 200
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)