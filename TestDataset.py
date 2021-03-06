#!/usr/bin/env python3

from __future__ import print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

class Rescale(object):
    """Rescale the image in a sample to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """
    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, target = sample['image'], sample['target']

        h, w = image.shape[:2]
        if isinstance(self.output_size, int):
            if h > w:
                new_h, new_w = self.output_size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transform.resize(image, (new_h, new_w))

        return {'image': img, 'target': target}

class Sample2Tensor(object):
    def __init__(self):
        pass

    def __call__(self, sample):
        img = sample['image'].transpose((2, 0, 1)).astype(np.float)
        target = sample['target']
        return {'image': torch.from_numpy(img),
                'target': torch.tensor(target)}

class SubtractMean(object):
    def __init__(self):
        pass

    def __call__(self, sample):
        img = sample['image']
        target = sample['target']

        img = img - np.mean(img)

        return {'image': img, 'target': target}

class TestDataset(Dataset):
    """Face Target dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.target_frame = pd.read_csv(csv_file,
                                           sep=";")
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.target_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.target_frame.iloc[idx, 0])
        image = io.imread(img_name)
        cls = int(self.target_frame.iloc[idx, 7])

        sample = {'image': image, 'target': cls}

        if self.transform:
            sample = self.transform(sample)

        return sample
