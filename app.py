from flask import Flask, render_template, request
import os
import glob
# from flask_sqlalchemy import SQLAlchemy
from util.generate_instance import write_instance
from util.run_experiments_demo import create_plot, create_animation
from threading import Thread
import time

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

# potential for use...
# https://stackoverflow.com/questions/18082683/need-to-execute-a-function-after-returning-the-response-in-flask
class Compute(Thread):
    def __init__(self, i_path, f_path):
        Thread.__init__(self)
        self.i_path = i_path
        self.f_path = f_path

    def run(self): # call the thread.start()
        print("start")
        # call cbs here
        print("done")

     
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/background')
def background():
    return render_template('background.html')


@app.route('/demo-CT/standard')
def demo_standardCT():
    # get animation figures
    figure_path = "/content/figures/CT_demo/standard_figs/expanded_nodes/"
    abs_path = os.path.abspath("static/content/figures/CT_demo/standard_figs/expanded_nodes") # or globs
    print(abs_path)
    branches = os.walk(abs_path)
    figure_path_demo = []
    for b in branches:
        print (b)
        (_,_,fig_files) = b
        for fig_file in fig_files:
            print(fig_files)
            figure_path_demo.append(figure_path + fig_file)
            print(figure_path + fig_file)
    figure_path_demo.sort()
    print(figure_path_demo)
    # get CT graphs
    CT_path = "/content/figures/CT_demo/standard_ct/"
    abs_path = os.path.abspath("static/content/figures/CT_demo/standard_ct")
    branches = os.walk(abs_path)
    CT_path_demo = []
    for b in branches:
        print (b)
        (_,_,CT_files) = b
        for fig_file in CT_files:
            # print(CT_files)
            CT_path_demo.append(CT_path + fig_file)
            # print(CT_path + fig_file)
    CT_path_demo.sort()
    print(figure_path_demo)
    print(CT_path_demo)


    return render_template('demo_CT.html', splitter="Standard", figures=figure_path_demo, CTs=CT_path_demo)

@app.route('/demo-CT/disjoint')
def demo_disjointCT():
    # get animation figures
    figure_path = "/content/figures/CT_demo/disjoint_figs/expanded_nodes/"
    abs_path = os.path.abspath("static/content/figures/CT_demo/disjoint_figs/expanded_nodes") # or globs
    print(abs_path)
    branches = os.walk(abs_path)
    figure_path_demo = []
    for b in branches:
        print (b)
        (_,_,fig_files) = b
        for fig_file in fig_files:
            print(fig_files)
            figure_path_demo.append(figure_path + fig_file)
            print(figure_path + fig_file)
    figure_path_demo.sort()
    print(figure_path_demo)
    # get CT graphs
    CT_path = "/content/figures/CT_demo/disjoint_ct/"
    abs_path = os.path.abspath("static/content/figures/CT_demo/disjoint_ct")
    branches = os.walk(abs_path)
    CT_path_demo = []
    for b in branches:
        print (b)
        (_,_,CT_files) = b
        for fig_file in CT_files:
            # print(CT_files)
            CT_path_demo.append(CT_path + fig_file)
            # print(CT_path + fig_file)
    CT_path_demo.sort()
    print(figure_path_demo)
    print(CT_path_demo)


    return render_template('demo_CT.html', splitter="Disjoint", figures=figure_path_demo, CTs=CT_path_demo)



# @app.route('/demo-CT/disjoint')
# def demo_disjointCT():
#     figure_path = "/content/figures/CT_demo/disjoint_figs/"
#     abs_path = os.path.abspath("static/content/figures/CT_demo/disjoint_figs") # or globs
#     print(abs_path)
#     # _,_,branches = os.walk(abs_path)
#     branches = os.walk(abs_path)
#     # print("AJJJJJJJJJJJJJJJJFDGADS")
#     figure_path_demo = []
#     for b in branches:
#         print (b)
#         (_,_,fig_files) = b
#         for fig_file in fig_files:
#             print(fig_files)
#             figure_path_demo.append(figure_path + fig_file)
#             print(figure_path + fig_file)

#     figure_path_demo.sort()
#     return render_template('demo_CT.html', figures=figure_path_demo, results=[])


@app.route('/demo')
def demo():
    figure_path = "content/figures/maps/newmap.png"
    return render_template('generate.html', figure=figure_path, results=[])

@app.route('/instance')
def instance():
    instance_path = os.path.abspath("static/content/instances/new_instance.txt")
    figure_path = os.path.abspath("static/content/figures/maps/newmap.png")
    write_instance(file_loc=instance_path)
    create_plot(instance_path, figure_path)

    # figure_path = os.path.abspath("static/content/figures/newfigure.gif")
    # # find solutions... CBS
    # solver = "CBS"
    # solution = create_animation(instance_path, figure_path, solver=solver)

    # # find solutions... ICBS

    return render_template('generate.html', figure="content/figures/maps/newmap.png", results=[])

@app.route('/figure-cbs')
def figure_cbs():
    instance_path = os.path.abspath("static/content/instances/new_instance.txt")
    figure_path = os.path.abspath("static/content/figures/newfigure.gif")
    solver = "CBS"
    solution = create_animation(instance_path, figure_path, solver=solver)
    # could move this into another function...
    results = []
    if solution is not None:
        paths, nodes_gen, nodes_exp, time = [solution[i] for i in range(4)]
        results.append('Search algorithm used: {}'.format(solver))
        results.append('Time taken: {}'.format(time))
        results.append('Number of nodes expanded: {}'.format(nodes_exp))
        results.append("Paths of agents:")
        for i, pa in enumerate(paths):
            pa_str = "agent {}: ".format(i)
            for j, loc in enumerate(pa):
                pa_str += "({},{})".format(loc[0],loc[1])
                if j < len(pa) - 1:
                    pa_str += "->"
            results.append(pa_str)
        
    return render_template('generate.html', figure="content/figures/newfigure.gif", results=results)

@app.route('/figure-icbs')
def figure_icbs():
    instance_path = os.path.abspath("static/content/instances/new_instance.txt")
    figure_path = os.path.abspath("static/content/figures/newfigure.gif")
    # write_instance(file_loc=instance_path)
    solver = "ICBS"
    solution = create_animation(instance_path, figure_path, solver=solver)
    # could move this into another function...
    results = []
    if solution is not None:
        paths, nodes_gen, nodes_exp, time = [solution[i] for i in range(4)]
        results.append('Search algorithm used: {}'.format(solver))
        results.append('Time taken: {} s'.format(time))
        results.append('Number of nodes expanded: {}'.format(nodes_exp))
        results.append("Paths of agents:")
        for i, pa in enumerate(paths):
            pa_str = "agent {}: ".format(i)
            for j, loc in enumerate(pa):
                pa_str += "({},{})".format(loc[0],loc[1])
                if j < len(pa) - 1:
                    pa_str += "->"
            results.append(pa_str)

    return render_template('generate.html', figure="content/figures/newfigure.gif", results=results)

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