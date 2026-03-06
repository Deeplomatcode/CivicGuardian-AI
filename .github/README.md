# CivicGuardian AI

**AWS 10,000 AIdeas 2026 Semifinalist - Social Impact Category**

AI-powered digital advocate protecting vulnerable adults from housing, benefits, and care crises.

## 🎯 Problem

12,000+ vulnerable adults in the UK lose housing annually due to missed correspondence deadlines. People with dementia, mental health conditions, and learning disabilities struggle to navigate complex letters from councils, housing associations, and healthcare providers.

## 💡 Solution

Multi-agent AI system that monitors correspondence, identifies urgent risks, and drafts policy-compliant responses before harm occurs.

**Architecture:** 3 specialized agents
- **Risk Analyst** (Amazon Nova Lite) - Urgency classification
- **Policy Reasoner** (Amazon Nova Pro) - Legal reasoning with UK Care Act 2014
- **Governor** (Pure Python) - Validation and safety checks

## 📊 Impact

- Target: <5% missed deadlines (down from 15%)
- Cost: $0.26 per case (sustainable at scale)
- Capacity: 1,000 cases/month on AWS Free Tier

## 🔒 Privacy & Security

Full GDPR compliance with end-to-end encryption, 7-day retention, and automated subject rights implementation.

## 🏗️ Built With

- **AI:** Amazon Bedrock (Nova Lite, Nova Pro)
- **Infrastructure:** AWS Lambda, Step Functions, S3, DynamoDB
- **Development:** AWS Kiro (specification-driven)
- **Testing:** 122 tests, 95%+ coverage

## 📖 Documentation

- [Full Article](article/builder-center-article.md)
- [Architecture Diagram](article/architecture-diagram.png)
- [GDPR Compliance](article/GDPR_COMPLIANCE_CHECKLIST.md)

## 🚀 Status

**Competition Ready** - Complete implementation with comprehensive documentation.

---

*Team Phenix | AWS 10,000 AIdeas 2026*
