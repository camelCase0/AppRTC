from project import app
import os

if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('PORT', 5000))
