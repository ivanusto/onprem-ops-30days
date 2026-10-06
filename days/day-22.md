<!-- DAY:START -->
# Day 22：被擋下的封包才是便宜情報：從防火牆靜默盲點到日誌降噪與自動化告警

- 狀態：已發表
- 發表日期：2026-10-06
- 文章：https://ithelp.ithome.com.tw/articles/10421745
- 類別：`change-mgmt`

| 專案 | tag | commit | 重點檔案 |
|---|---|---|---|
| [ivanusto/onprem-logs](https://github.com/ivanusto/onprem-logs) | [v0.2.0](https://github.com/ivanusto/onprem-logs/tree/v0.2.0) | `384b3d6` | [firewall/fw-report.py](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/firewall/fw-report.py)<br>[firewall/queries.md](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/firewall/queries.md)<br>[firewall/pve-firewall.md](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/firewall/pve-firewall.md)<br>[firewall/pvefw-journal.service](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/firewall/pvefw-journal.service)<br>[firewall/collector-docker-user-log.md](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/firewall/collector-docker-user-log.md)<br>[firewall/collector.cron](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/firewall/collector.cron)<br>[collector/docker-user-allowlist.sh](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/collector/docker-user-allowlist.sh)<br>[archive/archive-day.sh](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/archive/archive-day.sh)<br>[retention.md](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/retention.md)<br>[tests/smoke-firewall.sh](https://github.com/ivanusto/onprem-logs/tree/384b3d6cf6ab036ffd528e57001fcb21f46a3921/tests/smoke-firewall.sh) |
| [ivanusto/onprem-metrics](https://github.com/ivanusto/onprem-metrics) | [v0.2.2](https://github.com/ivanusto/onprem-metrics/tree/v0.2.2) | `992902b` | [prometheus/rules/firewall.yml](https://github.com/ivanusto/onprem-metrics/tree/992902b0da858eb8270964617d2442ee5cfafc2d/prometheus/rules/firewall.yml)<br>[tests/rules_test.yml](https://github.com/ivanusto/onprem-metrics/tree/992902b0da858eb8270964617d2442ee5cfafc2d/tests/rules_test.yml)<br>[alertmanager/alertmanager.yml.example](https://github.com/ivanusto/onprem-metrics/tree/992902b0da858eb8270964617d2442ee5cfafc2d/alertmanager/alertmanager.yml.example) |
<!-- DAY:END -->

## 摘要

## 怎麼跑

## 延伸閱讀
