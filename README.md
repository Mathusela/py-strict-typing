# py-strict-typing

[Boilerplate] [Helper]

---

Strict type checking for python.

Enforces types at runtime, either implicitly casting (and optionally warning) or throwing an error on an unexpected type.

```py
# @typed(True) warns on implicit cast; @typed() does not
@typed(True)
def mult(x: float, y: float) -> int:
	return x * y

mult(2.0, 5.0)
"""
WARNING in function 'mult': Implicit cast of argument 'y' of typed function 'mult', from type 'int' to expected type 'float'.
WARNING in function 'mult': Implicit cast of return value of typed function 'mult', from type 'float' to expected type 'int'.

10
"""

mult("test", 5)
"""
ERROR in function 'mult': Argument 'x' of typed function 'mult' is type 'str' when type 'float' is expected.
"""

```