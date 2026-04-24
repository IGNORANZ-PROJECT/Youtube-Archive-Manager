const apiKeyInputEl = document.getElementById("apiKeyInput");
const channelInputEl = document.getElementById("channelInput");
const autoSyncMinutesInputEl = document.getElementById("autoSyncMinutesInput");
const backupLimitInputEl = document.getElementById("backupLimitInput");
const languageInputEl = document.getElementById("languageInput");
const syncExcludedTagsInputEl = document.getElementById("syncExcludedTagsInput");
const defaultSortInputEl = document.getElementById("defaultSortInput");
const settingsIconPreviewEl = document.getElementById("settingsIconPreview");
const iconFileInputEl = document.getElementById("iconFileInput");

const saveSettingsBtnEl = document.getElementById("saveSettingsBtn");
const applySyncExcludedTagsBtnEl = document.getElementById("applySyncExcludedTagsBtn");
const saveIconBtnEl = document.getElementById("saveIconBtn");
const syncSettingsBtnEl = document.getElementById("syncSettingsBtn");
const channelInfoEl = document.getElementById("channelInfo");
const toastEl = document.getElementById("toast");

const segmentedButtons = Array.from(document.querySelectorAll(".segmented-btn"));
const statsPrevBtnEl = document.getElementById("statsPrevBtn");
const statsTodayBtnEl = document.getElementById("statsTodayBtn");
const statsNextBtnEl = document.getElementById("statsNextBtn");
const statsApplyBtnEl = document.getElementById("statsApplyBtn");
const statsSaveBtnEl = document.getElementById("statsSaveBtn");

const tagRatioQueryInputEl = document.getElementById("tagRatioQueryInput");
const ratioSuggestListEl = document.getElementById("ratioSuggestList");
const ratioTagDropdownEl = document.getElementById("ratioTagDropdown");
const ratioTagDropdownToggleEl = document.getElementById("ratioTagDropdownToggle");
const ratioTagDropdownLabelEl = document.getElementById("ratioTagDropdownLabel");
const ratioTagDropdownPanelEl = document.getElementById("ratioTagDropdownPanel");
const ratioTagDropdownMetaEl = document.getElementById("ratioTagDropdownMeta");
const ratioTagDropdownListEl = document.getElementById("ratioTagDropdownList");
const clearRatioTagSelectionBtnEl = document.getElementById("clearRatioTagSelectionBtn");

const averageQueryInputEl = document.getElementById("averageQueryInput");
const averageSuggestListEl = document.getElementById("averageSuggestList");
const averageTagDropdownEl = document.getElementById("averageTagDropdown");
const averageTagDropdownToggleEl = document.getElementById("averageTagDropdownToggle");
const averageTagDropdownLabelEl = document.getElementById("averageTagDropdownLabel");
const averageTagDropdownPanelEl = document.getElementById("averageTagDropdownPanel");
const averageTagDropdownMetaEl = document.getElementById("averageTagDropdownMeta");
const averageTagDropdownListEl = document.getElementById("averageTagDropdownList");
const clearAverageTagSelectionBtnEl = document.getElementById("clearAverageTagSelectionBtn");

const progressChartTotalEl = document.getElementById("progressChartTotal");
const progressWindowAverageEl = document.getElementById("progressWindowAverage");
const progressOverallAverageEl = document.getElementById("progressOverallAverage");
const progressChartEl = document.getElementById("progressChart");
const chartTooltipEl = document.getElementById("chartTooltip");
const tagRatioPieEl = document.getElementById("tagRatioPie");
const tagRatioValueEl = document.getElementById("tagRatioValue");
const tagRatioTextEl = document.getElementById("tagRatioText");
const averageDurationLabelEl = document.getElementById("averageDurationLabel");
const averageDurationValueEl = document.getElementById("averageDurationValue");
const averageDurationTextEl = document.getElementById("averageDurationText");

const LANGUAGE = window.YAM_LANGUAGE === "ja" ? "ja" : "en";
const LOCALE = window.YAM_LOCALE || (LANGUAGE === "ja" ? "ja-JP" : "en-US");
const MESSAGES = {
  ja: {
    request_failed: "リクエストに失敗しました。",
    none_selected: "未選択",
    selected_count: "{count}件選択",
    tag_dropdown_meta: "{shown}件表示 / {selected}件選択",
    no_tags: "タグがありません。",
    sync_unconfigured: "未設定",
    sync_prompt: "APIキーとチャンネルを設定すると同期できます。",
    syncing_button: "同期中",
    sync_button: "同期",
    sync_failed_prefix: "同期失敗: {message}",
    last_synced_prefix: "最終同期 {datetime}",
    every_minutes: "{minutes}分ごと",
    stats_no_history: "進捗履歴がありません。",
    unknown_video: "不明な動画",
    tag_ratio_text: "{matching} / {total}本が一致",
    window_average: "表示平均 {time}",
    overall_average: "全体平均 {time}",
    average_duration_day: "1日の平均配信時間",
    average_duration_month: "1か月の平均配信時間",
    average_duration_summary: "{period_count}期間 / {video_count}本を集計",
    settings_saved_with_apply: "設定を保存しました。既存 {count}件にも適用しました。",
    settings_saved: "設定を保存しました。",
    select_image_file: "画像ファイルを選択してください。",
    icon_saved: "アイコンを保存しました。",
    applied_count: "{count}件に適用しました。",
    save_api_first: "先にAPIキーとチャンネルを保存してください。",
    sync_started: "同期を開始しました。",
    stats_saved: "統計条件を保存しました。",
    stats_refresh_error: "統計更新エラー: {message}",
    init_error: "初期化エラー: {message}",
  },
  en: {
    request_failed: "Request failed.",
    none_selected: "None",
    selected_count: "{count} selected",
    tag_dropdown_meta: "{shown} shown / {selected} selected",
    no_tags: "No tags.",
    sync_unconfigured: "Not configured",
    sync_prompt: "Set your API key and channel to enable sync.",
    syncing_button: "Syncing",
    sync_button: "Sync",
    sync_failed_prefix: "Sync failed: {message}",
    last_synced_prefix: "Last sync {datetime}",
    every_minutes: "Every {minutes} min",
    stats_no_history: "No watch history yet.",
    unknown_video: "Unknown video",
    tag_ratio_text: "{matching} / {total} videos match",
    window_average: "Window avg {time}",
    overall_average: "Overall avg {time}",
    average_duration_day: "Average stream duration per day",
    average_duration_month: "Average stream duration per month",
    average_duration_summary: "{period_count} periods / {video_count} videos",
    settings_saved_with_apply: "Settings saved. Applied to {count} existing videos.",
    settings_saved: "Settings saved.",
    select_image_file: "Select an image file.",
    icon_saved: "Icon saved.",
    applied_count: "Applied to {count} videos.",
    save_api_first: "Save the API key and channel first.",
    sync_started: "Sync started.",
    stats_saved: "Stats queries saved.",
    stats_refresh_error: "Stats refresh error: {message}",
    init_error: "Initialization error: {message}",
  },
}[LANGUAGE];

const SETTINGS_CACHE_KEY = "yam:settings-state:v9";
const STATS_CACHE_KEY = "yam:stats-state:v9";
const INDEX_CACHE_KEY = "yam:index-state:v9";
const MAX_QUERY_SUGGESTIONS = 8;

let currentGranularity = "day";
let currentOffset = 0;
let toastTimer = null;
let syncPollTimer = null;
let currentSync = null;
let currentTagEntries = [];
let ratioSelectedTags = [];
let averageSelectedTags = [];
let ratioSuggestIndex = -1;
let averageSuggestIndex = -1;
let chartTooltipHideTimer = null;
let savedStatsPreferenceSignature = "";
let statsPreferenceSaveTimer = null;

function t(key, params = {}) {
  const template = MESSAGES[key] ?? key;
  return template.replace(/\{(\w+)\}/g, (_match, name) => String(params[name] ?? ""));
}

function formatDateTimeLabel(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value).replace("T", " ").replace("Z", "");
  }
  return new Intl.DateTimeFormat(LOCALE, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function showToast(message, isError = false) {
  toastEl.textContent = message;
  toastEl.classList.add("is-visible");
  toastEl.classList.toggle("is-error", isError);
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toastEl.classList.remove("is-visible", "is-error");
  }, 2500);
}

function summarizeChannelTitles(sync) {
  const titles = Array.isArray(sync?.channel_titles) && sync.channel_titles.length
    ? sync.channel_titles
    : (sync?.channel_title ? [sync.channel_title] : []);
  if (!titles.length) {
    return "";
  }
  if (titles.length <= 2) {
    return titles.join(", ");
  }
  return `${titles[0]}, ${titles[1]} +${titles.length - 2}`;
}

function buildStatsPreferencePayload() {
  return {
    stats_ratio_query: tagRatioQueryInputEl.value.trim(),
    stats_average_query: averageQueryInputEl.value.trim(),
  };
}

function buildStatsPreferenceSignature(payload = buildStatsPreferencePayload()) {
  return JSON.stringify(payload);
}

function updateSavedStatsPreferenceSignature(settings = {}) {
  savedStatsPreferenceSignature = buildStatsPreferenceSignature({
    stats_ratio_query: settings?.stats_ratio_query || "",
    stats_average_query: settings?.stats_average_query || "",
  });
}

function clearIndexCache() {
  try {
    sessionStorage.removeItem(INDEX_CACHE_KEY);
  } catch (_error) {
    return;
  }
}

function queueStatsPreferenceSave() {
  window.clearTimeout(statsPreferenceSaveTimer);
  statsPreferenceSaveTimer = window.setTimeout(() => {
    saveStatsPreferencesIfNeeded().catch(() => {});
  }, 500);
}

function cancelChartTooltipHide() {
  window.clearTimeout(chartTooltipHideTimer);
  chartTooltipHideTimer = null;
}

function scheduleChartTooltipHide() {
  cancelChartTooltipHide();
  chartTooltipHideTimer = window.setTimeout(() => {
    chartTooltipEl.hidden = true;
  }, 180);
}

function setButtonBusy(button, busy) {
  button.disabled = busy;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || t("request_failed"));
  }
  return data;
}

function normalizeTagArray(tags) {
  const ordered = [];
  const seen = new Set();
  for (const raw of tags || []) {
    const value = String(raw || "").trim().replace(/\s+/g, " ");
    if (!value) {
      continue;
    }
    const lowered = value.toLowerCase();
    if (seen.has(lowered)) {
      continue;
    }
    seen.add(lowered);
    ordered.push(value);
  }
  return ordered.sort((left, right) => left.localeCompare(right, "ja"));
}

function splitCommaTerms(raw) {
  return normalizeTagArray(String(raw || "").split(/[,\n、]+/));
}

function joinCommaTerms(values) {
  return normalizeTagArray(values).join(", ");
}

function sortedTagEntries() {
  return [...currentTagEntries].sort((left, right) => {
    const countDiff = Number(right.count || 0) - Number(left.count || 0);
    if (countDiff !== 0) {
      return countDiff;
    }
    return String(left.tag || "").localeCompare(String(right.tag || ""), "ja");
  });
}

function setDocumentIcons(url) {
  document.querySelectorAll("link[rel='icon']").forEach((link) => {
    link.href = url;
  });
  document.querySelectorAll(".brand-icon").forEach((image) => {
    image.src = url;
  });
}

function setSettingsIcon(url) {
  settingsIconPreviewEl.src = url;
  setDocumentIcons(url);
}

function getLastTokenInfo(raw) {
  const text = String(raw || "");
  const match = text.match(/(?:^|[\s,])(-?)([^\s,]*)$/);
  if (!match) {
    return {
      token: "",
      negative: false,
      rangeStart: text.length,
      rangeEnd: text.length,
    };
  }

  const negative = match[1] === "-";
  const token = match[2] || "";
  const rangeEnd = text.length;
  const rangeStart = rangeEnd - (negative ? token.length + 1 : token.length);
  return { token, negative, rangeStart, rangeEnd };
}

function replaceLastToken(inputEl, tag) {
  const text = String(inputEl.value || "");
  const info = getLastTokenInfo(text);
  const prefix = text.slice(0, info.rangeStart);
  const suffix = text.slice(info.rangeEnd);
  const replacement = `${info.negative ? "-" : ""}${tag}`;
  const needsSpace = prefix.length > 0 && !/[\s,]$/.test(prefix);
  inputEl.value = `${prefix}${needsSpace ? " " : ""}${replacement}${suffix}${suffix ? "" : " "}`.trimEnd();
}

function getQuerySuggestions(inputEl) {
  const { token } = getLastTokenInfo(inputEl.value);
  const query = String(token || "").trim().toLowerCase();
  const entries = sortedTagEntries();

  if (!query) {
    return entries.slice(0, MAX_QUERY_SUGGESTIONS);
  }

  const startsWith = [];
  const includes = [];
  for (const entry of entries) {
    const lowered = String(entry.tag || "").toLowerCase();
    if (!lowered.includes(query)) {
      continue;
    }
    if (lowered.startsWith(query)) {
      startsWith.push(entry);
    } else {
      includes.push(entry);
    }
  }
  return [...startsWith, ...includes].slice(0, MAX_QUERY_SUGGESTIONS);
}

function highlightSuggestionAt(listEl, index) {
  const items = Array.from(listEl.querySelectorAll(".search-suggest-item"));
  items.forEach((item, itemIndex) => {
    item.classList.toggle("is-highlighted", itemIndex === index);
  });
}

function renderSuggestList(inputEl, listEl, onPick) {
  const suggestions = getQuerySuggestions(inputEl);
  listEl.innerHTML = "";

  if (!suggestions.length) {
    listEl.hidden = true;
    return;
  }

  for (const entry of suggestions) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "search-suggest-item";

    const name = document.createElement("span");
    name.className = "search-suggest-name";
    name.textContent = entry.tag;

    const count = document.createElement("span");
    count.className = "search-suggest-count";
    count.textContent = String(entry.count || 0);

    button.append(name, count);
    button.addEventListener("click", async () => {
      replaceLastToken(inputEl, entry.tag);
      syncSelectedTagsFromInputs();
      renderAllDropdowns();
      listEl.hidden = true;
      await onPick();
    });

    listEl.appendChild(button);
  }

  listEl.hidden = false;
}

function hideSuggestLists() {
  ratioSuggestListEl.hidden = true;
  averageSuggestListEl.hidden = true;
  ratioSuggestIndex = -1;
  averageSuggestIndex = -1;
}

function deriveSelectedTagsFromInput(raw) {
  const available = new Map(sortedTagEntries().map((entry) => [String(entry.tag || "").toLowerCase(), entry.tag]));
  const selected = [];
  for (const term of splitCommaTerms(raw)) {
    if (term.startsWith("-")) {
      continue;
    }
    const matched = available.get(term.toLowerCase());
    if (matched) {
      selected.push(matched);
    }
  }
  return normalizeTagArray(selected);
}

function syncSelectedTagsFromInputs() {
  ratioSelectedTags = deriveSelectedTagsFromInput(tagRatioQueryInputEl.value);
  averageSelectedTags = deriveSelectedTagsFromInput(averageQueryInputEl.value);
  updateRatioDropdownLabel();
  updateAverageDropdownLabel();
}

function updateRatioDropdownLabel() {
  if (!ratioSelectedTags.length) {
    ratioTagDropdownLabelEl.textContent = t("none_selected");
  } else if (ratioSelectedTags.length === 1) {
    ratioTagDropdownLabelEl.textContent = ratioSelectedTags[0];
  } else {
    ratioTagDropdownLabelEl.textContent = t("selected_count", { count: ratioSelectedTags.length });
  }
}

function updateAverageDropdownLabel() {
  if (!averageSelectedTags.length) {
    averageTagDropdownLabelEl.textContent = t("none_selected");
  } else if (averageSelectedTags.length === 1) {
    averageTagDropdownLabelEl.textContent = averageSelectedTags[0];
  } else {
    averageTagDropdownLabelEl.textContent = t("selected_count", { count: averageSelectedTags.length });
  }
}

function addTagToInput(inputEl, tag) {
  const nextTerms = splitCommaTerms(inputEl.value);
  if (!nextTerms.some((value) => value.toLowerCase() === String(tag || "").toLowerCase())) {
    nextTerms.push(tag);
  }
  inputEl.value = joinCommaTerms(nextTerms);
}

function removeTagFromInput(inputEl, tag) {
  const lowered = String(tag || "").toLowerCase();
  const nextTerms = splitCommaTerms(inputEl.value).filter((value) => value.toLowerCase() !== lowered);
  inputEl.value = joinCommaTerms(nextTerms);
}

function clearSelectedTagsFromInput(inputEl, selectedTags) {
  let nextValue = inputEl.value;
  for (const tag of selectedTags) {
    const lowered = String(tag || "").toLowerCase();
    nextValue = splitCommaTerms(nextValue).filter((value) => value.toLowerCase() !== lowered).join(", ");
  }
  inputEl.value = nextValue;
}

function renderTagDropdown(listEl, metaEl, selectedTags, inputEl, onChange) {
  const entries = sortedTagEntries();
  listEl.innerHTML = "";
  metaEl.textContent = t("tag_dropdown_meta", {
    shown: entries.length,
    selected: selectedTags.length,
  });

  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state compact";
    empty.textContent = t("no_tags");
    listEl.appendChild(empty);
    return;
  }

  for (const entry of entries) {
    const row = document.createElement("label");
    row.className = "tag-check-row";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = selectedTags.some((tag) => tag.toLowerCase() === String(entry.tag || "").toLowerCase());

    const name = document.createElement("span");
    name.className = "tag-check-name";
    name.textContent = entry.tag;

    const count = document.createElement("span");
    count.className = "tag-check-count";
    count.textContent = String(entry.count || 0);

    checkbox.addEventListener("change", async () => {
      if (checkbox.checked) {
        addTagToInput(inputEl, entry.tag);
      } else {
        removeTagFromInput(inputEl, entry.tag);
      }
      syncSelectedTagsFromInputs();
      renderAllDropdowns();
      await onChange();
    });

    row.append(checkbox, name, count);
    listEl.appendChild(row);
  }
}

function renderRatioDropdown() {
  renderTagDropdown(ratioTagDropdownListEl, ratioTagDropdownMetaEl, ratioSelectedTags, tagRatioQueryInputEl, loadStats);
}

function renderAverageDropdown() {
  renderTagDropdown(averageTagDropdownListEl, averageTagDropdownMetaEl, averageSelectedTags, averageQueryInputEl, loadStats);
}

function renderAllDropdowns() {
  if (!ratioTagDropdownPanelEl.hidden) {
    renderRatioDropdown();
  }
  if (!averageTagDropdownPanelEl.hidden) {
    renderAverageDropdown();
  }
}

function openRatioDropdown() {
  ratioTagDropdownPanelEl.hidden = false;
  ratioTagDropdownToggleEl.setAttribute("aria-expanded", "true");
  ratioTagDropdownEl.classList.add("is-open");
  renderRatioDropdown();
}

function closeRatioDropdown() {
  ratioTagDropdownPanelEl.hidden = true;
  ratioTagDropdownToggleEl.setAttribute("aria-expanded", "false");
  ratioTagDropdownEl.classList.remove("is-open");
}

function toggleRatioDropdown() {
  if (ratioTagDropdownPanelEl.hidden) {
    openRatioDropdown();
  } else {
    closeRatioDropdown();
  }
}

function openAverageDropdown() {
  averageTagDropdownPanelEl.hidden = false;
  averageTagDropdownToggleEl.setAttribute("aria-expanded", "true");
  averageTagDropdownEl.classList.add("is-open");
  renderAverageDropdown();
}

function closeAverageDropdown() {
  averageTagDropdownPanelEl.hidden = true;
  averageTagDropdownToggleEl.setAttribute("aria-expanded", "false");
  averageTagDropdownEl.classList.remove("is-open");
}

function toggleAverageDropdown() {
  if (averageTagDropdownPanelEl.hidden) {
    openAverageDropdown();
  } else {
    closeAverageDropdown();
  }
}

function stopSyncPolling() {
  if (!syncPollTimer) {
    return;
  }
  window.clearInterval(syncPollTimer);
  syncPollTimer = null;
}

async function refreshSyncStatus(refreshAfter = false) {
  try {
    const data = await requestJson("/api/sync-status");
    const wasRunning = Boolean(currentSync?.running);
    updateSyncUI(data.sync);
    if (wasRunning && !data.sync.running && refreshAfter) {
      await Promise.all([loadSettings(), loadStats()]);
    }
  } catch (error) {
    stopSyncPolling();
    showToast(error.message, true);
  }
}

function ensureSyncPolling() {
  if (syncPollTimer || !currentSync?.running) {
    return;
  }
  syncPollTimer = window.setInterval(() => {
    refreshSyncStatus(true);
  }, 3000);
}

function updateSyncUI(sync) {
  currentSync = sync;
  const configured = Boolean(sync?.configured);
  const running = Boolean(sync?.running || sync?.last_sync_status === "syncing");

  if (!configured) {
    syncSettingsBtnEl.textContent = t("sync_unconfigured");
    syncSettingsBtnEl.disabled = false;
    channelInfoEl.textContent = t("sync_prompt");
    stopSyncPolling();
    return;
  }

  if (running) {
    syncSettingsBtnEl.textContent = t("syncing_button");
    syncSettingsBtnEl.disabled = true;
    ensureSyncPolling();
  } else {
    syncSettingsBtnEl.textContent = t("sync_button");
    syncSettingsBtnEl.disabled = false;
    stopSyncPolling();
  }

  const parts = [];
  const channelSummary = summarizeChannelTitles(sync);
  if (channelSummary) {
    parts.push(channelSummary);
  }
  if (sync.last_sync_status === "error" && sync.last_sync_message) {
    parts.push(t("sync_failed_prefix", { message: sync.last_sync_message }));
  } else if (sync.last_synced_at) {
    parts.push(t("last_synced_prefix", { datetime: formatDateTimeLabel(sync.last_synced_at) }));
  }
  parts.push(t("every_minutes", { minutes: sync.auto_sync_minutes }));
  channelInfoEl.textContent = parts.join(" / ");
}

function populateSettings(data) {
  const settings = data.settings || {};
  apiKeyInputEl.value = settings.youtube_api_key || "";
  channelInputEl.value = settings.channel_reference || "";
  autoSyncMinutesInputEl.value = settings.auto_sync_minutes || 30;
  backupLimitInputEl.value = settings.backup_limit || 5;
  languageInputEl.value = settings.ui_language || "en";
  syncExcludedTagsInputEl.value = settings.sync_excluded_tags || "";
  tagRatioQueryInputEl.value = settings.stats_ratio_query ?? "";
  averageQueryInputEl.value = settings.stats_average_query ?? "";
  defaultSortInputEl.value = settings.default_sort || "published_desc";
  setSettingsIcon(settings.ui_icon_url || "/assets/icon.png");
  updateSyncUI(settings.sync || null);
  updateSavedStatsPreferenceSignature(settings);
  populateTagEntries(data.tag_entries || []);
}

function populateTagEntries(entries) {
  currentTagEntries = Array.isArray(entries) ? entries : [];
  syncSelectedTagsFromInputs();
  renderAllDropdowns();
}

function renderProgressChart(points) {
  progressChartEl.innerHTML = "";
  progressChartEl.style.setProperty("--chart-columns", String(Math.max(1, points.length || 1)));
  chartTooltipEl.hidden = true;
  cancelChartTooltipHide();

  if (!points.length) {
    progressChartEl.innerHTML = `<div class="empty-state">${t("stats_no_history")}</div>`;
    return;
  }

  const maxValue = Math.max(...points.map((point) => Math.abs(Number(point.seconds || 0))), 1);
  for (const point of points) {
    const column = document.createElement("div");
    column.className = "chart-column";

    const value = document.createElement("div");
    value.className = "chart-value";
    value.textContent = point.text;

    const bar = document.createElement("div");
    bar.className = "chart-bar";
    bar.style.height = `${Math.max(8, (Math.abs(Number(point.seconds || 0)) / maxValue) * 100)}%`;
    if (point.is_negative) {
      bar.classList.add("is-negative");
    }

    const label = document.createElement("div");
    label.className = "chart-label";
    label.textContent = point.label;

    if (Array.isArray(point.items) && point.items.length) {
      column.addEventListener("mouseenter", () => {
        cancelChartTooltipHide();
        chartTooltipEl.innerHTML = "";

        const head = document.createElement("div");
        head.className = "chart-tooltip-head";
        head.textContent = `${point.label} / ${point.text}`;
        chartTooltipEl.appendChild(head);

        const list = document.createElement("div");
        list.className = "chart-tooltip-list";
        for (const item of point.items) {
          const row = document.createElement("div");
          row.className = "chart-tooltip-item";

          const titleEl = document.createElement("div");
          titleEl.className = "chart-tooltip-title";
          titleEl.textContent = item.title || t("unknown_video");

          const valueEl = document.createElement("div");
          valueEl.className = "chart-tooltip-value";
          valueEl.textContent = `${item.is_negative ? "-" : ""}${item.text || "00:00:00"}`;

          row.append(titleEl, valueEl);
          list.appendChild(row);
        }

        chartTooltipEl.appendChild(list);
        chartTooltipEl.hidden = false;
      });

      column.addEventListener("mousemove", (event) => {
        const margin = 14;
        const width = chartTooltipEl.offsetWidth || 0;
        const height = chartTooltipEl.offsetHeight || 0;
        const left = Math.min(window.innerWidth - width - margin, event.clientX + margin);
        const top = Math.min(window.innerHeight - height - margin, event.clientY + margin);
        chartTooltipEl.style.left = `${Math.max(margin, left)}px`;
        chartTooltipEl.style.top = `${Math.max(margin, top)}px`;
      });

      column.addEventListener("mouseleave", () => {
        scheduleChartTooltipHide();
      });
    }

    column.append(value, bar, label);
    progressChartEl.appendChild(column);
  }
}

function renderPieChart(ratio) {
  const percent = Math.max(0, Math.min(100, Number(ratio?.ratio_percent || 0)));
  tagRatioPieEl.style.background = `conic-gradient(var(--accent) 0 ${percent}%, var(--surface-muted) ${percent}% 100%)`;
  tagRatioValueEl.textContent = `${percent.toFixed(1)}%`;
  tagRatioTextEl.textContent = t("tag_ratio_text", {
    matching: ratio?.matching_count || 0,
    total: ratio?.total_count || 0,
  });
}

function renderStatistics(stats) {
  currentOffset = Number(stats?.progress_chart?.offset || 0);
  progressWindowAverageEl.textContent = t("window_average", {
    time: stats?.progress_chart?.window_average_text || stats?.progress_chart?.average_text || "00:00:00",
  });
  progressOverallAverageEl.textContent = t("overall_average", {
    time: stats?.progress_chart?.overall_average_text || "00:00:00",
  });
  renderProgressChart(stats?.progress_chart?.points || []);
  renderPieChart(stats?.tag_ratio || {});

  averageDurationLabelEl.textContent = currentGranularity === "month" ? t("average_duration_month") : t("average_duration_day");
  averageDurationValueEl.textContent = stats?.average_duration?.average_text || "00:00:00";
  averageDurationTextEl.textContent = t("average_duration_summary", {
    period_count: stats?.average_duration?.period_count || 0,
    video_count: stats?.average_duration?.video_count || 0,
  });

  statsNextBtnEl.disabled = !stats?.progress_chart?.has_next;
  statsTodayBtnEl.disabled = currentOffset === 0;
}

function persistSettingsCache(data) {
  try {
    sessionStorage.setItem(SETTINGS_CACHE_KEY, JSON.stringify(data));
  } catch (error) {
    sessionStorage.removeItem(SETTINGS_CACHE_KEY);
  }
}

function persistStatsCache(data) {
  try {
    sessionStorage.setItem(
      STATS_CACHE_KEY,
      JSON.stringify({
        granularity: currentGranularity,
        offset: currentOffset,
        ratioQuery: tagRatioQueryInputEl.value.trim(),
        averageQuery: averageQueryInputEl.value.trim(),
        response: data,
      }),
    );
  } catch (error) {
    sessionStorage.removeItem(STATS_CACHE_KEY);
  }
}

function hydrateSettingsCache() {
  try {
    const raw = sessionStorage.getItem(SETTINGS_CACHE_KEY);
    if (!raw) {
      return false;
    }
    populateSettings(JSON.parse(raw));
    return true;
  } catch (error) {
    return false;
  }
}

function hydrateStatsCache() {
  try {
    const raw = sessionStorage.getItem(STATS_CACHE_KEY);
    if (!raw) {
      return false;
    }
    const cached = JSON.parse(raw);
    currentGranularity = cached.granularity === "month" ? "month" : "day";
    currentOffset = Number(cached.offset || 0);
    tagRatioQueryInputEl.value = cached.ratioQuery || "";
    averageQueryInputEl.value = cached.averageQuery || "";
    syncSelectedTagsFromInputs();
    segmentedButtons.forEach((button) => {
      button.classList.toggle("is-current", button.dataset.granularity === currentGranularity);
    });
    if (cached.response?.stats) {
      renderStatistics(cached.response.stats);
    }
    if (cached.response?.tag_entries) {
      populateTagEntries(cached.response.tag_entries);
    }
    return true;
  } catch (error) {
    return false;
  }
}

async function loadSettings() {
  const data = await requestJson("/api/settings");
  populateSettings(data);
  persistSettingsCache(data);
}

async function loadStats() {
  const params = new URLSearchParams({
    granularity: currentGranularity,
    offset: String(currentOffset),
    ratio_q: tagRatioQueryInputEl.value.trim(),
    average_q: averageQueryInputEl.value.trim(),
  });
  const data = await requestJson(`/api/stats?${params.toString()}`);
  renderStatistics(data.stats);
  populateTagEntries(data.tag_entries || []);
  persistStatsCache(data);
  await saveStatsPreferencesIfNeeded();
}

async function saveStatsPreferencesIfNeeded() {
  const payload = buildStatsPreferencePayload();
  const signature = buildStatsPreferenceSignature(payload);
  if (signature === savedStatsPreferenceSignature) {
    return;
  }

  const data = await requestJson("/api/stats-preferences", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  updateSavedStatsPreferenceSignature(data.settings || payload);
  persistSettingsCache({
    settings: data.settings,
    tag_entries: currentTagEntries,
  });
}

saveSettingsBtnEl.addEventListener("click", async () => {
  setButtonBusy(saveSettingsBtnEl, true);
  try {
    const previousLanguage = document.documentElement.lang || LANGUAGE;
    const data = await requestJson("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        youtube_api_key: apiKeyInputEl.value,
        channel_reference: channelInputEl.value,
        auto_sync_minutes: Number(autoSyncMinutesInputEl.value || 30),
        backup_limit: Number(backupLimitInputEl.value || 5),
        ui_language: languageInputEl.value,
        sync_excluded_tags: syncExcludedTagsInputEl.value,
        stats_ratio_query: tagRatioQueryInputEl.value.trim(),
        stats_average_query: averageQueryInputEl.value.trim(),
        default_sort: defaultSortInputEl.value,
      }),
    });
    populateSettings(data);
    persistSettingsCache(data);
    clearIndexCache();
    if ((data.settings?.ui_language || previousLanguage) !== previousLanguage) {
      window.location.reload();
      return;
    }
    if (data.apply_result) {
      showToast(t("settings_saved_with_apply", { count: data.apply_result.changed_videos || 0 }));
    } else {
      showToast(t("settings_saved"));
    }
  } catch (error) {
    showToast(error.message, true);
  } finally {
    setButtonBusy(saveSettingsBtnEl, false);
  }
});

saveIconBtnEl.addEventListener("click", async () => {
  const file = iconFileInputEl.files?.[0];
  if (!file) {
    showToast(t("select_image_file"), true);
    return;
  }

  setButtonBusy(saveIconBtnEl, true);
  try {
    const formData = new FormData();
    formData.set("icon", file);
    const data = await requestJson("/api/ui-icon", {
      method: "POST",
      body: formData,
    });
    setSettingsIcon(data.settings?.ui_icon_url || "/assets/icon.png");
    persistSettingsCache({
      settings: data.settings,
      tag_entries: currentTagEntries,
    });
    clearIndexCache();
    iconFileInputEl.value = "";
    showToast(t("icon_saved"));
  } catch (error) {
    showToast(error.message, true);
  } finally {
    setButtonBusy(saveIconBtnEl, false);
  }
});

applySyncExcludedTagsBtnEl.addEventListener("click", async () => {
  setButtonBusy(applySyncExcludedTagsBtnEl, true);
  try {
    const data = await requestJson("/api/sync-tag-exclusions/apply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sync_excluded_tags: syncExcludedTagsInputEl.value,
      }),
    });
    populateSettings({
      settings: data.settings,
      tag_entries: data.tag_entries,
    });
    persistSettingsCache({
      settings: data.settings,
      tag_entries: data.tag_entries,
    });
    clearIndexCache();
    await loadStats();
    showToast(t("applied_count", { count: data.result?.changed_videos || 0 }));
  } catch (error) {
    showToast(error.message, true);
  } finally {
    setButtonBusy(applySyncExcludedTagsBtnEl, false);
  }
});

syncSettingsBtnEl.addEventListener("click", async () => {
  if (!currentSync?.configured) {
    showToast(t("save_api_first"), true);
    return;
  }

  setButtonBusy(syncSettingsBtnEl, true);
  try {
    const data = await requestJson("/api/sync", { method: "POST" });
    updateSyncUI(data.sync);
    ensureSyncPolling();
    showToast(t("sync_started"));
  } catch (error) {
    showToast(error.message, true);
  } finally {
    if (!currentSync?.running) {
      setButtonBusy(syncSettingsBtnEl, false);
    }
  }
});

statsApplyBtnEl.addEventListener("click", async () => {
  try {
    await loadStats();
  } catch (error) {
    showToast(error.message, true);
  }
});

statsSaveBtnEl.addEventListener("click", async () => {
  setButtonBusy(statsSaveBtnEl, true);
  try {
    await saveStatsPreferencesIfNeeded();
    showToast(t("stats_saved"));
  } catch (error) {
    showToast(error.message, true);
  } finally {
    setButtonBusy(statsSaveBtnEl, false);
  }
});

statsPrevBtnEl.addEventListener("click", async () => {
  currentOffset -= 1;
  try {
    await loadStats();
  } catch (error) {
    showToast(error.message, true);
  }
});

statsTodayBtnEl.addEventListener("click", async () => {
  currentOffset = 0;
  try {
    await loadStats();
  } catch (error) {
    showToast(error.message, true);
  }
});

statsNextBtnEl.addEventListener("click", async () => {
  currentOffset = Math.min(0, currentOffset + 1);
  try {
    await loadStats();
  } catch (error) {
    showToast(error.message, true);
  }
});

for (const button of segmentedButtons) {
  button.addEventListener("click", async () => {
    currentGranularity = button.dataset.granularity === "month" ? "month" : "day";
    currentOffset = 0;
    segmentedButtons.forEach((item) => {
      item.classList.toggle("is-current", item === button);
    });
    try {
      await loadStats();
    } catch (error) {
      showToast(error.message, true);
    }
  });
}

ratioTagDropdownToggleEl.addEventListener("click", toggleRatioDropdown);
averageTagDropdownToggleEl.addEventListener("click", toggleAverageDropdown);

clearRatioTagSelectionBtnEl.addEventListener("click", async () => {
  clearSelectedTagsFromInput(tagRatioQueryInputEl, ratioSelectedTags);
  syncSelectedTagsFromInputs();
  renderRatioDropdown();
  queueStatsPreferenceSave();
  try {
    await loadStats();
  } catch (error) {
    showToast(error.message, true);
  }
});

clearAverageTagSelectionBtnEl.addEventListener("click", async () => {
  clearSelectedTagsFromInput(averageQueryInputEl, averageSelectedTags);
  syncSelectedTagsFromInputs();
  renderAverageDropdown();
  queueStatsPreferenceSave();
  try {
    await loadStats();
  } catch (error) {
    showToast(error.message, true);
  }
});

function attachSuggestHandlers(inputEl, listEl, getIndex, setIndex) {
  inputEl.addEventListener("focus", () => {
    renderSuggestList(inputEl, listEl, loadStats);
  });

  inputEl.addEventListener("input", () => {
    syncSelectedTagsFromInputs();
    renderAllDropdowns();
    renderSuggestList(inputEl, listEl, loadStats);
    queueStatsPreferenceSave();
    setIndex(-1);
  });

  inputEl.addEventListener("keydown", async (event) => {
    const items = Array.from(listEl.querySelectorAll(".search-suggest-item"));

    if (event.key === "ArrowDown") {
      if (!items.length) {
        return;
      }
      event.preventDefault();
      const nextIndex = Math.min(items.length - 1, getIndex() + 1);
      setIndex(nextIndex);
      highlightSuggestionAt(listEl, nextIndex);
      return;
    }

    if (event.key === "ArrowUp") {
      if (!items.length) {
        return;
      }
      event.preventDefault();
      const nextIndex = Math.max(0, getIndex() - 1);
      setIndex(nextIndex);
      highlightSuggestionAt(listEl, nextIndex);
      return;
    }

    if (event.key === "Enter") {
      event.preventDefault();
      const index = getIndex();
      if (index >= 0 && items[index]) {
        items[index].click();
        return;
      }
      await loadStats().catch((error) => showToast(error.message, true));
      return;
    }

    if (event.key === "Escape") {
      listEl.hidden = true;
      setIndex(-1);
    }
  });
}

attachSuggestHandlers(tagRatioQueryInputEl, ratioSuggestListEl, () => ratioSuggestIndex, (value) => {
  ratioSuggestIndex = value;
});
attachSuggestHandlers(averageQueryInputEl, averageSuggestListEl, () => averageSuggestIndex, (value) => {
  averageSuggestIndex = value;
});

chartTooltipEl.addEventListener("mouseenter", () => {
  cancelChartTooltipHide();
});

chartTooltipEl.addEventListener("mouseleave", () => {
  scheduleChartTooltipHide();
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-suggest-shell")) {
    hideSuggestLists();
  }
  if (!event.target.closest("#ratioTagDropdown")) {
    closeRatioDropdown();
  }
  if (!event.target.closest("#averageTagDropdown")) {
    closeAverageDropdown();
  }
});

async function bootstrap() {
  try {
    const hasSettingsCache = hydrateSettingsCache();
    const hasStatsCache = hydrateStatsCache();
    syncSelectedTagsFromInputs();

    await loadSettings();

    if (hasStatsCache) {
      window.requestAnimationFrame(() => {
        loadStats().catch((error) => {
          showToast(t("stats_refresh_error", { message: error.message }), true);
        });
      });
      return;
    }

    if (!hasSettingsCache || !hasStatsCache) {
      await loadStats();
    }
  } catch (error) {
    showToast(t("init_error", { message: error.message }), true);
  }
}

bootstrap();
