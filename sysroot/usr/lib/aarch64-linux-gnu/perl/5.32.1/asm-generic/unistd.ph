require '_h2ph_pre.ph';

no warnings qw(redefine misc);

require 'asm/bitsperlong.ph';
unless(defined(&__SYSCALL)) {
    eval 'sub __SYSCALL {
        my($x, $y) = @_;
	    eval q();
    }' unless defined(&__SYSCALL);
}
if((defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) == 32|| defined(&__SYSCALL_COMPAT)) {
    eval 'sub __SC_3264 {
        my($_nr, $_32, $_64) = @_;
	    eval q( &__SYSCALL($_nr, $_32));
    }' unless defined(&__SC_3264);
} else {
    eval 'sub __SC_3264 {
        my($_nr, $_32, $_64) = @_;
	    eval q( &__SYSCALL($_nr, $_64));
    }' unless defined(&__SC_3264);
}
if(defined(&__SYSCALL_COMPAT)) {
    eval 'sub __SC_COMP {
        my($_nr, $_sys, $_comp) = @_;
	    eval q( &__SYSCALL($_nr, $_comp));
    }' unless defined(&__SC_COMP);
    eval 'sub __SC_COMP_3264 {
        my($_nr, $_32, $_64, $_comp) = @_;
	    eval q( &__SYSCALL($_nr, $_comp));
    }' unless defined(&__SC_COMP_3264);
} else {
    eval 'sub __SC_COMP {
        my($_nr, $_sys, $_comp) = @_;
	    eval q( &__SYSCALL($_nr, $_sys));
    }' unless defined(&__SC_COMP);
    eval 'sub __SC_COMP_3264 {
        my($_nr, $_32, $_64, $_comp) = @_;
	    eval q( &__SC_3264($_nr, $_32, $_64));
    }' unless defined(&__SC_COMP_3264);
}
eval 'sub __NR_io_setup () {0;}' unless defined(&__NR_io_setup);
eval 'sub __NR_io_destroy () {1;}' unless defined(&__NR_io_destroy);
eval 'sub __NR_io_submit () {2;}' unless defined(&__NR_io_submit);
eval 'sub __NR_io_cancel () {3;}' unless defined(&__NR_io_cancel);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_io_getevents () {4;}' unless defined(&__NR_io_getevents);
}
eval 'sub __NR_setxattr () {5;}' unless defined(&__NR_setxattr);
eval 'sub __NR_lsetxattr () {6;}' unless defined(&__NR_lsetxattr);
eval 'sub __NR_fsetxattr () {7;}' unless defined(&__NR_fsetxattr);
eval 'sub __NR_getxattr () {8;}' unless defined(&__NR_getxattr);
eval 'sub __NR_lgetxattr () {9;}' unless defined(&__NR_lgetxattr);
eval 'sub __NR_fgetxattr () {10;}' unless defined(&__NR_fgetxattr);
eval 'sub __NR_listxattr () {11;}' unless defined(&__NR_listxattr);
eval 'sub __NR_llistxattr () {12;}' unless defined(&__NR_llistxattr);
eval 'sub __NR_flistxattr () {13;}' unless defined(&__NR_flistxattr);
eval 'sub __NR_removexattr () {14;}' unless defined(&__NR_removexattr);
eval 'sub __NR_lremovexattr () {15;}' unless defined(&__NR_lremovexattr);
eval 'sub __NR_fremovexattr () {16;}' unless defined(&__NR_fremovexattr);
eval 'sub __NR_getcwd () {17;}' unless defined(&__NR_getcwd);
eval 'sub __NR_lookup_dcookie () {18;}' unless defined(&__NR_lookup_dcookie);
eval 'sub __NR_eventfd2 () {19;}' unless defined(&__NR_eventfd2);
eval 'sub __NR_epoll_create1 () {20;}' unless defined(&__NR_epoll_create1);
eval 'sub __NR_epoll_ctl () {21;}' unless defined(&__NR_epoll_ctl);
eval 'sub __NR_epoll_pwait () {22;}' unless defined(&__NR_epoll_pwait);
eval 'sub __NR_dup () {23;}' unless defined(&__NR_dup);
eval 'sub __NR_dup3 () {24;}' unless defined(&__NR_dup3);
eval 'sub __NR3264_fcntl () {25;}' unless defined(&__NR3264_fcntl);
eval 'sub __NR_inotify_init1 () {26;}' unless defined(&__NR_inotify_init1);
eval 'sub __NR_inotify_add_watch () {27;}' unless defined(&__NR_inotify_add_watch);
eval 'sub __NR_inotify_rm_watch () {28;}' unless defined(&__NR_inotify_rm_watch);
eval 'sub __NR_ioctl () {29;}' unless defined(&__NR_ioctl);
eval 'sub __NR_ioprio_set () {30;}' unless defined(&__NR_ioprio_set);
eval 'sub __NR_ioprio_get () {31;}' unless defined(&__NR_ioprio_get);
eval 'sub __NR_flock () {32;}' unless defined(&__NR_flock);
eval 'sub __NR_mknodat () {33;}' unless defined(&__NR_mknodat);
eval 'sub __NR_mkdirat () {34;}' unless defined(&__NR_mkdirat);
eval 'sub __NR_unlinkat () {35;}' unless defined(&__NR_unlinkat);
eval 'sub __NR_symlinkat () {36;}' unless defined(&__NR_symlinkat);
eval 'sub __NR_linkat () {37;}' unless defined(&__NR_linkat);
if(defined(&__ARCH_WANT_RENAMEAT)) {
    eval 'sub __NR_renameat () {38;}' unless defined(&__NR_renameat);
}
eval 'sub __NR_umount2 () {39;}' unless defined(&__NR_umount2);
eval 'sub __NR_mount () {40;}' unless defined(&__NR_mount);
eval 'sub __NR_pivot_root () {41;}' unless defined(&__NR_pivot_root);
eval 'sub __NR_nfsservctl () {42;}' unless defined(&__NR_nfsservctl);
eval 'sub __NR3264_statfs () {43;}' unless defined(&__NR3264_statfs);
eval 'sub __NR3264_fstatfs () {44;}' unless defined(&__NR3264_fstatfs);
eval 'sub __NR3264_truncate () {45;}' unless defined(&__NR3264_truncate);
eval 'sub __NR3264_ftruncate () {46;}' unless defined(&__NR3264_ftruncate);
eval 'sub __NR_fallocate () {47;}' unless defined(&__NR_fallocate);
eval 'sub __NR_faccessat () {48;}' unless defined(&__NR_faccessat);
eval 'sub __NR_chdir () {49;}' unless defined(&__NR_chdir);
eval 'sub __NR_fchdir () {50;}' unless defined(&__NR_fchdir);
eval 'sub __NR_chroot () {51;}' unless defined(&__NR_chroot);
eval 'sub __NR_fchmod () {52;}' unless defined(&__NR_fchmod);
eval 'sub __NR_fchmodat () {53;}' unless defined(&__NR_fchmodat);
eval 'sub __NR_fchownat () {54;}' unless defined(&__NR_fchownat);
eval 'sub __NR_fchown () {55;}' unless defined(&__NR_fchown);
eval 'sub __NR_openat () {56;}' unless defined(&__NR_openat);
eval 'sub __NR_close () {57;}' unless defined(&__NR_close);
eval 'sub __NR_vhangup () {58;}' unless defined(&__NR_vhangup);
eval 'sub __NR_pipe2 () {59;}' unless defined(&__NR_pipe2);
eval 'sub __NR_quotactl () {60;}' unless defined(&__NR_quotactl);
eval 'sub __NR_getdents64 () {61;}' unless defined(&__NR_getdents64);
eval 'sub __NR3264_lseek () {62;}' unless defined(&__NR3264_lseek);
eval 'sub __NR_read () {63;}' unless defined(&__NR_read);
eval 'sub __NR_write () {64;}' unless defined(&__NR_write);
eval 'sub __NR_readv () {65;}' unless defined(&__NR_readv);
eval 'sub __NR_writev () {66;}' unless defined(&__NR_writev);
eval 'sub __NR_pread64 () {67;}' unless defined(&__NR_pread64);
eval 'sub __NR_pwrite64 () {68;}' unless defined(&__NR_pwrite64);
eval 'sub __NR_preadv () {69;}' unless defined(&__NR_preadv);
eval 'sub __NR_pwritev () {70;}' unless defined(&__NR_pwritev);
eval 'sub __NR3264_sendfile () {71;}' unless defined(&__NR3264_sendfile);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_pselect6 () {72;}' unless defined(&__NR_pselect6);
    eval 'sub __NR_ppoll () {73;}' unless defined(&__NR_ppoll);
}
eval 'sub __NR_signalfd4 () {74;}' unless defined(&__NR_signalfd4);
eval 'sub __NR_vmsplice () {75;}' unless defined(&__NR_vmsplice);
eval 'sub __NR_splice () {76;}' unless defined(&__NR_splice);
eval 'sub __NR_tee () {77;}' unless defined(&__NR_tee);
eval 'sub __NR_readlinkat () {78;}' unless defined(&__NR_readlinkat);
if(defined(&__ARCH_WANT_NEW_STAT) || defined(&__ARCH_WANT_STAT64)) {
    eval 'sub __NR3264_fstatat () {79;}' unless defined(&__NR3264_fstatat);
    eval 'sub __NR3264_fstat () {80;}' unless defined(&__NR3264_fstat);
}
eval 'sub __NR_sync () {81;}' unless defined(&__NR_sync);
eval 'sub __NR_fsync () {82;}' unless defined(&__NR_fsync);
eval 'sub __NR_fdatasync () {83;}' unless defined(&__NR_fdatasync);
if(defined(&__ARCH_WANT_SYNC_FILE_RANGE2)) {
    eval 'sub __NR_sync_file_range2 () {84;}' unless defined(&__NR_sync_file_range2);
} else {
    eval 'sub __NR_sync_file_range () {84;}' unless defined(&__NR_sync_file_range);
}
eval 'sub __NR_timerfd_create () {85;}' unless defined(&__NR_timerfd_create);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_timerfd_settime () {86;}' unless defined(&__NR_timerfd_settime);
    eval 'sub __NR_timerfd_gettime () {87;}' unless defined(&__NR_timerfd_gettime);
}
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_utimensat () {88;}' unless defined(&__NR_utimensat);
}
eval 'sub __NR_acct () {89;}' unless defined(&__NR_acct);
eval 'sub __NR_capget () {90;}' unless defined(&__NR_capget);
eval 'sub __NR_capset () {91;}' unless defined(&__NR_capset);
eval 'sub __NR_personality () {92;}' unless defined(&__NR_personality);
eval 'sub __NR_exit () {93;}' unless defined(&__NR_exit);
eval 'sub __NR_exit_group () {94;}' unless defined(&__NR_exit_group);
eval 'sub __NR_waitid () {95;}' unless defined(&__NR_waitid);
eval 'sub __NR_set_tid_address () {96;}' unless defined(&__NR_set_tid_address);
eval 'sub __NR_unshare () {97;}' unless defined(&__NR_unshare);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_futex () {98;}' unless defined(&__NR_futex);
}
eval 'sub __NR_set_robust_list () {99;}' unless defined(&__NR_set_robust_list);
eval 'sub __NR_get_robust_list () {100;}' unless defined(&__NR_get_robust_list);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_nanosleep () {101;}' unless defined(&__NR_nanosleep);
}
eval 'sub __NR_getitimer () {102;}' unless defined(&__NR_getitimer);
eval 'sub __NR_setitimer () {103;}' unless defined(&__NR_setitimer);
eval 'sub __NR_kexec_load () {104;}' unless defined(&__NR_kexec_load);
eval 'sub __NR_init_module () {105;}' unless defined(&__NR_init_module);
eval 'sub __NR_delete_module () {106;}' unless defined(&__NR_delete_module);
eval 'sub __NR_timer_create () {107;}' unless defined(&__NR_timer_create);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_timer_gettime () {108;}' unless defined(&__NR_timer_gettime);
}
eval 'sub __NR_timer_getoverrun () {109;}' unless defined(&__NR_timer_getoverrun);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_timer_settime () {110;}' unless defined(&__NR_timer_settime);
}
eval 'sub __NR_timer_delete () {111;}' unless defined(&__NR_timer_delete);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_clock_settime () {112;}' unless defined(&__NR_clock_settime);
    eval 'sub __NR_clock_gettime () {113;}' unless defined(&__NR_clock_gettime);
    eval 'sub __NR_clock_getres () {114;}' unless defined(&__NR_clock_getres);
    eval 'sub __NR_clock_nanosleep () {115;}' unless defined(&__NR_clock_nanosleep);
}
eval 'sub __NR_syslog () {116;}' unless defined(&__NR_syslog);
eval 'sub __NR_ptrace () {117;}' unless defined(&__NR_ptrace);
eval 'sub __NR_sched_setparam () {118;}' unless defined(&__NR_sched_setparam);
eval 'sub __NR_sched_setscheduler () {119;}' unless defined(&__NR_sched_setscheduler);
eval 'sub __NR_sched_getscheduler () {120;}' unless defined(&__NR_sched_getscheduler);
eval 'sub __NR_sched_getparam () {121;}' unless defined(&__NR_sched_getparam);
eval 'sub __NR_sched_setaffinity () {122;}' unless defined(&__NR_sched_setaffinity);
eval 'sub __NR_sched_getaffinity () {123;}' unless defined(&__NR_sched_getaffinity);
eval 'sub __NR_sched_yield () {124;}' unless defined(&__NR_sched_yield);
eval 'sub __NR_sched_get_priority_max () {125;}' unless defined(&__NR_sched_get_priority_max);
eval 'sub __NR_sched_get_priority_min () {126;}' unless defined(&__NR_sched_get_priority_min);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_sched_rr_get_interval () {127;}' unless defined(&__NR_sched_rr_get_interval);
}
eval 'sub __NR_restart_syscall () {128;}' unless defined(&__NR_restart_syscall);
eval 'sub __NR_kill () {129;}' unless defined(&__NR_kill);
eval 'sub __NR_tkill () {130;}' unless defined(&__NR_tkill);
eval 'sub __NR_tgkill () {131;}' unless defined(&__NR_tgkill);
eval 'sub __NR_sigaltstack () {132;}' unless defined(&__NR_sigaltstack);
eval 'sub __NR_rt_sigsuspend () {133;}' unless defined(&__NR_rt_sigsuspend);
eval 'sub __NR_rt_sigaction () {134;}' unless defined(&__NR_rt_sigaction);
eval 'sub __NR_rt_sigprocmask () {135;}' unless defined(&__NR_rt_sigprocmask);
eval 'sub __NR_rt_sigpending () {136;}' unless defined(&__NR_rt_sigpending);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_rt_sigtimedwait () {137;}' unless defined(&__NR_rt_sigtimedwait);
}
eval 'sub __NR_rt_sigqueueinfo () {138;}' unless defined(&__NR_rt_sigqueueinfo);
eval 'sub __NR_rt_sigreturn () {139;}' unless defined(&__NR_rt_sigreturn);
eval 'sub __NR_setpriority () {140;}' unless defined(&__NR_setpriority);
eval 'sub __NR_getpriority () {141;}' unless defined(&__NR_getpriority);
eval 'sub __NR_reboot () {142;}' unless defined(&__NR_reboot);
eval 'sub __NR_setregid () {143;}' unless defined(&__NR_setregid);
eval 'sub __NR_setgid () {144;}' unless defined(&__NR_setgid);
eval 'sub __NR_setreuid () {145;}' unless defined(&__NR_setreuid);
eval 'sub __NR_setuid () {146;}' unless defined(&__NR_setuid);
eval 'sub __NR_setresuid () {147;}' unless defined(&__NR_setresuid);
eval 'sub __NR_getresuid () {148;}' unless defined(&__NR_getresuid);
eval 'sub __NR_setresgid () {149;}' unless defined(&__NR_setresgid);
eval 'sub __NR_getresgid () {150;}' unless defined(&__NR_getresgid);
eval 'sub __NR_setfsuid () {151;}' unless defined(&__NR_setfsuid);
eval 'sub __NR_setfsgid () {152;}' unless defined(&__NR_setfsgid);
eval 'sub __NR_times () {153;}' unless defined(&__NR_times);
eval 'sub __NR_setpgid () {154;}' unless defined(&__NR_setpgid);
eval 'sub __NR_getpgid () {155;}' unless defined(&__NR_getpgid);
eval 'sub __NR_getsid () {156;}' unless defined(&__NR_getsid);
eval 'sub __NR_setsid () {157;}' unless defined(&__NR_setsid);
eval 'sub __NR_getgroups () {158;}' unless defined(&__NR_getgroups);
eval 'sub __NR_setgroups () {159;}' unless defined(&__NR_setgroups);
eval 'sub __NR_uname () {160;}' unless defined(&__NR_uname);
eval 'sub __NR_sethostname () {161;}' unless defined(&__NR_sethostname);
eval 'sub __NR_setdomainname () {162;}' unless defined(&__NR_setdomainname);
if(defined(&__ARCH_WANT_SET_GET_RLIMIT)) {
    eval 'sub __NR_getrlimit () {163;}' unless defined(&__NR_getrlimit);
    eval 'sub __NR_setrlimit () {164;}' unless defined(&__NR_setrlimit);
}
eval 'sub __NR_getrusage () {165;}' unless defined(&__NR_getrusage);
eval 'sub __NR_umask () {166;}' unless defined(&__NR_umask);
eval 'sub __NR_prctl () {167;}' unless defined(&__NR_prctl);
eval 'sub __NR_getcpu () {168;}' unless defined(&__NR_getcpu);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_gettimeofday () {169;}' unless defined(&__NR_gettimeofday);
    eval 'sub __NR_settimeofday () {170;}' unless defined(&__NR_settimeofday);
    eval 'sub __NR_adjtimex () {171;}' unless defined(&__NR_adjtimex);
}
eval 'sub __NR_getpid () {172;}' unless defined(&__NR_getpid);
eval 'sub __NR_getppid () {173;}' unless defined(&__NR_getppid);
eval 'sub __NR_getuid () {174;}' unless defined(&__NR_getuid);
eval 'sub __NR_geteuid () {175;}' unless defined(&__NR_geteuid);
eval 'sub __NR_getgid () {176;}' unless defined(&__NR_getgid);
eval 'sub __NR_getegid () {177;}' unless defined(&__NR_getegid);
eval 'sub __NR_gettid () {178;}' unless defined(&__NR_gettid);
eval 'sub __NR_sysinfo () {179;}' unless defined(&__NR_sysinfo);
eval 'sub __NR_mq_open () {180;}' unless defined(&__NR_mq_open);
eval 'sub __NR_mq_unlink () {181;}' unless defined(&__NR_mq_unlink);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_mq_timedsend () {182;}' unless defined(&__NR_mq_timedsend);
    eval 'sub __NR_mq_timedreceive () {183;}' unless defined(&__NR_mq_timedreceive);
}
eval 'sub __NR_mq_notify () {184;}' unless defined(&__NR_mq_notify);
eval 'sub __NR_mq_getsetattr () {185;}' unless defined(&__NR_mq_getsetattr);
eval 'sub __NR_msgget () {186;}' unless defined(&__NR_msgget);
eval 'sub __NR_msgctl () {187;}' unless defined(&__NR_msgctl);
eval 'sub __NR_msgrcv () {188;}' unless defined(&__NR_msgrcv);
eval 'sub __NR_msgsnd () {189;}' unless defined(&__NR_msgsnd);
eval 'sub __NR_semget () {190;}' unless defined(&__NR_semget);
eval 'sub __NR_semctl () {191;}' unless defined(&__NR_semctl);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_semtimedop () {192;}' unless defined(&__NR_semtimedop);
}
eval 'sub __NR_semop () {193;}' unless defined(&__NR_semop);
eval 'sub __NR_shmget () {194;}' unless defined(&__NR_shmget);
eval 'sub __NR_shmctl () {195;}' unless defined(&__NR_shmctl);
eval 'sub __NR_shmat () {196;}' unless defined(&__NR_shmat);
eval 'sub __NR_shmdt () {197;}' unless defined(&__NR_shmdt);
eval 'sub __NR_socket () {198;}' unless defined(&__NR_socket);
eval 'sub __NR_socketpair () {199;}' unless defined(&__NR_socketpair);
eval 'sub __NR_bind () {200;}' unless defined(&__NR_bind);
eval 'sub __NR_listen () {201;}' unless defined(&__NR_listen);
eval 'sub __NR_accept () {202;}' unless defined(&__NR_accept);
eval 'sub __NR_connect () {203;}' unless defined(&__NR_connect);
eval 'sub __NR_getsockname () {204;}' unless defined(&__NR_getsockname);
eval 'sub __NR_getpeername () {205;}' unless defined(&__NR_getpeername);
eval 'sub __NR_sendto () {206;}' unless defined(&__NR_sendto);
eval 'sub __NR_recvfrom () {207;}' unless defined(&__NR_recvfrom);
eval 'sub __NR_setsockopt () {208;}' unless defined(&__NR_setsockopt);
eval 'sub __NR_getsockopt () {209;}' unless defined(&__NR_getsockopt);
eval 'sub __NR_shutdown () {210;}' unless defined(&__NR_shutdown);
eval 'sub __NR_sendmsg () {211;}' unless defined(&__NR_sendmsg);
eval 'sub __NR_recvmsg () {212;}' unless defined(&__NR_recvmsg);
eval 'sub __NR_readahead () {213;}' unless defined(&__NR_readahead);
eval 'sub __NR_brk () {214;}' unless defined(&__NR_brk);
eval 'sub __NR_munmap () {215;}' unless defined(&__NR_munmap);
eval 'sub __NR_mremap () {216;}' unless defined(&__NR_mremap);
eval 'sub __NR_add_key () {217;}' unless defined(&__NR_add_key);
eval 'sub __NR_request_key () {218;}' unless defined(&__NR_request_key);
eval 'sub __NR_keyctl () {219;}' unless defined(&__NR_keyctl);
eval 'sub __NR_clone () {220;}' unless defined(&__NR_clone);
eval 'sub __NR_execve () {221;}' unless defined(&__NR_execve);
eval 'sub __NR3264_mmap () {222;}' unless defined(&__NR3264_mmap);
eval 'sub __NR3264_fadvise64 () {223;}' unless defined(&__NR3264_fadvise64);
unless(defined(&__ARCH_NOMMU)) {
    eval 'sub __NR_swapon () {224;}' unless defined(&__NR_swapon);
    eval 'sub __NR_swapoff () {225;}' unless defined(&__NR_swapoff);
    eval 'sub __NR_mprotect () {226;}' unless defined(&__NR_mprotect);
    eval 'sub __NR_msync () {227;}' unless defined(&__NR_msync);
    eval 'sub __NR_mlock () {228;}' unless defined(&__NR_mlock);
    eval 'sub __NR_munlock () {229;}' unless defined(&__NR_munlock);
    eval 'sub __NR_mlockall () {230;}' unless defined(&__NR_mlockall);
    eval 'sub __NR_munlockall () {231;}' unless defined(&__NR_munlockall);
    eval 'sub __NR_mincore () {232;}' unless defined(&__NR_mincore);
    eval 'sub __NR_madvise () {233;}' unless defined(&__NR_madvise);
    eval 'sub __NR_remap_file_pages () {234;}' unless defined(&__NR_remap_file_pages);
    eval 'sub __NR_mbind () {235;}' unless defined(&__NR_mbind);
    eval 'sub __NR_get_mempolicy () {236;}' unless defined(&__NR_get_mempolicy);
    eval 'sub __NR_set_mempolicy () {237;}' unless defined(&__NR_set_mempolicy);
    eval 'sub __NR_migrate_pages () {238;}' unless defined(&__NR_migrate_pages);
    eval 'sub __NR_move_pages () {239;}' unless defined(&__NR_move_pages);
}
eval 'sub __NR_rt_tgsigqueueinfo () {240;}' unless defined(&__NR_rt_tgsigqueueinfo);
eval 'sub __NR_perf_event_open () {241;}' unless defined(&__NR_perf_event_open);
eval 'sub __NR_accept4 () {242;}' unless defined(&__NR_accept4);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_recvmmsg () {243;}' unless defined(&__NR_recvmmsg);
}
eval 'sub __NR_arch_specific_syscall () {244;}' unless defined(&__NR_arch_specific_syscall);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_wait4 () {260;}' unless defined(&__NR_wait4);
}
eval 'sub __NR_prlimit64 () {261;}' unless defined(&__NR_prlimit64);
eval 'sub __NR_fanotify_init () {262;}' unless defined(&__NR_fanotify_init);
eval 'sub __NR_fanotify_mark () {263;}' unless defined(&__NR_fanotify_mark);
eval 'sub __NR_name_to_handle_at () {264;}' unless defined(&__NR_name_to_handle_at);
eval 'sub __NR_open_by_handle_at () {265;}' unless defined(&__NR_open_by_handle_at);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_clock_adjtime () {266;}' unless defined(&__NR_clock_adjtime);
}
eval 'sub __NR_syncfs () {267;}' unless defined(&__NR_syncfs);
eval 'sub __NR_setns () {268;}' unless defined(&__NR_setns);
eval 'sub __NR_sendmmsg () {269;}' unless defined(&__NR_sendmmsg);
eval 'sub __NR_process_vm_readv () {270;}' unless defined(&__NR_process_vm_readv);
eval 'sub __NR_process_vm_writev () {271;}' unless defined(&__NR_process_vm_writev);
eval 'sub __NR_kcmp () {272;}' unless defined(&__NR_kcmp);
eval 'sub __NR_finit_module () {273;}' unless defined(&__NR_finit_module);
eval 'sub __NR_sched_setattr () {274;}' unless defined(&__NR_sched_setattr);
eval 'sub __NR_sched_getattr () {275;}' unless defined(&__NR_sched_getattr);
eval 'sub __NR_renameat2 () {276;}' unless defined(&__NR_renameat2);
eval 'sub __NR_seccomp () {277;}' unless defined(&__NR_seccomp);
eval 'sub __NR_getrandom () {278;}' unless defined(&__NR_getrandom);
eval 'sub __NR_memfd_create () {279;}' unless defined(&__NR_memfd_create);
eval 'sub __NR_bpf () {280;}' unless defined(&__NR_bpf);
eval 'sub __NR_execveat () {281;}' unless defined(&__NR_execveat);
eval 'sub __NR_userfaultfd () {282;}' unless defined(&__NR_userfaultfd);
eval 'sub __NR_membarrier () {283;}' unless defined(&__NR_membarrier);
eval 'sub __NR_mlock2 () {284;}' unless defined(&__NR_mlock2);
eval 'sub __NR_copy_file_range () {285;}' unless defined(&__NR_copy_file_range);
eval 'sub __NR_preadv2 () {286;}' unless defined(&__NR_preadv2);
eval 'sub __NR_pwritev2 () {287;}' unless defined(&__NR_pwritev2);
eval 'sub __NR_pkey_mprotect () {288;}' unless defined(&__NR_pkey_mprotect);
eval 'sub __NR_pkey_alloc () {289;}' unless defined(&__NR_pkey_alloc);
eval 'sub __NR_pkey_free () {290;}' unless defined(&__NR_pkey_free);
eval 'sub __NR_statx () {291;}' unless defined(&__NR_statx);
if(defined(&__ARCH_WANT_TIME32_SYSCALLS) || (defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) != 32) {
    eval 'sub __NR_io_pgetevents () {292;}' unless defined(&__NR_io_pgetevents);
}
eval 'sub __NR_rseq () {293;}' unless defined(&__NR_rseq);
eval 'sub __NR_kexec_file_load () {294;}' unless defined(&__NR_kexec_file_load);
if((defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) == 32) {
    eval 'sub __NR_clock_gettime64 () {403;}' unless defined(&__NR_clock_gettime64);
    eval 'sub __NR_clock_settime64 () {404;}' unless defined(&__NR_clock_settime64);
    eval 'sub __NR_clock_adjtime64 () {405;}' unless defined(&__NR_clock_adjtime64);
    eval 'sub __NR_clock_getres_time64 () {406;}' unless defined(&__NR_clock_getres_time64);
    eval 'sub __NR_clock_nanosleep_time64 () {407;}' unless defined(&__NR_clock_nanosleep_time64);
    eval 'sub __NR_timer_gettime64 () {408;}' unless defined(&__NR_timer_gettime64);
    eval 'sub __NR_timer_settime64 () {409;}' unless defined(&__NR_timer_settime64);
    eval 'sub __NR_timerfd_gettime64 () {410;}' unless defined(&__NR_timerfd_gettime64);
    eval 'sub __NR_timerfd_settime64 () {411;}' unless defined(&__NR_timerfd_settime64);
    eval 'sub __NR_utimensat_time64 () {412;}' unless defined(&__NR_utimensat_time64);
    eval 'sub __NR_pselect6_time64 () {413;}' unless defined(&__NR_pselect6_time64);
    eval 'sub __NR_ppoll_time64 () {414;}' unless defined(&__NR_ppoll_time64);
    eval 'sub __NR_io_pgetevents_time64 () {416;}' unless defined(&__NR_io_pgetevents_time64);
    eval 'sub __NR_recvmmsg_time64 () {417;}' unless defined(&__NR_recvmmsg_time64);
    eval 'sub __NR_mq_timedsend_time64 () {418;}' unless defined(&__NR_mq_timedsend_time64);
    eval 'sub __NR_mq_timedreceive_time64 () {419;}' unless defined(&__NR_mq_timedreceive_time64);
    eval 'sub __NR_semtimedop_time64 () {420;}' unless defined(&__NR_semtimedop_time64);
    eval 'sub __NR_rt_sigtimedwait_time64 () {421;}' unless defined(&__NR_rt_sigtimedwait_time64);
    eval 'sub __NR_futex_time64 () {422;}' unless defined(&__NR_futex_time64);
    eval 'sub __NR_sched_rr_get_interval_time64 () {423;}' unless defined(&__NR_sched_rr_get_interval_time64);
}
eval 'sub __NR_pidfd_send_signal () {424;}' unless defined(&__NR_pidfd_send_signal);
eval 'sub __NR_io_uring_setup () {425;}' unless defined(&__NR_io_uring_setup);
eval 'sub __NR_io_uring_enter () {426;}' unless defined(&__NR_io_uring_enter);
eval 'sub __NR_io_uring_register () {427;}' unless defined(&__NR_io_uring_register);
eval 'sub __NR_open_tree () {428;}' unless defined(&__NR_open_tree);
eval 'sub __NR_move_mount () {429;}' unless defined(&__NR_move_mount);
eval 'sub __NR_fsopen () {430;}' unless defined(&__NR_fsopen);
eval 'sub __NR_fsconfig () {431;}' unless defined(&__NR_fsconfig);
eval 'sub __NR_fsmount () {432;}' unless defined(&__NR_fsmount);
eval 'sub __NR_fspick () {433;}' unless defined(&__NR_fspick);
eval 'sub __NR_pidfd_open () {434;}' unless defined(&__NR_pidfd_open);
if(defined(&__ARCH_WANT_SYS_CLONE3)) {
    eval 'sub __NR_clone3 () {435;}' unless defined(&__NR_clone3);
}
eval 'sub __NR_close_range () {436;}' unless defined(&__NR_close_range);
eval 'sub __NR_openat2 () {437;}' unless defined(&__NR_openat2);
eval 'sub __NR_pidfd_getfd () {438;}' unless defined(&__NR_pidfd_getfd);
eval 'sub __NR_faccessat2 () {439;}' unless defined(&__NR_faccessat2);
eval 'sub __NR_process_madvise () {440;}' unless defined(&__NR_process_madvise);
undef(&__NR_syscalls) if defined(&__NR_syscalls);
eval 'sub __NR_syscalls () {441;}' unless defined(&__NR_syscalls);
if((defined(&__BITS_PER_LONG) ? &__BITS_PER_LONG : undef) == 64 && !defined(&__SYSCALL_COMPAT)) {
    eval 'sub __NR_fcntl () { &__NR3264_fcntl;}' unless defined(&__NR_fcntl);
    eval 'sub __NR_statfs () { &__NR3264_statfs;}' unless defined(&__NR_statfs);
    eval 'sub __NR_fstatfs () { &__NR3264_fstatfs;}' unless defined(&__NR_fstatfs);
    eval 'sub __NR_truncate () { &__NR3264_truncate;}' unless defined(&__NR_truncate);
    eval 'sub __NR_ftruncate () { &__NR3264_ftruncate;}' unless defined(&__NR_ftruncate);
    eval 'sub __NR_lseek () { &__NR3264_lseek;}' unless defined(&__NR_lseek);
    eval 'sub __NR_sendfile () { &__NR3264_sendfile;}' unless defined(&__NR_sendfile);
    if(defined(&__ARCH_WANT_NEW_STAT) || defined(&__ARCH_WANT_STAT64)) {
	eval 'sub __NR_newfstatat () { &__NR3264_fstatat;}' unless defined(&__NR_newfstatat);
	eval 'sub __NR_fstat () { &__NR3264_fstat;}' unless defined(&__NR_fstat);
    }
    eval 'sub __NR_mmap () { &__NR3264_mmap;}' unless defined(&__NR_mmap);
    eval 'sub __NR_fadvise64 () { &__NR3264_fadvise64;}' unless defined(&__NR_fadvise64);
    if(defined(&__NR3264_stat)) {
	eval 'sub __NR_stat () { &__NR3264_stat;}' unless defined(&__NR_stat);
	eval 'sub __NR_lstat () { &__NR3264_lstat;}' unless defined(&__NR_lstat);
    }
} else {
    eval 'sub __NR_fcntl64 () { &__NR3264_fcntl;}' unless defined(&__NR_fcntl64);
    eval 'sub __NR_statfs64 () { &__NR3264_statfs;}' unless defined(&__NR_statfs64);
    eval 'sub __NR_fstatfs64 () { &__NR3264_fstatfs;}' unless defined(&__NR_fstatfs64);
    eval 'sub __NR_truncate64 () { &__NR3264_truncate;}' unless defined(&__NR_truncate64);
    eval 'sub __NR_ftruncate64 () { &__NR3264_ftruncate;}' unless defined(&__NR_ftruncate64);
    eval 'sub __NR_llseek () { &__NR3264_lseek;}' unless defined(&__NR_llseek);
    eval 'sub __NR_sendfile64 () { &__NR3264_sendfile;}' unless defined(&__NR_sendfile64);
    if(defined(&__ARCH_WANT_NEW_STAT) || defined(&__ARCH_WANT_STAT64)) {
	eval 'sub __NR_fstatat64 () { &__NR3264_fstatat;}' unless defined(&__NR_fstatat64);
	eval 'sub __NR_fstat64 () { &__NR3264_fstat;}' unless defined(&__NR_fstat64);
    }
    eval 'sub __NR_mmap2 () { &__NR3264_mmap;}' unless defined(&__NR_mmap2);
    eval 'sub __NR_fadvise64_64 () { &__NR3264_fadvise64;}' unless defined(&__NR_fadvise64_64);
    if(defined(&__NR3264_stat)) {
	eval 'sub __NR_stat64 () { &__NR3264_stat;}' unless defined(&__NR_stat64);
	eval 'sub __NR_lstat64 () { &__NR3264_lstat;}' unless defined(&__NR_lstat64);
    }
}
1;
