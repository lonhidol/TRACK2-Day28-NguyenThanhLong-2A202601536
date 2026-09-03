# Screenshots Guide

## Cần chụp ảnh từ các dashboards đang chạy:

### 1. Architecture Diagram
- **Link:** `docs/images/lab28-architecture-overview.png`
- **Đã có:** ✅

### 2. Prometheus Targets (Metrics)
- **Link:** http://localhost:9090/targets
- **Cần chụp:** Tất cả targets đang UP (trừ vLLM expected down)
- **Chứng minh:** IP09 - All components → Prometheus

### 3. Grafana Dashboard (Golden Signals)
- **Link:** http://localhost:3000
- **Cần chụp:** Dashboard overview với metrics
- **Chứng minh:** IP09 - Metrics visible

### 4. Jaeger Trace (Trace Continuity)
- **Link:** http://localhost:16686
- **Cần chụp:** Trace list hoặc 1 trace detail
- **Chứng minh:** IP10 - Trace spans across services

### 5. Gateway Health + Rate Limit
- **Command:**
```bash
curl -s http://localhost:8080/health
curl -i http://localhost:8080/api/v1/documents -X POST -H "Content-Type: application/json" -d '{"doc_id":"test-ss","title":"Screenshot","text":"Test document for screenshot evidence"}'
```
- **Chứng minh:** IP08 - Gateway policy, x-request-id

### 6. Kafka Topics
- **Command:**
```bash
docker compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
```
- **Hoặc:** `uv run lab28 topics`
- **Chứng minh:** IP01 - Topics created

### 7. MLflow Champion
- **Link:** http://localhost:5001
- **Cần chụp:** Model registered với alias "champion"
- **Chứng minh:** IP06 - MLflow Model Registry

### 8. Qdrant Collection
- **Link:** http://localhost:6333/dashboard
- **Cần chụp:** Collection với points
- **Chứng minh:** IP05 - Vector store indexed

### 9. API /ready Response
- **Command:**
```bash
curl -s http://localhost:8000/ready | jq .
```
- **Chứng minh:** Readiness status

### 10. Load Test Results
- **Command:**
```bash
uv run python load-tests/run_profile.py --requests 20 --workers 4
```
- **Chứng minh:** P50/P95/P99 latency

## Cách chụp nhanh:

1. Mở browser trên các links trên
2. Chụp ảnh màn hình
3. Lưu vào folder `evidence/screenshots/`
4. Commit và push

## Các dashboard URLs:
- Gateway: http://localhost:8080
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Jaeger: http://localhost:16686
- MLflow: http://localhost:5001
- Qdrant: http://localhost:6333/dashboard
- Airflow: http://localhost:8082 (admin/admin)
