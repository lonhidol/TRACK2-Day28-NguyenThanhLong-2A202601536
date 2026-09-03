# Dashboard Links & Evidence Collection

## Live Dashboard URLs

### Observability (IP09 - Prometheus/Grafana)
| Dashboard | URL | Username/Password |
|-----------|-----|------------------|
| Prometheus Targets | http://localhost:9090/targets | - |
| Prometheus Graph | http://localhost:9090/graph | - |
| Grafana | http://localhost:3000 | admin/admin |

### Tracing (IP10 - Jaeger)
| Dashboard | URL |
|-----------|-----|
| Jaeger UI | http://localhost:16686 |
| Trace Search | http://localhost:16686/search |

### Serving (IP05/IP07/IP08)
| Service | URL |
|---------|-----|
| Gateway | http://localhost:8080 |
| API Docs | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

### ML/Data (IP06/IP03)
| Service | URL |
|---------|-----|
| MLflow | http://localhost:5001 |
| Airflow | http://localhost:8082 |
| Feast | http://localhost:8080/api/v1/ask |

### Architecture
| Resource | Path |
|----------|-------|
| Architecture Diagram | docs/images/lab28-architecture-overview.png |

---

## Commands to Collect Evidence

### 1. Prometheus Targets (IP09)
```bash
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'
```

### 2. Jaeger Traces (IP10)
```bash
curl -s "http://localhost:16686/api/traces?limit=5" | jq '.data[] | {traceID, spanCount: (.spans | length)}'
```

### 3. Gateway Rate Limit (IP08)
```bash
curl -i http://localhost:8080/api/v1/documents -X POST \
  -H "Content-Type: application/json" \
  -d '{"doc_id":"evidence","title":"Test","text":"Evidence collection"}'
```

### 4. System Readiness
```bash
curl -s http://localhost:8000/ready | jq '.'
```

### 5. Integration Report
```bash
uv run lab28 integration
```

### 6. Load Test
```bash
uv run python load-tests/run_profile.py --requests 20 --workers 4
```

### 7. Kafka Topics
```bash
uv run lab28 topics
```

---

## Evidence Files Index

| File | Description | Command/Source |
|------|-------------|----------------|
| `ip01-kafka-consume.json` | Kafka topics & events | `lab28 topics` |
| `ip02-airflow-run.json` | Airflow service | `docker compose ps` |
| `ip03-delta-history.json` | Delta tables | Pending Airflow DAG |
| `ip04-feast-online.json` | Feast feature store | `lab28 inspect` |
| `ip05-qdrant-search.json` | Vector store | `lab28 evidence` |
| `ip06-mlflow-release.json` | Model registry | `lab28 release` |
| `ip07-vllm-identity.json` | LLM endpoint | `lab28 inspect` |
| `ip08-gateway.json` | Gateway health | Gateway API |
| `ip09-prometheus-targets.json` | Metrics targets | Prometheus API |
| `ip10-trace.json` | Trace spans | Jaeger API |
| `integration-report.json` | IP status | `lab28 integration` |
| `load-profile.json` | Latency P50/P95/P99 | Load test |
| `happy-path-trace.json` | Run/Trace IDs | Seed output |
| `failure-recovery-record.md` | Incident notes | Observations |

---

## Collected Evidence Data

### Prometheus Targets Status
```json
{
  "lab28-airflow-batch": "up",
  "lab28-api": "up",
  "lab28-collector": "up",
  "lab28-feast": "up",
  "lab28-gateway": "up",
  "lab28-kafka": "up",
  "lab28-mlflow": "up",
  "lab28-prometheus": "up",
  "lab28-qdrant": "up",
  "lab28-vllm-optional": "down (expected - no GPU)"
}
```

### Gateway Rate Limit Evidence
```
HTTP/1.1 202 Accepted
x-request-id: <uuid>
trace_id: <uuid>
```

### Readiness Status
```
Kafka: ready
MLflow: ready  
Qdrant: ready
Feast: ready
vLLM: not_ready (no GPU)
```

### Integration Points Score: 67% (4/6 verified)
