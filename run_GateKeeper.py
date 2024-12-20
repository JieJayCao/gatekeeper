
import time
import torch
import numpy as np
from train import train, init_network,test

from importlib import import_module
import argparse
from utils_GateKeeper import build_dataset, build_iterator, get_time_dif

parser = argparse.ArgumentParser(description='Encrypted Traffic Classification')
parser.add_argument('--test', type=bool, default=False, help='Train or Test.')

args = parser.parse_args()



def main():
    
    dataset = "/media/jie/MyPassport/ExpBackup/11.26-3080/Program/GateKeeper/FNet/dataset/IoT23"    
    model_name = 'GateKeeper' 
    
    x = import_module(model_name)

    config = x.Config(dataset)
    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  

    start_time = time.time()
    print("Loading data...")
    train_data, dev_data, test_data = build_dataset(config)
    
    train_iter = build_iterator(train_data, config)
    

    dev_iter = build_iterator(dev_data, config)
    test_iter = build_iterator(test_data, config)
    
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    # train
    
    model = x.Model(config).to(config.device)
    #init_network(model)
    
    if args.test == False:
        print(args.test)
        print(model.parameters)
        train(config, model, train_iter, dev_iter, test_iter)
    else:
        test(config,model,test_iter)
    
if __name__ == '__main__':
    main()