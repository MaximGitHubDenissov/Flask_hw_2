from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)


@app.route('/')
def base():
    context = {'title': 'login'}
    return render_template('login.html', **context)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        res = make_response(redirect('/main/'))
        res.set_cookie('user_name', user_name, max_age=60 * 60 * 24 * 365 * 2)
        res.set_cookie('user_email', user_email, max_age=60 * 60 * 24 * 365 * 2)
        return res
    context = {'title': 'login'}
    res = make_response(render_template('login.html', **context))
    res.delete_cookie('user_name')
    res.delete_cookie('user_email')
    return res


@app.route('/main/')
def main():
    context = {'title': 'main',
               'user': None
               }
    if not request.cookies.get('user_name'):
        context['user'] = 'Незнакомец'
    else:
        context['user'] = request.cookies.get('user_name')
    return render_template('main.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
