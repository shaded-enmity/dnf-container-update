#!/usr/bin/python -tt
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import dnf
import dnf.cli
import dnfpluginsextras
import os

from ctypes import CDLL
libc = CDLL(None, use_errno=True)

_ = dnfpluginsextras._

''' Operate on packages in a running container

Because we still want to be able to execute scriptlets
we need to:
 * join target process namespaces
 * chroot into target process root

Otherwise executing scriptlets would have effect on the 
host system.
'''

class ContainerHandler(dnf.Plugin):
  name = 'container'

  def __init__(self, base, cli):
    super(ContainerHandler, self).__init__(base, cli)
    if cli is None:
      return
    cli.register_command(ContainerHandlerCommand)

class ContainerHandlerCommand(dnf.cli.Command):
  aliases = ('container',)
  summary = _('Perform operation in target container chroot')
  usage = '[--docker-id] CONTAINERPID [install|update|remove] [ARG0 ARG1 ...]'

  def __init__(self, args):
    super(ContainerHandlerCommand, self).__init__(args)
    self.pid = None
    self.action = None
    self.args = None

  def _unshare_chroot(self):
    nsdesc = []
    # keep the fd's open so we can `setns` _after_ chroot
    for ns in os.listdir('/proc/{0}/ns/'.format(self.pid)):
      nsdesc.append(open(os.path.join('/proc/{0}/ns'.format(self.pid), ns)))
    # chroot into the container
    os.chroot('/proc/{0}/root/'.format(self.pid))
    for ns in nsdesc:
      # join namespace and close fd
      assert libc.setns(ns.fileno(), 0) == 0
      ns.close()
    # fork and exit the parent so that we're in the same PID namespace
    npid = os.fork()
    if npid:
      print('[+] waiting for child: {0}'.format(npid))
      pid, exit = os.wait()
      # exit status indication: a 16-bit number, whose low byte is the signal number
      # that killed the process, and whose high byte is the exit status
      eccode = (exit >> 8) & 0xFF
      ecsig = exit & 0xFF
      print('[-] exiting child: {0}, signal: {1}, error code: {2}'.format(npid, ecsig, eccode))
      if not ecsig:
        os._exit(eccode)
      else:
        raise dnf.exceptions.Error('child process killed with a signal: {0}'.format(ecsig))
    else:
      print('[*] executing child: {0}'.format(os.getpid()))
      return True

  def _load_data(self):
    print('[*] reading repositories')
    self.base.read_all_repos()
    print('[*] filling sack')
    self.base.fill_sack()
    print('[*] reading comps')
    self.base.read_comps()
    #dnfpluginsextras.logger.debug(_("Error loading data:\n%s"), e.message)

  def _get_args(self, args):
    p = dnfpluginsextras.ArgumentParser(ContainerHandlerCommand.aliases[0])
    p.add_argument('--docker-id', action='store_true', help='interpret containerpid as container id')
    p.add_argument('--docker-commit', default=None, help='name for the new image')
    p.add_argument('containerpid', help='pid of the process')
    p.add_argument('action', help='one of install, update or remove')
    p.add_argument('pkgs', nargs='?', help='optional package names')
    return p.parse_args(args)

  def _validate_and_set_args(self, parsed):
    if parsed.docker_id:
      import docker
      d = docker.Client()
      stat = d.inspect_container(parsed.containerpid)
      if not stat:
        return False, 'Bad Docker container ID'
      parsed.containerpid = stat['State']['Pid']
    if type(parsed.containerpid) is not int:
      try:
        pid = int(parsed.containerpid.strip(), 10)
      except ValueError:
        pid = None
      if not pid:
        return False, 'Invalid CONTAINERPID'
      self.pid = pid
    else:
      self.pid = parsed.containerpid
    if parsed.action.lower() not in ['install', 'update', 'remove']:
      return False, 'Invalid action, see usage'
    self.action = parsed.action.lower()
    self.args = parsed.pkgs
    if self.action in ['install', 'remove'] and len(self.args) == 0:
      return False, 'No packages specified to install/remove'
    return True, None

  def configure(self, args):
    a = self._get_args(args)
    valid, msg = self._validate_and_set_args(a)
    if valid:
      self._unshare_chroot()
      self._load_data()
    else:
      print(msg)
      os.exit(os.EX_DATAERR)

  def run(self, args):
    print('[+] running ...')
    if self.action == 'update':
      if not self.args or self.args[0] == '*':
        self.base.upgrade_all()
      else:
        update = []
        for arg in self.args:
          if arg.startswith('@'):
            try:
              grp = self.base.comps.group_by_pattern(arg[1:])
              self.base.group_upgrade(grp)
            except dnf.exceptions.CompsError:
              pass
          else:
            update.append(arg)
        q = self.base.sack.query().installed()
        for n in update:
          u = q.filter(provides=n)
          if u:
            self.base.upgrade(n)
          else:
            raise dnf.exceptions.PackagesNotInstalledError(package=n)

      self.base.resolve(True)
      self.base.download_packages(self.base.transaction.install_set)
      self.base.do_transaction()
