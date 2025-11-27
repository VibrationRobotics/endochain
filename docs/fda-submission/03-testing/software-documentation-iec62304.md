# SOFTWARE DOCUMENTATION (IEC 62304 Class B)

**ENDOCHAIN-VIDUYA-2025**
**Viduya Family Legacy Glyph (C) 2025 – All Rights Reserved**

---

## 1. SOFTWARE SAFETY CLASSIFICATION

| Parameter | Value |
|-----------|-------|
| Standard | IEC 62304:2006/AMD1:2015 |
| Classification | Class B |
| Rationale | Non-serious injury possible; no death or serious injury |

### 1.1 Classification Justification

- Device provides decision support only
- Final diagnosis requires clinician confirmation
- False results may lead to delayed treatment (non-serious)
- System includes multiple redundancies and verification

---

## 2. SOFTWARE DEVELOPMENT PLAN

### 2.1 Development Model

- **Methodology:** Agile with regulatory gates
- **Sprint Length:** 2 weeks
- **Release Cycle:** Quarterly
- **Version Control:** Git (GitHub)
- **CI/CD:** GitHub Actions

### 2.2 Development Activities

| Phase | Activities | IEC 62304 Reference |
|-------|-----------|-------------------|
| Requirements | User needs, system requirements | 5.2 |
| Architecture | Software architecture design | 5.3 |
| Detailed Design | Module specifications | 5.4 |
| Implementation | Coding, unit testing | 5.5 |
| Integration | Integration testing | 5.6 |
| System Testing | Validation testing | 5.7 |
| Release | Release documentation | 5.8 |

---

## 3. SOFTWARE REQUIREMENTS SPECIFICATION

### 3.1 Functional Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-001 | System shall compute LEI-V from 6 electrode readings | Unit test |
| FR-002 | System shall classify LEI-V into 5 stages | Unit test |
| FR-003 | System shall generate FHIR Observation resource | Integration test |
| FR-004 | System shall generate audit hash for each computation | Unit test |
| FR-005 | System shall complete computation in <3 minutes | Performance test |
| FR-006 | System shall encrypt all PHI at rest and in transit | Security test |

### 3.2 Performance Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| PR-001 | LEI-V computation latency | <1 ms |
| PR-002 | End-to-end report generation | <3 min |
| PR-003 | API response time | <500 ms |
| PR-004 | System uptime | 99.9% |

### 3.3 Security Requirements

| ID | Requirement |
|----|-------------|
| SR-001 | TLS 1.3 for all network communication |
| SR-002 | AES-256 encryption for data at rest |
| SR-003 | JWT authentication for API access |
| SR-004 | Role-based access control (RBAC) |
| SR-005 | Audit logging of all PHI access |

---

## 4. SOFTWARE ARCHITECTURE

### 4.1 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ENDOCHAIN-VIDUYA-2025                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │    Core     │  │   Backend   │  │  Frontend   │          │
│  │  (Python)   │  │  (FastAPI)  │  │   (React)   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                  │
│         └────────────────┼────────────────┘                  │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────┐          │
│  │              PostgreSQL Database               │          │
│  └───────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 SOUP (Software of Unknown Provenance)

| Component | Version | Risk Assessment |
|-----------|---------|-----------------|
| Python | 3.11 | Low - widely validated |
| SymPy | 1.12 | Low - symbolic math library |
| FastAPI | 0.109 | Low - web framework |
| React | 18.2 | Low - UI framework |
| PostgreSQL | 15 | Low - database |
| OpenBCI SDK | 2.0 | Medium - hardware interface |

---

## 5. SOFTWARE TESTING

### 5.1 Test Coverage Requirements

| Level | Target Coverage |
|-------|-----------------|
| Unit Tests | ≥95% |
| Integration Tests | ≥90% |
| System Tests | 100% of requirements |

### 5.2 Test Summary (Current)

| Test Suite | Tests | Passed | Failed | Coverage |
|------------|-------|--------|--------|----------|
| Core LEI-V | 18 | 18 | 0 | 98% |
| Immutability | 14 | 14 | 0 | 100% |
| Backend API | TBD | TBD | TBD | TBD |
| Frontend | TBD | TBD | TBD | TBD |

---

## 6. CONFIGURATION MANAGEMENT

### 6.1 Version Numbering

- **Format:** MAJOR.MINOR.PATCH (SemVer)
- **Current:** 1.0.0
- **Branches:** main (production), develop (staging)

### 6.2 Change Control

All changes require:
1. Pull request with code review
2. Passing CI/CD pipeline
3. Documentation update
4. Regulatory impact assessment

---

## 7. PROBLEM RESOLUTION

### 7.1 Defect Classification

| Severity | Definition | Response Time |
|----------|------------|---------------|
| Critical | Patient safety impact | 24 hours |
| Major | Functional failure | 72 hours |
| Minor | Cosmetic/usability | Next release |

---

**Citation:** Viduya Family Legacy Glyph (C) 2025

