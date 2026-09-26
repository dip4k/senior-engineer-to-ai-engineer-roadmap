# ADR-042: Adoption of Apache Kafka for Event-Driven Telemetry Ingestion

- **Status**: Accepted
- **Date**: 2026-03-24
- **Deciders**: Principal Architect, Data Platform Lead, Senior Security Engineer
- **Consulted**: DevOps Lead, SRE Lead

---

## Context & Problem Statement
Our IoT edge telemetry ingestion pipeline currently receives 45,000 HTTP POST events per second during peak hours. The current architecture writes directly to a PostgreSQL database pool via an API gateway.

During morning traffic spikes, connection pool exhaustion causes API latency to spike from 35ms to over 4,500ms, triggering cascading HTTP 504 gateway timeouts and dropping approximately 2.3% of inbound sensor telemetry. We require a distributed, decoupled ingestion buffer capable of absorbing 150,000 events/sec with zero message loss while allowing independent downstream consumers to process data at their own pace.

---

## Decision Drivers
- Ingestion throughput: must scale horizontally to support 150,000 events/second.
- Zero data loss tolerance (at-least-once delivery semantics).
- Strict temporal ordering per device ID.
- Consumer decoupling: ability to add analytics, fraud detection, and cold storage consumers without impacting ingestion.
- Operational overhead and infrastructure cost.

---

## Considered Options
1. **Option A**: Apache Kafka (Managed AWS MSK / Confluent Cloud)
2. **Option B**: AWS SQS FIFO Queues
3. **Option C**: RabbitMQ with Consistent Hash Exchange

---

## Decision Outcome
Chosen Option: **Option A (Apache Kafka)**.

### Rationale:
- **Partition-Keyed Ordering**: By utilizing `DeviceId` as the Kafka message partition key, events for any single device are guaranteed to be processed in strict chronological sequence by a single partition consumer.
- **High Throughput & Low Latency**: Kafka's append-only sequential log architecture effortlessly handles 150k events/sec at single-digit millisecond write latencies.
- **Replayability**: Configurable multi-day log retention allows consumer services to be taken down for maintenance and replay state without data loss.

### Discarded Alternatives:
- *AWS SQS FIFO*: Enforces a hard limit of 300 messages/sec (or 3,000/sec with batching), requiring complex multi-queue sharding that introduces excessive operational complexity and cost at 150,000 events/sec.
- *RabbitMQ*: While capable of high throughput, RabbitMQ's performance degrades when queues accumulate millions of unacknowledged messages during downstream outages, lacking native multi-day replay logs.

---

## Consequences & Trade-offs
### Positive:
- Decouples ingestion HTTP edge proxies from downstream analytics processors.
- Provides durable, fault-tolerant event streaming with zero message loss.
- Enables new analytical consumer microservices to subscribe to the same stream independently.

### Negative / Operational Costs:
- Increases operational complexity: requires monitoring consumer lag, partition skew, and rebalance storms.
- Requires team training on distributed log semantics and offset management.
- Infrastructure cost of managed Kafka cluster ($1,800/month baseline).

---

## Compliance & Verification
- CI/CD pipelines must verify that all Kafka event payloads validate against registered Protobuf schemas.
- OpenTelemetry distributed trace contexts must be injected into Kafka message headers for end-to-end tracing.
