from bottle import Bottle, run, response
import subprocess
import os

app = Bottle()

# Path to your Python script
script_path = os.path.join(os.path.dirname(__file__), '../openai/htwcodingmentor.py')

@app.route('/run-script')
def run_python_script():
    try:
        # Run the Python script using subprocess
        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        if result.returncode == 0:
            # If script runs successfully, return its output
            response.content_type = 'text/plain'
            return result.stdout
        else:
            # If there is an error, return the error message
            response.status = 500
            return f"Error executing Python script: {result.stderr}"

    except Exception as e:
        response.status = 500
        return f"An error occurred: {str(e)}"

# Run the Bottle server on port 3000
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=3000)
