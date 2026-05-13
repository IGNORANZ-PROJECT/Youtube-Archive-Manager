(() => {
  const endpoint = "/api/app-lifecycle";
  const streamEndpoint = "/api/app-lifecycle/stream";
  const fallbackHeartbeatIntervalMs = 8000;

  function createClientId() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    return `yam-client-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  const clientId = createClientId();
  let closed = false;
  let fallbackHeartbeatTimer = 0;
  let lifecycleStream = null;

  function payloadFor(action) {
    return JSON.stringify({ action, tab_id: clientId });
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

  function stopFallbackHeartbeat() {
    if (fallbackHeartbeatTimer) {
      window.clearInterval(fallbackHeartbeatTimer);
      fallbackHeartbeatTimer = 0;
    }
  }

  function startFallbackHeartbeat() {
    stopFallbackHeartbeat();
    sendLifecycle("register");
    fallbackHeartbeatTimer = window.setInterval(() => {
      sendLifecycle("heartbeat");
    }, fallbackHeartbeatIntervalMs);
  }

  function closeLifecycleStream() {
    if (lifecycleStream) {
      lifecycleStream.close();
      lifecycleStream = null;
    }
  }

  function openLifecycleStream() {
    if (!("EventSource" in window) || lifecycleStream || closed) {
      return;
    }

    lifecycleStream = new EventSource(`${streamEndpoint}?tab_id=${encodeURIComponent(clientId)}`);
    lifecycleStream.onopen = () => {
      sendLifecycle("register");
    };
    lifecycleStream.onerror = () => {
      if (closed) {
        closeLifecycleStream();
        return;
      }
      if (lifecycleStream && lifecycleStream.readyState === EventSource.CLOSED) {
        closeLifecycleStream();
      }
    };
  }

  function registerClient() {
    closed = false;
    if ("EventSource" in window) {
      openLifecycleStream();
      return;
    }
    startFallbackHeartbeat();
  }

  function unregisterClient() {
    if (closed) {
      return;
    }
    closed = true;
    stopFallbackHeartbeat();
    closeLifecycleStream();
    sendLifecycle("unregister", true);
  }

  window.addEventListener("pageshow", () => {
    if (closed) {
      registerClient();
      return;
    }
    if ("EventSource" in window) {
      openLifecycleStream();
    } else {
      sendLifecycle("heartbeat");
    }
  });

  window.addEventListener("pagehide", unregisterClient);
  window.addEventListener("beforeunload", unregisterClient);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      return;
    }
    if ("EventSource" in window) {
      openLifecycleStream();
    } else {
      sendLifecycle("heartbeat");
    }
  });

  registerClient();
})();
