import platform

architecture = platform.machine()
if architecture.startswith('mips'):
    from DLFCN_mips import *
else:
    from DLFCN_default import *

del platform, architecture
