import os
import torch
import numpy as np
import pickle as pkl
from tqdm import tqdm
import time
from datetime import timedelta
import random

def Dec(content):
    new = [int(i.strip("\n")) for i in content]
    return new


def build_dataset(config):
   
    tokenizer = lambda x: x.split(' ')  
   
    def load_dataset(path):
        contents = []
        
        # Example IoT-23 KBS result 
        pos = [22, 42, 3, 23, 5, 24, 27, 26, 46, 2, 25, 10, 41, 35, 11, 20, 36, 4, 37, 32, 21, 30, 29, 31, 44, 34, 40, 9, 17, 33, 28, 8, 49, 47, 16, 48, 43, 45, 39, 38, 1, 15, 13, 19, 7, 12, 18, 14, 6, 0]
        # Randomly select 20 bytes
        # pos = random.sample(range(0, 50), config.byte_len_withKBS)
        pos = sorted(pos[:config.byte_len_withKBS])
        
        with open(path, 'r', encoding='UTF-8') as f:
            for line in tqdm(f):
                lin = line.strip()
                if not lin:
                    continue
                content, label = lin.split('\t')

                token = tokenizer(content)
      
                token = [token[i] for i in pos] 
                contents.append((Dec(token),pos,int(label)))
                
        return contents  

    train = load_dataset(config.train_path)
    dev = load_dataset(config.dev_path)
    test = load_dataset(config.test_path)
    return train, dev, test


class DatasetIterater(object):
    def __init__(self, batches, batch_size, device):
        self.batch_size = batch_size
        self.batches = batches
        self.n_batches = len(batches) // batch_size
        self.residue = False  
        if len(batches) % self.n_batches != 0:
            self.residue = True
        self.index = 0
        self.device = device

    def _to_tensor(self, datas):
        #x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
        #pos = torch.LongTensor([_[1] for _ in datas]).to(self.device)
        #y = torch.LongTensor([_[2] for _ in datas]).to(self.device)
        
        x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
        pos = torch.LongTensor([_[1] for _ in datas]).to(self.device)
        y = torch.LongTensor([_[2] for _ in datas]).to(self.device)
        
        #print(x.shape)
        #x = torch.reshape(x,(x.shape[0],50))
        
        
        return x,pos,y
        
        
    def __next__(self):
        if self.residue and self.index == self.n_batches:
            batches = self.batches[self.index * self.batch_size: len(self.batches)]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

        elif self.index >= self.n_batches:
            self.index = 0
            raise StopIteration
        else:
            batches = self.batches[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

    def __iter__(self):
        return self

    def __len__(self):
        if self.residue:
            return self.n_batches + 1
        else:
            return self.n_batches


def build_iterator(dataset, config):
    iter = DatasetIterater(dataset, config.batch_size, config.device)
    return iter


def get_time_dif(start_time):
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))

if __name__ == '__main__':
    test_list = ["ff" for i in range(50)]
    
