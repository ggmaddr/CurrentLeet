# Python Virtual Environments Guide

## What is a Virtual Environment?

A **virtual environment** is an isolated Python environment that allows you to:
- Install packages specific to a project without affecting your system Python
- Keep different projects with different package versions separate
- Avoid conflicts between projects
- Make your project reproducible

Think of it like a separate "workspace" for each project!

## Why Use Virtual Environments?

### Without Virtual Environments:
```
System Python
├── Project A needs Django 3.0
├── Project B needs Django 4.0  ❌ CONFLICT!
└── Project C needs Flask 2.0
```
All projects share the same packages → conflicts!

### With Virtual Environments:
```
venv_A/          venv_B/          venv_C/
├── Django 3.0   ├── Django 4.0   ├── Flask 2.0
└── ...          └── ...          └── ...
```
Each project has its own isolated environment → no conflicts! ✅

## What We Just Did

1. **Created a virtual environment** (`venv/` folder)
   ```bash
   python3 -m venv venv
   ```
   This creates a new folder with its own Python interpreter and package space.

2. **Activated the virtual environment**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```
   When activated, your terminal prompt shows `(venv)` to remind you.

3. **Installed BeautifulSoup**
   ```bash
   pip install beautifulsoup4
   ```
   This installed it ONLY in this virtual environment, not system-wide.

4. **Saved dependencies to requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```
   This creates a list of all installed packages with versions.

## Common Commands

### Activating the Virtual Environment
```bash
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# After activation, you'll see (venv) in your prompt:
(venv) $ python --version
```

### Deactivating
```bash
deactivate
```

### Installing Packages
```bash
# Activate first, then:
pip install package_name

# Install from requirements.txt:
pip install -r requirements.txt
```

### Updating requirements.txt
```bash
pip freeze > requirements.txt
```

### Checking Installed Packages
```bash
pip list
```

## Project Structure

Your CurrentLeet project now looks like:
```
CurrentLeet/
├── venv/                    # Virtual environment (don't commit this!)
│   ├── bin/                 # Executables (Python, pip, etc.)
│   ├── lib/                 # Installed packages
│   └── pyvenv.cfg           # Config file
├── requirements.txt         # List of dependencies (DO commit this!)
├── webTextExtract.py        # Your code
└── ...
```

## Best Practices

1. **Always activate before working**
   ```bash
   source venv/bin/activate
   ```

2. **Don't commit `venv/` folder**
   - Add `venv/` to `.gitignore`
   - DO commit `requirements.txt`

3. **Keep requirements.txt updated**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Share your project**
   - Share `requirements.txt`, not `venv/`
   - Others can recreate the environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

## Using in VS Code / Cursor

1. **Select the Python interpreter:**
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows)
   - Type "Python: Select Interpreter"
   - Choose `./venv/bin/python`

2. **Terminal will auto-activate:**
   - VS Code/Cursor detects `venv/` and activates it automatically

## Troubleshooting

### "Command not found: python"
- Make sure venv is activated: `source venv/bin/activate`

### "Module not found"
- Activate venv and install: `pip install module_name`

### Packages installed but not found
- Check you're using the venv Python interpreter
- Verify venv is activated: `which python` should show `venv/bin/python`

## Summary

✅ **Created**: `venv/` folder (isolated Python environment)
✅ **Installed**: beautifulsoup4 (only in this venv)
✅ **Saved**: requirements.txt (list of dependencies)

**Next time you work on this project:**
1. `cd /Users/gradyta/GResources/CurrentLeet`
2. `source venv/bin/activate`
3. Start coding! 🚀

