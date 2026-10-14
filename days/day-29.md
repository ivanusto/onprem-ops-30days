<!-- DAY:START -->
# Day 29：打造地端維運的 AI 圍欄：Agent 授權閘道實作，無工單即無工具，無核准即無不可逆變更

- 狀態：已發表
- 發表日期：2026-10-13
- 文章：https://ithelp.ithome.com.tw/articles/10424017
- 類別：`change-mgmt`

| 專案 | tag | commit | 重點檔案 |
|---|---|---|---|
| [ivanusto/onprem-agent-gate](https://github.com/ivanusto/onprem-agent-gate) | [v0.1.0](https://github.com/ivanusto/onprem-agent-gate/tree/v0.1.0) | `d123e11` | [gate/core.py](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/gate/core.py)<br>[gate/mcp_server.py](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/gate/mcp_server.py)<br>[bin/gatectl](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/bin/gatectl)<br>[bin/gate-mcp](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/bin/gate-mcp)<br>[tools.json](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/tools.json)<br>[config.json.example](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/config.json.example)<br>[prometheus/agent.yml](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/prometheus/agent.yml)<br>[docs/targets.md](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/docs/targets.md)<br>[docs/mcp-clients.md](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/docs/mcp-clients.md)<br>[docs/iso27001.md](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/docs/iso27001.md)<br>[tests](https://github.com/ivanusto/onprem-agent-gate/tree/d123e111c8a2994fab1d10491bf2b81e68fa3f61/tests) |
| [ivanusto/onprem-changes](https://github.com/ivanusto/onprem-changes) | [v0.3.0](https://github.com/ivanusto/onprem-changes/tree/v0.3.0) | `6b4b76d` | [changes/CR-2026-0015-agent-gate-qdevice.md](https://github.com/ivanusto/onprem-changes/tree/6b4b76d17062d8aa5ec4310e111127418bc638ed/changes/CR-2026-0015-agent-gate-qdevice.md)<br>[changes/TEMPLATE.md](https://github.com/ivanusto/onprem-changes/tree/6b4b76d17062d8aa5ec4310e111127418bc638ed/changes/TEMPLATE.md)<br>[scripts/check.py](https://github.com/ivanusto/onprem-changes/tree/6b4b76d17062d8aa5ec4310e111127418bc638ed/scripts/check.py) |
| [ivanusto/onprem-logs](https://github.com/ivanusto/onprem-logs) | [v0.5.4](https://github.com/ivanusto/onprem-logs/tree/v0.5.4) | `d154598` | [audit/audit-report.py](https://github.com/ivanusto/onprem-logs/tree/d15459843b58819c6fdcd6d52289697c94895f9a/audit/audit-report.py)<br>[audit/queries.md](https://github.com/ivanusto/onprem-logs/tree/d15459843b58819c6fdcd6d52289697c94895f9a/audit/queries.md)<br>[tests/smoke-audit.sh](https://github.com/ivanusto/onprem-logs/tree/d15459843b58819c6fdcd6d52289697c94895f9a/tests/smoke-audit.sh) |
| [ivanusto/onprem-metrics](https://github.com/ivanusto/onprem-metrics) | [v0.3.4](https://github.com/ivanusto/onprem-metrics/tree/v0.3.4) | `2dfbdb5` | [prometheus/rules/agent.yml](https://github.com/ivanusto/onprem-metrics/tree/2dfbdb59ea94d8010714373e3f172dd9a0de5e0d/prometheus/rules/agent.yml)<br>[tests/rules_agent_test.yml](https://github.com/ivanusto/onprem-metrics/tree/2dfbdb59ea94d8010714373e3f172dd9a0de5e0d/tests/rules_agent_test.yml)<br>[alertmanager/alertmanager.yml.example](https://github.com/ivanusto/onprem-metrics/tree/2dfbdb59ea94d8010714373e3f172dd9a0de5e0d/alertmanager/alertmanager.yml.example) |
<!-- DAY:END -->

## 摘要

## 怎麼跑

## 延伸閱讀
