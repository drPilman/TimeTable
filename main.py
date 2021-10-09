from flask import Flask, render_template

app = Flask(__name__)


def print_hi(name):
    print(f'Hi, {name}')

@app.route("/", methods=["POST", "GET"])
def process():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)