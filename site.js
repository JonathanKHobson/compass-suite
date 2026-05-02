(function () {
  const tabs = Array.from(document.querySelectorAll('[role="tab"][data-tab-target]'));
  const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));

  function showTab(targetId, updateHash) {
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

    if (updateHash) {
      history.replaceState(null, '', `#${selectedId}`);
    }
  }

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

  document.querySelectorAll('[data-download-url][data-learn-url]').forEach((link) => {
    link.addEventListener('click', () => {
      const learnUrl = link.dataset.learnUrl;
      if (!learnUrl) {
        return;
      }
      window.open(learnUrl, '_blank', 'noopener');
    });
  });
}());
