// Auto-switch API base (local vs production)
const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:10000/api" // match your Flask port
    : "https://food-recommender-web-tool.onrender.com/api";

// Show messages
function showMessage(elementId, message, type = "info") {
  const messageEl = document.getElementById(elementId);
  messageEl.textContent = message;
  messageEl.className = `message ${type}`;
  setTimeout(() => {
    messageEl.className = "message";
  }, 5000);
}

// Create User
document.getElementById("userForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const userData = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    cuisine_preference: document.getElementById("cuisine").value,
    spice_level: document.getElementById("spice").value,
    diet_type: document.getElementById("diet").value,
  };

  try {
    const response = await fetch(`${API_BASE}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      const user = await response.json();
      showMessage(
        "userMessage",
        `✓ Profile created! Your User ID: ${user.id}`,
        "success",
      );

      window.currentUserId = user.id;

      document.getElementById("welcomeMessage").classList.remove("hidden");
      document.getElementById("userName").textContent = user.name;
      document.getElementById("contentAfterProfile").classList.remove("hidden");

      setTimeout(() => {
        document
          .getElementById("welcomeMessage")
          .scrollIntoView({ behavior: "smooth" });
      }, 500);

      setTimeout(() => {
        const profileSection = document.getElementById("profileSection");
        profileSection.style.opacity = "0.5";
        profileSection.style.pointerEvents = "none";
      }, 1000);

      document.getElementById("userForm").reset();
    } else {
      const error = await response.json();
      showMessage(
        "userMessage",
        `✗ ${error.error || "Error creating profile"}`,
        "error",
      );
    }
  } catch (error) {
    showMessage("userMessage", `✗ Connection error: ${error.message}`, "error");
  }
});

// Get Recommendations
document
  .getElementById("recommendForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const userId = window.currentUserId;
    const topN = parseInt(document.getElementById("topN").value) || 3;

    if (!userId) {
      showMessage(
        "recommendMessage",
        "✗ Please create a profile first!",
        "error",
      );
      return;
    }

    try {
      const response = await fetch(
        `${API_BASE}/recommendations/${userId}?top_n=${topN}`,
      );

      if (response.ok) {
        const data = await response.json();
        const recommendations = data.recommendations || [];
        displayRecommendations(recommendations);

        showMessage(
          "recommendMessage",
          `✓ Found ${recommendations.length} recommendations!`,
          "success",
        );
      } else {
        const error = await response.json();
        showMessage(
          "recommendMessage",
          `✗ ${error.error || "User not found"}`,
          "error",
        );
      }
    } catch (error) {
      showMessage(
        "recommendMessage",
        `✗ Error fetching recommendations: ${error.message}`,
        "error",
      );
    }
  });

// Display Recommendations
function displayRecommendations(recommendations) {
  const container = document.getElementById("recommendationsList");

  if (!recommendations || recommendations.length === 0) {
    container.innerHTML =
      '<div class="empty-state"><p>No recommendations found</p></div>';
    return;
  }

  container.innerHTML = recommendations
    .map(
      (rec) => `
      <div class="recommendation-card">
        <h3>🍽️ ${rec.name}</h3>
        <p><strong>Cuisine:</strong> ${rec.cuisine}</p>
        <p><strong>Rating:</strong> ⭐ ${rec.rating.toFixed(1)}/5</p>
        <p><strong>Price:</strong> $${rec.price.toFixed(2)}</p>
        <p><strong>Tags:</strong> ${rec.tags ? rec.tags.map((tag) => `<span class="food-tag">${tag}</span>`).join("") : ""}</p>
        <span class="score-badge">Match Score: ${(rec.score * 10).toFixed(1)}%</span>
      </div>
    `,
    )
    .join("");
}

// Load Foods Catalog
document.getElementById("loadFoodsBtn").addEventListener("click", async () => {
  try {
    const response = await fetch(`${API_BASE}/foods`);

    if (response.ok) {
      const foods = await response.json();
      displayFoodsCatalog(foods);
    } else {
      showMessage("recommendMessage", "✗ Error loading foods", "error");
    }
  } catch (error) {
    showMessage("recommendMessage", `✗ Error: ${error.message}`, "error");
  }
});

// Display Foods Catalog
function displayFoodsCatalog(foods) {
  const container = document.getElementById("foodsList");

  if (!foods || foods.length === 0) {
    container.innerHTML =
      '<div class="empty-state"><p>No foods available</p></div>';
    return;
  }

  container.innerHTML = foods
    .map(
      (food) => `
      <div class="food-item">
        <h3>${food.name}</h3>
        <p><strong>${food.cuisine}</strong></p>
        <p class="food-rating">⭐ ${food.rating.toFixed(1)}/5</p>
        <p><strong>Price:</strong> $${food.price.toFixed(2)}</p>
        <div>${food.tags ? food.tags.map((tag) => `<span class="food-tag">${tag}</span>`).join("") : ""}</div>
      </div>
    `,
    )
    .join("");
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Food Recommender App loaded!");
});
