(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(pointer: fine)").matches;

  /* header state + mobile menu */
  const header = document.querySelector(".site-header");
  const onScroll = () => header && header.classList.toggle("is-scrolled", window.scrollY > 24);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const menuBtn = document.querySelector(".menu-btn");
  if (menuBtn) {
    menuBtn.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    document.querySelectorAll(".nav a").forEach((a) =>
      a.addEventListener("click", () => {
        document.body.classList.remove("menu-open");
        menuBtn.setAttribute("aria-expanded", "false");
      })
    );
  }

  /* blurred display type: the line nearest the pointer comes into focus */
  document.querySelectorAll("[data-focus]").forEach((block) => {
    const lines = [...block.querySelectorAll(".ln")];
    if (!lines.length) return;
    const set = (idx, strength = 1) => {
      lines.forEach((ln, i) => {
        const d = Math.abs(i - idx);
        const b = reduce ? 0 : Math.min(14, 1.2 + d * 5.5 * strength);
        ln.style.setProperty("--b", b.toFixed(1) + "px");
        ln.style.setProperty("--o", Math.max(0.28, 1 - d * 0.26).toFixed(2));
      });
    };
    let current = 0;
    set(current);
    if (reduce) return;

    if (finePointer) {
      window.addEventListener(
        "pointermove",
        (e) => {
          const r = block.getBoundingClientRect();
          if (e.clientY < r.top - 120 || e.clientY > r.bottom + 120) return;
          const rel = (e.clientY - r.top) / r.height;
          const idx = Math.max(0, Math.min(lines.length - 1, Math.round(rel * lines.length - 0.5)));
          if (idx !== current) { current = idx; set(idx); }
        },
        { passive: true }
      );
    } else {
      setInterval(() => { current = (current + 1) % lines.length; set(current); }, 2600);
    }
  });

  /* scramble text on hover */
  const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/_-+";
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const scramble = (el, done) => {
    if (reduce || el._busy) { if (done) done(); return; }
    const text = el.dataset.text || (el.dataset.text = el.textContent);
    el._busy = true;
    const glyphs = el.dataset.glyphs || GLYPHS;
    let frame = 0;
    const total = el.dataset.glyphs ? 34 : Math.min(26, 8 + text.length);
    const tick = () => {
      if (el.dataset.glyphs && frame % 2 && frame < total) { frame++; return requestAnimationFrame(tick); }
      const progress = frame / total;
      let out = "";
      for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        const settleAt = el.dataset.glyphs ? 0.55 + 0.45 * (i / text.length) : i / text.length;
        if (ch === " " || (el.dataset.glyphs && !el.dataset.glyphs.includes(ch)) || settleAt < progress) out += esc(ch);
        else out += `<span class="sc">${glyphs[(Math.random() * glyphs.length) | 0]}</span>`;
      }
      if (el.dataset.glyphs) el.innerHTML = out;
      else el.innerHTML = `<span class="scr-ghost" aria-hidden="true">${esc(text)}</span><span class="scr-live" aria-hidden="true">${out}</span>`;
      if (++frame <= total) requestAnimationFrame(tick);
      else { el.textContent = text; el._busy = false; if (done) done(); }
    };
    tick();
  };
  document.querySelectorAll("[data-scramble-trigger]").forEach((trigger) => {
    const target = trigger.querySelector("[data-scramble]");
    if (!target) return;
    trigger.addEventListener("mouseenter", () => scramble(target));
    trigger.addEventListener("focus", () => scramble(target));
  });

  /* stats: when the row scrolls into view, scramble each number in order */
  document.querySelectorAll(".stats").forEach((row) => {
    const nums = [...row.querySelectorAll(".stat [data-scramble]")];
    if (!nums.length || reduce || !("IntersectionObserver" in window)) return;
    nums.forEach((n) => n.closest(".stat").classList.add("is-waiting"));
    const run = (i) => {
      if (i >= nums.length) return;
      const stat = nums[i].closest(".stat");
      stat.classList.remove("is-waiting");
      scramble(nums[i], () => setTimeout(() => run(i + 1), 90));
    };
    const obs = new IntersectionObserver((entries) => {
      if (!entries.some((en) => en.isIntersecting)) return;
      obs.disconnect();
      setTimeout(() => run(0), 450);
    }, { threshold: 0.6, rootMargin: "0px 0px -10% 0px" });
    obs.observe(row);
  });

  /* pixel reveal on card images */
  const buildPix = (media) => {
    const cols = 12, rows = 9;
    const pix = document.createElement("div");
    pix.className = "pix";
    pix.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    pix.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const i = document.createElement("i");
        // sweep from bottom-left with noise, so it dissolves rather than wipes
        const bias = (c / cols) * 0.45 + ((rows - r) / rows) * 0.25;
        i.style.transitionDelay = (bias + Math.random() * 0.4).toFixed(2) + "s";
        pix.appendChild(i);
      }
    }
    media.appendChild(pix);
    return pix;
  };

  const io = "IntersectionObserver" in window
    ? new IntersectionObserver(
        (entries) => entries.forEach((en) => {
          if (!en.isIntersecting) return;
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }),
        { threshold: 0, rootMargin: "0px 0px -8% 0px" }
      )
    : null;

  document.querySelectorAll(".card-media").forEach((m) => {
    if (reduce || !io) return;
    io.observe(buildPix(m));
  });
  document.querySelectorAll(".reveal").forEach((el) => (io ? io.observe(el) : el.classList.add("is-in")));

  /* project filters */
  const filterBtns = document.querySelectorAll("[data-filter]");
  if (filterBtns.length) {
    const cards = document.querySelectorAll(".card[data-cat]");
    const count = document.querySelector("[data-count]");
    filterBtns.forEach((btn) =>
      btn.addEventListener("click", () => {
        const f = btn.dataset.filter;
        filterBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        let n = 0;
        cards.forEach((c) => {
          const show = f === "all" || c.dataset.cat === f;
          c.classList.toggle("is-hidden", !show);
          if (show) n++;
        });
        if (count) count.textContent = String(n).padStart(2, "0");
      })
    );
  }

  /* FIREFLIES — soft blue-white drifting particles behind the page */
  (() => {
    const cv = document.createElement("canvas");
    cv.className = "fireflies"; cv.setAttribute("aria-hidden", "true");
    document.body.prepend(cv);
    const ctx = cv.getContext("2d");
    let W = 0, H = 0, dpr = 1, flies = [], raf = 0, last = 0;
    const COLORS = ["176,196,222", "150,176,212", "128,160,204", "196,208,224"];
    const mouse = { x: -9999, y: -9999, on: false, t: 0, speed: 0 };
    window.addEventListener("pointermove", (e) => { if (e.pointerType === "mouse") { const now = performance.now(); const d = Math.hypot(e.clientX - mouse.x, e.clientY - mouse.y); if (mouse.on) mouse.speed = Math.min(1, d / 24); mouse.x = e.clientX; mouse.y = e.clientY; mouse.on = true; mouse.t = now; } }, { passive: true });
    document.addEventListener("pointerleave", () => { mouse.on = false; mouse.x = mouse.y = -9999; });
    window.addEventListener("blur", () => { mouse.on = false; });
    const make = () => {
      const depth = Math.random();                     // 0 = far (blurry, slow), 1 = near (sharp)
      return {
        x: Math.random() * W, y: Math.random() * H,
        r: 0.6 + Math.random() * 2.4,
        soft: 2 + (1 - depth) * 10,                     // blur radius
        vx: (Math.random() - 0.5) * (0.08 + depth * 0.18),
        vy: -0.03 - Math.random() * (0.06 + depth * 0.12),
        ph: Math.random() * Math.PI * 2, sp: 0.4 + Math.random() * 0.9,
        amp: 0.15 + Math.random() * 0.35,
        a: 0.12 + depth * 0.3, c: COLORS[(Math.random() * COLORS.length) | 0],
        dx: 0, dy: 0,
      };
    };
    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth; H = window.innerHeight;
      cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(46, Math.max(16, (W * H) / 38000)));
      while (flies.length < n) flies.push(make());
      flies.length = n;
    };
    const draw = (t) => {
      ctx.clearRect(0, 0, W, H);
      for (const f of flies) {
        const tw = 0.55 + 0.45 * Math.sin(t * 0.001 * f.sp + f.ph);   // twinkle
        const R = f.r + f.soft;
        const g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, R);
        g.addColorStop(0, `rgba(${f.c},${(f.a * tw).toFixed(3)})`);
        g.addColorStop(Math.min(0.9, f.r / R), `rgba(${f.c},${(f.a * tw * 0.55).toFixed(3)})`);
        g.addColorStop(1, `rgba(${f.c},0)`);
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(f.x, f.y, R, 0, Math.PI * 2); ctx.fill();
      }
    };
    const step = (t) => {
      const dt = Math.min(48, t - (last || t)); last = t;
      for (const f of flies) {
        // ripple: push away from the cursor like water, then ease back into drifting
        // moving cursor: dots scatter like water. resting cursor: dots are slowly drawn in and hover around it
        if (mouse.on) {
          const ddx = f.x - mouse.x, ddy = f.y - mouse.y, dist = Math.hypot(ddx, ddy) || 0.01;
          const idle = t - mouse.t;
          const stir = Math.max(0, 1 - idle / 180) * mouse.speed;
          if (stir > 0 && dist < 150) {
            const force = (1 - dist / 150) ** 2 * 0.55 * stir;
            f.dx += (ddx / dist) * force; f.dy += (ddy / dist) * force;
          }
          const pull = Math.min(1, Math.max(0, (idle - 350) / 900));   // eases in after the cursor rests
          const R = 460, ring = 26 + f.r * 16;
          if (pull > 0 && dist < R) {
            const k = (0.35 + 0.65 * (1 - dist / R)) * 0.05 * pull;
            const inward = dist > ring ? 1 : -0.6;                       // keep a soft halo, never collapse
            f.dx -= (ddx / dist) * k * inward * (dist > ring ? 1 : 2);
            f.dy -= (ddy / dist) * k * inward * (dist > ring ? 1 : 2);
            f.dx += (-ddy / dist) * k * 0.6; f.dy += (ddx / dist) * k * 0.6;  // gentle swirl
          }
        }
        f.dx *= 0.92; f.dy *= 0.92;
        f.x += (f.vx + Math.sin(t * 0.0006 * f.sp + f.ph) * f.amp * 0.3 + f.dx) * dt * 0.06;
        f.y += (f.vy + f.dy) * dt * 0.06;
        if (f.y < -20) { f.y = H + 20; f.x = Math.random() * W; }
        if (f.x < -20) f.x = W + 20; else if (f.x > W + 20) f.x = -20;
      }
      draw(t);
      raf = requestAnimationFrame(step);
    };
    resize();
    window.addEventListener("resize", resize, { passive: true });
    if (reduce) { draw(0); return; }
    raf = requestAnimationFrame(step);
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) { cancelAnimationFrame(raf); raf = 0; }
      else if (!raf) { last = 0; raf = requestAnimationFrame(step); }
    });
  })();

  /* SCRIBBLE CURSOR — a pencil-like dot that leaves a loose, fading hand-drawn trail */
  (() => {
    if (!finePointer || reduce) return;
    document.documentElement.classList.add("has-scribble");
    const cv = document.createElement("canvas");
    cv.className = "scribble"; cv.setAttribute("aria-hidden", "true");
    const dot = document.createElement("div");
    dot.className = "scribble-dot"; dot.setAttribute("aria-hidden", "true");
    dot.innerHTML = '<svg viewBox="0 0 60 60" aria-hidden="true"><path class="loop" d="M31 8c-9-1-21 5-22 17-2 13 9 26 22 25 12 0 21-9 21-21 0-10-8-18-19-19-6 0-11 2-14 5"/></svg>';
    document.body.append(cv, dot);
    const ctx = cv.getContext("2d");
    let W = 0, H = 0, dpr = 1;
    const resize = () => { dpr = Math.min(devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    resize(); addEventListener("resize", resize, { passive: true });

    const pts = [];                       // trail points
    let x = -100, y = -100, px = -100, py = -100, seen = false, raf = 0, hover = false, down = false;
    const LIFE = 520;                     // ms a stroke lingers
    const rnd = (a) => (Math.random() - 0.5) * a;

    addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse") return;
      x = e.clientX; y = e.clientY;
      if (!seen) { px = x; py = y; seen = true; dot.classList.add("on"); }
      const d = Math.hypot(x - px, y - py);
      // add a few jittered samples between frames so fast moves still read as a pencil line
      const steps = Math.min(6, Math.max(1, Math.round(d / 10)));
      for (let i = 1; i <= steps; i++) {
        const k = i / steps;
        pts.push({ x: px + (x - px) * k + rnd(1.6), y: py + (y - py) * k + rnd(1.6), t: performance.now(), w: 0.6 + Math.random() * 0.9 });
      }
      px = x; py = y;
      const el = e.target.closest && e.target.closest("a, button, [data-filter], .card, [role='button']");
      if (!!el !== hover) { hover = !!el; dot.classList.toggle("is-hover", hover); }
      if (!raf) raf = requestAnimationFrame(draw);
    }, { passive: true });
    addEventListener("pointerdown", () => { down = true; dot.classList.add("is-down"); });
    addEventListener("pointerup", () => { down = false; dot.classList.remove("is-down"); });
    document.addEventListener("pointerleave", () => { dot.classList.remove("on"); seen = false; });

    let dx = -100, dy = -100;
    const draw = () => {
      const now = performance.now();
      while (pts.length && now - pts[0].t > LIFE) pts.shift();
      if (pts.length > 140) pts.splice(0, pts.length - 140);
      ctx.clearRect(0, 0, W, H);
      // graphite stroke: two slightly offset passes with varying width and alpha
      for (let pass = 0; pass < 2; pass++) {
        for (let i = 1; i < pts.length; i++) {
          const a = pts[i - 1], b = pts[i];
          const age = (now - b.t) / LIFE, fade = Math.max(0, 1 - age);
          ctx.strokeStyle = pass ? `rgba(188,216,250,${(fade * 0.22).toFixed(3)})` : `rgba(233,242,252,${(fade * 0.55).toFixed(3)})`;
          ctx.lineWidth = (pass ? 2.2 : b.w) * (0.35 + fade * 0.65);
          ctx.lineCap = "round";
          ctx.beginPath();
          const o = pass ? 0.8 : 0;
          ctx.moveTo(a.x + o, a.y - o);
          ctx.quadraticCurveTo((a.x + b.x) / 2 + rnd(0.8), (a.y + b.y) / 2 + rnd(0.8), b.x + o, b.y - o);
          ctx.stroke();
        }
      }
      dx += (x - dx) * 0.45; dy += (y - dy) * 0.45;
      dot.style.transform = `translate3d(${dx}px, ${dy}px, 0)`;
      raf = pts.length || Math.hypot(x - dx, y - dy) > 0.3 ? requestAnimationFrame(draw) : 0;
    };
  })();

  /* THERMAL PAPER hover on work cards */
  (() => {
    const medias = document.querySelectorAll(".card-media");
    if (!medias.length) return;
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("width", "0"); svg.setAttribute("height", "0"); svg.setAttribute("aria-hidden", "true");
    svg.style.position = "absolute";
    const band = (v) => `<feFuncR type="discrete" tableValues="${v}"/><feFuncG type="discrete" tableValues="${v}"/><feFuncB type="discrete" tableValues="${v}"/>`;
    const lin = (s, i) => `<feFuncR type="linear" slope="${s}" intercept="${i}"/><feFuncG type="linear" slope="${s}" intercept="${i}"/><feFuncB type="linear" slope="${s}" intercept="${i}"/>`;
    svg.innerHTML =
      '<filter id="thermal-paper" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">' +
        '<feColorMatrix type="saturate" values="0" result="gray"/>' +
        '<feComponentTransfer in="gray" result="contrast">' + lin(1.25, 0.2) + '</feComponentTransfer>' +
        '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" seed="4" result="noise"/>' +
        '<feColorMatrix in="noise" type="saturate" values="0" result="grain"/>' +
        '<feComposite in="contrast" in2="grain" operator="arithmetic" k1="0" k2="1" k3="0.42" k4="-0.2" result="dither"/>' +
        '<feComponentTransfer in="dither" result="print">' + band("0 0.08 0.42 0.86 1 1") + '</feComponentTransfer>' +
        '<feTurbulence type="fractalNoise" baseFrequency="0.004 0.12" numOctaves="1" seed="9" result="streak"/>' +
        '<feColorMatrix in="streak" type="matrix" values="0 0 0 0 0.9  0 0 0 0 0.88  0 0 0 0 0.84  0.6 0 0 0 -0.34" result="fade"/>' +
        '<feComposite in="fade" in2="print" operator="over" result="aged"/>' +
        '<feColorMatrix in="aged" type="matrix" values="0.83 0 0 0 0.12  0.81 0 0 0 0.12  0.74 0 0 0 0.14  0 0 0 1 0"/>' +
      '</filter>';
    document.body.appendChild(svg);
    medias.forEach((m) => {
      const img = m.querySelector("img");
      if (!img) return;
      const t = img.cloneNode();
      t.className = "thermal"; t.alt = ""; t.setAttribute("aria-hidden", "true");
      t.removeAttribute("fetchpriority"); t.loading = "lazy";
      img.after(t);
    });
  })();
})();

/* portrait: after develop animation, allow hover to colour */
(() => {
  document.querySelectorAll(".portrait img").forEach((img) => {
    img.addEventListener("animationend", () => img.closest(".portrait").classList.add("is-developed"));
  });
})();

/* mobile swipe cards: page dots */
(() => {
  document.querySelectorAll(".skills, .awards").forEach((track) => {
    const items = [...track.children];
    if (items.length < 2) return;
    const dots = document.createElement("div");
    dots.className = "swipe-dots"; dots.setAttribute("aria-hidden", "true");
    items.forEach(() => dots.appendChild(document.createElement("i")));
    track.after(dots);
    const update = () => {
      const x = track.scrollLeft, w = track.scrollWidth - track.clientWidth;
      const idx = w <= 0 ? 0 : Math.round((x / w) * (items.length - 1));
      dots.querySelectorAll("i").forEach((d, i) => d.classList.toggle("on", i === idx));
    };
    track.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
    update();
  });
})();
