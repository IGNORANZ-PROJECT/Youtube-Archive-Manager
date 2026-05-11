(() => {
  const endpoint = "/api/app-lifecycle";
  const tabStorageKey = "yam:app-tab-id";
  const heartbeatIntervalMs = 10000;

  function createTabId() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    return `yam-tab-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  let tabId = "";
  try {
    tabId = window.sessionStorage.getItem(tabStorageKey) || "";
    if (!tabId) {
      tabId = createTabId();
      window.sessionStorage.setItem(tabStorageKey, tabId);
    }
  } catch (_error) {
    tabId = createTabId();
  }

  let heartbeatTimer = 0;
  let closed = false;

  function payloadFor(action) {
    return JSON.stringify({ action, tab_id: tabId });
  }

  function sendLifecycle(action, useBeacon = false) {
    const payload = payloadFor(action);
    if (useBeacon && navigator.sendBeacon) {
      try {
        const blob = new Blob([payload], { type: "application/json" });
        if (navigator.sendBeacon(endpoint, blob)) {
          return;
        }
      } catch (_error) {
        // Fall through to fetch.
      }
    }

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
      credentials: "same-origin",
      keepalive: useBeacon,
    }).catch(() => {});
  }

  function stopHeartbeat() {
    if (heartbeatTimer) {
      window.clearInterval(heartbeatTimer);
      heartbeatTimer = 0;
    }
  }

  function startHeartbeat() {
    stopHeartbeat();
    heartbeatTimer = window.setInterval(() => {
      sendLifecycle("heartbeat");
    }, heartbeatIntervalMs);
  }

  function registerTab() {
    closed = false;
    sendLifecycle("register");
    startHeartbeat();
  }

  function unregisterTab() {
    if (closed) {
      return;
    }
    closed = true;
    stopHeartbeat();
    sendLifecycle("unregister", true);
  }

  window.addEventListener("pageshow", () => {
    if (closed) {
      registerTab();
    } else {
      sendLifecycle("heartbeat");
    }
  });

  window.addEventListener("pagehide", unregisterTab);
  window.addEventListener("beforeunload", unregisterTab);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      sendLifecycle("heartbeat");
    }
  });

  registerTab();
})();
