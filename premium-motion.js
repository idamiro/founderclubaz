// Founder Club premium motion layer. Visual polish only; no content changes.
(() => {
  document.body.classList.add("premium-motion");

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const header = document.querySelector(".header");
  const syncHeader = () => {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 20);
  };
  syncHeader();
  window.addEventListener("scroll", syncHeader, { passive: true });

  const staggerSelectors = [
    ".full-hero-stats",
    ".values",
    ".selector-grid",
    ".testimonials",
    ".events-grid",
    ".training-grid",
    ".footer-grid"
  ];

  staggerSelectors.forEach((selector) => {
    document.querySelectorAll(selector).forEach((element) => {
      element.classList.add("motion-stagger");
      element.classList.remove("in-view");
    });
  });

  const animated = document.querySelectorAll(".reveal, .motion-reveal, .motion-stagger");

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    animated.forEach((element) => element.classList.add("in-view"));
  } else {
    animated.forEach((element) => element.classList.remove("in-view"));

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.12,
      rootMargin: "0px 0px -8% 0px"
    });

    animated.forEach((element) => observer.observe(element));
  }

  if (!prefersReducedMotion && window.matchMedia("(pointer: fine)").matches) {
    const glow = document.createElement("div");
    glow.className = "cursor-glow";
    document.body.appendChild(glow);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let glowX = mouseX;
    let glowY = mouseY;

    window.addEventListener("pointermove", (event) => {
      mouseX = event.clientX;
      mouseY = event.clientY;
    }, { passive: true });

    const moveGlow = () => {
      glowX += (mouseX - glowX) * 0.08;
      glowY += (mouseY - glowY) * 0.08;
      glow.style.transform = `translate3d(${glowX - 130}px, ${glowY - 130}px, 0)`;
      requestAnimationFrame(moveGlow);
    };
    requestAnimationFrame(moveGlow);
  }
})();
