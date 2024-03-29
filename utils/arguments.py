import argparse
import os
import torch
import random
import utils

def common_args(parser):
    return parser

def test_args():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Label Propagation')

    # Datasets
    parser.add_argument('--workers', default=4, type=int, metavar='N',
                        help='number of data loading workers (default: 4)')
    parser.add_argument('--resume', default='./pretrained.pth', type=str, metavar='PATH',
                        help='path to latest checkpoint (default: none)')
    parser.add_argument('--manualSeed', type=int, default=777, help='manual seed')
    parser.add_argument('--type', type=str, default='test', help='train/test')

    #Device options
    parser.add_argument('--gpu-id', default='0', type=str,
                        help='id(s) for CUDA_VISIBLE_DEVICES')
    parser.add_argument('--batchSize', default=1, type=int,
                        help='batchSize')
    parser.add_argument('--temperature', default=0.07, type=float,
                        help='temperature')
    parser.add_argument('--topk', default=10, type=int,
                        help='k for kNN')
    parser.add_argument('--radius', default=12, type=float,
                        help='spatial radius to consider neighbors from')
    parser.add_argument('--videoLen', default=1, type=int,
                        help='number of context frames')

    parser.add_argument('--cropSize', default=320, type=int,
                        help='resizing of test image, -1 for native size')

    parser.add_argument('--filelist', default='./eval/davis_vallist.txt', type=str)
    parser.add_argument('--save-path', default='./results/davis2', type=str)

    parser.add_argument('--visdom', default=False, action='store_true')
    parser.add_argument('--visdom-server', default='localhost', type=str)

    # Model Details
    parser.add_argument('--model-type', default='scratch', type=str)
    parser.add_argument('--head-depth', default=-1, type=int,
                        help='depth of mlp applied after encoder (0 = linear)')

    parser.add_argument('--remove-layers', default=['layer4'], help='layer[1-4]')
    parser.add_argument('--no-l2', default=False, action='store_true', help='')

    parser.add_argument('--long-mem', default=[0], type=int, nargs='*', help='')
    parser.add_argument('--texture', default=False, action='store_true', help='')
    parser.add_argument('--round', default=False, action='store_true', help='')

    parser.add_argument('--norm_mask', default=False, action='store_true', help='')
    parser.add_argument('--finetune', default=0, type=int, help='')
    parser.add_argument('--pca-utils', default=False, action='store_true')

    args = parser.parse_args()

    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_id
    use_cuda = torch.cuda.is_available()
    if use_cuda:
        print('Using GPU', args.gpu_id)
        args.device = 'cuda'
    else:
        args.device = 'cpu'

    # Set seed
    random.seed(args.manualSeed)
    torch.manual_seed(args.manualSeed)
    if use_cuda:
        torch.cuda.manual_seed_all(args.manualSeed)

    return args

def train_args():
    parser = argparse.ArgumentParser(description='Video Walk Training')

    parser.add_argument('--data-path', default='/home/qinzheyun/Data/Kinetics400/',
        help='/home/ajabri/data/places365_standard/train/ | /data/ajabri/kinetics/')
    parser.add_argument('--ytvos-path', default='/home/qinzheyun/Data/YouTube/',
        help='/home/ajabri/data/places365_standard/train/ | /data/ajabri/kinetics/')
    parser.add_argument('--ytvos-masks', default=False,
                        help="Train segmentation head if the flag is provided")
    parser.add_argument('--type', type=str, default='train', help='train/test')


    parser.add_argument('--data-fold', default=200, help='The proportion of training data')
    parser.add_argument('--device', default='cuda', help='device')
    parser.add_argument('--device_ids', default=[0], help='device')
    parser.add_argument('--clip-len', default=8, type=int, metavar='N',
                        help='number of frames per clip')
    parser.add_argument('--clips-per-video', default=5, type=int, metavar='N',
                        help='maximum number of clips per video to consider')
    parser.add_argument('-b', '--batch-size', default=4, type=int)
    parser.add_argument('--epochs', default=25, type=int, metavar='N',
                        help='number of total epochs to run')
    parser.add_argument('--steps-per-epoch', default=1e10, type=int, help='max number of batches per epoch')
    parser.add_argument('-j', '--workers', default=0, type=int, metavar='N',
                        help='number of data loading workers (default: 16)')
    parser.add_argument('--lr', default=1e-4, type=float, help='initial learning rate')
    parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                        help='momentum')
    parser.add_argument('--wd', '--weight-decay', default=1e-4, type=float,
                        metavar='W', help='weight decay (default: 1e-4)',
                        dest='weight_decay')

    parser.add_argument('--lr-milestones', nargs='+', default=[20, 30, 40], type=int, help='decrease lr on milestones')
    parser.add_argument('--lr-gamma', default=0.3, type=float, help='decrease lr by a factor of lr-gamma')
    parser.add_argument('--lr-warmup-epochs', default=0, type=int, help='number of warmup epochs')
    parser.add_argument('--print-freq', default=10, type=int, help='print frequency')
    parser.add_argument('--output-dir', default='auto', help='path where to save')
    parser.add_argument('--resume', default='', help='resume from checkpoint')
    parser.add_argument('--partial-reload', default='', help='reload net from checkpoint, ignoring keys that are not in current model')
    parser.add_argument('--start-epoch', default=0, type=int, metavar='N',
                        help='start epoch')
    
    parser.add_argument( "--cache-dataset", dest="cache_dataset",
                         help="Cache the datasets for quicker initialization. It also serializes the transforms",
                         default=True )
    parser.add_argument( "--data-parallel", dest="data_parallel", help="", default=True)
    parser.add_argument( "--fast-test", dest="fast_test", help="", action="store_true", )

    parser.add_argument('--name', default='', type=str, help='')
    parser.add_argument('--dropout', default=0.1, type=float, help='dropout rate on A')
    parser.add_argument('--zero-diagonal', help='always zero diagonal of A', action="store_true", )
    parser.add_argument('--flip', default=False, help='flip transitions (bug)', action="store_true", )

    parser.add_argument('--frame-aug', default='grid', type=str,
        help='grid or none')
    parser.add_argument('--frame-transforms', default='crop', type=str,
        help='combine, ex: crop, cj, flip')

    parser.add_argument('--frame-skip', default=8, type=int, help='kinetics: fps | others: skip between frames')
    parser.add_argument('--img-size', default=256, type=int)
    parser.add_argument('--patch-size', default=[64, 64, 3], type=int, nargs="+")

    parser.add_argument('--port', default=8095, type=int, help='visdom port')
    parser.add_argument('--server', default='localhost', type=str, help='visdom server')

    parser.add_argument('--model-type', default='scratch', type=str, help='scratch | imagenet | moco')
    parser.add_argument('--optim', default='adam', type=str, help='adam | sgd')

    parser.add_argument('--temp', default=0.07,
        type=float, help='softmax temperature when computing affinity')
    parser.add_argument('--featdrop', default=0.0, type=float, help='"regular" dropout on features')
    parser.add_argument('--restrict', default=-1, type=int, help='restrict attention')
    parser.add_argument('--head-depth', default=0, type=int, help='depth of head mlp; 0 is linear')
    parser.add_argument('--visualize', default=False, help='visualize with wandb and visdom')
    parser.add_argument('--remove-layers', default=[], help='layer[1-4]')

    # sinkhorn-knopp ideas (experimental)
    parser.add_argument('--sk-align', default=False, action='store_true',
        help='use sinkhorn-knopp to align matches between frames')
    parser.add_argument('--sk-targets', default=False, action='store_true',
        help='use sinkhorn-knopp to obtain targets, by taking the argmax')

    # graph kernel
    parser.add_argument('--hidden-graphs', type=int, default=10, metavar='N', help='Number of hidden graphs')
    parser.add_argument('--size-hidden-graphs', type=int, default=5, metavar='N',
                        help='Number of nodes of each hidden graph')
    parser.add_argument('--hidden-dim', type=int, default=4, metavar='N', help='Size of hidden layer of NN')
    parser.add_argument('--penultimate-dim', type=int, default=512, metavar='N', help='Size of penultimate layer of NN')
    parser.add_argument('--n_classes', type=int, default=40, help='Size of penultimate layer of NN')
    parser.add_argument('--max-step', type=int, default=5, metavar='N', help='Max length of walks')
    parser.add_argument('--rw_normalize', action='store_true', default=False,
                        help='Whether to normalize the kernel values')
    parser.add_argument('--rw_dropout', type=float, default=0.2, help='Dropout rate (1 - keep probability).')

    args = parser.parse_args()

    if args.fast_test:
        args.batch_size = 1
        args.workers = 0
        args.data_parallel = False

    if args.output_dir == 'auto':
        keys = {
            'dropout':'drop', 'clip_len': 'len', 'frame_transforms': 'ftrans', 'frame_aug':'faug', 
            'optim':'optim', 'temp':'temp', 'featdrop':'fdrop', 'lr':'lr', 'head_depth':'mlp'
        }
        name = '-'.join(["%s%s" % (keys[k], getattr(args, k) if not isinstance(getattr(args, k), list) else '-'.join([str(s) for s in getattr(args, k)])) for k in keys])
        args.output_dir = "checkpoints/%s_%s/" % (args.name, name)

        import datetime
        dt = datetime.datetime.today()
        args.name = "%s-%s-%s_%s" % (str(dt.month), str(dt.day), args.name, name)

    utils.mkdir(args.output_dir)

    return args




