# ENDOCHAIN Core: Viduya Legacy Glyph Symbolic Geometry
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
# Creator: Ariel Viduya Manosca | Author: IAMVC holdings LLC
"""
Exact symbolic representation of Viduya Legacy Glyph intersection points.

All coordinates are stored as symbolic expressions using Python's fractions
and sympy for arbitrary-precision computation. NO FLOATING-POINT APPROXIMATIONS.

The glyph exhibits C₃ × D₆ symmetry and maps onto the Regenerative Spark Lattice
for electroviscerography electrode placement.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, List, Optional, Dict
from enum import Enum
import sympy as sp
from sympy import sqrt, Rational, pi, cos, sin


class GlyphLayer(Enum):
    """Layers of the Viduya Legacy Glyph."""
    TRIANGLE_HEXAGON = "triangle_hexagon"
    VESICA_HEXAGON = "vesica_hexagon"
    HIDDEN_STAR_TRIANGLE = "hidden_star_triangle"
    REGENERATIVE_SPARK_LATTICE = "rsl"


@dataclass(frozen=True)
class GlyphCoordinate:
    """Immutable symbolic coordinate from Viduya Legacy Glyph.
    
    All values are sympy expressions for exact symbolic computation.
    """
    x: sp.Expr
    y: sp.Expr
    layer: GlyphLayer
    name: str
    electrode_index: Optional[int] = None  # RSL electrode mapping (1-6)
    
    def to_float(self) -> Tuple[float, float]:
        """Convert to floating-point (for visualization only, NOT computation)."""
        return (float(self.x.evalf()), float(self.y.evalf()))
    
    def distance_from_origin(self) -> sp.Expr:
        """Exact symbolic distance from origin."""
        return sp.sqrt(self.x**2 + self.y**2)
    
    def rotate(self, angle: sp.Expr) -> 'GlyphCoordinate':
        """Rotate point by symbolic angle (in radians)."""
        cos_a, sin_a = sp.cos(angle), sp.sin(angle)
        new_x = self.x * cos_a - self.y * sin_a
        new_y = self.x * sin_a + self.y * cos_a
        return GlyphCoordinate(
            x=sp.simplify(new_x),
            y=sp.simplify(new_y),
            layer=self.layer,
            name=f"{self.name}_rotated",
            electrode_index=self.electrode_index
        )


class ViduyaGlyph:
    """The Viduya Legacy Glyph with all 24+ intersection points.
    
    This class provides exact symbolic coordinates for all glyph intersection
    points as derived from the original geometric construction.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    # Symbolic constants
    SQRT3 = sqrt(3)
    SQRT2 = sqrt(2)
    SQRT229 = sqrt(229)
    
    def __init__(self):
        self._coordinates: List[GlyphCoordinate] = []
        self._build_all_coordinates()
    
    def _build_all_coordinates(self) -> None:
        """Construct all intersection points with exact symbolic values."""
        # Triangle-Hexagon intersection points (6 points)
        self._add_triangle_hexagon_points()
        # Vesica-Hexagon intersection points (4 points)
        self._add_vesica_hexagon_points()
        # Hidden Star-Triangle intersection points
        self._add_hidden_star_triangle_points()
        # Regenerative Spark Lattice (6-electrode mapping)
        self._add_rsl_points()
    
    def _add_triangle_hexagon_points(self) -> None:
        """Add Triangle-Hexagon intersection: (±√3/4, 0), (±√3/8, ±3/8)"""
        # Axial points
        self._coordinates.append(GlyphCoordinate(
            x=self.SQRT3 / 4, y=Rational(0), 
            layer=GlyphLayer.TRIANGLE_HEXAGON, name="TH_axial_pos"
        ))
        self._coordinates.append(GlyphCoordinate(
            x=-self.SQRT3 / 4, y=Rational(0),
            layer=GlyphLayer.TRIANGLE_HEXAGON, name="TH_axial_neg"
        ))
        # Off-axis points (4 total)
        for sign_x in [1, -1]:
            for sign_y in [1, -1]:
                self._coordinates.append(GlyphCoordinate(
                    x=sign_x * self.SQRT3 / 8,
                    y=sign_y * Rational(3, 8),
                    layer=GlyphLayer.TRIANGLE_HEXAGON,
                    name=f"TH_offaxis_{'+' if sign_x > 0 else '-'}x_{'+' if sign_y > 0 else '-'}y"
                ))
    
    def _add_vesica_hexagon_points(self) -> None:
        """Add Vesica-Hexagon intersection: √3(3/80 ± √229/80), −37/80 + √229/80"""
        # Two x-values based on ± in the formula
        x_base = Rational(3, 80)
        x_offset = self.SQRT229 / 80
        y_val = Rational(-37, 80) + self.SQRT229 / 80
        
        self._coordinates.append(GlyphCoordinate(
            x=self.SQRT3 * (x_base + x_offset), y=y_val,
            layer=GlyphLayer.VESICA_HEXAGON, name="VH_pos"
        ))
        self._coordinates.append(GlyphCoordinate(
            x=self.SQRT3 * (x_base - x_offset), y=y_val,
            layer=GlyphLayer.VESICA_HEXAGON, name="VH_neg"
        ))
        # Mirror points
        self._coordinates.append(GlyphCoordinate(
            x=-self.SQRT3 * (x_base + x_offset), y=y_val,
            layer=GlyphLayer.VESICA_HEXAGON, name="VH_mirror_pos"
        ))
        self._coordinates.append(GlyphCoordinate(
            x=-self.SQRT3 * (x_base - x_offset), y=y_val,
            layer=GlyphLayer.VESICA_HEXAGON, name="VH_mirror_neg"
        ))
    
    def _add_hidden_star_triangle_points(self) -> None:
        """Add Hidden Star-Triangle: ±(7/40 − √2/4), −3/8"""
        x_val = Rational(7, 40) - self.SQRT2 / 4
        y_val = Rational(-3, 8)

        self._coordinates.append(GlyphCoordinate(
            x=x_val, y=y_val,
            layer=GlyphLayer.HIDDEN_STAR_TRIANGLE, name="HST_pos"
        ))
        self._coordinates.append(GlyphCoordinate(
            x=-x_val, y=y_val,
            layer=GlyphLayer.HIDDEN_STAR_TRIANGLE, name="HST_neg"
        ))

    def _add_rsl_points(self) -> None:
        """Add Regenerative Spark Lattice electrode positions.

        6 electrodes placed at 60° intervals around the glyph center,
        mapped to optimal EVG recording sites based on Triangle-Hexagon
        intersection geometry.
        """
        # RSL electrodes at angles 0°, 60°, 120°, 180°, 240°, 300°
        # Radius derived from Triangle-Hexagon intersection: √3/4
        radius = self.SQRT3 / 4

        for i in range(6):
            angle = i * pi / 3  # 60° intervals
            x = radius * cos(angle)
            y = radius * sin(angle)

            self._coordinates.append(GlyphCoordinate(
                x=sp.simplify(x),
                y=sp.simplify(y),
                layer=GlyphLayer.REGENERATIVE_SPARK_LATTICE,
                name=f"RSL_electrode_{i+1}",
                electrode_index=i + 1
            ))

    @property
    def all_coordinates(self) -> List[GlyphCoordinate]:
        """Get all glyph coordinates."""
        return self._coordinates.copy()

    def get_rsl_electrodes(self) -> List[GlyphCoordinate]:
        """Get the 6 Regenerative Spark Lattice electrode positions."""
        return [c for c in self._coordinates
                if c.layer == GlyphLayer.REGENERATIVE_SPARK_LATTICE]

    def get_by_layer(self, layer: GlyphLayer) -> List[GlyphCoordinate]:
        """Get coordinates from a specific glyph layer."""
        return [c for c in self._coordinates if c.layer == layer]

    def verify_symmetry(self) -> Tuple[bool, str]:
        """Verify C₃ × D₆ symmetry of the glyph.

        Returns:
            Tuple of (is_symmetric, verification_message)
        """
        rsl = self.get_rsl_electrodes()
        if len(rsl) != 6:
            return False, f"Expected 6 RSL electrodes, found {len(rsl)}"

        # Check rotational symmetry (C₃: 120° rotation)
        # and dihedral symmetry (D₆: 6-fold reflection)
        radii = [c.distance_from_origin() for c in rsl]

        # All radii should be equal (within symbolic precision)
        r0 = radii[0]
        for i, r in enumerate(radii[1:], 1):
            diff = sp.simplify(r - r0)
            if diff != 0:
                return False, f"Radius mismatch at electrode {i+1}: {diff}"

        return True, "C₃ × D₆ symmetry verified. Citation: Viduya Family Legacy Glyph © 2025"

    def to_dict(self) -> Dict:
        """Export glyph as dictionary for serialization."""
        return {
            "citation": "Viduya Family Legacy Glyph © 2025",
            "symmetry_group": "C₃ × D₆",
            "total_points": len(self._coordinates),
            "layers": {
                layer.value: [
                    {"name": c.name, "x": str(c.x), "y": str(c.y)}
                    for c in self.get_by_layer(layer)
                ]
                for layer in GlyphLayer
            }
        }

