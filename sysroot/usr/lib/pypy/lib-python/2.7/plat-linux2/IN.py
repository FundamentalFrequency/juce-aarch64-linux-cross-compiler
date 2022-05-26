import platform

architecture = platform.machine()
if architecture == 'alpha':
    from IN_alpha import *
elif architecture.startswith('parisc'):
    from IN_hppa import *
elif architecture.startswith('mips'):
    from IN_mips import *
elif architecture.startswith('sparc'):
    from IN_sparc import *
else:
    from IN_default import *

del platform, architecture
