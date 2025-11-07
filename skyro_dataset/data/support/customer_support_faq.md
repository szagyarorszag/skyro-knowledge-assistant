# Customer Support FAQ - Internal Knowledge Base

**Last Updated:** October 28, 2024  
**Owner:** Customer Support Team  
**Version:** 3.4

## Payment Issues

### Q: Customer says their payment failed. How do I troubleshoot?

**A:** Follow these steps in order:

1. **Check payment status in admin panel**
   - Look up transaction by payment ID or customer email
   - Check the error code and status

2. **Common failure reasons:**
   - **PE001 (Insufficient funds):** Customer needs to add funds or use different payment method
   - **PE002 (Card declined):** Customer should contact their bank
   - **PE003 (Invalid card details):** Customer entered wrong card number/CVV/expiry
   - **PE004 (Transaction limit exceeded):** Customer has reached their daily/monthly limit
   - **PE005 (Suspected fraud):** Transaction flagged by fraud detection system

3. **For fraud flags (PE005):**
   - Escalate to fraud team via #fraud-review Slack channel
   - Do NOT process manually without fraud team approval
   - Average review time: 2-4 hours

4. **If customer can't resolve:**
   - Suggest alternative payment method
   - Check if merchant account is in good standing
   - Verify customer has completed KYC if required

### Q: Customer was charged twice for the same transaction. What should I do?

**A:** This is a PRIORITY issue. Follow immediately:

1. Verify in admin panel - check if there are actually two charges or just an authorization hold
2. If genuinely charged twice:
   - One charge is likely an authorization hold that will drop off in 3-5 business days
   - If both are captures (not holds), issue immediate refund for duplicate
   - Log incident in JIRA with tag "duplicate-charge"
   
3. Explain to customer:
   - Authorization holds appear as pending charges but will be released
   - If actual duplicate charge, refund processed immediately (appears in 5-7 days)
   - Offer ₱25 goodwill credit for inconvenience

**Escalation:** If customer disputes this explanation, escalate to payments-team@skyro.com

### Q: How long does a refund take?

**A:** Standard response:

"Refunds are processed immediately on our end, but it can take 5-7 business days for the funds to appear in your account depending on your bank. Credit card refunds typically appear faster (3-5 days) than debit card refunds (5-7 days).

If you don't see the refund after 7 business days, please contact your bank to check the status. If your bank confirms no refund was received, please reply to this ticket and we'll investigate further."

**Notes:**
- International refunds can take up to 10 business days
- Weekend/holiday refunds may be delayed
- Always provide refund ID for customer reference

### Q: Customer wants to increase their transaction limit. How do I handle this?

**A:** Transaction limits are based on KYC verification level:

**Level 1 (Basic):** ₱5,000/month
- Requirements: Email and phone verification only
- Cannot be increased

**Level 2 (Standard):** ₱50,000/month  
- Requirements: Government ID + proof of address + selfie
- Process time: 24-48 hours
- Send customer link: skyro.com/verify

**Level 3 (Enhanced):** Unlimited
- Requirements: All Level 2 + source of funds + business docs
- Process time: 3-5 business days
- Requires compliance team review
- Send customer link: skyro.com/verify-enhanced

**To request increase:**
1. Verify customer's current KYC level in admin panel
2. Guide customer to appropriate verification flow
3. Set expectation on processing time
4. Note in ticket: "KYC upgrade requested - Level X to Level Y"

## Account and KYC Issues

### Q: Customer's KYC verification was rejected. Why?

**A:** Check rejection reason in admin panel under KYC tab. Common reasons:

1. **Blurry or unclear photos**
   - Ask customer to retake photos in good lighting
   - Document should fill most of the frame
   - All text must be clearly readable

2. **Document expired**
   - Document must be valid (not expired)
   - Must be within 3 months for proof of address

3. **Name mismatch**
   - Name on ID must match name on account
   - If legal name change, need supporting documentation

4. **Document not accepted**
   - Some documents not accepted (e.g., student ID, work ID)
   - Accepted: Passport, driver's license, national ID, utility bill

5. **Liveness check failed (selfie)**
   - Take selfie in good lighting, without glasses
   - Face must be clearly visible
   - No filters or editing

**Standard Response:**
"Your verification was unsuccessful because [specific reason]. To complete verification, please [specific action needed]. You can resubmit at skyro.com/verify. If you have questions about requirements, please see our verification guide at skyro.com/help/kyc"

### Q: How do I handle high-risk customer escalations?

**A:** 

**DO NOT:**
- Override compliance decisions
- Process payments manually for high-risk flagged accounts
- Promise specific timelines for high-risk reviews

**DO:**
- Acknowledge customer frustration professionally
- Explain that additional review is for security and compliance
- Provide realistic timeline: 3-5 business days for high-risk reviews
- Escalate to compliance@skyro.com with all details

**Template Response:**
"For security and regulatory compliance, your account requires additional verification. Our compliance team is reviewing your information and will contact you within 3-5 business days. We understand this is frustrating, but these measures protect all our customers. Thank you for your patience."

## Technical Issues

### Q: Customer can't log in. What should I check?

**A:** Troubleshooting steps:

1. **Password reset attempt:**
   - Ask if customer tried password reset
   - If not, send password reset link
   - Reset emails can take up to 15 minutes (check spam)

2. **Account status check:**
   - Verify account is active (not suspended or closed)
   - Check if email address is verified
   - Look for failed login attempts (may be locked)

3. **Browser/device issues:**
   - Ask customer to try different browser
   - Clear cookies and cache
   - Try incognito/private mode
   - Update browser to latest version

4. **If still not working:**
   - Manually verify customer identity (ask security questions)
   - Generate temporary login link (valid 1 hour)
   - Log issue in JIRA with tag "login-issue"

### Q: Customer reports website is down or loading slowly

**A:** 

1. **Check status page immediately:** status.skyro.com
   - If incident is active, acknowledge and provide ETA from status page
   - Direct customer to status page for updates

2. **If no known incident:**
   - Ask customer for screenshot or error message
   - Check specific URL/feature they're accessing
   - Verify if issue is widespread (check #support-alerts Slack)
   - Report to engineering via #incidents if multiple customers affected

3. **Temporary workarounds:**
   - Mobile app as alternative to website
   - API access for technical merchants
   - Phone support for urgent transactions

## Merchant/Business Accounts

### Q: Merchant wants to integrate Skyro API. Where do I send them?

**A:** 

1. **Technical documentation:** docs.skyro.com
2. **API keys:** Available in merchant dashboard → Settings → API Keys
3. **Sandbox environment:** sandbox.skyro.com
4. **Developer support:** api-support@skyro.com or join Slack: skyro.com/slack

**For complex integrations:**
- Offer to schedule call with solutions engineer
- Send integration checklist: docs.skyro.com/integration-guide
- Typical integration time: 3-5 days for basic, 2-3 weeks for advanced

### Q: Merchant asking about settlement times

**A:** 

**Standard Settlement Schedule:**
- **Daily settlements:** For merchants processing >₱100k/month
- **Weekly settlements:** For merchants processing <₱100k/month
- **Settlement day:** T+2 (2 business days after transaction)

**Example:** Transaction on Monday → Settled on Wednesday

**Hold periods:**
- New merchants: First 2 weeks held for risk assessment
- High-risk industries: 7-day rolling reserve (10% of volume)
- After incident/chargeback spike: May impose temporary hold

**To check settlement status:**
1. Dashboard → Settlements → View schedule
2. Pending settlements show estimated date
3. Completed settlements show transaction breakdown

## Escalation Procedures

### When to Escalate

**Immediate Escalation (Within 1 hour):**
- Suspected fraud or security breach
- Duplicate charge affecting >10 customers
- Customer threatening legal action
- Payment processing completely down
- Data privacy concern or breach

**Standard Escalation (Same day):**
- High-value transaction issue (>₱10,000)
- VIP merchant/customer (flag in system)
- Compliance or regulatory question
- Technical issue you can't resolve
- Customer extremely dissatisfied (CSAT < 2)

**Escalation Channels:**
- **Slack:** #support-escalations (monitored 24/7)
- **Email:** escalations@skyro.com
- **Phone:** Duty manager (number in internal wiki)
- **PagerDuty:** For SEV-1 incidents only

### Escalation Template
```
**Customer:** [Name/Email/ID]
**Issue:** [Brief description]
**Priority:** [Low/Medium/High/Critical]
**Actions Taken:** [What you've already tried]
**Customer Impact:** [How urgent/severe]
**Ticket ID:** [SUPPORT-XXXXX]
```

## Compliance and Legal

### Q: Customer asking about data privacy or GDPR

**A:** 

**Standard Response:**
"Skyro is fully compliant with GDPR, CCPA, and other data protection regulations. You can review our privacy policy at skyro.com/privacy. For specific questions about how we handle your data, please email privacy@skyro.com."

**Data deletion requests (Right to be Forgotten):**
- Must be submitted in writing to privacy@skyro.com
- Identity verification required
- Process takes up to 30 days
- Note: Some data retained for legal/regulatory requirements (7-10 years)

**Data access requests:**
- Customer can download their data from Dashboard → Settings → Privacy
- Automated export includes: profile, transactions, documents
- Delivered within 24 hours

### Q: Customer received a SAR (Suspicious Activity Report) notice

**A:** 

**DO NOT:**
- Confirm or deny SAR filing
- Discuss specific reasons for SAR
- Provide detailed transaction analysis

**DO:**
- Acknowledge receipt of customer inquiry
- Explain we cannot discuss SARs per regulatory requirements
- Advise customer to contact Financial Intelligence Unit if they have concerns
- Document interaction in compliance system

**Template Response:**
"We cannot provide information about regulatory reporting activities. If you have concerns about your account, please contact our compliance team at compliance@skyro.com who can discuss what information can be shared within legal limits."

**ALWAYS escalate SAR-related inquiries to compliance team immediately.**

## Resources

**Internal Tools:**
- Admin Panel: admin.skyro.com
- Status Page: status.skyro.com
- Knowledge Base: wiki.skyro.com
- Ticket System: support.skyro.com

**Slack Channels:**
- #customer-support (main channel)
- #support-escalations (urgent issues)
- #fraud-review (fraud investigations)
- #compliance-questions (compliance/legal)
- #tech-support (technical issues)

**Contact Information:**
- Support Manager: Sarah Johnson (sarah.j@skyro.com)
- Compliance Officer: Michael Rodriguez (michael.r@skyro.com)
- Engineering On-Call: See PagerDuty schedule
- Legal: legal@skyro.com (non-urgent)

**Training Materials:**
- New hire orientation: wiki.skyro.com/onboarding
- Product updates: #product-announcements Slack
- Monthly support training: First Friday of each month, 2 PM EST
