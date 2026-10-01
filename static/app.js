const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".panel");

tabs.forEach(tab => {
  tab.addEventListener("click", () => {
    tabs.forEach(t => t.classList.remove("active"));
    panels.forEach(p => p.classList.remove("active-panel"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active-panel");
    document.getElementById("result").classList.add("hidden");
  });
});

function showResult(data) {
  const result = document.getElementById("result");
  result.className = `result ${data.color}`;
  result.innerHTML = `
    <span class="badge ${data.color}">${data.level}</span>
    <div class="score">Risk indicator score: <strong>${data.score}/100</strong></div>
    <h3>Why?</h3>
    <ul>${data.indicators.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
    <h3>What should I do?</h3>
    <p>${escapeHtml(data.action)}</p>
  `;
  result.classList.remove("hidden");
  result.scrollIntoView({behavior: "smooth"});
}

async function checkMessage() {
  const message = document.getElementById("messageInput").value.trim();
  if (!message) return alert("Please enter a message.");
  const response = await fetch("/api/check-message", {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message})
  });
  const data = await response.json();
  response.ok ? showResult(data) : alert(data.error || "Something went wrong.");
}

async function checkUrl() {
  const url = document.getElementById("urlInput").value.trim();
  if (!url) return alert("Please enter a URL.");
  const response = await fetch("/api/check-url", {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({url})
  });
  const data = await response.json();
  response.ok ? showResult(data) : alert(data.error || "Something went wrong.");
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, char => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[char]));
}
