import ctypes
import os
import tempfile

# Create pipe BEFORE loading library
r, w = os.pipe()

# Redirect stdout to the pipe
saved = os.dup(1)
os.dup2(w, 1)

# NOW load the library
lib = ctypes.CDLL("./mylib.so", mode=ctypes.RTLD_GLOBAL)

# Call printf func
lib.my_printf_function()

# Flush
ctypes.CDLL(None).fflush(None)

# Restore stdout
os.dup2(saved, 1)

# Read pipe
os.close(w)
out = os.read(r, 4096).decode()

print("Captured:", repr(out))
