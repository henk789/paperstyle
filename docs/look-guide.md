# Look guide

Paperstyle aims for a slightly tuned default Matplotlib look: familiar,
restrained, and ready for a paper. A reader should notice the result before the
styling.

- Keep Matplotlib's standard axis text colors and title placement.
- Use ordinary axes, ticks, labels, legends, and spines as the starting point.
- Keep peer panels the same height when they form columns, and the same width
  when they form rows. For composite panels, align the outer panel regions even
  when their internal subplot grids differ.
- Use shared alignment lines throughout a figure: align comparable axes edges,
  titles, labels, and subplot groups so the layout reads as one system. Depart
  from the grid only when the scientific structure benefits from it.
- Nothing may overlap: not labels, titles, legends, annotations, axes, or data.
  Treat overlap as a figure correctness defect. Reserve enough room in the
  layout and inspect the final exported figure, including its bounding box.
- Use whitespace when it makes grouping, hierarchy, or the data easier to
  understand. Filling every part of the canvas is not a goal.
- Use lowercase panel labels such as `a` and `b` for multi-panel figures.
  Place them at the left edge in reserved whitespace with
  `paperstyle.panel_label`; its rounded, low-contrast backdrop keeps the label
  distinct without becoming decorative. Adjust its `x` and `y` position for
  composite layouts instead of allowing it to collide with a title or panel.
  Major panel labels in the same figure must share one horizontal baseline,
  and each label's left edge should align with its panel's outer left border.
  Reserve a common header strip instead of nudging labels to different heights.
- Center subplot titles when titles are useful. Let the panel label, rather than
  title alignment, identify the panel.
- Let paperstyle provide publication dimensions, typography, line weights,
  export settings, and a dependable color cycle.
- Choose plot-specific encodings explicitly when they carry meaning, such as a
  threshold band or a training-reference distribution.
- Avoid custom title coordinates, colored labels, decorative frames, and other
  styling that does not clarify the science.

Matplotlib keyword arguments always override paperstyle, so a figure can depart
from these defaults when the data genuinely calls for it.
