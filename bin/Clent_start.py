#!/usr/bin/env python
# coding:utf-8
# Author: Sun Yang
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.client import Client

if __name__ == '__main__':
    a = Client()