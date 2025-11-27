# ENDOCHAIN Hardware: OpenBCI EVG Driver
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
OpenBCI Cyton board driver for 6-channel EVG acquisition.

Specifications:
- 6 channels using ADS1299 24-bit ADC
- Sample rate: 250 Hz (configurable)
- Bandpass: 0.01 - 1 Hz for pelvic autonomic signals
- Real-time streaming with V-CAW window tracking

Reference: OpenBCI Cyton with ADS1299 biosignal acquisition
"""

import asyncio
import struct
from typing import Optional, List, Callable, AsyncIterator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("endochain.hardware")


class ChannelGain(Enum):
    """ADS1299 gain settings."""
    GAIN_1 = 1
    GAIN_2 = 2
    GAIN_4 = 4
    GAIN_6 = 6
    GAIN_8 = 8
    GAIN_12 = 12
    GAIN_24 = 24


@dataclass
class EVGChannel:
    """Single EVG channel data."""
    channel_index: int  # 1-6 (RSL electrode)
    value_uv: float  # Microvolt reading
    impedance_ohms: Optional[float]
    timestamp: datetime
    sample_number: int


@dataclass
class EVGSample:
    """Complete 6-channel EVG sample."""
    channels: List[EVGChannel]
    timestamp: datetime
    sample_number: int
    v_caw_hour: Optional[int]
    cycle_day: Optional[int]
    audit_hash: Optional[str] = None


@dataclass 
class EVGConfig:
    """EVG acquisition configuration."""
    sample_rate_hz: int = 250
    bandpass_low_hz: float = 0.01
    bandpass_high_hz: float = 1.0
    gain: ChannelGain = ChannelGain.GAIN_24
    reference_electrode: str = "common"
    v_caw_duration_hours: int = 96
    auto_impedance_check: bool = True


class OpenBCIEVG:
    """OpenBCI Cyton driver for EVG acquisition.
    
    Implements the Regenerative Spark Lattice 6-channel recording
    protocol for pelvic electroviscerography.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    CYTON_CHANNELS = 8  # Cyton has 8 channels, we use 6 for RSL
    RSL_CHANNELS = 6
    
    # OpenBCI Cyton commands
    CMD_STREAM_START = b'b'
    CMD_STREAM_STOP = b's'
    CMD_SOFT_RESET = b'v'
    CMD_CHANNEL_OFF = b'1234567890qwer'
    CMD_CHANNEL_ON = b'!@#$%^&*()QWER'
    
    def __init__(
        self,
        serial_port: str = "/dev/ttyUSB0",
        baud_rate: int = 115200,
        config: Optional[EVGConfig] = None
    ):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.config = config or EVGConfig()
        self._serial = None
        self._streaming = False
        self._sample_count = 0
        self._callbacks: List[Callable[[EVGSample], None]] = []
    
    async def connect(self) -> bool:
        """Connect to OpenBCI Cyton board.
        
        Returns:
            True if connection successful
        """
        try:
            import serial_asyncio
            
            reader, writer = await serial_asyncio.open_serial_connection(
                url=self.serial_port,
                baudrate=self.baud_rate
            )
            self._serial = (reader, writer)
            
            # Soft reset
            await self._send_command(self.CMD_SOFT_RESET)
            await asyncio.sleep(2)  # Wait for reset
            
            # Configure channels (enable 6, disable 7-8)
            await self._configure_channels()
            
            logger.info(f"Connected to OpenBCI Cyton at {self.serial_port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to OpenBCI: {e}")
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from OpenBCI board."""
        if self._streaming:
            await self.stop_streaming()
        
        if self._serial:
            self._serial[1].close()
            self._serial = None
    
    async def start_streaming(self) -> None:
        """Start EVG data streaming."""
        if not self._serial:
            raise RuntimeError("Not connected to OpenBCI")
        
        await self._send_command(self.CMD_STREAM_START)
        self._streaming = True
        logger.info("EVG streaming started (V-CAW protocol)")
    
    async def stop_streaming(self) -> None:
        """Stop EVG data streaming."""
        if self._serial:
            await self._send_command(self.CMD_STREAM_STOP)
        self._streaming = False
        logger.info("EVG streaming stopped")
    
    async def read_samples(self) -> AsyncIterator[EVGSample]:
        """Async generator yielding EVG samples.
        
        Yields:
            Complete 6-channel EVG samples
        """
        if not self._serial:
            raise RuntimeError("Not connected to OpenBCI")
        
        reader, _ = self._serial
        
        while self._streaming:
            try:
                # OpenBCI packet: 33 bytes (1 header + 24 data + 6 aux + 2 footer)
                packet = await reader.read(33)
                if len(packet) == 33:
                    sample = self._parse_packet(packet)
                    if sample:
                        yield sample
            except asyncio.CancelledError:
                break
    
    def _parse_packet(self, packet: bytes) -> Optional[EVGSample]:
        """Parse OpenBCI packet into EVG sample."""
        if packet[0] != 0xA0:  # Sync byte
            return None
        
        self._sample_count += 1
        timestamp = datetime.utcnow()
        channels = []
        
        # Parse 6 RSL channels (24-bit values, 3 bytes each)
        for i in range(self.RSL_CHANNELS):
            offset = 2 + (i * 3)  # Skip sync byte and sample number
            raw = struct.unpack('>i', b'\x00' + packet[offset:offset+3])[0]
            # Convert to microvolts (ADS1299 scaling)
            uv = (raw * 4.5) / (self.config.gain.value * 2**23) * 1e6
            
            channels.append(EVGChannel(
                channel_index=i + 1,
                value_uv=uv,
                impedance_ohms=None,  # Measured separately
                timestamp=timestamp,
                sample_number=self._sample_count
            ))
        
        return EVGSample(
            channels=channels,
            timestamp=timestamp,
            sample_number=self._sample_count,
            v_caw_hour=None,  # Set by V-CAW tracker
            cycle_day=None    # Set by cycle tracker
        )
    
    async def _send_command(self, cmd: bytes) -> None:
        """Send command to OpenBCI board."""
        if self._serial:
            _, writer = self._serial
            writer.write(cmd)
            await writer.drain()
    
    async def _configure_channels(self) -> None:
        """Configure channel settings for RSL."""
        # Enable channels 1-6, disable 7-8
        for i in range(8):
            if i < 6:
                await self._send_command(bytes([ord(self.CMD_CHANNEL_ON[i])]))
            else:
                await self._send_command(bytes([ord(self.CMD_CHANNEL_OFF[i])]))
            await asyncio.sleep(0.1)

