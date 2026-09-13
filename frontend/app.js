/**
 * VoiceShield-AI — Frontend Application Logic
 * Real-Time Audio Streaming, WebSockets, Canvas Visualizer, & Blockchain Forensics
 */

let audioContext = null;
let mediaStream = null;
let analyserNode = null;
let scriptProcessor = null;
let websocket = null;
let isRecording = false;
let animationFrameId = null;

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
    initVisualizerCanvas();
    setupWebSocket();
    setInterval(refreshStats, 4000);
});

// Switch Dashboard Tabs
function switchTab(tabId) {
    const tabs = ['live-monitor', 'file-forensics', 'blockchain-ledger', 'incidents-log', 'voice-vault'];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab-${t}`);
        const content = document.getElementById(`tab-content-${t}`);
        if (btn && content) {
            if (t === tabId) {
                btn.classList.add('active-tab');
                btn.classList.remove('text-slate-400');
                content.classList.remove('hidden');
            } else {
                btn.classList.remove('active-tab');
                btn.classList.add('text-slate-400');
                content.classList.add('hidden');
            }
        }
    });

    if (tabId === 'blockchain-ledger') fetchBlockchainLedger();
    if (tabId === 'incidents-log') fetchIncidents();
    if (tabId === 'voice-vault') fetchVoiceProfiles();
}

// Fetch Real-Time Stats
async function refreshStats() {
    try {
        const res = await fetch('/api/stats');
        const json = await res.json();
        if (json.status === 'success') {
            const data = json.data;
            document.getElementById('stat-total-scans').innerText = data.total_scans;
            document.getElementById('stat-threats-blocked').innerText = data.threats_blocked;
            document.getElementById('stat-verified-calls').innerText = data.verified_calls;
            document.getElementById('stat-blockchain-blocks').innerText = data.blockchain_blocks_sealed;
            document.getElementById('stat-latency').innerText = `${data.avg_detection_latency_ms} ms`;
        }
    } catch (err) {
        console.warn('Stats fetch offline:', err);
    }
}

async function initDashboard() {
    await refreshStats();
    await fetchIncidents();
    await fetchBlockchainLedger();
    await fetchVoiceProfiles();
}

// WebSocket Setup
function setupWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/stream-audio`;

    try {
        websocket = new WebSocket(wsUrl);

        websocket.onopen = () => {
            const el = document.getElementById('connection-status');
            if (el) {
                el.innerText = 'SHIELD ONLINE';
                el.className = 'text-[11px] font-mono font-medium text-emerald-400';
            }
        };

        websocket.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.type === 'DETECTION_RESULT') {
                updateThreatDashboard(msg.data);
            }
        };

        websocket.onclose = () => {
            const el = document.getElementById('connection-status');
            if (el) {
                el.innerText = 'OFFLINE (RECONNECTING)';
                el.className = 'text-[11px] font-mono font-medium text-amber-400';
            }
            setTimeout(setupWebSocket, 3000);
        };
    } catch (e) {
        console.warn("WebSocket init error", e);
    }
}

// Toggle Browser Microphone for Real-Time Streaming
async function toggleMicrophone() {
    const btn = document.getElementById('btn-toggle-mic');
    const micText = document.getElementById('mic-text');
    const micIcon = document.getElementById('mic-icon');

    if (!isRecording) {
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
            mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });

            const source = audioContext.createMediaStreamSource(mediaStream);
            analyserNode = audioContext.createAnalyser();
            analyserNode.fftSize = 512;
            source.connect(analyserNode);

            // Buffer audio chunks and stream via WebSocket every 500ms
            scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
            let chunkBuffer = [];

            scriptProcessor.onaudioprocess = (e) => {
                const inputData = e.inputBuffer.getChannelData(0);
                chunkBuffer.push(...inputData);

                // When 8000 samples (~500ms at 16kHz) accumulated, send to backend
                if (chunkBuffer.length >= 8000) {
                    if (websocket && websocket.readyState === WebSocket.OPEN) {
                        websocket.send(JSON.stringify({
                            type: 'AUDIO_CHUNK',
                            samples: Array.from(chunkBuffer)
                        }));
                    }
                    chunkBuffer = [];
                }
            };

            source.connect(scriptProcessor);
            scriptProcessor.connect(audioContext.destination);

            isRecording = true;
            btn.className = 'px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-slate-100 font-bold text-xs transition-all flex items-center space-x-2 shadow-lg shadow-rose-600/30 animate-pulse';
            micText.innerText = 'Stop Stream';
            micIcon.innerText = '⏹️';

            drawVisualizer();
        } catch (err) {
            alert('Microphone access denied or not supported: ' + err.message);
        }
    } else {
        // Stop recording
        if (scriptProcessor) scriptProcessor.disconnect();
        if (mediaStream) mediaStream.getTracks().forEach(t => t.stop());
        if (audioContext) audioContext.close();

        isRecording = false;
        btn.className = 'px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold text-xs transition-all flex items-center space-x-2 shadow-lg shadow-cyan-600/20';
        micText.innerText = 'Start Live Mic';
        micIcon.innerText = '🎤';
    }
}

// Update Real-Time Threat Meter & Forensics
function updateThreatDashboard(result) {
    const score = result.confidence_score || 0;
    const classification = result.classification || 'UNKNOWN';
    const gauge = document.getElementById('gauge-container');
    const scoreEl = document.getElementById('gauge-score');
    const labelEl = document.getElementById('gauge-label');
    const alertBox = document.getElementById('alert-box');
    const alertTitle = document.getElementById('alert-title');
    const alertAction = document.getElementById('alert-action');
    const alertDesc = document.getElementById('alert-desc');
    const xaiList = document.getElementById('xai-reasons-list');

    scoreEl.innerText = `${score.toFixed(1)}%`;
    gauge.classList.remove('gauge-safe', 'gauge-warning', 'gauge-danger');

    if (classification === 'CLONED_ATTACK' || score >= 75.0) {
        gauge.classList.add('gauge-danger');
        labelEl.innerText = 'CLONED ATTACK';
        labelEl.className = 'text-[11px] font-bold uppercase tracking-widest text-rose-400 mt-1';
        alertBox.className = 'p-3.5 rounded-xl bg-rose-950/60 border border-rose-800 text-left';
        alertTitle.innerText = '⚠️ VOICE CLONING IMPERSONATION DETECTED';
        alertTitle.className = 'text-xs font-bold text-rose-300';
        alertAction.innerText = 'INTERCEPT TRIGGERED';
        alertAction.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-rose-900 text-rose-200 font-bold';
        alertDesc.innerText = 'High-frequency vocoder artifacts and non-biological pitch stability identified. Call blocked and evidence sealed to blockchain.';
    } else if (classification === 'SUSPICIOUS_VOICE' || score >= 45.0) {
        gauge.classList.add('gauge-warning');
        labelEl.innerText = 'SUSPICIOUS';
        labelEl.className = 'text-[11px] font-bold uppercase tracking-widest text-amber-400 mt-1';
        alertBox.className = 'p-3.5 rounded-xl bg-amber-950/60 border border-amber-800 text-left';
        alertTitle.innerText = '⚠️ POTENTIAL SYNTHETIC MODULATION';
        alertTitle.className = 'text-xs font-bold text-amber-300';
        alertAction.innerText = 'OTP CHALLENGE PROMPT';
        alertAction.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-amber-900 text-amber-200 font-bold';
        alertDesc.innerText = 'Acoustic anomalies detected. Initiating biological liveness secondary challenge.';
    } else {
        gauge.classList.add('gauge-safe');
        labelEl.innerText = 'AUTHENTIC HUMAN';
        labelEl.className = 'text-[11px] font-bold uppercase tracking-widest text-emerald-400 mt-1';
        alertBox.className = 'p-3.5 rounded-xl bg-emerald-950/60 border border-emerald-800 text-left';
        alertTitle.innerText = '✓ VERIFIED AUTHENTIC HUMAN VOICE';
        alertTitle.className = 'text-xs font-bold text-emerald-300';
        alertAction.innerText = 'STREAM ALLOWED';
        alertAction.className = 'text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-900 text-emerald-200 font-bold';
        alertDesc.innerText = 'Natural involuntary vocal fold jitter and warm biological harmonics verified.';
    }

    // Update acoustic sub-metrics
    const feats = result.forensics?.acoustic_features || {};
    if (feats.pitch_jitter_pct !== undefined) document.getElementById('live-jitter').innerText = `${feats.pitch_jitter_pct} %`;
    if (feats.amplitude_shimmer_pct !== undefined) document.getElementById('live-shimmer').innerText = `${feats.amplitude_shimmer_pct} %`;
    if (feats.high_freq_energy_ratio !== undefined) document.getElementById('live-hf-ratio').innerText = feats.high_freq_energy_ratio;
    if (feats.spectral_flatness !== undefined) document.getElementById('live-flatness').innerText = feats.spectral_flatness;

    // Update XAI Diagnostic breakdown
    const anomalies = result.forensics?.detected_anomalies || [];
    if (anomalies.length > 0) {
        xaiList.innerHTML = anomalies.map(a => `
            <li class="flex items-start space-x-1.5 text-rose-300">
                <span class="text-rose-500">›</span>
                <span>${a}</span>
            </li>
        `).join('');
    } else {
        xaiList.innerHTML = `
            <li class="flex items-start space-x-1.5 text-emerald-400">
                <span class="text-emerald-500">✓</span>
                <span>Natural vocal respiration and pitch micro-perturbations within standard biological bounds.</span>
            </li>
        `;
    }

    refreshStats();
}

// 1-Click Live Test Sample Runner for Hackathon Demos
async function runSampleTest(sampleFilename, label) {
    try {
        const audioUrl = `/uploads/${sampleFilename}`;
        const audioPlayer = document.getElementById('audio-playback');
        audioPlayer.src = audioUrl;
        audioPlayer.play().catch(e => console.log('Audio autoplay prevented'));

        // Fetch sample file as blob and send to analyze-file endpoint
        const fileRes = await fetch(audioUrl);
        const blob = await fileRes.blob();
        const formData = new FormData();
        formData.append('file', blob, sampleFilename);
        formData.append('caller_id', `Live Demo: ${label}`);

        const scanRes = await fetch('/api/analyze-file', {
            method: 'POST',
            body: formData
        });
        const scanData = await scanRes.json();
        if (scanData.status === 'success') {
            updateThreatDashboard(scanData.result);
            fetchIncidents();
            fetchBlockchainLedger();
        }
    } catch (err) {
        alert('Error executing sample simulation: ' + err.message);
    }
}

// Handle File Upload for Tab 2
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('caller_id', `Uploaded File: ${file.name}`);

    try {
        const res = await fetch('/api/analyze-file', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (data.status === 'success') {
            const r = data.result;
            document.getElementById('file-scan-placeholder').classList.add('hidden');
            document.getElementById('file-scan-result-content').classList.remove('hidden');
            document.getElementById('file-scan-time').innerText = new Date().toLocaleTimeString();
            
            const classEl = document.getElementById('file-result-classification');
            const badgeEl = document.getElementById('file-result-badge');
            classEl.innerText = `${r.classification} (${r.confidence_score}%)`;

            if (r.classification === 'CLONED_ATTACK') {
                badgeEl.innerText = 'HIGH RISK BLOCKED';
                badgeEl.className = 'text-xs font-mono font-bold px-2.5 py-1 rounded-full bg-rose-950 text-rose-400 border border-rose-800';
            } else {
                badgeEl.innerText = 'AUTHENTIC SAFE';
                badgeEl.className = 'text-xs font-mono font-bold px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800';
            }

            document.getElementById('file-result-hash').innerText = r.audio_hash;
            document.getElementById('file-result-tx').innerText = r.blockchain_tx || 'SEALED_ON_CHAIN';
            document.getElementById('btn-download-forensic-report').href = `/api/export-report/${r.incident_id}`;

            fetchIncidents();
            fetchBlockchainLedger();
        }
    } catch (err) {
        alert('File forensic scan failed: ' + err.message);
    }
}

// Fetch and Render Blockchain Ledger
async function fetchBlockchainLedger() {
    try {
        const res = await fetch('/api/blockchain');
        const json = await res.json();
        if (json.status === 'success') {
            const tbody = document.getElementById('blockchain-table-body');
            if (!tbody) return;

            tbody.innerHTML = json.blocks.map(b => `
                <tr class="hover:bg-slate-900/60 transition-colors">
                    <td class="p-3 font-bold text-sky-400">#${b.block_index}</td>
                    <td class="p-3 text-slate-400">${b.created_at}</td>
                    <td class="p-3 text-cyan-400 font-mono text-[10px]">${b.hash.substring(0, 16)}...${b.hash.substring(56)}</td>
                    <td class="p-3 text-slate-500 font-mono text-[10px]">${b.previous_hash.substring(0, 12)}...</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">
                            ${b.data?.classification || (b.data?.genesis ? 'GENESIS_BLOCK' : 'EVIDENCE_SEAL')}
                        </span>
                    </td>
                    <td class="p-3 text-purple-400">${b.nonce}</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.warn('Blockchain fetch offline:', err);
    }
}

// Verify Cryptographic Chain Integrity
async function verifyChainIntegrity() {
    try {
        const res = await fetch('/api/blockchain/verify');
        const json = await res.json();
        const banner = document.getElementById('chain-verify-banner');
        const msg = document.getElementById('chain-verify-msg');

        if (json.status === 'success' && json.verification.valid) {
            banner.classList.remove('hidden');
            msg.innerText = `✓ Cryptographic Audit Passed: ${json.verification.total_blocks} Blocks Verified Tamper-Proof (Latest Hash: ${json.verification.latest_block_hash.substring(0, 16)}...)`;
        } else {
            banner.classList.remove('hidden');
            banner.className = 'p-3.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-300 text-xs font-mono';
            msg.innerText = `⚠️ Tampering Detected: ${json.verification.reason}`;
        }
    } catch (err) {
        alert('Verification failed: ' + err.message);
    }
}

// Fetch and Render Incidents
async function fetchIncidents() {
    try {
        const res = await fetch('/api/incidents');
        const json = await res.json();
        if (json.status === 'success') {
            const badge = document.getElementById('badge-incident-count');
            if (badge) badge.innerText = json.count;

            const tbody = document.getElementById('incidents-table-body');
            if (!tbody) return;

            if (json.data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-500">No security incidents logged yet. Run a live test!</td></tr>`;
                return;
            }

            tbody.innerHTML = json.data.map(inc => `
                <tr class="hover:bg-slate-900/60 transition-colors">
                    <td class="p-3 font-mono font-bold text-cyan-400">${inc.incident_id}</td>
                    <td class="p-3 text-slate-400 text-[11px]">${inc.created_at}</td>
                    <td class="p-3 font-medium">${inc.caller_id}</td>
                    <td class="p-3">
                        <span class="px-2.5 py-1 rounded-full text-[10px] font-bold ${inc.classification === 'CLONED_ATTACK' ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-emerald-950 text-emerald-400 border border-emerald-800'}">
                            ${inc.classification}
                        </span>
                    </td>
                    <td class="p-3 font-mono font-bold ${inc.confidence_score > 70 ? 'text-rose-400' : 'text-emerald-400'}">${inc.confidence_score}%</td>
                    <td class="p-3"><span class="text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">${inc.status}</span></td>
                    <td class="p-3">
                        <a href="/api/export-report/${inc.incident_id}" target="_blank" class="text-cyan-400 hover:text-cyan-300 font-semibold text-[11px] underline">
                            Forensic Report ↗
                        </a>
                    </td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.warn('Incidents fetch offline:', err);
    }
}

// Enroll Speaker Profile
async function handleEnrollSpeaker(event) {
    event.preventDefault();
    const name = document.getElementById('enroll-name').value;
    const role = document.getElementById('enroll-role').value;
    const audioInput = document.getElementById('enroll-audio');

    if (!audioInput.files[0]) {
        alert('Please select a voice baseline audio file.');
        return;
    }

    const formData = new FormData();
    formData.append('speaker_name', name);
    formData.append('role', role);
    formData.append('file', audioInput.files[0]);

    try {
        const res = await fetch('/api/enroll-voice', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (data.status === 'success') {
            alert(`Voice baseline for ${name} successfully enrolled!`);
            document.getElementById('enroll-name').value = '';
            document.getElementById('enroll-role').value = '';
            document.getElementById('enroll-audio').value = '';
            fetchVoiceProfiles();
        }
    } catch (err) {
        alert('Enrollment failed: ' + err.message);
    }
}

// Fetch Voice Profiles
async function fetchVoiceProfiles() {
    try {
        const res = await fetch('/api/voice-profiles');
        const json = await res.json();
        if (json.status === 'success') {
            const listEl = document.getElementById('enrolled-speakers-list');
            if (!listEl) return;

            if (json.profiles.length === 0) {
                listEl.innerHTML = `<div class="p-4 text-center text-xs text-slate-500 bg-slate-950/40 rounded-xl border border-slate-800">No voice profiles enrolled. Enroll baseline above.</div>`;
                return;
            }

            listEl.innerHTML = json.profiles.map(p => `
                <div class="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-center justify-between">
                    <div>
                        <div class="text-xs font-bold text-slate-200">${p.speaker_name}</div>
                        <div class="text-[11px] text-slate-400">${p.role} • Enrolled: ${p.enrolled_at}</div>
                    </div>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                        BIO-LOCKED
                    </span>
                </div>
            `).join('');
        }
    } catch (err) {
        console.warn('Voice profiles offline:', err);
    }
}

// Canvas Waveform & Oscilloscope Visualizer
function initVisualizerCanvas() {
    const canvas = document.getElementById('visualizer-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = 140;

    // Draw initial idle grid
    ctx.fillStyle = '#020617';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();
}

function drawVisualizer() {
    if (!isRecording || !analyserNode) return;

    const canvas = document.getElementById('visualizer-canvas');
    const ctx = canvas.getContext('2d');
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function render() {
        if (!isRecording) return;
        animationFrameId = requestAnimationFrame(render);
        analyserNode.getByteTimeDomainData(dataArray);

        ctx.fillStyle = 'rgba(2, 6, 23, 0.3)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.lineWidth = 2;
        ctx.strokeStyle = '#06b6d4';
        ctx.beginPath();

        const sliceWidth = canvas.width * 1.0 / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const v = dataArray[i] / 128.0;
            const y = v * (canvas.height / 2);

            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
            x += sliceWidth;
        }

        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
    }

    render();
}
