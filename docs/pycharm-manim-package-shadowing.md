# PyCharm Package Shadowing Foot Gun

## Problem Description

When working with [Manim Community Edition (CE)](https://www.manim.community/) in PyCharm, I encountered an issue related to package shadowing. 
Specifically, I created a local package named `manim` to organize my Manim example scripts:

```
project_root/
    manim/
        example_scene.py
    main.py
```

In PyCharm, this caused problems with the IDE's ability to locate the official `manim` package installed in my Python 
virtual environment. As a result:
- **PyCharm failed to resolve imports** from the real Manim package (e.g., `from manim import Scene`), 
- instead referencing the local directory.
- The IDE reported unresolved references and autocompletion didn’t work.
- Running the code from the terminal (or outside the IDE) worked fine, because Python’s import system correctly 
- prioritized the installed package in the venv over the local directory.

Let me stress that this problem was entirely self-inflicted and easily avoided by giving all local packages names
that are different from installed Python packages.
However, it does point out a behavioral difference in how the Python interpreter locates packages versus how
PyCharm locates them.

## Steps to Reproduce

1. Create a directory named `manim` inside your project.
2. Place example scripts inside this directory.
3. Attempt to import from `manim` in your code (e.g., `from manim import Scene`).
4. Observe that PyCharm reports unresolved imports, but running the code directly from the Terminal works.

## Root Cause

PyCharm’s import resolution can be confused when a local directory shares the same name as an installed package. 
The IDE may prioritize the local directory, shadowing the real package in the venv, 
even though the runtime behavior is correct.

## Solution / Workaround

- **Rename the local directory** to something other than `manim` (e.g., `manim_examples` or `my_manim_scenes`).
- Avoid naming local packages or directories after installed third-party packages to prevent shadowing.

## References

- https://youtrack.jetbrains.com/issue/PY-82615/Unresolved-imports-when-project-contains-a-package-which-name-clashes-with-an-installed-library

## Additional Notes

This issue is not unique to Manim; it can occur with any package if a local directory or module shares its name. 
Always check your project structure to avoid such naming conflicts.
