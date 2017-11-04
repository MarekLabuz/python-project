from flask import Flask, send_file
app = Flask(__name__)


@app.route('/')
def root():
    return send_file('./front/build/index.html', mimetype='text/html')


@app.route('/bundle.js')
def bundle():
    return send_file('./front/build/bundle.js', mimetype='text/javascript')

if __name__ == '__main__':
    app.run()
