# ENDOCHAIN-VIDUYA-2025

**The World's First Geometrically-Anchored, Non-Invasive Endometriosis Diagnostic System**

[![CI/CD](https://github.com/endochain/endochain-viduya-2025/workflows/CI/badge.svg)](https://github.com/endochain/endochain-viduya-2025/actions)
[![Coverage](https://codecov.io/gh/endochain/endochain-viduya-2025/branch/main/graph/badge.svg)](https://codecov.io/gh/endochain/endochain-viduya-2025)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

---

## 🎯 Mission

End the **10-year diagnostic delay** for **200 million women** suffering from endometriosis worldwide.

---

## ⚡ Key Innovation

**LEI-V (Lesion Entropy Index - Viduya variant)** is a novel biomarker derived from the **Viduya Legacy Glyph** – a sacred geometric construction with provable C₃ × D₆ symmetry.

### Performance (Pilot n=18)
- **Sensitivity:** 100%
- **Specificity:** 92%
- **Target AUC:** ≥0.95

---

## 🏗️ Architecture

```
ENDOCHAIN-VIDUYA-2025/
├── core/               # LEI-V mathematics (SymPy)
├── backend/            # FastAPI + FHIR server
├── frontend/           # React medical dashboard
├── ai_integrations/    # Med-Gemini, Aidoc, Tempus, Viz.ai
├── hardware/           # OpenBCI EVG driver
├── tests/              # pytest (≥95% coverage)
└── docs/               # Master manual + FDA submission
```

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/endochain/endochain-viduya-2025.git
cd endochain-viduya-2025

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Start backend server
uvicorn backend.main:app --reload

# Start frontend (in separate terminal)
cd frontend && npm install && npm run dev
```

---

## 📊 LEI-V Thresholds

| Stage | LEI-V Range | Interpretation |
|-------|-------------|----------------|
| Healthy | < 0.018 | No endometriosis |
| Stage-0 | 0.018 - 0.08 | Early/molecular |
| Stage I-II | 0.08 - 0.25 | Minimal to mild |
| Stage III-IV | > 0.25 | Moderate to severe |

---

## 🔬 Viduya Legacy Glyph Coordinates

All coordinates are **exact symbolic expressions**:

```
Triangle-Hexagon: (±√3/4, 0), (±√3/8, ±3/8)
Vesica-Hexagon: √3(3/80 ± √229/80), −37/80 + √229/80
Hidden Star: ±(7/40 − √2/4), −3/8
```

**Symmetry:** C₃ × D₆

---

## 📋 Regulatory Status

| Region | Pathway | Status |
|--------|---------|--------|
| FDA | 510(k) De Novo | In preparation |
| EU | MDR Class IIa | Planned |
| Health Canada | Class III | Planned |

---

## 📄 Citation

```bibtex
@misc{endochain2025,
  title={ENDOCHAIN-VIDUYA-2025: Geometric Entropy Biomarker for Endometriosis},
  author={Manosca, Ariel Viduya and IAMVC Holdings LLC},
  year={2025},
  note={Viduya Family Legacy Glyph © 2025}
}
```

---

## ⚖️ License

**Viduya Family Legacy Glyph © 2025 – All Rights Reserved**

Creator: Ariel Viduya Manosca | Author: IAMVC Holdings LLC

The LEI-V calculation algorithm and electrode mapping are open-source (MIT).
The Viduya Legacy Glyph coordinates and geometric derivation are proprietary.

---

## 📬 Contact

- **Research:** research@endochain.org
- **Clinical:** clinical@endochain.org
- **Website:** https://endochain.org

