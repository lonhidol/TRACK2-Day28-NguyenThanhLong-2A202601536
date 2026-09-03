# Submission — Day 28 Track 2: Modern AI Platform Integration Lab

- **Họ và tên:** Nguyễn Thành Long
- **Mã sinh viên:** 2A202601536
- **Hình thức thực hiện:** Cá nhân (Bao phủ đầy đủ 5 vai trò kỹ thuật theo chuẩn Integration Matrix)
- **URL Repo Private:** `https://github.com/lonhidol/TRACK2-Day28-NguyenThanhLong-2A202601536.git`
- **Nhánh thực hiện (Branch):** `ca-nhan-NguyenLong`

---

## Danh mục Deliverables & Bằng chứng Nộp bài

### 1. Báo cáo Kết quả Kiểm thử & Integration Matrix
- **Điểm số Readiness Engine:** **83%** (5/6 verified points passing; IP07 unverified do môi trường không có GPU vật lý theo đúng rubric).
- **Chi tiết báo cáo:** [`evidence/integration-report.json`](evidence/integration-report.json)
- **Kết quả chạy Fast Suite:**
  - `uv run ruff check .` -> ✅ **All checks passed**
  - `uv run python scripts/verify_matrix.py` -> ✅ **245/245 checks passed**
  - `uv run python scripts/check_portability.py` -> ✅ **Supported workflow is host-path and shell independent**
  - `uv run python scripts/validate_manifests.py` -> ✅ **Kubernetes and GitOps manifest contracts passed**
  - `uv run pytest tests -q` -> ✅ **83 passed in 15.15s**

### 2. Danh mục 10/10 Evidence Files (Theo Integration Matrix)

| ID | Boundary | File Evidence | Nội dung đã chứng minh |
|---|---|---|---|
| **IP01** | Data ingestion → Kafka | [`evidence/ip01-kafka-consume.json`](evidence/ip01-kafka-consume.json) | Message trên `data.raw`, W3C `traceparent`, `idempotency-key` |
| **IP02** | Kafka → Airflow 3 | [`evidence/ip02-airflow-run.json`](evidence/ip02-airflow-run.json) | DAG run `it-a37d93ab` thành công, 4 task instances, 4 asset events |
| **IP03** | Pipeline → Delta Lake | [`evidence/ip03-delta-history.json`](evidence/ip03-delta-history.json) | Commit history, time travel diff cho `feedback` và `documents` (v0) |
| **IP04** | Delta → Feature Store (Feast) | [`evidence/ip04-feast-online.json`](evidence/ip04-feast-online.json) | Entity `asker_id: it-j1-310f1e4f`, feature service `asker_serving_v1`, `delta_version: 0` |
| **IP05** | Delta → Vector Store (Qdrant) | [`evidence/ip05-qdrant-search.json`](evidence/ip05-qdrant-search.json) | 13 points, MiniLM-L12 embeddings, hybrid search scores & doc_ids |
| **IP06** | Evaluation → MLflow Registry | [`evidence/ip06-mlflow-release.json`](evidence/ip06-mlflow-release.json) | Model `lab28-rag-release` v2 có alias `@champion` |
| **IP07** | RAG prompt → real vLLM | [`evidence/ip07-vllm-identity.json`](evidence/ip07-vllm-identity.json) | Gate GPU: Báo unverified trung thực do không có GPU vật lý (theo rubric) |
| **IP08** | Client → Envoy Gateway | [`evidence/ip08-gateway.json`](evidence/ip08-gateway.json) | Envoy rate limit 10 rps, response 200 & 429 mang `x-request-id` |
| **IP09** | Components → Prometheus/Grafana | [`evidence/ip09-prometheus-targets.json`](evidence/ip09-prometheus-targets.json)<br>[`evidence/ip09-grafana-dashboards.json`](evidence/ip09-grafana-dashboards.json) | 100% active targets UP, provisioned dashboards |
| **IP10** | Components → OTLP Trace | [`evidence/ip10-trace.json`](evidence/ip10-trace.json) | Trace `b3cb298ae16b4eeab647f1d39ed64916` với 19 spans trên Jaeger |

### 3. Architecture & Ownership Diagram
- Sơ đồ kiến trúc 5 tầng, 10 integration points và vai trò:
  - SVG: [`docs/images/lab28-architecture-overview.svg`](docs/images/lab28-architecture-overview.svg)
  - PNG: [`docs/images/lab28-architecture-overview.png`](docs/images/lab28-architecture-overview.png)

### 4. Happy-Path Trace & Bằng chứng Luồng Đúng
- **Dữ liệu Trace:** [`evidence/happy-path-trace.json`](evidence/happy-path-trace.json)
  - **Trace ID:** `b3cb298ae16b4eeab647f1d39ed64916`
  - **Airflow DAG Run ID:** `it-a37d93ab`
  - **MLflow Version:** `2` (alias `@champion`, run ID `731cc00a09f44a908208e089ef6cba83`)
  - **Delta Lake Version:** `0` (bảng `feedback`, `documents`)
- **Ảnh chụp giao diện thực tế:**
  - Jaeger Trace Tree (19 spans): [`evidence/screenshots/jaeger-trace.png`](evidence/screenshots/jaeger-trace.png)
  - MLflow Model Champion: [`evidence/screenshots/mlflow-champion.png`](evidence/screenshots/mlflow-champion.png)
  - Qdrant Vector Points: [`evidence/screenshots/qdrant-collection.png`](evidence/screenshots/qdrant-collection.png)
  - Prometheus Targets UP: [`evidence/screenshots/prometheus-targets.png`](evidence/screenshots/prometheus-targets.png)

### 5. Failure / Recovery Record & No-Data-Loss Proof
- Chi tiết ghi nhận tại: [`evidence/failure-recovery-record.md`](evidence/failure-recovery-record.md)
- **Tóm tắt 4 sự cố đã tái hiện và khắc phục:**
  1. Xung đột cổng 5000 trên macOS do ControlCenter/AirPlay -> chuyển sang cổng 5001.
  2. Mất topics Kafka khi recreate containers -> chạy `uv run lab28 topics` và replay an toàn.
  3. Thiếu GPU vật lý -> kích hoạt cơ chế degraded mode, phản hồi an toàn có ghi chú lý do.
  4. Quá tải request lên Gateway -> kích hoạt HTTP 429 rate limited với `x-request-id`.
- **Chứng minh không mất dữ liệu:** Idempotency key ngăn chặn bản tin lặp, Kafka replay bảo toàn context, hàm `dedupe_latest` sắp xếp deterministic theo `(occurred_at, event_id)` đảm bảo Delta MERGE luôn nhất quán.

### 6. Load Profile & Phân tích Bottleneck
- File kết quả: [`evidence/load-profile.json`](evidence/load-profile.json)
  - **Số lượng request:** 50 requests (4 workers song song)
  - **Tỷ lệ thành công:** 100% (50/50 mã HTTP 200 OK)
  - **Latency:** **P50:** 402.6 ms | **P95:** 1856.6 ms | **P99:** 2852.0 ms
- **Phân tích nút thắt cổ chai:**
  - Endpoint `/ready` kiểm tra đồng thời nhiều backend (Kafka, Delta log, Feast, Qdrant, MLflow) khiến tail latency tăng dưới tải đồng thời.
  - Rate limiting của Gateway giới hạn ở 10 rps.
  - CPU FastEmbed không có gia tốc phần cứng.
  - *Giải pháp:* Caching trạng thái probe bằng Redis TTL 3-5s.

### 7. Kubernetes & GitOps Validation
- Kết quả chạy lệnh kiểm tra: `uv run python scripts/validate_manifests.py` -> **Passed**.
- Các manifest trong `deploy/` và `gitops/` tuân thủ đúng Gateway API spec, hỗ trợ đồng bộ Argo CD và rollback desired-state.

### 8. Contribution & Reflection (ANSWERS.md)
- Chi tiết đầy đủ tại: [`ANSWERS.md`](ANSWERS.md)
  - **Phần phụ trách cá nhân:** Bao phủ trọn vẹn cả 5 vai trò kỹ thuật (Ingestion & Orchestration, Data & ML, Serving & Retrieval, Platform & Observability, Presenter / Incident Commander).
  - **Reflection:**
    1. *Điều khó nhất:* Bảo toàn tính liên tục của W3C Trace Context (`traceparent`) qua ranh giới bất đồng bộ Kafka -> Airflow.
    2. *Trade-offs đã chọn:* Degraded mode thay vì crash 500 khi thiếu GPU; FastEmbed ONNX INT8 nhẹ cho tính portability; deterministic sorting theo idempotency-key.
    3. *Điều sẽ cải tiến:* Triển khai Argo CD GitOps trên cụm K8s thực tế, kết nối GPU worker cho vLLM, và thêm caching layer cho probes.
