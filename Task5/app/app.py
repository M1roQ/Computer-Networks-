from flask import Flask, request, jsonify

from db import get_db

app = Flask(__name__)


@app.route("/api/add_url", methods=["POST"])
def add_url():
    url = request.args.get("url")
    if not url:
        return "No URL provided", 400

    conn, cursor = get_db()
    cursor.execute("INSERT INTO urls (url) VALUES (%s);", (url,))
    conn.commit()
    return "URL added", 200


@app.route("/api/urls", methods=["GET"])
def get_urls():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM urls;")
    rows = cursor.fetchall()
    return jsonify([{"id": r[0], "url": r[1]} for r in rows])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
