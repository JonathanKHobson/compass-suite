export function startNavigation() {
  const button = document.querySelector("[data-menu-toggle]");
  const nav = document.querySelector("[data-site-nav]");
  if (!button || !nav) return;

  button.addEventListener("click", () => {
    const open = nav.dataset.open !== "true";
    nav.dataset.open = String(open);
    button.setAttribute("aria-expanded", String(open));
    button.textContent = open ? "Close" : "Menu";
  });

  nav.addEventListener("click", (event) => {
    if (!(event.target instanceof HTMLAnchorElement) || window.innerWidth > 768) return;
    nav.dataset.open = "false";
    button.setAttribute("aria-expanded", "false");
    button.textContent = "Menu";
  });
}
