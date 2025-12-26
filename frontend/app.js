let healthWelcomeRemoved = false, counselorWelcomeRemoved = false, currentSearchType = 'all';

function formatMessageContent(text) {
  if (!text) return '';
  
  // Convert line breaks to HTML
  let formatted = text
    .replace(/\n\n+/g, '</p><p>')
    .replace(/\n/g, '<br>');
  
  // Format bullet points (- item)
  formatted = formatted.replace(/^- /gm, '• ');
  
  // Format numbered lists (1. item)
  formatted = formatted.replace(/^(\d+)\. /gm, '<strong>$1.</strong> ');
  
  // Format bold text (**text**)
  formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Format italic text (*text*)
  formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  
  // Wrap in paragraph if not already wrapped
  if (!formatted.includes('<p>')) {
    formatted = '<p>' + formatted + '</p>';
  } else {
    formatted = '<p>' + formatted + '</p>';
  }
  
  return formatted;
}

function toggleHealthChat() {
  const chatWindow = document.getElementById('health-chat-window');
  chatWindow.classList.toggle('hidden');
  if (!chatWindow.classList.contains('hidden')) document.getElementById("health-user-input").focus();
}

function toggleCounselorChat() {
  const chatWindow = document.getElementById('counselor-chat-window');
  chatWindow.classList.toggle('hidden');
  if (!chatWindow.classList.contains('hidden')) document.getElementById("counselor-user-input").focus();
}

function openChat(mode = 'health') {
  if (mode === 'counselor') {
    document.getElementById('counselor-chat-window').classList.remove('hidden');
    setTimeout(() => document.getElementById("counselor-user-input").focus(), 100);
  } else {
    document.getElementById('health-chat-window').classList.remove('hidden');
    setTimeout(() => document.getElementById("health-user-input").focus(), 100);
  }
}

async function sendHealthMessage() {
  const input = document.getElementById("health-user-input"), 
    chatBox = document.getElementById("health-chat-box"),
    sendButton = document.getElementById("health-send-button"), 
    loadingIndicator = document.getElementById("health-loading-indicator");
  const userMessage = input.value.trim();
  if (!userMessage) return;

  if (!healthWelcomeRemoved) {
    const welcomeMsg = chatBox.querySelector('.welcome-message');
    if (welcomeMsg) { welcomeMsg.remove(); healthWelcomeRemoved = true; }
  }

  const userMessageDiv = document.createElement('div');
  userMessageDiv.className = 'message user';
  userMessageDiv.innerHTML = `<div class="message-content">${escapeHtml(userMessage)}</div>`;
  chatBox.appendChild(userMessageDiv);
  input.value = "";
  sendButton.disabled = true;
  loadingIndicator.classList.remove('hidden');
  scrollToBottom('health');

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    loadingIndicator.classList.add('hidden');
    const botMessageDiv = document.createElement('div');
    botMessageDiv.className = 'message bot';
    const formattedContent = formatMessageContent(data.reply);
    botMessageDiv.innerHTML = `<div class="message-content">${formattedContent}</div>`;
    chatBox.appendChild(botMessageDiv);
    scrollToBottom('health');
  } catch (error) {
    loadingIndicator.classList.add('hidden');
    const errorMessageDiv = document.createElement('div');
    errorMessageDiv.className = 'message bot';
    errorMessageDiv.innerHTML = `<div class="message-content">Sorry, I encountered an error. Please make sure the backend server is running on http://localhost:8000</div>`;
    chatBox.appendChild(errorMessageDiv);
    console.error('Error:', error);
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
}

async function sendCounselorMessage() {
  const input = document.getElementById("counselor-user-input"), 
    chatBox = document.getElementById("counselor-chat-box"),
    sendButton = document.getElementById("counselor-send-button"), 
    loadingIndicator = document.getElementById("counselor-loading-indicator");
  const userMessage = input.value.trim();
  if (!userMessage) return;

  if (!counselorWelcomeRemoved) {
    const welcomeMsg = chatBox.querySelector('.welcome-message');
    if (welcomeMsg) { welcomeMsg.remove(); counselorWelcomeRemoved = true; }
  }

  const userMessageDiv = document.createElement('div');
  userMessageDiv.className = 'message user';
  userMessageDiv.innerHTML = `<div class="message-content">${escapeHtml(userMessage)}</div>`;
  chatBox.appendChild(userMessageDiv);
  input.value = "";
  sendButton.disabled = true;
  loadingIndicator.classList.remove('hidden');
  scrollToBottom('counselor');

  try {
    const response = await fetch("http://localhost:8000/counselor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    loadingIndicator.classList.add('hidden');
    const botMessageDiv = document.createElement('div');
    botMessageDiv.className = 'message bot';
    const formattedContent = formatMessageContent(data.reply);
    botMessageDiv.innerHTML = `<div class="message-content">${formattedContent}</div>`;
    chatBox.appendChild(botMessageDiv);
    scrollToBottom('counselor');
  } catch (error) {
    loadingIndicator.classList.add('hidden');
    const errorMessageDiv = document.createElement('div');
    errorMessageDiv.className = 'message bot';
    errorMessageDiv.innerHTML = `<div class="message-content">Sorry, I encountered an error. Please make sure the backend server is running on http://localhost:8000</div>`;
    chatBox.appendChild(errorMessageDiv);
    console.error('Error:', error);
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function scrollToBottom(chatType = 'health') {
  const boxId = chatType === 'counselor' ? 'counselor-chat-box' : 'health-chat-box';
  const chatBox = document.getElementById(boxId);
  if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('navToggle'), navMenu = document.getElementById('navMenu');
  if (navToggle) navToggle.addEventListener('click', () => navMenu.classList.toggle('active'));
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => navMenu.classList.remove('active'));
  });

  // Health chat input
  const healthInput = document.getElementById("health-user-input");
  if (healthInput) healthInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendHealthMessage(); }
  });

  // Counselor chat input
  const counselorInput = document.getElementById("counselor-user-input");
  if (counselorInput) counselorInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendCounselorMessage(); }
  });

  const nearmeInput = document.getElementById('nearme-search-input');
  if (nearmeInput) nearmeInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); searchNearMe(); }
  });
});

function getCurrentLocation(type = 'nearme') {
  const input = document.getElementById('nearme-search-input');
  if (!input || !navigator.geolocation) { alert('Geolocation is not supported.'); return; }
  input.value = 'Getting location...';
  input.disabled = true;
  navigator.geolocation.getCurrentPosition(
    (position) => {
      input.value = `${position.coords.latitude}, ${position.coords.longitude}`;
      input.disabled = false;
      searchNearMe();
    },
    () => { input.value = ''; input.disabled = false; alert('Unable to retrieve your location.'); }
  );
}

function switchSearchTab(type) {
  currentSearchType = type;
  document.querySelectorAll('.search-tab').forEach(tab => tab.classList.remove('active'));
  document.getElementById(`tab-${type}`).classList.add('active');
  const input = document.getElementById('nearme-search-input');
  if (input && input.value.trim()) searchNearMe();
}

function searchNearMe() {
  const input = document.getElementById('nearme-search-input'), location = input.value.trim(),
    resultsContainer = document.getElementById('nearme-results');
  if (!location) { alert('Please enter a location or use your current location.'); return; }
  
  resultsContainer.innerHTML = `<div class="nearme-loading"><i class="fas fa-spinner"></i><p>Searching for healthcare facilities near you...</p></div>`;
  
  try {
    fetch("http://localhost:8000/api/search-nearby", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        location: location, 
        search_type: currentSearchType,
        radius: 5000
      })
    })
    .then(r => r.json())
    .then(data => {
      if (data.success && data.results && data.results.length > 0) {
        displayNearMeResults(data.results);
      } else {
        resultsContainer.innerHTML = `<div class="nearme-placeholder"><i class="fas fa-search"></i><p>${data.error || 'No healthcare facilities found in this area.'}</p></div>`;
      }
    })
    .catch(err => {
      resultsContainer.innerHTML = `<div class="nearme-placeholder"><i class="fas fa-exclamation-circle"></i><p>Error searching nearby locations. Make sure the backend server is running.</p></div>`;
      console.error('Error:', err);
    });
  } catch (err) {
    resultsContainer.innerHTML = `<div class="nearme-placeholder"><i class="fas fa-exclamation-circle"></i><p>Error: ${err.message}</p></div>`;
  }
}

function displayNearMeResults(results) {
  const resultsContainer = document.getElementById('nearme-results');
  if (results.length === 0) {
    resultsContainer.innerHTML = `<div class="nearme-placeholder"><i class="fas fa-search"></i><p>No healthcare facilities found in this area.</p></div>`;
    return;
  }
  const resultsList = document.createElement('div');
  resultsList.className = 'nearme-list';
  results.forEach(item => {
    const card = document.createElement('div');
    if (item.type === 'pharmacy') {
      card.className = 'pharmacy-card';
      card.innerHTML = `<div class="pharmacy-card-header"><div><div class="pharmacy-name">${escapeHtml(item.name)}</div></div><div class="pharmacy-distance">${escapeHtml(item.distance)}</div></div><div class="pharmacy-info"><div class="pharmacy-info-item"><i class="fas fa-map-marker-alt"></i><span>${escapeHtml(item.address)}</span></div><div class="pharmacy-info-item"><i class="fas fa-phone"></i><span>${item.phone !== 'N/A' ? escapeHtml(item.phone) : 'Phone not available'}</span></div><div class="pharmacy-info-item"><i class="fas fa-clock"></i><span>${escapeHtml(item.hours)}</span></div></div><div class="pharmacy-actions"><button class="pharmacy-btn pharmacy-btn-primary" onclick="openGoogleMaps(${item.latitude}, ${item.longitude})"><i class="fas fa-directions"></i> Get Directions</button>${item.phone !== 'N/A' ? `<button class="pharmacy-btn pharmacy-btn-secondary" onclick="callPharmacy('${escapeHtml(item.phone)}')"><i class="fas fa-phone"></i> Call</button>` : ''}</div>`;
    } else if (item.type === 'hospital') {
      card.className = 'hospital-card';
      card.innerHTML = `<div class="hospital-card-header"><div><div class="hospital-name">${escapeHtml(item.name)}</div></div><div class="hospital-distance">${escapeHtml(item.distance)}</div></div><div class="hospital-info"><div class="hospital-info-item"><i class="fas fa-map-marker-alt"></i><span>${escapeHtml(item.address)}</span></div><div class="hospital-info-item"><i class="fas fa-phone"></i><span>${item.phone !== 'N/A' ? escapeHtml(item.phone) : 'Phone not available'}</span></div><div class="hospital-info-item"><i class="fas fa-clock"></i><span>${escapeHtml(item.hours)}</span></div>${item.website ? `<div class="hospital-info-item"><i class="fas fa-globe"></i><span><a href="${escapeHtml(item.website)}" target="_blank">${escapeHtml(item.website)}</a></span></div>` : ''}</div><div class="hospital-actions"><button class="hospital-btn hospital-btn-primary" onclick="openGoogleMaps(${item.latitude}, ${item.longitude})"><i class="fas fa-directions"></i> Get Directions</button>${item.phone !== 'N/A' ? `<button class="hospital-btn hospital-btn-secondary" onclick="callPharmacy('${escapeHtml(item.phone)}')"><i class="fas fa-phone"></i> Call</button>` : ''}</div>`;
    }
    resultsList.appendChild(card);
  });
  resultsContainer.innerHTML = '';
  resultsContainer.appendChild(resultsList);
}

function openGoogleMaps(lat, lon) {
  window.open(`https://www.google.com/maps/@${lat},${lon},15z`, '_blank');
}

function getDirections(address) {
  fetch("http://localhost:8000/api/get-directions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ address: address })
  })
  .then(r => r.json())
  .then(data => { if (data.success) window.open(data.url, '_blank'); })
  .catch(e => console.error('Error:', e));
}

function callPharmacy(phone) {
  window.location.href = `tel:${phone}`;
}