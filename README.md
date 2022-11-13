# lips

## TODO NOW

 - refactor sample and finish surf.py
 - fix color args (centralize kwargs)
 - remove shape from json; no need to re-write json for downsamples
 - makedirs for lips and rips
   - figures/surf/{surf_name}/{~surface figures~}
   - figures/{rips,lips}/{surf_name}/{sample_name}/{~sample figures~}
 - rename
   - usgs.py -> import.py (support for other formats, like gaussian)
   - surf.py -> load.py (remove rips stuff)
             -> surf.py (redundant: load, contours, and (make) sample)
             -> rips.py (todo; rips stuff; requires a sample!)
   - lips.py -> lips.py (todo; requires two samples!)

## TODO FUTURE

 - sample and keep going; no need to reload before rendering
 - greedy grid sample and refine
 - lips and subsamples
 - rips and lips barcodes
 - rips bit from surf to rips.py
 - refactor as contours, topology and util different packages

## NOTES

  - no need to subsample, just provide two samples
    - take the functions from one and the geometry from the other
