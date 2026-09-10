# Look guide

Paperstyle aims for a slightly tuned default Matplotlib look: familiar,
restrained, and ready for a paper. A reader should notice the result before the
styling.

## Visual language

- Start with ordinary Matplotlib axes, ticks, labels, legends, and spines. Keep
  standard axis-text colors and default centered title placement.
- Avoid custom title coordinates, colored axis text, decorative frames, and
  other styling that does not clarify the science.
- Do not use a global title in a paper figure. The caption supplies the wider
  context; concise centered subplot titles identify local content when needed.
- Use whitespace when it improves grouping, hierarchy, or readability. Remove
  purposeless empty space by adjusting the canvas or layout, not by tightening
  the export bounds.

## Layout and alignment

- Build the layout on shared alignment lines. Align comparable axes edges,
  titles, labels, and subplot groups so the figure reads as one system.
- Keep peer panels the same height when they form columns and the same width
  when they form rows. Composite panels with different internal grids must
  still have aligned outer borders.
- Nothing may overlap: not labels, titles, legends, annotations, axes, or data.
  Treat overlap as a correctness defect, not a cosmetic compromise.
- Nothing may be clipped. Leave visible padding around the outermost artists
  and inspect the final exported artifact, not only the interactive canvas.
- Reserve layout space for shared legends. Keep a clear visual gap between axis
  labels and a legend below the panels; do not use the last few pixels of the
  canvas merely because the artists technically fit.

## Panel labels

- Use lowercase labels such as `a` and `b`, without parentheses, for major
  panels. A rounded, low-contrast backdrop distinguishes them without becoming
  decorative.
- All major labels must share one horizontal baseline. Align that baseline with
  the panel-title row and place each backdrop about 10 points before the panel's
  outer y-axis. The glyph must be optically centered in the backdrop.
- Use `paperstyle.panel_labels(fig, axes, labels)` for aligned major panels.
  Pass the top-left axes of each composite panel as the anchors. Use
  `paperstyle.panel_label` only for a single label or deliberately different
  placement.
- Keep labels fully inside the canvas and separate from titles and data. Never
  solve one collision by giving labels different y positions.

## Encodings

- Keep model order, color, and line style consistent across panels and related
  figures. Put the focal method first and label it explicitly as `(ours)` when
  applicable.
- Use the same structures, filtering, binning, and denominators across panels
  that claim a direct comparison. Label training, validation, and test
  references explicitly.
- Format proportions as percentages when readers interpret them as rates.
  Preserve meaningful endpoints such as 100% in the tick labels.
- Show uncertainty when it is part of the comparison, using intervals computed
  from the actual sample count represented by each point. Keep bounds secondary
  to the central estimate but clearly visible.
- A nonlinear scale may expose differences near a boundary, but tick labels
  must remain in the original positive units. Keep the transformation mild,
  show interpretable reference ticks, and disclose it in the caption or methods.
- Encode scientific thresholds directly when they aid interpretation, for
  example with a restrained shaded invalid region. Reference or training
  distributions should remain visually secondary to the compared methods.

## Size and export

- Match the canvas to the publication width and keep every artist inside it.
  ICLR full width is 5.5 inches. Choose height from the content; a golden-ratio
  default is only a starting point, especially for compact composite figures.
- Choose `tex=True` or `tex=False` explicitly in reproducible plotting scripts.
  The automatic fallback is convenient interactively but changes typography.
- Do not use `bbox_inches="tight"` for publication figures. It changes the file
  bounds and therefore the effective typography and line weights when LaTeX
  scales the result back to `\linewidth`.
- Export vector PDF and high-resolution PNG from the same plotting script.
  Avoid manual post-processing and separate plotting paths for compact and full
  variants; share data loading, encodings, and styling wherever possible.
- Use `paperstyle.savefig(fig, path)` for the standard PDF/PNG pair. It preserves
  the configured canvas and creates the output directory when needed.
- Inspect every final format at its intended paper size. Confirm that the canvas
  dimensions are unchanged and that no label, confidence band, or legend is
  clipped or uncomfortably close to another element.

## Per-figure checklist

Before considering a figure finished:

1. Set the target publication width and a content-appropriate height.
2. Establish the outer grid and equal panel dimensions before adding details.
3. Add centered local titles and aligned `a`, `b`, ... labels; omit a global
   title.
4. Apply one stable order and visual identity to methods everywhere, with the
   focal method first.
5. Use meaningful units, percentage formatting, correct uncertainty, and only
   scientifically justified thresholds or transformed scales.
6. Reserve explicit space for legends and outer labels.
7. Export PNG and PDF without a tight bounding box, then inspect both for
   overlap, clipping, alignment, and unnecessary whitespace.

Matplotlib keyword arguments always override paperstyle, so a figure can depart
from these defaults when the data genuinely calls for it.
