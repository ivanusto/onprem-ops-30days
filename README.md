# 地端維運三十天：系列文章與程式碼索引

一套跑得起來的地端環境，要補上哪些東西，才能被稱為可長期維運。

這個 repo 是鐵人賽系列「地端維運三十天」的總索引。每一天的文章儘量對應一個可執行的 GitHub 專案（套件、腳本或範本），這裡記錄文章與程式碼的對應關係，並把每一篇釘在專案當天的版本上。

前一系列：[128GB 統一記憶體的三十天：DGX Spark 地端 LLM 與生成式 AI 部署實戰](https://ithelp.ithome.com.tw/users/20141816/ironman/9217)

## 怎麼讀這份索引

- **程式碼欄連到的是 tag，不是 main。** 專案會持續演進，文章描述的是發表當天的版本。想看最新版，進 repo 後切回預設分支即可。
- **tag 可能被移動，SHA 不會。** 每一筆都另外記錄 tag 指向的 commit SHA，`days/day-NN.md` 內的檔案連結直接釘在 SHA 上。
- **同一個專案可能出現在不同天**，各自對應不同的 tag。
- 實驗場域的設備清單見 [lab/inventory.md](lab/inventory.md)。

## 四類維運問題

| 類別 | 代號 | 要解決的事 |
|---|---|---|
| 服務沒有被封裝 | `packaging` | 可安裝、可升級、可驗證的套件，打包過程可重現 |
| 節點沒有被守護 | `node-guard` | 熱與記憶體邊界的取樣、告警與自動降載 |
| 儲存與備份沒有被治理 | `storage-backup` | 權限、版本、校驗碼、保留期限、還原演練 |
| 變更沒有被記錄 | `change-mgmt` | 誰在什麼時候改了什麼、能不能回滾 |

## 索引

<!-- INDEX:START -->
### 第一段：開源服務封裝

| Day | 主題 | 類別 | 文章 | 程式碼 |
|---:|---|---|---|---|
| [01](days/day-01.md) | 前言：第二個三十天，換一個問題 | `overview` | 撰寫中 |   |
| [02](days/day-02.md) | 薄殼架構 | `packaging` | 即將發表 | [open-webui-ollama-qpkg@v1.0.7](https://github.com/ivanusto/open-webui-ollama-qpkg/tree/v1.0.7) |
| [03](days/day-03.md) | Open WebUI 加 Ollama 封裝（暫定） | `packaging` | 即將發表 |   |
| [04](days/day-04.md) | ComfyUI 封裝（暫定） | `packaging` | 即將發表 |   |
| [05](days/day-05.md) | Jellyfin 與 Roon 封裝（暫定） | `packaging` | 即將發表 |   |
| [06](days/day-06.md) | changedetection.io 與 Homepage 封裝（暫定） | `packaging` | 即將發表 |   |
| [07](days/day-07.md) | GitHub Actions 自動打包與 release（暫定） | `packaging` | 即將發表 |   |
| [08](days/day-08.md) | image digest 鎖定與 SHA256SUMS（暫定） | `packaging` | 即將發表 |   |

### 第二段：容量規劃、GPU 節點、儲存與備份

| Day | 主題 | 類別 | 文章 | 程式碼 |
|---:|---|---|---|---|
| [09](days/day-09.md) | 容量規劃：模型與硬體搭配矩陣（暫定） | `node-guard` | 即將發表 |   |
| [10](days/day-10.md) | DGX Spark 節點基線（暫定） | `node-guard` | 即將發表 |   |
| [11](days/day-11.md) | 熱與記憶體守護（暫定） | `node-guard` | 即將發表 |   |
| [12](days/day-12.md) | NFS 集中模型庫的權限與版本治理（暫定） | `storage-backup` | 即將發表 |   |
| [13](days/day-13.md) | 儲存路徑實測（暫定） | `storage-backup` | 即將發表 |   |
| [14](days/day-14.md) | Proxmox VE 雙節點 HA（暫定） | `storage-backup` | 即將發表 |   |
| [15](days/day-15.md) | Proxmox VE 備份與還原演練（暫定） | `storage-backup` | 即將發表 |   |
| [16](days/day-16.md) | NAS 快照（暫定） | `storage-backup` | 即將發表 |   |
| [17](days/day-17.md) | 3-2-1 備份（暫定） | `storage-backup` | 即將發表 |   |
| [18](days/day-18.md) | 媒體庫外移 GCS 與 S3（暫定） | `storage-backup` | 即將發表 |   |

### 第三段：可觀測性、資安維運與可稽核的變更管理

| Day | 主題 | 類別 | 文章 | 程式碼 |
|---:|---|---|---|---|
| [19](days/day-19.md) | 指標收集（暫定） | `node-guard` | 即將發表 |   |
| [20](days/day-20.md) | Grafana 儀表板（暫定） | `node-guard` | 即將發表 |   |
| [21](days/day-21.md) | 日誌集中與保存（暫定） | `change-mgmt` | 即將發表 |   |
| [22](days/day-22.md) | 防火牆日誌判讀（暫定） | `change-mgmt` | 即將發表 |   |
| [23](days/day-23.md) | 網路封包擷取與分析（暫定） | `change-mgmt` | 即將發表 |   |
| [24](days/day-24.md) | 維運工作站（暫定） | `change-mgmt` | 即將發表 |   |
| [25](days/day-25.md) | 資產 EOL 監看（暫定） | `change-mgmt` | 即將發表 |   |
| [26](days/day-26.md) | 變更管理（暫定） | `change-mgmt` | 即將發表 |   |
| [27](days/day-27.md) | 稽核軌跡（暫定） | `change-mgmt` | 即將發表 |   |
| [28](days/day-28.md) | 回滾與變更演練（暫定） | `change-mgmt` | 即將發表 |   |
| [29](days/day-29.md) | AI Agent 進入維運流程的授權閘道（暫定） | `change-mgmt` | 即將發表 |   |
| [30](days/day-30.md) | 一年成本與用電總結（暫定） | `change-mgmt` | 即將發表 |   |

<!-- INDEX:END -->

## 維護方式

資料只寫在 [`series.yaml`](series.yaml)，README 的索引表與 `days/*.md` 的表頭都由腳本產生。

```bash
pip install pyyaml
python3 scripts/render.py            # 產生索引表與每日頁面表頭
python3 scripts/render.py --check    # 只檢查是否已同步（CI 使用）
GITHUB_TOKEN=$(gh auth token) python3 scripts/check.py   # 驗證 tag、SHA、檔案路徑、文章連結與文字
python3 scripts/check.py --offline   # 只做欄位與文字檢查
```

每日發文流程：

1. 在專案 repo 打 release tag 並建 GitHub Release，Release notes 回連文章。
2. 更新 `series.yaml` 該天條目：填 `date`、`article`、`tag`、`sha`，`status` 改為 `published`。
3. 執行 `render.py` 與 `check.py`，commit 訊息格式為 `day-NN: 標題`。
4. 文章結尾連到本 repo 與專案的 `tree/<tag>`。

本 repo 只在里程碑打 tag：`part-1`（Day 8）、`part-2`（Day 18）、`v1.0.0`（Day 30）。

## 授權

腳本以 MIT 授權釋出。文章內容著作權屬原作者，各專案依其 repo 內的授權條款。
