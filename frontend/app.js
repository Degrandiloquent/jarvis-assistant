const GEMINI_PROXY = '/api/gemini';

class JarvisUI {
  constructor() {
    this.micBtn = document.getElementById('micBtn');
    this.userInput = document.getElementById('userInput');
    this.sendBtn = document.getElementById('sendBtn');
    this.chatMessages = document.getElementById('chatMessages');
    this.waveCanvas = document.getElementById('waveVisualizer');
    this.timeDate = document.querySelector('.time-date');
    
    this.isListening = false;
    this.recognition = null;
    this.synth = window.speechSynthesis;
    this.waveCtx = this.waveCanvas.getContext('2d');
    
    this.audioContext = null;
    this.analyser = null;
    this.dataArray = null;
    
    this.init();
    this.updateTime();
    this.animateStars();
    this.setupEventListeners();
    this.initVisualizer();
    this.say('JARVIS online and ready, sir.');
  }

  init() {
    // Speech Recognition
    if ('webkitSpeechRecognition' in window) {
      this.recognition = new webkitSpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';
    }

    this.waveCanvas.width = this.waveCanvas.offsetWidth;
    this.waveCanvas.height = this.waveCanvas.offsetHeight;
  }

  setupEventListeners() {
    this.micBtn.addEventListener('click', () => this.toggleListening());
    
    this.sendBtn.addEventListener('click', () => this.sendMessage());
    this.userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });

    document.querySelectorAll('.cmd-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const cmd = e.target.dataset.cmd;
        this.handleCommand(cmd);
      });
    });
  }

  toggleListening() {
    if (this.isListening) {
      this.stopListening();
    } else {
      this.startListening();
    }
  }

  startListening() {
    this.isListening = true;
    this.micBtn.classList.add('listening');
    this.addMessage('JARVIS', 'Listening...', 'jarvis');
    
    if (this.recognition) {
      this.recognition.start();
      this.recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        this.addMessage('You', text, 'user');
        this.processCommand(text);
      };
      this.recognition.onerror = () => this.stopListening();
      this.recognition.onend = () => this.stopListening();
    } else {
      this.addMessage('JARVIS', 'Speech recognition not supported', 'jarvis');
      this.stopListening();
    }
  }

  stopListening() {
    this.isListening = false;
    this.micBtn.classList.remove('listening');
    if (this.recognition) this.recognition.stop();
  }

  sendMessage() {
    const text = this.userInput.value.trim();
    if (!text) return;
    
    this.userInput.value = '';
    this.addMessage('You', text, 'user');
    this.processCommand(text);
  }

  async processCommand(text) {
    this.addTypingIndicator();
    
    // Quick commands
    if (text.toLowerCase().includes('time')) {
      this.say(`The time is ${new Date().toLocaleTimeString()}`);
      return;
    }
    if (text.toLowerCase().includes('date')) {
      this.say(`Today is ${new Date().toLocaleDateString()}`);
      return;
    }
    
    // App mocks
    if (text.toLowerCase().includes('chrome')) {
      window.open('https://google.com', '_blank');
      this.say('Opening Chrome');
      return;
    }
    if (text.toLowerCase().includes('youtube') || text.toLowerCase().includes('yt')) {
      window.open('https://youtube.com', '_blank');
      this.say('Opening YouTube');
      return;
    }
    if (text.toLowerCase().includes('search')) {
      const query = text.toLowerCase().replace(/search/gi, '').trim();
      window.open(`https://google.com/search?q=${encodeURIComponent(query)}`, '_blank');
      this.say(`Searching for ${query}`);
      return;
    }
    
    // Volume mock
    if (text.toLowerCase().includes('volume up') || text.toLowerCase().includes('louder')) {
      this.say('Volume increased');
      return;
    }
    if (text.toLowerCase().includes('volume down') || text.toLowerCase().includes('quieter')) {
      this.say('Volume decreased');
      return;
    }
    
    // Gemini AI via proxy
    try {
      const response = await fetch(GEMINI_PROXY, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: `JARVIS Iron Man assistant: ${text}` }] }]
        })
      });
      const data = await response.json();
      const answer = data.candidates[0].content.parts[0].text;
      this.say(answer);
      this.addMessage('JARVIS', answer, 'jarvis');
    } catch (error) {
      this.say('Gemini API error. Check key.');
      this.addMessage('JARVIS', 'AI service temporarily unavailable.', 'jarvis');
    }
    
    this.removeTypingIndicator();
  }

  handleCommand(cmd) {
    const commands = {
      time: 'What is the time?',
      date: 'What is the date?',
      chrome: 'open chrome',
      youtube: 'open youtube',
      search: 'search something'
    };
    this.processCommand(commands[cmd]);
  }

  addMessage(sender, text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}-message`;
    msgDiv.innerHTML = `
      <div class="message-bubble">
        <strong>${sender}:</strong> ${this.typewriter(text)}
      </div>
    `;
    this.chatMessages.appendChild(msgDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message jarvis-message typing-indicator';
    typingDiv.innerHTML = `
      <div class="message-bubble typing">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        JARVIS is thinking...
      </div>
    `;
    this.chatMessages.appendChild(typingDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    this.typingElement = typingDiv;
  }

  removeTypingIndicator() {
    if (this.typingElement) {
      this.typingElement.remove();
      this.typingElement = null;
    }
  }

  typewriter(text) {
    return text.replace(/./g, (char) => `<span style="animation-delay: ${Math.random()*0.2}s;">${char}</span>`);
  }

  async say(text) {
    if (this.synth.speaking) {
      this.synth.cancel();
    }
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.1;
    utterance.pitch = 0.9;
    utterance.volume = 1;
    // Try to get more robotic voice
    const voices = this.synth.getVoices();
    const roboticVoice = voices.find(v => v.name.includes('Microsoft') || v.name.includes('David') || v.lang === 'en-US');
    if (roboticVoice) utterance.voice = roboticVoice;
    
    this.synth.speak(utterance);
    this.startVisualizer();
  }

  initVisualizer() {
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());
  }

  resizeCanvas() {
    this.waveCanvas.width = this.waveCanvas.offsetWidth * window.devicePixelRatio;
    this.waveCanvas.height = this.waveCanvas.offsetHeight * window.devicePixelRatio;
    this.waveCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  startVisualizer() {
    this.animateWaves();
  }

  animateWaves() {
    requestAnimationFrame(() => this.animateWaves());
    
    const centerX = this.waveCanvas.width / 2;
    const centerY = this.waveCanvas.height / 2;
    const radius = 100 + Math.sin(Date.now() * 0.01) * 20;
    
    this.waveCtx.save();
    this.waveCtx.translate(centerX, centerY);
    
    // Outer glow rings
    for (let i = 0; i < 3; i++) {
      const r = radius + i * 30;
      const alpha = 0.3 - i * 0.1;
      this.waveCtx.beginPath();
      this.waveCtx.arc(0, 0, r, 0, Math.PI * 2);
      this.waveCtx.strokeStyle = `rgba(0, 212, 255, ${alpha})`;
      this.waveCtx.lineWidth = 3;
      this.waveCtx.shadowBlur = 20;
      this.waveCtx.shadowColor = '#00d4ff';
      this.waveCtx.stroke();
    }
    
    // Wave bars
    const barCount = 32;
    const barWidth = 4;
    for (let i = 0; i < barCount; i++) {
      const angle = (i / barCount) * Math.PI * 2;
      const amp = 0.5 + Math.sin(Date.now() * 0.02 + i) * 0.5;
      const barHeight = radius * amp * 0.6;
      
      this.waveCtx.save();
      this.waveCtx.translate(0, 0);
      this.waveCtx.rotate(angle);
      
      const gradient = this.waveCtx.createLinearGradient(0, 0, 0, -barHeight);
      gradient.addColorStop(0, '#00d4ff');
      gradient.addColorStop(1, '#0099cc');
      
      this.waveCtx.fillStyle = gradient;
      this.waveCtx.shadowBlur = 15;
      this.waveCtx.shadowColor = '#00d4ff';
      this.waveCtx.fillRect(-barWidth/2, -barHeight, barWidth, barHeight);
      this.waveCtx.restore();
    }
    
    this.waveCtx.restore();
  }

  updateTime() {
    const now = new Date();
    this.timeDate.textContent = now.toLocaleDateString() + ' | ' + now.toLocaleTimeString();
    setTimeout(() => this.updateTime(), 1000);
  }

  animateStars() {
    const stars = document.querySelector('.stars');
    const rect = stars.getBoundingClientRect();
    stars.style.transform = `translate(${Math.sin(Date.now() * 0.0005) * 10}px, ${Math.cos(Date.now() * 0.0003) * 5}px)`;
  }
}

// Initialize when DOM loaded
document.addEventListener('DOMContentLoaded', () => {
  new JarvisUI();
});

