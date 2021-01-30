#!/usr/bin/python3
#coding=utf-8

import os
import tempfile
import sys
#sys.path.insert(0, '../')
sys.dont_write_bytecode = True

import cv2
import numpy as np

import torch
import Ldf.dataset
from torch.utils.data import DataLoader
from Ldf.net import LDF

class Test(object):
    def __init__(self, Dataset, Network, Path):
        ## dataset
        #self.cfg    = Dataset.Config(datapath=".", snapshot='./model-40', mode='test')
        self.cfg    = Dataset.Config(datapath=".", snapshot= os.path.join(os.path.dirname(__file__), 'model-40'), mode='test')
        self.data   = Dataset.Data(self.cfg)
        self.loader = DataLoader(self.data, batch_size=1, shuffle=False, num_workers=2)
        ## network
        self.net    = Network(self.cfg)
        self.net.train(False)
        #self.net.cuda()

    def save(self):
        with torch.no_grad():
            for image, (H, W), name in self.loader:
                #image, shape  = image.cuda().float(), (H, W)#
                image, shape  = image.float(), (H, W)
                outb1, outd1, out1, outb2, outd2, out2 = self.net(image, shape)
                out  = out2
                pred = torch.sigmoid(out[0,0]).cpu().numpy()*255
            
                cv2.imwrite(os.path.join(tempfile.gettempdir(), "image_out.png"), np.round(pred))



if __name__=='__main__':
    t = Test(dataset, LDF, "./")
    t.save()
    print("success")
