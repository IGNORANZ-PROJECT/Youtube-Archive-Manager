const videoListEl = document.getElementById("videoList");
const resultCountEl = document.getElementById("resultCount");
const searchInputEl = document.getElementById("searchInput");
const searchSuggestListEl = document.getElementById("searchSuggestList");
const statusFilterEl = document.getElementById("statusFilter");
const sortFilterEl = document.getElementById("sortFilter");
const searchBtnEl = document.getElementById("searchBtn");
const resetBtnEl = document.getElementById("resetBtn");
const syncBtnEl = document.getElementById("syncBtn");
const addBtnEl = document.getElementById("addBtn");
const jumpSearchBtnEl = document.getElementById("jumpSearchBtn");
const searchPanelEl = document.getElementById("searchPanel");
const channelInfoEl = document.getElementById("channelInfo");
const toastEl = document.getElementById("toast");
const overviewTooltipEl = document.getElementById("overviewTooltip");
const videoCardTemplateEl = document.getElementById("videoCardTemplate");
const videoEditorTemplateEl = document.getElementById("videoEditorTemplate");

const indexTagDropdownEl = document.getElementById("indexTagDropdown");
const indexTagDropdownToggleEl = document.getElementById("indexTagDropdownToggle");
const indexTagDropdownLabelEl = document.getElementById("indexTagDropdownLabel");
const indexTagDropdownPanelEl = document.getElementById("indexTagDropdownPanel");
const indexTagDropdownMetaEl = document.getElementById("indexTagDropdownMeta");
const indexTagDropdownListEl = document.getElementById("indexTagDropdownList");
const clearIndexTagSelectionBtnEl = document.getElementById("clearIndexTagSelectionBtn");

const selectVisibleBtnEl = document.getElementById("selectVisibleBtn");
const clearSelectionBtnEl = document.getElementById("clearSelectionBtn");
const bulkActionBarEl = document.getElementById("bulkActionBar");
const bulkSelectionCountEl = document.getElementById("bulkSelectionCount");
const bulkMarkWatchedBtnEl = document.getElementById("bulkMarkWatchedBtn");
const bulkMarkUnwatchedBtnEl = document.getElementById("bulkMarkUnwatchedBtn");
const bulkAddTagsInputEl = document.getElementById("bulkAddTagsInput");
const bulkAddTagsBtnEl = document.getElementById("bulkAddTagsBtn");
const bulkRemoveTagsInputEl = document.getElementById("bulkRemoveTagsInput");
const bulkRemoveTagsBtnEl = document.getElementById("bulkRemoveTagsBtn");
const bulkDeleteBtnEl = document.getElementById("bulkDeleteBtn");

const manualModalEl = document.getElementById("manualModal");
const manualFormEl = document.getElementById("manualForm");
const manualCloseBtnEl = document.getElementById("manualCloseBtn");
const manualUrlInputEl = document.getElementById("manualUrlInput");
const manualWatchedInputEl = document.getElementById("manualWatchedInput");
const manualMarkWatchedInputEl = document.getElementById("manualMarkWatchedInput");
const manualTitleInputEl = document.getElementById("manualTitleInput");
const manualDurationInputEl = document.getElementById("manualDurationInput");
const manualTagsInputEl = document.getElementById("manualTagsInput");
const manualThumbnailInputEl = document.getElementById("manualThumbnailInput");
const manualNoteInputEl = document.getElementById("manualNoteInput");
const manualSubmitBtnEl = document.getElementById("manualSubmitBtn");

const watchedPercentEl = document.getElementById("watchedPercent");
const watchedCountEl = document.getElementById("watchedCount");
const totalCountEl = document.getElementById("totalCount");
const partialCountEl = document.getElementById("partialCount");
const unseenCountEl = document.getElementById("unseenCount");
const overviewProgressEl = document.getElementById("overviewProgress");
const watchedTotalTextEl = document.getElementById("watchedTotalText");
const remainingTotalTextEl = document.getElementById("remainingTotalText");
const progressFillEl = document.getElementById("progressFill");
const balanceWatchedEl = document.getElementById("balanceWatched");
const balanceRemainingEl = document.getElementById("balanceRemaining");

const LANGUAGE = window.YAM_LANGUAGE === "ja" ? "ja" : "en";
const LOCALE = window.YAM_LOCALE || (LANGUAGE === "ja" ? "ja-JP" : "en-US");
const MESSAGES = {
  ja: {
    request_failed: "リクエストに失敗しました。",
    status_watched: "見た",
    status_partial: "途中",
    status_unseen: "未視聴",
    system_tag_deleted: "削除",
    system_tag_manual: "手動追加",
    overview_title: "一覧の進捗",
    overview_videos_label: "動画本数",
    overview_time_label: "視聴時間",
    overview_partial_unseen_label: "途中 / 未視聴",
    overview_remaining_label: "残り時間",
    overview_videos_value: "{watched} / {total}本 ({percent}%)",
    overview_time_value: "{watched} / {total} ({percent}%)",
    overview_partial_unseen_value: "{partial}本 / {unseen}本",
    sync_unconfigured: "未設定",
    sync_index_hint: "同期は設定・統計から設定できます。",
    syncing_button: "同期中",
    sync_button: "同期",
    sync_failed_prefix: "同期失敗: {message}",
    last_synced_prefix: "最終同期 {datetime}",
    every_minutes: "{minutes}分ごと",
    none_selected: "未選択",
    selected_count: "{count}件選択",
    tag_dropdown_meta: "{shown}件表示 / {selected}件選択",
    no_matching_tags: "一致するタグがありません。",
    manual_added_meta: "手動追加",
    added_at: "追加 {datetime}",
    selection_count: "{count}件選択中",
    result_count: "{count}件",
    no_tags: "タグなし",
    tag_summary: "タグ",
    tag_summary_count: "タグ {count}",
    progress_saved: "進捗を保存しました。",
    watched_updated: "視聴済みに更新しました。",
    progress_reset: "視聴状態を解除しました。",
    tags_saved: "タグを保存しました。",
    note_saved: "感想を保存しました。",
    untitled: "タイトル未設定",
    edit_with_note: "編集・メモあり",
    edit: "編集",
    progress_prefix: "進捗 {percent}%",
    watched_remaining: "見た {watched} / 残り {remaining}",
    no_matching_videos: "条件に合う動画がありません。",
    load_more_remaining: "さらに表示 ({remaining}件残り)",
    select_videos_error: "対象の動画を選択してください。",
    bulk_updated: "一括更新しました。",
    sync_started: "同期を開始しました。",
    manual_added_success: "手動追加しました。",
    bulk_marked_watched_success: "視聴済みに更新しました。",
    bulk_marked_unwatched_success: "未視聴に更新しました。",
    bulk_add_tags_success: "タグを一括追加しました。",
    bulk_remove_tags_success: "タグを一括削除しました。",
    delete_confirm: "選択した動画を削除します。同期対象の動画は次回同期で再追加される場合があります。",
    deleted_success: "動画を削除しました。",
    init_error: "初期化エラー: {message}",
  },
  en: {
    request_failed: "Request failed.",
    status_watched: "Watched",
    status_partial: "In progress",
    status_unseen: "Unwatched",
    system_tag_deleted: "Deleted",
    system_tag_manual: "Manual",
    overview_title: "Library progress",
    overview_videos_label: "Videos",
    overview_time_label: "Watch time",
    overview_partial_unseen_label: "In progress / Unwatched",
    overview_remaining_label: "Remaining time",
    overview_videos_value: "{watched} / {total} videos ({percent}%)",
    overview_time_value: "{watched} / {total} ({percent}%)",
    overview_partial_unseen_value: "{partial} videos / {unseen} videos",
    sync_unconfigured: "Not configured",
    sync_index_hint: "Configure sync from Settings & Stats.",
    syncing_button: "Syncing",
    sync_button: "Sync",
    sync_failed_prefix: "Sync failed: {message}",
    last_synced_prefix: "Last sync {datetime}",
    every_minutes: "Every {minutes} min",
    none_selected: "None",
    selected_count: "{count} selected",
    tag_dropdown_meta: "{shown} shown / {selected} selected",
    no_matching_tags: "No matching tags.",
    manual_added_meta: "Manual",
    added_at: "Added {datetime}",
    selection_count: "{count} selected",
    result_count: "{count} items",
    no_tags: "No tags",
    tag_summary: "Tags",
    tag_summary_count: "Tags {count}",
    progress_saved: "Progress saved.",
    watched_updated: "Marked as watched.",
    progress_reset: "Watch status cleared.",
    tags_saved: "Tags saved.",
    note_saved: "Notes saved.",
    untitled: "Untitled",
    edit_with_note: "Edit · note",
    edit: "Edit",
    progress_prefix: "Progress {percent}%",
    watched_remaining: "Watched {watched} / Remaining {remaining}",
    no_matching_videos: "No videos match the current filters.",
    load_more_remaining: "Show more ({remaining} left)",
    select_videos_error: "Select at least one video.",
    bulk_updated: "Bulk update completed.",
    sync_started: "Sync started.",
    manual_added_success: "Video added.",
    bulk_marked_watched_success: "Marked as watched.",
    bulk_marked_unwatched_success: "Marked as unwatched.",
    bulk_add_tags_success: "Tags added.",
    bulk_remove_tags_success: "Tags removed.",
    delete_confirm: "Delete the selected videos? Synced videos may be added again on the next sync.",
    deleted_success: "Videos deleted.",
    init_error: "Initialization error: {message}",
  },
}[LANGUAGE];

const LIST_CACHE_KEY = "yam:index-state:v9";
const INITIAL_RENDER_COUNT = 18;
const LOAD_MORE_RENDER_COUNT = 24;
const FRAME_RENDER_COUNT = 6;
const BACKGROUND_REFRESH_DELAY = 900;
const CACHE_PERSIST_DELAY = 140;
const MAX_SEARCH_SUGGESTIONS = 8;

let defaultSort = "published_desc";
let toastTimer = null;
let syncPollTimer = null;
let fetchController = null;
let backgroundRefreshTimer = null;
let cachePersistTimer = null;
let renderToken = 0;
let currentTagEntries = [];
let currentSync = null;
let currentVideos = [];
let currentSummary = createEmptySummary();
let selectedDropdownTags = [];
let selectedVideoIds = new Set();
let searchSuggestionIndex = -1;
let overviewTooltipHideTimer = null;
let renderedVideoCount = 0;
let renderTargetCount = 0;
let loadMoreBtnEl = null;

function t(key, params = {}) {
  const template = MESSAGES[key] ?? key;
  return template.replace(/\{(\w+)\}/g, (_match, name) => String(params[name] ?? ""));
}

function createEmptySummary() {
  return {
    total_count: 0,
    watched_count: 0,
    partial_count: 0,
    unseen_count: 0,
    watched_percent: 0,
    watched_total_seconds: 0,
    remaining_total_seconds: 0,
    watched_total_text: "00:00:00",
    remaining_total_text: "00:00:00",
  };
}

function normalizeSummary(summary) {
  return {
    total_count: Number(summary?.total_count || 0),
    watched_count: Number(summary?.watched_count || 0),
    partial_count: Number(summary?.partial_count || 0),
    unseen_count: Number(summary?.unseen_count || 0),
    watched_percent: Number(summary?.watched_percent || 0),
    watched_total_seconds: Number(summary?.watched_total_seconds || 0),
    remaining_total_seconds: Number(summary?.remaining_total_seconds || 0),
    watched_total_text: summary?.watched_total_text || "00:00:00",
    remaining_total_text: summary?.remaining_total_text || "00:00:00",
  };
}

function formatSeconds(totalSeconds) {
  const seconds = Math.max(0, Number(totalSeconds || 0));
  const h = String(Math.floor(seconds / 3600)).padStart(2, "0");
  const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
  const s = String(seconds % 60).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

function formatPercent(value) {
  const number = Number(value || 0);
  return number.toFixed(1).replace(/\.0$/, "");
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

function statusText(status) {
  switch (status) {
    case "watched":
      return t("status_watched");
    case "partial":
      return t("status_partial");
    case "unseen":
    default:
      return t("status_unseen");
  }
}

function showToast(message, isError = false) {
  toastEl.textContent = message;
  toastEl.classList.add("is-visible");
  toastEl.classList.toggle("is-error", isError);
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toastEl.classList.remove("is-visible", "is-error");
  }, 2600);
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

function cancelOverviewTooltipHide() {
  window.clearTimeout(overviewTooltipHideTimer);
  overviewTooltipHideTimer = null;
}

function scheduleOverviewTooltipHide() {
  cancelOverviewTooltipHide();
  overviewTooltipHideTimer = window.setTimeout(() => {
    overviewTooltipEl.hidden = true;
  }, 120);
}

function positionFloatingTooltip(tooltipEl, event) {
  const margin = 14;
  const width = tooltipEl.offsetWidth || 0;
  const height = tooltipEl.offsetHeight || 0;
  const left = Math.min(window.innerWidth - width - margin, event.clientX + margin);
  const top = Math.min(window.innerHeight - height - margin, event.clientY + margin);
  tooltipEl.style.left = `${Math.max(margin, left)}px`;
  tooltipEl.style.top = `${Math.max(margin, top)}px`;
}

function setButtonBusy(button, busy) {
  button.disabled = busy;
}

function setLinkState(link, href) {
  const enabled = Boolean(href);
  link.href = enabled ? href : "#";
  link.classList.toggle("is-disabled", !enabled);
  link.setAttribute("aria-disabled", String(!enabled));
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

function splitTagText(raw) {
  return normalizeTagArray(String(raw || "").split(/[,\n、]+/));
}

function joinTagText(tags) {
  return normalizeTagArray(tags).join(", ");
}

function parseSearchTerms(raw) {
  const include = [];
  const exclude = [];
  for (const token of String(raw || "").trim().split(/[\s,]+/)) {
    if (!token) {
      continue;
    }
    if (token.startsWith("-") && token.length > 1) {
      exclude.push(token.slice(1).toLowerCase());
    } else {
      include.push(token.toLowerCase());
    }
  }
  return { include, exclude };
}

function matchesTerms(text, include, exclude) {
  const normalized = String(text || "").toLowerCase();
  if (include.some((term) => !normalized.includes(term))) {
    return false;
  }
  if (exclude.some((term) => normalized.includes(term))) {
    return false;
  }
  return true;
}

function getLastSearchToken(raw) {
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

function replaceLastSearchToken(tag) {
  const text = String(searchInputEl.value || "");
  const info = getLastSearchToken(text);
  const prefix = text.slice(0, info.rangeStart);
  const suffix = text.slice(info.rangeEnd);
  const replacement = `${info.negative ? "-" : ""}${tag}`;
  const needsSpace = prefix.length > 0 && !/[\s,]$/.test(prefix);
  searchInputEl.value = `${prefix}${needsSpace ? " " : ""}${replacement}${suffix}${suffix ? "" : " "}`.trimEnd();
}

function buildWatchUrl(url, seconds) {
  if (!url) {
    return "";
  }
  const safeSeconds = Math.max(0, Number(seconds || 0));
  const separator = url.includes("?") ? "&" : "?";
  return `${url}${separator}t=${safeSeconds}s`;
}

function collectSystemTags(video) {
  const tags = [];
  if (video.deleted) {
    tags.push(t("system_tag_deleted"));
  }
  if (video.source === "manual") {
    tags.push(t("system_tag_manual"));
  }
  return tags;
}

function normalizeVideo(video) {
  const manualTags = normalizeTagArray(video?.manual_tags || []);
  return {
    ...video,
    deleted: Boolean(video?.deleted),
    duration_seconds: Number(video?.duration_seconds || 0),
    watched_seconds: Number(video?.watched_seconds || 0),
    last_position_seconds: Number(video?.last_position_seconds || 0),
    watched_percent: Number(video?.watched_percent || 0),
    remaining_seconds: Number(video?.remaining_seconds || 0),
    manual_tags: manualTags,
    manual_tags_text: joinTagText(manualTags),
    tags: normalizeTagArray(video?.tags || [...collectSystemTags(video || {}), ...manualTags]),
  };
}

function buildSearchableText(video) {
  return [
    video.title || "",
    video.note || "",
    (video.tags || []).join(" "),
    video.channel_title || "",
  ].join(" ");
}

function buildEffectiveTagQuery() {
  return joinTagText(selectedDropdownTags);
}

function matchesVideoFilters(video) {
  const keywordTerms = parseSearchTerms(searchInputEl.value.trim());
  const status = statusFilterEl.value;
  const videoTagsLower = (video.tags || []).map((tag) => String(tag || "").toLowerCase());

  if (!matchesTerms(buildSearchableText(video), keywordTerms.include, keywordTerms.exclude)) {
    return false;
  }

  if (selectedDropdownTags.length > 0) {
    const hasAllTags = selectedDropdownTags.every((tag) => videoTagsLower.includes(String(tag).toLowerCase()));
    if (!hasAllTags) {
      return false;
    }
  }

  if (status && status !== "all" && video.status !== status) {
    return false;
  }

  return true;
}

function updateSummary(summary) {
  const normalized = normalizeSummary(summary);
  currentSummary = normalized;

  watchedPercentEl.textContent = normalized.watched_percent.toFixed(1);
  watchedCountEl.textContent = normalized.watched_count;
  totalCountEl.textContent = normalized.total_count;
  partialCountEl.textContent = normalized.partial_count;
  unseenCountEl.textContent = normalized.unseen_count;
  watchedTotalTextEl.textContent = normalized.watched_total_text;
  remainingTotalTextEl.textContent = normalized.remaining_total_text;
  progressFillEl.style.width = `${normalized.watched_percent}%`;

  const totalSeconds = normalized.watched_total_seconds + normalized.remaining_total_seconds;
  const watchedRatio = totalSeconds > 0 ? (normalized.watched_total_seconds / totalSeconds) * 100 : 0;
  balanceWatchedEl.style.width = `${watchedRatio}%`;
  balanceRemainingEl.style.width = `${100 - watchedRatio}%`;
}

function renderOverviewTooltip() {
  const totalSeconds = Number(currentSummary.watched_total_seconds || 0) + Number(currentSummary.remaining_total_seconds || 0);
  const watchedRatio = totalSeconds > 0 ? (Number(currentSummary.watched_total_seconds || 0) / totalSeconds) * 100 : 0;

  overviewTooltipEl.innerHTML = "";

  const head = document.createElement("div");
  head.className = "chart-tooltip-head";
  head.textContent = t("overview_title");

  const list = document.createElement("div");
  list.className = "chart-tooltip-list";

  const rows = [
    {
      label: t("overview_videos_label"),
      value: t("overview_videos_value", {
        watched: currentSummary.watched_count,
        total: currentSummary.total_count,
        percent: formatPercent(currentSummary.watched_percent),
      }),
    },
    {
      label: t("overview_time_label"),
      value: t("overview_time_value", {
        watched: currentSummary.watched_total_text,
        total: formatSeconds(totalSeconds),
        percent: formatPercent(watchedRatio),
      }),
    },
    {
      label: t("overview_partial_unseen_label"),
      value: t("overview_partial_unseen_value", {
        partial: currentSummary.partial_count,
        unseen: currentSummary.unseen_count,
      }),
    },
    {
      label: t("overview_remaining_label"),
      value: currentSummary.remaining_total_text,
    },
  ];

  for (const rowData of rows) {
    const row = document.createElement("div");
    row.className = "chart-tooltip-item";

    const titleEl = document.createElement("div");
    titleEl.className = "chart-tooltip-title";
    titleEl.textContent = rowData.label;

    const valueEl = document.createElement("div");
    valueEl.className = "chart-tooltip-value";
    valueEl.textContent = rowData.value;

    row.append(titleEl, valueEl);
    list.appendChild(row);
  }

  overviewTooltipEl.append(head, list);
}

function stopSyncPolling() {
  if (!syncPollTimer) {
    return;
  }
  window.clearInterval(syncPollTimer);
  syncPollTimer = null;
}

async function refreshSyncStatus(fetchAfter = false) {
  try {
    const data = await requestJson("/api/sync-status");
    const wasRunning = Boolean(currentSync?.running);
    updateSyncUI(data.sync);
    if (wasRunning && !data.sync.running && fetchAfter) {
      await fetchVideos();
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
    syncBtnEl.textContent = t("sync_unconfigured");
    syncBtnEl.disabled = false;
    channelInfoEl.textContent = t("sync_index_hint");
    stopSyncPolling();
    return;
  }

  if (running) {
    syncBtnEl.textContent = t("syncing_button");
    syncBtnEl.disabled = true;
    ensureSyncPolling();
  } else {
    syncBtnEl.textContent = t("sync_button");
    syncBtnEl.disabled = false;
    stopSyncPolling();
  }

  const info = [];
  const channelSummary = summarizeChannelTitles(sync);
  if (channelSummary) {
    info.push(channelSummary);
  }
  if (sync.last_sync_status === "error" && sync.last_sync_message) {
    info.push(t("sync_failed_prefix", { message: sync.last_sync_message }));
  } else if (sync.last_synced_at) {
    info.push(t("last_synced_prefix", { datetime: formatDateTimeLabel(sync.last_synced_at) }));
  }
  info.push(t("every_minutes", { minutes: sync.auto_sync_minutes }));
  channelInfoEl.textContent = info.join(" / ");
}

function applyManualTagsToVideo(video, manualTags) {
  const normalizedTags = normalizeTagArray(manualTags);
  video.manual_tags = normalizedTags;
  video.manual_tags_text = joinTagText(normalizedTags);
  video.tags = normalizeTagArray([...collectSystemTags(video), ...normalizedTags]);
}

function getSearchTagSuggestions() {
  const { token } = getLastSearchToken(searchInputEl.value);
  const query = String(token || "").trim().toLowerCase();
  const entries = [...currentTagEntries].sort((left, right) => Number(right.count || 0) - Number(left.count || 0));
  if (!query) {
    return entries.slice(0, MAX_SEARCH_SUGGESTIONS);
  }

  const startsWith = [];
  const includes = [];
  for (const entry of entries) {
    const name = String(entry.tag || "");
    const lowered = name.toLowerCase();
    if (!lowered.includes(query)) {
      continue;
    }
    if (lowered.startsWith(query)) {
      startsWith.push(entry);
    } else {
      includes.push(entry);
    }
  }
  return [...startsWith, ...includes].slice(0, MAX_SEARCH_SUGGESTIONS);
}

function renderSearchTagSuggestions() {
  const suggestions = getSearchTagSuggestions();
  searchSuggestListEl.innerHTML = "";
  searchSuggestionIndex = -1;

  if (!suggestions.length) {
    searchSuggestListEl.hidden = true;
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
      replaceLastSearchToken(entry.tag);
      renderSearchTagSuggestions();
      await fetchVideos();
    });

    searchSuggestListEl.appendChild(button);
  }

  searchSuggestListEl.hidden = false;
}

function highlightSearchSuggestionAt(index) {
  const items = Array.from(searchSuggestListEl.querySelectorAll(".search-suggest-item"));
  items.forEach((item, itemIndex) => {
    item.classList.toggle("is-highlighted", itemIndex === index);
  });
}

function openIndexTagDropdown() {
  indexTagDropdownPanelEl.hidden = false;
  indexTagDropdownToggleEl.setAttribute("aria-expanded", "true");
  indexTagDropdownEl.classList.add("is-open");
  renderIndexTagDropdown();
}

function closeIndexTagDropdown() {
  indexTagDropdownPanelEl.hidden = true;
  indexTagDropdownToggleEl.setAttribute("aria-expanded", "false");
  indexTagDropdownEl.classList.remove("is-open");
}

function toggleIndexTagDropdown() {
  if (indexTagDropdownPanelEl.hidden) {
    openIndexTagDropdown();
  } else {
    closeIndexTagDropdown();
  }
}

function updateIndexTagDropdownLabel() {
  if (selectedDropdownTags.length === 0) {
    indexTagDropdownLabelEl.textContent = t("none_selected");
    return;
  }
  if (selectedDropdownTags.length === 1) {
    indexTagDropdownLabelEl.textContent = selectedDropdownTags[0];
    return;
  }
  indexTagDropdownLabelEl.textContent = t("selected_count", { count: selectedDropdownTags.length });
}

function setSelectedDropdownTags(nextTags) {
  selectedDropdownTags = normalizeTagArray(nextTags || []);
  updateIndexTagDropdownLabel();
  if (!indexTagDropdownPanelEl.hidden) {
    renderIndexTagDropdown();
  }
}

function addSelectedDropdownTag(tag) {
  const normalized = String(tag || "").trim();
  if (!normalized) {
    return;
  }
  if (selectedDropdownTags.some((value) => value.toLowerCase() === normalized.toLowerCase())) {
    return;
  }
  setSelectedDropdownTags([...selectedDropdownTags, normalized]);
}

function removeSelectedDropdownTag(tag) {
  const lowered = String(tag || "").toLowerCase();
  setSelectedDropdownTags(selectedDropdownTags.filter((value) => value.toLowerCase() !== lowered));
}

function getIndexTagDropdownEntries() {
  return [...currentTagEntries].sort((left, right) => {
    const countDiff = Number(right.count || 0) - Number(left.count || 0);
    if (countDiff !== 0) {
      return countDiff;
    }
    return String(left.tag || "").localeCompare(String(right.tag || ""), "ja");
  });
}

function renderIndexTagDropdown() {
  const entries = getIndexTagDropdownEntries();
  indexTagDropdownListEl.innerHTML = "";
  indexTagDropdownMetaEl.textContent = t("tag_dropdown_meta", {
    shown: entries.length,
    selected: selectedDropdownTags.length,
  });

  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state compact";
    empty.textContent = t("no_matching_tags");
    indexTagDropdownListEl.appendChild(empty);
    return;
  }

  for (const entry of entries) {
    const row = document.createElement("label");
    row.className = "tag-check-row";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = selectedDropdownTags.some((tag) => tag.toLowerCase() === String(entry.tag || "").toLowerCase());

    const name = document.createElement("span");
    name.className = "tag-check-name";
    name.textContent = entry.tag;

    const count = document.createElement("span");
    count.className = "tag-check-count";
    count.textContent = String(entry.count || 0);

    checkbox.addEventListener("change", async () => {
      if (checkbox.checked) {
        addSelectedDropdownTag(entry.tag);
      } else {
        removeSelectedDropdownTag(entry.tag);
      }
      renderIndexTagDropdown();
      await fetchVideos();
    });

    row.append(checkbox, name, count);
    indexTagDropdownListEl.appendChild(row);
  }
}

function populateTagEntries(entries) {
  currentTagEntries = Array.isArray(entries) ? entries : [];
  updateIndexTagDropdownLabel();
  if (!indexTagDropdownPanelEl.hidden) {
    renderIndexTagDropdown();
  }
  renderSearchTagSuggestions();
}

function buildMetaText(video) {
  const parts = [];
  if (video.source === "manual") {
    parts.push(t("manual_added_meta"));
  }
  if (video.published_at) {
    parts.push(formatDateTimeLabel(video.published_at));
  } else if (video.created_at) {
    parts.push(t("added_at", { datetime: formatDateTimeLabel(video.created_at) }));
  }
  if (video.duration_seconds) {
    parts.push(formatSeconds(video.duration_seconds));
  }
  return parts.join(" ・ ");
}

function statusCountKey(status) {
  switch (status) {
    case "watched":
      return "watched_count";
    case "partial":
      return "partial_count";
    case "unseen":
    default:
      return "unseen_count";
  }
}

function patchSummaryForProgress(previousStatus, nextStatus, previousWatched, nextWatched, previousRemaining, nextRemaining) {
  currentSummary.watched_total_seconds = Math.max(
    0,
    Number(currentSummary.watched_total_seconds || 0) + (nextWatched - previousWatched),
  );
  currentSummary.remaining_total_seconds = Math.max(
    0,
    Number(currentSummary.remaining_total_seconds || 0) + (nextRemaining - previousRemaining),
  );
  currentSummary.watched_total_text = formatSeconds(currentSummary.watched_total_seconds);
  currentSummary.remaining_total_text = formatSeconds(currentSummary.remaining_total_seconds);

  if (previousStatus !== nextStatus) {
    currentSummary[statusCountKey(previousStatus)] = Math.max(
      0,
      Number(currentSummary[statusCountKey(previousStatus)] || 0) - 1,
    );
    currentSummary[statusCountKey(nextStatus)] = Number(currentSummary[statusCountKey(nextStatus)] || 0) + 1;
  }

  currentSummary.watched_percent = currentSummary.total_count > 0
    ? Number(((currentSummary.watched_count / currentSummary.total_count) * 100).toFixed(1))
    : 0;
  updateSummary(currentSummary);
}

function applyProgressResultToVideo(video, result) {
  const previousStatus = video.status;
  const previousWatched = Number(video.watched_seconds || 0);
  const previousRemaining = Number(video.remaining_seconds || 0);
  const durationSeconds = Number(video.duration_seconds || 0);

  video.status = result.status || video.status;
  video.watched_seconds = Number(result.watched_seconds || 0);
  video.watched_time_text = result.watched_time_text || formatSeconds(video.watched_seconds);
  video.last_position_seconds = Number(result.last_position_seconds || 0);
  video.watched_percent = durationSeconds > 0
    ? Number(Math.min(100, (video.watched_seconds / durationSeconds) * 100).toFixed(1))
    : 0;
  video.remaining_seconds = durationSeconds > 0 ? Math.max(0, durationSeconds - video.watched_seconds) : 0;
  video.remaining_time_text = formatSeconds(video.remaining_seconds);
  video.resume_url = buildWatchUrl(video.url, video.last_position_seconds);
  video.watch_url = buildWatchUrl(video.url, video.watched_seconds);

  patchSummaryForProgress(
    previousStatus,
    video.status,
    previousWatched,
    video.watched_seconds,
    previousRemaining,
    video.remaining_seconds,
  );
}

function persistListCache() {
  try {
    sessionStorage.setItem(
      LIST_CACHE_KEY,
      JSON.stringify({
        filters: {
          q: searchInputEl.value.trim(),
          selectedDropdownTags,
          status: statusFilterEl.value,
          sort: sortFilterEl.value || defaultSort,
          selectedVideoIds: [...selectedVideoIds],
        },
        response: {
          summary: currentSummary,
          count: currentVideos.length,
          videos: currentVideos,
          tag_entries: currentTagEntries,
          sync: currentSync,
          sort: sortFilterEl.value || defaultSort,
        },
      }),
    );
  } catch (_error) {
    try {
      sessionStorage.removeItem(LIST_CACHE_KEY);
    } catch (_ignored) {
      return;
    }
  }
}

function schedulePersistListCache() {
  window.clearTimeout(cachePersistTimer);
  cachePersistTimer = window.setTimeout(() => {
    persistListCache();
  }, CACHE_PERSIST_DELAY);
}

function hydrateListCache() {
  try {
    const raw = sessionStorage.getItem(LIST_CACHE_KEY);
    if (!raw) {
      return false;
    }
    const cached = JSON.parse(raw);
    const filters = cached?.filters || {};

    searchInputEl.value = filters.q || "";
    selectedDropdownTags = normalizeTagArray(filters.selectedDropdownTags || []);
    selectedVideoIds = new Set((filters.selectedVideoIds || []).map((value) => String(value || "")));
    statusFilterEl.value = filters.status || "all";
    defaultSort = filters.sort || defaultSort;
    sortFilterEl.value = defaultSort;

    applyVideoResponse(cached.response || {}, false);
    return true;
  } catch (_error) {
    return false;
  }
}

function scheduleBackgroundRefresh() {
  window.clearTimeout(backgroundRefreshTimer);
  backgroundRefreshTimer = window.setTimeout(() => {
    fetchVideos().catch((error) => {
      if (error?.name !== "AbortError") {
        showToast(error.message, true);
      }
    });
  }, BACKGROUND_REFRESH_DELAY);
}

function reconcileSelectedVideos() {
  const visibleIds = new Set(currentVideos.map((video) => String(video.video_id || "")));
  selectedVideoIds = new Set(
    [...selectedVideoIds].filter((videoId) => visibleIds.has(String(videoId || ""))),
  );
}

function updateBulkActionState() {
  const count = selectedVideoIds.size;
  bulkSelectionCountEl.textContent = t("selection_count", { count });
  bulkActionBarEl.hidden = count === 0;
  clearSelectionBtnEl.disabled = count === 0;
}

function isVideoSelected(videoId) {
  return selectedVideoIds.has(String(videoId || ""));
}

function setVideoSelected(videoId, selected) {
  const key = String(videoId || "");
  if (!key) {
    return;
  }
  if (selected) {
    selectedVideoIds.add(key);
  } else {
    selectedVideoIds.delete(key);
  }
  updateBulkActionState();
  schedulePersistListCache();
}

function clearSelectedVideos() {
  selectedVideoIds.clear();
  updateBulkActionState();
  renderVideos(currentVideos);
  schedulePersistListCache();
}

function selectVisibleVideos() {
  selectedVideoIds = new Set(currentVideos.map((video) => String(video.video_id || "")));
  updateBulkActionState();
  renderVideos(currentVideos);
  schedulePersistListCache();
}

async function fetchVideos() {
  if (fetchController) {
    fetchController.abort();
  }

  fetchController = new AbortController();
  const params = new URLSearchParams({
    q: searchInputEl.value.trim(),
    tag_q: buildEffectiveTagQuery(),
    status: statusFilterEl.value,
    sort: sortFilterEl.value || defaultSort,
  });

  const data = await requestJson(`/api/videos?${params.toString()}`, {
    signal: fetchController.signal,
  });
  applyVideoResponse(data, true);
}

function applyVideoResponse(data, persist = true) {
  defaultSort = data.sort || defaultSort;
  sortFilterEl.value = data.sort || defaultSort;
  currentVideos = Array.isArray(data.videos) ? data.videos.map(normalizeVideo) : [];
  reconcileSelectedVideos();
  updateSummary(data.summary || createEmptySummary());
  updateSyncUI(data.sync || null);
  populateTagEntries(data.tag_entries || []);
  renderVideos(currentVideos);
  updateBulkActionState();
  resultCountEl.textContent = t("result_count", { count: Number(data.count || currentVideos.length) });
  if (persist) {
    schedulePersistListCache();
  }
}

function createEditableTagPreview(container, tagsInput, onChange) {
  const previewTags = splitTagText(tagsInput.value);
  container.innerHTML = "";

  if (!previewTags.length) {
    const empty = document.createElement("div");
    empty.className = "tag-empty";
    empty.textContent = t("no_tags");
    container.appendChild(empty);
    onChange(0);
    return;
  }

  for (const tag of previewTags) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "tag-chip tag-chip-editable";

    const label = document.createElement("span");
    label.textContent = tag;

    const remove = document.createElement("span");
    remove.className = "tag-chip-remove";
    remove.textContent = "×";

    button.append(label, remove);
    button.addEventListener("click", () => {
      const nextTags = splitTagText(tagsInput.value).filter((value) => value.toLowerCase() !== tag.toLowerCase());
      tagsInput.value = joinTagText(nextTags);
      createEditableTagPreview(container, tagsInput, onChange);
    });
    container.appendChild(button);
  }

  onChange(previewTags.length);
}

function createVideoCard(video) {
  const fragment = videoCardTemplateEl.content.cloneNode(true);
  const card = fragment.querySelector(".video-card");
  const checkbox = fragment.querySelector(".video-select-checkbox");
  const thumb = fragment.querySelector(".thumb");
  const title = fragment.querySelector(".title");
  const statusBadge = fragment.querySelector(".status-badge");
  const meta = fragment.querySelector(".meta");
  const miniProgressFill = fragment.querySelector(".mini-progress-fill");
  const miniProgressText = fragment.querySelector(".mini-progress-text");
  const progressBalance = fragment.querySelector(".progress-balance");
  const openLink = fragment.querySelector(".open-link");
  const resumeLink = fragment.querySelector(".resume-link");
  const thumbDownloadLink = fragment.querySelector(".thumb-download-link");
  const detailsBox = fragment.querySelector(".details-box");
  const editSummary = fragment.querySelector(".edit-summary");
  const editorHost = fragment.querySelector(".lazy-editor-host");

  let editorRefs = null;

  function fillEditor() {
    if (!editorRefs) {
      return;
    }

    const {
      tagEditorSummary,
      editableTagList,
      tagsInput,
      noteTextarea,
      watchedTimeInput,
    } = editorRefs;

    function refreshTagPreview() {
      createEditableTagPreview(editableTagList, tagsInput, (count) => {
        tagEditorSummary.textContent = count > 0 ? t("tag_summary_count", { count }) : t("tag_summary");
      });
    }

    if (document.activeElement !== watchedTimeInput) {
      watchedTimeInput.value = video.watched_time_text || "00:00:00";
    }
    if (document.activeElement !== tagsInput) {
      tagsInput.value = video.manual_tags_text || "";
    }
    if (document.activeElement !== noteTextarea) {
      noteTextarea.value = video.note || "";
    }
    refreshTagPreview();
  }

  function ensureEditor() {
    if (editorRefs) {
      return editorRefs;
    }

    const editorFragment = videoEditorTemplateEl.content.cloneNode(true);
    const watchedTimeInput = editorFragment.querySelector(".watched-time-input");
    const saveProgressBtn = editorFragment.querySelector(".save-progress-btn");
    const markWatchedBtn = editorFragment.querySelector(".mark-watched-btn");
    const clearProgressBtn = editorFragment.querySelector(".clear-progress-btn");
    const tagEditorSummary = editorFragment.querySelector(".tag-editor-summary");
    const editableTagList = editorFragment.querySelector(".editable-tag-list");
    const tagsInput = editorFragment.querySelector(".tags-input");
    const saveTagsBtn = editorFragment.querySelector(".save-tags-btn");
    const noteTextarea = editorFragment.querySelector(".note-textarea");
    const saveNoteBtn = editorFragment.querySelector(".save-note-btn");

    function refreshTagPreview() {
      createEditableTagPreview(editableTagList, tagsInput, (count) => {
        tagEditorSummary.textContent = count > 0 ? t("tag_summary_count", { count }) : t("tag_summary");
      });
    }

    tagsInput.addEventListener("input", refreshTagPreview);

    saveProgressBtn.addEventListener("click", async () => {
      setButtonBusy(saveProgressBtn, true);
      try {
        const data = await requestJson("/api/progress", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            video_id: video.video_id,
            watched_time_text: watchedTimeInput.value,
          }),
        });
        applyProgressResultToVideo(video, data.result || {});
        fillCard();
        schedulePersistListCache();
        showToast(t("progress_saved"));
        if (!matchesVideoFilters(video)) {
          await fetchVideos();
        }
      } catch (error) {
        showToast(error.message, true);
      } finally {
        setButtonBusy(saveProgressBtn, false);
      }
    });

    markWatchedBtn.addEventListener("click", async () => {
      setButtonBusy(markWatchedBtn, true);
      try {
        const data = await requestJson("/api/progress", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            video_id: video.video_id,
            watched_time_text: watchedTimeInput.value,
            mark_watched: true,
          }),
        });
        applyProgressResultToVideo(video, data.result || {});
        fillCard();
        schedulePersistListCache();
        showToast(t("watched_updated"));
        if (!matchesVideoFilters(video)) {
          await fetchVideos();
        }
      } catch (error) {
        showToast(error.message, true);
      } finally {
        setButtonBusy(markWatchedBtn, false);
      }
    });

    clearProgressBtn.addEventListener("click", async () => {
      setButtonBusy(clearProgressBtn, true);
      try {
        const data = await requestJson("/api/progress", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            video_id: video.video_id,
            clear_progress: true,
          }),
        });
        applyProgressResultToVideo(video, data.result || {});
        fillCard();
        schedulePersistListCache();
        showToast(t("progress_reset"));
        if (!matchesVideoFilters(video)) {
          await fetchVideos();
        }
      } catch (error) {
        showToast(error.message, true);
      } finally {
        setButtonBusy(clearProgressBtn, false);
      }
    });

    saveTagsBtn.addEventListener("click", async () => {
      setButtonBusy(saveTagsBtn, true);
      try {
        const data = await requestJson("/api/video-tags", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            video_id: video.video_id,
            manual_tags: tagsInput.value,
          }),
        });
        applyManualTagsToVideo(video, data.result?.manual_tags || splitTagText(tagsInput.value));
        tagsInput.value = video.manual_tags_text;
        refreshTagPreview();
        fillCard();
        schedulePersistListCache();
        showToast(t("tags_saved"));
        if (!matchesVideoFilters(video)) {
          await fetchVideos();
        } else {
          scheduleBackgroundRefresh();
        }
      } catch (error) {
        showToast(error.message, true);
      } finally {
        setButtonBusy(saveTagsBtn, false);
      }
    });

    saveNoteBtn.addEventListener("click", async () => {
      setButtonBusy(saveNoteBtn, true);
      try {
        const data = await requestJson("/api/note", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            video_id: video.video_id,
            note: noteTextarea.value,
          }),
        });
        video.note = data.result?.note || noteTextarea.value;
        fillCard();
        schedulePersistListCache();
        showToast(t("note_saved"));
        if (searchInputEl.value.trim()) {
          scheduleBackgroundRefresh();
        }
      } catch (error) {
        showToast(error.message, true);
      } finally {
        setButtonBusy(saveNoteBtn, false);
      }
    });

    editorHost.appendChild(editorFragment);
    editorRefs = {
      watchedTimeInput,
      tagEditorSummary,
      editableTagList,
      tagsInput,
      noteTextarea,
    };
    fillEditor();
    return editorRefs;
  }

  function fillCard() {
    card.classList.toggle("is-deleted", video.deleted);
    checkbox.checked = isVideoSelected(video.video_id);

    if (video.thumbnail_url) {
      thumb.src = video.thumbnail_url;
    } else {
      thumb.removeAttribute("src");
    }
    thumb.alt = video.title || "thumbnail";

    title.textContent = video.title || t("untitled");
    statusBadge.textContent = statusText(video.status);
    statusBadge.className = "status-badge";
    statusBadge.classList.add(`status-${video.status}`);
    meta.textContent = buildMetaText(video);

    miniProgressFill.style.width = `${video.watched_percent}%`;
    miniProgressText.textContent = t("progress_prefix", { percent: formatPercent(video.watched_percent) });
    progressBalance.textContent =
      t("watched_remaining", {
        watched: video.watched_time_text || formatSeconds(video.watched_seconds),
        remaining: video.remaining_time_text || formatSeconds(video.remaining_seconds),
      });

    setLinkState(openLink, video.deleted ? "" : video.url || "");
    setLinkState(resumeLink, video.deleted ? "" : video.resume_url || video.url || "");
    setLinkState(thumbDownloadLink, video.thumbnail_url ? video.thumbnail_download_url : "");
    editSummary.textContent = video.note && video.note.trim() ? t("edit_with_note") : t("edit");

    if (editorRefs) {
      fillEditor();
    }
  }

  checkbox.addEventListener("change", () => {
    setVideoSelected(video.video_id, checkbox.checked);
  });

  detailsBox.addEventListener("toggle", () => {
    if (detailsBox.open) {
      ensureEditor();
    }
  });

  fillCard();
  return card;
}

function renderVideos(videos) {
  renderToken += 1;
  const token = renderToken;
  videoListEl.innerHTML = "";
  renderedVideoCount = 0;
  renderTargetCount = 0;
  loadMoreBtnEl = null;

  if (!videos.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = t("no_matching_videos");
    videoListEl.appendChild(empty);
    return;
  }

  const ensureLoadMoreButton = () => {
    if (token !== renderToken) {
      return;
    }

    if (renderedVideoCount >= videos.length) {
      if (loadMoreBtnEl) {
        loadMoreBtnEl.remove();
        loadMoreBtnEl = null;
      }
      return;
    }

    if (!loadMoreBtnEl) {
      loadMoreBtnEl = document.createElement("button");
      loadMoreBtnEl.type = "button";
      loadMoreBtnEl.className = "btn ghost load-more-trigger";
      loadMoreBtnEl.addEventListener("click", () => {
        renderTargetCount = Math.min(videos.length, renderTargetCount + LOAD_MORE_RENDER_COUNT);
        appendBatch();
      });
      videoListEl.appendChild(loadMoreBtnEl);
    }

    const remaining = Math.max(0, videos.length - renderedVideoCount);
    loadMoreBtnEl.textContent = t("load_more_remaining", { remaining });
  };

  const appendBatch = () => {
    if (token !== renderToken) {
      return;
    }

    if (loadMoreBtnEl) {
      loadMoreBtnEl.remove();
      loadMoreBtnEl = null;
    }

    const fragment = document.createDocumentFragment();
    let appended = 0;
    while (
      appended < FRAME_RENDER_COUNT
      && renderedVideoCount < renderTargetCount
      && renderedVideoCount < videos.length
    ) {
      fragment.appendChild(createVideoCard(videos[renderedVideoCount]));
      renderedVideoCount += 1;
      appended += 1;
    }
    if (fragment.childNodes.length > 0) {
      videoListEl.appendChild(fragment);
    }

    if (renderedVideoCount < renderTargetCount && renderedVideoCount < videos.length) {
      window.requestAnimationFrame(appendBatch);
      return;
    }

    ensureLoadMoreButton();
  };

  renderTargetCount = Math.min(videos.length, INITIAL_RENDER_COUNT);
  window.requestAnimationFrame(appendBatch);
}

function resetFilters() {
  searchInputEl.value = "";
  setSelectedDropdownTags([]);
  statusFilterEl.value = "all";
  sortFilterEl.value = defaultSort;
  searchSuggestListEl.hidden = true;
  closeIndexTagDropdown();
}

function updateJumpButton() {
  jumpSearchBtnEl.classList.toggle("is-visible", window.scrollY > 260);
}

function openManualModal() {
  manualFormEl.reset();
  manualWatchedInputEl.disabled = false;
  if (typeof manualModalEl.showModal === "function") {
    manualModalEl.showModal();
  }
}

function closeManualModal() {
  if (typeof manualModalEl.close === "function") {
    manualModalEl.close();
  }
}

async function submitBulkAction({
  addTags = "",
  removeTags = "",
  deleteVideos = false,
  markWatched = false,
  clearProgress = false,
  successMessage,
}) {
  const videoIds = [...selectedVideoIds];
  if (!videoIds.length) {
    showToast(t("select_videos_error"), true);
    return;
  }

  const data = await requestJson("/api/videos/bulk", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      video_ids: videoIds,
      add_tags: addTags,
      remove_tags: removeTags,
      delete_videos: deleteVideos,
      mark_watched: markWatched,
      clear_progress: clearProgress,
    }),
  });

  if (deleteVideos) {
    selectedVideoIds.clear();
  }
  updateBulkActionState();
  bulkAddTagsInputEl.value = "";
  bulkRemoveTagsInputEl.value = "";
  showToast(successMessage || t("bulk_updated"));
  await fetchVideos();
  return data;
}

syncBtnEl.addEventListener("click", async () => {
  if (!currentSync?.configured) {
    window.location.href = "/settings";
    return;
  }

  setButtonBusy(syncBtnEl, true);
  try {
    const data = await requestJson("/api/sync", { method: "POST" });
    updateSyncUI(data.sync);
    ensureSyncPolling();
    schedulePersistListCache();
    showToast(t("sync_started"));
  } catch (error) {
    showToast(error.message, true);
    updateSyncUI(currentSync || { configured: false });
  } finally {
    if (!currentSync?.running) {
      setButtonBusy(syncBtnEl, false);
    }
  }
});

addBtnEl.addEventListener("click", openManualModal);
manualCloseBtnEl.addEventListener("click", closeManualModal);
manualModalEl.addEventListener("click", (event) => {
  if (event.target === manualModalEl) {
    closeManualModal();
  }
});

manualMarkWatchedInputEl.addEventListener("change", () => {
  manualWatchedInputEl.disabled = manualMarkWatchedInputEl.checked;
});

manualFormEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  setButtonBusy(manualSubmitBtnEl, true);

  const formData = new FormData();
  formData.set("url", manualUrlInputEl.value.trim());
  formData.set("watched_time_text", manualWatchedInputEl.value.trim());
  formData.set("mark_watched", manualMarkWatchedInputEl.checked ? "1" : "0");
  formData.set("title", manualTitleInputEl.value.trim());
  formData.set("duration_text", manualDurationInputEl.value.trim());
  formData.set("manual_tags", manualTagsInputEl.value.trim());
  formData.set("note", manualNoteInputEl.value.trim());

  if (manualThumbnailInputEl.files[0]) {
    formData.set("thumbnail", manualThumbnailInputEl.files[0]);
  }

  try {
    await requestJson("/api/manual-video", {
      method: "POST",
      body: formData,
    });
    closeManualModal();
    showToast(t("manual_added_success"));
    await fetchVideos();
  } catch (error) {
    showToast(error.message, true);
  } finally {
    setButtonBusy(manualSubmitBtnEl, false);
  }
});

searchBtnEl.addEventListener("click", () => {
  fetchVideos().catch((error) => showToast(error.message, true));
});

resetBtnEl.addEventListener("click", async () => {
  resetFilters();
  try {
    await fetchVideos();
  } catch (error) {
    showToast(error.message, true);
  }
});

selectVisibleBtnEl.addEventListener("click", () => {
  selectVisibleVideos();
});

clearSelectionBtnEl.addEventListener("click", () => {
  clearSelectedVideos();
});

bulkMarkWatchedBtnEl.addEventListener("click", async () => {
  try {
    await submitBulkAction({
      markWatched: true,
      successMessage: t("bulk_marked_watched_success"),
    });
  } catch (error) {
    showToast(error.message, true);
  }
});

bulkMarkUnwatchedBtnEl.addEventListener("click", async () => {
  try {
    await submitBulkAction({
      clearProgress: true,
      successMessage: t("bulk_marked_unwatched_success"),
    });
  } catch (error) {
    showToast(error.message, true);
  }
});

bulkAddTagsBtnEl.addEventListener("click", async () => {
  try {
    await submitBulkAction({
      addTags: bulkAddTagsInputEl.value.trim(),
      successMessage: t("bulk_add_tags_success"),
    });
  } catch (error) {
    showToast(error.message, true);
  }
});

bulkRemoveTagsBtnEl.addEventListener("click", async () => {
  try {
    await submitBulkAction({
      removeTags: bulkRemoveTagsInputEl.value.trim(),
      successMessage: t("bulk_remove_tags_success"),
    });
  } catch (error) {
    showToast(error.message, true);
  }
});

bulkDeleteBtnEl.addEventListener("click", async () => {
  if (!selectedVideoIds.size) {
    showToast(t("select_videos_error"), true);
    return;
  }
  if (!window.confirm(t("delete_confirm"))) {
    return;
  }
  try {
    await submitBulkAction({
      deleteVideos: true,
      successMessage: t("deleted_success"),
    });
  } catch (error) {
    showToast(error.message, true);
  }
});

clearIndexTagSelectionBtnEl.addEventListener("click", async () => {
  setSelectedDropdownTags([]);
  renderIndexTagDropdown();
  try {
    await fetchVideos();
  } catch (error) {
    showToast(error.message, true);
  }
});

indexTagDropdownToggleEl.addEventListener("click", () => {
  toggleIndexTagDropdown();
});

statusFilterEl.addEventListener("change", () => {
  fetchVideos().catch((error) => showToast(error.message, true));
});

sortFilterEl.addEventListener("change", () => {
  fetchVideos().catch((error) => showToast(error.message, true));
});

searchInputEl.addEventListener("input", () => {
  renderSearchTagSuggestions();
});

searchInputEl.addEventListener("focus", () => {
  renderSearchTagSuggestions();
});

searchInputEl.addEventListener("keydown", async (event) => {
  const items = Array.from(searchSuggestListEl.querySelectorAll(".search-suggest-item"));

  if (event.key === "ArrowDown") {
    if (!items.length) {
      return;
    }
    event.preventDefault();
    searchSuggestionIndex = Math.min(items.length - 1, searchSuggestionIndex + 1);
    highlightSearchSuggestionAt(searchSuggestionIndex);
    return;
  }

  if (event.key === "ArrowUp") {
    if (!items.length) {
      return;
    }
    event.preventDefault();
    searchSuggestionIndex = Math.max(0, searchSuggestionIndex - 1);
    highlightSearchSuggestionAt(searchSuggestionIndex);
    return;
  }

  if (event.key === "Enter") {
    if (searchSuggestionIndex >= 0 && items[searchSuggestionIndex]) {
      event.preventDefault();
      items[searchSuggestionIndex].click();
      return;
    }
    fetchVideos().catch((error) => showToast(error.message, true));
    return;
  }

  if (event.key === "Escape") {
    searchSuggestListEl.hidden = true;
  }
});

jumpSearchBtnEl.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

overviewProgressEl.addEventListener("mouseenter", (event) => {
  cancelOverviewTooltipHide();
  renderOverviewTooltip();
  overviewTooltipEl.hidden = false;
  positionFloatingTooltip(overviewTooltipEl, event);
});

overviewProgressEl.addEventListener("mousemove", (event) => {
  if (overviewTooltipEl.hidden) {
    renderOverviewTooltip();
    overviewTooltipEl.hidden = false;
  }
  positionFloatingTooltip(overviewTooltipEl, event);
});

overviewProgressEl.addEventListener("mouseleave", () => {
  scheduleOverviewTooltipHide();
});

overviewTooltipEl.addEventListener("mouseenter", () => {
  cancelOverviewTooltipHide();
});

overviewTooltipEl.addEventListener("mouseleave", () => {
  scheduleOverviewTooltipHide();
});

window.addEventListener("scroll", updateJumpButton);

document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-suggest-shell")) {
    searchSuggestListEl.hidden = true;
  }
  if (!event.target.closest("#indexTagDropdown")) {
    closeIndexTagDropdown();
  }
  if (!event.target.closest("#overviewProgress") && !event.target.closest("#overviewTooltip")) {
    overviewTooltipEl.hidden = true;
  }
});

async function bootstrap() {
  try {
    const hydrated = hydrateListCache();
    updateIndexTagDropdownLabel();
    updateJumpButton();
    updateBulkActionState();

    if (hydrated) {
      window.requestAnimationFrame(() => {
        fetchVideos().catch((error) => {
          if (error?.name !== "AbortError") {
            showToast(error.message, true);
          }
        });
      });
      return;
    }

    await fetchVideos();
  } catch (error) {
    if (error.name !== "AbortError") {
      showToast(t("init_error", { message: error.message }), true);
    }
  }
}

bootstrap();
