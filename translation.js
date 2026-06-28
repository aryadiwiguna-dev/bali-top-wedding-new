(function () {
  function initTranslation() {
    if (typeof i18next === 'undefined') {
      setTimeout(initTranslation, 50);
      return;
    }

    const savedLang = localStorage.getItem('preferredLanguage') || 'id';

    i18next.init({
      lng: savedLang,
      resources: window.TRANSLATION_RESOURCES || {}
    }, function (err, t) {
      if (err) return console.error('i18n initialization failed', err);
      translatePage();
      setupLangSwitchers();
    });
  }

  function translatePage() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = i18next.t(key);
      if (translation && translation !== key) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          if (el.hasAttribute('placeholder')) {
            el.setAttribute('placeholder', translation);
          } else {
            el.value = translation;
          }
        } else {
          el.innerHTML = translation;
        }
      }
    });

    // Update switcher buttons
    const currentLang = i18next.language;
    const switchers = document.querySelectorAll('.lang-switch');
    switchers.forEach(sw => {
      const labelSpan = sw.querySelector('span');
      if (labelSpan) {
        labelSpan.innerText = currentLang === 'id' ? 'EN' : 'ID';
      }
      sw.setAttribute('title', currentLang === 'id' ? 'Switch to English' : 'Ubah ke Bahasa Indonesia');
    });
  }

  function setupLangSwitchers() {
    document.body.addEventListener('click', function (e) {
      const switcher = e.target.closest('.lang-switch');
      if (switcher) {
        e.preventDefault();
        const currentLang = i18next.language;
        const newLang = currentLang === 'id' ? 'en' : 'id';
        
        localStorage.setItem('preferredLanguage', newLang);
        i18next.changeLanguage(newLang, function (err) {
          if (!err) {
            translatePage();
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: newLang }));
          }
        });
      }
    });
  }

  // Run on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTranslation);
  } else {
    initTranslation();
  }
})();
