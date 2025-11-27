# ENDOCHAIN AI Integrations
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Multi-platform AI integration layer with unified interface.

Platforms:
- Google Med-Gemini: Clinical NLP and structured reports
- Aidoc: Radiology AI for TVUS/MRI (AUC 0.95 for POD detection)
- Tempus: Genomic correlation and risk stratification
- Viz.ai: Vascular perfusion and deep infiltrating scoring
- OpenEvidence: Real-time literature synthesis and citations
"""

from .universal_caller import UniversalAICaller
from .med_gemini import MedGeminiClient
from .aidoc import AidocClient
from .tempus import TempusClient
from .viz_ai import VizAIClient
from .openevidence import OpenEvidenceClient
from .bayesian_fusion import BayesianFusionEngine

__all__ = [
    "UniversalAICaller",
    "MedGeminiClient",
    "AidocClient",
    "TempusClient",
    "VizAIClient",
    "OpenEvidenceClient",
    "BayesianFusionEngine"
]

