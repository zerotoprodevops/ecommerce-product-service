from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Connect to PostgreSQL using the K8 Service name
DB_HOST = os.getenv('DB_HOST', 'product-db-service')
DB_NAME = os.getenv('DB_NAME', 'shop')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

def get_db_connection():
    # Retry logic for when the DB is still starting up
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except Exception as e:
            print(f"Waiting for DB... {e}")
            time.sleep(3)
    raise Exception("Could not connect to database")

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    # Assuming a table called 'products' exists
    cur.execute('SELECT id, name, price FROM products;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        })
    return jsonify(products)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)