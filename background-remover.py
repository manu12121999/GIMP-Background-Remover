#!/usr/bin/env python3
import os
import sys
import tempfile

# This Plugin is only for GIMP Version >= 3.0.0 and linux
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


# pip install numpy, torch, pillow, opencv-python
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
#from torchvision import transforms

from Ldf.net import LDF
import Ldf.test
import Ldf.dataset


class BackgroundRemover(Gimp.PlugIn):

    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        return [ 'python-plugin-offline-background-remover' ]


    def do_create_procedure(self, name):
        procedure = None
        
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

        return procedure
        
    def remove_background(self, procedure, run_mode, image, drawables, config, data):
        image.undo_group_start()

        file1 = Gio.file_new_for_path(os.path.join(tempfile.gettempdir(), "image_in.png"))
        file2 = Gio.file_new_for_path(os.path.join(tempfile.gettempdir(), "image_out.png"))
        #file1 = Gimp.temp_file('png')
        #file2 = Gimp.temp_file('png')
        
        GimpUi.init("python-plugin-offline-background-remover")
            
        dialog = GimpUi.ProcedureDialog.new(procedure, config, "Hello World")
        dialog.fill(None)
    

        #create Input for LDF
        Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, file1, None)

        #Inference
        try:
            Ldf.test.Test(Ldf.dataset, LDF, "./").save()
        except FileNotFoundError:
            return procedure.new_return_values (Gimp.PDBStatusType.CALLING_ERROR,
                                          GLib.Error(f"Weights not found. Please download all files described in the README"))

        #output
        result_layer = Gimp.file_load_layer(Gimp.RunMode.NONINTERACTIVE, image, file2)
        mask = result_layer.create_mask(5)
        drawables[0].add_mask(mask)

        image.undo_group_end()
        Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
        
 
Gimp.main(BackgroundRemover.__gtype__, sys.argv)