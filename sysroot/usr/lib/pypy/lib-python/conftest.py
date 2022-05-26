"""

test configuration(s) for running CPython's regression
test suite on top of PyPy

"""
import py
import pytest
import sys
import re
import pypy
from pypy.interpreter.gateway import ApplevelClass
from pypy.interpreter.error import OperationError
from pypy.interpreter.module import Module as PyPyModule
from pypy.interpreter.main import run_string, run_file

# the following adds command line options as a side effect!
from pypy.conftest import option as pypy_option

from pypy.tool.pytest import appsupport
from pypy.tool.pytest.confpath import pypydir, testdir, testresultdir
from rpython.config.parse import parse_info

pytest_plugins = "resultlog",
rsyncdirs = ['.', '../pypy/']

#
# Interfacing/Integrating with py.test's collection process
#

def pytest_addoption(parser):
    group = parser.getgroup("complicance testing options")
    group.addoption('-T', '--timeout', action="store", type="string",
                    default="1000", dest="timeout",
                    help="fail a test module after the given timeout. "
                         "specify in seconds or 'NUMmp' aka Mega-Pystones")
    group.addoption('--pypy', action="store", type="string", dest="pypy",
                    help="use given pypy executable to run lib-python tests. "
                         "This will run the tests directly (i.e. not through py.py)")
    group.addoption('--filter', action="store", type="string", default=None,
                    dest="unittest_filter", help="Similar to -k, XXX")

def gettimeout(timeout):
    from rpython.translator.test import rpystone
    if timeout.endswith('mp'):
        megapystone = float(timeout[:-2])
        t, stone = pystone.Proc0(10000)
        pystonetime = t/stone
        seconds = megapystone * 1000000 * pystonetime
        return seconds
    return float(timeout)

# ________________________________________________________________________
#
# classification of all tests files (this is ongoing work)
#

class RegrTest:
    """ Regression Test Declaration."""
    def __init__(self, basename, core=False, compiler=None, usemodules='',
                 skip=None):
        self.basename = basename
        self._usemodules = usemodules.split() + ['signal', 'time', 'itertools', '_socket']
        self._compiler = compiler
        self.core = core
        self.skip = skip
        assert self.getfspath().check(), "%r not found!" % (basename,)

    def usemodules(self):
        return self._usemodules  # + pypy_option.usemodules
    usemodules = property(usemodules)

    def compiler(self):
        return self._compiler  # or pypy_option.compiler
    compiler = property(compiler)

    def ismodified(self):
        #XXX: ask hg
        return None

    def getfspath(self):
        return testdir.join(self.basename)

    def run_file(self, space):
        fspath = self.getfspath()
        assert fspath.check()
        modname = fspath.purebasename
        space.appexec([], '''():
            from test import %(modname)s
            m = %(modname)s
            if hasattr(m, 'test_main'):
                m.test_main()
        ''' % locals())

testmap = [
    RegrTest('test___all__.py', core=True),
    RegrTest('test___future__.py', core=True),
    RegrTest('test__locale.py', usemodules='_locale'),
    RegrTest('test__osx_support.py'),
    RegrTest('test_abc.py'),
    RegrTest('test_abstract_numbers.py'),
    RegrTest('test_aepack.py'),
    RegrTest('test_aifc.py'),
    RegrTest('test_al.py'),
    RegrTest('test_anydbm.py', usemodules='struct'),
    RegrTest('test_applesingle.py'),
    RegrTest('test_argparse.py', usemodules='binascii'),
    RegrTest('test_array.py', core=True, usemodules='struct array binascii'),
    RegrTest('test_ascii_formatd.py'),
    RegrTest('test_ast.py', core=True, usemodules='struct'),
    RegrTest('test_asynchat.py', usemodules='select fcntl'),
    RegrTest('test_asyncore.py', usemodules='select fcntl'),
    RegrTest('test_atexit.py', core=True),
    RegrTest('test_audioop.py'),
    RegrTest('test_augassign.py', core=True),
    RegrTest('test_base64.py', usemodules='struct'),
    RegrTest('test_bastion.py'),
    RegrTest('test_bdb.py', usemodules='bdb'),
    RegrTest('test_bigaddrspace.py'),
    RegrTest('test_bigmem.py'),
    RegrTest('test_binascii.py', usemodules='binascii'),
    RegrTest('test_binhex.py'),
    RegrTest('test_binop.py', core=True),
    RegrTest('test_bisect.py', core=True, usemodules='_bisect'),
    RegrTest('test_bool.py', core=True),
    RegrTest('test_bsddb.py'),
    RegrTest('test_bsddb185.py'),
    RegrTest('test_bsddb3.py'),
    RegrTest('test_buffer.py'),
    RegrTest('test_bufio.py', core=True),
    RegrTest('test_builtin.py', core=True, usemodules='binascii'),
    RegrTest('test_bytes.py', usemodules='struct binascii'),
    RegrTest('test_bz2.py', usemodules='bz2'),
    RegrTest('test_calendar.py'),
    RegrTest('test_call.py', core=True),
    RegrTest('test_capi.py', usemodules='cpyext'),
    RegrTest('test_cd.py'),
    RegrTest('test_cfgparser.py'),
    RegrTest('test_cgi.py'),
    RegrTest('test_charmapcodec.py', core=True),
    RegrTest('test_cl.py'),
    RegrTest('test_class.py', core=True),
    RegrTest('test_cmath.py', core=True),
    RegrTest('test_cmd.py'),
    RegrTest('test_cmd_line.py'),
    RegrTest('test_cmd_line_script.py'),
    RegrTest('test_code.py', core=True),
    RegrTest('test_codeccallbacks.py', core=True),
    RegrTest('test_codecencodings_cn.py', usemodules='_multibytecodec'),
    RegrTest('test_codecencodings_hk.py', usemodules='_multibytecodec'),
    RegrTest('test_codecencodings_iso2022.py', usemodules='_multibytecodec'),
    RegrTest('test_codecencodings_jp.py', usemodules='_multibytecodec'),
    RegrTest('test_codecencodings_kr.py', usemodules='_multibytecodec'),
    RegrTest('test_codecencodings_tw.py', usemodules='_multibytecodec'),
    RegrTest('test_codecmaps_cn.py', usemodules='_multibytecodec'),
    RegrTest('test_codecmaps_hk.py', usemodules='_multibytecodec'),
    RegrTest('test_codecmaps_jp.py', usemodules='_multibytecodec'),
    RegrTest('test_codecmaps_kr.py', usemodules='_multibytecodec'),
    RegrTest('test_codecmaps_tw.py', usemodules='_multibytecodec'),
    RegrTest('test_codecs.py', core=True, usemodules='_multibytecodec'),
    RegrTest('test_codeop.py', core=True),
    RegrTest('test_coercion.py', core=True, usemodules='struct'),
    RegrTest('test_collections.py', usemodules='binascii struct'),
    RegrTest('test_colorsys.py'),
    RegrTest('test_commands.py'),
    RegrTest('test_compare.py', core=True),
    RegrTest('test_compile.py', core=True),
    RegrTest('test_compileall.py'),
    RegrTest('test_compiler.py', core=False, skip="slowly deprecating compiler"),
    RegrTest('test_complex.py', core=True),
    RegrTest('test_complex_args.py'),
    RegrTest('test_contains.py', core=True),
    RegrTest('test_contextlib.py', usemodules="thread"),
    RegrTest('test_cookie.py'),
    RegrTest('test_cookielib.py'),
    RegrTest('test_copy.py', core=True),
    RegrTest('test_copy_reg.py', core=True),
    RegrTest('test_cpickle.py', core=True),
    RegrTest('test_cprofile.py'),
    RegrTest('test_crypt.py'),
    RegrTest('test_csv.py', usemodules='_csv'),
    RegrTest('test_ctypes.py', usemodules="_rawffi thread cpyext"),
    RegrTest('test_curses.py'),
    RegrTest('test_datetime.py', usemodules='binascii struct'),
    RegrTest('test_dbm.py'),
    RegrTest('test_decimal.py'),
    RegrTest('test_decorators.py', core=True),
    RegrTest('test_defaultdict.py', usemodules='_collections'),
    RegrTest('test_deque.py', core=True, usemodules='_collections'),
    RegrTest('test_descr.py', core=True, usemodules='_weakref'),
    RegrTest('test_descrtut.py', core=True),
    RegrTest('test_dict.py', core=True),
    RegrTest('test_dictcomps.py', core=True),
    RegrTest('test_dictviews.py', core=True),
    RegrTest('test_difflib.py'),
    RegrTest('test_dircache.py', core=True),
    RegrTest('test_dis.py'),
    RegrTest('test_distutils.py', skip=True),
    RegrTest('test_dl.py'),
    RegrTest('test_doctest.py', usemodules="thread"),
    RegrTest('test_doctest2.py'),
    RegrTest('test_docxmlrpc.py'),
    RegrTest('test_dumbdbm.py'),
    RegrTest('test_dummy_thread.py', core=True),
    RegrTest('test_dummy_threading.py', core=True),
    RegrTest('test_email.py'),
    RegrTest('test_email_codecs.py'),
    RegrTest('test_email_renamed.py'),
    RegrTest('test_ensurepip.py'),
    RegrTest('test_enumerate.py', core=True),
    RegrTest('test_eof.py', core=True),
    RegrTest('test_epoll.py'),
    RegrTest('test_errno.py', usemodules="errno"),
    RegrTest('test_exception_variations.py'),
    RegrTest('test_exceptions.py', core=True),
    RegrTest('test_extcall.py', core=True),
    RegrTest('test_fcntl.py', usemodules='fcntl'),
    RegrTest('test_file.py', usemodules="posix", core=True),
    RegrTest('test_file2k.py', usemodules="posix", core=True),
    RegrTest('test_file_eintr.py'),
    RegrTest('test_filecmp.py', core=True),
    RegrTest('test_fileinput.py', core=True),
    RegrTest('test_fileio.py'),
    RegrTest('test_float.py', core=True),
    RegrTest('test_fnmatch.py', core=True),
    RegrTest('test_fork1.py', usemodules="thread"),
    RegrTest('test_format.py', core=True),
    RegrTest('test_fpformat.py', core=True),
    RegrTest('test_fractions.py'),
    RegrTest('test_frozen.py', skip="unsupported extension module"),
    RegrTest('test_ftplib.py'),
    RegrTest('test_funcattrs.py', core=True),
    RegrTest('test_functools.py'),
    RegrTest('test_future.py', core=True),
    RegrTest('test_future1.py', core=True),
    RegrTest('test_future2.py', core=True),
    RegrTest('test_future3.py', core=True),
    RegrTest('test_future4.py', core=True),
    RegrTest('test_future5.py', core=True),
    RegrTest('test_future_builtins.py'),
    RegrTest('test_gc.py', usemodules='_weakref', skip="implementation detail"),
    RegrTest('test_gdb.py', skip="not applicable"),
    RegrTest('test_gdbm.py'),
    RegrTest('test_generators.py', core=True, usemodules='thread _weakref'),
    RegrTest('test_genericpath.py'),
    RegrTest('test_genexps.py', core=True, usemodules='_weakref'),
    RegrTest('test_getargs.py'),
    RegrTest('test_getargs2.py', usemodules='binascii', skip=True),
    RegrTest('test_getopt.py', core=True),
    RegrTest('test_gettext.py'),
    RegrTest('test_gl.py'),
    RegrTest('test_glob.py', core=True),
    RegrTest('test_global.py', core=True),
    RegrTest('test_grammar.py', core=True),
    RegrTest('test_grp.py'),
    RegrTest('test_gzip.py', usemodules='zlib'),
    RegrTest('test_hash.py', core=True),
    RegrTest('test_hashlib.py', core=True),
    RegrTest('test_heapq.py', core=True),
    RegrTest('test_hmac.py'),
    RegrTest('test_hotshot.py', skip="unsupported extension module"),
    RegrTest('test_htmllib.py'),
    RegrTest('test_htmlparser.py'),
    RegrTest('test_httplib.py'),
    RegrTest('test_httpservers.py'),
    RegrTest('test_idle.py'),
    RegrTest('test_imageop.py'),
    RegrTest('test_imaplib.py'),
    RegrTest('test_imgfile.py'),
    RegrTest('test_imghdr.py'),
    RegrTest('test_imp.py', core=True, usemodules='thread'),
    RegrTest('test_import.py', core=True),
    RegrTest('test_importhooks.py', core=True),
    RegrTest('test_importlib.py'),
    RegrTest('test_import_magic.py'),
    RegrTest('test_index.py'),
    RegrTest('test_inspect.py'),
    RegrTest('test_int.py', core=True),
    RegrTest('test_int_literal.py', core=True),
    RegrTest('test_io.py', usemodules='array binascii'),
    RegrTest('test_ioctl.py'),
    RegrTest('test_isinstance.py', core=True),
    RegrTest('test_iter.py', core=True),
    RegrTest('test_iterlen.py', core=True, usemodules="_collections itertools"),
    RegrTest('test_itertools.py', core=True, usemodules="itertools struct"),
    RegrTest('test_json.py'),
    RegrTest('test_kqueue.py'),
    RegrTest('test_largefile.py'),
    RegrTest('test_lib2to3.py'),
    RegrTest('test_linecache.py'),
    RegrTest('test_linuxaudiodev.py', skip="unsupported extension module"),
    RegrTest('test_list.py', core=True),
    RegrTest('test_locale.py', usemodules="_locale"),
    RegrTest('test_logging.py', usemodules='thread'),
    RegrTest('test_long.py', core=True),
    RegrTest('test_long_future.py', core=True),
    RegrTest('test_longexp.py', core=True),
    RegrTest('test_macos.py'),
    RegrTest('test_macostools.py'),
    RegrTest('test_macpath.py'),
    RegrTest('test_macurl2path.py'),
    RegrTest('test_mailbox.py'),
    RegrTest('test_marshal.py', core=True),
    RegrTest('test_math.py', core=True, usemodules='math'),
    RegrTest('test_memoryio.py'),
    RegrTest('test_memoryview.py'),
    RegrTest('test_md5.py'),
    RegrTest('test_mhlib.py', usemodules='binascii struct'),
    RegrTest('test_mimetools.py'),
    RegrTest('test_mimetypes.py'),
    RegrTest('test_MimeWriter.py', core=False, usemodules='binascii'),
    RegrTest('test_minidom.py'),
    RegrTest('test_mmap.py', usemodules="mmap"),
    RegrTest('test_module.py', core=True),
    RegrTest('test_modulefinder.py'),
    RegrTest('test_msilib.py'),
    RegrTest('test_multibytecodec.py', usemodules='_multibytecodec'),
    RegrTest('test_multifile.py'),
    RegrTest('test_multiprocessing.py'),
    RegrTest('test_mutants.py', core="possibly"),
    RegrTest('test_mutex.py'),
    RegrTest('test_netrc.py'),
    RegrTest('test_new.py', core=True),
    RegrTest('test_nis.py'),
    RegrTest('test_normalization.py'),
    RegrTest('test_nntplib.py'),
    RegrTest('test_ntpath.py'),
    RegrTest('test_old_mailbox.py'),
    RegrTest('test_opcodes.py', core=True),
    RegrTest('test_openpty.py'),
    RegrTest('test_operator.py', core=True),
    RegrTest('test_optparse.py'),
    RegrTest('test_ordered_dict.py'),
    RegrTest('test_os.py', core=True),
    RegrTest('test_ossaudiodev.py'),
    RegrTest('test_parser.py', skip="slowly deprecating compiler"),
    RegrTest('test_pdb.py'),
    RegrTest('test_peepholer.py'),
    RegrTest('test_pep247.py'),
    RegrTest('test_pep277.py'),
    RegrTest('test_pep352.py'),
    RegrTest('test_pickle.py', core=True),
    RegrTest('test_pickletools.py', core=False),
    RegrTest('test_pipes.py'),
    RegrTest('test_pkg.py', core=True),
    RegrTest('test_pkgimport.py', core=True),
    RegrTest('test_pkgutil.py'),
    RegrTest('test_platform.py'),
    RegrTest('test_plistlib.py'),
    RegrTest('test_poll.py'),
    RegrTest('test_popen.py'),
    RegrTest('test_popen2.py'),
    RegrTest('test_poplib.py'),
    RegrTest('test_posix.py', usemodules="_rawffi"),
    RegrTest('test_posixpath.py'),
    RegrTest('test_pow.py', core=True),
    RegrTest('test_pprint.py', core=True),
    RegrTest('test_print.py', core=True),
    RegrTest('test_profile.py'),
    RegrTest('test_property.py', core=True),
    RegrTest('test_pstats.py'),
    RegrTest('test_pty.py', usemodules='fcntl termios select'),
    RegrTest('test_pwd.py', usemodules="pwd"),
    RegrTest('test_py3kwarn.py'),
    RegrTest('test_py_compile.py'),
    RegrTest('test_pyclbr.py'),
    RegrTest('test_pydoc.py'),
    RegrTest('test_pyexpat.py'),
    RegrTest('test_queue.py', usemodules='thread'),
    RegrTest('test_quopri.py'),
    RegrTest('test_random.py'),
    RegrTest('test_re.py', core=True),
    RegrTest('test_readline.py'),
    RegrTest('test_regrtest.py'),
    RegrTest('test_repr.py', core=True),
    RegrTest('test_resource.py'),
    RegrTest('test_rfc822.py'),
    RegrTest('test_richcmp.py', core=True),
    RegrTest('test_rlcompleter.py'),
    RegrTest('test_robotparser.py'),
    RegrTest('test_runpy.py'),
    RegrTest('test_sax.py'),
    RegrTest('test_scope.py', core=True),
    RegrTest('test_scriptpackages.py'),
    RegrTest('test_select.py'),
    RegrTest('test_set.py', core=True),
    RegrTest('test_sets.py'),
    RegrTest('test_setcomps.py', core=True),
    RegrTest('test_sgmllib.py'),
    RegrTest('test_sha.py'),
    RegrTest('test_shelve.py'),
    RegrTest('test_shlex.py'),
    RegrTest('test_shutil.py'),
    RegrTest('test_signal.py'),
    RegrTest('test_SimpleHTTPServer.py', usemodules='binascii'),
    RegrTest('test_site.py', core=False),
    RegrTest('test_slice.py', core=True),
    RegrTest('test_smtplib.py'),
    RegrTest('test_smtpnet.py'),
    RegrTest('test_socket.py', usemodules='thread _weakref'),
    RegrTest('test_socketserver.py', usemodules='thread'),
    RegrTest('test_softspace.py', core=True),
    RegrTest('test_sort.py', core=True),
    RegrTest('test_source_encoding.py'),
    RegrTest('test_spwd.py'),
    RegrTest('test_sqlite.py', usemodules="thread _rawffi zlib"),
    RegrTest('test_ssl.py', usemodules='_socket select'),
    RegrTest('test_startfile.py'),
    RegrTest('test_stat.py'),
    RegrTest('test_str.py', core=True),
    RegrTest('test_strftime.py'),
    RegrTest('test_string.py', core=True),
    RegrTest('test_StringIO.py', core=True, usemodules='cStringIO array'),
    RegrTest('test_stringprep.py'),
    RegrTest('test_strop.py', skip="deprecated"),
    RegrTest('test_strptime.py'),
    RegrTest('test_strtod.py'),
    RegrTest('test_struct.py', usemodules='struct'),
    RegrTest('test_structmembers.py', skip="CPython specific"),
    RegrTest('test_structseq.py'),
    RegrTest('test_subprocess.py', usemodules='signal'),
    RegrTest('test_sunau.py'),
    RegrTest('test_sunaudiodev.py'),
    RegrTest('test_sundry.py'),
    RegrTest('test_symtable.py', skip="implementation detail"),
    RegrTest('test_syntax.py', core=True),
    RegrTest('test_sys.py', core=True, usemodules='struct'),
    RegrTest('test_sys_setprofile.py', core=True),
    RegrTest('test_sys_settrace.py', core=True),
    RegrTest('test_sysconfig.py'),
    RegrTest('test_tarfile.py'),
    RegrTest('test_tcl.py'),
    RegrTest('test_telnetlib.py'),
    RegrTest('test_tempfile.py'),
    RegrTest('test_test_support.py'),
    RegrTest('test_textwrap.py'),
    RegrTest('test_thread.py', usemodules="thread", core=True),
    RegrTest('test_threaded_import.py', usemodules="thread", core=True),
    RegrTest('test_threadedtempfile.py',
             usemodules="thread", core=False),
    RegrTest('test_threading.py', usemodules="thread", core=True),
    RegrTest('test_threading_local.py', usemodules="thread", core=True),
    RegrTest('test_threadsignals.py', usemodules="thread"),
    RegrTest('test_time.py', core=True),
    RegrTest('test_timeit.py'),
    RegrTest('test_timeout.py'),
    RegrTest('test_tk.py'),
    RegrTest('test_tokenize.py'),
    RegrTest('test_tools.py'),
    RegrTest('test_trace.py'),
    RegrTest('test_traceback.py', core=True),
    RegrTest('test_transformer.py', core=True),
    RegrTest('test_ttk_guionly.py'),
    RegrTest('test_ttk_textonly.py'),
    RegrTest('test_tuple.py', core=True),
    RegrTest('test_turtle.py'),
    RegrTest('test_typechecks.py'),
    RegrTest('test_types.py', core=True),
    RegrTest('test_ucn.py'),
    RegrTest('test_unary.py', core=True),
    RegrTest('test_undocumented_details.py'),
    RegrTest('test_unicode.py', core=True),
    RegrTest('test_unicode_file.py'),
    RegrTest('test_unicodedata.py'),
    RegrTest('test_unittest.py', core=True),
    RegrTest('test_univnewlines.py'),
    RegrTest('test_univnewlines2k.py', core=True),
    RegrTest('test_unpack.py', core=True),
    RegrTest('test_urllib.py'),
    RegrTest('test_urllib2.py'),
    RegrTest('test_urllib2_localnet.py', usemodules="thread"),
    RegrTest('test_urllib2net.py'),
    RegrTest('test_urllibnet.py'),
    RegrTest('test_urlparse.py'),
    RegrTest('test_userdict.py', core=True),
    RegrTest('test_userlist.py', core=True),
    RegrTest('test_userstring.py', core=True),
    RegrTest('test_uu.py'),
    RegrTest('test_uuid.py'),
    RegrTest('test_wait3.py', usemodules="thread"),
    RegrTest('test_wait4.py', usemodules="thread"),
    RegrTest('test_warnings.py', core=True),
    RegrTest('test_wave.py'),
    RegrTest('test_weakref.py', core=True, usemodules='_weakref'),
    RegrTest('test_weakset.py'),
    RegrTest('test_whichdb.py'),
    RegrTest('test_winreg.py'),
    RegrTest('test_winsound.py'),
    RegrTest('test_with.py'),
    RegrTest('test_wsgiref.py'),
    RegrTest('test_xdrlib.py'),
    RegrTest('test_xml_etree.py'),
    RegrTest('test_xml_etree_c.py'),
    RegrTest('test_xmllib.py'),
    RegrTest('test_xmlrpc.py'),
    RegrTest('test_xpickle.py'),
    RegrTest('test_xrange.py', core=True),
    RegrTest('test_zipfile.py'),
    RegrTest('test_zipfile64.py'),
    RegrTest('test_zipimport.py', usemodules='zlib zipimport'),
    RegrTest('test_zipimport_support.py', usemodules='zlib zipimport'),
    RegrTest('test_zlib.py', usemodules='zlib'),
]

def check_testmap_complete():
    listed_names = dict.fromkeys([regrtest.basename for regrtest in testmap])
    assert len(listed_names) == len(testmap)
    # names to ignore
    listed_names['test_support.py'] = True
    listed_names['test_multibytecodec_support.py'] = True
    missing = []
    for path in testdir.listdir(fil='test_*.py'):
        name = path.basename
        if name not in listed_names:
            missing.append('    RegrTest(%r),' % (name,))
    missing.sort()
    assert not missing, "non-listed tests:\n%s" % ('\n'.join(missing),)
check_testmap_complete()

def pytest_configure(config):
    config._basename2spec = cache = {}
    for x in testmap:
        cache[x.basename] = x

def pytest_ignore_collect(path, config):
    if path.isfile():
        regrtest = config._basename2spec.get(path.basename, None)
        if regrtest is None or path.dirpath() != testdir:
            return True

@pytest.hookimpl(tryfirst=True)
def pytest_pycollect_makemodule(path, parent):
    config = parent.config
    regrtest = config._basename2spec[path.basename]
    return RunFileExternal(path.basename, parent=parent, regrtest=regrtest)

class RunFileExternal(py.test.collect.File):
    def __init__(self, name, parent, regrtest):
        super(RunFileExternal, self).__init__(name, parent)
        self.regrtest = regrtest
        self.fspath = regrtest.getfspath()

    def collect(self):
        if self.regrtest.ismodified():
            name = 'modified'
        else:
            name = 'unmodified'
        return [ReallyRunFileExternal(name, parent=self)]

#
# testmethod:
# invoking in a separate process: py.py TESTFILE
#
import os

class ReallyRunFileExternal(py.test.collect.Item):
    class ExternalFailure(Exception):
        """Failure in running subprocess"""

    def getinvocation(self, regrtest):
        fspath = regrtest.getfspath()
        python = sys.executable
        pypy_script = pypydir.join('bin', 'pyinteractive.py')
        alarm_script = pypydir.join('tool', 'alarm.py')
        if sys.platform == 'win32':
            watchdog_name = 'watchdog_nt.py'
        else:
            watchdog_name = 'watchdog.py'
        watchdog_script = pypydir.join('tool', watchdog_name)

        regr_script = pypydir.join('tool', 'pytest',
                                   'run-script', 'regrverbose.py')

        regrrun = str(regr_script)
        option = self.config.option
        TIMEOUT = gettimeout(option.timeout.lower())
        if option.pypy:
            execpath = py.path.local(option.pypy)
            if not execpath.check():
                execpath = py.path.local.sysfind(option.pypy)
            if not execpath:
                raise LookupError("could not find executable %r" % option.pypy)

            # check modules
            info = py.process.cmdexec("%s --info" % execpath)
            info = parse_info(info)
            for mod in regrtest.usemodules:
                if info.get('objspace.usemodules.%s' % mod) is not True:
                    py.test.skip("%s module not included in %s" % (mod,
                                                                   execpath))

            cmd = "%s %s %s" % (execpath, regrrun, fspath.purebasename)
            # add watchdog for timing out
            cmd = "%s %s %s %s" % (python, watchdog_script, TIMEOUT, cmd)
        else:
            pypy_options = []
            pypy_options.extend(
                ['--withmod-%s' % mod for mod in regrtest.usemodules])
            sopt = " ".join(pypy_options)
            cmd = "%s %s %d %s -S %s %s %s -v" % (
                python, alarm_script, TIMEOUT,
                pypy_script, sopt,
                regrrun, fspath.purebasename)
        return cmd

    def runtest(self):
        """ invoke a subprocess running the test file via PyPy.
            record its output into the 'result/user@host' subdirectory.
            (we might want to create subdirectories for
            each user, because we will probably all produce
            such result runs and they will not be the same
            i am afraid.
        """
        regrtest = self.parent.regrtest
        if regrtest.skip:
            if regrtest.skip is True:
                msg = "obsolete or unsupported platform"
            else:
                msg = regrtest.skip
            py.test.skip(msg)
        (skipped, exit_status, test_stdout, test_stderr) = \
            self.getresult(regrtest)
        if skipped:
            py.test.skip(test_stderr.splitlines()[-1])
        if exit_status:
            raise self.ExternalFailure(test_stdout, test_stderr)

    def repr_failure(self, excinfo):
        if not excinfo.errisinstance(self.ExternalFailure):
            return super(ReallyRunFileExternal, self).repr_failure(excinfo)
        out, err = excinfo.value.args
        return out + err

    def getstatusouterr(self, cmd):
        tempdir = py.test.ensuretemp(self.fspath.basename)
        stdout = tempdir.join(self.fspath.basename) + '.out'
        stderr = tempdir.join(self.fspath.basename) + '.err'
        if sys.platform == 'win32':
            status = os.system("%s >%s 2>%s" % (cmd, stdout, stderr))
            if status >= 0:
                status = status
            else:
                status = 'abnormal termination 0x%x' % status
        else:
            if self.config.option.unittest_filter is not None:
                cmd += ' --filter %s' % self.config.option.unittest_filter
            if self.config.option.usepdb:
                cmd += ' --pdb'
            if self.config.option.capture == 'no':
                status = os.system(cmd)
                stdout.write('')
                stderr.write('')
            else:
                status = os.system("%s >>%s 2>>%s" % (cmd, stdout, stderr))
            if os.WIFEXITED(status):
                status = os.WEXITSTATUS(status)
            else:
                status = 'abnormal termination 0x%x' % status
        return status, stdout.read(mode='rU'), stderr.read(mode='rU')

    def getresult(self, regrtest):
        cmd = self.getinvocation(regrtest)
        tempdir = py.test.ensuretemp(self.fspath.basename)
        oldcwd = tempdir.chdir()
        exit_status, test_stdout, test_stderr = self.getstatusouterr(cmd)
        oldcwd.chdir()
        skipped = False
        timedout = test_stderr.rfind(26*"=" + "timedout" + 26*"=") != -1
        if not timedout:
            timedout = test_stderr.rfind("KeyboardInterrupt") != -1
        if test_stderr.rfind(26*"=" + "skipped" + 26*"=") != -1:
            skipped = True
        if not exit_status:
            # match "FAIL" but not e.g. "FAILURE", which is in the output of a
            # test in test_zipimport_support.py
            if re.search(r'\bFAIL\b', test_stdout) or re.search('[^:]ERROR', test_stderr):
                exit_status = 2

        return skipped, exit_status, test_stdout, test_stderr

    def _keywords(self):
        lst = list(py.test.collect.Item._keywords(self))
        regrtest = self.parent.regrtest
        if regrtest.core:
            lst.append('core')
        return lst
