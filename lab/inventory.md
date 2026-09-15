# 實驗場域設備清單

本系列所有實作與數字主要來自以下環境。清單刻意不列 IP、主機名與序號。

| 角色 | 設備 | 備註 |
|---|---|---|
| GPU 運算節點 | NVIDIA DGX Spark（GB10，128GB 統一記憶體）兩台 | 兩台之間以 QSFP28 100GbE 直連，各自另接 10GbE 交換器 |
| 集中儲存 | QNAP TS-464 | NFS 集中模型庫，所有運算節點掛載同一份模型目錄 |
| 虛擬化 | Proxmox VE 節點伺服器三台 | 承載管理服務、監控與各類工作用 VM |
| GPU 工作站 | Intel 平台，128GB RAM，RTX 5060 Ti 16GB | ComfyUI 與封裝測試用 |
| GPU 工作站 | AMD 平台，32GB RAM，RTX 3060 12GB | 對照組與輕量任務 |
| 工作用筆電 | Apple 平台，24GB RAM，Mac M5 Air | 日常工作與輕量任務 |
| 網路骨幹 | 10GbE 交換器 | Mercury SE106 Pro，有切 VLAN |
| 無線網路 | Wi-Fi 5 基地台 | Fortinet FAP-221E 兩台 |
| 路由器 | 防火牆 | FortiGate 60F |
| 空調 | 冷暖變頻冷氣機 | Panasonic LX |

這不是企業機房的規模，但具備企業機房會遇到的維運問題：多節點、集中儲存、GPU 熱與記憶體的邊界、跨設備的備份與還原，以及稽核時一定會被問到的變更紀錄。
