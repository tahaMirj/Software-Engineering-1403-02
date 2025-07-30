document.addEventListener("DOMContentLoaded", function () {
  const profileBtn = document.getElementById("profileBtn");
  const dropdownMenu = document.getElementById("dropdownMenu");

  profileBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    dropdownMenu.classList.toggle("show");
    // Update aria-expanded for accessibility
    const expanded = profileBtn.getAttribute("aria-expanded") === "true";
    profileBtn.setAttribute("aria-expanded", String(!expanded));
  });

  // Close dropdown if clicked outside
  document.addEventListener("click", function (e) {
    if (!profileBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
      dropdownMenu.classList.remove("show");
      profileBtn.setAttribute("aria-expanded", "false");
    }
  });
});

  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.querySelector('.notification-btn');
    const dropdown = document.querySelector('.notification-dropdown');

    if (btn && dropdown) {
      btn.addEventListener('click', function () {
        dropdown.classList.toggle('show');
      });
    }
  });

