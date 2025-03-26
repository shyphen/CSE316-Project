from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import psutil
import time  # CHANGE: Added for timing the endpoint response
import logging  # CHANGE: Added for error logging

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# CHANGE: Set up logging to capture errors and performance metrics
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

terminated_processes = []

# Serve the interactive dashboard
@app.route('/')
def index():
    return send_from_directory('static', 'interactive_dashboard.html')

# System usage API
@app.route('/get_system_usage')
def get_system_usage():
    return jsonify({
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent
    })

# Process list API
@app.route('/get_processes')
def get_processes():
    start_time = time.time()  # CHANGE: Start timing the endpoint
    processes = []
    
    # CHANGE: Use a single cpu_percent call with interval=0 to avoid cumulative delays
    # First, collect all process objects to avoid repeated iterations
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'num_threads']):
        try:
            process_list.append(proc)
        except Exception as e:
            logger.error(f"Error accessing process: {e}")  # CHANGE: Log errors instead of silently passing

    # CHANGE: Calculate cpu_percent for all processes in one go to minimize delays
    for proc in process_list:
        try:
            info = proc.as_dict(attrs=['pid', 'name', 'memory_info', 'num_threads'])
            # Calculate cpu_percent with a minimal interval
            info['cpu_percent'] = proc.cpu_percent(interval=0)
            processes.append({
                'pid': info['pid'],
                'name': info['name'],
                'cpu_percent': info['cpu_percent'],
                'memory_usage': round(info['memory_info'].rss / 1024 / 1024, 2),
                'num_threads': info['num_threads']
            })
        except Exception as e:
            logger.error(f"Error processing process {proc.pid}: {e}")  # CHANGE: Log errors

    # CHANGE: Sort processes by CPU usage (descending) and limit to top 50 to improve response time
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    processes = processes[:50]

    end_time = time.time()  # CHANGE: End timing the endpoint
    logger.info(f"/get_processes took {end_time - start_time:.2f} seconds to process {len(processes)} processes")

    return jsonify(processes)

# Terminate process API
@app.route('/terminate', methods=['POST'])
def terminate_process():
    data = request.get_json()
    pid = data.get('pid')
    try:
        process = psutil.Process(pid)
        process_info = {
            'pid': pid,
            'name': process.name(),
            'cpu_percent': process.cpu_percent(interval=0),  # CHANGE: Use interval=0 to avoid delay
            'memory_usage': round(process.memory_info().rss / 1024 / 1024, 2),
            'num_threads': process.num_threads()
        }
        process.terminate()

        terminated_processes.append(process_info)
        return jsonify({'message': f'Process {pid} terminated.'})
    except Exception as e:
        logger.error(f"Error terminating process {pid}: {e}")  # CHANGE: Log errors
        return jsonify({'error': str(e)}), 500

@app.route('/get_terminated_processes')
def get_terminated_processes():
    return jsonify(terminated_processes)

if __name__ == '__main__':
    print("🌐 Server running at http://localhost:8070/")
    app.run(port=8070)
