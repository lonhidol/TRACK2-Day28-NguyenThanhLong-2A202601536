# ANSWERS.md — Day 28 Track 2 Reflection

## 1. Trade-offs kỹ thuật

### IP01 — Kafka Headers (event_headers)
- **Trade-off:** Cần truyền cả `idempotency-key` (bắt buộc) và `traceparent` (tùy chọn)
- **Quyết định:** Không gửi `traceparent` khi không có trace đang hoạt động, tránh header rỗng/invalid
- **Kết quả:** Header luôn ở dạng bytes để Kafka header API yêu cầu
- **Trạng thái:** ✅ IP01 ready — Kafka topics created, events accepted

### IP03 — Delta Deduplication (dedupe_latest)
- **Trade-off:** Kafka có thể gửi lại bản tin (replay), nhưng Delta MERGE cần merge key
- **Quyết định:** So sánh `(occurred_at, event_id)` để giữ bản tin mới nhất, dùng idempotency_key làm merge key
- **Kết quả:** Kết quả deterministic theo thứ tự idempotency_key (sắp xếp) để đảm bảo replay cho cùng output
- **Trạng thái:** ⚠️ IP03 not_ready — Delta tables chưa tồn tại (cần Airflow/Spark)

### IP04 — Feast Feature Request (feast_online_request)
- **Trade-off:** Feast yêu cầu format chính xác: entities, features, full_feature_names
- **Quyết định:** Dùng `FEATURE_REFS` từ contracts.py thay vì hardcode để tránh inconsistency
- **Kết quả:** Request format đúng với feature registry
- **Trạng thái:** ✅ IP04 ready — Feast healthy

### IP07/IP08 — Readiness Status (readiness_status)
- **Trade-off:** Phân biệt giữa mandatory failure (not_ready) và optional failure (degraded)
- **Quyết định:** Thứ tự kiểm tra: mandatory failed → not_ready, optional failed → degraded, còn lại → ready
- **Kết quả:** Gateway có thể quyết định remove pod hay vẫn giữ với degraded mode
- **Trạng thái:** ⚠️ IP07 not_ready — vLLM /health returned 404 (không có GPU)

## 2. Production gaps

| Gap | Mô tả | Mức độ ảnh hưởng |
|-----|-------|-------------------|
| GPU/vLLM | Không có GPU thật, vLLM ở not_ready mode | Cao - ảnh hưởng IP07 |
| Airflow/Spark | Chưa chạy profile=full để tạo Delta tables | Cao - ảnh hưởng IP03 |
| IP02 (Airflow DAG) | Airflow chưa được start | Trung bình - IP02 unverified |
| Kubernetes/GitOps | Chưa triển khai trên K8s | Thấp - CI/CD pipeline |
| IP08 (Gateway) | Rate limiting triggered, cần gateway evidence | Trung bình |
| IP09 (Prometheus) | Metrics collection | Thấp - observability |
| IP10 (Trace) | OpenTelemetry tracing | Thấp - observability |
| Security | Không có authentication/authorization | Cao - production |

## 3. Contribution

### Cá nhân (NguyenThanhLong)

| Phần | Mô tả | Thời gian |
|------|-------|-----------|
| IP01 event_headers | Implement Kafka headers với trace và idempotency | 30 phút |
| IP03 dedupe_latest | Implement deduplication logic với replay safety | 45 phút |
| IP04 feast_online_request | Implement Feast feature request builder | 15 phút |
| IP07/IP08 readiness_status | Implement readiness state machine | 20 phút |
| Testing | Unit tests và integration tests | 30 phút |
| Docker setup | Cài môi trường, chạy Docker compose | 90 phút |
| Evidence collection | lab28 evidence, integration report | 30 phút |

**Tổng thời gian:** ~4.5 giờ

### Các vấn đề đã debug
1. `KeyError` trong `dedupe_latest` — logic so sánh được gọi trước khi check key tồn tại
2. Dòng quá dài (ruff E501) — format code theo line-length 100
3. Feast request dùng `feature_refs` thay vì `features` theo test
4. Docker port 5000 bị chiếm bởi ControlCenter
5. Rate limiting (429) khi seed qua gateway

### Học được
- Kafka idempotency và deduplication pattern
- W3C trace context propagation
- Feast online feature serving
- Readiness probe semantics (ready/degraded/not_ready)
- Delta Lake MERGE operations
- Docker compose networking và port management

## 4. Kết quả Integration Points

| IP | Trạng thái | Ghi chú |
|----|-------------|---------|
| IP01 Kafka | ✅ ready | 4 topics created, events accepted |
| IP02 Airflow | ⚠️ unverified | Cần Airflow run |
| IP03 Delta | ⚠️ not_ready | Cần Spark/Airflow |
| IP04 Feast | ✅ ready | Feature store healthy |
| IP05 Qdrant | ✅ ready | 13 points indexed |
| IP06 MLflow | ✅ ready | v1 champion registered |
| IP07 vLLM | ⚠️ not_ready | Không có GPU |
| IP08 Gateway | ⚠️ unverified | Rate limiting hoạt động |
| IP09 Prometheus | ⚠️ unverified | Cần external evidence |
| IP10 Tracing | ⚠️ unverified | Cần external evidence |

**Score: 67%** (4/6 verified points passing)

## 5. Evidence files đã thu thập

- ✅ evidence/ip05-qdrant-search.json
- ✅ evidence/ip06-mlflow-release.json
- ✅ evidence/ip07-vllm-identity.json
- ✅ evidence/integration-report.json

**Outstanding (cần từ external sources):**
- ip01-kafka-consume.json — integration test
- ip02-airflow-run.json — Airflow DAG run
- ip04-feast-online.json — Feast materialization
- ip08-gateway.json — Gateway rate limiting
- ip09-prometheus-targets.json — Prometheus scrape
- ip10-trace.json — Trace backend
