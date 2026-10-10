/* Reversible GitHub Pages forwarding for published Working Tools HTML routes. */
(function () {
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
