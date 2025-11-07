# Skyro Internal Knowledge Base - Dataset Overview

**Created:** November 6, 2024  
**Total Documents:** 14  
**Purpose:** Test dataset for AI-powered knowledge assistant prototype

## Document Categories and Contents

### Product & Feature Specifications (1 document)
1. **payment_processing_v2.md** - Product spec for Payment Processing System V2
   - Multi-currency support, architecture, rollout plan
   - Business goals, technical components, success metrics

### Compliance & Legal (1 document)
2. **kyc_process.md** - KYC compliance procedures
   - Customer verification levels, document requirements
   - Risk categories, regulatory compliance

### Technical Documentation (4 documents)
3. **fraud_detection_system.md** - Fraud detection technical architecture
   - ML model details, API endpoints, integration
   - Performance metrics, future enhancements

4. **merchant_api_documentation.md** - Merchant API reference
   - Authentication, endpoints, webhooks
   - Rate limits, testing, code examples

5. **adr_015_database_selection.md** - Architecture Decision Record
   - Database selection rationale (CockroachDB vs alternatives)
   - Trade-offs, migration strategy, validation results

6. **incident_response_playbook.md** - Security incident response procedures
   - Severity levels, response phases, escalation
   - Communication, forensics, post-incident review

### Meeting Notes & Planning (2 documents)
7. **sprint_42_planning.md** - Sprint planning meeting notes
   - Committed stories, capacity planning, risks
   - Action items, decisions made

8. **incident_postmortem_089.md** - Payment gateway outage postmortem
   - Root cause analysis, timeline, impact
   - Lessons learned, action items

### Business & Strategy (2 documents)
9. **q4_2024_okrs.md** - Q4 2024 Objectives and Key Results
   - Company objectives, key results, progress tracking
   - Resource allocation, risks, dependencies

10. **q3_2024_business_review.md** - Quarterly business review
    - Financial performance, operational metrics
    - Strategic initiatives, market analysis, team updates

### Operations & Support (2 documents)
11. **customer_support_faq.md** - Internal customer support knowledge base
    - Common issues, troubleshooting steps, escalation procedures
    - Templates, scripts, contact information

12. **chargeback_procedures.md** - Chargeback handling procedures
    - Chargeback lifecycle, evidence submission
    - Prevention strategies, monitoring, compliance

### Onboarding & Training (1 document)
13. **new_engineer_guide.md** - New engineer onboarding guide
    - Week-by-week onboarding schedule
    - Development setup, engineering practices, resources

### Experiments & Results (1 document)
14. **payment_retry_logic_results.md** - A/B test results for payment retry feature
    - Hypothesis, methodology, results
    - Business impact, recommendations

## Document Statistics

**Total Word Count:** ~47,000 words  
**Total Pages (estimated):** ~150 pages  
**Content Types:**
- Technical specs: 5
- Business/strategy: 3
- Operations/procedures: 3
- Meeting notes: 2
- Reference/FAQ: 1

**File Formats:** All markdown (.md)

## Sample Questions for Testing

### Cross-Document Questions
1. "What are the main causes of the October payment gateway incident and how does it relate to our fraud detection system?"
2. "What is our current chargeback rate and how does it compare to our payment success rate targets?"
3. "How do our KYC verification levels affect transaction limits mentioned in the OKRs?"

### Specific Factual Questions
4. "What is our KYC verification process for Level 2 customers?"
5. "What were the results of the payment retry logic experiment?"
6. "What are the accepted payment methods according to the product spec?"
7. "How do I handle a customer asking about a failed payment?"

### Policy & Procedure Questions
8. "What is the escalation process for a SEV-1 security incident?"
9. "How long does a customer have to respond to a chargeback?"
10. "What are the steps for onboarding a new engineer in their first week?"

### Strategic & Metrics Questions
11. "What are our Q4 2024 objectives and how are we tracking?"
12. "What was our revenue and transaction volume in Q3 2024?"
13. "Why did we choose CockroachDB over other database options?"

### Technical Implementation Questions
14. "What is the fraud detection API endpoint and what parameters does it accept?"
15. "How does our payment retry logic work?"
16. "What are the deployment windows for production releases?"

## Document Interconnections

**Payment Processing** connects to:
- Fraud Detection (integration point)
- API Documentation (merchant usage)
- Incident Postmortem (outage details)
- OKRs (performance targets)

**KYC Process** connects to:
- Support FAQ (customer inquiries)
- Business Review (conversion metrics)
- OKRs (verification speed targets)

**Fraud Detection** connects to:
- Payment Processing (scoring integration)
- OKRs (false positive reduction)
- Business Review (fraud prevention results)

**Database ADR** connects to:
- Incident Postmortem (resilience requirements)
- OKRs (scalability targets)
- Sprint Planning (migration tasks)

## Realistic Elements Included

**People & Roles:**
- Sarah Chen (Product Manager)
- Alex Kumar (Principal Engineer)
- Jennifer Liu (Senior Engineer)
- Michael Rodriguez (Compliance Officer)
- David Thompson (VP Engineering)

**Technologies:**
- CockroachDB, PostgreSQL
- Stripe API
- Kubernetes, Docker
- XGBoost ML models
- DataDog, PagerDuty

**Business Metrics:**
- Transaction volumes
- Revenue figures
- Success rates
- Chargeback rates
- Customer counts

**Real-world Scenarios:**
- System outages
- A/B experiments
- Regulatory compliance
- Customer support cases
- Engineering decisions

## Usage Notes

This dataset simulates a realistic fintech company's internal knowledge base with:
- Multiple document types (specs, procedures, meeting notes)
- Cross-references between documents
- Real technical details and business context
- Authentic terminology and metrics
- Interconnected information requiring synthesis

Ideal for testing:
- Document retrieval accuracy
- Multi-document answer synthesis
- Context understanding
- Technical vs business query handling
- Factual accuracy in responses
