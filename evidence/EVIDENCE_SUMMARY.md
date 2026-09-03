# Evidence Summary

## Cách thu thập Evidence

### Từ Terminal (Data)

```bash
# 1. Prometheus Targets
curl -s http://localhost:9090/api/v1/targets | jq '.'

# 2. Gateway Health & Rate Limit
curl -s http://localhost:8080/health
curl -i http://localhost:8080/api/v1/documents -X POST -H "Content-Type: application/json" -d '{"doc_id":"test","title":"Test","text":"Test document"}'

# 3. Kafka Topics
uv run lab28 topics

# 4. System Readiness
uv run lab28 ready

# 5. Integration Report
uv run lab28 integration

# 6. Load Test
uv run python load-tests/run_profile.py --requests 20 --workers 4
```

### Từ Browser (Screenshots)

Mở các links sau và chụp ảnh:

| Service | URL | Evidence |
|---------|-----|----------|
| Architecture | `docs/images/lab28-architecture-overview.png` | IP00 Overview |
| Gateway | http://localhost:8080 | IP08 Gateway |
| API Docs | http://localhost:8000/docs | API Endpoints |
| Grafana | http://localhost:3000 | IP09 Metrics |
| Prometheus | http://localhost:9090/targets | IP09 Targets |
| Jaeger | http://localhost:16686 | IP10 Trace |
| MLflow | http://localhost:5001 | IP06 Model |
| Qdrant | http://localhost:6333/dashboard | IP05 Vector |
| Airflow | http://localhost:8082 | IP02 DAG |

## Evidence Files Index

| File | Source | IP |
|------|--------|-----|
| `ip01-kafka-consume.json` | `lab28 topics` | IP01 |
| `ip02-airflow-run.json` | Airflow UI/API | IP02 |
| `ip03-delta-history.json` | Delta tables | IP03 |
| `ip04-feast-online.json` | Feast probe | IP04 |
| `ip05-qdrant-search.json` | `lab28 evidence` | IP05 |
| `ip06-mlflow-release.json` | MLflow UI | IP06 |
| `ip07-vllm-identity.json` | vLLM /version | IP07 |
| `ip08-gateway.json` | Gateway API | IP08 |
| `ip09-prometheus-targets.json` | Prometheus API | IP09 |
| `ip10-trace.json` | Jaeger API | IP10 |
| `happy-path-trace.json` | Seed output | All |
| `failure-recovery-record.md` | Observations | Recovery |
| `load-profile.json` | Load test | Performance |
| `integration-report.json` | `lab28 integration` | Report |

## Terminal Output Cho Evidence

### Prometheus Targets (IP09)
```
lab28-airflow-batch: up
lab28-api: up
lab28-collector: up
lab28-feast: up
lab28-gateway: up
lab28-kafka: up
lab28-mlflow: up
lab28-prometheus: up
lab28-qdrant: up
lab28-vllm-optional: down (expected - no GPU)
```

### Gateway Response (IP08)
```
HTTP/1.1 202 Accepted
x-request-id: <uuid>
trace_id: <trace_id>
```

### Kafka Topics (IP01)
```
data.raw: created/exists
data.processed: created/exists
model.events: created/exists
data.raw.dlq: created/exists
```

### Readiness Status
```
Kafka: ready
MLflow: ready
Qdrant: ready
Feast: ready
vLLM: not_ready (no GPU)
```
