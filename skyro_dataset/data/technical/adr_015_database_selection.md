# Architecture Decision Record: Database Selection for Transaction Storage

**ADR Number:** 015  
**Status:** Accepted  
**Date:** September 15, 2024  
**Decision Makers:** Alex Kumar (Principal Engineer), Jennifer Liu (Senior Engineer), David Thompson (VP Engineering)  
**Consulted:** Database Team, Infrastructure Team, Security Team

## Context and Problem Statement
Skyro's current transaction database (PostgreSQL 13) is reaching scalability limits as we approach 10,000 transactions per second. We need to select a database solution that can:
- Handle 30,000+ TPS with room to scale to 100,000 TPS
- Provide strong consistency for financial transactions (ACID guarantees)
- Support complex queries for reporting and analytics
- Ensure data durability and disaster recovery
- Maintain low latency (<100ms for writes, <50ms for reads)
- Be cost-effective at scale

## Decision Drivers
1. **Scalability**: Must handle 3x current load immediately, 10x within 2 years
2. **Consistency**: Financial data requires strong consistency guarantees
3. **Latency**: Payment processing latency directly impacts user experience
4. **Cost**: Infrastructure costs are significant at our scale
5. **Team Expertise**: Minimize learning curve and operational complexity
6. **Compliance**: Must support audit logs and data retention requirements
7. **Multi-region**: Support for global deployment with low latency

## Options Considered

### Option 1: PostgreSQL (Current) with Optimization
**Approach:** Upgrade to PostgreSQL 15, implement read replicas, partition tables, optimize queries

**Pros:**
- Team already has deep expertise
- Mature ecosystem with excellent tooling
- Strong ACID guarantees
- No migration required
- Open source with no licensing costs

**Cons:**
- Vertical scaling limitations (eventual ceiling)
- Complex sharding would be required for massive scale
- Read replicas add complexity to application logic
- Limited built-in multi-region support

**Estimated Cost:** ₱25,000/month (current: ₱18,000/month)

### Option 2: CockroachDB
**Approach:** Distributed SQL database with PostgreSQL compatibility

**Pros:**
- Strong consistency with distributed architecture
- Horizontal scalability (theoretically unlimited)
- PostgreSQL wire protocol (minimal application changes)
- Built-in multi-region support
- Automatic rebalancing and failover
- No single point of failure

**Cons:**
- Relatively newer technology (less mature than PostgreSQL)
- Higher latency for single-row operations compared to PostgreSQL
- Limited team expertise (learning curve)
- More complex to operate and debug
- Higher cost at smaller scales

**Estimated Cost:** ₱45,000/month at target scale

### Option 3: Amazon DynamoDB
**Approach:** Fully managed NoSQL database with conditional writes for consistency

**Pros:**
- Proven scalability (handles millions of TPS)
- Fully managed (minimal operational overhead)
- Pay-per-request pricing can be cost-effective
- Single-digit millisecond latency
- Excellent multi-region support (Global Tables)

**Cons:**
- NoSQL model requires significant application refactoring
- Limited query capabilities (no joins, limited indexing)
- Eventual consistency model conflicts with financial requirements
- Vendor lock-in to AWS
- Complex pricing model
- Team has no DynamoDB expertise

**Estimated Cost:** ₱65,000/month at target scale (highly variable)

### Option 4: Hybrid Approach (PostgreSQL + Read Replicas + Caching)
**Approach:** Keep PostgreSQL for writes, add read replicas and Redis caching layer

**Pros:**
- Minimal changes to existing system
- Proven pattern used by many companies
- Can handle read-heavy workloads efficiently
- Caching reduces database load significantly
- Team familiar with all components

**Cons:**
- Cache invalidation complexity
- Eventual consistency between replicas and cache
- Still limited by PostgreSQL write scalability
- More moving parts to manage
- Doesn't solve core scalability issue long-term

**Estimated Cost:** ₱35,000/month

## Decision Outcome

**Chosen Option:** **Option 2 - CockroachDB**

### Rationale
After extensive evaluation and load testing, we chose CockroachDB for the following reasons:

1. **Scalability Without Compromise:** CockroachDB provides horizontal scalability while maintaining ACID guarantees, which is critical for financial transactions. Unlike NoSQL options, we don't have to sacrifice consistency.

2. **PostgreSQL Compatibility:** Our application uses PostgreSQL-specific features. CockroachDB's wire protocol compatibility means we can migrate with minimal code changes (estimated <5% of queries need modification).

3. **Multi-Region by Design:** Built-in geo-partitioning and replication support our global expansion plans without complex application-level logic.

4. **Future-Proof:** While more expensive initially, CockroachDB scales linearly. This avoids a future re-architecture when we hit PostgreSQL limits.

5. **Risk Mitigation:** Load testing showed CockroachDB handling 50,000 TPS with p95 latency of 45ms, proving it can handle our growth trajectory.

### Trade-offs Accepted
- **Higher Cost:** 80% increase in database costs (₱45k vs ₱25k/month)
- **Learning Curve:** Team needs 2-3 months to build operational expertise
- **Query Performance:** Some complex analytical queries 20-30% slower than PostgreSQL
- **Maturity:** Newer technology means potential for undiscovered edge cases

### Migration Strategy
**Phase 1 (Month 1-2):** Setup and Testing
- Deploy CockroachDB cluster in staging
- Migrate schema and run parallel writes
- Performance testing and query optimization
- Team training and runbook creation

**Phase 2 (Month 3):** Gradual Migration
- Start dual-writing to both databases
- Read from PostgreSQL (primary)
- Validate data consistency daily
- Monitor CockroachDB performance

**Phase 3 (Month 4):** Cutover
- Week 1: Shift 25% of reads to CockroachDB
- Week 2: Shift 50% of reads to CockroachDB
- Week 3: Shift 100% of reads to CockroachDB
- Week 4: CockroachDB becomes primary, stop writing to PostgreSQL

**Phase 4 (Month 5):** Cleanup
- Keep PostgreSQL as cold backup for 30 days
- Decommission PostgreSQL
- Remove dual-write logic from application

### Rollback Plan
- Can revert to PostgreSQL at any point during Phase 2-3
- After Phase 4, rollback would require restoring from backups
- Maintain PostgreSQL for 90 days post-migration as safety net

## Validation and Monitoring

### Load Testing Results
Performed 3-week load test with production-like traffic:
- **Test Load:** 30,000 TPS sustained, 50,000 TPS peak
- **Write Latency:** p50: 12ms, p95: 45ms, p99: 89ms
- **Read Latency:** p50: 8ms, p95: 28ms, p99: 52ms
- **Success Rate:** 99.98%
- **Consistency:** Zero data loss or inconsistencies detected

### Success Criteria
CockroachDB migration will be considered successful if:
1. Sustained 30,000+ TPS in production
2. Write latency p95 < 80ms
3. Read latency p95 < 50ms
4. Zero data loss incidents
5. Transaction success rate ≥ 99.95%
6. Cost within 20% of projection

### Monitoring Plan
- Real-time dashboards for latency, throughput, and error rates
- Automated alerts for latency >100ms or error rate >0.1%
- Daily data consistency checks between systems during migration
- Weekly performance review meetings during first 3 months

## Consequences

### Positive
- Eliminates database as scalability bottleneck for next 3-5 years
- Supports multi-region deployment for global expansion
- Reduces operational burden compared to sharding PostgreSQL
- Strong consistency maintains data integrity for financial transactions
- Automatic failover improves system reliability

### Negative
- Higher infrastructure costs (₱27k/month increase)
- 3-month migration period with associated engineering effort
- Team learning curve may slow down other initiatives temporarily
- Some complex queries need optimization
- Newer technology carries some unknown risks

### Neutral
- Application code changes minimal but required
- Operational procedures need to be rewritten
- Backup and disaster recovery processes need updating

## Related Decisions
- ADR-012: Microservices architecture (supports distributed database)
- ADR-014: Multi-region deployment strategy (requires distributed database)
- ADR-016: API rate limiting (will use CockroachDB for state storage)

## References
- [CockroachDB Architecture Whitepaper](internal link)
- [Load Testing Results](internal link)
- [Cost Analysis Spreadsheet](internal link)
- [PostgreSQL Performance Analysis](internal link)

## Lessons Learned (Post-Implementation Update)
*To be added after migration completion (estimated March 2025)*

## Notes
- This decision was made after 6 weeks of evaluation including POC development
- Alternative to CockroachDB was continuing with PostgreSQL and re-evaluating in 12 months
- Finance team approved increased infrastructure budget
- Security team reviewed and approved CockroachDB from compliance perspective

**Approval:** David Thompson (VP Engineering) - Approved September 20, 2024
