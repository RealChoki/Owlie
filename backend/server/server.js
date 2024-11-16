const path = require('path');
const { PythonShell } = require('python-shell');
const Fastify = require('fastify');
const fastify = Fastify({ logger: true });

// Use `path.resolve` to create an absolute path to the Python script
const scriptPath = path.resolve(__dirname, '../openai/htwcodingmentor.py');

fastify.post('/chat', async (request, reply) => {
  const { message } = request.body;  // Get the message from the request body

  if (!message) {
    return reply.status(400).send({ error: 'Message is required' });
  }

  console.log("Received message:", message);

  // Pass the message to Python script
  const options = {
    args: [message]
  };
  

  try {
    const result = await new Promise((resolve, reject) => {
      console.log("Executing Python script...");
      PythonShell.run(scriptPath, options, (err, results) => {
        console.log("Python script executed");
        console.log(scriptPath, options);
        if (err) {
          reject(err);
        } else {
          resolve(results);
        }
      });
    });

    // Log and send the Python script result back to the client
    console.log("Python script response:", result);  // Log the result from the Python script
    reply.send({ response: result.join(' ') });
  } catch (error) {
    console.error('Error executing Python script:', error);
    reply.status(500).send({ error: 'Internal server error' });
  }
});

// Start the Fastify server
fastify.listen({ port: 3000, host: '0.0.0.0' }, (err, address) => {
  if (err) {
    fastify.log.error(err);
    process.exit(1);
  }
  fastify.log.info(`Server listening at ${address}`);
});
