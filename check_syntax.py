import os
import py_compile

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                py_compile.compile(filepath, doraise=True)
            except py_compile.PyCompileError as e:
                print(f"Error in {filepath}: {e}")
