from flask import Blueprint, jsonify, request
import os
import json
from website.routes.auth_routes import login_required

api = Blueprint('api', __name__)

@api.route('/api/calls', methods=['GET'])
@login_required
def get_calls():
    """API endpoint to get all call logs"""
    call_logs = get_call_logs()
    return jsonify({"success": True, "data": call_logs})

@api.route('/api/calls/recent', methods=['GET'])
@login_required
def get_recent_calls():
    """API endpoint to get recent call logs"""
    limit = request.args.get('limit', 5, type=int)
    call_logs = get_call_logs()
    recent_logs = call_logs[:limit]
    return jsonify({"success": True, "data": recent_logs})

@api.route('/api/calls/<timestamp>', methods=['GET'])
@login_required
def get_call(timestamp):
    """API endpoint to get a specific call log"""
    call_log = get_call_log_by_timestamp(timestamp)
    if call_log:
        return jsonify({"success": True, "data": call_log})
    return jsonify({"success": False, "message": "Call log not found"}), 404

@api.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """API endpoint to get call statistics"""
    call_logs = get_call_logs()
    
    # Calculate statistics
    total_calls = len(call_logs)
    
    # Count calls by service type
    service_types = {}
    for log in call_logs:
        service = log.get('service_requested', 'Unknown')
        if service in service_types:
            service_types[service] += 1
        else:
            service_types[service] = 1
    
    # Count calls by day (last 7 days)
    import datetime
    calls_by_day = {}
    today = datetime.datetime.now().date()
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        calls_by_day[day_str] = 0
    
    for log in call_logs:
        try:
            timestamp = log.get('timestamp', '')
            if timestamp:
                dt = datetime.datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                day_str = dt.strftime("%Y-%m-%d")
                if day_str in calls_by_day:
                    calls_by_day[day_str] += 1
        except:
            pass
    
    return jsonify({
        "success": True, 
        "data": {
            "total_calls": total_calls,
            "service_types": service_types,
            "calls_by_day": calls_by_day
        }
    })

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
