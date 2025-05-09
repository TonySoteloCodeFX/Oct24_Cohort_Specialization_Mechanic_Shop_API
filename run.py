from app import create_app
from app. models import db
from flask_cors import CORS
from flask import redirect
import os



app = create_app('ProductionConfig')

@app.route('/', methods = ['GET'])
def index():
    return redirect('/api/docs')

with app.app_context():
    # db.drop_all()
    db.create_all()

CORS(app)

if __name__ == '__main__':
    app.run(host='tonys-my-mechanic-shop-api.onrender.com', port=int(os.environ.get("PORT", 5000)))



