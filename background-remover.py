#!/usr/bin/env python3
import os
import sys
import tempfile
import importlib


# This Plugin is only for GIMP Version >= 3.0.0 and Windows
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gegl
from gi.repository import Gio

baseLoc = os.path.dirname(os.path.realpath(__file__))+'/'
for version in range(6,20):
    sys.path.extend([baseLoc+f'gimpenv/lib/python3.{version}', baseLoc+f'gimpenv/lib/python3.{version}/site-packages', baseLoc+f'gimpenv/lib/python3.{version}/site-packages/setuptools'])
sys.path.extend([baseLoc+'gimpenv/Lib', baseLoc+'gimpenv/Lib/site-packages', baseLoc+'gimpenv/Lib/site-packages/setuptools'])


def find_windows_python312():
    import shutil
    import subprocess
    import winreg

    candidates = []
    registry_path = r"SOFTWARE\Python\PythonCore\3.12\InstallPath"
    registry_views = [
        winreg.KEY_READ,
        winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
        winreg.KEY_READ | winreg.KEY_WOW64_32KEY,
    ]
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for access in registry_views:
            try:
                with winreg.OpenKey(hive, registry_path, 0, access) as key:
                    try:
                        candidates.append(winreg.QueryValueEx(key, "ExecutablePath")[0])
                    except OSError:
                        candidates.append(os.path.join(winreg.QueryValue(key, None), "python.exe"))
            except OSError:
                pass

    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("ProgramFiles")
    candidates.extend([
        r"C:\Python312\python.exe",
        os.path.join(local_app_data, "Programs", "Python", "Python312", "python.exe") if local_app_data else "",
        os.path.join(program_files, "Python312", "python.exe") if program_files else "",
        shutil.which("python.exe") or "",
        shutil.which("python") or "",
    ])

    checked = set()
    for candidate in candidates:
        if not candidate or os.path.normcase(candidate) in checked or not os.path.isfile(candidate):
            continue
        checked.add(os.path.normcase(candidate))
        try:
            result = subprocess.run(
                [candidate, "-c", "import struct, sys; print(sys.version_info[0], sys.version_info[1], struct.calcsize('P') * 8)"],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            continue
        if result.returncode == 0 and result.stdout.strip() == "3 12 64":
            return candidate
    return None


class BackgroundRemover(Gimp.PlugIn):

    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        return [ 'python-plugin-offline-background-remover', 'python-plugin-offline-background-remover-installer' ]


    def do_create_procedure(self, name):
        procedure = None
        if name=='python-plugin-offline-background-remover':
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                self.remove_background, None)
            
            procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)

            procedure.set_documentation(
                "Easy way to remove any background from an image",
                "Easy way to remove any background from an image. Works Offline using the background-removal network LDF",  
                None)
            procedure.set_menu_label("Offline Background Remover")
            procedure.set_attribution("Manuel Vogel",
                                      "Manuel Vogel",
                                      "2021-2025")
            procedure.add_menu_path("<Image>/Filters/Remove_BG/")
        elif name=='python-plugin-offline-background-remover-installer':
            
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                self.install_remove_background, None)
            
            procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)

            procedure.set_documentation(
                "Easy way to remove any background from an image",
                "Easy way to remove any background from an image. Works Offline using the background-removal network LDF",  
                None)
            procedure.set_menu_label("[INSTALL] Offline Background Remover")
            procedure.set_attribution("Manuel Vogel",
                                      "Manuel Vogel",
                                      "2021-2025")
            procedure.add_menu_path("<Image>/Filters/Remove_BG/")
            procedure.add_boolean_argument("info", "This might take 5 minutes, please wait until this window closes", "info",
                                       True, GObject.ParamFlags.READWRITE)
            # procedure.add_double_argument("progress_bar", "Progress bar", "progress_bar", 0.0, 100.0, 0.0, GObject.ParamFlags.READWRITE)
        return procedure
    
    def install_remove_background(self, procedure, run_mode, image, drawables, config, data):
        import subprocess
        GimpUi.init("python-plugin-offline-background-remover")
            
        dialog = GimpUi.ProcedureDialog.new(procedure, config)
        dialog.fill(None)
        if not dialog.run():
            dialog.destroy()
            return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, GLib.Error())
        
        # config.set_property("progress_bar", 2.0)
        
        base_path = os.path.dirname(os.path.realpath(__file__))
        venv_dir = base_path +'/'+ "gimpenv"
        base_python = find_windows_python312()
        if not base_python:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error("Could not find 64-bit Python 3.12. Install it from python.org, then rerun the installer.")
            )
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        model_path = os.path.join(base_path, "Ldf", "model-40")
        powershell_exe = os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"),
            "System32", "WindowsPowerShell", "v1.0", "powershell.exe"
        )
        trusted_hosts = [
            "--trusted-host", "pypi.org",
            "--trusted-host", "pypi.python.org",
            "--trusted-host", "files.pythonhosted.org",
            "--trusted-host", "download.pytorch.org",
        ]
        
        try:
            download_env = os.environ.copy()
            download_env["LDF_MODEL_URL"] = "https://huggingface.co/ManuelVogel12/LDF_weights/resolve/main/model-40"
            download_env["LDF_MODEL_OUTPUT"] = model_path
            subprocess.run(
                [powershell_exe, "-NoProfile", "-NonInteractive", "-Command",
                 "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri $env:LDF_MODEL_URL -OutFile $env:LDF_MODEL_OUTPUT"],
                check=True,
                capture_output=True,
                text=True,
                env=download_env,
            )

            subprocess.run([base_python, "-m", "venv", "--clear", venv_dir],
                check=True,
                capture_output=True,
                text=True
            )
            
            # config.set_property("progress_bar", 10.0)
            subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip", *trusted_hosts],
            check=True,
            capture_output=True,
            text=True
        )
            # config.set_property("progress_bar", 15.0)
            subprocess.run([
                python_exe, "-m", "pip", "install", "--only-binary=:all:", *trusted_hosts,
                "numpy", "pillow", "opencv-python",
            ],
            check=True,
            capture_output=True,
            text=True
        )
            # config.set_property("progress_bar", 75.0)
            subprocess.run([
                python_exe, "-m", "pip", "install", "--only-binary=:all:", *trusted_hosts,
                "torch", "--index-url", "https://download.pytorch.org/whl/cpu", "--force-reinstall"
            ],
            check=True,
            capture_output=True,
            text=True
        )
            # config.set_property("progress_bar", 100.0)
        except subprocess.CalledProcessError as e:
            return procedure.new_return_values (Gimp.PDBStatusType.CALLING_ERROR,
                                          GLib.Error(f"Installation was not fully successful, please check the console output or rerun\nThe Error is:\n{e}. \n{e.stderr or e.stdout}"))
        except FileNotFoundError as e:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error(f"Could not start Windows PowerShell: {e}. Verify PowerShell is available, then rerun the installer.")
            )
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
    
    def remove_background(self, procedure, run_mode, image, drawables, config, data):
        import subprocess

        image.undo_group_start()

        file1 = Gio.file_new_for_path(os.path.join(tempfile.gettempdir(), "image_in.png"))
        file2 = Gio.file_new_for_path(os.path.join(tempfile.gettempdir(), "image_out.png"))

        GimpUi.init("python-plugin-offline-background-remover")

        # Create Input for LDF
        Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, file1, None)

        # Inference via external Windows Python 3.12
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        runner_script = os.path.join(plugin_dir, "run_ldf.py")
        python_exe = os.path.join(plugin_dir, "gimpenv", "Scripts", "python.exe")

        try:
            subprocess.run(
                [python_exe, runner_script],
                cwd=plugin_dir,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            image.undo_group_end()
            err_msg = e.stderr.strip() or e.stdout.strip() or "Unknown inference error."
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error(f"Inference failed:\n{err_msg}")
            )
        except FileNotFoundError:
            image.undo_group_end()
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error("Could not find gimpenv\\Scripts\\python.exe or run_ldf.py. Run the installer and verify Python 3.12 is installed.")
            )

        # Output
        result_layer = Gimp.file_load_layer(Gimp.RunMode.NONINTERACTIVE, image, file2)
        mask = result_layer.create_mask(5)
        drawables[0].add_mask(mask)

        image.undo_group_end()
        Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
 
Gimp.main(BackgroundRemover.__gtype__, sys.argv)
