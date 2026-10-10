/* Preserve historical GitHub Pages paths while directing current-site legacy URLs to one archive doorway. */
(function () {
  const legacyRoutes = new Set([
    'critical-compass',
    'prompt-compass',
    'ux-heuristic-compass',
    'job-application-compass',
    'creative-writing-studio',
    'marketing-social-studio',
    'career-grants-studio',
    'ttrpg-gm-director',
    'ux-design-toolkit',
    'builder-tools',
    'humanizer'
  ]);

  if (location.hostname === 'working-tools.jkylehobson.chatgpt.site') {
    const route = location.pathname.split('/').filter(Boolean)[0];
    if (legacyRoutes.has(route)) {
      const destination = new URL('/legacy/', location.origin);
      destination.search = location.search;
      destination.hash = location.hash;
      location.replace(destination.href);
    }
    return;
  }

  if (location.hostname !== 'jonathankhobson.github.io') return;
  const parts = location.pathname.split('/');
  const repo = parts[1];
  if (!['compass-suite', 'critical-compass', 'prompt-compass', 'job-application-compass', 'ux-heuristic-compass', 'what-is-an-mcp'].includes(repo)) return;
  if (new URLSearchParams(location.search).get('_legacy') === '1') return;
  const suffix = parts.slice(2).join('/');
  const sitePrefix = repo === 'compass-suite' ? '/' : '/' + repo + '/';
  const destination = new URL(sitePrefix + suffix + location.search + location.hash,
    'https://working-tools.jkylehobson.chatgpt.site');
  location.replace(destination.href);
})();
