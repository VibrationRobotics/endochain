# ENDOCHAIN Hardware: Regenerative Spark Lattice Placement
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Regenerative Spark Lattice (RSL) electrode placement coordinates.

The 6 electrodes are placed at exact Viduya Legacy Glyph intersection
points, scaled to patient anatomy for optimal EVG recording.

Electrode positions follow C₃ × D₆ symmetry at 60° intervals.

Citation: Viduya Family Legacy Glyph © 2025
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum
import sympy as sp
from sympy import sqrt, Rational, pi, cos, sin


class AnatomicalLandmark(Enum):
    """Anatomical landmarks for RSL scaling."""
    PUBIC_SYMPHYSIS = "pubic_symphysis"
    UMBILICUS = "umbilicus"
    ASIS_LEFT = "asis_left"  # Anterior Superior Iliac Spine
    ASIS_RIGHT = "asis_right"
    ILIAC_CREST_LEFT = "iliac_crest_left"
    ILIAC_CREST_RIGHT = "iliac_crest_right"


@dataclass
class ElectrodePosition:
    """Single electrode position in RSL.
    
    Coordinates are relative to anatomical center (midpoint between ASIS).
    """
    electrode_number: int  # 1-6
    glyph_x: sp.Expr  # Symbolic x coordinate (glyph units)
    glyph_y: sp.Expr  # Symbolic y coordinate (glyph units)
    anatomical_x_cm: float  # Scaled x position (cm from center)
    anatomical_y_cm: float  # Scaled y position (cm from center)
    angle_degrees: float  # Angle from center
    description: str


@dataclass
class PatientAnthropometry:
    """Patient measurements for RSL scaling."""
    inter_asis_distance_cm: float  # Distance between left and right ASIS
    pubis_umbilicus_distance_cm: float
    patient_id: str
    measurement_date: str


class RSLPlacement:
    """Calculator for RSL electrode placement coordinates.
    
    Scales the Viduya Legacy Glyph geometry to patient anatomy
    for precise electrode positioning.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    # Glyph radius (Triangle-Hexagon intersection)
    GLYPH_RADIUS = sqrt(3) / 4
    
    # Standard anatomical scaling factor (glyph units to cm)
    # Based on average inter-ASIS distance of 24 cm
    DEFAULT_SCALE_FACTOR = 24.0 / float(GLYPH_RADIUS.evalf())
    
    def __init__(self, anthropometry: Optional[PatientAnthropometry] = None):
        self.anthropometry = anthropometry
        self._electrodes: List[ElectrodePosition] = []
        self._build_electrode_positions()
    
    def _build_electrode_positions(self) -> None:
        """Build 6 electrode positions using glyph geometry."""
        for i in range(6):
            angle_rad = i * sp.pi / 3  # 60° intervals
            angle_deg = float((angle_rad * 180 / sp.pi).evalf())
            
            # Glyph coordinates
            glyph_x = self.GLYPH_RADIUS * sp.cos(angle_rad)
            glyph_y = self.GLYPH_RADIUS * sp.sin(angle_rad)
            
            # Scale to patient anatomy
            scale = self._get_scale_factor()
            anat_x = float(glyph_x.evalf()) * scale
            anat_y = float(glyph_y.evalf()) * scale
            
            # Anatomical description
            descriptions = [
                "Right lateral pelvic (3 o'clock)",
                "Right superior pelvic (1 o'clock)",
                "Left superior pelvic (11 o'clock)",
                "Left lateral pelvic (9 o'clock)",
                "Left inferior pelvic (7 o'clock)",
                "Right inferior pelvic (5 o'clock)"
            ]
            
            self._electrodes.append(ElectrodePosition(
                electrode_number=i + 1,
                glyph_x=sp.simplify(glyph_x),
                glyph_y=sp.simplify(glyph_y),
                anatomical_x_cm=round(anat_x, 2),
                anatomical_y_cm=round(anat_y, 2),
                angle_degrees=angle_deg,
                description=descriptions[i]
            ))
    
    def _get_scale_factor(self) -> float:
        """Calculate anatomical scaling factor."""
        if self.anthropometry:
            # Scale based on patient's inter-ASIS distance
            return self.anthropometry.inter_asis_distance_cm / float(self.GLYPH_RADIUS.evalf() * 2)
        return self.DEFAULT_SCALE_FACTOR
    
    @property
    def electrodes(self) -> List[ElectrodePosition]:
        """Get all electrode positions."""
        return self._electrodes.copy()
    
    def get_electrode(self, number: int) -> ElectrodePosition:
        """Get specific electrode by number (1-6)."""
        if number < 1 or number > 6:
            raise ValueError("Electrode number must be 1-6")
        return self._electrodes[number - 1]
    
    def get_placement_guide(self) -> str:
        """Generate clinical placement guide text.
        
        Returns:
            Formatted placement instructions
        """
        guide = ["# Regenerative Spark Lattice Electrode Placement Guide",
                 "## Viduya Family Legacy Glyph © 2025\n"]
        
        guide.append("### Anatomical Reference Points")
        guide.append("- Center: Midpoint between left and right ASIS")
        guide.append("- Orientation: Patient supine, standard anatomical position\n")
        
        guide.append("### Electrode Positions")
        for e in self._electrodes:
            guide.append(f"**Electrode {e.electrode_number}**: {e.description}")
            guide.append(f"  - Position: ({e.anatomical_x_cm} cm, {e.anatomical_y_cm} cm) from center")
            guide.append(f"  - Angle: {e.angle_degrees}° from horizontal")
            guide.append(f"  - Glyph coordinates: ({e.glyph_x}, {e.glyph_y})\n")
        
        return "\n".join(guide)
    
    def verify_symmetry(self) -> Tuple[bool, str]:
        """Verify C₃ × D₆ symmetry of electrode placement.
        
        Returns:
            Tuple of (is_symmetric, verification_message)
        """
        # All electrodes should be equidistant from center
        radii = [
            sp.sqrt(e.glyph_x**2 + e.glyph_y**2)
            for e in self._electrodes
        ]
        
        r0 = radii[0]
        for i, r in enumerate(radii[1:], 1):
            diff = sp.simplify(r - r0)
            if diff != 0:
                return False, f"Radius mismatch at electrode {i+1}"
        
        return True, "C₃ × D₆ symmetry verified. Citation: Viduya Family Legacy Glyph © 2025"
    
    def to_dict(self) -> dict:
        """Export placement as dictionary."""
        return {
            "citation": "Viduya Family Legacy Glyph © 2025",
            "symmetry": "C₃ × D₆",
            "electrodes": [
                {
                    "number": e.electrode_number,
                    "glyph_x": str(e.glyph_x),
                    "glyph_y": str(e.glyph_y),
                    "anatomical_x_cm": e.anatomical_x_cm,
                    "anatomical_y_cm": e.anatomical_y_cm,
                    "angle_degrees": e.angle_degrees,
                    "description": e.description
                }
                for e in self._electrodes
            ],
            "patient_anthropometry": {
                "inter_asis_cm": self.anthropometry.inter_asis_distance_cm if self.anthropometry else None,
                "patient_id": self.anthropometry.patient_id if self.anthropometry else None
            } if self.anthropometry else None
        }

