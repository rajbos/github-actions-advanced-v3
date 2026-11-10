import { createServer } from 'node:http';
import { pathToFileURL } from 'node:url';
import pc from 'picocolors';

export function createApp() {
  return createServer((request, response) => {
    response.setHeader('content-type', 'application/json');
    if (request.url === '/health') {
      response.end(JSON.stringify({ status: 'ok' }));
      return;
    }
    response.statusCode = 404;
    response.end(JSON.stringify({ error: 'not found' }));
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const server = createApp();
  server.listen(3000, '127.0.0.1', () => {
    console.log(pc.green('Listening at http://127.0.0.1:3000/health'));
  });
}
