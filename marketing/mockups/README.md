# App Store / marketing mockups

Five cohesive, on-brand feature frames (Savings · FlowCast · Calm logging · Doctor-ready
report · Food story) at 1206×2622. **Representative-polished design mockups** — built from the
app's real UI code + design tokens and rendered in a browser, NOT captures of the live app.

- **Use for:** App Store gallery direction, pitch/press, the creator kit, and as a build-target
  spec for real captures.
- **Caveats:** they take small design liberties (e.g. a friendlier "Solids/Trends/Journey" tab
  bar vs the real Today·Analytics·Development·Family·Settings dock; a unified "Food story" screen).
  The App Store should also carry real captures matched to these.

## Regenerate / edit
Each `*.html` links `base.css` and renders standalone. To re-render (Chromium):

    chromium --headless=new --window-size=1206,2622 \
      --screenshot=out.png file://$PWD/savings.html

Edit the HTML (copy, numbers, colours in `base.css`) and re-render.
