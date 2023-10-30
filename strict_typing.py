from typing import Callable
import warnings

warnings.formatwarning = lambda msg, *args, **kwargs: str(msg) + '\n'

# TODO: Add support for parameterized generics

def typed(warn=False):
	"""
	Strict typing decorator. Type hints are used to define expected types. Types are evaluated at runtime.
	Function arguments will be attempted to be cast to a valid input type; if this is not possible a ValueError is raised.
	If the return type of the function is found to be incorrect it will similarly be attempted to be cast, or a ValueError will be raised.
	Optionally, warnings can be raised on implicit casts by setting the warn flag.
	"""
	def decorator(func: Callable, *args):
		def wrapper(*args):
			# New arguments after casting
			newArgs = []

			# Handle arguments
			for i in range(len(args)):
				# Get arg and argName
				arg, argName = args[i], func.__code__.co_varnames[i]
				if (not (expected := func.__annotations__.get(argName)) == None) and (not isinstance(arg, expected)):		# If types do not match
					actual = type(arg)
					actualName = actual.__name__ if hasattr(actual, "__name__") else actual
					expectedName = expected.__name__ if hasattr(expected, "__name__") else expected
					error = True
					# Cast
					try:
						arg = expected(arg)
						if warn:
							warnings.warn(f"WARNING in function '{func.__name__}': Implicit cast of argument '{argName}' of typed function '{func.__name__}', from type '{actualName}' to expected type '{expectedName}'.", RuntimeWarning)
						error = False
					# Raise error
					except (ValueError, TypeError):
						pass
					if error:
						raise TypeError(f"ERROR in function '{func.__name__}': Argument '{argName}' of typed function '{func.__name__}' is type '{actualName}' when type '{expectedName}' is expected.")
				# Add new argument to newArgs
				newArgs.append(arg)

			# Execute decorated function
			out = func(*newArgs)

			# Handle return type
			if (not (expected := func.__annotations__.get("return")) == None) and (not isinstance(out, expected)):		# If types do not match
				actual = type(out)
				actualName = actual.__name__ if hasattr(actual, "__name__") else actual
				expectedName = expected.__name__ if hasattr(expected, "__name__") else expected
				error = True
				# Cast
				try:
					out = expected(out)
					if warn:
						warnings.warn(f"WARNING in function '{func.__name__}': Implicit cast of return value of typed function '{func.__name__}', from type '{actualName}' to expected type '{expectedName}'.", RuntimeWarning)
					error = False
				# Raise error
				except (ValueError, TypeError):
					pass
				if error:
					raise TypeError(f"ERROR in function '{func.__name__}': Typed function '{func.__name__}' returns type '{actualName}' when type '{expectedName}' is expected.")
			
			return out
		return wrapper
	return decorator