# Skyro Dataset - File Formats Summary

## Total Files: 18 files (14 unique documents)

### Format Distribution:

**Markdown Files (.md): 14 files**
- DATASET_OVERVIEW.md
- business/q3_2024_business_review.md
- business/q4_2024_okrs.md
- compliance/kyc_process.md
- experiments/payment_retry_logic_results.md
- meetings/incident_postmortem_089.md
- meetings/sprint_42_planning.md
- onboarding/new_engineer_guide.md
- operations/chargeback_procedures.md
- product_specs/payment_processing_v2.md
- security/incident_response_playbook.md
- support/customer_support_faq.md
- technical/adr_015_database_selection.md
- technical/fraud_detection_system.md
- technical/merchant_api_documentation.md

**DOCX Files (.docx): 2 files**
- meetings/sprint_42_planning.docx (converted from .md)
- support/customer_support_faq.docx (converted from .md)

**PDF Files (.pdf): 2 files**
- compliance/kyc_process.pdf (converted from .md)
- operations/chargeback_procedures.pdf (converted from .md)

## Files for RAG Ingestion (Remove duplicates):

**Use these 14 files (mixed formats):**

1. business/q3_2024_business_review.md
2. business/q4_2024_okrs.md
3. compliance/kyc_process.pdf (USE PDF, not .md)
4. experiments/payment_retry_logic_results.md
5. meetings/incident_postmortem_089.md
6. meetings/sprint_42_planning.docx (USE DOCX, not .md)
7. onboarding/new_engineer_guide.md
8. operations/chargeback_procedures.pdf (USE PDF, not .md)
9. product_specs/payment_processing_v2.md
10. security/incident_response_playbook.md
11. support/customer_support_faq.docx (USE DOCX, not .md)
12. technical/adr_015_database_selection.md
13. technical/fraud_detection_system.md
14. technical/merchant_api_documentation.md

**Do NOT use (duplicates in different format):**
- compliance/kyc_process.md (use PDF instead)
- meetings/sprint_42_planning.md (use DOCX instead)
- operations/chargeback_procedures.md (use PDF instead)
- support/customer_support_faq.md (use DOCX instead)

## Format Rationale:

**PDF files (2):** 
- Compliance documents (KYC Process)
- Operational procedures (Chargeback Procedures)
- Realistic: These types often come as PDFs

**DOCX files (2):**
- Meeting notes (Sprint Planning)
- Support documentation (FAQ)
- Realistic: Often created in Word/Google Docs

**Markdown files (10):**
- Technical documentation
- Architecture decisions
- Product specs
- Business reviews
- Realistic: Often from Confluence, wiki, or code repos

## File Sizes:


### Approximate Sizes:
