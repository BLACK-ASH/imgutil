"""imgutil: Multi-utility image processing tool."""

import sys
import types

# Patch for basicsr compatibility with torchvision >=0.17
# basicsr imports torchvision.transforms.functional_tensor which was removed
if "torchvision.transforms.functional_tensor" not in sys.modules:
    try:
        import torchvision.transforms.functional_tensor  # noqa: F401
    except ImportError:
        import torchvision.transforms.functional as _f
        _ft = types.ModuleType("torchvision.transforms.functional_tensor")
        _ft.rgb_to_grayscale = _f.rgb_to_grayscale
        sys.modules["torchvision.transforms.functional_tensor"] = _ft

__version__ = "0.2.0"
