# New Engineer Onboarding Guide

**Welcome to Skyro Engineering!**

**Version:** 4.2  
**Last Updated:** October 1, 2024  
**Owner:** Engineering Operations Team

## Week 1: Getting Started

### Day 1: Orientation and Setup

**Morning (9:00 AM - 12:00 PM):**
- 9:00 AM: Welcome meeting with your manager
- 9:30 AM: HR orientation (benefits, policies, paperwork)
- 10:30 AM: Office tour and meet the team
- 11:00 AM: IT setup (laptop, accounts, security badge)
- 11:30 AM: Security and compliance training (mandatory)

**Afternoon (1:00 PM - 5:00 PM):**
- Set up development environment (see Dev Setup Guide below)
- Complete required training modules in Learning Portal
- Join Slack channels (see list below)
- Schedule 1-on-1s with team members for Week 1

**Required Accounts:**
- GitHub (company org)
- AWS Console
- Jira
- Confluence
- Slack
- PagerDuty (if on-call eligible)
- DataDog (monitoring)

### Day 2-3: Learning the Stack

**Technical Overview Sessions:**
- Architecture overview (2 hours)
- Payment processing system walkthrough
- Fraud detection system overview
- Database and data architecture
- DevOps and deployment processes
- Security practices and compliance requirements

**Code Walkthrough:**
- Clone main repositories
- Review code structure and conventions
- Read README files and technical documentation
- Set up local development environment
- Run test suite locally

**Key Repositories:**
- `payment-gateway` - Core payment processing
- `fraud-detection` - ML-based fraud detection
- `customer-api` - Customer-facing REST API
- `merchant-api` - Merchant integration APIs
- `kyc-service` - KYC verification system
- `web-app` - Customer web application
- `admin-panel` - Internal admin tools

### Day 4-5: First Contributions

**Starter Tasks:**
- Fix a "good first issue" bug (tagged in Jira)
- Write or update documentation
- Add unit tests to increase coverage
- Code review practice (shadow experienced engineers)

**Pairing Sessions:**
- Pair with senior engineer on small task
- Observe code review process
- Learn debugging techniques
- Understand deployment workflow

## Week 2: Diving Deeper

### Technical Deep Dives

**Monday:** Payment Processing Deep Dive
- Multi-currency support architecture
- Payment method integrations (Stripe, bank transfers)
- Transaction lifecycle and state management
- Error handling and retry logic
- Settlement and reconciliation

**Tuesday:** Fraud Detection Deep Dive
- Machine learning model architecture
- Feature engineering and data pipeline
- Real-time scoring system
- Rule engine and configuration
- Model training and deployment

**Wednesday:** Infrastructure and DevOps
- Kubernetes cluster architecture
- CI/CD pipeline (GitHub Actions)
- Monitoring and alerting (DataDog, PagerDuty)
- Log aggregation (ELK stack)
- Database architecture (CockroachDB)

**Thursday:** Security and Compliance
- Authentication and authorization (OAuth 2.0)
- Data encryption (at rest and in transit)
- PCI DSS compliance requirements
- GDPR and data privacy
- Incident response procedures

**Friday:** Product and Business Context
- Company vision and mission
- Product roadmap overview
- Key metrics and OKRs
- Customer personas and use cases
- Competitive landscape

### First Real Task

**Assignment:** Take ownership of a small feature or bug fix
- Typical scope: 2-5 days of work
- Work through full development lifecycle
- Write code, tests, documentation
- Submit PR, incorporate feedback
- Deploy to staging, then production

**Support:**
- Assigned mentor for questions
- Daily check-ins with manager
- Access to entire team via Slack

## Week 3-4: Becoming Productive

### Expanding Responsibilities

**Week 3:**
- Join sprint planning meeting
- Take on sprint tasks (1-2 stories)
- Participate in daily standups
- Start reviewing other engineers' PRs
- Begin learning on-call procedures (if applicable)

**Week 4:**
- Lead a small feature implementation
- Present work in sprint demo
- Participate in technical design discussions
- Shadow on-call engineer (if applicable)
- Complete security and compliance certifications

## Development Environment Setup

### Prerequisites
- macOS (recommended) or Linux
- 16GB RAM minimum, 32GB recommended
- Git, Docker, and Docker Compose

### Setup Steps

1. **Install Developer Tools:**
```bash
# Install Homebrew (macOS)
/bin/bash -c "₱(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install essential tools
brew install git node python@3.11 postgresql@15 redis

# Install Docker Desktop
# Download from docker.com
```

2. **Clone Repositories:**
```bash
# Create workspace
mkdir ~/skyro && cd ~/skyro

# Clone main repos (using SSH)
git clone git@github.com:skyro/payment-gateway.git
git clone git@github.com:skyro/fraud-detection.git
git clone git@github.com:skyro/customer-api.git
```

3. **Configure Environment:**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials (get from IT team)
# - Database connection strings
# - API keys for third-party services
# - AWS credentials
```

4. **Install Dependencies:**
```bash
# For Node.js projects
npm install

# For Python projects
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Set up Local Database:**
```bash
# Start PostgreSQL
brew services start postgresql@15

# Create databases
createdb skyro_development
createdb skyro_test

# Run migrations
npm run migrate
```

6. **Run Tests:**
```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests (requires Docker)
npm run test:e2e
```

7. **Start Local Services:**
```bash
# Using Docker Compose
docker-compose up

# Or start services individually
npm run dev  # Starts on localhost:3000
```

### Verification
- Navigate to http://localhost:3000
- You should see the Skyro development dashboard
- Try creating a test payment
- Check logs for any errors

## Slack Channels

**Must Join:**
- #engineering - Main engineering channel
- #engineering-[your-team] - Your specific team channel
- #deployments - Deployment notifications
- #incidents - Production incidents
- #tech-announcements - Important technical updates

**Recommended:**
- #random - Casual chat
- #help-[topic] - Get help on specific topics
- #code-reviews - Request code reviews
- #learning - Share learning resources
- #product-updates - Product announcements

**Optional but Useful:**
- #customer-support - See customer issues firsthand
- #data-engineering - For data pipeline questions
- #frontend or #backend - Specialty channels
- #security - Security discussions and alerts

## Engineering Practices

### Code Standards

**Language-Specific Guides:**
- Python: Follow PEP 8, use Black formatter
- JavaScript/TypeScript: ESLint with Airbnb config
- Go: Follow standard Go conventions

**General Principles:**
- Write self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Write comprehensive tests (aim for 80%+ coverage)
- No commented-out code in commits

### Git Workflow

**Branch Naming:**
```
feature/SKYRO-123-add-payment-retry
bugfix/SKYRO-456-fix-kyc-timeout
hotfix/critical-security-patch
```

**Commit Messages:**
```
SKYRO-123: Add automatic payment retry logic

- Implement exponential backoff strategy
- Add retry for transient failures only
- Update tests and documentation
```

**Pull Request Process:**
1. Create feature branch from `main`
2. Make changes and commit regularly
3. Push to GitHub and open PR
4. Fill out PR template completely
5. Request reviews from 2+ engineers
6. Address feedback and update PR
7. Merge after approval (squash and merge)

### Code Review Guidelines

**As Author:**
- Keep PRs small (<500 lines if possible)
- Provide context in PR description
- Self-review before requesting reviews
- Be responsive to feedback
- Test thoroughly before requesting review

**As Reviewer:**
- Review within 24 hours (48 hours max)
- Be constructive and kind
- Ask questions to understand intent
- Suggest alternatives, don't just criticize
- Approve when satisfied (not perfect)

### Testing Requirements

**Required for All Code:**
- Unit tests for new functions/methods
- Integration tests for API endpoints
- Update existing tests if behavior changes
- All tests must pass before merge

**Coverage Targets:**
- Unit test coverage: 80%+
- Integration test coverage: 70%+
- Critical payment paths: 95%+

### Deployment Process

**Environments:**
- **Local:** Your development machine
- **Staging:** staging.skyro.com (auto-deploys from `main`)
- **Production:** skyro.com (manual deployment process)

**Deployment Steps:**
1. Code merged to `main`
2. Automated tests run (CI pipeline)
3. Auto-deploy to staging
4. QA verification in staging
5. Create release tag
6. Deploy to production (requires approval)
7. Monitor for issues (15-30 minutes)

**Deployment Windows:**
- Regular deployments: Tuesday and Thursday, 10 AM - 2 PM EST
- Emergency hotfixes: Anytime (requires incident commander approval)
- No deployments: Friday afternoon, weekends, holidays

## On-Call Rotation

**Eligibility:** After 3 months and completing on-call training

**Responsibilities:**
- Monitor PagerDuty alerts
- Respond to incidents within 15 minutes
- Investigate and resolve issues
- Escalate if needed
- Document all incidents

**Rotation Schedule:**
- 1 week on-call rotation
- 24/7 availability during rotation
- Backup engineer assigned
- ₱200/week on-call bonus + overtime pay

**Preparation:**
- Complete on-call training
- Shadow experienced on-call engineer
- Review runbooks and playbooks
- Test PagerDuty notifications
- Have laptop and phone ready

## Resources and Documentation

**Technical Documentation:**
- Architecture diagrams: Confluence → Engineering → Architecture
- API documentation: docs.skyro.com
- Runbooks: wiki.skyro.com/runbooks
- ADRs (Architecture Decision Records): GitHub → /docs/adr/

**Learning Resources:**
- Internal tech talks (recorded): Learning Portal
- External courses: Unlimited access to Udemy for Business
- Conference attendance: 1-2 per year (budget permitting)
- Books: Reimbursed up to ₱500/year

**Getting Help:**
- Your mentor (assigned on Day 1)
- Team members (via Slack or in-person)
- Engineering wiki: wiki.skyro.com
- Ask in #help-engineering Slack channel

## Performance and Growth

### 30-60-90 Day Goals

**30 Days:**
- Complete onboarding checklist
- Deploy first feature to production
- Understand core systems
- Build relationships with team

**60 Days:**
- Independently complete sprint tasks
- Participate in technical design
- Review others' code effectively
- Contribute to documentation

**90 Days:**
- Take ownership of features
- Mentor newer engineers
- Propose improvements
- Fully productive team member

### Career Development

**Engineering Levels:**
- Engineer I (Entry level)
- Engineer II (Mid-level)
- Senior Engineer
- Staff Engineer
- Principal Engineer

**Promotion Criteria:**
- Technical skills and impact
- Leadership and mentorship
- Communication and collaboration
- Initiative and ownership

**Growth Opportunities:**
- Quarterly performance reviews
- Annual promotion cycles
- Technical leadership paths
- Management paths (optional)

## Company Culture

### Values
- **Customer First:** Everything we build serves customers
- **Move Fast:** Bias for action and rapid iteration
- **Own It:** Take ownership and see things through
- **Learn Always:** Continuous improvement mindset
- **Team Success:** We win or lose together

### Work-Life Balance
- Core hours: 10 AM - 4 PM (flexible outside this)
- Remote work: 2 days/week (team-dependent)
- Unlimited PTO (minimum 15 days/year encouraged)
- No after-hours work expected (except on-call)

### Perks and Benefits
- Competitive salary and equity
- Comprehensive health insurance
- 401(k) with company match
- Professional development budget
- Gym membership reimbursement
- Free lunch (in-office days)
- Standing desks and ergonomic equipment

## Important Contacts

**Your Manager:** [Name assigned on Day 1]  
**HR:** hr@skyro.com  
**IT Support:** it@skyro.com  
**Facilities:** facilities@skyro.com  
**Security:** security@skyro.com  

**Emergency Contacts:**
- Building Security: [Phone]
- IT Emergency: [Phone]
- On-Call Manager: See PagerDuty

---

## Onboarding Checklist

### Week 1
- [ ] Complete HR paperwork
- [ ] Set up all accounts and tools
- [ ] Complete security training
- [ ] Set up development environment
- [ ] Meet all team members
- [ ] Read key documentation
- [ ] Complete first contribution

### Week 2
- [ ] Attend all technical deep dives
- [ ] Complete first real task
- [ ] Submit first substantial PR
- [ ] Participate in sprint ceremonies
- [ ] Set up 1-on-1 with manager

### Week 3-4
- [ ] Take on sprint tasks independently
- [ ] Start reviewing PRs
- [ ] Present work in sprint demo
- [ ] Complete compliance certifications
- [ ] Shadow on-call (if applicable)

### 30 Days
- [ ] Deploy feature to production
- [ ] Provide onboarding feedback
- [ ] 30-day review with manager

---

**Welcome to the team! We're excited to have you at Skyro.**

For questions about this guide: engineering-ops@skyro.com
