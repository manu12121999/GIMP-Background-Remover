# GIMP-Background-Remover
A small gimp plugin to easily remove the background of an image with [LDF](https://arxiv.org/pdf/2008.11048.pdf).  [Github of LDF](https://github.com/weijun88/LDF). 

## Made for Gimp3.0. Works only on Windows

Fork from the Linux only version [GIMP-Background-Remover ](https://github.com/manu12121999/GIMP-Background-Remover).

## Why Windows Needs a Separate Python Setup
GIMP 3.0 on Windows bundles an MSYS2/MinGW build of Python, which cannot download or install standard pre-compiled PyPI wheels (`numpy`, `opencv-python`, `torch`). To work around this, the plugin creates a local virtual environment (`gimpenv`) using a standard Windows Python 3.12 installation and runs model inference through that environment.

---

## Prerequisites
1. **GIMP 3.0** (or newer) installed on Windows 10 or Windows 11.
2. **Python 3.12 for Windows (64-bit)**:
   * Download from [python.org](https://python.org).
   * During installation, check **"Add python.exe to PATH"**.
---

## Installation Steps

### Step 1: Copy Plugin Files to GIMP
1. Press **Win + R**, type `%APPDATA%\GIMP\3.0\plug-ins`, and press **Enter**.
2. Copy the `background-remover` folder into this `plug-ins` directory.
3. Verify the folder structure looks like this:
   ```text
   %APPDATA%\GIMP\3.0\plug-ins\background-remover\
   ├── background-remover.py
   ├── README.md
   ├── run_ldf.py
   └── Ldf\
       ├── dataset.py
       ├── net.py
       ├── README.md
       └── test.py
   ```

### Step 2: Run the Built-In Installer inside GIMP
1. Open **GIMP 3.0**.
2. In the top menu bar, go to **Filters** > **Remove_BG** > **[INSTALL] Offline Background Remover**.
3. Click **OK** on the dialog prompt.
4. Wait for the background installation to finish (it will create `gimpenv`, install `numpy`, `pillow`, `opencv-python`, and CPU `torch`) and download [model-40](https://huggingface.co/ManuelVogel12/LDF_weights/blob/main/model-40).
5. Verify the folder structure looks like this:
   ```text
   %APPDATA%\GIMP\3.0\plug-ins\background-remover\
   ├── gimpenv\
       ├── Include\
       ├── Lib\
       ├── Scripts\
       ├── share\
       └── pyvenv.cfg
   └── Ldf\
       ├── dataset.py
       ├── model-40
       ├── net.py
       ├── README.md
       └── test.py
   ├── background-remover.py
   ├── README.md
   └── run_ldf.py
   ```
6. You may need to restart **GIMP 3.0** once the dialog disappears

---

## Usage
1. Open an image in **GIMP 3.0** and select the layer you want to cut out.
2. Go to **Filters** > **Remove_BG** > **Offline Background Remover**.
3. The plugin will process the image offline and apply the cutout as a **Layer Mask** on your active layer.

![Image](https://github.com/user-attachments/assets/843f3074-f595-4fc0-b209-c5f0b486745c)

## Notes:
- The results might be slightly worse than with my removebg plugin, but it works offline and the libraries are open source.
