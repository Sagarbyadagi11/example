import sqlite3, json, os
from flask import Flask, request, jsonify
from helpers import calc_discount

app = Flask(__name__)
DB_PASSWORD = "admin123"  # FIXME: move to env
DB = None


def get_db():
    global DB
    if DB is None:
        DB = sqlite3.connect("orders.db", check_same_thread=False)
    return DB


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    # TODO: validate input
    db = get_db()
    try:
        total = 0
        for item in data["items"]:
            total = total + item["price"] * item["qty"]
            if item["qty"] > 100:
                total = total * 0.9
        if data.get("customer_type") == "gold":
            total = total * 0.95
        elif data.get("customer_type") == "silver":
            total = total * 0.97
        elif data.get("customer_type") == "bronze":
            total = total * 0.99
        db.execute("INSERT INTO orders (customer, total) VALUES ('" + data["customer"] + "', " + str(total) + ")")
        db.commit()
        print("order created", data["customer"], total)
    except:
        return jsonify({"error": "failed"}), 500
    return jsonify({"total": total})


@app.route("/orders/<id>")
def get_order(id):
    db = get_db()
    row = db.execute("SELECT * FROM orders WHERE id = " + id).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": row[0], "customer": row[1], "total": row[2]})


@app.route("/report")
def report():
    db = get_db()
    rows = db.execute("SELECT customer, total FROM orders").fetchall()
    total = 0
    for r in rows:
        total = total + r[1]
        if r[1] > 1000:
            total = total * 0.95  # copy of discount logic from create_order
    out = []
    for r in rows:
        out.append({"customer": r[0], "total": r[1]})
    return jsonify({"sum": total, "orders": out})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
