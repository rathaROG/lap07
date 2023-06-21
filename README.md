# Linear Assignment Problem Solver

lap07 (v0.5.1) is a customized version of Tomas Kazmar's lap05.

## 📥 Installation
---

### On Windows

* Clone and build:

  ```
  git clone https://github.com/rathaROG/lap07.git
  cd lap07
  create_whl.cmd
  cd dist
  rem pip install your lap07-0.5.1-cp3xx-cp3xx-win_amd64.whl
  ```
* Test passed on Windows 11, Python 3.10 + Cython 0.29.35 ✅

### On Linux

* Clone and build:

  ```
  git clone https://github.com/rathaROG/lap07.git
  cd lap07
  pip install wheel build
  python -m build --wheel --skip-dependency-check --no-isolation
  cd dist
  pip install *.whl
  ```
* Test passed on GitHub `ubuntu-latest`, Ubuntu 22.04, Python 3.11 + Cython 0.29.35 ✅

<br />

<details><summary><ins>Click here to show more ...</ins></summary>

<br />

lap: Linear Assignment Problem solver
=====================================

**lap** is a [linear assignment
problem](https://en.wikipedia.org/wiki/Assignment_problem) solver using
Jonker-Volgenant algorithm for dense (LAPJV [1]) or sparse (LAPMOD [2])
matrices.

Both algorithms are implemented from scratch based solely on the papers [1,2]
and the public domain Pascal implementation provided by A. Volgenant [3].

In my tests the LAPMOD implementation seems to be faster than the LAPJV
implementation for matrices with a side of more than ~5000 and with less than
50% finite coefficients.

[1] R. Jonker and A. Volgenant, "A Shortest Augmenting Path Algorithm for Dense
and Sparse Linear Assignment Problems", Computing 38, 325-340 (1987)<br>
[2] A. Volgenant, "Linear and Semi-Assignment Problems: A Core Oriented
Approach", Computer Ops Res. 23, 917-932 (1996)<br>
[3] http://www.assignmentproblems.com/LAPJV.htm


### Usage

```
cost, x, y = lap.lapjv(C)
```

The function `lapjv(C)` returns the assignment cost (`cost`) and two arrays, `x, y`. If cost matrix `C` has shape N x M, then `x` is a size-N array specifying to which column is row is assigned, and `y` is a size-M array specifying to which row each column is assigned. For example, an output of `x = [1, 0]` indicates that row 0 is assigned to column 1 and row 1 is assigned to column 0. Similarly, an output of `x = [2, 1, 0]` indicates that row 0 is assigned to column 2, row 1 is assigned to column 1, and row 2 is assigned to column 0.

Note that this function *does not* return the assignment matrix (as done by scipy's [`linear_sum_assignment`](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html) and lapsolver's [`solve dense`](https://github.com/cheind/py-lapsolver)). The assignment matrix can be constructed from `x` as follows:
```
A = np.zeros((N, M))
for i in range(N):
    A[i, x[i]] = 1
```
Equivalently, we could construct the assignment matrix from `y`:
```
A = np.zeros((N, M))
for j in range(M):
    A[y[j], j] = 1
```

Finally, note that the outputs are redundant: we can construct `x` from `y`, and vise versa:
```
x = [np.where(y == i)[0][0] for i in range(N)]
y = [np.where(x == j)[0][0] for j in range(M)]
```

</details>

<br />

License
-------

Released under the 2-clause BSD license, see `LICENSE`.

Copyright (C) 2012-2017, Tomas Kazmar