const form = document.getElementById('weather-form');
const cityInput = document.getElementById('city');
const dateInput = document.getElementById('date');
const resultCard = document.getElementById('result-card');
const errorMsg = document.getElementById('error-msg');
const spinner = document.getElementById('spinner');
const citySuggestions = document.getElementById('city-suggestions');

let lastCityQuery = '';
let citySuggestTimeout = null;

cityInput.addEventListener('input', function () {
    const query = cityInput.value.trim();
    if (query.length < 2) {
        citySuggestions.innerHTML = '';
        return;
    }
    if (citySuggestTimeout) clearTimeout(citySuggestTimeout);
    citySuggestTimeout = setTimeout(async () => {
        lastCityQuery = query;
        try {
            const res = await fetch(`/api/city-suggest?query=${encodeURIComponent(query)}`);
            if (!res.ok) throw new Error('City suggest error');
            const data = await res.json();
            if (cityInput.value.trim() !== lastCityQuery) return; // Prevent race
            citySuggestions.innerHTML = '';
            data.forEach(city => {
                const option = document.createElement('option');
                option.value = `${city.name}, ${city.country}`;
                citySuggestions.appendChild(option);
            });
        } catch (err) {
            citySuggestions.innerHTML = '';
        }
    }, 200);
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resultCard.style.display = 'none';
    errorMsg.style.display = 'none';
    spinner.style.display = 'block';
    const city = cityInput.value.trim();
    const date = dateInput.value;
    if (!city || !date) {
        spinner.style.display = 'none';
        return;
    }
    const btn = document.getElementById('get-weather-btn');
    btn.disabled = true;
    btn.textContent = 'Loading...';
    try {
        const url = `/api/weather-stats?city=${encodeURIComponent(city)}&date=${date}`;
        const res = await fetch(url);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'API error');
        document.getElementById('result-city').textContent = data.city;
        document.getElementById('result-date').textContent = data.date;
        document.getElementById('result-pred').textContent = data.predicted_tavg;
        document.getElementById('result-avg7d').textContent = data.avg_tavg_7d;
        document.getElementById('result-type').textContent = data.is_forecast ? (data.is_ml_forecast ? 'Predicted by ML model' : 'Forecasted value') : 'Historical/statistical value';
        document.getElementById('result-type').className = data.is_forecast ? (data.is_ml_forecast ? 'result-type forecast' : 'result-type forecast') : 'result-type historical';
        resultCard.style.display = 'block';
    } catch (err) {
        errorMsg.textContent = err.message === 'Failed to fetch' ? 'Could not connect to server. Please try again.' : err.message;
        errorMsg.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Get Weather';
        spinner.style.display = 'none';
    }
}); 