# Chargeback Handling Procedures

**Document Type:** Operations Manual  
**Owner:** Risk & Operations Team  
**Last Updated:** October 5, 2024  
**Version:** 2.3

## Overview

This document outlines Skyro's procedures for handling payment chargebacks. Chargebacks occur when customers dispute transactions with their card issuers, and funds are forcibly returned to the customer.

## Chargeback Basics

### What is a Chargeback?

A chargeback is a reversal of a credit or debit card transaction, initiated by the cardholder through their issuing bank. The merchant (our customer) is debited for the transaction amount plus a chargeback fee.

### Common Chargeback Reasons

**Fraud-related:**
- Card stolen or lost
- Transaction not authorized by cardholder
- Fraudulent use of card details

**Service/Product Issues:**
- Product not received
- Product significantly different from description
- Defective or damaged product
- Service not rendered

**Processing Errors:**
- Duplicate charge
- Incorrect amount charged
- Credit not processed

**Friendly Fraud:**
- Customer doesn't recognize charge
- Family member made purchase without knowledge
- Customer forgot about transaction
- Buyer's remorse

### Chargeback Lifecycle

1. **Customer disputes transaction** with their bank (Day 0)
2. **Bank initiates chargeback** and debits merchant account (Day 1-3)
3. **Merchant receives notification** from Skyro (Day 3-5)
4. **Merchant submits evidence** to dispute chargeback (within 7-14 days)
5. **Bank reviews evidence** and makes decision (30-90 days)
6. **Final decision** issued (merchant wins or loses)

### Financial Impact

**Costs per Chargeback:**
- Transaction amount: ₱X (varies)
- Chargeback fee: ₱15-25 (passed to merchant)
- Time cost: ~2 hours of staff time
- Potential account termination if ratio too high

**Acceptable Chargeback Rate:** <0.65%
- Industry average: 0.6%
- Warning threshold: 0.9%
- Suspension threshold: 1.5%

## Skyro's Role

### What We Do

1. **Monitor chargeback rates** for all merchants
2. **Notify merchants immediately** when chargeback occurs
3. **Provide platform** for submitting evidence
4. **Track chargeback lifecycle** and outcomes
5. **Alert merchants** at risk of exceeding thresholds
6. **Provide data and insights** to reduce chargebacks

### What We Don't Do

- We cannot prevent chargebacks from being filed
- We don't make the final decision (bank does)
- We don't guarantee winning disputes
- We're not responsible for merchant's chargeback rate

## Notification Process

### Immediate Notification (Within 24 Hours)

When a chargeback is received:

1. **Email sent to merchant** with details:
   - Transaction ID and amount
   - Chargeback reason code
   - Customer information
   - Due date for response
   - Link to dispute portal

2. **Dashboard notification** appears in merchant portal

3. **Webhook sent** (if merchant has configured)

### Notification Contents

**Subject:** Action Required: Chargeback on Transaction [ID]

**Body includes:**
- Chargeback ID
- Original transaction details
- Amount in dispute
- Reason code and description
- Evidence submission deadline
- Instructions for responding
- Link to dispute portal

## Evidence Submission

### Response Timeline

- **Standard timeline:** 7 business days
- **Expedited (fraud):** 48 hours
- **Extensions:** Not available

**Late submissions:** Automatically forfeit - merchant loses by default

### Required Evidence by Reason Code

**Code 83: Fraud - Card Not Present**
- Proof of delivery (tracking number, signature)
- IP address and geolocation
- AVS/CVV match results
- Customer communication history
- Previous successful transactions from same customer
- Device fingerprint data

**Code 53: Not as Described/Defective**
- Product description from listing
- Photos of actual product sent
- Customer communication acknowledging receipt
- Refund/return policy
- Shipping information

**Code 30: Services Not Provided**
- Service agreement or contract
- Proof of service delivery (screenshots, logs, reports)
- Customer usage data
- Communication history
- Terms and conditions

**Code 12: Duplicate Processing**
- Proof charges are for separate transactions
- Invoices showing different order IDs
- Different delivery dates/addresses
- Explanation of charges

**Code 37: Fraudulent Transaction**
- Same as Code 83
- Additionally: fraud detection scores and reasoning

### Evidence Submission Process

1. **Log into merchant dashboard**
2. **Navigate to Chargebacks section**
3. **Select chargeback to dispute**
4. **Complete evidence form:**
   - Select evidence type for each item
   - Upload supporting documents
   - Provide written explanation
   - Review and submit

5. **Receive confirmation** email

### Evidence Best Practices

**Do:**
- Submit clear, legible documents
- Provide comprehensive evidence
- Use professional language
- Include all relevant information
- Submit before deadline
- Follow specific requirements for reason code

**Don't:**
- Submit irrelevant documents
- Include customer payment information
- Use emotional or unprofessional language
- Miss the deadline
- Submit partial evidence
- Forget to explain how evidence supports your case

### Supported File Formats

- PDF (preferred)
- JPEG/PNG images
- Excel/CSV spreadsheets
- Maximum file size: 25MB per file
- Maximum 10 files per chargeback

## Chargeback Decision Outcomes

### Merchant Wins

- **Result:** Funds returned to merchant, chargeback fee refunded
- **Timeline:** 30-90 days for funds to return
- **Notification:** Email and dashboard update

### Merchant Loses

- **Result:** Customer keeps refunded amount, merchant pays chargeback fee
- **Impact:** Loss recorded in merchant account
- **Next steps:** Review why lost, improve processes

### Partial Win

- **Result:** Partial refund to customer, reduced chargeback fee
- **Rare:** Only in specific circumstances

## Merchant Support

### Chargeback Prevention

We provide tools and guidance to help reduce chargebacks:

**Best Practices:**
1. **Clear billing descriptors** (match business name)
2. **Detailed product descriptions** on website
3. **Prompt customer service** to resolve issues before chargeback
4. **Clear refund policy** and easy refund process
5. **Delivery confirmations** and tracking
6. **Fraud prevention** tools (AVS, CVV, 3D Secure)
7. **Transaction receipts** sent to customers

**Skyro Tools:**
- Fraud detection alerts (high-risk transactions)
- Chargeback analytics dashboard
- Automated chargeback alerts
- Evidence template generator
- Historical win/loss analysis

### Chargeback Analytics

Available in merchant dashboard:

- **Chargeback rate** (percentage of transactions)
- **Chargeback volume** over time
- **Reason code breakdown**
- **Win/loss ratio**
- **Average dispute amount**
- **Comparison to industry benchmarks**

### Risk Management

**Monitoring Thresholds:**

**Green (Healthy):** <0.65% chargeback rate
- Standard processing, no action needed

**Yellow (Warning):** 0.65%-0.9% chargeback rate
- Email warning sent to merchant
- Recommendation to review processes
- Offer consultation with risk team

**Orange (At Risk):** 0.9%-1.5% chargeback rate
- Account flagged for review
- Mandatory consultation with risk team
- May implement temporary holds on funds
- Rolling reserve may be required (10% of volume)

**Red (Critical):** >1.5% chargeback rate
- Account suspended (new transactions blocked)
- Existing transactions held for 90 days
- Merchant enrolled in monitoring program
- May lead to account termination

### Getting Off Monitoring Program

Requirements to exit monitoring:
1. Chargeback rate below 0.9% for 3 consecutive months
2. Completion of risk consultation
3. Implementation of recommended improvements
4. No fraud incidents in monitoring period

## Preventing Chargebacks

### Proactive Strategies

**Communication:**
- Send order confirmation emails immediately
- Provide shipping updates and tracking
- Send delivery confirmation
- Follow up after delivery
- Make customer service easy to reach

**Transparency:**
- Clear billing descriptor (appears on statement)
- Detailed product descriptions and photos
- Transparent pricing (no hidden fees)
- Clear refund and return policies
- Accurate delivery timeframes

**Fraud Prevention:**
- Use AVS (Address Verification System)
- Require CVV for card-not-present transactions
- Enable 3D Secure for high-risk transactions
- Flag and review high-risk orders
- Use Skyro's fraud detection tools

**Fulfillment:**
- Ship orders promptly
- Use trackable shipping methods
- Require signature for high-value items
- Package items securely
- Inspect items before shipping

### When Customer Contacts You

**Before they file a chargeback:**
1. Respond quickly (within 24 hours)
2. Listen to their concern
3. Offer resolution (refund, replacement, credit)
4. Document the interaction
5. Follow through on promises

**Friendly Fraud Prevention:**
- Send reminder emails before recurring charges
- Make cancellation easy
- Use clear billing descriptors
- Provide detailed receipts
- Keep communication history

## Escalation Procedures

### When to Escalate to Skyro

Contact our risk team if:
- Chargeback rate approaching 0.9%
- Unusual spike in chargebacks
- Specific customer filing multiple chargebacks
- Need help with evidence submission
- Questions about chargeback process
- Suspected organized fraud ring

### How to Contact Us

- **Email:** chargebacks@skyro.com
- **Phone:** 1-800-SKYRO-CB (1-800-759-7622)
- **Slack:** #merchant-support (for integrated merchants)
- **Dashboard:** Submit support ticket

**Response Time:**
- Email: Within 24 hours
- Phone: Immediate (business hours)
- Urgent cases: Within 2 hours

## Representment (Second Dispute)

### What is Representment?

If a merchant loses a chargeback and believes the decision was incorrect, they can file a second dispute (representment).

### Representment Eligibility

- Available only for certain reason codes
- Must have new evidence not submitted originally
- Only one representment allowed per chargeback
- Additional ₱15 fee if representment is lost

### Representment Process

1. Request representment through dashboard
2. Provide new evidence
3. Pay representment fee (₱25)
4. Wait for final decision (60-120 days)

### Success Rate

- Average representment win rate: 25%
- Only recommended if strong new evidence available

## Reporting and Compliance

### Monthly Reports

Merchants receive monthly chargeback reports including:
- Total chargebacks filed
- Chargeback rate
- Win/loss ratio
- Reason code breakdown
- Recommendations for improvement

### Card Network Monitoring

**Visa:** Visa Dispute Monitoring Program (VDMP)
- Threshold: 0.9% chargeback rate
- Review: Monthly
- Consequences: Fines, increased fees, program enrollment

**Mastercard:** Excessive Chargeback Merchant (ECM)
- Threshold: 1.5% chargeback rate
- Review: Monthly
- Consequences: Similar to Visa

**Our Role:**
- Monitor merchant compliance with card network rules
- Alert merchants before thresholds are reached
- Help merchants implement improvement plans
- Report to card networks as required

## Frequently Asked Questions

### Q: How long do I have to respond to a chargeback?

A: 7 business days for most chargebacks, 48 hours for fraud-related. Check the specific deadline in your notification email.

### Q: Can I issue a refund after receiving a chargeback?

A: No, the funds have already been returned to the customer. Issuing a refund would result in the customer receiving a double refund.

### Q: What happens if I don't respond to a chargeback?

A: You automatically lose the dispute, and the customer keeps the refunded amount. You also pay the chargeback fee.

### Q: How long until I know the outcome?

A: Typically 30-90 days after submitting evidence. You'll receive email notification when a decision is made.

### Q: Can Skyro help me win chargebacks?

A: We provide tools, templates, and guidance, but the final decision is made by the card issuing bank. We cannot guarantee outcomes.

### Q: What if my chargeback rate is too high?

A: We'll work with you to identify issues and improve processes. Persistent high rates may result in account restrictions or termination.

### Q: Do I have to pay the chargeback fee even if I win?

A: No, if you win the dispute, the chargeback fee is refunded to you along with the transaction amount.

### Q: Can I talk to the customer directly?

A: Yes, and we encourage it! Often disputes can be resolved by contacting the customer before the bank makes a decision.

## Resources

**Internal Links:**
- Chargeback dashboard: dashboard.skyro.com/chargebacks
- Evidence submission portal: dashboard.skyro.com/chargebacks/submit
- Analytics and reporting: dashboard.skyro.com/analytics/chargebacks

**External Resources:**
- Visa chargeback reason codes: visa.com/chargebacks
- Mastercard chargeback guide: mastercard.com/chargebacks
- Chargeback best practices: skyro.com/resources/chargebacks

**Training:**
- Chargeback prevention webinar: Register at skyro.com/webinars
- One-on-one consultation: Email chargebacks@skyro.com
- Chargeback workshop: Quarterly, announced via email

## Document History

- v2.3 (October 2024): Updated thresholds and card network rules
- v2.2 (July 2024): Added representment section
- v2.1 (April 2024): Enhanced evidence requirements
- v2.0 (January 2024): Major rewrite for new platform
- v1.0 (October 2023): Initial version

**Next Review:** January 2025
