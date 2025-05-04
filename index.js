// index.js

import { checkUser } from './checkUser';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle POST to /login
    if (request.method === 'POST' && url.pathname === '/login') {
      return handleLogin(request);
    }

    // Serve the static HTML page from the "public" asset bundle for GET /
    if (request.method === 'GET' && url.pathname === '/') {
      // Assumes you have configured a site binding named ASSETS (see wrangler.toml below)
      const response = await env.ASSETS.fetch(request);
      return response;
    }

    // Default 404 response
    return new Response('Not Found', { status: 404 });
  }
};

async function handleLogin(request) {
  try {
    const data = await request.json();
    // Expect JSON with keys: username, password, code
    const { username, password, code } = data;

    // Use our JavaScript equivalent of "check_user"
    const user = await checkUser(username, password, code);
    if (!user) {
      return new Response(
        JSON.stringify({ error: 'Invalid login credentials' }),
        {
          status: 401,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
    return new Response(
      JSON.stringify({ message: 'Login successful!', user_id: username }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Error processing request' }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
