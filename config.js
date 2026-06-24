// Bali Top Wedding — Centralized Configuration File
// Edit the numbers below to update WhatsApp contacts across the entire website instantly.

window.BTW_CONFIG = {
  // WhatsApp Contact Details
  // IMPORTANT: For 'number', use international format without '+' or spaces (e.g. "628123456789")
  whatsapp: {
    ika: {
      number: "6281237495930",
      label: "Ika",
      display: "081237495930"
    },
    suci: {
      number: "6282266316766",
      label: "Suci",
      display: "082266316766"
    },
    yoga: {
      number: "6281238490222",
      label: "Yoga",
      display: "081238490222"
    }
  }
};

// Automatic DOM Update for WhatsApp Links on Page Load
document.addEventListener("DOMContentLoaded", () => {
  const updateWaElements = () => {
    const waElements = document.querySelectorAll("[data-wa]");
    waElements.forEach(el => {
      const target = el.getAttribute("data-wa");
      const config = window.BTW_CONFIG.whatsapp[target];
      if (config) {
        // If it's a link (<a>), update its href
        if (el.tagName === "A" || el.hasAttribute("href")) {
          el.href = `https://wa.me/${config.number}`;
        }
        
        // Check if we should preserve the original text content (e.g. for buttons)
        const keepText = el.classList.contains("btn-bubble") || el.getAttribute("data-wa-keep-text") === "true";
        
        if (!keepText) {
          // Update the display text based on attributes
          const isSimple = el.getAttribute("data-wa-simple") === "true";
          if (isSimple) {
            el.textContent = config.display;
          } else {
            el.textContent = `Contact ${config.label}`;
          }
        }
      }
    });
  };

  updateWaElements();
});
