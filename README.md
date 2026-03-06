# CivicGuardian AI

**Digital safeguarding advocate for vulnerable adults**

AWS 10,000 AIdeas Competition - Social Impact Category

## Team
**Team Phenix** | Mohammed Bakare | United Kingdom

## Project Status

### Competition Timeline
- **Deadline:** March 13, 2025, 8:00 PM UTC
- **Voting Ends:** March 20, 2025
- **Days Remaining:** 14

### Development Progress
- ✅ **Phase 1: Requirements** (Feb 27) - 20 detailed specifications
- ✅ **Phase 2: Design** (Feb 27) - Complete architecture
- ⏳ **Phase 3: Implementation** - Starting next
- ⏳ **Phase 4: Testing** - Pending
- ⏳ **Phase 5: Article** - Pending

### Kiro Development Log
| Date | Task | Credits Used | Running Total |
|------|------|--------------|---------------|
| Feb 27 | Requirements specification | 0.51 | 0.51 / 2000 |
| Feb 27 | System design & architecture | 0.47 | 0.98 / 2000 |

### AWS Resources
- **Credits:** $200 (Code: PC1WER98M1RRR95) ✅ Applied
- **Services:** Bedrock (Nova), Lambda, S3, Step Functions, DynamoDB, Textract, Transcribe, SNS, API Gateway, CloudWatch

## Architecture

Multi-agent serverless Guardian Loop:
1. **Document Ingestion:** S3 → Lambda → Textract/Transcribe → extract text
2. **Risk Analysis:** Nova Lite classifies urgency (LOW/MEDIUM/HIGH/CRITICAL)
3. **Policy Reasoning:** Nova Pro applies UK legislation
4. **Governor:** Validates outputs, flags low-confidence cases
5. **Human Escalation:** Critical cases → SNS → caseworker approval

## Cost Analysis
- **During Pilot:** $0.001 per document (AWS Free Tier)
- **Post Free Tier:** $0.040 per document
- **Monthly Cost:** <$5 for 100 documents/day

## Documentation
- `specs/requirements.md` - 20 detailed requirements with acceptance criteria
- `specs/design.md` - Complete system architecture, Lambda pseudocode, testing strategy

## Privacy & GDPR Compliance

CivicGuardian AI processes sensitive data about vulnerable adults with full GDPR compliance:

- **Legal Basis:** Article 6(1)(d) vital interests + Article 9(2)(c) special category health data
- **Encryption:** AES-256 at rest (S3, DynamoDB), TLS 1.2+ in transit
- **Data Minimization:** 7-day retention policy, no unnecessary PII storage
- **Subject Rights:** Access, erasure, portability, rectification via API
- **Governance:** DPIA template prepared, privacy notice drafted for pilot partners

See `article/GDPR_COMPLIANCE_CHECKLIST.md` for complete compliance documentation.

## Next Steps
1. Implement Lambda functions (Kiro-assisted)
2. Create DynamoDB schemas
3. Build Step Functions workflow
4. Write integration tests
5. Prepare Builder Center article

---

**Built with Kiro** | Competing for AWS 10,000 AIdeas Finals
