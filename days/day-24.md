<!-- DAY:START -->
# Day 24：稽核問「某台工作站上個月連到哪裡了」？FortiGate AUP 雙軌日誌實踐：線上 LogsQL 檢索與離線對帳修煉

- 狀態：已發表
- 發表日期：2026-10-08
- 文章：https://ithelp.ithome.com.tw/articles/10422472
- 類別：`change-mgmt`

| 專案 | tag | commit | 重點檔案 |
|---|---|---|---|
| [ivanusto/onprem-logs](https://github.com/ivanusto/onprem-logs) | [v0.4.0](https://github.com/ivanusto/onprem-logs/tree/v0.4.0) | `429e606` | [firewall/fortigate-webfilter.md](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/firewall/fortigate-webfilter.md)<br>[firewall/aup-report.py](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/firewall/aup-report.py)<br>[firewall/fortigate-export-load.py](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/firewall/fortigate-export-load.py)<br>[firewall/aup-compare.sh](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/firewall/aup-compare.sh)<br>[firewall/rules-aup.yml](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/firewall/rules-aup.yml)<br>[firewall/collector.cron](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/firewall/collector.cron)<br>[retention.md](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/retention.md)<br>[tests/smoke-aup.sh](https://github.com/ivanusto/onprem-logs/tree/429e606931cf88515e4b5524be8f994013e21d62/tests/smoke-aup.sh) |
| [ivanusto/onprem-metrics](https://github.com/ivanusto/onprem-metrics) | [v0.2.3](https://github.com/ivanusto/onprem-metrics/tree/v0.2.3) | `6718ef5` | [prometheus/rules/aup.yml](https://github.com/ivanusto/onprem-metrics/tree/6718ef50074b1a9107f1b123d763c8f2be19b110/prometheus/rules/aup.yml)<br>[tests/rules_aup_test.yml](https://github.com/ivanusto/onprem-metrics/tree/6718ef50074b1a9107f1b123d763c8f2be19b110/tests/rules_aup_test.yml)<br>[alertmanager/alertmanager.yml.example](https://github.com/ivanusto/onprem-metrics/tree/6718ef50074b1a9107f1b123d763c8f2be19b110/alertmanager/alertmanager.yml.example) |
| [ivanusto/fortigate-log-viewer](https://github.com/ivanusto/fortigate-log-viewer) | [v0.1.0](https://github.com/ivanusto/fortigate-log-viewer/tree/v0.1.0) | `375f51e` | [README.md](https://github.com/ivanusto/fortigate-log-viewer/tree/375f51e0ac4cc6b711f782e45f766a8738796bc5/README.md)<br>[src/utils/fortigateParser.js](https://github.com/ivanusto/fortigate-log-viewer/tree/375f51e0ac4cc6b711f782e45f766a8738796bc5/src/utils/fortigateParser.js)<br>[src/utils/reverseDns.js](https://github.com/ivanusto/fortigate-log-viewer/tree/375f51e0ac4cc6b711f782e45f766a8738796bc5/src/utils/reverseDns.js)<br>[Dockerfile](https://github.com/ivanusto/fortigate-log-viewer/tree/375f51e0ac4cc6b711f782e45f766a8738796bc5/Dockerfile)<br>[tests/parser.test.mjs](https://github.com/ivanusto/fortigate-log-viewer/tree/375f51e0ac4cc6b711f782e45f766a8738796bc5/tests/parser.test.mjs) |
<!-- DAY:END -->

## 摘要

## 怎麼跑

## 延伸閱讀
