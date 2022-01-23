from project import app
import os

if __name__ == "__main__":
    app.run(debug=False, port=os.environ.get('PORT', 5000), host='0.0.0.0')
