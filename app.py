from flask import Flask, render_template
app = Flask(__name__, template_folder='template')


@app.route('/')
def main():
    return render_template('welcome.html')

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/profile')
def pro():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run()
