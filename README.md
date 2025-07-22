# MayaPlanarComponents

Planar Components script for Autodesk Maya

Original script from this video:  
https://www.youtube.com/watch?v=ieN5SyGJwIw&t=26s

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

This is the easiest and most portable method.

---

## 🛠️ Alternative method (manual via `.cmd`)

1. Copy the file `maya_install_numpy.cmd` to the directory where Maya is installed.  
   Example:  
   `C:\Program Files\Autodesk\Maya2023\bin`

2. Run `maya_install_numpy.cmd`.

---

## Usage

After installing NumPy, run the main script from the Maya Script Editor.

---

## Assets

- [Installation CMD screenshot](https://github.com/user-attachments/assets/172ef66c-ab6e-47de-8778-17919d2046e4)
- [Script usage screenshot](https://github.com/user-attachments/assets/9eccd5e2-e92d-486c-81fd-4e1622f6e0cd)
