async function shortenUrl() {
  const url = document.getElementById("url").value;
  const response = await fetch("http://localhost:8000/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ original_url: url }),
  });
  if (response.status === 422) {
    document.getElementById("result").innerHTML =
      "<p>Please enter a valid URL.</p>";
  } else {
    const result = await response.json();
    document.getElementById(
      "result"
    ).innerHTML = `Shortened URL: <a href="http://${result.new_url}" target="_blank">${result.new_url}</a>`;
  }
}

async function getStats() {
  const url = document.getElementById("stats-url").value;
  const response = await fetch("http://localhost:8000/stats", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ original_url: url }),
  });

  if (response.status === 404) {
    document.getElementById("stats").innerHTML =
      "<p>Please register the URL first.</p>";
    document.getElementById("charts").innerHTML = '';
  } else {
    const stats = await response.json();
    // Display URL info and clicks if present
    let urlInfoHtml = '';
    if (stats.original_url) {
      urlInfoHtml += `<p>Original URL: <a href="${stats.original_url}" target="_blank">${stats.original_url}</a></p>`;
    }
    if (stats.new_url) {
      urlInfoHtml += `<p>Shortened URL: <a href="http://localhost:8000/${stats.new_url}" target="_blank">http://localhost:8000/${stats.new_url}</a></p>`;
    }
    if (stats.craeted_at) {
      urlInfoHtml += `<p>Created At: <span class="inner-stat">${stats.craeted_at}</span></p>`;
    }
    if (typeof stats.clicks !== 'undefined') {
      urlInfoHtml += `<p>Clicks: <span class="inner-stat">${stats.clicks}</span></p>`;
    }
    let busyHours = stats.busy_hours ? stats.busy_hours.join(", ") : "N/A";
    urlInfoHtml += `<p><b>Busy Hours:</b> <span class="inner-stat">${busyHours}</span></p>`;
    document.getElementById("stats").innerHTML = urlInfoHtml;

    // Display charts
    let chartsHtml = '';
    chartsHtml += `<div class='chart-block'><h4>Device Distribution</h4><img src='${stats.device_chart}' alt='Device Distribution' style='max-width:400px;max-height:400px;width:100%;margin:10px;'></div>`;
    chartsHtml += `<div class='chart-block'><h4>OS Distribution</h4><img src='${stats.os_chart}' alt='OS Distribution' style='max-width:400px;max-height:400px;width:100%;margin:10px;'></div>`;
    chartsHtml += `<div class='chart-block'><h4>Browser Distribution</h4><img src='${stats.browser_chart}' alt='Browser Distribution' style='max-width:400px;max-height:400px;width:100%;margin:10px;'></div>`;
    chartsHtml += `<div class='chart-block'><h4>Hourly Distribution</h4><img src='${stats.hour_chart}' alt='Hourly Distribution' style='max-width:600px;max-height:400px;width:100%;margin:10px;'></div>`;
    chartsHtml += `<div class='chart-block'><h4>Day Distribution</h4><img src='${stats.day_chart}' alt='Day Distribution' style='max-width:600px;max-height:400px;width:100%;margin:10px;'></div>`;
    chartsHtml += `<div class='chart-block'><h4>Month Distribution</h4><img src='${stats.month_chart}' alt='Month Distribution' style='max-width:600px;max-height:400px;width:100%;margin:10px;'></div>`;
    document.getElementById("charts").innerHTML = `<div class='charts-flex'>${chartsHtml}</div>`;
  }
}
