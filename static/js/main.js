document.addEventListener('DOMContentLoaded', () => {
    const laptopInput = document.getElementById('laptop-input');
    const gameInput = document.getElementById('game-input');
    const laptopList = document.getElementById('laptop-list');
    const gameList = document.getElementById('game-list');
    const predictBtn = document.getElementById('predict-btn');
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('result-section');
    const resultBadge = document.getElementById('result-badge');
    const predictionText = document.getElementById('prediction-text');
    const bottleneckSection = document.getElementById('bottleneck-section');
    const bottleneckList = document.getElementById('bottleneck-list');
    
    let allLaptops = [];

    // Fetch initial options
    fetch('/api/options')
        .then(response => response.json())
        .then(data => {
            allLaptops = data.laptops;
            
            // Populate Laptops
            data.laptops.forEach(laptop => {
                const opt = document.createElement('option');
                opt.value = laptop.name;
                laptopList.appendChild(opt);
            });

            // Populate Games
            // Sort alphabetically for UX
            data.games.sort().forEach(game => {
                const opt = document.createElement('option');
                opt.value = game;
                gameList.appendChild(opt);
            });
        })
        .catch(err => {
            console.error("Failed to load options:", err);
            laptopInput.placeholder = "Error loading laptops";
            gameInput.placeholder = "Error loading games";
        });

    // Handle Prediction
    predictBtn.addEventListener('click', () => {
        const laptopName = laptopInput.value;
        const gameName = gameInput.value;

        if (!laptopName || !gameName) {
            alert("Please type and select both a laptop and a game.");
            return;
        }
        
        const selectedLaptop = allLaptops.find(l => l.name === laptopName);
        if (!selectedLaptop) {
            alert("Invalid laptop selected. Please choose one from the list.");
            return;
        }
        
        const laptopId = selectedLaptop.id;

        // UI States
        predictBtn.disabled = true;
        resultSection.classList.add('hidden');
        bottleneckSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                laptop_id: laptopId,
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
            
            // Map code to style (0: Cannot Run, 1: Playable, 2: Optimal)
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
                    // Clean up feature names
                    let cleanFeature = bn.feature.replace('_', ' ');
                    li.innerHTML = `<span><strong>${cleanFeature}</strong> (Current: ${bn.value}) is heavily bottlenecking performance.</span>`;
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
