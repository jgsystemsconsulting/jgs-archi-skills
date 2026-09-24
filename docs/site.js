// Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
// SPDX-License-Identifier: MIT
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js-reveal');
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }
  if (!('IntersectionObserver' in window)) { return; }
  var sections = document.querySelectorAll('main section[id]');
  var pending = [];
  for (var i = 0; i < sections.length; i++) {
    var s = sections[i];
    if (s.getBoundingClientRect().top >= window.innerHeight) {
      s.classList.add('reveal-pending');
      pending.push(s);
    }
  }
  if (!pending.length) { return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) { return; }
      e.target.classList.remove('reveal-pending');
      e.target.classList.add('revealed');
      io.unobserve(e.target);
    });
  }, { threshold: 0, rootMargin: '0px 0px -10% 0px' });
  pending.forEach(function (s) { io.observe(s); });
})();
