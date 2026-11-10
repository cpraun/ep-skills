# OCR caveats

Part of the `read-pdf` skill. Read this file when a page was extracted with `(ocr)`.

- OCR text may contain recognition errors (`rn`↔`m`, `l`↔`1`, `0`↔`O`, broken umlauts). When a quotation matters (claim features, numbers, dates, reference signs), re-check the words against the page image: `pdftoppm -r 150 -f N -l N -png FILE.pdf page` and view the PNG.
- Multi-column pages: the default page segmentation keeps column order in most cases. If text from two columns is interleaved, re-run with `--ocr` and inspect, or check the image.
- Tables and figures: the text layer gives cell text in reading order, not table structure. Describe table content from the image when structure matters.
- Rotated or skewed scans: tesseract handles small skews; for rotated pages, view the image and say so — do not guess.
- **Text layer present but unreadable** (wrong encoding, Type 3 fonts): re-run with `--ocr`.
