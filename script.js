async function shortenUrl() {
    const url = document.getElementById('url').value;
    const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ original_url: url })
    });

    const result = await response.json();
    document.getElementById('result').innerHTML = `Shortened URL: <a href="http://${result.new_url}" target="_blank">${result.new_url}</a>`;
}

async function getStats() {
    const url = document.getElementById('stats-url').value;
    const response = await fetch('http://localhost:8000/stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ original_url: url })
    });

    if (response.status === 404) {
        document.getElementById('stats').innerHTML = "<p>Please register the URL first.</p>";
    } else {
        const stats = await response.json();
        document.getElementById('stats').innerHTML = `
            <p>Original URL: <a href=${stats.original_url}>${stats.original_url}</a></p>

            <p>Shortened URL: <a href=http://${stats.new_url}>http://${stats.new_url}</a></p>

            <p>Created At: 
                <p class="inner-stat">${stats.craeted_at}</p>
            </p>

            <p>Clicks: <p class="inner-stat"> ${stats.clicks}</p></p>
        `;
    }
}
