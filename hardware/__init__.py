# ENDOCHAIN Hardware: OpenBCI EVG Acquisition
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Hardware integration for 6-channel Electroviscerography (EVG) acquisition
using OpenBCI Cyton board with ADS1299 drivers.

The Regenerative Spark Lattice electrode placement follows exact
Viduya Legacy Glyph geometry for optimal pelvic autonomic recording.

Reference: OpenBCI open-source biosignal acquisition framework
"""

from .openbci_evg import OpenBCIEVG, EVGChannel
from .rsl_placement import RSLPlacement, ElectrodePosition
from .signal_processor import EVGSignalProcessor

__all__ = [
    "OpenBCIEVG",
    "EVGChannel",
    "RSLPlacement",
    "ElectrodePosition",
    "EVGSignalProcessor"
]

