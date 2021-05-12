#!/usr/bin/env python3
import os
import sys
import tempfile

# This Plugin is for GIMP Version >= 2.99
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio

import gettext

baseLoc = os.path.dirname(os.path.realpath(__file__))+'/'
sys.path.extend([baseLoc+'gimpenv/lib/python2.7', baseLoc+'gimpenv/lib/python2.7/site-packages', baseLoc+'gimpenv/lib/python2.7/site-packages/setuptools'])
sys.path.extend([baseLoc+'gimpenv/lib/python3.6', baseLoc+'gimpenv/lib/python3.6/site-packages', baseLoc+'gimpenv/lib/python3.6/site-packages/setuptools'])
sys.path.extend([baseLoc+'gimpenv/lib/python3.7', baseLoc+'gimpenv/lib/python3.7/site-packages', baseLoc+'gimpenv/lib/python3.7/site-packages/setuptools'])
sys.path.extend([baseLoc+'gimpenv/lib/python3.8', baseLoc+'gimpenv/lib/python3.8/site-packages', baseLoc+'gimpenv/lib/python3.8/site-packages/setuptools'])
sys.path.extend([baseLoc+'gimpenv/lib/python3.9', baseLoc+'gimpenv/lib/python3.9/site-packages', baseLoc+'gimpenv/lib/python3.9/site-packages/setuptools'])

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

_ = gettext.gettext
def N_(message): return message


class BackgroundRemover(Gimp.PlugIn):

    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        self.set_translation_domain("gimp30-python",
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return [ 'python-fu-background-remover' ]


    def do_create_procedure(self, name):
        procedure = None
        
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.remove_background, None)
        procedure.set_image_types("*")
        procedure.set_documentation(
            N_("Easy way to remove any background from an image"),
            "test",  
            name)
        procedure.set_menu_label(N_("Background Remover"))
        procedure.set_attribution("Manuel Vogel",
                                  "Manuel Vogel",
                                  "2021")
        procedure.add_menu_path("<Image>/Filters/RemoveBackground")

        return procedure
        
    def remove_background(self, procedure, run_mode, image, n_drawables, drawables, args, data):
        image.undo_group_start()

        file1 = Gio.file_new_for_path(os.path.join(tempfile.gettempdir(), "image_in.png"))
        file2 = Gio.file_new_for_path(os.path.join(tempfile.gettempdir(), "image_out.png"))

        #create Input for LDF
        Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, [drawables[0]], file1)

        #Interference
        Ldf.test.Test(Ldf.dataset, LDF, "./").save()

        #output
        result_layer = Gimp.file_load_layer(Gimp.RunMode.NONINTERACTIVE, image, file2)
        mask = result_layer.create_mask(5)
        drawables[0].add_mask(mask)

        image.undo_group_end()
        Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
        
 
Gimp.main(BackgroundRemover.__gtype__, sys.argv)
