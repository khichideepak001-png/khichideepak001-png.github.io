// =============================================
// ErgoElite — Main JavaScript
// =============================================

document.addEventListener('DOMContentLoaded', () => {

  // ─── Reading Progress Bar ───
  const progressBar = document.getElementById('readingProgress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = `${progress}%`;
    });
  }

  // ─── Back to Top ───
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) backToTop.classList.add('visible');
      else backToTop.classList.remove('visible');
    });
  }

  // ─── Mobile Navigation ───
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');
  const navCta    = document.getElementById('navCta');

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      navCta.classList.toggle('open');
      const spans = hamburger.querySelectorAll('span');
      spans[0].style.transform = navLinks.classList.contains('open') ? 'rotate(45deg) translate(5px, 5px)' : '';
      spans[1].style.opacity   = navLinks.classList.contains('open') ? '0' : '1';
      spans[2].style.transform = navLinks.classList.contains('open') ? 'rotate(-45deg) translate(5px, -5px)' : '';
    });
  }

  // ─── Intersection Observer — Fade-in Animations ───
  const fadeEls = document.querySelectorAll('.fade-in, .slide-in-left');
  if (fadeEls.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, i * 80);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    fadeEls.forEach(el => observer.observe(el));
  }

  // ─── Animated Score Bars ───
  const bars = document.querySelectorAll('.score-bar-fill');
  if (bars.length > 0) {
    const barObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = el.getAttribute('data-width') || el.style.width;
          el.style.width = '0%';
          setTimeout(() => { el.style.width = target; }, 200);
          barObserver.unobserve(el);
        }
      });
    }, { threshold: 0.2 });

    bars.forEach(bar => barObserver.observe(bar));
  }

  // ─── Smooth anchor scrolling ───
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ─── Sticky Nav Shadow on scroll ───
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        nav.style.boxShadow = '0 4px 32px rgba(0,0,0,0.4)';
      } else {
        nav.style.boxShadow = 'none';
      }
    });
  }
});

// ─── FAQ Toggle (global function) ───
function toggleFaq(button) {
  const answer = button.nextElementSibling;
  const icon   = button.querySelector('.faq-icon');
  const isOpen = answer.classList.contains('open');

  // Close all first
  document.querySelectorAll('.faq-answer.open').forEach(a => a.classList.remove('open'));
  document.querySelectorAll('.faq-icon').forEach(i => { i.textContent = '+'; });

  if (!isOpen) {
    answer.classList.add('open');
    icon.textContent = '−';
  }
}

// ─── Tab Switcher (used in comparison pages) ───
function switchTab(tabId, groupClass) {
  const group = document.querySelectorAll(`.${groupClass}`);
  group.forEach(el => el.classList.remove('active'));
  document.querySelectorAll(`[data-tab="${tabId}"]`).forEach(el => el.classList.add('active'));

  const panels = document.querySelectorAll('[data-panel]');
  panels.forEach(p => p.classList.remove('active'));
  const target = document.querySelector(`[data-panel="${tabId}"]`);
  if (target) target.classList.add('active');
}

// ─── Copy affiliate link helper ───
function copyLink(url) {
  navigator.clipboard.writeText(url).then(() => {
    const btn = event.target;
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    setTimeout(() => { btn.textContent = orig; }, 2000);
  });
}
