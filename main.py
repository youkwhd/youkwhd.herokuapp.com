from app import create_app

app = create_app()
print(__name__)

@app.route("/")
def home():
    return "welcome to my webpage"

if __name__ == "__main__":
    app.run(debug=True)
