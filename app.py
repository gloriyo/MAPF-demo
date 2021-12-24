from flask import Flask, render_template, request
import os
# from flask_sqlalchemy import SQLAlchemy
from code.generate_instance import write_instance
from code.run_experiments_demo import create_plot


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

@app.route('/demo')
def demo():
    figure_path = "content/figures/maps/newmap.png"
    return render_template('generate.html', figure=figure_path)

@app.route('/instance')
def instance():
    instance_path = os.path.abspath("static/content/instances/new_instance.txt")
    figure_path = os.path.abspath("static/content/figures/maps/newmap.png")
    write_instance(file_loc=instance_path)
    create_plot(instance_path, figure_path)

    return render_template('generate.html', figure="content/figures/maps/newmap.png")

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