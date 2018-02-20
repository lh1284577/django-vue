#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory,Host,Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
from collections import namedtuple
import logging
import json , sys , os
from  ansible_callback import ResultCallback
import multiprocessing
import time,datetime


class AnsibleTask(object):

    def __init__(self, rediskey=None,extra_vars=None,playbook_path=None):
        self.results_raw = {}
        self.callback = None
        self.runner = None
        self.playbook_path = playbook_path
        self.extra_vars = extra_vars
        self.rediskey = rediskey


    def ansiblePlay(self):

        '''run ansible playbook'''
        variable_manager = VariableManager()
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'listhosts', 'listtasks',  'listtags',  'syntax', 'become', 'become_method', 'become_user', 'check'])
        options = Options(connection='ssh', module_path='', forks=1, become=None, listhosts=None, listtasks=False, listtags=False, syntax=False, become_method=None, become_user=None, check=False)
        loader = DataLoader()

        inventory = Inventory(loader=loader, variable_manager=variable_manager)
        variable_manager.set_inventory(inventory)
        self.callback = ResultCallback(self.rediskey)
        variable_manager.extra_vars = self.extra_vars

        self.runner = PlaybookExecutor(playbooks=self.playbook_path, inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=None)
        self.runner._tqm._stdout_callback = self.callback

    '''执行playbook'''
    def run(self):
        dprocess = multiprocessing.Process(target = self.multipF,args=())
        dprocess.start()
        return 'run playbook'

    '''开启一个子进程跑ansible'''
    def multipF(self):
        self.runner.run()
        return 



if __name__ == '__main__':
    ansibleTask = AnsibleTask('ansible.deploy.9647000277',{"hosts":"localhost","user":"root"},['/opt/lihao.yml'])
    ansibleTask.ansiblePlay()
    ansibleTask.run()
