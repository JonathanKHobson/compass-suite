import { startCatalog } from "./catalog.js?v=phase3-ux7";
import { startNavigation } from "./site-nav.js";

document.documentElement.classList.add("js-enabled");

startNavigation();
startCatalog();
