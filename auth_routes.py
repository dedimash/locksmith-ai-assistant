from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

auth = Blueprint('auth', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials against configured admin credentials
        from flask import current_app
        if (username == current_app.config['ADMIN_USERNAME'] and 
            password == current_app.config['ADMIN_PASSWORD']):
            
            session['logged_in'] = True
            session['username'] = username
            flash('You are now logged in', 'success')
            
            # Redirect to next parameter if available, otherwise to dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))
