from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import psutil

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

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
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'num_threads']):
        try:
            info = proc.info
            processes.append({
                'pid': info['pid'],
                'name': info['name'],
                'cpu_percent': info['cpu_percent'],
                'memory_usage': round(info['memory_info'].rss / 1024 / 1024, 2),
                'num_threads': info['num_threads']
            })
        except Exception:
            pass
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
            'cpu_percent': process.cpu_percent(),
            'memory_usage': round(process.memory_info().rss / 1024 / 1024, 2),
            'num_threads': process.num_threads()
        }
        process.terminate()

        terminated_processes.append(process_info)
        return jsonify({'message': f'Process {pid} terminated.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/get_terminated_processes')
def get_terminated_processes():
    return jsonify(terminated_processes)


if __name__ == '__main__':
    print("🌐 Server running at http://localhost:8070/")
    app.run(port=8070)
