
#ifdef _WIN64
/* this check is for sanity, but also because the 'temporary fix'
   below seems to become permanent and would cause unexpected
   nonsense on Win64---but note that it's not the only reason for
   why Win64 is not supported!  If you want to help, see
   http://doc.pypy.org/en/latest/windows.html#what-is-missing-for-a-full-64-bit-translation
   */
#  error "PyPy does not support 64-bit on Windows.  Use Win32"
#endif

#include "cpyext_object.h"
#define Signed   Py_ssize_t     /* xxx temporary fix */
#define Unsigned unsigned long  /* xxx temporary fix */

#define PyMember_GetOne PyPyMember_GetOne
PyAPI_FUNC(PyObject *) PyMember_GetOne(const char *arg0, PyMemberDef *arg1);
#define PyMember_SetOne PyPyMember_SetOne
PyAPI_FUNC(int) PyMember_SetOne(char *arg0, PyMemberDef *arg1, PyObject *arg2);

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */
