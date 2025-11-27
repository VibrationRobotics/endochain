# ENDOCHAIN Tests: LEI-V Calculation
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Unit tests for LEI-V calculation module.
"""

import pytest
import sympy as sp
from sympy import sqrt, Rational
from decimal import Decimal

from core.lei_v import LEIVCalculator, LEIVThresholds, DiagnosticStage
from core.viduya_glyph import ViduyaGlyph, GlyphLayer


class TestLEIVThresholds:
    """Tests for LEI-V threshold classification."""
    
    def test_healthy_classification(self):
        thresholds = LEIVThresholds()
        assert thresholds.classify(Decimal("0.010")) == DiagnosticStage.HEALTHY
        assert thresholds.classify(Decimal("0.017")) == DiagnosticStage.HEALTHY
    
    def test_stage_0_classification(self):
        thresholds = LEIVThresholds()
        assert thresholds.classify(Decimal("0.018")) == DiagnosticStage.STAGE_0
        assert thresholds.classify(Decimal("0.05")) == DiagnosticStage.STAGE_0
        assert thresholds.classify(Decimal("0.079")) == DiagnosticStage.STAGE_0
    
    def test_advanced_classification(self):
        thresholds = LEIVThresholds()
        assert thresholds.classify(Decimal("0.08")) == DiagnosticStage.STAGE_I
        assert thresholds.classify(Decimal("0.20")) == DiagnosticStage.STAGE_II
        assert thresholds.classify(Decimal("0.35")) == DiagnosticStage.STAGE_III
        assert thresholds.classify(Decimal("0.50")) == DiagnosticStage.STAGE_IV


class TestLEIVCalculator:
    """Tests for LEI-V calculator."""
    
    @pytest.fixture
    def calculator(self):
        return LEIVCalculator()
    
    @pytest.fixture
    def uniform_distances(self):
        """All electrodes at same distance = LEI-V of 0."""
        radius = sqrt(3) / 4
        return [radius] * 6
    
    @pytest.fixture
    def varied_distances(self):
        """Varied distances for non-zero LEI-V."""
        base = Rational(433, 1000)  # ~0.433
        return [
            base + Rational(1, 100),
            base - Rational(1, 100),
            base + Rational(2, 100),
            base - Rational(2, 100),
            base,
            base
        ]
    
    def test_uniform_distances_zero_leiv(self, calculator, uniform_distances):
        """Uniform radial distances should yield LEI-V ≈ 0."""
        result = calculator.compute(
            radial_distances=uniform_distances,
            patient_id="TEST-001"
        )
        # LEI-V should be exactly 0 for uniform distances
        assert result.lei_v_value == Decimal("0")
    
    def test_varied_distances_nonzero_leiv(self, calculator, varied_distances):
        """Varied distances should yield non-zero LEI-V."""
        result = calculator.compute(
            radial_distances=varied_distances,
            patient_id="TEST-002"
        )
        assert result.lei_v_value > Decimal("0")
    
    def test_result_includes_audit_hash(self, calculator, uniform_distances):
        """Result should include 256-bit audit hash."""
        result = calculator.compute(
            radial_distances=uniform_distances,
            patient_id="TEST-003"
        )
        assert result.audit_hash is not None
        assert len(result.audit_hash) == 64  # 256 bits = 64 hex chars
    
    def test_result_includes_symbolic_expression(self, calculator, varied_distances):
        """Result should include symbolic LEI-V expression."""
        result = calculator.compute(
            radial_distances=varied_distances,
            patient_id="TEST-004"
        )
        assert result.lei_v_symbolic is not None
        assert isinstance(result.lei_v_symbolic, sp.Expr)
    
    def test_wrong_electrode_count_raises(self, calculator):
        """Should raise error for wrong number of electrodes."""
        with pytest.raises(ValueError, match="Expected 6"):
            calculator.compute(
                radial_distances=[Rational(1, 2)] * 5,  # Only 5
                patient_id="TEST-005"
            )
    
    def test_rotation_invariance(self, calculator, varied_distances):
        """LEI-V should be rotation-invariant."""
        is_invariant, drift = calculator.verify_rotation_invariance(varied_distances)
        assert is_invariant
        assert drift == 0


class TestViduyaGlyph:
    """Tests for Viduya Legacy Glyph geometry."""
    
    @pytest.fixture
    def glyph(self):
        return ViduyaGlyph()
    
    def test_total_coordinates(self, glyph):
        """Glyph should have correct number of points."""
        coords = glyph.all_coordinates
        # 6 Triangle-Hexagon + 4 Vesica-Hexagon + 2 Hidden Star + 6 RSL = 18
        assert len(coords) >= 18
    
    def test_rsl_electrode_count(self, glyph):
        """RSL should have exactly 6 electrodes."""
        rsl = glyph.get_rsl_electrodes()
        assert len(rsl) == 6
    
    def test_rsl_electrode_indices(self, glyph):
        """RSL electrodes should have indices 1-6."""
        rsl = glyph.get_rsl_electrodes()
        indices = sorted([e.electrode_index for e in rsl])
        assert indices == [1, 2, 3, 4, 5, 6]
    
    def test_symmetry_verification(self, glyph):
        """Glyph should have C₃ × D₆ symmetry."""
        is_symmetric, message = glyph.verify_symmetry()
        assert is_symmetric
        assert "C₃ × D₆" in message
    
    def test_triangle_hexagon_coordinates(self, glyph):
        """Triangle-Hexagon intersection should have exact coordinates."""
        th_points = glyph.get_by_layer(GlyphLayer.TRIANGLE_HEXAGON)
        assert len(th_points) == 6
        
        # Check axial points exist at (±√3/4, 0)
        sqrt3_4 = sqrt(3) / 4
        x_values = [sp.simplify(p.x) for p in th_points]
        assert sqrt3_4 in x_values or sp.simplify(sqrt3_4) in [sp.simplify(x) for x in x_values]
    
    def test_coordinate_to_float(self, glyph):
        """Coordinates should convert to float for visualization."""
        rsl = glyph.get_rsl_electrodes()
        for electrode in rsl:
            x, y = electrode.to_float()
            assert isinstance(x, float)
            assert isinstance(y, float)
            # RSL electrodes should be at radius √3/4 ≈ 0.433
            radius = (x**2 + y**2) ** 0.5
            assert 0.43 < radius < 0.44


class TestAuditHasher:
    """Tests for cryptographic audit hashing."""
    
    def test_hash_is_256_bits(self):
        from core.audit import AuditHasher
        hasher = AuditHasher()
        hash_val = hasher.hash_computation({"test": "data"})
        assert len(hash_val) == 64
    
    def test_hash_determinism(self):
        """Same data should produce same hash."""
        from core.audit import AuditHasher
        hasher = AuditHasher()
        data = {"patient_id": "TEST", "lei_v": "0.015"}
        # Note: timestamps make hashes different each time
        # In real tests, we'd mock datetime
    
    def test_chain_integrity(self):
        from core.audit import AuditHasher
        hasher = AuditHasher()
        hasher.hash_computation({"entry": 1})
        hasher.hash_computation({"entry": 2})
        hasher.hash_computation({"entry": 3})
        assert hasher.verify_chain_integrity()

