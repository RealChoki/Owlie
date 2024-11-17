const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

// Route to execute Python script
app.get('/run-python', (req, res) => {
  console.log('Route hit: /run-python'); // Log when the route is hit

  // Run the Python script
  exec('python ../openai/htwcodingmentor.py "beschreibe mir java in 3 worten"', (error, stdout, stderr) => {
    console.log('Execution started');

    // Check for errors during the execution
    if (error) {
      console.error('Execution error:', error.message);
      return res.status(500).json({ error: 'Failed to execute Python script', details: error.message });
    }

    // Check for errors from the Python script (stderr)
    if (stderr) {
      console.error('Python error:', stderr);
      return res.status(500).json({ error: 'Error in Python script', details: stderr });
    }

    // If everything is fine, send the Python script output
    console.log('Python script output:', stdout.trim());
    return res.json({ output: stdout.trim() });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
