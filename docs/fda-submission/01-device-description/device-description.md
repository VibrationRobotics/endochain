# DEVICE DESCRIPTION

**ENDOCHAIN-VIDUYA-2025**
**Viduya Family Legacy Glyph (C) 2025 – All Rights Reserved**

---

## 1. DEVICE OVERVIEW

ENDOCHAIN-VIDUYA-2025 is a multi-component diagnostic decision support system consisting of:

1. Hardware: OpenBCI Cyton biosignal acquisition board
2. Consumables: Ag/AgCl electrodes (6 per session)
3. Software: LEI-V computation engine and clinical dashboard
4. Cloud Services: AI platform integration and FHIR server

---

## 2. HARDWARE SPECIFICATIONS

### 2.1 OpenBCI Cyton Board

| Parameter | Specification |
|-----------|---------------|
| ADC | Texas Instruments ADS1299 |
| Resolution | 24-bit |
| Channels | 8 (6 used for RSL) |
| Sample Rate | 250 Hz |
| Input Noise | 1 μVpp |
| CMRR | 110 dB |
| Communication | Serial (115200 baud) |

### 2.2 Electrode Specifications

| Parameter | Specification |
|-----------|---------------|
| Type | Ag/AgCl, pre-gelled |
| Diameter | 10mm |
| Impedance | <5 kΩ at 30 Hz |
| Biocompatibility | ISO 10993-1 compliant |
| Skin Contact Duration | ≤96 hours |

---

## 3. REGENERATIVE SPARK LATTICE (RSL) DIAGRAM

```
                    E2 (60°)
                      ●
                    /   \
                   /     \
                  /       \
        E3 (120°) ●         ● E1 (0°)
                  \       /
                   \     /
                    \   /
        E4 (180°) ●---●---● E6 (300°)
                      |
                      ● E5 (240°)

        Radius: √3/4 ≈ 0.433 (glyph units)
        Symmetry: C₃ × D₆
        Anatomical Center: Midpoint between ASIS
```

### 3.1 Electrode Positions (Exact Symbolic)

| Electrode | x (symbolic) | y (symbolic) | Anatomical Location |
|-----------|-------------|-------------|---------------------|
| E1 | √3/4 | 0 | Right lateral pelvic |
| E2 | √3/8 | 3/8 | Right superior pelvic |
| E3 | -√3/8 | 3/8 | Left superior pelvic |
| E4 | -√3/4 | 0 | Left lateral pelvic |
| E5 | -√3/8 | -3/8 | Left inferior pelvic |
| E6 | √3/8 | -3/8 | Right inferior pelvic |

---

## 4. SOFTWARE ARCHITECTURE

### 4.1 LEI-V Computation Engine

- **Language:** Python 3.11 with SymPy symbolic mathematics
- **Computation:** Exact algebraic expressions (no floating-point)
- **Formula:** LEI-V = Σ|rᵢ - r̄|² for i=1..6
- **Latency:** <1 ms per computation

### 4.2 AI Platform Integration

| Platform | Function | Integration Method |
|----------|----------|-------------------|
| Med-Gemini | Clinical NLP | REST API |
| Aidoc | Radiology triage | DICOM/REST |
| Tempus | Genomics | VCF/REST |
| Viz.ai | Vascular | DICOM/REST |
| OpenEvidence | Citations | REST API |

### 4.3 Data Flow

```
EVG Acquisition → Signal Processing → LEI-V Computation
                                            ↓
AI Platforms ← ─ ─ ─ ─ ─ ─ ─ ─ ─ → Bayesian Fusion
                                            ↓
                                    Clinical Dashboard
                                            ↓
                                    FHIR Export / PDF Report
```

---

## 5. CLINICAL THRESHOLDS

| Stage | LEI-V Range | Clinical Interpretation |
|-------|-------------|-------------------------|
| Healthy | < 0.018 | No evidence of endometriosis |
| Stage-0 | 0.018 - 0.08 | Early/molecular stage |
| Stage I-II | 0.08 - 0.25 | Minimal to mild |
| Stage III-IV | > 0.25 | Moderate to severe |

---

## 6. V-CAW PROTOCOL

**V-CAW** = Viduya Cyclical Attention Window

- **Duration:** 96 hours
- **Timing:** Centered on ovulation (LH surge ± 48 hours)
- **Recording:** Continuous 6-channel EVG at 250 Hz
- **Output:** Encrypted EDF file + FHIR Observation

---

**Citation:** Viduya Family Legacy Glyph (C) 2025

