module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query } = req.body;
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
    const answer = data.candidates[0]?.content?.parts[0]?.text || 'No response';
    res.json({ answer });
  })
  .catch(error => {
    console.error(error);
    res.status(500).json({ error: 'Gemini API error' });
  });
};

