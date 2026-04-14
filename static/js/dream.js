document.addEventListener('DOMContentLoaded', () => {
    // Dynamic displays for the sliders
    const coresInput = document.getElementById('cores');
    const ramInput = document.getElementById('ram');
    const vramInput = document.getElementById('vram');
    
    document.getElementById('val-cores').textContent = coresInput.value;
    document.getElementById('val-ram').textContent = ramInput.value;
    document.getElementById('val-vram').textContent = vramInput.value;

    coresInput.addEventListener('input', (e) => document.getElementById('val-cores').textContent = e.target.value);
    ramInput.addEventListener('input', (e) => document.getElementById('val-ram').textContent = e.target.value);
    vramInput.addEventListener('input', (e) => document.getElementById('val-vram').textContent = e.target.value);

    // Predict Logic
    const gameInput = document.getElementById('game-input');
    const gameList = document.getElementById('game-list');
    const predictBtn = document.getElementById('predict-btn');
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('result-section');
    const resultBadge = document.getElementById('result-badge');
    const predictionText = document.getElementById('prediction-text');
    const bottleneckSection = document.getElementById('bottleneck-section');
    const bottleneckList = document.getElementById('bottleneck-list');

    // Fetch initial options
    fetch('/api/options')
        .then(response => response.json())
        .then(data => {
            // Populate Games
            data.games.sort().forEach(game => {
                const opt = document.createElement('option');
                opt.value = game;
                gameList.appendChild(opt);
            });
        })
        .catch(err => {
            gameInput.placeholder = "Error loading games";
        });

    // Handle Prediction
    predictBtn.addEventListener('click', () => {
        const gameName = gameInput.value;

        if (!gameName) {
            alert("Please type and select a game.");
            return;
        }

        // UI States
        predictBtn.disabled = true;
        resultSection.classList.add('hidden');
        bottleneckSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        fetch('/api/predict_dream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cores: coresInput.value,
                ram: ramInput.value,
                vram: vramInput.value,
                game_name: gameName
            })
        })
        .then(response => response.json())
        .then(data => {
            loadingSection.classList.add('hidden');
            predictBtn.disabled = false;

            if (data.error) {
                alert(data.error);
                return;
            }

            // Display Results
            resultSection.classList.remove('hidden');
            predictionText.textContent = data.prediction;

            // Reset classes
            resultBadge.className = 'result-badge';
            
            // Map code to style
            if (data.prediction_code === 2) {
                resultBadge.classList.add('optimal');
            } else if (data.prediction_code === 1) {
                resultBadge.classList.add('playable');
            } else {
                resultBadge.classList.add('cannot');
            }

            // Display Bottlenecks
            bottleneckList.innerHTML = '';
            if (data.bottlenecks && data.bottlenecks.length > 0) {
                bottleneckSection.classList.remove('hidden');
                data.bottlenecks.forEach(bn => {
                    const li = document.createElement('li');
                    let cleanFeature = bn.feature.replace('_', ' ');
                    li.innerHTML = `<span><strong>${cleanFeature}</strong> (Current: ${bn.value}) is bottlenecking this custom build.</span>`;
                    bottleneckList.appendChild(li);
                });
            }
        })
        .catch(err => {
            loadingSection.classList.add('hidden');
            predictBtn.disabled = false;
            alert("An error occurred during prediction.");
            console.error(err);
        });
    });
});
