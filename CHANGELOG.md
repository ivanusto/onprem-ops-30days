# Changelog

本 repo 只在里程碑打 tag。每日進度看 commit 紀錄（`day-NN: 標題`）。

## 未發行

- onprem-changes 改寫 CR-2026-0012 之後的歷史，v0.2.0、v0.3.0 的 SHA 隨之改變，Day 28、29 改釘新的 SHA（tag 名稱不變，v0.1.0 不受影響）。

## v1.0.0（2026-10-14）

系列完賽，Day 1 到 30 全數發表。與 `part-3` 打在同一個 commit。

- 30 篇文章、23 個 repo，每一篇都釘在專案 repo 的 tag 與 SHA，CI 每週一驗 tag 沒有被移動、文章連結還開得起來。

## part-3（2026-10-14）

第三段「指標、日誌、變更與稽核」Day 19 到 30 全數發表。

- Day 19 到 29 改為已發表，釘 onprem-metrics、onprem-logs、fortigate-log-viewer、onprem-changes、onprem-agent-gate 的 tag 與 SHA。
- Day 30：`series.yaml` 新增 `repos` 段（23 個 repo 的 `runs`、`fate`、`note`），`check.py` 驗 repos 與 days 一對一及欄位合法值，`render.py` 在 README 產生「專案一覽」。
- Day 30：成本模型 `lab/cost.yaml` 與 `scripts/cost.py`（累進電價的邊際段、攤提、雲端對照，回本只算被雲端取代的設備），`tests/` 的手算測試進 CI；可維運檢查清單 `lab/checklist.md`；`lab/inventory.md` 依場域實況更正。

## part-2（2026-10-02）

第二段「容量規劃、GPU 節點、儲存與備份」Day 9 到 18 全數發表。

- Day 9 到 18 改為已發表，各自釘在專案 repo 的 tag 與 SHA：open-model-selector、dsv41-flash-vllm030-2x-gb10、spark-baseline、gb10-ops、nfs-model-library、storage-path-bench、pve-qdevice-on-qnap、pve-backup-drill、nas-backup-drill、cloud-offload-drill。
- 2026-09-24 調整第二段排程：Day 10 插入補丁移植，原 Day 16 快照與 Day 17 3-2-1 合併為 Day 17，Day 18 改為異地物件儲存。

## part-1（2026-09-25）

第一段「開源服務封裝」Day 1 到 8 全數發表。tag 打在 Day 8 補登為已發表的 commit（`dde9b9e`），當時 Day 9 到 11 也已發表。

- Day 1 到 8 改為已發表，釘 qpkg-template、Jellyfin-QPKG、roon-qpkg、changedetection-qpkg、homepage-qpkg、qnap-comfyui-qpkg、open-webui-ollama-qpkg 的 tag 與 SHA。

## 初始版本

- 建立索引骨架：`series.yaml`、`scripts/render.py`、`scripts/check.py`、CI。
- 依路線圖先填入 Day 1 到 30 的暫定標題。
