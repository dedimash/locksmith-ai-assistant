from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
import os
import json
import datetime
from website.routes.auth_routes import login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page"""
    if 'logged_in' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page with call logs summary"""
    # Get call logs
    call_logs = get_call_logs()
    
    # Calculate statistics
    total_calls = len(call_logs)
    recent_calls = len([log for log in call_logs if is_recent(log.get('timestamp', ''))])
    
    # Group calls by service type
    service_types = {}
    for log in call_logs:
        service = log.get('service_requested', 'Unknown')
        if service in service_types:
            service_types[service] += 1
        else:
            service_types[service] = 1
    
    return render_template('dashboard.html', 
                          total_calls=total_calls,
                          recent_calls=recent_calls,
                          service_types=service_types,
                          recent_call_logs=get_recent_call_logs(5))

@main.route('/calls')
@login_required
def calls():
    """Page displaying all call logs"""
    call_logs = get_call_logs()
    return render_template('calls.html', call_logs=call_logs)

@main.route('/call/<timestamp>')
@login_required
def call_detail(timestamp):
    """Page displaying details of a specific call"""
    call_log = get_call_log_by_timestamp(timestamp)
    if call_log:
        return render_template('call_detail.html', call=call_log)
    flash('Call log not found', 'danger')
    return redirect(url_for('main.calls'))

@main.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')

def get_call_logs():
    """Get all call logs"""
    logs = []
    from flask import current_app
    logs_dir = current_app.config['CALL_LOGS_DIR']
    
    if not os.path.exists(logs_dir):
        return logs
    
    for filename in os.listdir(logs_dir):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(logs_dir, filename), 'r') as f:
                    log_data = json.load(f)
                    # Add timestamp from filename
                    timestamp = filename.replace('call_', '').replace('.json', '')
                    log_data['timestamp'] = timestamp
                    logs.append(log_data)
            except Exception as e:
                print(f"Error reading log file {filename}: {e}")
    
    # Sort logs by timestamp (newest first)
    logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return logs

def get_recent_call_logs(limit=5):
    """Get recent call logs with limit"""
    logs = get_call_logs()
    return logs[:limit]

def get_call_log_by_timestamp(timestamp):
    """Get a specific call log by timestamp"""
    from flask import current_app
    logs_dir = current_app.config['CALL_LOGS_DIR']
    
    filename = f"call_{timestamp}.json"
    file_path = os.path.join(logs_dir, filename)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                log_data = json.load(f)
                log_data['timestamp'] = timestamp
                return log_data
        except Exception as e:
            print(f"Error reading log file {filename}: {e}")
    
    return None

def is_recent(timestamp, days=1):
    """Check if a timestamp is recent (within specified days)"""
    try:
        # Parse timestamp from format YYYYMMDD_HHMMSS
        dt = datetime.datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        now = datetime.datetime.now()
        delta = now - dt
        return delta.days < days
    except:
        return False
