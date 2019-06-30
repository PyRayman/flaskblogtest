# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for , request
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm, CreatePostForm
from flask_login import current_user,login_user, logout_user, login_required
from app.models import User,Post
from app import db


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('user_page'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc !='':
			next_page = url_for('user_page',username=current_user.username)  
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)



@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return refirect(url_for('user_page'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register', form=form)



@app.route('/create_post',methods=['GET','POST'])
def create_post():
	if  not current_user.is_authenticated:
		return redirect(url_for('login'))
	form = CreatePostForm()
	if form.validate_on_submit():

		post = Post(body=form.body.data,user_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash('Post Was Created!')
		return redirect(url_for('user_page',username=current_user.username))
	return render_template('create_post.html',form=form, title = 'Create Post')






@app.route('/user/<username>')
@login_required
def user_page(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('User_page.html', posts=Post.query.filter_by(user_id=user.id).all(), user=user)




#обработка ошибок
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))