require '_h2ph_pre.ph';

no warnings qw(redefine misc);

if(defined(&_LIBC)) {
    die("Applications\ may\ not\ define\ the\ macro\ _LIBC");
}
eval 'sub __stub___compat_bdflush () {1;}' unless defined(&__stub___compat_bdflush);
eval 'sub __stub___compat_create_module () {1;}' unless defined(&__stub___compat_create_module);
eval 'sub __stub___compat_get_kernel_syms () {1;}' unless defined(&__stub___compat_get_kernel_syms);
eval 'sub __stub___compat_query_module () {1;}' unless defined(&__stub___compat_query_module);
eval 'sub __stub___compat_uselib () {1;}' unless defined(&__stub___compat_uselib);
eval 'sub __stub_chflags () {1;}' unless defined(&__stub_chflags);
eval 'sub __stub_fchflags () {1;}' unless defined(&__stub_fchflags);
eval 'sub __stub_gtty () {1;}' unless defined(&__stub_gtty);
eval 'sub __stub_lchmod () {1;}' unless defined(&__stub_lchmod);
eval 'sub __stub_revoke () {1;}' unless defined(&__stub_revoke);
eval 'sub __stub_setlogin () {1;}' unless defined(&__stub_setlogin);
eval 'sub __stub_sigreturn () {1;}' unless defined(&__stub_sigreturn);
eval 'sub __stub_sstk () {1;}' unless defined(&__stub_sstk);
eval 'sub __stub_stty () {1;}' unless defined(&__stub_stty);
eval 'sub __stub_sysctl () {1;}' unless defined(&__stub_sysctl);
1;
