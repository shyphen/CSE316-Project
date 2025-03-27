from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import psutil
import time
import logging
import threading  # Added for benchmark simulation

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

terminated_processes = []

@app.route('/')
def index():
    return send_from_directory('static', 'interactive_dashboard.html')

@app.route('/get_system_usage')
def get_system_usage():
    return jsonify({
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent
    })

@app.route('/get_processes')
def get_processes():
    start_time = time.time()
    processes = []
    
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'num_threads']):
        try:
            process_list.append(proc)
        except Exception as e:
            logger.error(f"Error accessing process: {e}")

    for proc in process_list:
        try:
            info = proc.as_dict(attrs=['pid', 'name', 'memory_info', 'num_threads'])
            info['cpu_percent'] = proc.cpu_percent(interval=0)
            processes.append({
                'pid': info['pid'],
                'name': info['name'],
                'cpu_percent': info['cpu_percent'],
                'memory_usage': round(info['memory_info'].rss / 1024 / 1024, 2),
                'num_threads': info['num_threads']
            })
        except Exception as e:
            logger.error(f"Error processing process {proc.pid}: {e}")

    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    processes = processes[:50]

    end_time = time.time()
    logger.info(f"/get_processes took {end_time - start_time:.2f} seconds to process {len(processes)} processes")
    return jsonify(processes)

@app.route('/terminate', methods=['POST'])
def terminate_process():
    data = request.get_json()
    pid = data.get('pid')
    try:
        process = psutil.Process(pid)
        process_info = {
            'pid': pid,
            'name': process.name(),
            'cpu_percent': process.cpu_percent(interval=0),
            'memory_usage': round(process.memory_info().rss / 1024 / 1024, 2),
            'num_threads': process.num_threads()
        }
        process.terminate()

        terminated_processes.append(process_info)
        return jsonify({'message': f'Process {pid} terminated.'})
    except Exception as e:
        logger.error(f"Error terminating process {pid}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_terminated_processes')
def get_terminated_processes():
    for proc in terminated_processes:
        if 'timestamp' not in proc:
            proc['timestamp'] = time.time()
    return jsonify(terminated_processes)

# New: Battery Status Endpoint
@app.route('/get_battery_status')
def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return jsonify({
                'percent': 100,  # Default for systems without battery
                'secsleft': -1,
                'power_plugged': True,
                'power_consumption': 0.0  # Placeholder, as this isn't directly available
            })
        # Estimate power consumption (simplified, as psutil doesn't provide this directly)
        power_consumption = psutil.cpu_percent() * 0.1  # Rough estimate in watts
        return jsonify({
            'percent': battery.percent,
            'secsleft': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else -1,
            'power_plugged': battery.power_plugged,
            'power_consumption': power_consumption
        })
    except Exception as e:
        logger.error(f"Error fetching battery status: {e}")
        return jsonify({'error': str(e)}), 500

# New: Benchmark Endpoint
@app.route('/run_benchmark', methods=['POST'])
def run_benchmark():
    data = request.get_json()
    test_type = data.get('test_type')
    try:
        # Simulate a benchmark (since real benchmarking requires more complex logic)
        start_time = time.time()
        if test_type == "cpu":
            # Simulate CPU stress
            for _ in range(1000000):
                _ = 2 ** 20
            score = 1000 / (time.time() - start_time)  # Arbitrary score based on time
        elif test_type == "memory":
            # Simulate memory allocation
            temp = [0] * (10 ** 7)  # Allocate 10M integers
            score = 500 / (time.time() - start_time)  # Arbitrary score
            del temp
        else:
            return jsonify({'error': 'Invalid test type'}), 400

        return jsonify({
            'test_type': test_type,
            'score': round(score, 2),
            'baseline_comparison': "Average",  # Placeholder for real comparison
            'system_load': psutil.cpu_percent(interval=0)
        })
    except Exception as e:
        logger.error(f"Error running benchmark {test_type}: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Server running at http://localhost:8070/")
    app.run(port=8070)
