import os
import sys

# Ensure the plugin directory is on Python's path so it finds the Ldf folder
plugin_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(plugin_dir)
sys.path.insert(0, plugin_dir)

from Ldf.net import LDF
import Ldf.test
import Ldf.dataset

if __name__ == "__main__":
    Ldf.test.Test(Ldf.dataset, LDF, "./").save()
