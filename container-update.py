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

#+---------------------------+#
#| Does not work as expected |#
#+---------------------------+#
def _cache_python():
  import abc as cache_abc
  import _abcoll as cache__abcoll
  import argparse as cache_argparse
  import array as cache_array
  import atexit as cache_atexit
  import base64 as cache_base64
  import bdb as cache_bdb
  import binascii as cache_binascii
  import bz2 as cache_bz2
  import calendar as cache_calendar
  import cmd as cache_cmd
  import codecs as cache_codecs
  import _codecs as cache__codecs
  import collections as cache_collections
  import _collections as cache__collections
  import ConfigParser as cache_ConfigParser
  import contextlib as cache_contextlib
  import copy as cache_copy
  import copy_reg as cache_copy_reg
  import cPickle as cache_cPickle
  import cStringIO as cache_cStringIO
  import curses as cache_curses
  import _curses as cache__curses
  import curses.has_key as cache_curses_has_key
  import curses.wrapper as cache_curses_wrapper
  import datetime as cache_datetime
  import difflib as cache_difflib
  import dis as cache_dis
  import distutils as cache_distutils
  import distutils.debug as cache_distutils_debug
  import distutils.errors as cache_distutils_errors
  import distutils.log as cache_distutils_log
  import distutils.spawn as cache_distutils_spawn
  import distutils.sysconfig as cache_distutils_sysconfig
  import distutils.text_file as cache_distutils_text_file
  import distutils.version as cache_distutils_version
  import dnf as cache_dnf
  import dnf.arch as cache_dnf_arch
  import dnf.base as cache_dnf_base
  import dnf.callback as cache_dnf_callback
  import dnf.cli as cache_dnf_cli
  import dnf.cli.cli as cache_dnf_cli_cli
  import dnf.cli.commands as cache_dnf_cli_commands
  import dnf.cli.commands.autoremove as cache_dnf_cli_commands_autoremove
  import dnf.cli.commands.clean as cache_dnf_cli_commands_clean
  import dnf.cli.commands.distrosync as cache_dnf_cli_commands_distrosync
  import dnf.cli.commands.downgrade as cache_dnf_cli_commands_downgrade
  import dnf.cli.commands.group as cache_dnf_cli_commands_group
  import dnf.cli.commands.install as cache_dnf_cli_commands_install
  import dnf.cli.commands.makecache as cache_dnf_cli_commands_makecache
  import dnf.cli.commands.mark as cache_dnf_cli_commands_mark
  import dnf.cli.commands.reinstall as cache_dnf_cli_commands_reinstall
  import dnf.cli.commands.remove as cache_dnf_cli_commands_remove
  import dnf.cli.commands.repolist as cache_dnf_cli_commands_repolist
  import dnf.cli.commands.search as cache_dnf_cli_commands_search
  import dnf.cli.commands.updateinfo as cache_dnf_cli_commands_updateinfo
  import dnf.cli.commands.upgrade as cache_dnf_cli_commands_upgrade
  import dnf.cli.commands.upgradeto as cache_dnf_cli_commands_upgradeto
  import dnf.cli.demand as cache_dnf_cli_demand
  import dnf.cli.format as cache_dnf_cli_format
  import dnf.cli.main as cache_dnf_cli_main
  import dnf.cli.option_parser as cache_dnf_cli_option_parser
  import dnf.cli.output as cache_dnf_cli_output
  import dnf.cli.progress as cache_dnf_cli_progress
  import dnf.cli.term as cache_dnf_cli_term
  import dnf.cli.utils as cache_dnf_cli_utils
  import dnf.comps as cache_dnf_comps
  import dnf.conf as cache_dnf_conf
  import dnf.conf.parser as cache_dnf_conf_parser
  import dnf.conf.read as cache_dnf_conf_read
  import dnf.conf.substitutions as cache_dnf_conf_substitutions
  import dnf.const as cache_dnf_const
  import dnf.crypto as cache_dnf_crypto
  import dnf.drpm as cache_dnf_drpm
  import dnf.exceptions as cache_dnf_exceptions
  import dnf.goal as cache_dnf_goal
  import dnf.history as cache_dnf_history
  import dnf.i18n as cache_dnf_i18n
  import dnf.lock as cache_dnf_lock
  import dnf.logging as cache_dnf_logging
  import dnf.match_counter as cache_dnf_match_counter
  import dnf.package as cache_dnf_package
  import dnf.persistor as cache_dnf_persistor
  import dnf.plugin as cache_dnf_plugin
  import dnf.pycomp as cache_dnf_pycomp
  import dnf.query as cache_dnf_query
  import dnf.repo as cache_dnf_repo
  import dnf.repodict as cache_dnf_repodict
  import dnf.rpm as cache_dnf_rpm
  import dnf.rpm.connection as cache_dnf_rpm_connection
  import dnf.rpm.error as cache_dnf_rpm_error
  import dnf.rpm.miscutils as cache_dnf_rpm_miscutils
  import dnf.rpm.transaction as cache_dnf_rpm_transaction
  import dnf.sack as cache_dnf_sack
  import dnf.selector as cache_dnf_selector
  import dnf.subject as cache_dnf_subject
  import dnf.transaction as cache_dnf_transaction
  import dnf.util as cache_dnf_util
  import dnf.yum as cache_dnf_yum
  import dnf.yum.config as cache_dnf_yum_config
  import dnf.yum.history as cache_dnf_yum_history
  import dnf.yum.misc as cache_dnf_yum_misc
  import dnf.yum.packages as cache_dnf_yum_packages
  import dnf.yum.rpmsack as cache_dnf_yum_rpmsack
  import dnf.yum.rpmtrans as cache_dnf_yum_rpmtrans
  import dnf.yum.sqlutils as cache_dnf_yum_sqlutils
  import doctest as cache_doctest
  import dummy_thread as cache_dummy_thread
  import dummy_threading as cache_dummy_threading
  import email as cache_email
  import email.base64mime as cache_email_base64mime
  import email.charset as cache_email_charset
  import email.encoders as cache_email_encoders
  import email.errors as cache_email_errors
  import email.feedparser as cache_email_feedparser
  import email.generator as cache_email_generator
  import email.header as cache_email_header
  import email.iterators as cache_email_iterators
  import email.message as cache_email_message
  import email.mime as cache_email_mime
  import email.mime.base as cache_email_mime_base
  import email.mime.nonmultipart as cache_email_mime_nonmultipart
  import email.mime.text as cache_email_mime_text
  import email._parseaddr as cache_email__parseaddr
  import email.parser as cache_email_parser
  import email.quoprimime as cache_email_quoprimime
  import email.utils as cache_email_utils
  import encodings as cache_encodings
  import encodings.aliases as cache_encodings_aliases
  import errno as cache_errno
  import exceptions as cache_exceptions
  import fcntl as cache_fcntl
  import fnmatch as cache_fnmatch
  import ftplib as cache_ftplib
  import functools as cache_functools
  import _functools as cache__functools
  import __future__ as cache___future__
  import gc as cache_gc
  import genericpath as cache_genericpath
  import getopt as cache_getopt
  import getpass as cache_getpass
  import gettext as cache_gettext
  import glob as cache_glob
  import gpgme as cache_gpgme
  import gpgme.editutil as cache_gpgme_editutil
  import gpgme._gpgme as cache_gpgme__gpgme
  import grp as cache_grp
  import gzip as cache_gzip
  import hashlib as cache_hashlib
  import _hashlib as cache__hashlib
  import hawkey as cache_hawkey
  import hawkey._hawkey as cache_hawkey__hawkey
  import heapq as cache_heapq
  import _heapq as cache__heapq
  import httplib as cache_httplib
  import imp as cache_imp
  import importlib as cache_importlib
  import iniparse as cache_iniparse
  import iniparse.compat as cache_iniparse_compat
  import iniparse.config as cache_iniparse_config
  import iniparse.configparser as cache_iniparse_configparser
  import iniparse.ini as cache_iniparse_ini
  import iniparse.utils as cache_iniparse_utils
  import inspect as cache_inspect
  import io as cache_io
  import _io as cache__io
  import itertools as cache_itertools
  import json as cache_json
  import _json as cache__json
  import json.decoder as cache_json_decoder
  import json.encoder as cache_json_encoder
  import json.scanner as cache_json_scanner
  import keyword as cache_keyword
  import libcomps as cache_libcomps
  import libcomps._libpycomps as cache_libcomps__libpycomps
  import librepo as cache_librepo
  import librepo._librepo as cache_librepo__librepo
  import linecache as cache_linecache
  import locale as cache_locale
  import _locale as cache__locale
  import logging as cache_logging
  import lzma as cache_lzma
  import marshal as cache_marshal
  import math as cache_math
  import mimetools as cache_mimetools
  import mimetypes as cache_mimetypes
  import ntpath as cache_ntpath
  import nturl2path as cache_nturl2path
  import opcode as cache_opcode
  import operator as cache_operator
  import optparse as cache_optparse
  import os as cache_os
  import os2emxpath as cache_os2emxpath
  import _osx_support as cache__osx_support
  import pdb as cache_pdb
  import pickle as cache_pickle
  import posix as cache_posix
  import posixpath as cache_posixpath
  import pprint as cache_pprint
  import pwd as cache_pwd
  import py_compile as cache_py_compile
  import Queue as cache_Queue
  import quopri as cache_quopri
  import random as cache_random
  import _random as cache__random
  import re as cache_re
  import readline as cache_readline
  import repr as cache_repr
  import rfc822 as cache_rfc822
  import rpm as cache_rpm
  import rpm._rpm as cache_rpm__rpm
  import rpm._rpmb as cache_rpm__rpmb
  import rpm.transaction as cache_rpm_transaction
  import select as cache_select
  import shlex as cache_shlex
  import shutil as cache_shutil
  import signal as cache_signal
  import six as cache_six
  import socket as cache_socket
  import _socket as cache__socket
  import sqlite3 as cache_sqlite3
  import _sqlite3 as cache__sqlite3
  import sqlite3.dbapi2 as cache_sqlite3_dbapi2
  import _sre as cache__sre
  import sre_compile as cache_sre_compile
  import sre_constants as cache_sre_constants
  import sre_parse as cache_sre_parse
  import ssl as cache_ssl
  import _ssl as cache__ssl
  import stat as cache_stat
  import string as cache_string
  import StringIO as cache_StringIO
  import strop as cache_strop
  import struct as cache_struct
  import _struct as cache__struct
  import subprocess as cache_subprocess
  import sys as cache_sys
  import _sysconfigdata as cache__sysconfigdata
  import tarfile as cache_tarfile
  import tempfile as cache_tempfile
  import termios as cache_termios
  import textwrap as cache_textwrap
  import thread as cache_thread
  import threading as cache_threading
  import _threading_local as cache__threading_local
  import time as cache_time
  import token as cache_token
  import tokenize as cache_tokenize
  import traceback as cache_traceback
  import types as cache_types
  import unicodedata as cache_unicodedata
  import unittest as cache_unittest
  import unittest.case as cache_unittest_case
  import unittest.loader as cache_unittest_loader
  import unittest.main as cache_unittest_main
  import unittest.result as cache_unittest_result
  import unittest.runner as cache_unittest_runner
  import unittest.signals as cache_unittest_signals
  import unittest.suite as cache_unittest_suite
  import unittest.util as cache_unittest_util
  import urllib as cache_urllib
  import urlparse as cache_urlparse
  import UserDict as cache_UserDict
  import uu as cache_uu
  import warnings as cache_warnings
  import _warnings as cache__warnings
  import weakref as cache_weakref
  import _weakref as cache__weakref
  import _weakrefset as cache__weakrefset
  import zipfile as cache_zipfile
  import zlib as cache_zlib
  cached = [cache_ConfigParser, cache_Queue, cache_StringIO, cache_UserDict,
 	     cache___future__, cache__abcoll, cache__codecs, cache__collections,
            cache__curses, cache__functools, cache__hashlib, cache__heapq, cache__io,
            cache__json, cache__locale, cache__osx_support, cache__random,
            cache__socket, cache__sqlite3, cache__sre, cache__ssl, cache__struct,
            cache__sysconfigdata, cache__threading_local, cache__warnings,
            cache__weakref, cache__weakrefset, cache_abc, cache_argparse,
            cache_array, cache_atexit, cache_base64, cache_bdb, cache_binascii, cache_bz2,
            cache_cPickle, cache_cStringIO, cache_calendar, cache_cmd, cache_codecs,
            cache_collections, cache_contextlib, cache_copy, cache_copy_reg, cache_curses,
            cache_curses_has_key, cache_curses_wrapper, cache_datetime, cache_difflib,
            cache_dis, cache_distutils, cache_distutils_debug, cache_distutils_errors,
            cache_distutils_log, cache_distutils_spawn, cache_distutils_sysconfig,
            cache_distutils_text_file, cache_distutils_version, cache_dnf, cache_dnf_arch,
            cache_dnf_base, cache_dnf_callback, cache_dnf_cli, cache_dnf_cli_cli,
            cache_dnf_cli_commands, cache_dnf_cli_commands_autoremove, cache_dnf_cli_commands_clean,
            cache_dnf_cli_commands_distrosync, cache_dnf_cli_commands_downgrade,
            cache_dnf_cli_commands_group, cache_dnf_cli_commands_install, cache_dnf_cli_commands_makecache,
            cache_dnf_cli_commands_mark, cache_dnf_cli_commands_reinstall, cache_dnf_cli_commands_remove,
            cache_dnf_cli_commands_repolist, cache_dnf_cli_commands_search, cache_dnf_cli_commands_updateinfo,
            cache_dnf_cli_commands_upgrade, cache_dnf_cli_commands_upgradeto, cache_dnf_cli_demand,
            cache_dnf_cli_format, cache_dnf_cli_main, cache_dnf_cli_option_parser, cache_dnf_cli_output,
            cache_dnf_cli_progress, cache_dnf_cli_term, cache_dnf_cli_utils, cache_dnf_comps, cache_dnf_conf,
            cache_dnf_conf_parser, cache_dnf_conf_read, cache_dnf_conf_substitutions, cache_dnf_const,
	     cache_dnf_crypto, cache_dnf_drpm, cache_dnf_exceptions, cache_dnf_goal, cache_dnf_history,
	     cache_dnf_i18n, cache_dnf_lock, cache_dnf_logging, cache_dnf_match_counter, cache_dnf_package,
	     cache_dnf_persistor, cache_dnf_plugin, cache_dnf_pycomp, cache_dnf_query, cache_dnf_repo,
            cache_dnf_repodict, cache_dnf_rpm, cache_dnf_rpm_connection, cache_dnf_rpm_error, cache_dnf_rpm_miscutils,
            cache_dnf_rpm_transaction, cache_dnf_sack, cache_dnf_selector, cache_dnf_subject, cache_dnf_transaction,
            cache_dnf_util, cache_dnf_yum, cache_dnf_yum_config, cache_dnf_yum_history, cache_dnf_yum_misc,
            cache_dnf_yum_packages, cache_dnf_yum_rpmsack, cache_dnf_yum_rpmtrans, cache_dnf_yum_sqlutils, cache_doctest,
            cache_dummy_thread, cache_dummy_threading, cache_email, cache_email__parseaddr, cache_email_base64mime,
            cache_email_charset, cache_email_encoders, cache_email_errors, cache_email_feedparser, cache_email_generator,
            cache_email_header, cache_email_iterators, cache_email_message, cache_email_mime, cache_email_mime_base,
            cache_email_mime_nonmultipart, cache_email_mime_text, cache_email_parser, cache_email_quoprimime, cache_email_utils,
            cache_encodings, cache_encodings_aliases, cache_errno, cache_exceptions, cache_fcntl,
            cache_fnmatch, cache_ftplib, cache_functools, cache_gc, cache_genericpath,
            cache_getopt, cache_getpass, cache_gettext, cache_glob, cache_gpgme,
            cache_gpgme__gpgme, cache_gpgme_editutil, cache_grp, cache_gzip, cache_hashlib,
            cache_hawkey, cache_hawkey__hawkey, cache_heapq, cache_httplib, cache_imp,
            cache_importlib, cache_iniparse, cache_iniparse_compat, cache_iniparse_config, cache_iniparse_configparser,
            cache_iniparse_ini, cache_iniparse_utils, cache_inspect, cache_io, cache_itertools,
            cache_json, cache_json_decoder, cache_json_encoder, cache_json_scanner, cache_keyword,
            cache_libcomps, cache_libcomps__libpycomps, cache_librepo, cache_librepo__librepo, cache_linecache,
            cache_locale, cache_logging, cache_lzma, cache_marshal, cache_math,
            cache_mimetools, cache_mimetypes, cache_ntpath, cache_nturl2path, cache_opcode,
            cache_operator, cache_optparse, cache_os, cache_os2emxpath, cache_pdb,
            cache_pickle, cache_posix, cache_posixpath, cache_pprint, cache_pwd,
            cache_py_compile, cache_quopri, cache_random, cache_re, cache_readline,
            cache_repr, cache_rfc822, cache_rpm, cache_rpm__rpmb,
            cache_rpm__rpm, cache_rpm_transaction, cache_select, cache_shlex, cache_shutil,
            cache_signal, cache_six, cache_socket, cache_sqlite3, cache_sqlite3_dbapi2,
            cache_sre_compile, cache_sre_constants, cache_sre_parse, cache_ssl, cache_stat,
            cache_string, cache_strop, cache_struct, cache_subprocess, cache_sys,
            cache_tarfile, cache_tempfile, cache_termios, cache_textwrap, cache_thread,
            cache_threading, cache_time, cache_token, cache_tokenize, cache_traceback,
            cache_types, cache_unicodedata, cache_unittest, cache_unittest_case, cache_unittest_loader,
            cache_unittest_main, cache_unittest_result, cache_unittest_runner, cache_unittest_signals, cache_unittest_suite,
            cache_unittest_util, cache_urllib, cache_urlparse, cache_uu, cache_warnings,
            cache_weakref, cache_zipfile, cache_zlib]
  return cached

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
    nss = '/proc/{0}/ns'.format(self.pid)
    for ns in os.listdir(nss):
      if ns == 'user':
        continue
      if ns == 'pid':
        self.pid_ns = open(os.path.join(nss, ns))
      nsdesc.append(open(os.path.join(nss, ns)))
    # chroot into the container
    os.chroot('/proc/{0}/root/'.format(self.pid))
    os.chdir('/')
    for ns in nsdesc:
      # join namespace and close fd
      if libc.setns(ns.fileno(), 0) != 0:
        print('[-] error entering: {0}'.format(ns.name))
      ns.close()
    # fork and exit the parent so that we're in the same PID namespace
    '''npid = os.fork()
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
      return True'''
    return True

  def _load_data(self):
    print('[*] loading from PID: {0}'.format(os.getpid()))
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
      self.cached = _cache_python()
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

    assert libc.setns(self.pid_ns, 0) == 0
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
      print('[*] executing child (transaction): {0}'.format(os.getpid()))
      self.base.do_transaction()

      return True
