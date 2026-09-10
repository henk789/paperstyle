# Look guide

Paperstyle aims for a slightly tuned default Matplotlib look: familiar,
restrained, and ready for a paper. A reader should notice the result before the
styling.

- Keep Matplotlib's standard axis text colors and title placement.
- Use ordinary axes, ticks, labels, legends, and spines as the starting point.
- Let paperstyle provide publication dimensions, typography, line weights,
  export settings, and a dependable color cycle.
- Choose plot-specific encodings explicitly when they carry meaning, such as a
  threshold band or a training-reference distribution.
- Avoid custom title coordinates, colored labels, decorative frames, and other
  styling that does not clarify the science.

Matplotlib keyword arguments always override paperstyle, so a figure can depart
from these defaults when the data genuinely calls for it.
