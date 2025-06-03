async function fetchInternships() {
    try {
        const response = await fetch('{{ url_for("get_internships") }}');
        const data = await response.json();
        if (response.ok) {
            return data;
        } else {
            console.error('Error fetching internships:', data.error);
            document.getElementById("internshipList").innerHTML = "<p>Error loading internships.</p>";
            return [];
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("internshipList").innerHTML = "<p>Error loading internships.</p>";
        return [];
    }
}

function loadInternships(data) {
    const list = document.getElementById("internshipList");
    list.innerHTML = data.length ? "" : "<p>No internships found.</p>";

    data.forEach(({ title, company, location, duration, stipend, category, startDate, postedDaysAgo }) => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <h3>${title}</h3>
            <p><strong>Company:</strong> ${company}</p>
            <p><span class="sticker">📍</span><strong>Location:</strong> ${location}</p>
            <p><span class="sticker">🧩</span><strong>Category:</strong> ${category}</p>
            <p><span class="sticker">⏳</span><strong>Duration:</strong> ${duration} month(s)</p>
            <p><span class="sticker">💰</span><strong>Stipend:</strong> ₹${stipend}/month</p>
            <p><span class="sticker">📅</span><strong>Start Date:</strong> ${startDate}</p>
            <p><span class="sticker">🕓</span><strong>Posted:</strong> ${postedDaysAgo} day(s) ago</p>
            <button class="apply-btn">Apply Now</button>
        `;
        list.appendChild(card);
    });

    setupApplyButtons();
}

function filterInternships() {
    const keyword = document.getElementById("search").value.toLowerCase();
    const location = document.getElementById("location").value;
    const duration = document.getElementById("duration").value;
    const stipend = document.getElementById("stipend").value;
    const category = document.getElementById("category").value;
    const sort = document.getElementById("sort").value;

    fetchInternships().then(internships => {
        let results = internships.filter(i =>
            (i.title.toLowerCase().includes(keyword) || i.company.toLowerCase().includes(keyword)) &&
            (location === "" || i.location === location) &&
            (duration === "" || i.duration === parseInt(duration)) &&
            (stipend === "" || i.stipend >= parseInt(stipend)) &&
            (category === "" || i.category === category)
        );

        if (sort === "stipend") {
            results.sort((a, b) => b.stipend - a.stipend);
        } else {
            results.sort((a, b) => a.postedDaysAgo - b.postedDaysAgo);
        }

        loadInternships(results);
    });
}

function setupApplyButtons() {
    const applyButtons = document.querySelectorAll('.apply-btn');
    applyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            alert("✅ Application Submitted!");
            btn.textContent = "Applied";
            btn.disabled = true;
            btn.style.backgroundColor = '#4caf50';
            btn.style.color = 'white';
        });
    });
}

window.onload = () => fetchInternships().then(loadInternships);