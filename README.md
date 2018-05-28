# app-lap-single-example
This app performs automatic example-based tract segmentation using the Linear Assignemt Problem (LAP) algorithm with a single example. The user can specify up to four tracts of interest, otherwise all the tracts of the given segmentation are considered as input.

## compiling linear_assignment.so

We've built the linear_assignment.so with following commands

```
cython linear_assignment.pyx;
python setup_lapjv.py build_ext --inplace;
```

