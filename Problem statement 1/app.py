from flask import Flask, jsonify, request
import sqlite3
from datetime import date
from connection import condb
app = Flask(__name__)
@app.route("/add-book", methods=["POST"])
def add_book():
    data = request.json

    title = data["title"]
    author = data["author"]
    year = data["year"]

    conn = condb()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO books (title, author, year, available)
        VALUES (?, ?, ?, 1)
    """, (title, author, year))

    book_id = cur.lastrowid  # AUTO GENERATED ID

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Book added successfully",
        "bookid": book_id
    })

@app.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.json
    regno = data["regno"]
    name = data["name"]
    bookid = data["bookid"]
    title = data["title"]
    author = data["author"]
    year = data["year"]
    conn = condb()
    cur = conn.cursor()

    # Verify book exists and matches details
    book = cur.execute("""
        SELECT available FROM books
        WHERE bookid = ? AND title = ? AND author = ? AND year = ?
    """, (bookid, title, author, year)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    if book["available"] == 0:
        conn.close()
        return jsonify({"error": "Book not available"}), 400

    # Borrow book
    cur.execute("""
        INSERT INTO borrowed_books (regno, bookid, date)
        VALUES (?, ?, DATE('now'))
    """, (regno, bookid))

    # Update book availability
    cur.execute("""
        UPDATE books SET available = 0 WHERE bookid = ?
    """, (bookid,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Book borrowed successfully"})
@app.route("/return", methods=["POST"])
def return_book():
    data = request.json

    bookid = data["bookid"]
    title = data["title"]
    author = data["author"]
    year = data["year"]

    conn = condb()
    cur = conn.cursor()

    # Verify book exists
    book = cur.execute("""
        SELECT bookid FROM books
        WHERE bookid = ? AND title = ? AND author = ? AND year = ?
    """, (bookid, title, author, year)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    # Check if book is borrowed
    borrowed = cur.execute("""
        SELECT id FROM borrowed_books WHERE bookid = ?
    """, (bookid,)).fetchone()

    if not borrowed:
        conn.close()
        return jsonify({"error": "Book is not currently borrowed"}), 400

    # Remove borrow record
    cur.execute("""
        DELETE FROM borrowed_books WHERE bookid = ?
    """, (bookid,))

    # Mark book as available
    cur.execute("""
        UPDATE books SET available = 1 WHERE bookid = ?
    """, (bookid,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Book returned successfully"})

@app.route("/books", methods=["GET"])
def list_books():
    conn = condb()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return jsonify([dict(b) for b in books])
if __name__ == "__main__":
    app.run(debug=True)



