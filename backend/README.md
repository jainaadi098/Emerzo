# Emerzo backend

## Virtual Environment (venv) Usage

This project uses a Python **virtual environment** to manage dependencies.

---

### Setup

Create and activate `venv` in the project root:

* **Linux / macOS** (in **Emerzo/backend** path)

```
python3 -m venv venv
source venv/bin/activate
```

* **Windows (PowerShell)** (in **Emerzo/backend** path)

```
python -m venv venv
venv\\Scripts\\Activate.ps1
```

Install dependencies:

```
pip install -r requirements.txt
```

---

### Daily Use

Activate before running the project:

```
source venv/bin/activate   # or venv\\Scripts\\Activate.ps1
```

Deactivate when done:

```
deactivate
```

---

### Updating Dependencies

After installing new packages:

```
pip freeze > requirements.txt
```

---

### Notes

* `venv/` is **not committed** to git
* `requirements.txt` **is committed**
* If `venv` breaks, delete it and repeat setup

---

### TL;DR

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


