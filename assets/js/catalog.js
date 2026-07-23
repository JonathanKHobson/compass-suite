const JOB_LABELS = {
  all: "All work",
  write: "Write",
  research: "Research",
  design: "Design",
  build: "Build",
  career: "Career",
  teach: "Teach",
  table: "Run a game"
};

const COMPASS_JOBS = {
  "critical-compass": ["research", "write"],
  "prompt-compass": ["write", "build"],
  "ux-heuristics-compass": ["design", "build"],
  "job-application-compass": ["career", "write"]
};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function normalizeCompass(product) {
  const hasDownloads = product.downloads?.some((download) => download.availability === "available");
  return {
    id: product.id,
    name: product.name,
    kind: "Compass project",
    access: hasDownloads ? "public-download" : "public-site",
    jobs: COMPASS_JOBS[product.id] || [],
    tagline: product.tagline,
    description: product.description,
    href: product.learn_more_url?.startsWith("http") ? product.learn_more_url : undefined,
    action: product.learn_more_url?.startsWith("http") ? `Open ${product.name}` : undefined,
    downloads: product.downloads || [],
    maturity: product.maturity,
    status: product.status
  };
}

function createSkillDetails(skills) {
  const details = document.createElement("details");
  const summary = element("summary", "", `${skills.length} included ${skills.length === 1 ? "skill" : "skills"}`);
  const list = element("ul", "skill-list");
  skills.forEach((skill) => {
    const item = document.createElement("li");
    item.append(element("code", "", skill));
    list.append(item);
  });
  details.append(summary, list);
  return details;
}

function createDownloadDetails(downloads) {
  const available = downloads.filter((download) => download.availability === "available");
  if (!available.length) return null;

  const details = document.createElement("details");
  const summary = element("summary", "", `${available.length} verified ${available.length === 1 ? "download" : "downloads"}`);
  const list = element("ul", "download-list");

  available.forEach((download) => {
    const item = document.createElement("li");
    const link = element("a", "", download.label);
    link.href = download.url;
    link.setAttribute("download", "");
    const audience = element("small", "", download.recommended_for || download.filename);
    item.append(link, audience);
    if (download.checksum) item.append(element("code", "", `SHA-256 ${download.checksum}`));
    list.append(item);
  });

  details.append(summary, list);
  return details;
}

function createRow(item, accessLabels) {
  const row = element("article", "library-row");
  row.dataset.access = item.access;

  const meta = element("div", "library-meta");
  meta.append(element("p", "library-kind", item.kind));
  const statusText = item.status ? `${item.status} · ${accessLabels[item.access]}` : accessLabels[item.access];
  const status = element("span", "status-label", statusText);
  status.dataset.access = item.access;
  meta.append(status);

  const main = element("div", "library-main");
  main.append(element("h3", "", item.name));
  if (item.tagline) main.append(element("p", "library-tagline", item.tagline));
  main.append(element("p", "library-description", item.description));

  const side = element("div", "library-side");
  if (item.href && item.action) {
    const link = element("a", "button button-primary", item.action);
    link.href = item.href;
    side.append(link);
  }

  if (item.skills?.length) side.append(createSkillDetails(item.skills));
  if (item.downloads?.length) {
    const downloadDetails = createDownloadDetails(item.downloads);
    if (downloadDetails) side.append(downloadDetails);
  }

  row.append(meta, main, side);
  return row;
}

export async function startCatalog() {
  const list = document.querySelector("[data-library-list]");
  const search = document.querySelector("[data-library-search]");
  const filters = [...document.querySelectorAll("[data-library-filter]")];
  const status = document.querySelector("[data-library-status]");
  const empty = document.querySelector("[data-library-empty]");
  const error = document.querySelector("[data-library-error]");
  if (!list || !search || !status) return;

  const initialHash = window.location.hash;
  const state = { job: "all", query: "" };

  try {
    const [libraryResponse, compassResponse] = await Promise.all([
      fetch("data/tool-library.json"),
      fetch("suite-manifest.json")
    ]);
    if (!libraryResponse.ok || !compassResponse.ok) throw new Error("Catalog source unavailable");
    const library = await libraryResponse.json();
    const compass = await compassResponse.json();
    const publicCompasses = compass.products
      .filter((product) => product.downloads?.some((download) => download.availability === "available"))
      .map(normalizeCompass);
    const items = [...publicCompasses, ...library.items];

    function render() {
      const query = state.query.trim().toLowerCase();
      const matches = items.filter((item) => {
        const jobMatch = state.job === "all" || item.jobs.includes(state.job);
        const haystack = [item.name, item.kind, item.tagline, item.description, ...(item.skills || [])]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();
        return jobMatch && (!query || haystack.includes(query));
      });

      list.replaceChildren(...matches.map((item) => createRow(item, library.access_labels)));
      status.textContent = `${matches.length} ${matches.length === 1 ? "tool" : "tools"} shown · ${JOB_LABELS[state.job]}`;
      empty.hidden = matches.length !== 0;
    }

    search.addEventListener("input", () => {
      state.query = search.value;
      render();
    });

    filters.forEach((button) => {
      button.addEventListener("click", () => {
        state.job = button.dataset.libraryFilter;
        filters.forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
        render();
      });
    });

    document.querySelectorAll("[data-job-link]").forEach((link) => {
      link.addEventListener("click", () => {
        const job = link.dataset.jobLink;
        const button = filters.find((candidate) => candidate.dataset.libraryFilter === job);
        if (button) button.click();
      });
    });

    render();

    if (initialHash) {
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          document.querySelector(initialHash)?.scrollIntoView();
        });
      });
    }
  } catch (catalogError) {
    console.error(catalogError);
    error.hidden = false;
    status.textContent = "Library unavailable";
  }
}
