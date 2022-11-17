# lips

## TODO

10000 is a bit much...

parser.py
 - abstract, supports surf.py
 - built in: gauss and usgs
surf.py <- parser.py
 - generate surface (implements parsers)
 - load/plot surface
 - plot surface contours
 - surface barcode
sample.py <- surf.py
 - default: show surface (and sample, if provided/generated)
 - sample surface
 - plot cover/union and contours
 - plot lips cover/union and contours
rips.py
 - no cover plots
 - always compute 2/sqrt(3) rips and filter
   - plot both
 - lips plot and contours
 - lips sub plot and contours
 - rips and lips (sub) barcodes

color flag saves an additional file; no recompute.

## TODO FUTURE

 - decentralize ploting to avoid unnecessary loads
  - no plt in main
 - implement --rips --union vs. --cover --union
 - just hide edges
 - no need to re-write json for downsamples
 - sample and keep going; no need to reload before rendering
 - refactor as contours, topology and util different packages
