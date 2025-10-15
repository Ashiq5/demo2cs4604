// Minimal enhancements for the Movies page
document.addEventListener("DOMContentLoaded", () => {
  const movieList = document.querySelector("main ul");
  if (!movieList) return; // Only run on the movies page

  const items = Array.from(movieList.querySelectorAll("li"));

  // Extract dates from "(YYYY-MM-DD)" in each list item and tag them as data-date
  const dateSet = new Set();
  items.forEach((li) => {
    const m = li.textContent.match(/\((\d{4}-\d{2}-\d{2})\)/);
    if (m) {
      li.dataset.date = m[1];
      dateSet.add(m[1]);
    }
  });

  // Build a simple "Filter by date" dropdown above the list
  if (dateSet.size > 0) {
    const container = document.createElement("div");
    container.style.margin = "0 0 12px 0";

    const label = document.createElement("label");
    label.textContent = "Filter by date: ";
    label.style.fontWeight = "bold";
    label.style.marginRight = "8px";

    const select = document.createElement("select");
    const allOpt = document.createElement("option");
    allOpt.value = "";
    allOpt.textContent = "All dates";
    select.appendChild(allOpt);

    Array.from(dateSet).sort().forEach((d) => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = d;
      select.appendChild(opt);
    });

    select.addEventListener("change", () => {
      const chosen = select.value;
      items.forEach((li) => {
        li.style.display = !chosen || li.dataset.date === chosen ? "" : "none";
      });
    });

    container.appendChild(label);
    container.appendChild(select);
    movieList.parentNode.insertBefore(container, movieList);
  }

  // Prevent double-submit on reserve forms (gives quick UX feedback)
  movieList.addEventListener("submit", (e) => {
    const btn = e.target.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Reserving...";
    }
  });
});
