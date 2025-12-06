# MayaPlanarComponents

Planar Components script for Autodesk Maya

Original script from this video:  
https://www.youtube.com/watch?v=ieN5SyGJwIw&t=26s

https://github.com/user-attachments/assets/9eccd5e2-e92d-486c-81fd-4e1622f6e0cd

---

## Script Versions

- **`PlanarComponents.py`** - Original version (1.0): Aligns all selected vertices to best-fit plane
- **`PlanarComponentsAutoSnapToAxis.py`** - Enhanced version (1.2):
  - Auto-snaps plane normal to world axes (X/Y/Z) when within 0.1° threshold
  - Only moves vertices that are OFF the plane (selective displacement)
  - Detects existing coplanar vertices and preserves them
  - Shows in-viewport notification at top with moved vertex count and plane orientation
  - Preserves original selection mode after operation

---

## Usage

After installing NumPy, run the main script from the Maya Script Editor.

---

## Requirements

The script requires the **NumPy** library.

---

## ✅ Recommended installation method (Python-based)

Use the `check_and_install_numpy.py` script to automatically install NumPy from within Maya:

1. Open Maya.
2. Open the **Script Editor**.
3. Copy and run the contents of [`check_and_install_numpy.py`](check_and_install_numpy.py).
4. The script will check if NumPy is installed, and install it automatically using `mayapy.exe` if needed.

https://github.com/user-attachments/assets/359df3eb-54d6-4e08-b37c-63f29d075fbb

This is the easiest and most portable method.

---

## 🛠️ Alternative method (manual via `.cmd`)

1. Copy the file `maya_install_numpy.cmd` to the directory where Maya is installed.  
   Example:  
   `C:\Program Files\Autodesk\Maya2023\bin`

2. Run `maya_install_numpy.cmd`.

https://github.com/user-attachments/assets/172ef66c-ab6e-47de-8778-17919d2046e4

---
