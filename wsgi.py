from app2 import init_app

app, db = init_app()

if __name__ == "__main__":
    app.run(debug=True)