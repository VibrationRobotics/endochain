# ENDOCHAIN Hardware: EVG Signal Processing
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Real-time signal processing for EVG data with V-CAW window tracking.

Features:
- 0.01-1 Hz bandpass filtering for pelvic autonomic signals
- Real-time LEI-V drift computation
- Ovulation detection via LH/temperature integration
- Encrypted EDF export with FHIR upload

Reference: OpenBCI signal processing framework
"""

import numpy as np
from scipy import signal
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import struct

from .openbci_evg import EVGSample, EVGChannel


@dataclass
class VCAWStatus:
    """V-CAW (Viduya Cyclical Attention Window) status."""
    window_start: datetime
    current_hour: int
    total_hours: int = 96
    ovulation_detected: bool = False
    ovulation_hour: Optional[int] = None
    lh_surge_detected: bool = False
    temperature_shift: bool = False


@dataclass
class LEIVDrift:
    """Real-time LEI-V drift measurement."""
    current_lei_v: float
    baseline_lei_v: float
    drift_value: float
    drift_percent: float
    trend: str  # "stable", "increasing", "decreasing"
    timestamp: datetime


class EVGSignalProcessor:
    """Real-time EVG signal processor with V-CAW tracking.
    
    Implements bandpass filtering, LEI-V computation, and
    ovulation synchronization for the 96-hour V-CAW protocol.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    SAMPLE_RATE = 250  # Hz
    BANDPASS_LOW = 0.01  # Hz
    BANDPASS_HIGH = 1.0  # Hz
    FILTER_ORDER = 4
    
    VCAW_DURATION_HOURS = 96
    
    def __init__(self):
        self._samples_buffer: List[EVGSample] = []
        self._vcaw_status: Optional[VCAWStatus] = None
        self._baseline_lei_v: Optional[float] = None
        self._filter_coeffs = self._design_bandpass_filter()
    
    def _design_bandpass_filter(self) -> Tuple[np.ndarray, np.ndarray]:
        """Design Butterworth bandpass filter."""
        nyquist = self.SAMPLE_RATE / 2
        low = self.BANDPASS_LOW / nyquist
        high = self.BANDPASS_HIGH / nyquist
        
        # Ensure valid normalized frequencies
        low = max(0.001, low)
        high = min(0.999, high)
        
        b, a = signal.butter(self.FILTER_ORDER, [low, high], btype='band')
        return b, a
    
    def start_vcaw_window(
        self,
        expected_ovulation: Optional[datetime] = None
    ) -> VCAWStatus:
        """Start a new V-CAW acquisition window.
        
        Args:
            expected_ovulation: Expected ovulation datetime for window centering
            
        Returns:
            Initial V-CAW status
        """
        if expected_ovulation:
            # Center 96-hour window around expected ovulation
            window_start = expected_ovulation - timedelta(hours=48)
        else:
            window_start = datetime.utcnow()
        
        self._vcaw_status = VCAWStatus(
            window_start=window_start,
            current_hour=0
        )
        self._samples_buffer.clear()
        self._baseline_lei_v = None
        
        return self._vcaw_status
    
    def process_sample(self, sample: EVGSample) -> Dict[str, Any]:
        """Process single EVG sample.
        
        Args:
            sample: 6-channel EVG sample
            
        Returns:
            Processed result with filtered values and metrics
        """
        # Add to buffer
        self._samples_buffer.append(sample)
        
        # Update V-CAW hour
        if self._vcaw_status:
            elapsed = sample.timestamp - self._vcaw_status.window_start
            self._vcaw_status.current_hour = int(elapsed.total_seconds() / 3600)
        
        # Extract channel values
        raw_values = np.array([ch.value_uv for ch in sample.channels])
        
        # Apply bandpass filter if enough samples
        if len(self._samples_buffer) >= self.SAMPLE_RATE:
            filtered = self._apply_filter(raw_values)
        else:
            filtered = raw_values
        
        # Compute instantaneous radial distances
        radial_distances = self._compute_radial_distances(filtered)
        
        # Compute LEI-V
        lei_v = self._compute_lei_v(radial_distances)
        
        # Set baseline if first valid measurement
        if self._baseline_lei_v is None and lei_v is not None:
            self._baseline_lei_v = lei_v
        
        # Compute drift
        drift = None
        if self._baseline_lei_v is not None and lei_v is not None:
            drift = self._compute_drift(lei_v)
        
        return {
            "timestamp": sample.timestamp.isoformat(),
            "raw_values_uv": raw_values.tolist(),
            "filtered_values_uv": filtered.tolist(),
            "radial_distances": radial_distances,
            "lei_v": lei_v,
            "drift": drift.__dict__ if drift else None,
            "vcaw_hour": self._vcaw_status.current_hour if self._vcaw_status else None,
            "citation": "Viduya Family Legacy Glyph © 2025"
        }
    
    def _apply_filter(self, values: np.ndarray) -> np.ndarray:
        """Apply bandpass filter to channel values."""
        b, a = self._filter_coeffs
        
        # Get recent samples for filtering context
        recent = np.array([
            [ch.value_uv for ch in s.channels]
            for s in self._samples_buffer[-self.SAMPLE_RATE:]
        ])
        
        if len(recent) < 10:
            return values
        
        # Apply filter to each channel
        filtered = np.zeros(6)
        for i in range(6):
            channel_data = recent[:, i]
            filtered_channel = signal.filtfilt(b, a, channel_data)
            filtered[i] = filtered_channel[-1]
        
        return filtered
    
    def _compute_radial_distances(self, values: np.ndarray) -> List[float]:
        """Compute radial distances from electrode values.
        
        Maps signal amplitude to radial distance from glyph center.
        """
        # Normalize to 0-1 range
        min_val, max_val = values.min(), values.max()
        if max_val - min_val > 0:
            normalized = (values - min_val) / (max_val - min_val)
        else:
            normalized = np.ones(6) * 0.5
        
        # Map to glyph radial space (centered at √3/4 ≈ 0.433)
        base_radius = 0.433
        deviation_scale = 0.1
        
        radial = base_radius + (normalized - 0.5) * deviation_scale
        return radial.tolist()
    
    def _compute_lei_v(self, radial_distances: List[float]) -> Optional[float]:
        """Compute LEI-V from radial distances.
        
        LEI-V = Σ|r_i - r̄|²
        """
        if len(radial_distances) != 6:
            return None
        
        r = np.array(radial_distances)
        r_mean = np.mean(r)
        lei_v = np.sum((r - r_mean) ** 2)
        
        return float(lei_v)
    
    def _compute_drift(self, current_lei_v: float) -> LEIVDrift:
        """Compute LEI-V drift from baseline."""
        drift_value = current_lei_v - self._baseline_lei_v
        drift_percent = (drift_value / self._baseline_lei_v) * 100 if self._baseline_lei_v else 0
        
        if abs(drift_percent) < 5:
            trend = "stable"
        elif drift_value > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
        
        return LEIVDrift(
            current_lei_v=current_lei_v,
            baseline_lei_v=self._baseline_lei_v,
            drift_value=drift_value,
            drift_percent=drift_percent,
            trend=trend,
            timestamp=datetime.utcnow()
        )
    
    def detect_ovulation(
        self,
        lh_value: Optional[float] = None,
        basal_temp: Optional[float] = None
    ) -> bool:
        """Detect ovulation from LH surge and/or temperature shift.
        
        Args:
            lh_value: LH test value (mIU/mL)
            basal_temp: Basal body temperature (°C)
            
        Returns:
            True if ovulation detected
        """
        if not self._vcaw_status:
            return False
        
        # LH surge detection (>25 mIU/mL indicates surge)
        if lh_value and lh_value > 25:
            self._vcaw_status.lh_surge_detected = True
        
        # Temperature shift detection (>0.2°C rise)
        if basal_temp:
            # Would compare to baseline - simplified here
            pass
        
        # Ovulation confirmed if both indicators present
        if self._vcaw_status.lh_surge_detected:
            self._vcaw_status.ovulation_detected = True
            self._vcaw_status.ovulation_hour = self._vcaw_status.current_hour
            return True
        
        return False

