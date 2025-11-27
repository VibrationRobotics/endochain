# ENDOCHAIN Core Mathematics Module
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
# Creator: Ariel Viduya Manosca | Author: IAMVC holdings LLC
"""
Core LEI-V (Lesion Entropy Index - Viduya variant) calculation engine.

This module provides symbolically-exact geometric computations with
256-bit cryptographic audit hashes for regulatory compliance.
"""

__version__ = "1.0.0"
__author__ = "IAMVC Holdings LLC"
__copyright__ = "Viduya Family Legacy Glyph © 2025"

from .viduya_glyph import ViduyaGlyph, GlyphCoordinate
from .lei_v import LEIVCalculator, LEIVResult
from .audit import AuditHasher

__all__ = [
    "ViduyaGlyph",
    "GlyphCoordinate", 
    "LEIVCalculator",
    "LEIVResult",
    "AuditHasher",
]

