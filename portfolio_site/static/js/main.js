document.addEventListener("DOMContentLoaded", function () {
  var header = document.getElementById("siteHeader");
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("mainNav");
  var navLinks = document.querySelectorAll(".main-nav a");
  var sections = [];
  var ticking = false;
  var typeTimer = 0;
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  for (var i = 0; i < navLinks.length; i++) {
    var href = navLinks[i].getAttribute("href");
    sections.push(href && href.charAt(0) === "#" ? document.querySelector(href) : null);
  }

  function onFrame() {
    ticking = false;
    if (header) {
      header.classList.toggle("scrolled", window.scrollY > 8);
    }

    var scrollPos = window.scrollY + 140;
    var active = -1;
    for (var s = 0; s < sections.length; s++) {
      var section = sections[s];
      if (!section) continue;
      var top = section.offsetTop;
      if (scrollPos >= top && scrollPos < top + section.offsetHeight) {
        active = s;
      }
    }
    if (active >= 0) {
      for (var n = 0; n < navLinks.length; n++) {
        navLinks[n].classList.toggle("active", n === active);
      }
    }
  }

  function requestFrame() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(onFrame);
  }

  window.addEventListener("scroll", requestFrame, { passive: true });
  onFrame();

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("open");
      toggle.classList.toggle("open", isOpen);
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    nav.addEventListener("click", function (event) {
      if (event.target.tagName !== "A") return;
      nav.classList.remove("open");
      toggle.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 860 && nav.classList.contains("open")) {
        nav.classList.remove("open");
        toggle.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  var revealEls = document.querySelectorAll("[data-reveal]");
  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    for (var r = 0; r < revealEls.length; r++) {
      revealEls[r].classList.add("in-view");
    }
  } else {
    var observer = new IntersectionObserver(function (entries) {
      for (var e = 0; e < entries.length; e++) {
        if (entries[e].isIntersecting) {
          entries[e].target.classList.add("in-view");
          observer.unobserve(entries[e].target);
        }
      }
    }, { threshold: 0.08, rootMargin: "0px 0px 40px 0px" });

    for (var v = 0; v < revealEls.length; v++) {
      var el = revealEls[v];
      if (el.getBoundingClientRect().top <= window.innerHeight) {
        el.classList.add("in-view");
      } else {
        observer.observe(el);
      }
    }
  }

  var typeEl = document.querySelector(".typewriter");
  var textEl = typeEl ? typeEl.querySelector(".typewriter-text") : null;
  var roles = typeEl
    ? (typeEl.getAttribute("data-roles") || "Data Analyst,Web Developer,App Developer,Python Developer")
        .split(",")
        .map(function (role) { return role.trim(); })
        .filter(Boolean)
    : [];

  function typeLoop() {
    if (document.hidden || !textEl || roles.length === 0) return;
    var currentRole = roles[typeLoop.roleIndex];
    if (typeLoop.deleting) {
      typeLoop.charIndex--;
      if (typeLoop.charIndex <= 0) {
        textEl.textContent = "\u00a0";
        typeLoop.deleting = false;
        typeLoop.roleIndex = (typeLoop.roleIndex + 1) % roles.length;
        typeTimer = window.setTimeout(typeLoop, 280);
        return;
      }
      textEl.textContent = currentRole.substring(0, typeLoop.charIndex);
      typeTimer = window.setTimeout(typeLoop, 36);
      return;
    }
    typeLoop.charIndex++;
    textEl.textContent = currentRole.substring(0, typeLoop.charIndex);
    if (typeLoop.charIndex >= currentRole.length) {
      typeLoop.deleting = true;
      typeTimer = window.setTimeout(typeLoop, 1700);
      return;
    }
    typeTimer = window.setTimeout(typeLoop, 72);
  }
  typeLoop.roleIndex = 0;
  typeLoop.charIndex = roles[0] ? roles[0].length : 0;
  typeLoop.deleting = true;

  if (textEl && roles.length) {
    typeTimer = window.setTimeout(typeLoop, 1100);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) {
        window.clearTimeout(typeTimer);
      } else {
        window.clearTimeout(typeTimer);
        typeTimer = window.setTimeout(typeLoop, 200);
      }
    });
  }
});
