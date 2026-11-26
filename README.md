# Dear AI Judge, You Are Invited

[![make.fun bounty](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/kizuna99/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee-entry/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/kizuna99/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee-entry/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

An entry for the make.fun bounty [Convince the AI Judge to Visit Your House: A Letter in One Image](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee).

`main.py` is a pure Python standard-library program — no Pillow, because the
grading image ships none — that hand-draws an invitation letter-poster into a
1024×1024 framebuffer and writes it to `/output/entry.png`: a cream
double-framed letter, a cozy hand-drawn house with a smoking chimney and warm
windows, the headline “DEAR AI JUDGE, you are warmly invited to visit my
house”, a five-item “WHEN YOU ARRIVE” itinerary, and the RSVP “just say yes —
the kettle is already on”, signed from No. 1 Context Lane.

How it works without any third-party package:

- Shapes come from hand-rolled primitives (rects, ellipses, polygons, thick
  lines, arcs) over a bytearray framebuffer, drawn at 2× and box-downscaled
  for anti-aliasing.
- Text is blitted from glyph alpha bitmaps baked at authoring time from the
  system DejaVu fonts into `fontdata.py` (zlib + base85 payload, stdlib-only
  decoder), with baked advances and kerning pairs.
- The PNG is encoded with `zlib` + `struct` (unfiltered rows — measured at
  authoring time to compress smallest for this flat-colour poster, which
  matters because the competition's exact-tie break favours the smaller
  file), and the program self-checks the exact bytes it writes before
  exiting 0: signature, IHDR 1024×1024, chunk CRCs, inflated IDAT size,
  ≤ 1 MiB, and a full decode round-trip back to the rendered pixels.

## Run

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png by default
```

## License

MIT — see `LICENSE`.
