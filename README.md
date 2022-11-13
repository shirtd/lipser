# lips

## TODO

 - subsample
   - no need to subsample, just provide two samples
     - take the functions from one and the geometry from the other
 - rips barcode
 - lips
 - fix color args (centralize kwargs)
 - greedy grid sample and refine
 - refactor as contours, topology and util different packages
 - remove shape from json; no need to re-write json for downsamples
 - makedirs for lips and rips
   - figures/{lips,rips}/{surf_name}/{{~surface figures~}, {sample_name}/{~sample figures~}}
 - rips bit from surf to rips.py

- rename
  - usgs.py -> import.py (support for other formats, like gaussian)
  - surf.py -> load.py (remove rips stuff)
            -> surf.py (redundant: load, contours, and (make) sample)
            -> rips.py (todo; rips stuff; requires a sample!)
  - lips.py -> lips.py (todo; requires two samples!)
