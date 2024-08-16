from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST', 'coolify-db')
DB_NAME = os.environ.get('DB_NAME', 'coolify')
DB_USER = os.environ.get('DB_USER', 'coolify')
DB_PASS = os.environ.get('DB_PASS', 'your_password')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/status/<application_id>', methods=['GET'])
def get_status(application_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Adjust this query based on Coolify's actual database schema
        query = f"""
        SELECT
            deployment_uuid,
            status
        FROM
            application_deployment_queues
        WHERE
            application_id = '{application_id}'
        ORDER BY
            created_at DESC
        LIMIT
            1;

        """
        cur.execute(query)

        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify({"deployment_uuid": result["deployment_uuid"],"status": result['status']})
        else:
            return jsonify({"error": "Application not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)