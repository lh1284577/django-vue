#coding=utf-8

import os, sys, django, logging, time
from ansible.plugins.callback import CallbackBase
sys.path.append('../../')
os.environ['DJANGO_SETTINGS_MODULE'] ='baiwei.settings'
from baiwei import settings
from yunwei.data.Redis import Redis
import json
django.setup()

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

class ResultCallback(CallbackBase):

    def __init__(self,rediskey,*args, **kwargs):
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}
        self.task_changed = {}
        self.rediskey = rediskey
        self.count = 0
        self.out = {}
        self.deploy_out = []



    def output_handler(self, res, status):

        msg = "%s: [%s]\noutput_lines:\n" % (status, res._host.get_name().encode('utf-8'))
        if res._result.get('stdout'):
            stdout = res._result.get('stdout')
        elif res._result.get('stdout_lines'):
            stdout = res._result.get('stdout_lines')
        elif res._result.get('msg'):
            stdout = res._result.get('msg')
        elif res._result.get('stderr'):
            stdout = res._result.get('stderr')
        else:
            stdout = [u'该任务无输出']
        if isinstance(stdout, unicode) or isinstance(stdout, str):
            msg += '    ' + stdout.encode('utf-8')
        else:
            for i in stdout:
                msg += '    ' + i
        Redis.lpush(self.rediskey,msg)


    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result._result
        if result._task.action in ('include', 'include_role'):
            return
        elif result._result.get('changed', False):
            self.output_handler(result, 'ok')
        else:
                msg = "ok: [%s]" % result._host.get_name()
                Redis.lpush(self.rediskey,msg)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result._result
        self.output_handler(result, 'failed')


    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result._result
        msg = "fatal: [{host}]: UNREACHABLE! => {msg}\n".format(host=result._host.get_name(),msg=json.dumps(result._result))
        Redis.lpush(self.rediskey,msg)

    def v2_runner_on_changed(self, result):
        self.task_changed[result._host.get_name()] = result._result
        msg = "changed: [{host}]\n".format(host=result._host.get_name())
        Redis.lpush(self.rediskey,msg)

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()]  = result._result
        msg = "skipped: [{host}]\n".format(host=result._host.get_name())
        Redis.lpush(self.rediskey,msg)

    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if not name:
            msg = u"PLAY"
        else:
            msg = u"PLAY [%s] " % name
        if len(msg) < 80:msg = msg + '*'*(79-len(msg))
        Redis.lpush(self.rediskey,msg)

    def _print_task_banner(self, task):
        msg = "\nTASK [%s] " % (task.get_name().strip())
        if len(msg) < 80:
            msg = msg + '*'*(80-len(msg))
        self.count += 1
        Redis.lpush(self.rediskey,msg)

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._print_task_banner(task)

    def v2_playbook_on_cleanup_task_start(self, task):
        msg = "CLEANUP TASK [%s]" % task.get_name().strip()
        Redis.lpush(self.rediskey,msg)

    def v2_playbook_on_handler_task_start(self, task):
        msg = "RUNNING HANDLER [%s]" % task.get_name().strip()
        Redis.lpush(self.rediskey,msg)

    def v2_playbook_on_stats(self, stats):
        msg = "\nPLAY RECAP *********************************************************************"
        hosts = sorted(stats.processed.keys())
        Redis.lpush(self.rediskey, 'Deploy End')
    def v2_runner_item_on_ok(self, result):
        if result._task.action in ('include', 'include_role'):
            return
        elif result._result.get('changed', False):
            msg = 'changed'
        else:
            msg = 'ok'
        msg += " => (item=%s)" % (json.dumps(self._get_item(result._result)))
        # msg += " => %s" % json.dumps(result._result)
        Redis.lpush(self.rediskey,msg)

    def v2_runner_item_on_failed(self, result):
        msg = "failed: [%s]" % result._host.get_name()
        msg += "[%s]" % (result._host.get_name())
        msg = msg + " (item=%s) => %s\n" % (self._get_item(json.dumps(result._result)), json.dumps(result._result)),
        Redis.lpush(self.rediskey,msg)


    def v2_runner_item_on_skipped(self, result):
        msg = "skipping: [%s] => (item=%s) " % (result._host.get_name(), self._get_item(result._result))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s" % json.dumps(result._result)
        Redis.lpush(self.rediskey,msg)

    def v2_runner_retry(self, result):
        task_name = result.task_name or result._task
        msg = "FAILED - RETRYING: %s (%d retries left)." % (task_name, result._result['retries'] - result._result['attempts'])
        if (self._display.verbosity > 2 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += "Result was: %s" % json.dumps(result._result,indent=4)
        Redis.lpush(self.rediskey,msg)


