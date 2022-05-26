
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

#define PyArray_CopyInto PyPyArray_CopyInto
PyAPI_FUNC(int) PyArray_CopyInto(PyObject *arg0, PyObject *arg1);
#define PyArray_DescrFromType PyPyArray_DescrFromType
PyAPI_FUNC(PyObject *) PyArray_DescrFromType(Signed arg0);
#define PyUFunc_FromFuncAndData PyPyUFunc_FromFuncAndData
PyAPI_FUNC(PyObject *) PyUFunc_FromFuncAndData(void (**arg0)(char **, Py_ssize_t *, Py_ssize_t *, void *), void *arg1, char *arg2, Signed arg3, Signed arg4, Signed arg5, Signed arg6, char *arg7, char *arg8, Signed arg9);
#define PyUFunc_FromFuncAndDataAndSignature PyPyUFunc_FromFuncAndDataAndSignature
PyAPI_FUNC(PyObject *) PyUFunc_FromFuncAndDataAndSignature(void (**arg0)(char **, Py_ssize_t *, Py_ssize_t *, void *), void *arg1, char *arg2, Signed arg3, Signed arg4, Signed arg5, Signed arg6, char *arg7, char *arg8, Signed arg9, char *arg10);
#define _PyArray_Check _PyPyArray_Check
PyAPI_FUNC(int) _PyArray_Check(PyObject *arg0);
#define _PyArray_CheckExact _PyPyArray_CheckExact
PyAPI_FUNC(int) _PyArray_CheckExact(PyObject *arg0);
#define _PyArray_DATA _PyPyArray_DATA
PyAPI_FUNC(void *) _PyArray_DATA(PyObject *arg0);
#define _PyArray_DIM _PyPyArray_DIM
PyAPI_FUNC(Signed) _PyArray_DIM(PyObject *arg0, Signed arg1);
#define _PyArray_FLAGS _PyPyArray_FLAGS
PyAPI_FUNC(int) _PyArray_FLAGS(PyObject *arg0);
#define _PyArray_FromAny _PyPyArray_FromAny
PyAPI_FUNC(PyObject *) _PyArray_FromAny(PyObject *arg0, PyObject *arg1, Signed arg2, Signed arg3, Signed arg4, void *arg5);
#define _PyArray_FromObject _PyPyArray_FromObject
PyAPI_FUNC(PyObject *) _PyArray_FromObject(PyObject *arg0, Signed arg1, Signed arg2, Signed arg3);
#define _PyArray_ITEMSIZE _PyPyArray_ITEMSIZE
PyAPI_FUNC(int) _PyArray_ITEMSIZE(PyObject *arg0);
#define _PyArray_NBYTES _PyPyArray_NBYTES
PyAPI_FUNC(Signed) _PyArray_NBYTES(PyObject *arg0);
#define _PyArray_NDIM _PyPyArray_NDIM
PyAPI_FUNC(int) _PyArray_NDIM(PyObject *arg0);
#define _PyArray_New _PyPyArray_New
PyAPI_FUNC(PyObject *) _PyArray_New(void *arg0, Signed arg1, Signed *arg2, Signed arg3, Signed *arg4, void *arg5, Signed arg6, Signed arg7, PyObject *arg8);
#define _PyArray_SIZE _PyPyArray_SIZE
PyAPI_FUNC(Signed) _PyArray_SIZE(PyObject *arg0);
#define _PyArray_STRIDE _PyPyArray_STRIDE
PyAPI_FUNC(Signed) _PyArray_STRIDE(PyObject *arg0, Signed arg1);
#define _PyArray_SimpleNew _PyPyArray_SimpleNew
PyAPI_FUNC(PyObject *) _PyArray_SimpleNew(Signed arg0, Signed *arg1, Signed arg2);
#define _PyArray_SimpleNewFromData _PyPyArray_SimpleNewFromData
PyAPI_FUNC(PyObject *) _PyArray_SimpleNewFromData(Signed arg0, Signed *arg1, Signed arg2, void *arg3);
#define _PyArray_SimpleNewFromDataOwning _PyPyArray_SimpleNewFromDataOwning
PyAPI_FUNC(PyObject *) _PyArray_SimpleNewFromDataOwning(Signed arg0, Signed *arg1, Signed arg2, void *arg3);
#define _PyArray_TYPE _PyPyArray_TYPE
PyAPI_FUNC(int) _PyArray_TYPE(PyObject *arg0);
#define PyArray_Type PyPyArray_Type
PyAPI_DATA(PyTypeObject) PyArray_Type;

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */
