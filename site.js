(function () {
  /* ── Progress bar ─────────────────────────────── */
  const bar = document.getElementById('progress-bar');
  if (bar) {
    window.addEventListener('scroll', () => {
      const scrolled = document.documentElement.scrollTop;
      const total = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const pct = total > 0 ? Math.round((scrolled / total) * 100) : 0;
      bar.style.width = pct + '%';
      bar.setAttribute('aria-valuenow', pct);
    }, { passive: true });
  }

  /* ── Mobile navigation ────────────────────────── */
  document.documentElement.classList.add('js-enabled');

  function wireMenuToggle(toggleSelector, menuSelector, openClass) {
    const toggle = document.querySelector(toggleSelector);
    const menu = document.querySelector(menuSelector);
    if (!toggle || !menu) return null;

    function setOpen(isOpen) {
      toggle.setAttribute('aria-expanded', String(isOpen));
      menu.classList.toggle(openClass, isOpen);
    }

    toggle.addEventListener('click', (event) => {
      event.stopPropagation();
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    menu.addEventListener('click', (event) => {
      if (event.target.closest('a, button')) {
        setOpen(false);
      }
    });

    document.addEventListener('click', (event) => {
      if (!menu.classList.contains(openClass)) return;
      if (menu.contains(event.target) || toggle.contains(event.target)) return;
      setOpen(false);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    });

    return { setOpen };
  }

  wireMenuToggle('.site-nav-toggle', '.site-nav-links', 'is-open');
  wireMenuToggle('.section-nav-toggle', '.tab-nav', 'is-open');

  /* ── Tab system ───────────────────────────────── */
  const tabs = Array.from(document.querySelectorAll('[role="tab"][data-tab-target]'));
  const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));
  const sectionLabel = document.querySelector('.section-nav-current');
  const liveRegion = document.createElement('div');
  liveRegion.className = 'sr-only';
  liveRegion.setAttribute('aria-live', 'polite');
  liveRegion.setAttribute('aria-atomic', 'true');
  document.body.append(liveRegion);

  function updateSectionLabel() {
    const selected = tabs.find((tab) => tab.getAttribute('aria-selected') === 'true');
    if (sectionLabel && selected) {
      sectionLabel.textContent = selected.textContent.trim();
    }
  }

  function showTab(targetId, updateHash) {
    if (!tabs.length || !panels.length) return;
    const selectedTab = tabs.find((tab) => tab.dataset.tabTarget === targetId) || tabs[0];
    const selectedId = selectedTab.dataset.tabTarget;

    tabs.forEach((tab) => {
      const isSelected = tab === selectedTab;
      tab.setAttribute('aria-selected', String(isSelected));
      tab.tabIndex = isSelected ? 0 : -1;
    });

    panels.forEach((panel) => {
      panel.hidden = panel.id !== selectedId;
    });
    updateSectionLabel();

    if (updateHash) {
      history.replaceState(null, '', `#${selectedId}`);
    }
  }

  if (tabs.length && panels.length) {
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => showTab(tab.dataset.tabTarget, true));
      tab.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
          return;
        }
        event.preventDefault();
        let nextIndex = index;
        if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') nextIndex = 0;
        if (event.key === 'End') nextIndex = tabs.length - 1;
        tabs[nextIndex].focus();
        showTab(tabs[nextIndex].dataset.tabTarget, true);
      });
    });

    const initialTab = location.hash ? location.hash.slice(1) : 'get-started';
    showTab(initialTab, false);

    document.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const targetId = link.getAttribute('href').slice(1);
        if (tabs.some((tab) => tab.dataset.tabTarget === targetId)) {
          event.preventDefault();
          showTab(targetId, true);
          document.getElementById(`tab-${targetId}`)?.focus();
        }
      });
    });
  }

  document.querySelectorAll('[data-download-url][data-learn-url]').forEach((link) => {
    link.addEventListener('click', () => {
      const learnUrl = link.dataset.learnUrl;
      if (!learnUrl) return;
      window.open(learnUrl, '_blank', 'noopener');
      const originalText = link.dataset.originalText || link.textContent.trim();
      link.dataset.originalText = originalText;
      link.textContent = 'Download started. Guide opened.';
      liveRegion.textContent = 'Download started. Product guide opened in a new tab.';
      window.setTimeout(() => {
        link.textContent = link.dataset.originalText || originalText;
      }, 2200);
    });
  });
}());
