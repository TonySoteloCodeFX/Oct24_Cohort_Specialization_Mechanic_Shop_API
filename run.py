from app import create_app
from app. models import db
from flask_cors import CORS
import os



app = create_app('ProductionConfig')

with app.app_context():
    # db.drop_all()
    db.create_all()

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))



