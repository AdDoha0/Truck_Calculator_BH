"""
UI adapters - bridge between UI layer and application layer.

These adapters handle the translation between UI frameworks
(like Streamlit) and the application use cases.
"""

from .streamlit_adapter import StreamlitAdapter

__all__ = [
    "StreamlitAdapter",
]
