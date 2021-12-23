from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# from MAPF import show_animation

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Messages(db.Model):
#     __tablename_ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.Text())

#     def __init__(self, message):
#         self.message = message


     
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/demo')
# def demo():
#     animation = show_animation()

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if message == '':
            return render_template('index.html', message='Enter a message.')
        # data = Messages(message)
        # db.session.add(data)
        # db.session.commit()
        return render_template('success.html')


if __name__ == '__main__':

    app.run()