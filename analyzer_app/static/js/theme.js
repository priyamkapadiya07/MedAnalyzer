// static/js/theme.js

document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const toggle = document.getElementById("theme-toggle");

  if (!toggle) return;

  const icon = toggle.querySelector("i");

  // Load saved theme
  const currentTheme = localStorage.getItem("theme");
  if (currentTheme === "dark") {
    body.classList.add("bg-dark", "text-white");
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
    toggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
  }

  // Toggle on click
  toggle.addEventListener("click", () => {
    body.classList.toggle("bg-dark");
    body.classList.toggle("text-white");

    const isDark = body.classList.contains("bg-dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    icon.classList.toggle("fa-moon");
    icon.classList.toggle("fa-sun");
    toggle.innerHTML = isDark
      ? '<i class="fas fa-sun"></i> Light Mode'
      : '<i class="fas fa-moon"></i> Dark Mode';
  });
});
