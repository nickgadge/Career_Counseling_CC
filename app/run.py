from app import create_app  # your factory function

app = create_app()  # keep this if you use factory, otherwise directly use app = Flask(__name__)

# Enable debug and auto-reload templates
app.debug = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "dev_secret_key"  # required for sessions

if __name__ == "__main__":
    # Use 0.0.0.0 if you want to access from other devices in the network
    app.run(host="127.0.0.1", port=5000, debug=True)
