from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
CORS(app)

# Prometheus Metriken
REQUEST_COUNT   = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency')

# MySQL Verbindung
def get_db():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'db'),
        user=os.environ.get('MYSQL_USER', 'pokemon'),
        password=os.environ.get('MYSQL_PASSWORD', 'pokemon123'),
        database=os.environ.get('MYSQL_DATABASE', 'pokemon_tracker')
    )

# ============================================
# Karten (Cards)
# ============================================

@app.route('/api/cards', methods=['POST'])
def save_card():
    """Karte von TCG API lokal speichern"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cards (id, name, set_name, image_url, market_price)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                market_price = VALUES(market_price),
                updated_at   = NOW()
        ''', (data['id'], data['name'], data.get('set_name'), data.get('image_url'), data.get('market_price')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Karte gespeichert'}), 201
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ============================================
# Einträge (Entries)
# ============================================

@app.route('/api/entries', methods=['GET'])
def get_entries():
    start = time.time()
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT e.*, c.image_url, c.market_price as current_market_price
            FROM entries e
            LEFT JOIN cards c ON e.card_id = c.id
            ORDER BY e.date DESC, e.created_at DESC
        ''')
        entries = cursor.fetchall()
        for e in entries:
            e['date']       = str(e['date'])
            e['created_at'] = str(e['created_at'])
            e['amount']     = float(e['amount']) if e['amount'] else 0
        cursor.close()
        conn.close()
        REQUEST_COUNT.labels('GET', '/api/entries', '200').inc()
        return jsonify(entries)
    except Exception as ex:
        REQUEST_COUNT.labels('GET', '/api/entries', '500').inc()
        return jsonify({'error': str(ex)}), 500
    finally:
        REQUEST_LATENCY.observe(time.time() - start)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    start = time.time()
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO entries (type, name, amount, date, card_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (data['type'], data['name'], data['amount'], data['date'], data.get('card_id')))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        REQUEST_COUNT.labels('POST', '/api/entries', '201').inc()
        return jsonify({'id': new_id, 'message': 'Eintrag gespeichert'}), 201
    except Exception as ex:
        REQUEST_COUNT.labels('POST', '/api/entries', '500').inc()
        return jsonify({'error': str(ex)}), 500
    finally:
        REQUEST_LATENCY.observe(time.time() - start)

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM entries WHERE id = %s', (entry_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Eintrag gelöscht'})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ============================================
# Portfolio
# ============================================

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT p.*, c.name, c.set_name, c.image_url, c.market_price
            FROM portfolio p
            JOIN cards c ON p.card_id = c.id
            WHERE p.quantity > 0
            ORDER BY c.name
        ''')
        portfolio = cursor.fetchall()
        for p in portfolio:
            p['buy_price']    = float(p['buy_price'])   if p['buy_price']   else 0
            p['market_price'] = float(p['market_price']) if p['market_price'] else 0
            p['updated_at']   = str(p['updated_at'])
        cursor.close()
        conn.close()
        return jsonify(portfolio)
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/api/portfolio', methods=['POST'])
def update_portfolio():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO portfolio (card_id, quantity, buy_price)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                quantity   = quantity + VALUES(quantity),
                updated_at = NOW()
        ''', (data['card_id'], data.get('quantity', 1), data['buy_price']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Portfolio aktualisiert'}), 201
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/api/portfolio/<string:card_id>', methods=['DELETE'])
def remove_from_portfolio(card_id):
    try:
        data = request.json or {}
        qty  = data.get('quantity', 1)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE portfolio
            SET quantity = GREATEST(0, quantity - %s)
            WHERE card_id = %s
        ''', (qty, card_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Portfolio aktualisiert'})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ============================================
# Statistiken
# ============================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM entries WHERE type IN ('buy', 'pack')")
        spent = float(cursor.fetchone()['total'])
        cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM entries WHERE type = 'sell'")
        earned = float(cursor.fetchone()['total'])
        cursor.execute("SELECT COALESCE(SUM(c.market_price * p.quantity), 0) as total FROM portfolio p JOIN cards c ON p.card_id = c.id WHERE p.quantity > 0")
        portfolio_value = float(cursor.fetchone()['total'])
        cursor.close()
        conn.close()
        return jsonify({
            'spent':           spent,
            'earned':          earned,
            'profit':          round(earned - spent, 2),
            'portfolio_value': portfolio_value
        })
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ============================================
# System
# ============================================

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health')
def health():
    try:
        conn = get_db()
        conn.close()
        db_status = 'ok'
    except:
        db_status = 'error'
    return jsonify({'status': 'ok', 'db': db_status, 'timestamp': str(datetime.now())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
