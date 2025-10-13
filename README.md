# GIMP-Background-Remover
A small gimp plugin to easily remove the background of an image with [LDF](https://arxiv.org/pdf/2008.11048.pdf).  [Github of LDF](https://github.com/weijun88/LDF). 

## Made for Gimp3.0. Works only on Linux

## Installation:

1. Put the background-remover folder in your Gimp Plugins directory.
  To find it, go inside GIMP to `Edit`->`Preferences`->`Folders`->`Plugins`. The folder must be named `background-remover`!!!

2. In GIMP, run "Filter -> Remove_BG -> [INSTALL] Offline Background Remover

If the second step does not work, run the fallback method instead:

<details><summary><b>Old (Fallback) Instructions</b></summary>



2. Install python

3. make the python file executable and install dependencies with: 

```
bash ./setup.sh
```

4. Download the weights and put both in the Ldf directory:

    [Trained model weights](https://drive.google.com/file/d/1qGQ6wSWTFqt8oy_YT3_aj-_pdlf5vKWL/view?usp=sharing)

 </details>

## Usage:
Open an image
- Filters -> RemoveBackground -> Offline Background Remover

![Image](https://github.com/user-attachments/assets/843f3074-f595-4fc0-b209-c5f0b486745c)

## Notes:
- The results might be slightly worse than with my removebg plugin, but it works offline and the libraries are open source.
