module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let query = 'Hello JARVIS';
  if (req.body && req.body.contents && req.body.contents[0] && req.body.contents[0].parts && req.body.contents[0].parts[0] && req.body.contents[0].parts[0].text) {
    query = req.body.contents[0].parts[0].text;
  } else if (req.body.query) {
    query = req.body.query;
  }

  const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
  
  if (!GEMINI_API_KEY) {
    return res.status(500).json({ error: 'Gemini API key not configured' });
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${GEMINI_API_KEY}`;

  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: `JARVIS Iron Man assistant: ${query}` }] }]
    })
  })
  .then(response => response.json())
  .then(data => {
    const answer = data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] ? data.candidates[0].content.parts[0].text : 'No response from JARVIS.';
    res.json({ answer });
  })
  .catch(error => {
    console.error(error);
    res.status(500).json({ error: 'Gemini API error' });
  });
};
