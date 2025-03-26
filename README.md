# CSE316-Project
Real-Time Process Monitoring Dashboard

Project Overview
The Real-Time Process Monitoring Dashboard is a CSE316 project that provides real-time information on running processes and system parameters, similar to a task manager. It allows users to monitor system metrics like CPU and memory usage, and terminate processes directly from the dashboard. The backend is built using Flask, while the frontend uses HTML, CSS, and JavaScript for a responsive interface.

Features

- Real-time process monitoring**: Displays running processes with details like CPU and memory usage.
- Process termination**: Allows users to terminate selected processes.
- System performance monitoring**: Provides updates on key system parameters.
- Responsive frontend**: A user-friendly UI for interacting with the system.
- Backend API**: Handles system queries and user commands via Flask.

Technologies Used

Backend (Python)

- Flask:
  - Flask is the web framework used for serving the API to the frontend. It handles requests from the user interface, processes them, and returns the necessary data. Flask is ideal for small, lightweight applications.
  - Flask-CORS: This is used to allow cross-origin resource sharing, enabling the frontend (running on a different port) to communicate with the backend without security restrictions.
  
- psutil:
  - Provides an interface for retrieving system information such as CPU and memory usage, and process data. It enables the backend to gather real-time stats for the dashboard.
  
Frontend (HTML, CSS, JavaScript)

- HTML/CSS: 
  - The structure and styling of the dashboard. It presents the system data in a clean and organized layout.
  
- JavaScript:
  - AJAX Requests: JavaScript is responsible for making asynchronous requests to the Flask backend API using AJAX (Asynchronous JavaScript and XML). This allows the frontend to fetch real-time data without reloading the page.
  - DOM Manipulation: Once data is fetched from the backend, JavaScript dynamically updates the DOM (Document Object Model) to display the list of running processes, CPU usage, and memory stats.
  - Process Termination: When a user clicks the "Terminate" button next to a process, JavaScript sends the selected process's PID to the Flask backend for termination.

File Structure

- backend.py: 
  - This script runs the Flask server and serves API endpoints.
  - Key functionalities:
    - Retrieve the list of running processes via psutil.
    - Provide system stats like CPU and memory usage.
    - Handle requests to terminate specific processes, based on the Process ID (PID).
  
- frontend.html:
  - The user interface for interacting with the system. It includes tables that display real-time data, buttons for terminating processes, and dynamically updated stats.
  - JavaScript: Handles the interaction between the HTML interface and the backend API through AJAX requests.
  
- processmonitor.ipynb: 
  - Jupyter Notebook used for testing and prototyping. It includes code for fetching and displaying process data using psutil, and was an early step in developing the main features.

How It Works

Frontend (JavaScript):

1. Fetching Data:
   - JavaScript uses `fetch` to make asynchronous calls to the Flask API endpoints.
   - Data is fetched from the `/processes` API endpoint to retrieve the list of running processes.
   
2. Updating the Interface:
   - Once the data is received, JavaScript dynamically updates the HTML table that lists all processes, showing details like the process ID (PID), name, CPU usage, and memory usage.

3. Process Termination:
   - When the user clicks on the "Terminate" button next to a process, JavaScript captures the PID and sends a POST request to the Flask backend at `/terminate` to kill the process.

Backend (Flask and Flask-CORS):

1. Routing:
   - The Flask application provides several routes, such as:
     - `/processes`: Fetches the list of running processes using psutil.
     - `/terminate`: Accepts a PID and terminates the corresponding process.
  
2. CORS Support:
   - Using Flask-CORS, the backend allows the frontend (which might be served from a different port) to interact with it, ensuring proper communication without security issues.

3. Handling Requests:
   - Flask handles GET requests for system information (e.g., the list of processes) and POST requests when the user attempts to terminate a process.
  
4. Process Termination:
   - On receiving a termination request, Flask calls the psutil methods to safely kill the process with the given PID.

Installation & Setup

1. Clone the Repository:
   ```bash
   git clone https://github.com/Savant261/CSE316-Project.git
   cd CSE316-Project
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   This installs Flask, Flask-CORS, psutil, and other necessary dependencies.

3. **Run the Application**:
   Start the Flask server:
   ```bash
   python backend.py
   ```
   The dashboard will be accessible at `localhost:5000` in your browser.


License
This project is licensed under the Apache-2.0 license. See the [LICENSE](LICENSE) file for more details.
