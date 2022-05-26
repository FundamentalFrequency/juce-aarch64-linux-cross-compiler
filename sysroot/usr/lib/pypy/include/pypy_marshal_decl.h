
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

#define PyMarshal_ReadObjectFromString PyPyMarshal_ReadObjectFromString
PyAPI_FUNC(PyObject *) PyMarshal_ReadObjectFromString(char *arg0, Signed arg1);
#define PyMarshal_WriteObjectToString PyPyMarshal_WriteObjectToString
PyAPI_FUNC(PyObject *) PyMarshal_WriteObjectToString(PyObject *arg0, int arg1);

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */
