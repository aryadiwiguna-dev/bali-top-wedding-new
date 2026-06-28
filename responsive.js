(function () {
  function initMobileMenu() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelector('.navbar-links');
    if (!navbar || !navLinks) return;

    // Check if toggle already exists to avoid duplicates
    if (navbar.querySelector('.navbar-toggle')) return;

    // Create Hamburger Toggle Button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'navbar-toggle';
    toggleBtn.setAttribute('aria-label', 'Toggle Menu');
    toggleBtn.innerHTML = `
      <span></span>
      <span></span>
      <span></span>
    `;
    navbar.appendChild(toggleBtn);

    // Toggle menu visibility
    toggleBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      navbar.classList.toggle('menu-open');
    });

    // Close menu when clicking links (except dropdown trigger)
    const links = navLinks.querySelectorAll('.nav-item:not(.nav-dropdown > a)');
    links.forEach(link => {
      link.addEventListener('click', () => {
        navbar.classList.remove('menu-open');
        closeAllDropdowns();
      });
    });

    // Close menu when clicking language switcher
    const langSwitch = navLinks.querySelector('.lang-switch');
    if (langSwitch) {
      langSwitch.addEventListener('click', () => {
        navbar.classList.remove('menu-open');
        closeAllDropdowns();
      });
    }

    // Handle dropdown links on mobile (tap-to-expand)
    const dropdowns = navbar.querySelectorAll('.nav-dropdown');
    dropdowns.forEach(dropdown => {
      const triggerLink = dropdown.querySelector('a.nav-item');
      if (triggerLink) {
        triggerLink.addEventListener('click', function (e) {
          if (window.innerWidth <= 900) {
            if (!dropdown.classList.contains('dropdown-open')) {
              e.preventDefault();
              e.stopPropagation();
              closeAllDropdowns();
              dropdown.classList.add('dropdown-open');
            }
          }
        });
      }
    });

    function closeAllDropdowns() {
      dropdowns.forEach(d => d.classList.remove('dropdown-open'));
    }

    // Close menu or dropdowns when clicking outside
    document.addEventListener('click', function (e) {
      if (!navbar.contains(e.target)) {
        navbar.classList.remove('menu-open');
        closeAllDropdowns();
      }
    });

    // Handle window resizing
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) {
        navbar.classList.remove('menu-open');
        closeAllDropdowns();
      }
    });
  }

  // Run on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileMenu);
  } else {
    initMobileMenu();
  }
})();
