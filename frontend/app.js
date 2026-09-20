/* AeroGrid AI - technician interface
 * Talks to the FastAPI backend:
 *   GET  /health  -> { "status": "healthy", "service": "AeroGrid AI" }
 *   POST /query   -> { "answer": "...", "sources": ["file.txt"] }
 * Demo mode runs without a backend so the page can be hosted as a static site.
 */
(function () {
  'use strict';

  var DEFAULT_API = 'http://localhost:8000';
  var REQUEST_TIMEOUT_MS = 90000; // local LLM inference can be slow
  var HEALTH_INTERVAL_MS = 15000;
  var NO_ANSWER = 'INSUFFICIENT_CONTEXT';

  var $ = function (id) { return document.getElementById(id); };
  var els = {
    form: $('ask-form'), question: $('question'), count: $('count'), submit: $('submit'),
    formError: $('form-error'), status: $('status'), statusText: $('status-text'),
    result: $('result'), empty: $('empty'), loading: $('loading'), notice: $('notice'),
    card: $('answer-card'), demoFlag: $('demo-flag'), answer: $('answer'),
    timing: $('timing'), sources: $('sources'), examples: $('examples'),
    settings: $('settings'), apiUrl: $('api-url'), save: $('save-settings')
  };

  /* ---------- settings (stored per browser; storage may be unavailable) ---------- */
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  };

  var onStaticHost = /\.github\.io$/.test(window.location.hostname);
  var state = {
    mode: store.get('aeroGrid.mode') || (onStaticHost ? 'demo' : 'live'),
    api: store.get('aeroGrid.api') || DEFAULT_API,
    busy: false,
    healthTimer: null
  };

  function apiBase() { return state.api.replace(/\/+$/, ''); }

  /* ---------- demo data (clearly labelled, not real guidance) ---------- */
  var DEMO_ANSWER =
    'This is a sample response from demo mode.\n\n' +
    'In live mode, AeroGrid AI retrieves the most relevant passages from the local maintenance ' +
    'documents, re-ranks them, and writes an answer that uses only those passages.';
  var DEMO = [
    { match: /e-?301|overheat/i, sources: ['wind_turbine_maintenance.txt'] },
    { match: /safety|loto|lockout/i, sources: ['safety_procedures.txt'] },
    { match: /inverter/i, sources: ['solar_troubleshooting.txt'] }
  ];

  function demoQuery(question) {
    return new Promise(function (resolve) {
      var hit = null;
      for (var i = 0; i < DEMO.length; i++) { if (DEMO[i].match.test(question)) { hit = DEMO[i]; break; } }
      window.setTimeout(function () {
        resolve(hit
          ? { answer: DEMO_ANSWER, sources: hit.sources }
          : { answer: NO_ANSWER, sources: [] });
      }, 700);
    });
  }

  /* ---------- API calls ---------- */
  function fetchWithTimeout(url, options, ms) {
    var ctrl = new AbortController();
    var timer = window.setTimeout(function () { ctrl.abort(); }, ms);
    options = options || {};
    options.signal = ctrl.signal;
    return fetch(url, options).finally(function () { window.clearTimeout(timer); });
  }

  function liveQuery(question) {
    return fetchWithTimeout(apiBase() + '/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ question: question })
    }, REQUEST_TIMEOUT_MS).then(function (res) {
      if (!res.ok) {
        var err = new Error('The API returned an error (HTTP ' + res.status + ').');
        err.kind = 'http';
        throw err;
      }
      return res.json();
    });
  }

  function checkHealth() {
    if (state.mode === 'demo') { setStatus('demo', 'Demo mode (sample data)'); return; }
    fetchWithTimeout(apiBase() + '/health', { headers: { 'Accept': 'application/json' } }, 5000)
      .then(function (res) { if (!res.ok) { throw new Error('bad status'); } return res.json(); })
      .then(function (data) {
        if (data && data.status === 'healthy') { setStatus('online', 'Connected to ' + (data.service || 'API')); }
        else { setStatus('offline', 'API responded but is not healthy'); }
      })
      .catch(function () { setStatus('offline', 'API not reachable'); });
  }

  function setStatus(kind, text) {
    els.status.setAttribute('data-state', kind);
    els.statusText.textContent = text;
  }

  function startHealthLoop() {
    window.clearInterval(state.healthTimer);
    checkHealth();
    if (state.mode === 'live') { state.healthTimer = window.setInterval(checkHealth, HEALTH_INTERVAL_MS); }
  }

  /* ---------- rendering (textContent only, never innerHTML) ---------- */
  function show(which) {
    els.empty.hidden = which !== 'empty';
    els.loading.hidden = which !== 'loading';
    els.card.hidden = which !== 'answer';
    els.result.setAttribute('aria-busy', which === 'loading' ? 'true' : 'false');
  }

  function clearNotice() { els.notice.hidden = true; els.notice.className = 'notice'; els.notice.textContent = ''; }

  function showNotice(kind, title, message) {
    els.notice.className = 'notice ' + kind;
    els.notice.textContent = '';
    var strong = document.createElement('strong');
    strong.textContent = title;
    var p = document.createElement('p');
    p.textContent = message;
    els.notice.appendChild(strong);
    els.notice.appendChild(p);
    els.notice.hidden = false;
    els.empty.hidden = true;
  }

  function renderResult(data, seconds) {
    var answer = data && typeof data.answer === 'string' ? data.answer.trim() : '';
    var sources = data && Array.isArray(data.sources) ? data.sources : [];

    if (!answer) {
      show('empty');
      showNotice('error', 'No answer returned', 'The API responded without an answer. Check the backend logs.');
      return;
    }
    if (answer === NO_ANSWER) {
      show('empty');
      showNotice('warn', 'No verified source found',
        'The documents do not cover this question, so no answer was generated. Rephrase the question or check the official manual.');
      return;
    }

    els.answer.textContent = answer;
    els.timing.textContent = 'Answered in ' + seconds.toFixed(1) + ' s';
    els.demoFlag.hidden = state.mode !== 'demo';

    els.sources.textContent = '';
    if (sources.length === 0) {
      var none = document.createElement('li');
      none.textContent = 'No sources listed.';
      els.sources.appendChild(none);
    }
    sources.forEach(function (s) {
      var li = document.createElement('li');
      li.textContent = String(s);
      els.sources.appendChild(li);
    });
    show('answer');
  }

  function describeError(err) {
    if (err && err.name === 'AbortError') {
      return ['Request timed out', 'The model took longer than ' + (REQUEST_TIMEOUT_MS / 1000) + ' seconds. Check that Ollama is running, then try again.'];
    }
    if (err && err.kind === 'http') { return ['Request failed', err.message]; }
    return ['Could not reach the API',
      'Check that the backend is running at ' + apiBase() + ' and that CORS allows this page. You can also switch to demo mode in Connection settings.'];
  }

  /* ---------- events ---------- */
  function updateCount() {
    els.count.textContent = els.question.value.length + ' / ' + els.question.maxLength;
  }

  function submit() {
    if (state.busy) { return; }
    var question = els.question.value.trim();
    els.formError.hidden = true;
    if (question.length < 5) {
      els.formError.textContent = 'Enter a question with at least 5 characters.';
      els.formError.hidden = false;
      els.question.focus();
      return;
    }

    state.busy = true;
    els.submit.disabled = true;
    els.submit.textContent = 'Searching';
    clearNotice();
    show('loading');
    var started = performance.now();
    var run = state.mode === 'demo' ? demoQuery : liveQuery;

    run(question).then(function (data) {
      renderResult(data, (performance.now() - started) / 1000);
    }).catch(function (err) {
      show('empty');
      var d = describeError(err);
      showNotice('error', d[0], d[1]);
      if (state.mode === 'live') { checkHealth(); }
    }).then(function () {
      state.busy = false;
      els.submit.disabled = false;
      els.submit.textContent = 'Get answer';
    });
  }

  els.form.addEventListener('submit', function (e) { e.preventDefault(); submit(); });
  els.question.addEventListener('input', updateCount);
  els.question.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); submit(); }
  });

  els.examples.addEventListener('click', function (e) {
    var btn = e.target.closest ? e.target.closest('button.chip') : null;
    if (!btn) { return; }
    els.question.value = btn.textContent.trim();
    updateCount();
    els.question.focus();
  });

  function syncSettingsForm() {
    els.apiUrl.value = state.api;
    var radios = document.querySelectorAll('input[name="mode"]');
    for (var i = 0; i < radios.length; i++) { radios[i].checked = radios[i].value === state.mode; }
  }

  els.save.addEventListener('click', function () {
    var chosen = document.querySelector('input[name="mode"]:checked');
    var url = els.apiUrl.value.trim();
    if (url && !/^https?:\/\//i.test(url)) { url = 'http://' + url; }
    state.mode = chosen ? chosen.value : state.mode;
    state.api = url || DEFAULT_API;
    store.set('aeroGrid.mode', state.mode);
    store.set('aeroGrid.api', state.api);
    syncSettingsForm();
    clearNotice();
    startHealthLoop();
    els.settings.open = false;
  });

  /* ---------- start ---------- */
  syncSettingsForm();
  updateCount();
  show('empty');
  startHealthLoop();
})();
