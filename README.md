# app-lap-single-example
Will run LAP_single example

## compiling linear_assignment.so

We've built the linear_assignment.so with following commands

```
cython linear_assignment.pyx;
python setup_lapjv.py build_ext --inplace;
```

