#!/usr/bin/python3
#coding=utf-8

import os
import cv2
import torch
import numpy as np
import tempfile
from torch.utils.data import Dataset

########################### Data Augmentation ###########################
class Normalize(object):
    def __init__(self, mean, std):
        self.mean = mean 
        self.std  = std
    
    def __call__(self, image, mask=None, body=None, detail=None):
        image = (image - self.mean)/self.std
        if mask is None:
            return image
        return image, mask/255, body/255, detail/255

class Resize(object):
    def __init__(self, H, W):
        self.H = H
        self.W = W

    def __call__(self, image, mask=None, body=None, detail=None):
        image = cv2.resize(image, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        if mask is None:
            return image
        mask  = cv2.resize( mask, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        body  = cv2.resize( body, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        detail= cv2.resize( detail, dsize=(self.W, self.H), interpolation=cv2.INTER_LINEAR)
        return image, mask, body, detail

class ToTensor(object):
    def __call__(self, image, mask=None, body=None, detail=None):
        image = torch.from_numpy(image)
        image = image.permute(2, 0, 1)
        if mask is None:
            return image
        mask  = torch.from_numpy(mask)
        body  = torch.from_numpy(body)
        detail= torch.from_numpy(detail)
        return image, mask, body, detail


########################### Config File ###########################
class Config(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.mean   = np.array([[[124.55, 118.90, 102.94]]])
        self.std    = np.array([[[ 56.77,  55.97,  57.50]]])
        #print('\nParameters...')
        #for k, v in self.kwargs.items():
         #   print('%-10s: %s'%(k, v))

    def __getattr__(self, name):
        if name in self.kwargs:
            return self.kwargs[name]
        else:
            return None


########################### Dataset Class ###########################
class Data(Dataset):
    def __init__(self, cfg):
        self.cfg        = cfg
        self.normalize  = Normalize(mean=cfg.mean, std=cfg.std)
        self.resize     = Resize(352, 352)
        self.totensor   = ToTensor()


    def __getitem__(self, idx):
        image = cv2.imread(os.path.join(tempfile.gettempdir(), "image_in.png"))[:,:,::-1].astype(np.float32)
        shape = image.shape[:2]
        image = self.normalize(image)
        image = self.resize(image)
        image = self.totensor(image)
        return image, shape, 'image_in'

    def __len__(self):
        return 1

    
    def collate(self, batch):
        size = [224, 256, 288, 320, 352][np.random.randint(0, 5)]
        image, mask, body, detail = [list(item) for item in zip(*batch)]
        for i in range(len(batch)):
            image[i] = cv2.resize(image[i], dsize=(size, size), interpolation=cv2.INTER_LINEAR)
            mask[i]  = cv2.resize(mask[i],  dsize=(size, size), interpolation=cv2.INTER_LINEAR)
            body[i]  = cv2.resize(body[i],  dsize=(size, size), interpolation=cv2.INTER_LINEAR)
            detail[i]= cv2.resize(detail[i],  dsize=(size, size), interpolation=cv2.INTER_LINEAR)
        image  = torch.from_numpy(np.stack(image, axis=0)).permute(0,3,1,2)
        mask   = torch.from_numpy(np.stack(mask, axis=0)).unsqueeze(1)
        body   = torch.from_numpy(np.stack(body, axis=0)).unsqueeze(1)
        detail = torch.from_numpy(np.stack(detail, axis=0)).unsqueeze(1)
        return image, mask, body, detail
