#!/usr/bin/env python3
import argparse
import logging
import os
import shutil
import sys
from distutils.dir_util import copy_tree
from pathlib import Path

import StableDiffusionAPI
from StableDiffusionAPI.helpers import script_path, print_api_result
from StableDiffusionAPI.config import Config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stable Diffusion WebUI API.')
    parser.add_argument('--config', default=os.path.join(script_path, 'config.yml'), help='Path to the config file.')
    parser.add_argument('--force', action='store_true', help='Override any checks.')
    parser.add_argument('-y', '--yes', action='store_true', help='Always default to yes.')
    parser.add_argument('-v', dest='verbose_logging', action='store_true', help='Verbose logging.')

    root_choice = parser.add_subparsers(required=True)

    # Show info
    show_info = root_choice.add_parser('info', help='Show info.')
    show_info.add_argument('show_info', nargs='*', help='Show info.')

    # Hypernetworks
    hypernetwork = root_choice.add_parser('hypernetwork', help='Manage hypernetworks')
    hypernetwork_root = hypernetwork.add_subparsers(required=True)

    # Create hypernetwork
    hypernetwork_create = hypernetwork_root.add_parser('create', help='Create a blank hypernetwork.')
    hypernetwork_create.add_argument('hypernetwork_create_name', metavar='name', help='Name of the blank hypernetwork.')

    # Train hypernetwork
    hypernetwork_train = hypernetwork_root.add_parser('train', help='Train a hypernetwork.')
    hypernetwork_train.add_argument('hypernetwork_train_name', metavar='name', help='Name of the hypernetwork to train.')
    hypernetwork_train.add_argument('hypernetwork_train_dataset', metavar='dataset_path', help='Path to the directory containing the images to train on.')
    hypernetwork_train.add_argument('--learning-rate', metavar='LEARNING RATE', dest='hypernetwork_train_lr', type=float, default=0.005, required=False, help='Learning rate.')
    hypernetwork_train.add_argument('--batch', metavar='BATCH', dest='hypernetwork_train_batch', type=int, default=1, required=False, help='Batch size.')
    hypernetwork_train.add_argument('--log', metavar='PATH', dest='hypernetwork_train_log', default='hypernetwork_training', required=False, help='Log directory.')
    hypernetwork_train.add_argument('--steps', metavar='STEPS', dest='hypernetwork_train_steps', type=int, default=100000, required=False, help='Max number of steps.')
    hypernetwork_train.add_argument('--img', metavar='IMG', dest='hypernetwork_train_img', type=int, default=500, required=False, help='Save an image to log directory every N steps. 0 to disable.')
    hypernetwork_train.add_argument('--emb', metavar='EMB', dest='hypernetwork_train_emb', type=int, default=500, required=False, help='Save a copy of embedding to log directory every N steps. 0 to disable.')
    hypernetwork_train.add_argument('--template', metavar='PATH', dest='hypernetwork_train_template', type=str, default=None, required=False, help='Prompt template file. Automatically set.')
    hypernetwork_train.add_argument('--read-params', metavar='READ', dest='hypernetwork_train_read', choices=[True, False], type=bool, default=False, required=False, help='Read parameters (prompt, etc...) from txt2img tab when making previews.')
    hypernetwork_train.add_argument('--create', metavar='CREATE', dest='hypernetwork_train_create', choices=[True, False], type=bool, default=False, required=False, help='Create a blank hypernetwork before training.')

    # Install
    install = root_choice.add_parser('install', help='Install this CLI program.')
    install.add_argument('--path', metavar='PATH', dest='install_path', default='~/.stablediffusion/api/', required=False, help='Path to install the application to.')

    # Uninstall
    uninstall = root_choice.add_parser('uninstall', help='Uninstall this CLI program.')
    uninstall.add_argument('--path', metavar='PATH', dest='uninstall_path', default='~/.stablediffusion/api/', required=True, help='')

    args = parser.parse_args()

    if args.verbose_logging:
        log_level = logging.DEBUG
    else:
        log_level = logging.CRITICAL
    logging.basicConfig(level=log_level)

    # If we can't find the config file check other places
    if not os.path.isfile(args.config):
        x = os.path.join(os.path.expanduser('~'), '.stablediffusion', 'api')
        if os.path.isfile(os.path.join(script_path, 'config.yaml')):
            config = os.path.join(script_path, 'config.yaml')
        elif os.path.isfile(os.path.join(x, 'config.yml')):
            config = os.path.join(x, 'config.yml')
        elif os.path.isfile(os.path.join(x, 'config.yaml')):
            config = os.path.join(x, 'config.yaml')
        else:
            print('Could not find config file in these locations:', '\n', args.config, '\n', os.path.join(script_path, 'config.yaml'), '\n', os.path.join(x, 'config.yml'), '\n', os.path.join(x, 'config.yaml'))
            sys.exit(1)
    else:
        config = Config(args.config)
    logging.debug(f'Config file loaded from: {config}')

    api = StableDiffusionAPI.API(config)
    # Info
    if 'show_info' in args:
        print('=== Stable Diffusion API ===')
        print('For AUTOMATIC1111\'s stable-diffusion-webui\n')
        print('Target:', config.target_server)
        print('Target URL:', config.webui_base_url if config.target_server == 'webui' else config.django_base_url)
        print('Installed to:', script_path)


    # Install
    elif 'install_path' in args:
        target_path = Path(args.install_path).expanduser()
        print(target_path, script_path)
        if target_path == script_path:
            print('Already installed!')
            print(script_path, ' --> ', target_path)
            sys.exit(1)
        if not os.path.exists(target_path) or args.force:
            if not os.path.exists(os.path.join(target_path, 'bin')):
                os.makedirs(os.path.join(target_path, 'bin'))
            shutil.copyfile(os.path.join(script_path, 'config.yml'), os.path.join(target_path, 'config.yml'))
            shutil.copyfile(os.path.join(script_path, 'stable-diffusion.py'), os.path.join(target_path, 'bin', 'stable-diffusion'))
            copy_tree(os.path.join(script_path, 'StableDiffusionAPI'), os.path.join(target_path, 'bin', 'StableDiffusionAPI'))
            print('Installed to', target_path)
            print('Add this to your PATH:', os.path.join(target_path, 'bin'))
            print('New config file:', os.path.join(target_path, 'config.yml'))
            print('Run with command: stable-diffusion')
        else:
            print('Install dir exists:', args.install_path)
            print('Use --force to override')


    # Uninstall
    elif 'uninstall_path' in args:
        target_path = Path(args.uninstall_path).expanduser()
        if os.path.exists(target_path):
            if not args.yes:
                print('Uninstall from:', target_path)
                while True:
                    i = input('Delete the ENTIRE directory? y/n: ')
                    if i.lower() == 'y' or i.lower() == 'n':
                        break
            else:
                i = 'y'
            if i.lower() == 'y':
                shutil.rmtree(target_path)
                print('Uninstalled stable-diffusion API')
        else:
            print('Directory not found:', args.uninstall_path)


    # Hypernetworks
    elif 'hypernetwork_create_name' in args:
        r = api.create_hypernetwork(args.hypernetwork_create_name)
        print(print_api_result(r))
    elif 'hypernetwork_train_name' in args:
        r = api.train_hypernetwork(args.hypernetwork_train_name, args.hypernetwork_train_dataset,
                                   lr=args.hypernetwork_train_lr, batch=args.hypernetwork_train_batch, log=args.hypernetwork_train_log,
                                   steps=args.hypernetwork_train_steps, sample_img_n=args.hypernetwork_train_img, sample_emb_n=args.hypernetwork_train_emb,
                                   template=args.hypernetwork_train_template, read_params=args.hypernetwork_train_read, create=args.hypernetwork_train_create)
        print(print_api_result(r))
