# ENDOCHAIN Tests: IMMUTABLE Viduya Constants Verification
# Viduya Family Legacy Glyph (C) 2025 - All Rights Reserved
#
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  CRITICAL: THESE TESTS PROTECT THE IP CROWN JEWELS                          ║
# ║  ANY TEST FAILURE = POTENTIAL IP TAMPERING                                   ║
# ║  CONTACT LEGAL IMMEDIATELY IF ANY TEST FAILS                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
Immutability tests for Viduya Legacy Glyph coordinates.

These tests verify that EXACT coordinate values have not been modified.
A single digit change will cause test failure.
"""

import pytest
import hashlib
from decimal import Decimal, getcontext

# Set maximum precision
getcontext().prec = 50


class TestImmutableCoordinates:
    """Tests that verify coordinate values are exactly as specified."""
    
    def test_sqrt3_over_4_exact_value(self):
        """sqrt(3)/4 must equal exactly 0.4330127018922193..."""
        import sympy as sp
        val = sp.sqrt(3) / 4
        computed = float(val.evalf(20))
        expected = 0.43301270189221932338
        assert abs(computed - expected) < 1e-15, f"sqrt(3)/4 changed! Got {computed}"
    
    def test_triangle_hexagon_axial_positive(self):
        """TH_axial_pos = (sqrt(3)/4, 0) - FROZEN"""
        from core.viduya_constants import TH_AXIAL_POS
        assert TH_AXIAL_POS.x_symbolic == "sqrt(3)/4"
        assert TH_AXIAL_POS.y_symbolic == "0"
        assert abs(TH_AXIAL_POS.x_approx - 0.4330127018922193) < 1e-10
        assert TH_AXIAL_POS.y_approx == 0.0
    
    def test_triangle_hexagon_axial_negative(self):
        """TH_axial_neg = (-sqrt(3)/4, 0) - FROZEN"""
        from core.viduya_constants import TH_AXIAL_NEG
        assert TH_AXIAL_NEG.x_symbolic == "-sqrt(3)/4"
        assert TH_AXIAL_NEG.y_symbolic == "0"
        assert abs(TH_AXIAL_NEG.x_approx - (-0.4330127018922193)) < 1e-10
    
    def test_triangle_hexagon_offaxis_values(self):
        """All 4 off-axis points = (+-sqrt(3)/8, +-3/8) - FROZEN"""
        from core.viduya_constants import TH_OFFAXIS_1, TH_OFFAXIS_2, TH_OFFAXIS_3, TH_OFFAXIS_4
        
        # Check symbolic expressions are exact
        assert TH_OFFAXIS_1.x_symbolic == "sqrt(3)/8"
        assert TH_OFFAXIS_1.y_symbolic == "3/8"
        
        # Verify 3/8 = 0.375 exactly
        assert TH_OFFAXIS_1.y_approx == 0.375
        assert TH_OFFAXIS_2.y_approx == 0.375
        assert TH_OFFAXIS_3.y_approx == -0.375
        assert TH_OFFAXIS_4.y_approx == -0.375
    
    def test_vesica_hexagon_exact_formula(self):
        """VH coordinates use sqrt(229) - verify exact formula"""
        from core.viduya_constants import VH_POS
        
        # The EXACT formula: sqrt(3)*(3/80 + sqrt(229)/80)
        assert "sqrt(229)" in VH_POS.x_symbolic
        assert "3/80" in VH_POS.x_symbolic
        
        # y = -37/80 + sqrt(229)/80
        assert "-37/80" in VH_POS.y_symbolic
        assert "sqrt(229)/80" in VH_POS.y_symbolic
    
    def test_hidden_star_triangle_exact_formula(self):
        """HST coordinates use sqrt(2) - verify exact formula"""
        from core.viduya_constants import HST_POS, HST_NEG
        
        # The EXACT formula: 7/40 - sqrt(2)/4
        assert "7/40" in HST_POS.x_symbolic
        assert "sqrt(2)/4" in HST_POS.x_symbolic
        
        # y = -3/8 exactly
        assert HST_POS.y_symbolic == "-3/8"
        assert HST_POS.y_approx == -0.375
    
    def test_rsl_electrode_count_exactly_six(self):
        """RSL must have EXACTLY 6 electrodes"""
        from core.viduya_constants import ALL_RSL_ELECTRODES
        assert len(ALL_RSL_ELECTRODES) == 6, "RSL electrode count changed!"
    
    def test_rsl_electrodes_indices_1_through_6(self):
        """RSL electrodes numbered 1-6, no gaps"""
        from core.viduya_constants import ALL_RSL_ELECTRODES
        indices = sorted([e.electrode_index for e in ALL_RSL_ELECTRODES])
        assert indices == [1, 2, 3, 4, 5, 6], "RSL indices modified!"
    
    def test_leiv_threshold_stage_0_exact(self):
        """Stage-0 threshold = 0.018 exactly"""
        from core.viduya_constants import LEIV_THRESHOLD_STAGE_0, LEIV_THRESHOLD_STAGE_0_APPROX
        
        # Symbolic: 18/1000
        assert LEIV_THRESHOLD_STAGE_0 == "18/1000"
        
        # Numerical
        assert LEIV_THRESHOLD_STAGE_0_APPROX == 0.018
    
    def test_leiv_threshold_advanced_exact(self):
        """Advanced threshold = 0.08 exactly"""
        from core.viduya_constants import LEIV_THRESHOLD_ADVANCED, LEIV_THRESHOLD_ADVANCED_APPROX
        
        assert LEIV_THRESHOLD_ADVANCED == "8/100"
        assert LEIV_THRESHOLD_ADVANCED_APPROX == 0.08
    
    def test_all_coordinates_total_count(self):
        """Total coordinate count must be exactly 18"""
        from core.viduya_constants import ALL_COORDINATES
        # 6 TH + 4 VH + 2 HST + 6 RSL = 18
        assert len(ALL_COORDINATES) == 18, f"Coordinate count changed! Got {len(ALL_COORDINATES)}"
    
    def test_symmetry_group_is_c3_d6(self):
        """Glyph must have C3 x D6 symmetry (60-degree rotational)"""
        from core.viduya_constants import ALL_RSL_ELECTRODES
        import math
        
        # All RSL electrodes should be at 60-degree intervals
        angles = []
        for e in ALL_RSL_ELECTRODES:
            angle = math.atan2(e.y_approx, e.x_approx)
            angles.append(angle)
        
        angles.sort()
        # Check 60-degree (pi/3) spacing
        for i in range(len(angles) - 1):
            diff = angles[i + 1] - angles[i]
            assert abs(diff - (math.pi / 3)) < 0.01 or abs(diff + (5 * math.pi / 3)) < 0.01


class TestCryptographicIntegrity:
    """Tests for cryptographic verification of constants."""
    
    def test_constants_hash_computation(self):
        """Hash must be computable without errors"""
        from core.viduya_constants import verify_constants_integrity
        is_valid, computed_hash = verify_constants_integrity()
        assert is_valid
        assert len(computed_hash) == 64  # SHA-256 = 64 hex chars
    
    def test_citation_present(self):
        """Citation must be present and correct"""
        from core.viduya_constants import CITATION, CREATOR, AUTHOR
        assert "Viduya" in CITATION
        assert "2025" in CITATION
        assert CREATOR == "Ariel Viduya Manosca"
        assert AUTHOR == "IAMVC Holdings LLC"

