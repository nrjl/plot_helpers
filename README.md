# Plot Helpers

Basic tools to help with a few plotting tasks.
Local install:
```
cd /path/to/plot_helpers
pip install --editable .
```

## Axes equal
Axis equal for 3D plots to have a fixed ratio.

```
import matplotlib.pyplot
from plot_helpers import axes_equal
```

## Covariance ellipses
A basic exmaple of a covariance ellipsoid and associated animation can be run with:
```
python3 examples/ellipsoid_plot_test.py
```

This should produce something like:
