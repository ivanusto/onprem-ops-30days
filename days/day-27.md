<!-- DAY:START -->
# Day 27：自動化稽核比對：當機器留下的日誌，對上工程師寫的變更單（VictoriaLogs × FortiGate × PVE）

- 狀態：已發表
- 發表日期：2026-10-11
- 文章：https://ithelp.ithome.com.tw/articles/10423393
- 類別：`change-mgmt`

| 專案 | tag | commit | 重點檔案 |
|---|---|---|---|
| [ivanusto/onprem-logs](https://github.com/ivanusto/onprem-logs) | [v0.5.0](https://github.com/ivanusto/onprem-logs/tree/v0.5.0) | `284aeab` | [audit](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/audit)<br>[archive/archive-day.sh](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/archive/archive-day.sh)<br>[archive/verify-archive.sh](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/archive/verify-archive.sh)<br>[docker-compose.yml](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/docker-compose.yml)<br>[collector/docker-user-allowlist.sh](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/collector/docker-user-allowlist.sh)<br>[retention.md](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/retention.md)<br>[tests/smoke-audit.sh](https://github.com/ivanusto/onprem-logs/tree/284aeabc5461e763ae62a85ab8ab0316070d0a2c/tests/smoke-audit.sh) |
| [ivanusto/onprem-metrics](https://github.com/ivanusto/onprem-metrics) | [v0.3.2](https://github.com/ivanusto/onprem-metrics/tree/v0.3.2) | `5e8264d` | [prometheus/rules/audit.yml](https://github.com/ivanusto/onprem-metrics/tree/5e8264d6d403cb59635c184ac2020db916e96599/prometheus/rules/audit.yml)<br>[tests/rules_audit_test.yml](https://github.com/ivanusto/onprem-metrics/tree/5e8264d6d403cb59635c184ac2020db916e96599/tests/rules_audit_test.yml)<br>[alertmanager/alertmanager.yml.example](https://github.com/ivanusto/onprem-metrics/tree/5e8264d6d403cb59635c184ac2020db916e96599/alertmanager/alertmanager.yml.example) |
<!-- DAY:END -->

## 摘要

## 怎麼跑

## 延伸閱讀
