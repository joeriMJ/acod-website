// Formulieren sturen naar FORM_ENDPOINT (bv. Formspree) zodra dat ingevuld is.
// Zolang het leeg is, opent het formulier het mailprogramma met de ingevulde gegevens.
const FORM_ENDPOINT = "";

// Menu op kleine schermen
(function () {
  const btn = document.querySelector(".nav-toggle");
  const nav = document.getElementById("hoofdmenu");
  if (!btn || !nav) return;
  btn.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("open")) {
      nav.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
      btn.focus();
    }
  });
})();

// Vertrekbord: elke cel draait een paar keer en valt dan op zijn plaats
(function () {
  const flaps = document.querySelectorAll(".flap");
  if (!flaps.length) return;
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const chars = "ABCDEFGHIJKLMNOPRSTUVWXYZ";

  flaps.forEach((flap, row) => {
    const text = flap.textContent.trim();
    const width = Number(flap.dataset.width) || text.length;
    const target = text.padEnd(width, " ");
    flap.setAttribute("aria-label", text);
    flap.textContent = "";
    const cells = [...target].map((ch) => {
      const c = document.createElement("span");
      c.className = "c";
      c.setAttribute("aria-hidden", "true");
      c.textContent = still ? ch : " ";
      flap.appendChild(c);
      return { el: c, ch };
    });
    if (still) return;
    cells.forEach(({ el, ch }, i) => {
      if (ch === " ") return;
      let turns = 6 + ((i * 7 + row * 3) % 9);
      setTimeout(function tick() {
        if (turns-- <= 0) { el.textContent = ch; return; }
        el.textContent = chars[Math.floor(Math.random() * chars.length)];
        setTimeout(tick, 55);
      }, 250 + row * 180 + i * 25);
    });
  });
})();

// Formulieren
(function () {
  document.querySelectorAll("form[data-form]").forEach((form) => {
    const status = form.querySelector(".form-status");
    const show = (msg, isError) => {
      status.textContent = msg;
      status.classList.toggle("error", !!isError);
      status.hidden = false;
    };

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new FormData(form);

      if (!FORM_ENDPOINT) {
        const lines = [];
        for (const [key, value] of data) {
          if (String(value).trim()) lines.push(`${key}: ${value}`);
        }
        const subject = encodeURIComponent(form.dataset.subject || "Bericht via de website");
        const body = encodeURIComponent(lines.join("\n"));
        window.location.href = `mailto:${form.dataset.to}?subject=${subject}&body=${body}`;
        show("Je mailprogramma opent met je gegevens. Verstuur de mail daar om af te ronden.");
        return;
      }

      const button = form.querySelector("button[type=submit]");
      button.disabled = true;
      try {
        data.append("_onderwerp", form.dataset.subject || "");
        const res = await fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error(res.status);
        form.reset();
        show(form.dataset.done || "Verstuurd. We nemen snel contact met je op.");
      } catch {
        show(`Versturen lukte niet. Probeer opnieuw of mail naar ${form.dataset.to}.`, true);
      } finally {
        button.disabled = false;
      }
    });
  });
})();
