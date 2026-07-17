"""HPA Cell Segmentator Portable: a repackaging of HPA Cell Segmentator with
updated libraries and simplified usage."""

from pathlib import Path

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()