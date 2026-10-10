import { startCatalog } from "./catalog.js?v=phase3-ux6";
import { startNavigation } from "./site-nav.js";

document.documentElement.classList.add("js-enabled");

startNavigation();
startCatalog();
