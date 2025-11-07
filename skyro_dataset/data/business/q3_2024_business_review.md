# Q3 2024 Business Review

**Prepared by:** Finance & Strategy Team  
**Date:** September 30, 2024  
**Audience:** Executive Team, Board of Directors

## Executive Summary

Q3 2024 was a strong quarter for Skyro with significant progress on key strategic initiatives. Despite a critical payment gateway incident in October, the team demonstrated excellent response capabilities and maintained customer trust.

**Key Highlights:**
- Revenue grew 34% YoY to ₱43.2M
- Processed 856M transactions (up 41% YoY)
- Expanded to 3 new markets (Brazil, Mexico, India)
- Reduced customer acquisition cost by 18%
- Achieved SOC 2 Type II certification

**Challenges:**
- Payment gateway incident resulted in ₱127K direct revenue loss
- KYC verification bottlenecks delaying customer onboarding
- Higher than expected churn in small merchant segment (8.2%)

## Financial Performance

### Revenue

**Total Revenue:** ₱43.2M (Q3 2024)
- Q3 2023: ₱32.2M
- Growth: +34% YoY
- Q2 2024: ₱39.8M
- Growth: +8.5% QoQ

**Revenue Breakdown:**
- Transaction fees: ₱38.7M (89.6%)
- Subscription revenue: ₱3.2M (7.4%)
- Premium features: ₱1.3M (3.0%)

**Geographic Distribution:**
- North America: ₱28.4M (65.7%)
- Europe: ₱10.2M (23.6%)
- Asia Pacific: ₱3.8M (8.8%)
- Latin America: ₱0.8M (1.9%)

**Customer Segments:**
- Enterprise (>₱1M/year): ₱22.1M (51.2%)
- Mid-market (₱100K-₱1M/year): ₱14.6M (33.8%)
- Small business (<₱100K/year): ₱6.5M (15.0%)

### Expenses

**Total Operating Expenses:** ₱31.8M
- Cost of revenue: ₱12.6M (29.2% of revenue)
- Sales & marketing: ₱9.8M (22.7%)
- R&D: ₱6.9M (16.0%)
- G&A: ₱2.5M (5.8%)

**Key Cost Drivers:**
- Infrastructure costs: ₱8.2M (19.0% of revenue)
- Personnel costs: ₱18.7M (43.3% of revenue)
- Third-party services: ₱2.4M (5.6% of revenue)

### Profitability

**EBITDA:** ₱11.4M (26.4% margin)
- Q3 2023: ₱7.8M (24.2% margin)
- Improvement: +2.2 percentage points

**Net Income:** ₱8.9M (20.6% margin)
- Q3 2023: ₱5.7M (17.7% margin)

**Cash Position:**
- Cash and equivalents: ₱87.3M
- Burn rate: -₱2.1M/month (negative burn = generating cash)
- Runway: >3 years at current burn rate

## Operational Metrics

### Transaction Metrics

**Total Transactions:** 856 million
- Q3 2023: 608 million (+41% YoY)
- Daily average: 9.3 million transactions
- Peak: 14.7 million transactions (September 15 - major shopping event)

**Transaction Success Rate:** 96.8%
- Target: 98%
- Impact from October incident: -1.2 percentage points
- Improvements from payment retry logic: +3.6 percentage points

**Average Transaction Value:** ₱47.35
- Q3 2023: ₱49.20 (-3.8% YoY)
- Trend: Shift toward smaller transactions as we expand to emerging markets

**Processing Volume:** ₱40.5B
- Q3 2023: ₱29.9B (+35% YoY)

### Customer Metrics

**Active Merchants:** 14,682
- Q3 2023: 10,234 (+43% YoY)
- Net new merchants: +1,847 in Q3

**Customer Retention:**
- Enterprise: 98% (industry-leading)
- Mid-market: 94%
- Small business: 92% (down from 94% in Q2)

**Net Revenue Retention:** 118%
- Existing customers growing revenue by 18% through expansion

**Average Revenue Per User (ARPU):**
- Enterprise: ₱28,400/month
- Mid-market: ₱7,600/month
- Small business: ₱320/month

**Customer Acquisition Cost (CAC):** ₱2,840
- Q3 2023: ₱3,450 (-18% improvement)
- LTV/CAC ratio: 4.2:1 (healthy, target >3:1)

**Customer Lifetime Value (LTV):** ₱11,900
- Q3 2023: ₱10,200 (+17% improvement)

### Product Metrics

**API Availability:** 99.94%
- Target: 99.95%
- Impact from October incident
- Excluding incident: 99.97%

**Average API Latency:**
- p50: 87ms (target: <100ms) ✓
- p95: 234ms (target: <300ms) ✓
- p99: 567ms (target: <500ms) ✗

**Payment Methods Supported:** 25
- Added 6 new currencies in Q3
- Added 2 local payment methods (Alipay, WeChat Pay)

**Developer Satisfaction:** 8.4/10
- API documentation quality: 9.1/10
- Integration ease: 8.2/10
- Support responsiveness: 8.0/10

## Strategic Initiatives Progress

### Initiative 1: Global Expansion

**Status:** On Track (75% complete)

**Achievements:**
- Launched in Brazil (July), Mexico (August), India (September)
- Completed regulatory approvals for all 3 markets
- Onboarded 427 merchants in new markets
- ₱2.3M revenue from new markets (5.3% of total)

**Challenges:**
- Regulatory complexity higher than expected in India
- Local payment method integrations taking longer
- Need local language support for customer service

**Next Steps:**
- Launch in Indonesia and Philippines (Q4)
- Build local partnerships for payment methods
- Hire regional account managers

### Initiative 2: Fraud Reduction

**Status:** Ahead of Schedule (90% complete)

**Achievements:**
- Deployed new ML model with 96% accuracy
- Reduced false positive rate from 1.2% to 0.7%
- Prevented ₱8.7M in fraudulent transactions
- Improved fraud detection speed to <50ms

**Impact:**
- ₱3.2M in chargeback savings
- Improved customer experience (fewer legitimate transactions blocked)
- 25% reduction in manual review queue

**Next Steps:**
- Implement graph-based fraud detection (Q4)
- Add behavioral biometrics
- Expand training data to include new markets

### Initiative 3: Platform Scalability

**Status:** On Track (60% complete)

**Achievements:**
- Migrated to CockroachDB (in progress)
- Increased throughput capacity to 22,000 TPS
- Reduced payment processing latency by 18%
- Implemented circuit breakers and auto-rollback

**Challenges:**
- Database migration more complex than expected
- October incident exposed resilience gaps
- Need more automated testing

**Next Steps:**
- Complete CockroachDB migration (November)
- Implement multi-region active-active architecture
- Build chaos engineering test suite
- Target: 50,000 TPS capacity by year-end

### Initiative 4: Developer Experience

**Status:** On Track (70% complete)

**Achievements:**
- Launched self-service sandbox environment
- Published 12 new API guides and tutorials
- Released 4 new SDKs (Python, Ruby, Go, PHP)
- Reduced integration time from 14 days to 9 days

**Developer Feedback:**
- "Best payment API I've used" - SaaS company CTO
- "Documentation is excellent" - E-commerce platform
- "Sandbox made testing so easy" - Mobile app startup

**Next Steps:**
- Launch developer community forum
- Create video tutorials
- Offer integration certifications
- Host virtual developer conference (Q4)

## Market Analysis

### Competitive Landscape

**Market Position:** #4 in global payment processing
- #1: Stripe (₱95B valuation)
- #2: Adyen (₱50B valuation)
- #3: PayPal (₱75B valuation)
- #4: Skyro (private, last valued at ₱2.1B)

**Competitive Advantages:**
- Superior fraud detection (0.7% false positive vs industry avg 2.1%)
- Best-in-class API documentation and developer experience
- Faster innovation cycle (ship features 2x faster than competitors)
- Better pricing for mid-market customers

**Competitive Threats:**
- Stripe expanding aggressively to emerging markets
- Adyen's strong relationships with large enterprises
- New entrants with crypto payment focus
- Banks building their own payment platforms

### Market Trends

**Opportunities:**
1. **Embedded Finance:** Growing demand for payments within non-financial apps
2. **Real-time Payments:** Increasing adoption of instant payment systems
3. **Crypto Adoption:** Merchants want to accept crypto payments
4. **Buy Now Pay Later:** Strong growth in installment payment options

**Risks:**
1. **Regulatory Pressure:** Increasing regulation in fintech globally
2. **Economic Downturn:** Recession could reduce transaction volume
3. **Security Threats:** Rising sophistication of fraud and cyber attacks
4. **Big Tech Entry:** Amazon, Apple, Google expanding payment offerings

## Customer Highlights

### Success Stories

**Enterprise Customer A (E-commerce Platform):**
- Switched from Stripe to Skyro in July
- Processing ₱12M/month
- 99.2% payment success rate (up from 96% with previous provider)
- Saved ₱84K/month in fees

**Mid-Market Customer B (SaaS Company):**
- Used our multi-currency support to expand globally
- Grew from ₱200K/month to ₱1.2M/month in 6 months
- "Skyro made international expansion easy" - CEO

**Small Business Customer C (Online Marketplace):**
- Startup that grew with us from ₱5K/month to ₱80K/month
- Our fraud detection saved them from ₱45K in chargebacks
- Using our developer tools to build custom checkout flow

### Customer Feedback

**Net Promoter Score (NPS):** 67
- Enterprise: 72
- Mid-market: 68
- Small business: 61

**Customer Satisfaction (CSAT):** 4.3/5
- Product functionality: 4.5/5
- Support quality: 4.2/5
- Pricing: 4.0/5
- Documentation: 4.6/5

**Top Feature Requests:**
1. More local payment methods (38% of requests)
2. Better reporting and analytics (24%)
3. Subscription billing features (18%)
4. Invoice generation (12%)
5. Multi-user account management (8%)

## Incidents and Learnings

### Major Incidents

**INC-2024-089: Payment Gateway Outage (October 22)**
- Duration: 2 hours 17 minutes
- Impact: 3,400 failed transactions, ₱127K revenue loss
- Root cause: Deployment with inadequate timeout configuration
- Resolution: Rollback + circuit breaker implementation

**Lessons Learned:**
1. Need automated rollback on degradation
2. Insufficient load testing before deployment
3. Circuit breaker pattern critical for resilience
4. Cross-team communication on API changes essential

**Actions Taken:**
- Implemented circuit breakers across all services
- Enhanced deployment automation with automatic rollback
- Improved monitoring and alerting
- Conducted quarterly disaster recovery drills

### Security

**Security Incidents:** 0 major incidents (Q3)
- 3 minor incidents (phishing attempts blocked)
- 0 data breaches
- 0 compliance violations

**Certifications:**
- Achieved SOC 2 Type II certification (September)
- Maintained PCI DSS Level 1 compliance
- GDPR compliant in all EU operations

## Team and Culture

### Headcount

**Total Employees:** 287
- Engineering: 142 (49%)
- Product: 28 (10%)
- Sales & Marketing: 67 (23%)
- Customer Success: 31 (11%)
- G&A: 19 (7%)

**New Hires in Q3:** 34
- Engineering: 18
- Sales: 9
- Customer Success: 5
- Product: 2

**Attrition Rate:** 6.2% annualized
- Industry average: 13.2%
- Voluntary: 4.8%
- Involuntary: 1.4%

### Diversity & Inclusion

**Gender Diversity:**
- Overall: 42% women
- Engineering: 31% women (up from 28% in Q2)
- Leadership: 38% women

**Ethnic Diversity:**
- 58% representation from underrepresented groups
- Commitment to increase to 65% by end of 2025

### Employee Satisfaction

**eNPS (Employee Net Promoter Score):** 58
- Engineering: 62
- Sales: 54
- Overall satisfaction: 4.2/5

**Top Reasons Employees Love Skyro:**
1. Great team and culture (87%)
2. Interesting technical challenges (78%)
3. Work-life balance (76%)
4. Growth opportunities (73%)
5. Competitive compensation (71%)

## Looking Ahead: Q4 Preview

### Key Priorities

1. **Complete Platform Scalability Initiative**
   - Finish CockroachDB migration
   - Achieve 50,000 TPS capacity
   - Multi-region deployment

2. **Expand to 5 Additional Markets**
   - Indonesia, Philippines, Thailand, Vietnam, Kenya
   - Revenue target: ₱5M from new markets in Q4

3. **Launch New Product Features**
   - Subscription billing
   - Advanced reporting and analytics
   - Crypto payment support (beta)

4. **Improve Unit Economics**
   - Reduce infrastructure costs by 15%
   - Increase ARPU by 12%
   - Maintain LTV/CAC ratio above 4:1

### Financial Targets (Q4 2024)

- Revenue: ₱48-52M
- EBITDA margin: 27-29%
- Transaction volume: 950M-1B transactions
- Net new merchants: 2,000+

### Risks to Monitor

- Holiday season traffic surge (Black Friday, Cyber Monday)
- Competitive pressure in key markets
- Regulatory changes in new markets
- Talent retention during year-end bonus season

---

## Conclusion

Q3 2024 demonstrated Skyro's ability to execute on strategic priorities while maintaining strong financial performance. Despite operational challenges, the team showed resilience and commitment to continuous improvement.

The foundation built this quarter positions us well for Q4 success and sets the stage for continued growth in 2025.

**Approved by:**
- CEO: Jennifer Wang
- CFO: David Martinez
- COO: Sarah Thompson

**Board Presentation:** October 15, 2024
