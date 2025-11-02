const express = require('express');
const axios = require('axios');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Simple logger
app.use(morgan('tiny'));

// Serve static frontend
app.use(express.static('public'));

/**
 * GET /download?url=<remote-file-url>
 * Streams the remote file through this server so the browser can download it.
 */
app.get('/download', async (req, res) => {
  const target = req.query.url;
  if (!target) {
    return res.status(400).send('Missing url parameter. Usage: /download?url=<remote-file-url>');
  }

  // Basic URL validation
  let parsed;
  try {
    parsed = new URL(target);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return res.status(400).send('Only http(s) URLs are supported.');
    }
  } catch (err) {
    return res.status(400).send('Invalid URL.');
  }

  try {
    // Stream the remote response
    const resp = await axios.get(target, {
      responseType: 'stream',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; music-download-free-web/1.0)'
      },
      timeout: 30000
    });

    // Try to determine filename from remote headers or URL path
    let filename = 'download';
    const disp = resp.headers['content-disposition'];
    if (disp) {
      const m1 = disp.match(/filename\*=UTF-8''([^;]+)/);
      const m2 = disp.match(/filename="?([^" ]+)"?/);
      if (m1 && m1[1]) filename = decodeURIComponent(m1[1]);
      else if (m2 && m2[1]) filename = m2[1];
    }
    if (!filename || filename === 'download') {
      const pathParts = parsed.pathname.split('/');
      const last = pathParts[pathParts.length - 1];
      if (last) filename = last.split('?')[0] || 'download';
    }

    // Set headers for browser download
    res.setHeader('Content-Type', resp.headers['content-type'] || 'application/octet-stream');
    if (resp.headers['content-length']) {
      res.setHeader('Content-Length', resp.headers['content-length']);
    }
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);

    // Pipe remote stream directly to response
    resp.data.pipe(res);

    // Handle stream errors
    resp.data.on('error', (err) => {
      console.error('Stream error from remote:', err.message || err);
      if (!res.headersSent) res.status(500).send('Error streaming remote file.');
      else res.destroy(err);
    });
  } catch (err) {
    console.error('Download proxy error:', err && err.message ? err.message : err);
    if (err.response && err.response.status) {
      return res.status(err.response.status).send(`Upstream responded with status ${err.response.status}`);
    }
    return res.status(500).send('Failed to fetch remote file.');
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
