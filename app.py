#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 12:27:04 2020

@author: ben
"""

from flask import Flask, render_template, url_for, request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soc.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.String(200), nullable=True)
    pic = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])

def index():
    
    if request.method == 'POST':
        task_content = request.form['content']
        task_deadline = request.form['deadline']
        task_pic = request.form['pic']
        new_task = Todo(content=task_content, deadline=task_deadline, pic=task_pic )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
 
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
            return 'There was an issue with deleting that task'
        
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
   
    if request.method == 'POST':   
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with updating that task'
    else:
        return render_template('update.html', task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)