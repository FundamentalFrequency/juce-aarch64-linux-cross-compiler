
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

typedef struct { PyObject_HEAD } PyMethodObject;
typedef struct { PyObject_HEAD } PyListObject;
typedef struct { PyObject_HEAD } PyLongObject;
typedef struct { PyObject_HEAD } PyClassObject;
typedef struct { PyObject_HEAD } PyBaseExceptionObject;

/* hack for https://bugs.python.org/issue29943 */

PyAPI_FUNC(int) PyPySlice_GetIndicesEx(PySliceObject *arg0,
                    Signed arg1, Signed *arg2,
                    Signed *arg3, Signed *arg4, Signed *arg5);
#ifdef __GNUC__
__attribute__((__unused__))
#endif
static int PySlice_GetIndicesEx(PySliceObject *arg0, Py_ssize_t arg1,
        Py_ssize_t *arg2, Py_ssize_t *arg3, Py_ssize_t *arg4,
        Py_ssize_t *arg5) {
    return PyPySlice_GetIndicesEx(arg0, arg1, arg2, arg3,
                arg4, arg5);
}
#define PyAnySet_Check PyPyAnySet_Check
PyAPI_FUNC(int) PyAnySet_Check(PyObject *arg0);
#define PyAnySet_CheckExact PyPyAnySet_CheckExact
PyAPI_FUNC(int) PyAnySet_CheckExact(PyObject *arg0);
#define PyBool_FromLong PyPyBool_FromLong
PyAPI_FUNC(PyObject *) PyBool_FromLong(Signed arg0);
#define PyBuffer_FillInfo PyPyBuffer_FillInfo
PyAPI_FUNC(int) PyBuffer_FillInfo(Py_buffer *arg0, PyObject *arg1, void *arg2, Signed arg3, Signed arg4, Signed arg5);
#define PyBuffer_IsContiguous PyPyBuffer_IsContiguous
PyAPI_FUNC(int) PyBuffer_IsContiguous(Py_buffer *arg0, char arg1);
#define PyByteArray_AsString PyPyByteArray_AsString
PyAPI_FUNC(char *) PyByteArray_AsString(PyObject *arg0);
#define PyByteArray_Check PyPyByteArray_Check
PyAPI_FUNC(int) PyByteArray_Check(void * arg0);
#define PyByteArray_CheckExact PyPyByteArray_CheckExact
PyAPI_FUNC(int) PyByteArray_CheckExact(void * arg0);
#define PyByteArray_Concat PyPyByteArray_Concat
PyAPI_FUNC(PyObject *) PyByteArray_Concat(PyObject *arg0, PyObject *arg1);
#define PyByteArray_FromObject PyPyByteArray_FromObject
PyAPI_FUNC(PyObject *) PyByteArray_FromObject(PyObject *arg0);
#define PyByteArray_FromStringAndSize PyPyByteArray_FromStringAndSize
PyAPI_FUNC(PyObject *) PyByteArray_FromStringAndSize(const char *arg0, Signed arg1);
#define PyByteArray_Resize PyPyByteArray_Resize
PyAPI_FUNC(int) PyByteArray_Resize(PyObject *arg0, Signed arg1);
#define PyByteArray_Size PyPyByteArray_Size
PyAPI_FUNC(Signed) PyByteArray_Size(PyObject *arg0);
#define PyCFunction_Call PyPyCFunction_Call
PyAPI_FUNC(PyObject *) PyCFunction_Call(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyCFunction_Check PyPyCFunction_Check
PyAPI_FUNC(int) PyCFunction_Check(PyObject *arg0);
#define PyCFunction_GetFunction PyPyCFunction_GetFunction
PyAPI_FUNC(PyCFunction) PyCFunction_GetFunction(PyObject * arg0);
#define PyCFunction_NewEx PyPyCFunction_NewEx
PyAPI_FUNC(PyObject *) PyCFunction_NewEx(PyMethodDef *arg0, PyObject *arg1, PyObject *arg2);
#define PyCallIter_New PyPyCallIter_New
PyAPI_FUNC(PyObject *) PyCallIter_New(PyObject *arg0, PyObject *arg1);
#define PyCallable_Check PyPyCallable_Check
PyAPI_FUNC(int) PyCallable_Check(PyObject *arg0);
#define PyClassMethod_New PyPyClassMethod_New
PyAPI_FUNC(PyObject *) PyClassMethod_New(PyObject *arg0);
#define PyClass_Check PyPyClass_Check
PyAPI_FUNC(int) PyClass_Check(void * arg0);
#define PyClass_CheckExact PyPyClass_CheckExact
PyAPI_FUNC(int) PyClass_CheckExact(void * arg0);
#define PyClass_New PyPyClass_New
PyAPI_FUNC(PyObject *) PyClass_New(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyCode_Check PyPyCode_Check
PyAPI_FUNC(int) PyCode_Check(void * arg0);
#define PyCode_CheckExact PyPyCode_CheckExact
PyAPI_FUNC(int) PyCode_CheckExact(void * arg0);
#define PyCode_GetNumFree PyPyCode_GetNumFree
PyAPI_FUNC(Signed) PyCode_GetNumFree(PyCodeObject *arg0);
#define PyCode_New PyPyCode_New
PyAPI_FUNC(PyCodeObject *) PyCode_New(int arg0, int arg1, int arg2, int arg3, PyObject *arg4, PyObject *arg5, PyObject *arg6, PyObject *arg7, PyObject *arg8, PyObject *arg9, PyObject *arg10, PyObject *arg11, int arg12, PyObject *arg13);
#define PyCode_NewEmpty PyPyCode_NewEmpty
PyAPI_FUNC(PyCodeObject *) PyCode_NewEmpty(const char *arg0, const char *arg1, int arg2);
#define PyCodec_Decoder PyPyCodec_Decoder
PyAPI_FUNC(PyObject *) PyCodec_Decoder(const char *arg0);
#define PyCodec_Encoder PyPyCodec_Encoder
PyAPI_FUNC(PyObject *) PyCodec_Encoder(const char *arg0);
#define PyCodec_IncrementalDecoder PyPyCodec_IncrementalDecoder
PyAPI_FUNC(PyObject *) PyCodec_IncrementalDecoder(const char *arg0, const char *arg1);
#define PyCodec_IncrementalEncoder PyPyCodec_IncrementalEncoder
PyAPI_FUNC(PyObject *) PyCodec_IncrementalEncoder(const char *arg0, const char *arg1);
#define PyComplex_Check PyPyComplex_Check
PyAPI_FUNC(int) PyComplex_Check(void * arg0);
#define PyComplex_CheckExact PyPyComplex_CheckExact
PyAPI_FUNC(int) PyComplex_CheckExact(void * arg0);
#define PyComplex_FromDoubles PyPyComplex_FromDoubles
PyAPI_FUNC(PyObject *) PyComplex_FromDoubles(double arg0, double arg1);
#define PyComplex_ImagAsDouble PyPyComplex_ImagAsDouble
PyAPI_FUNC(double) PyComplex_ImagAsDouble(PyObject *arg0);
#define PyComplex_RealAsDouble PyPyComplex_RealAsDouble
PyAPI_FUNC(double) PyComplex_RealAsDouble(PyObject *arg0);
#define PyDateTime_Check PyPyDateTime_Check
PyAPI_FUNC(int) PyDateTime_Check(PyObject *arg0);
#define PyDateTime_CheckExact PyPyDateTime_CheckExact
PyAPI_FUNC(int) PyDateTime_CheckExact(PyObject *arg0);
#define PyDateTime_DATE_GET_HOUR PyPyDateTime_DATE_GET_HOUR
PyAPI_FUNC(int) PyDateTime_DATE_GET_HOUR(void *arg0);
#define PyDateTime_DATE_GET_MICROSECOND PyPyDateTime_DATE_GET_MICROSECOND
PyAPI_FUNC(int) PyDateTime_DATE_GET_MICROSECOND(void *arg0);
#define PyDateTime_DATE_GET_MINUTE PyPyDateTime_DATE_GET_MINUTE
PyAPI_FUNC(int) PyDateTime_DATE_GET_MINUTE(void *arg0);
#define PyDateTime_DATE_GET_SECOND PyPyDateTime_DATE_GET_SECOND
PyAPI_FUNC(int) PyDateTime_DATE_GET_SECOND(void *arg0);
#define PyDateTime_DELTA_GET_DAYS PyPyDateTime_DELTA_GET_DAYS
PyAPI_FUNC(int) PyDateTime_DELTA_GET_DAYS(void *arg0);
#define PyDateTime_DELTA_GET_MICROSECONDS PyPyDateTime_DELTA_GET_MICROSECONDS
PyAPI_FUNC(int) PyDateTime_DELTA_GET_MICROSECONDS(void *arg0);
#define PyDateTime_DELTA_GET_SECONDS PyPyDateTime_DELTA_GET_SECONDS
PyAPI_FUNC(int) PyDateTime_DELTA_GET_SECONDS(void *arg0);
#define PyDateTime_FromTimestamp PyPyDateTime_FromTimestamp
PyAPI_FUNC(PyObject *) PyDateTime_FromTimestamp(PyObject *arg0);
#define PyDateTime_GET_DAY PyPyDateTime_GET_DAY
PyAPI_FUNC(int) PyDateTime_GET_DAY(void *arg0);
#define PyDateTime_GET_MONTH PyPyDateTime_GET_MONTH
PyAPI_FUNC(int) PyDateTime_GET_MONTH(void *arg0);
#define PyDateTime_GET_YEAR PyPyDateTime_GET_YEAR
PyAPI_FUNC(int) PyDateTime_GET_YEAR(void *arg0);
#define PyDateTime_TIME_GET_HOUR PyPyDateTime_TIME_GET_HOUR
PyAPI_FUNC(int) PyDateTime_TIME_GET_HOUR(void *arg0);
#define PyDateTime_TIME_GET_MICROSECOND PyPyDateTime_TIME_GET_MICROSECOND
PyAPI_FUNC(int) PyDateTime_TIME_GET_MICROSECOND(void *arg0);
#define PyDateTime_TIME_GET_MINUTE PyPyDateTime_TIME_GET_MINUTE
PyAPI_FUNC(int) PyDateTime_TIME_GET_MINUTE(void *arg0);
#define PyDateTime_TIME_GET_SECOND PyPyDateTime_TIME_GET_SECOND
PyAPI_FUNC(int) PyDateTime_TIME_GET_SECOND(void *arg0);
#define PyDate_Check PyPyDate_Check
PyAPI_FUNC(int) PyDate_Check(PyObject *arg0);
#define PyDate_CheckExact PyPyDate_CheckExact
PyAPI_FUNC(int) PyDate_CheckExact(PyObject *arg0);
#define PyDate_FromTimestamp PyPyDate_FromTimestamp
PyAPI_FUNC(PyObject *) PyDate_FromTimestamp(PyObject *arg0);
#define PyDelta_Check PyPyDelta_Check
PyAPI_FUNC(int) PyDelta_Check(PyObject *arg0);
#define PyDelta_CheckExact PyPyDelta_CheckExact
PyAPI_FUNC(int) PyDelta_CheckExact(PyObject *arg0);
#define PyDescr_NewClassMethod PyPyDescr_NewClassMethod
PyAPI_FUNC(PyObject *) PyDescr_NewClassMethod(PyTypeObject * arg0, PyMethodDef * arg1);
#define PyDictProxy_Check PyPyDictProxy_Check
PyAPI_FUNC(int) PyDictProxy_Check(PyObject *arg0);
#define PyDictProxy_CheckExact PyPyDictProxy_CheckExact
PyAPI_FUNC(int) PyDictProxy_CheckExact(PyObject *arg0);
#define PyDictProxy_New PyPyDictProxy_New
PyAPI_FUNC(PyObject *) PyDictProxy_New(PyObject *arg0);
#define PyDict_Clear PyPyDict_Clear
PyAPI_FUNC(void) PyDict_Clear(PyObject *arg0);
#define PyDict_Contains PyPyDict_Contains
PyAPI_FUNC(int) PyDict_Contains(PyObject *arg0, PyObject *arg1);
#define PyDict_Copy PyPyDict_Copy
PyAPI_FUNC(PyObject *) PyDict_Copy(PyObject *arg0);
#define PyDict_DelItem PyPyDict_DelItem
PyAPI_FUNC(int) PyDict_DelItem(PyObject *arg0, PyObject *arg1);
#define PyDict_DelItemString PyPyDict_DelItemString
PyAPI_FUNC(int) PyDict_DelItemString(PyObject *arg0, const char *arg1);
#define PyDict_GetItem PyPyDict_GetItem
PyAPI_FUNC(PyObject *) PyDict_GetItem(PyObject *arg0, PyObject *arg1);
#define PyDict_GetItemString PyPyDict_GetItemString
PyAPI_FUNC(PyObject *) PyDict_GetItemString(PyObject *arg0, const char *arg1);
#define PyDict_Items PyPyDict_Items
PyAPI_FUNC(PyObject *) PyDict_Items(PyObject *arg0);
#define PyDict_Keys PyPyDict_Keys
PyAPI_FUNC(PyObject *) PyDict_Keys(PyObject *arg0);
#define PyDict_Merge PyPyDict_Merge
PyAPI_FUNC(int) PyDict_Merge(PyObject *arg0, PyObject *arg1, int arg2);
#define PyDict_New PyPyDict_New
PyAPI_FUNC(PyObject *) PyDict_New(void);
#define PyDict_Next PyPyDict_Next
PyAPI_FUNC(int) PyDict_Next(PyObject *arg0, Signed *arg1, PyObject **arg2, PyObject **arg3);
#define PyDict_SetItem PyPyDict_SetItem
PyAPI_FUNC(int) PyDict_SetItem(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyDict_SetItemString PyPyDict_SetItemString
PyAPI_FUNC(int) PyDict_SetItemString(PyObject *arg0, const char *arg1, PyObject *arg2);
#define PyDict_Size PyPyDict_Size
PyAPI_FUNC(Signed) PyDict_Size(PyObject *arg0);
#define PyDict_Update PyPyDict_Update
PyAPI_FUNC(int) PyDict_Update(PyObject *arg0, PyObject *arg1);
#define PyDict_Values PyPyDict_Values
PyAPI_FUNC(PyObject *) PyDict_Values(PyObject *arg0);
#define PyErr_BadArgument PyPyErr_BadArgument
PyAPI_FUNC(int) PyErr_BadArgument(void);
#define PyErr_BadInternalCall PyPyErr_BadInternalCall
PyAPI_FUNC(void) PyErr_BadInternalCall(void);
#define PyErr_CheckSignals PyPyErr_CheckSignals
PyAPI_FUNC(int) PyErr_CheckSignals(void);
#define PyErr_Clear PyPyErr_Clear
PyAPI_FUNC(void) PyErr_Clear(void);
#define PyErr_Display PyPyErr_Display
PyAPI_FUNC(void) PyErr_Display(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyErr_ExceptionMatches PyPyErr_ExceptionMatches
PyAPI_FUNC(int) PyErr_ExceptionMatches(PyObject *arg0);
#define PyErr_Fetch PyPyErr_Fetch
PyAPI_FUNC(void) PyErr_Fetch(PyObject **arg0, PyObject **arg1, PyObject **arg2);
#define PyErr_GetExcInfo PyPyErr_GetExcInfo
PyAPI_FUNC(void) PyErr_GetExcInfo(PyObject **arg0, PyObject **arg1, PyObject **arg2);
#define PyErr_GivenExceptionMatches PyPyErr_GivenExceptionMatches
PyAPI_FUNC(int) PyErr_GivenExceptionMatches(PyObject *arg0, PyObject *arg1);
#define PyErr_NoMemory PyPyErr_NoMemory
PyAPI_FUNC(PyObject *) PyErr_NoMemory(void);
#define PyErr_NormalizeException PyPyErr_NormalizeException
PyAPI_FUNC(void) PyErr_NormalizeException(PyObject **arg0, PyObject **arg1, PyObject **arg2);
#define PyErr_Occurred PyPyErr_Occurred
PyAPI_FUNC(PyObject *) PyErr_Occurred(void);
#define PyErr_Print PyPyErr_Print
PyAPI_FUNC(void) PyErr_Print(void);
#define PyErr_PrintEx PyPyErr_PrintEx
PyAPI_FUNC(void) PyErr_PrintEx(int arg0);
#define PyErr_Restore PyPyErr_Restore
PyAPI_FUNC(void) PyErr_Restore(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyErr_SetExcInfo PyPyErr_SetExcInfo
PyAPI_FUNC(void) PyErr_SetExcInfo(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyErr_SetFromErrno PyPyErr_SetFromErrno
PyAPI_FUNC(PyObject *) PyErr_SetFromErrno(PyObject *arg0);
#define PyErr_SetFromErrnoWithFilename PyPyErr_SetFromErrnoWithFilename
PyAPI_FUNC(PyObject *) PyErr_SetFromErrnoWithFilename(PyObject *arg0, char *arg1);
#define PyErr_SetFromErrnoWithFilenameObject PyPyErr_SetFromErrnoWithFilenameObject
PyAPI_FUNC(PyObject *) PyErr_SetFromErrnoWithFilenameObject(PyObject *arg0, PyObject *arg1);
#define PyErr_SetInterrupt PyPyErr_SetInterrupt
PyAPI_FUNC(void) PyErr_SetInterrupt(void);
#define PyErr_SetNone PyPyErr_SetNone
PyAPI_FUNC(void) PyErr_SetNone(PyObject *arg0);
#define PyErr_SetObject PyPyErr_SetObject
PyAPI_FUNC(void) PyErr_SetObject(PyObject *arg0, PyObject *arg1);
#define PyErr_SetString PyPyErr_SetString
PyAPI_FUNC(void) PyErr_SetString(PyObject *arg0, const char *arg1);
#define PyErr_Warn PyPyErr_Warn
PyAPI_FUNC(int) PyErr_Warn(PyObject *arg0, const char *arg1);
#define PyErr_WarnEx PyPyErr_WarnEx
PyAPI_FUNC(int) PyErr_WarnEx(PyObject *arg0, const char *arg1, int arg2);
#define PyErr_WriteUnraisable PyPyErr_WriteUnraisable
PyAPI_FUNC(void) PyErr_WriteUnraisable(PyObject *arg0);
#define PyEval_AcquireThread PyPyEval_AcquireThread
PyAPI_FUNC(void) PyEval_AcquireThread(PyThreadState *arg0);
#define PyEval_CallObjectWithKeywords PyPyEval_CallObjectWithKeywords
PyAPI_FUNC(PyObject *) PyEval_CallObjectWithKeywords(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyEval_EvalCode PyPyEval_EvalCode
PyAPI_FUNC(PyObject *) PyEval_EvalCode(PyCodeObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyEval_GetBuiltins PyPyEval_GetBuiltins
PyAPI_FUNC(PyObject *) PyEval_GetBuiltins(void);
#define PyEval_GetFrame PyPyEval_GetFrame
PyAPI_FUNC(PyFrameObject *) PyEval_GetFrame(void);
#define PyEval_GetGlobals PyPyEval_GetGlobals
PyAPI_FUNC(PyObject *) PyEval_GetGlobals(void);
#define PyEval_GetLocals PyPyEval_GetLocals
PyAPI_FUNC(PyObject *) PyEval_GetLocals(void);
#define PyEval_InitThreads PyPyEval_InitThreads
PyAPI_FUNC(void) PyEval_InitThreads(void);
#define PyEval_MergeCompilerFlags PyPyEval_MergeCompilerFlags
PyAPI_FUNC(int) PyEval_MergeCompilerFlags(PyCompilerFlags *arg0);
#define PyEval_ReleaseThread PyPyEval_ReleaseThread
PyAPI_FUNC(void) PyEval_ReleaseThread(PyThreadState *arg0);
#define PyEval_RestoreThread PyPyEval_RestoreThread
PyAPI_FUNC(void) PyEval_RestoreThread(PyThreadState *arg0);
#define PyEval_SaveThread PyPyEval_SaveThread
PyAPI_FUNC(PyThreadState *) PyEval_SaveThread(void);
#define PyEval_ThreadsInitialized PyPyEval_ThreadsInitialized
PyAPI_FUNC(int) PyEval_ThreadsInitialized(void);
#define PyExceptionInstance_Class PyPyExceptionInstance_Class
PyAPI_FUNC(PyObject *) PyExceptionInstance_Class(PyObject *arg0);
#define PyFile_AsFile PyPyFile_AsFile
PyAPI_FUNC(FILE *) PyFile_AsFile(PyObject *arg0);
#define PyFile_Check PyPyFile_Check
PyAPI_FUNC(int) PyFile_Check(void * arg0);
#define PyFile_CheckExact PyPyFile_CheckExact
PyAPI_FUNC(int) PyFile_CheckExact(void * arg0);
#define PyFile_FromFile PyPyFile_FromFile
PyAPI_FUNC(PyObject *) PyFile_FromFile(FILE *arg0, const char *arg1, const char *arg2, void *arg3);
#define PyFile_FromString PyPyFile_FromString
PyAPI_FUNC(PyObject *) PyFile_FromString(const char *arg0, const char *arg1);
#define PyFile_GetLine PyPyFile_GetLine
PyAPI_FUNC(PyObject *) PyFile_GetLine(PyObject *arg0, int arg1);
#define PyFile_Name PyPyFile_Name
PyAPI_FUNC(PyObject *) PyFile_Name(PyObject *arg0);
#define PyFile_SetBufSize PyPyFile_SetBufSize
PyAPI_FUNC(void) PyFile_SetBufSize(PyObject *arg0, int arg1);
#define PyFile_SoftSpace PyPyFile_SoftSpace
PyAPI_FUNC(int) PyFile_SoftSpace(PyObject *arg0, int arg1);
#define PyFile_WriteObject PyPyFile_WriteObject
PyAPI_FUNC(int) PyFile_WriteObject(PyObject *arg0, PyObject *arg1, int arg2);
#define PyFile_WriteString PyPyFile_WriteString
PyAPI_FUNC(int) PyFile_WriteString(const char *arg0, PyObject *arg1);
#define PyFloat_AS_DOUBLE PyPyFloat_AS_DOUBLE
PyAPI_FUNC(double) PyFloat_AS_DOUBLE(void *arg0);
#define PyFloat_AsDouble PyPyFloat_AsDouble
PyAPI_FUNC(double) PyFloat_AsDouble(PyObject *arg0);
#define PyFloat_FromDouble PyPyFloat_FromDouble
PyAPI_FUNC(PyObject *) PyFloat_FromDouble(double arg0);
#define PyFloat_FromString PyPyFloat_FromString
PyAPI_FUNC(PyObject *) PyFloat_FromString(PyObject *arg0, char **arg1);
#define PyFrame_New PyPyFrame_New
PyAPI_FUNC(PyFrameObject *) PyFrame_New(PyThreadState *arg0, PyCodeObject *arg1, PyObject *arg2, PyObject *arg3);
#define PyFrozenSet_Check PyPyFrozenSet_Check
PyAPI_FUNC(int) PyFrozenSet_Check(void * arg0);
#define PyFrozenSet_CheckExact PyPyFrozenSet_CheckExact
PyAPI_FUNC(int) PyFrozenSet_CheckExact(void * arg0);
#define PyFrozenSet_New PyPyFrozenSet_New
PyAPI_FUNC(PyObject *) PyFrozenSet_New(PyObject *arg0);
#define PyFunction_Check PyPyFunction_Check
PyAPI_FUNC(int) PyFunction_Check(void * arg0);
#define PyFunction_CheckExact PyPyFunction_CheckExact
PyAPI_FUNC(int) PyFunction_CheckExact(void * arg0);
#define PyFunction_GetCode PyPyFunction_GetCode
PyAPI_FUNC(PyObject *) PyFunction_GetCode(PyObject *arg0);
#define PyGILState_Ensure PyPyGILState_Ensure
PyAPI_FUNC(int) PyGILState_Ensure(void);
#define PyGILState_Release PyPyGILState_Release
PyAPI_FUNC(void) PyGILState_Release(int arg0);
#define PyImport_AddModule PyPyImport_AddModule
PyAPI_FUNC(PyObject *) PyImport_AddModule(const char *arg0);
#define PyImport_ExecCodeModule PyPyImport_ExecCodeModule
PyAPI_FUNC(PyObject *) PyImport_ExecCodeModule(char *arg0, PyObject *arg1);
#define PyImport_ExecCodeModuleEx PyPyImport_ExecCodeModuleEx
PyAPI_FUNC(PyObject *) PyImport_ExecCodeModuleEx(char *arg0, PyObject *arg1, char *arg2);
#define PyImport_GetModuleDict PyPyImport_GetModuleDict
PyAPI_FUNC(PyObject *) PyImport_GetModuleDict(void);
#define PyImport_Import PyPyImport_Import
PyAPI_FUNC(PyObject *) PyImport_Import(PyObject *arg0);
#define PyImport_ImportModule PyPyImport_ImportModule
PyAPI_FUNC(PyObject *) PyImport_ImportModule(const char *arg0);
#define PyImport_ImportModuleNoBlock PyPyImport_ImportModuleNoBlock
PyAPI_FUNC(PyObject *) PyImport_ImportModuleNoBlock(const char *arg0);
#define PyImport_ReloadModule PyPyImport_ReloadModule
PyAPI_FUNC(PyObject *) PyImport_ReloadModule(PyObject *arg0);
#define PyIndex_Check PyPyIndex_Check
PyAPI_FUNC(int) PyIndex_Check(PyObject *arg0);
#define PyInstance_Check PyPyInstance_Check
PyAPI_FUNC(int) PyInstance_Check(void * arg0);
#define PyInstance_CheckExact PyPyInstance_CheckExact
PyAPI_FUNC(int) PyInstance_CheckExact(void * arg0);
#define PyInstance_New PyPyInstance_New
PyAPI_FUNC(PyObject *) PyInstance_New(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyInstance_NewRaw PyPyInstance_NewRaw
PyAPI_FUNC(PyObject *) PyInstance_NewRaw(PyObject *arg0, PyObject *arg1);
#define PyInt_AS_LONG PyPyInt_AS_LONG
PyAPI_FUNC(Signed) PyInt_AS_LONG(void *arg0);
#define PyInt_AsLong PyPyInt_AsLong
PyAPI_FUNC(Signed) PyInt_AsLong(PyObject *arg0);
#define PyInt_AsSsize_t PyPyInt_AsSsize_t
PyAPI_FUNC(Signed) PyInt_AsSsize_t(PyObject *arg0);
#define PyInt_AsUnsignedLong PyPyInt_AsUnsignedLong
PyAPI_FUNC(Unsigned) PyInt_AsUnsignedLong(PyObject *arg0);
#define PyInt_AsUnsignedLongLongMask PyPyInt_AsUnsignedLongLongMask
PyAPI_FUNC(Unsigned) PyInt_AsUnsignedLongLongMask(PyObject *arg0);
#define PyInt_AsUnsignedLongMask PyPyInt_AsUnsignedLongMask
PyAPI_FUNC(Unsigned) PyInt_AsUnsignedLongMask(PyObject *arg0);
#define PyInt_FromSize_t PyPyInt_FromSize_t
PyAPI_FUNC(PyObject *) PyInt_FromSize_t(Unsigned arg0);
#define PyInt_FromSsize_t PyPyInt_FromSsize_t
PyAPI_FUNC(PyObject *) PyInt_FromSsize_t(Signed arg0);
#define PyInt_FromString PyPyInt_FromString
PyAPI_FUNC(PyObject *) PyInt_FromString(const char *arg0, char **arg1, int arg2);
#define PyInt_GetMax PyPyInt_GetMax
PyAPI_FUNC(Signed) PyInt_GetMax(void);
#define PyInterpreterState_Head PyPyInterpreterState_Head
PyAPI_FUNC(PyInterpreterState *) PyInterpreterState_Head(void);
#define PyInterpreterState_Next PyPyInterpreterState_Next
PyAPI_FUNC(PyInterpreterState *) PyInterpreterState_Next(PyInterpreterState *arg0);
#define PyIter_Check PyPyIter_Check
PyAPI_FUNC(int) PyIter_Check(PyObject *arg0);
#define PyIter_Next PyPyIter_Next
PyAPI_FUNC(PyObject *) PyIter_Next(PyObject *arg0);
#define PyList_Append PyPyList_Append
PyAPI_FUNC(int) PyList_Append(PyObject *arg0, PyObject *arg1);
#define PyList_AsTuple PyPyList_AsTuple
PyAPI_FUNC(PyObject *) PyList_AsTuple(PyObject *arg0);
#define PyList_GET_ITEM PyPyList_GET_ITEM
PyAPI_FUNC(PyObject *) PyList_GET_ITEM(void *arg0, Signed arg1);
#define PyList_GET_SIZE PyPyList_GET_SIZE
PyAPI_FUNC(Signed) PyList_GET_SIZE(void *arg0);
#define PyList_GetItem PyPyList_GetItem
PyAPI_FUNC(PyObject *) PyList_GetItem(PyObject *arg0, Signed arg1);
#define PyList_GetSlice PyPyList_GetSlice
PyAPI_FUNC(PyObject *) PyList_GetSlice(PyObject *arg0, Signed arg1, Signed arg2);
#define PyList_Insert PyPyList_Insert
PyAPI_FUNC(int) PyList_Insert(PyObject *arg0, Signed arg1, PyObject *arg2);
#define PyList_New PyPyList_New
PyAPI_FUNC(PyObject *) PyList_New(Signed arg0);
#define PyList_Reverse PyPyList_Reverse
PyAPI_FUNC(int) PyList_Reverse(PyObject *arg0);
#define PyList_SET_ITEM PyPyList_SET_ITEM
PyAPI_FUNC(void) PyList_SET_ITEM(void *arg0, Signed arg1, PyObject *arg2);
#define PyList_SetItem PyPyList_SetItem
PyAPI_FUNC(int) PyList_SetItem(PyObject *arg0, Signed arg1, PyObject *arg2);
#define PyList_SetSlice PyPyList_SetSlice
PyAPI_FUNC(int) PyList_SetSlice(PyObject *arg0, Signed arg1, Signed arg2, PyObject *arg3);
#define PyList_Size PyPyList_Size
PyAPI_FUNC(Signed) PyList_Size(PyObject *arg0);
#define PyList_Sort PyPyList_Sort
PyAPI_FUNC(int) PyList_Sort(PyObject *arg0);
#define PyLong_AsDouble PyPyLong_AsDouble
PyAPI_FUNC(double) PyLong_AsDouble(PyObject *arg0);
#define PyLong_AsLong PyPyLong_AsLong
PyAPI_FUNC(Signed) PyLong_AsLong(PyObject *arg0);
#define PyLong_AsLongAndOverflow PyPyLong_AsLongAndOverflow
PyAPI_FUNC(Signed) PyLong_AsLongAndOverflow(PyObject *arg0, int *arg1);
#define PyLong_AsLongLong PyPyLong_AsLongLong
PyAPI_FUNC(Signed) PyLong_AsLongLong(PyObject *arg0);
#define PyLong_AsLongLongAndOverflow PyPyLong_AsLongLongAndOverflow
PyAPI_FUNC(Signed) PyLong_AsLongLongAndOverflow(PyObject *arg0, int *arg1);
#define PyLong_AsSsize_t PyPyLong_AsSsize_t
PyAPI_FUNC(Signed) PyLong_AsSsize_t(PyObject *arg0);
#define PyLong_AsUnsignedLong PyPyLong_AsUnsignedLong
PyAPI_FUNC(Unsigned) PyLong_AsUnsignedLong(PyObject *arg0);
#define PyLong_AsUnsignedLongLong PyPyLong_AsUnsignedLongLong
PyAPI_FUNC(Unsigned) PyLong_AsUnsignedLongLong(PyObject *arg0);
#define PyLong_AsUnsignedLongLongMask PyPyLong_AsUnsignedLongLongMask
PyAPI_FUNC(Unsigned) PyLong_AsUnsignedLongLongMask(PyObject *arg0);
#define PyLong_AsUnsignedLongMask PyPyLong_AsUnsignedLongMask
PyAPI_FUNC(Unsigned) PyLong_AsUnsignedLongMask(PyObject *arg0);
#define PyLong_AsVoidPtr PyPyLong_AsVoidPtr
PyAPI_FUNC(void *) PyLong_AsVoidPtr(PyObject *arg0);
#define PyLong_FromDouble PyPyLong_FromDouble
PyAPI_FUNC(PyObject *) PyLong_FromDouble(double arg0);
#define PyLong_FromLong PyPyLong_FromLong
PyAPI_FUNC(PyObject *) PyLong_FromLong(Signed arg0);
#define PyLong_FromLongLong PyPyLong_FromLongLong
PyAPI_FUNC(PyObject *) PyLong_FromLongLong(Signed arg0);
#define PyLong_FromSize_t PyPyLong_FromSize_t
PyAPI_FUNC(PyObject *) PyLong_FromSize_t(Unsigned arg0);
#define PyLong_FromSsize_t PyPyLong_FromSsize_t
PyAPI_FUNC(PyObject *) PyLong_FromSsize_t(Signed arg0);
#define PyLong_FromString PyPyLong_FromString
PyAPI_FUNC(PyObject *) PyLong_FromString(const char *arg0, char **arg1, int arg2);
#define PyLong_FromUnicode PyPyLong_FromUnicode
PyAPI_FUNC(PyObject *) PyLong_FromUnicode(wchar_t *arg0, Signed arg1, int arg2);
#define PyLong_FromUnsignedLong PyPyLong_FromUnsignedLong
PyAPI_FUNC(PyObject *) PyLong_FromUnsignedLong(Unsigned arg0);
#define PyLong_FromUnsignedLongLong PyPyLong_FromUnsignedLongLong
PyAPI_FUNC(PyObject *) PyLong_FromUnsignedLongLong(Unsigned arg0);
#define PyLong_FromVoidPtr PyPyLong_FromVoidPtr
PyAPI_FUNC(PyObject *) PyLong_FromVoidPtr(void *arg0);
#define PyMapping_Check PyPyMapping_Check
PyAPI_FUNC(int) PyMapping_Check(PyObject *arg0);
#define PyMapping_GetItemString PyPyMapping_GetItemString
PyAPI_FUNC(PyObject *) PyMapping_GetItemString(PyObject *arg0, const char *arg1);
#define PyMapping_HasKey PyPyMapping_HasKey
PyAPI_FUNC(int) PyMapping_HasKey(PyObject *arg0, PyObject *arg1);
#define PyMapping_HasKeyString PyPyMapping_HasKeyString
PyAPI_FUNC(int) PyMapping_HasKeyString(PyObject *arg0, const char *arg1);
#define PyMapping_Items PyPyMapping_Items
PyAPI_FUNC(PyObject *) PyMapping_Items(PyObject *arg0);
#define PyMapping_Keys PyPyMapping_Keys
PyAPI_FUNC(PyObject *) PyMapping_Keys(PyObject *arg0);
#define PyMapping_Length PyPyMapping_Length
PyAPI_FUNC(Signed) PyMapping_Length(PyObject *arg0);
#define PyMapping_SetItemString PyPyMapping_SetItemString
PyAPI_FUNC(int) PyMapping_SetItemString(PyObject *arg0, const char *arg1, PyObject *arg2);
#define PyMapping_Size PyPyMapping_Size
PyAPI_FUNC(Signed) PyMapping_Size(PyObject *arg0);
#define PyMapping_Values PyPyMapping_Values
PyAPI_FUNC(PyObject *) PyMapping_Values(PyObject *arg0);
#define PyMemoryView_Check PyPyMemoryView_Check
PyAPI_FUNC(int) PyMemoryView_Check(void * arg0);
#define PyMemoryView_CheckExact PyPyMemoryView_CheckExact
PyAPI_FUNC(int) PyMemoryView_CheckExact(void * arg0);
#define PyMemoryView_FromBuffer PyPyMemoryView_FromBuffer
PyAPI_FUNC(PyObject *) PyMemoryView_FromBuffer(Py_buffer *arg0);
#define PyMemoryView_FromObject PyPyMemoryView_FromObject
PyAPI_FUNC(PyObject *) PyMemoryView_FromObject(PyObject *arg0);
#define PyMemoryView_GetContiguous PyPyMemoryView_GetContiguous
PyAPI_FUNC(PyObject *) PyMemoryView_GetContiguous(PyObject *arg0, int arg1, char arg2);
#define PyMethodDescr_Check PyPyMethodDescr_Check
PyAPI_FUNC(int) PyMethodDescr_Check(void * arg0);
#define PyMethodDescr_CheckExact PyPyMethodDescr_CheckExact
PyAPI_FUNC(int) PyMethodDescr_CheckExact(void * arg0);
#define PyMethod_Check PyPyMethod_Check
PyAPI_FUNC(int) PyMethod_Check(void * arg0);
#define PyMethod_CheckExact PyPyMethod_CheckExact
PyAPI_FUNC(int) PyMethod_CheckExact(void * arg0);
#define PyMethod_Class PyPyMethod_Class
PyAPI_FUNC(PyObject *) PyMethod_Class(PyObject *arg0);
#define PyMethod_Function PyPyMethod_Function
PyAPI_FUNC(PyObject *) PyMethod_Function(PyObject *arg0);
#define PyMethod_New PyPyMethod_New
PyAPI_FUNC(PyObject *) PyMethod_New(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyMethod_Self PyPyMethod_Self
PyAPI_FUNC(PyObject *) PyMethod_Self(PyObject *arg0);
#define PyModule_Check PyPyModule_Check
PyAPI_FUNC(int) PyModule_Check(PyObject *arg0);
#define PyModule_GetDict PyPyModule_GetDict
PyAPI_FUNC(PyObject *) PyModule_GetDict(PyObject *arg0);
#define PyModule_GetName PyPyModule_GetName
PyAPI_FUNC(char *) PyModule_GetName(PyObject *arg0);
#define PyModule_New PyPyModule_New
PyAPI_FUNC(PyObject *) PyModule_New(char *arg0);
#define PyNumber_Absolute PyPyNumber_Absolute
PyAPI_FUNC(PyObject *) PyNumber_Absolute(PyObject *arg0);
#define PyNumber_Add PyPyNumber_Add
PyAPI_FUNC(PyObject *) PyNumber_Add(PyObject *arg0, PyObject *arg1);
#define PyNumber_And PyPyNumber_And
PyAPI_FUNC(PyObject *) PyNumber_And(PyObject *arg0, PyObject *arg1);
#define PyNumber_AsSsize_t PyPyNumber_AsSsize_t
PyAPI_FUNC(Signed) PyNumber_AsSsize_t(PyObject *arg0, PyObject *arg1);
#define PyNumber_Check PyPyNumber_Check
PyAPI_FUNC(int) PyNumber_Check(PyObject *arg0);
#define PyNumber_Coerce PyPyNumber_Coerce
PyAPI_FUNC(int) PyNumber_Coerce(PyObject **arg0, PyObject **arg1);
#define PyNumber_CoerceEx PyPyNumber_CoerceEx
PyAPI_FUNC(int) PyNumber_CoerceEx(PyObject **arg0, PyObject **arg1);
#define PyNumber_Divide PyPyNumber_Divide
PyAPI_FUNC(PyObject *) PyNumber_Divide(PyObject *arg0, PyObject *arg1);
#define PyNumber_Divmod PyPyNumber_Divmod
PyAPI_FUNC(PyObject *) PyNumber_Divmod(PyObject *arg0, PyObject *arg1);
#define PyNumber_Float PyPyNumber_Float
PyAPI_FUNC(PyObject *) PyNumber_Float(PyObject *arg0);
#define PyNumber_FloorDivide PyPyNumber_FloorDivide
PyAPI_FUNC(PyObject *) PyNumber_FloorDivide(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceAdd PyPyNumber_InPlaceAdd
PyAPI_FUNC(PyObject *) PyNumber_InPlaceAdd(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceAnd PyPyNumber_InPlaceAnd
PyAPI_FUNC(PyObject *) PyNumber_InPlaceAnd(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceDivide PyPyNumber_InPlaceDivide
PyAPI_FUNC(PyObject *) PyNumber_InPlaceDivide(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceFloorDivide PyPyNumber_InPlaceFloorDivide
PyAPI_FUNC(PyObject *) PyNumber_InPlaceFloorDivide(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceLshift PyPyNumber_InPlaceLshift
PyAPI_FUNC(PyObject *) PyNumber_InPlaceLshift(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceMultiply PyPyNumber_InPlaceMultiply
PyAPI_FUNC(PyObject *) PyNumber_InPlaceMultiply(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceOr PyPyNumber_InPlaceOr
PyAPI_FUNC(PyObject *) PyNumber_InPlaceOr(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlacePower PyPyNumber_InPlacePower
PyAPI_FUNC(PyObject *) PyNumber_InPlacePower(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyNumber_InPlaceRemainder PyPyNumber_InPlaceRemainder
PyAPI_FUNC(PyObject *) PyNumber_InPlaceRemainder(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceRshift PyPyNumber_InPlaceRshift
PyAPI_FUNC(PyObject *) PyNumber_InPlaceRshift(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceSubtract PyPyNumber_InPlaceSubtract
PyAPI_FUNC(PyObject *) PyNumber_InPlaceSubtract(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceTrueDivide PyPyNumber_InPlaceTrueDivide
PyAPI_FUNC(PyObject *) PyNumber_InPlaceTrueDivide(PyObject *arg0, PyObject *arg1);
#define PyNumber_InPlaceXor PyPyNumber_InPlaceXor
PyAPI_FUNC(PyObject *) PyNumber_InPlaceXor(PyObject *arg0, PyObject *arg1);
#define PyNumber_Index PyPyNumber_Index
PyAPI_FUNC(PyObject *) PyNumber_Index(PyObject *arg0);
#define PyNumber_Int PyPyNumber_Int
PyAPI_FUNC(PyObject *) PyNumber_Int(PyObject *arg0);
#define PyNumber_Invert PyPyNumber_Invert
PyAPI_FUNC(PyObject *) PyNumber_Invert(PyObject *arg0);
#define PyNumber_Long PyPyNumber_Long
PyAPI_FUNC(PyObject *) PyNumber_Long(PyObject *arg0);
#define PyNumber_Lshift PyPyNumber_Lshift
PyAPI_FUNC(PyObject *) PyNumber_Lshift(PyObject *arg0, PyObject *arg1);
#define PyNumber_Multiply PyPyNumber_Multiply
PyAPI_FUNC(PyObject *) PyNumber_Multiply(PyObject *arg0, PyObject *arg1);
#define PyNumber_Negative PyPyNumber_Negative
PyAPI_FUNC(PyObject *) PyNumber_Negative(PyObject *arg0);
#define PyNumber_Or PyPyNumber_Or
PyAPI_FUNC(PyObject *) PyNumber_Or(PyObject *arg0, PyObject *arg1);
#define PyNumber_Positive PyPyNumber_Positive
PyAPI_FUNC(PyObject *) PyNumber_Positive(PyObject *arg0);
#define PyNumber_Power PyPyNumber_Power
PyAPI_FUNC(PyObject *) PyNumber_Power(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyNumber_Remainder PyPyNumber_Remainder
PyAPI_FUNC(PyObject *) PyNumber_Remainder(PyObject *arg0, PyObject *arg1);
#define PyNumber_Rshift PyPyNumber_Rshift
PyAPI_FUNC(PyObject *) PyNumber_Rshift(PyObject *arg0, PyObject *arg1);
#define PyNumber_Subtract PyPyNumber_Subtract
PyAPI_FUNC(PyObject *) PyNumber_Subtract(PyObject *arg0, PyObject *arg1);
#define PyNumber_ToBase PyPyNumber_ToBase
PyAPI_FUNC(PyObject *) PyNumber_ToBase(PyObject *arg0, int arg1);
#define PyNumber_TrueDivide PyPyNumber_TrueDivide
PyAPI_FUNC(PyObject *) PyNumber_TrueDivide(PyObject *arg0, PyObject *arg1);
#define PyNumber_Xor PyPyNumber_Xor
PyAPI_FUNC(PyObject *) PyNumber_Xor(PyObject *arg0, PyObject *arg1);
#define PyOS_AfterFork PyPyOS_AfterFork
PyAPI_FUNC(void) PyOS_AfterFork(void);
#define PyOS_InterruptOccurred PyPyOS_InterruptOccurred
PyAPI_FUNC(int) PyOS_InterruptOccurred(void);
#define PyOS_double_to_string PyPyOS_double_to_string
PyAPI_FUNC(char *) PyOS_double_to_string(double arg0, char arg1, int arg2, int arg3, int *arg4);
#define PyOS_string_to_double PyPyOS_string_to_double
PyAPI_FUNC(double) PyOS_string_to_double(const char *arg0, char **arg1, PyObject *arg2);
#define PyObject_AsCharBuffer PyPyObject_AsCharBuffer
PyAPI_FUNC(int) PyObject_AsCharBuffer(PyObject *arg0, const char **arg1, Signed *arg2);
#define PyObject_AsFileDescriptor PyPyObject_AsFileDescriptor
PyAPI_FUNC(int) PyObject_AsFileDescriptor(PyObject *arg0);
#define PyObject_Call PyPyObject_Call
PyAPI_FUNC(PyObject *) PyObject_Call(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyObject_CallObject PyPyObject_CallObject
PyAPI_FUNC(PyObject *) PyObject_CallObject(PyObject *arg0, PyObject *arg1);
#define PyObject_ClearWeakRefs PyPyObject_ClearWeakRefs
PyAPI_FUNC(void) PyObject_ClearWeakRefs(PyObject *arg0);
#define PyObject_Cmp PyPyObject_Cmp
PyAPI_FUNC(int) PyObject_Cmp(PyObject *arg0, PyObject *arg1, int *arg2);
#define PyObject_Compare PyPyObject_Compare
PyAPI_FUNC(int) PyObject_Compare(PyObject *arg0, PyObject *arg1);
#define PyObject_DelAttr PyPyObject_DelAttr
PyAPI_FUNC(int) PyObject_DelAttr(PyObject *arg0, PyObject *arg1);
#define PyObject_DelAttrString PyPyObject_DelAttrString
PyAPI_FUNC(int) PyObject_DelAttrString(PyObject *arg0, const char *arg1);
#define PyObject_DelItem PyPyObject_DelItem
PyAPI_FUNC(int) PyObject_DelItem(PyObject *arg0, PyObject *arg1);
#define PyObject_Dir PyPyObject_Dir
PyAPI_FUNC(PyObject *) PyObject_Dir(PyObject *arg0);
#define PyObject_Format PyPyObject_Format
PyAPI_FUNC(PyObject *) PyObject_Format(PyObject *arg0, PyObject *arg1);
#define PyObject_GenericGetAttr PyPyObject_GenericGetAttr
PyAPI_FUNC(PyObject *) PyObject_GenericGetAttr(PyObject *arg0, PyObject *arg1);
#define PyObject_GenericSetAttr PyPyObject_GenericSetAttr
PyAPI_FUNC(int) PyObject_GenericSetAttr(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyObject_GetAttr PyPyObject_GetAttr
PyAPI_FUNC(PyObject *) PyObject_GetAttr(PyObject *arg0, PyObject *arg1);
#define PyObject_GetAttrString PyPyObject_GetAttrString
PyAPI_FUNC(PyObject *) PyObject_GetAttrString(PyObject *arg0, const char *arg1);
#define PyObject_GetItem PyPyObject_GetItem
PyAPI_FUNC(PyObject *) PyObject_GetItem(PyObject *arg0, PyObject *arg1);
#define PyObject_GetIter PyPyObject_GetIter
PyAPI_FUNC(PyObject *) PyObject_GetIter(PyObject *arg0);
#define PyObject_HasAttr PyPyObject_HasAttr
PyAPI_FUNC(int) PyObject_HasAttr(PyObject *arg0, PyObject *arg1);
#define PyObject_HasAttrString PyPyObject_HasAttrString
PyAPI_FUNC(int) PyObject_HasAttrString(PyObject *arg0, const char *arg1);
#define PyObject_Hash PyPyObject_Hash
PyAPI_FUNC(Signed) PyObject_Hash(PyObject *arg0);
#define PyObject_HashNotImplemented PyPyObject_HashNotImplemented
PyAPI_FUNC(Signed) PyObject_HashNotImplemented(PyObject *arg0);
#define PyObject_IsInstance PyPyObject_IsInstance
PyAPI_FUNC(int) PyObject_IsInstance(PyObject *arg0, PyObject *arg1);
#define PyObject_IsSubclass PyPyObject_IsSubclass
PyAPI_FUNC(int) PyObject_IsSubclass(PyObject *arg0, PyObject *arg1);
#define PyObject_IsTrue PyPyObject_IsTrue
PyAPI_FUNC(int) PyObject_IsTrue(PyObject *arg0);
#define PyObject_Malloc PyPyObject_Malloc
PyAPI_FUNC(void *) PyObject_Malloc(Unsigned arg0);
#define PyObject_Not PyPyObject_Not
PyAPI_FUNC(int) PyObject_Not(PyObject *arg0);
#define PyObject_Print PyPyObject_Print
PyAPI_FUNC(int) PyObject_Print(PyObject *arg0, FILE *arg1, int arg2);
#define PyObject_Realloc PyPyObject_Realloc
PyAPI_FUNC(void *) PyObject_Realloc(void *arg0, Unsigned arg1);
#define PyObject_Repr PyPyObject_Repr
PyAPI_FUNC(PyObject *) PyObject_Repr(PyObject *arg0);
#define PyObject_RichCompare PyPyObject_RichCompare
PyAPI_FUNC(PyObject *) PyObject_RichCompare(PyObject *arg0, PyObject *arg1, int arg2);
#define PyObject_RichCompareBool PyPyObject_RichCompareBool
PyAPI_FUNC(int) PyObject_RichCompareBool(PyObject *arg0, PyObject *arg1, int arg2);
#define PyObject_SelfIter PyPyObject_SelfIter
PyAPI_FUNC(PyObject *) PyObject_SelfIter(PyObject *arg0);
#define PyObject_SetAttr PyPyObject_SetAttr
PyAPI_FUNC(int) PyObject_SetAttr(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyObject_SetAttrString PyPyObject_SetAttrString
PyAPI_FUNC(int) PyObject_SetAttrString(PyObject *arg0, const char *arg1, PyObject *arg2);
#define PyObject_SetItem PyPyObject_SetItem
PyAPI_FUNC(int) PyObject_SetItem(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyObject_Size PyPyObject_Size
PyAPI_FUNC(Signed) PyObject_Size(PyObject *arg0);
#define PyObject_Str PyPyObject_Str
PyAPI_FUNC(PyObject *) PyObject_Str(PyObject *arg0);
#define PyObject_Type PyPyObject_Type
PyAPI_FUNC(PyObject *) PyObject_Type(PyObject *arg0);
#define PyObject_Unicode PyPyObject_Unicode
PyAPI_FUNC(PyObject *) PyObject_Unicode(PyObject *arg0);
#define PyRun_File PyPyRun_File
PyAPI_FUNC(PyObject *) PyRun_File(FILE *arg0, const char *arg1, int arg2, PyObject *arg3, PyObject *arg4);
#define PyRun_SimpleString PyPyRun_SimpleString
PyAPI_FUNC(int) PyRun_SimpleString(const char *arg0);
#define PyRun_String PyPyRun_String
PyAPI_FUNC(PyObject *) PyRun_String(const char *arg0, int arg1, PyObject *arg2, PyObject *arg3);
#define PyRun_StringFlags PyPyRun_StringFlags
PyAPI_FUNC(PyObject *) PyRun_StringFlags(const char *arg0, int arg1, PyObject *arg2, PyObject *arg3, PyCompilerFlags *arg4);
#define PySeqIter_New PyPySeqIter_New
PyAPI_FUNC(PyObject *) PySeqIter_New(PyObject *arg0);
#define PySequence_Check PyPySequence_Check
PyAPI_FUNC(int) PySequence_Check(PyObject *arg0);
#define PySequence_Concat PyPySequence_Concat
PyAPI_FUNC(PyObject *) PySequence_Concat(PyObject *arg0, PyObject *arg1);
#define PySequence_Contains PyPySequence_Contains
PyAPI_FUNC(int) PySequence_Contains(PyObject *arg0, PyObject *arg1);
#define PySequence_DelItem PyPySequence_DelItem
PyAPI_FUNC(int) PySequence_DelItem(PyObject *arg0, Signed arg1);
#define PySequence_DelSlice PyPySequence_DelSlice
PyAPI_FUNC(int) PySequence_DelSlice(PyObject *arg0, Signed arg1, Signed arg2);
#define PySequence_Fast PyPySequence_Fast
PyAPI_FUNC(PyObject *) PySequence_Fast(PyObject *arg0, const char *arg1);
#define PySequence_Fast_GET_ITEM PyPySequence_Fast_GET_ITEM
PyAPI_FUNC(PyObject *) PySequence_Fast_GET_ITEM(void *arg0, Signed arg1);
#define PySequence_Fast_GET_SIZE PyPySequence_Fast_GET_SIZE
PyAPI_FUNC(Signed) PySequence_Fast_GET_SIZE(void *arg0);
#define PySequence_Fast_ITEMS PyPySequence_Fast_ITEMS
PyAPI_FUNC(PyObject **) PySequence_Fast_ITEMS(void *arg0);
#define PySequence_GetItem PyPySequence_GetItem
PyAPI_FUNC(PyObject *) PySequence_GetItem(PyObject *arg0, Signed arg1);
#define PySequence_GetSlice PyPySequence_GetSlice
PyAPI_FUNC(PyObject *) PySequence_GetSlice(PyObject *arg0, Signed arg1, Signed arg2);
#define PySequence_ITEM PyPySequence_ITEM
PyAPI_FUNC(PyObject *) PySequence_ITEM(void *arg0, Signed arg1);
#define PySequence_InPlaceConcat PyPySequence_InPlaceConcat
PyAPI_FUNC(PyObject *) PySequence_InPlaceConcat(PyObject *arg0, PyObject *arg1);
#define PySequence_InPlaceRepeat PyPySequence_InPlaceRepeat
PyAPI_FUNC(PyObject *) PySequence_InPlaceRepeat(PyObject *arg0, Signed arg1);
#define PySequence_Index PyPySequence_Index
PyAPI_FUNC(Signed) PySequence_Index(PyObject *arg0, PyObject *arg1);
#define PySequence_Length PyPySequence_Length
PyAPI_FUNC(Signed) PySequence_Length(PyObject *arg0);
#define PySequence_List PyPySequence_List
PyAPI_FUNC(PyObject *) PySequence_List(PyObject *arg0);
#define PySequence_Repeat PyPySequence_Repeat
PyAPI_FUNC(PyObject *) PySequence_Repeat(PyObject *arg0, Signed arg1);
#define PySequence_SetItem PyPySequence_SetItem
PyAPI_FUNC(int) PySequence_SetItem(PyObject *arg0, Signed arg1, PyObject *arg2);
#define PySequence_SetSlice PyPySequence_SetSlice
PyAPI_FUNC(int) PySequence_SetSlice(PyObject *arg0, Signed arg1, Signed arg2, PyObject *arg3);
#define PySequence_Size PyPySequence_Size
PyAPI_FUNC(Signed) PySequence_Size(PyObject *arg0);
#define PySequence_Tuple PyPySequence_Tuple
PyAPI_FUNC(PyObject *) PySequence_Tuple(PyObject *arg0);
#define PySet_Add PyPySet_Add
PyAPI_FUNC(int) PySet_Add(PyObject *arg0, PyObject *arg1);
#define PySet_Check PyPySet_Check
PyAPI_FUNC(int) PySet_Check(void * arg0);
#define PySet_CheckExact PyPySet_CheckExact
PyAPI_FUNC(int) PySet_CheckExact(void * arg0);
#define PySet_Clear PyPySet_Clear
PyAPI_FUNC(int) PySet_Clear(PyObject *arg0);
#define PySet_Contains PyPySet_Contains
PyAPI_FUNC(int) PySet_Contains(PyObject *arg0, PyObject *arg1);
#define PySet_Discard PyPySet_Discard
PyAPI_FUNC(int) PySet_Discard(PyObject *arg0, PyObject *arg1);
#define PySet_GET_SIZE PyPySet_GET_SIZE
PyAPI_FUNC(Signed) PySet_GET_SIZE(void *arg0);
#define PySet_New PyPySet_New
PyAPI_FUNC(PyObject *) PySet_New(PyObject *arg0);
#define PySet_Pop PyPySet_Pop
PyAPI_FUNC(PyObject *) PySet_Pop(PyObject *arg0);
#define PySet_Size PyPySet_Size
PyAPI_FUNC(Signed) PySet_Size(PyObject *arg0);
#define PySlice_GetIndices PyPySlice_GetIndices
PyAPI_FUNC(int) PySlice_GetIndices(PySliceObject *arg0, Signed arg1, Signed *arg2, Signed *arg3, Signed *arg4);
#define PySlice_GetIndicesEx PyPySlice_GetIndicesEx
PyAPI_FUNC(int) PySlice_GetIndicesEx(PySliceObject *arg0, Signed arg1, Signed *arg2, Signed *arg3, Signed *arg4, Signed *arg5);
#define PySlice_New PyPySlice_New
PyAPI_FUNC(PyObject *) PySlice_New(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyStaticMethod_New PyPyStaticMethod_New
PyAPI_FUNC(PyObject *) PyStaticMethod_New(PyObject *arg0);
#define PyString_AS_STRING PyPyString_AS_STRING
PyAPI_FUNC(char *) PyString_AS_STRING(void *arg0);
#define PyString_AsDecodedObject PyPyString_AsDecodedObject
PyAPI_FUNC(PyObject *) PyString_AsDecodedObject(PyObject *arg0, const char *arg1, const char *arg2);
#define PyString_AsEncodedObject PyPyString_AsEncodedObject
PyAPI_FUNC(PyObject *) PyString_AsEncodedObject(PyObject *arg0, const char *arg1, const char *arg2);
#define PyString_AsString PyPyString_AsString
PyAPI_FUNC(char *) PyString_AsString(PyObject *arg0);
#define PyString_AsStringAndSize PyPyString_AsStringAndSize
PyAPI_FUNC(int) PyString_AsStringAndSize(PyObject *arg0, char **arg1, Signed *arg2);
#define PyString_Concat PyPyString_Concat
PyAPI_FUNC(void) PyString_Concat(PyObject **arg0, PyObject *arg1);
#define PyString_ConcatAndDel PyPyString_ConcatAndDel
PyAPI_FUNC(void) PyString_ConcatAndDel(PyObject **arg0, PyObject *arg1);
#define PyString_Format PyPyString_Format
PyAPI_FUNC(PyObject *) PyString_Format(PyObject *arg0, PyObject *arg1);
#define PyString_FromString PyPyString_FromString
PyAPI_FUNC(PyObject *) PyString_FromString(const char *arg0);
#define PyString_FromStringAndSize PyPyString_FromStringAndSize
PyAPI_FUNC(PyObject *) PyString_FromStringAndSize(const char *arg0, Signed arg1);
#define PyString_InternFromString PyPyString_InternFromString
PyAPI_FUNC(PyObject *) PyString_InternFromString(const char *arg0);
#define PyString_InternInPlace PyPyString_InternInPlace
PyAPI_FUNC(void) PyString_InternInPlace(PyObject **arg0);
#define PyString_Size PyPyString_Size
PyAPI_FUNC(Signed) PyString_Size(PyObject *arg0);
#define PySys_GetObject PyPySys_GetObject
PyAPI_FUNC(PyObject *) PySys_GetObject(const char *arg0);
#define PySys_SetObject PyPySys_SetObject
PyAPI_FUNC(int) PySys_SetObject(const char *arg0, PyObject *arg1);
#define PyTZInfo_Check PyPyTZInfo_Check
PyAPI_FUNC(int) PyTZInfo_Check(PyObject *arg0);
#define PyTZInfo_CheckExact PyPyTZInfo_CheckExact
PyAPI_FUNC(int) PyTZInfo_CheckExact(PyObject *arg0);
#define PyThreadState_Clear PyPyThreadState_Clear
PyAPI_FUNC(void) PyThreadState_Clear(PyThreadState *arg0);
#define PyThreadState_Delete PyPyThreadState_Delete
PyAPI_FUNC(void) PyThreadState_Delete(PyThreadState *arg0);
#define PyThreadState_DeleteCurrent PyPyThreadState_DeleteCurrent
PyAPI_FUNC(void) PyThreadState_DeleteCurrent(void);
#define PyThreadState_Get PyPyThreadState_Get
PyAPI_FUNC(PyThreadState *) PyThreadState_Get(void);
#define PyThreadState_GetDict PyPyThreadState_GetDict
PyAPI_FUNC(PyObject *) PyThreadState_GetDict(void);
#define PyThreadState_New PyPyThreadState_New
PyAPI_FUNC(PyThreadState *) PyThreadState_New(PyInterpreterState *arg0);
#define PyThreadState_Swap PyPyThreadState_Swap
PyAPI_FUNC(PyThreadState *) PyThreadState_Swap(PyThreadState *arg0);
#define PyTime_Check PyPyTime_Check
PyAPI_FUNC(int) PyTime_Check(PyObject *arg0);
#define PyTime_CheckExact PyPyTime_CheckExact
PyAPI_FUNC(int) PyTime_CheckExact(PyObject *arg0);
#define PyTraceBack_Check PyPyTraceBack_Check
PyAPI_FUNC(int) PyTraceBack_Check(PyObject *arg0);
#define PyTraceBack_Here PyPyTraceBack_Here
PyAPI_FUNC(int) PyTraceBack_Here(PyFrameObject *arg0);
#define PyTraceBack_Print PyPyTraceBack_Print
PyAPI_FUNC(int) PyTraceBack_Print(PyObject *arg0, PyObject *arg1);
#define PyTuple_GetItem PyPyTuple_GetItem
PyAPI_FUNC(PyObject *) PyTuple_GetItem(PyObject *arg0, Signed arg1);
#define PyTuple_GetSlice PyPyTuple_GetSlice
PyAPI_FUNC(PyObject *) PyTuple_GetSlice(PyObject *arg0, Signed arg1, Signed arg2);
#define PyTuple_SetItem PyPyTuple_SetItem
PyAPI_FUNC(int) PyTuple_SetItem(PyObject *arg0, Signed arg1, PyObject *arg2);
#define PyTuple_Size PyPyTuple_Size
PyAPI_FUNC(Signed) PyTuple_Size(PyObject *arg0);
#define PyType_GenericNew PyPyType_GenericNew
PyAPI_FUNC(PyObject *) PyType_GenericNew(PyTypeObject *arg0, PyObject *arg1, PyObject *arg2);
#define PyType_IsSubtype PyPyType_IsSubtype
PyAPI_FUNC(int) PyType_IsSubtype(PyTypeObject *arg0, PyTypeObject *arg1);
#define PyType_Modified PyPyType_Modified
PyAPI_FUNC(void) PyType_Modified(PyTypeObject *arg0);
#define PyType_Ready PyPyType_Ready
PyAPI_FUNC(int) PyType_Ready(PyTypeObject *arg0);
#define PyUnicode_AS_DATA PyPyUnicode_AS_DATA
PyAPI_FUNC(char *) PyUnicode_AS_DATA(void *arg0);
#define PyUnicode_AS_UNICODE PyPyUnicode_AS_UNICODE
PyAPI_FUNC(wchar_t *) PyUnicode_AS_UNICODE(void *arg0);
#define PyUnicode_AsASCIIString PyPyUnicode_AsASCIIString
PyAPI_FUNC(PyObject *) PyUnicode_AsASCIIString(PyObject *arg0);
#define PyUnicode_AsEncodedObject PyPyUnicode_AsEncodedObject
PyAPI_FUNC(PyObject *) PyUnicode_AsEncodedObject(PyObject *arg0, const char *arg1, const char *arg2);
#define PyUnicode_AsEncodedString PyPyUnicode_AsEncodedString
PyAPI_FUNC(PyObject *) PyUnicode_AsEncodedString(PyObject *arg0, const char *arg1, const char *arg2);
#define PyUnicode_AsLatin1String PyPyUnicode_AsLatin1String
PyAPI_FUNC(PyObject *) PyUnicode_AsLatin1String(PyObject *arg0);
#define PyUnicode_AsUTF16String PyPyUnicode_AsUTF16String
PyAPI_FUNC(PyObject *) PyUnicode_AsUTF16String(PyObject *arg0);
#define PyUnicode_AsUTF32String PyPyUnicode_AsUTF32String
PyAPI_FUNC(PyObject *) PyUnicode_AsUTF32String(PyObject *arg0);
#define PyUnicode_AsUTF8String PyPyUnicode_AsUTF8String
PyAPI_FUNC(PyObject *) PyUnicode_AsUTF8String(PyObject *arg0);
#define PyUnicode_AsUnicode PyPyUnicode_AsUnicode
PyAPI_FUNC(wchar_t *) PyUnicode_AsUnicode(PyObject *arg0);
#define PyUnicode_AsUnicodeEscapeString PyPyUnicode_AsUnicodeEscapeString
PyAPI_FUNC(PyObject *) PyUnicode_AsUnicodeEscapeString(PyObject *arg0);
#define PyUnicode_AsWideChar PyPyUnicode_AsWideChar
PyAPI_FUNC(Signed) PyUnicode_AsWideChar(PyUnicodeObject *arg0, wchar_t *arg1, Signed arg2);
#define PyUnicode_Compare PyPyUnicode_Compare
PyAPI_FUNC(int) PyUnicode_Compare(PyObject *arg0, PyObject *arg1);
#define PyUnicode_Concat PyPyUnicode_Concat
PyAPI_FUNC(PyObject *) PyUnicode_Concat(PyObject *arg0, PyObject *arg1);
#define PyUnicode_Count PyPyUnicode_Count
PyAPI_FUNC(Signed) PyUnicode_Count(PyObject *arg0, PyObject *arg1, Signed arg2, Signed arg3);
#define PyUnicode_Decode PyPyUnicode_Decode
PyAPI_FUNC(PyObject *) PyUnicode_Decode(const char *arg0, Signed arg1, const char *arg2, const char *arg3);
#define PyUnicode_DecodeASCII PyPyUnicode_DecodeASCII
PyAPI_FUNC(PyObject *) PyUnicode_DecodeASCII(const char *arg0, Signed arg1, const char *arg2);
#define PyUnicode_DecodeLatin1 PyPyUnicode_DecodeLatin1
PyAPI_FUNC(PyObject *) PyUnicode_DecodeLatin1(const char *arg0, Signed arg1, const char *arg2);
#define PyUnicode_DecodeUTF16 PyPyUnicode_DecodeUTF16
PyAPI_FUNC(PyObject *) PyUnicode_DecodeUTF16(const char *arg0, Signed arg1, const char *arg2, int *arg3);
#define PyUnicode_DecodeUTF32 PyPyUnicode_DecodeUTF32
PyAPI_FUNC(PyObject *) PyUnicode_DecodeUTF32(const char *arg0, Signed arg1, const char *arg2, int *arg3);
#define PyUnicode_DecodeUTF8 PyPyUnicode_DecodeUTF8
PyAPI_FUNC(PyObject *) PyUnicode_DecodeUTF8(const char *arg0, Signed arg1, const char *arg2);
#define PyUnicode_EncodeASCII PyPyUnicode_EncodeASCII
PyAPI_FUNC(PyObject *) PyUnicode_EncodeASCII(const wchar_t *arg0, Signed arg1, const char *arg2);
#define PyUnicode_EncodeDecimal PyPyUnicode_EncodeDecimal
PyAPI_FUNC(int) PyUnicode_EncodeDecimal(wchar_t *arg0, Signed arg1, char *arg2, const char *arg3);
#define PyUnicode_EncodeLatin1 PyPyUnicode_EncodeLatin1
PyAPI_FUNC(PyObject *) PyUnicode_EncodeLatin1(const wchar_t *arg0, Signed arg1, const char *arg2);
#define PyUnicode_EncodeUTF8 PyPyUnicode_EncodeUTF8
PyAPI_FUNC(PyObject *) PyUnicode_EncodeUTF8(const wchar_t *arg0, Signed arg1, const char *arg2);
#define PyUnicode_Find PyPyUnicode_Find
PyAPI_FUNC(Signed) PyUnicode_Find(PyObject *arg0, PyObject *arg1, Signed arg2, Signed arg3, int arg4);
#define PyUnicode_Format PyPyUnicode_Format
PyAPI_FUNC(PyObject *) PyUnicode_Format(PyObject *arg0, PyObject *arg1);
#define PyUnicode_FromEncodedObject PyPyUnicode_FromEncodedObject
PyAPI_FUNC(PyObject *) PyUnicode_FromEncodedObject(PyObject *arg0, const char *arg1, const char *arg2);
#define PyUnicode_FromObject PyPyUnicode_FromObject
PyAPI_FUNC(PyObject *) PyUnicode_FromObject(PyObject *arg0);
#define PyUnicode_FromOrdinal PyPyUnicode_FromOrdinal
PyAPI_FUNC(PyObject *) PyUnicode_FromOrdinal(int arg0);
#define PyUnicode_FromString PyPyUnicode_FromString
PyAPI_FUNC(PyObject *) PyUnicode_FromString(const char *arg0);
#define PyUnicode_FromStringAndSize PyPyUnicode_FromStringAndSize
PyAPI_FUNC(PyObject *) PyUnicode_FromStringAndSize(const char *arg0, Signed arg1);
#define PyUnicode_FromUnicode PyPyUnicode_FromUnicode
PyAPI_FUNC(PyObject *) PyUnicode_FromUnicode(const wchar_t *arg0, Signed arg1);
#define PyUnicode_FromWideChar PyPyUnicode_FromWideChar
PyAPI_FUNC(PyObject *) PyUnicode_FromWideChar(const wchar_t *arg0, Signed arg1);
#define PyUnicode_GET_DATA_SIZE PyPyUnicode_GET_DATA_SIZE
PyAPI_FUNC(Signed) PyUnicode_GET_DATA_SIZE(void *arg0);
#define PyUnicode_GET_SIZE PyPyUnicode_GET_SIZE
PyAPI_FUNC(Signed) PyUnicode_GET_SIZE(void *arg0);
#define PyUnicode_GetDefaultEncoding PyPyUnicode_GetDefaultEncoding
PyAPI_FUNC(char *) PyUnicode_GetDefaultEncoding(void);
#define PyUnicode_GetMax PyPyUnicode_GetMax
PyAPI_FUNC(wchar_t) PyUnicode_GetMax(void);
#define PyUnicode_GetSize PyPyUnicode_GetSize
PyAPI_FUNC(Signed) PyUnicode_GetSize(PyObject *arg0);
#define PyUnicode_Join PyPyUnicode_Join
PyAPI_FUNC(PyObject *) PyUnicode_Join(PyObject *arg0, PyObject *arg1);
#define PyUnicode_Replace PyPyUnicode_Replace
PyAPI_FUNC(PyObject *) PyUnicode_Replace(PyObject *arg0, PyObject *arg1, PyObject *arg2, Signed arg3);
#define PyUnicode_Resize PyPyUnicode_Resize
PyAPI_FUNC(int) PyUnicode_Resize(PyObject **arg0, Signed arg1);
#define PyUnicode_SetDefaultEncoding PyPyUnicode_SetDefaultEncoding
PyAPI_FUNC(int) PyUnicode_SetDefaultEncoding(const char *arg0);
#define PyUnicode_Split PyPyUnicode_Split
PyAPI_FUNC(PyObject *) PyUnicode_Split(PyObject *arg0, PyObject *arg1, Signed arg2);
#define PyUnicode_Splitlines PyPyUnicode_Splitlines
PyAPI_FUNC(PyObject *) PyUnicode_Splitlines(PyObject *arg0, int arg1);
#define PyUnicode_Tailmatch PyPyUnicode_Tailmatch
PyAPI_FUNC(int) PyUnicode_Tailmatch(PyObject *arg0, PyObject *arg1, Signed arg2, Signed arg3, int arg4);
#define PyWeakref_Check PyPyWeakref_Check
PyAPI_FUNC(int) PyWeakref_Check(PyObject *arg0);
#define PyWeakref_CheckProxy PyPyWeakref_CheckProxy
PyAPI_FUNC(int) PyWeakref_CheckProxy(PyObject *arg0);
#define PyWeakref_CheckRef PyPyWeakref_CheckRef
PyAPI_FUNC(int) PyWeakref_CheckRef(PyObject *arg0);
#define PyWeakref_CheckRefExact PyPyWeakref_CheckRefExact
PyAPI_FUNC(int) PyWeakref_CheckRefExact(PyObject *arg0);
#define PyWeakref_GET_OBJECT PyPyWeakref_GET_OBJECT
PyAPI_FUNC(PyObject *) PyWeakref_GET_OBJECT(void *arg0);
#define PyWeakref_GetObject PyPyWeakref_GetObject
PyAPI_FUNC(PyObject *) PyWeakref_GetObject(PyObject *arg0);
#define PyWeakref_LockObject PyPyWeakref_LockObject
PyAPI_FUNC(PyObject *) PyWeakref_LockObject(PyObject *arg0);
#define PyWeakref_NewProxy PyPyWeakref_NewProxy
PyAPI_FUNC(PyObject *) PyWeakref_NewProxy(PyObject *arg0, PyObject *arg1);
#define PyWeakref_NewRef PyPyWeakref_NewRef
PyAPI_FUNC(PyObject *) PyWeakref_NewRef(PyObject *arg0, PyObject *arg1);
#define Py_AddPendingCall PyPy_AddPendingCall
PyAPI_FUNC(int) Py_AddPendingCall(int (*arg0)(void *), void *arg1);
#define Py_AtExit PyPy_AtExit
PyAPI_FUNC(int) Py_AtExit(void (*arg0)(void));
#define Py_CompileStringFlags PyPy_CompileStringFlags
PyAPI_FUNC(PyObject *) Py_CompileStringFlags(const char *arg0, const char *arg1, int arg2, PyCompilerFlags *arg3);
#define Py_DecRef PyPy_DecRef
PyAPI_FUNC(void) Py_DecRef(PyObject *arg0);
#define Py_EnterRecursiveCall PyPy_EnterRecursiveCall
PyAPI_FUNC(int) Py_EnterRecursiveCall(char *arg0);
#define Py_FindMethod PyPy_FindMethod
PyAPI_FUNC(PyObject *) Py_FindMethod(PyMethodDef *arg0, PyObject *arg1, const char *arg2);
#define Py_GetProgramName PyPy_GetProgramName
PyAPI_FUNC(char *) Py_GetProgramName(void);
#define Py_GetRecursionLimit PyPy_GetRecursionLimit
PyAPI_FUNC(int) Py_GetRecursionLimit(void);
#define Py_GetVersion PyPy_GetVersion
PyAPI_FUNC(char *) Py_GetVersion(void);
#define Py_IncRef PyPy_IncRef
PyAPI_FUNC(void) Py_IncRef(PyObject *arg0);
#define Py_IsInitialized PyPy_IsInitialized
PyAPI_FUNC(int) Py_IsInitialized(void);
#define Py_LeaveRecursiveCall PyPy_LeaveRecursiveCall
PyAPI_FUNC(void) Py_LeaveRecursiveCall(void);
#define Py_MakePendingCalls PyPy_MakePendingCalls
PyAPI_FUNC(int) Py_MakePendingCalls(void);
#define Py_ReprEnter PyPy_ReprEnter
PyAPI_FUNC(int) Py_ReprEnter(PyObject *arg0);
#define Py_ReprLeave PyPy_ReprLeave
PyAPI_FUNC(void) Py_ReprLeave(PyObject *arg0);
#define Py_SetRecursionLimit PyPy_SetRecursionLimit
PyAPI_FUNC(void) Py_SetRecursionLimit(int arg0);
#define Py_UNICODE_COPY PyPy_UNICODE_COPY
PyAPI_FUNC(void) Py_UNICODE_COPY(wchar_t *arg0, wchar_t *arg1, Signed arg2);
#define Py_UNICODE_ISALNUM PyPy_UNICODE_ISALNUM
PyAPI_FUNC(int) Py_UNICODE_ISALNUM(wchar_t arg0);
#define Py_UNICODE_ISALPHA PyPy_UNICODE_ISALPHA
PyAPI_FUNC(int) Py_UNICODE_ISALPHA(wchar_t arg0);
#define Py_UNICODE_ISDECIMAL PyPy_UNICODE_ISDECIMAL
PyAPI_FUNC(int) Py_UNICODE_ISDECIMAL(wchar_t arg0);
#define Py_UNICODE_ISDIGIT PyPy_UNICODE_ISDIGIT
PyAPI_FUNC(int) Py_UNICODE_ISDIGIT(wchar_t arg0);
#define Py_UNICODE_ISLINEBREAK PyPy_UNICODE_ISLINEBREAK
PyAPI_FUNC(int) Py_UNICODE_ISLINEBREAK(wchar_t arg0);
#define Py_UNICODE_ISLOWER PyPy_UNICODE_ISLOWER
PyAPI_FUNC(int) Py_UNICODE_ISLOWER(wchar_t arg0);
#define Py_UNICODE_ISNUMERIC PyPy_UNICODE_ISNUMERIC
PyAPI_FUNC(int) Py_UNICODE_ISNUMERIC(wchar_t arg0);
#define Py_UNICODE_ISSPACE PyPy_UNICODE_ISSPACE
PyAPI_FUNC(int) Py_UNICODE_ISSPACE(wchar_t arg0);
#define Py_UNICODE_ISTITLE PyPy_UNICODE_ISTITLE
PyAPI_FUNC(int) Py_UNICODE_ISTITLE(wchar_t arg0);
#define Py_UNICODE_ISUPPER PyPy_UNICODE_ISUPPER
PyAPI_FUNC(int) Py_UNICODE_ISUPPER(wchar_t arg0);
#define Py_UNICODE_TODECIMAL PyPy_UNICODE_TODECIMAL
PyAPI_FUNC(int) Py_UNICODE_TODECIMAL(wchar_t arg0);
#define Py_UNICODE_TODIGIT PyPy_UNICODE_TODIGIT
PyAPI_FUNC(int) Py_UNICODE_TODIGIT(wchar_t arg0);
#define Py_UNICODE_TOLOWER PyPy_UNICODE_TOLOWER
PyAPI_FUNC(wchar_t) Py_UNICODE_TOLOWER(wchar_t arg0);
#define Py_UNICODE_TONUMERIC PyPy_UNICODE_TONUMERIC
PyAPI_FUNC(double) Py_UNICODE_TONUMERIC(wchar_t arg0);
#define Py_UNICODE_TOTITLE PyPy_UNICODE_TOTITLE
PyAPI_FUNC(wchar_t) Py_UNICODE_TOTITLE(wchar_t arg0);
#define Py_UNICODE_TOUPPER PyPy_UNICODE_TOUPPER
PyAPI_FUNC(wchar_t) Py_UNICODE_TOUPPER(wchar_t arg0);
#define _PyComplex_AsCComplex _PyPyComplex_AsCComplex
PyAPI_FUNC(int) _PyComplex_AsCComplex(PyObject *arg0, struct Py_complex_t *arg1);
#define _PyComplex_FromCComplex _PyPyComplex_FromCComplex
PyAPI_FUNC(PyObject *) _PyComplex_FromCComplex(struct Py_complex_t *arg0);
#define _PyDateTime_FromDateAndTime _PyPyDateTime_FromDateAndTime
PyAPI_FUNC(PyObject *) _PyDateTime_FromDateAndTime(int arg0, int arg1, int arg2, int arg3, int arg4, int arg5, int arg6, PyObject *arg7, PyTypeObject *arg8);
#define _PyDateTime_FromTimestamp _PyPyDateTime_FromTimestamp
PyAPI_FUNC(PyObject *) _PyDateTime_FromTimestamp(PyObject *arg0, PyObject *arg1, PyObject *arg2);
#define _PyDateTime_Import _PyPyDateTime_Import
PyAPI_FUNC(PyDateTime_CAPI *) _PyDateTime_Import(void);
#define _PyDate_FromDate _PyPyDate_FromDate
PyAPI_FUNC(PyObject *) _PyDate_FromDate(int arg0, int arg1, int arg2, PyTypeObject *arg3);
#define _PyDate_FromTimestamp _PyPyDate_FromTimestamp
PyAPI_FUNC(PyObject *) _PyDate_FromTimestamp(PyObject *arg0, PyObject *arg1);
#define _PyDelta_FromDelta _PyPyDelta_FromDelta
PyAPI_FUNC(PyObject *) _PyDelta_FromDelta(int arg0, int arg1, int arg2, int arg3, PyTypeObject *arg4);
#define _PyDict_GetItemWithError _PyPyDict_GetItemWithError
PyAPI_FUNC(PyObject *) _PyDict_GetItemWithError(PyObject *arg0, PyObject *arg1);
#define _PyEval_SliceIndex _PyPyEval_SliceIndex
PyAPI_FUNC(int) _PyEval_SliceIndex(PyObject *arg0, Signed *arg1);
#define _PyFloat_Unpack4 _PyPyFloat_Unpack4
PyAPI_FUNC(double) _PyFloat_Unpack4(const char *arg0, int arg1);
#define _PyFloat_Unpack8 _PyPyFloat_Unpack8
PyAPI_FUNC(double) _PyFloat_Unpack8(const char *arg0, int arg1);
#define _PyImport_AcquireLock _PyPyImport_AcquireLock
PyAPI_FUNC(void) _PyImport_AcquireLock(void);
#define _PyImport_ReleaseLock _PyPyImport_ReleaseLock
PyAPI_FUNC(int) _PyImport_ReleaseLock(void);
#define _PyInstance_Lookup _PyPyInstance_Lookup
PyAPI_FUNC(PyObject *) _PyInstance_Lookup(PyObject *arg0, PyObject *arg1);
#define _PyLong_AsByteArrayO _PyPyLong_AsByteArrayO
PyAPI_FUNC(int) _PyLong_AsByteArrayO(PyObject *arg0, unsigned char *arg1, Unsigned arg2, int arg3, int arg4);
#define _PyLong_FromByteArray _PyPyLong_FromByteArray
PyAPI_FUNC(PyObject *) _PyLong_FromByteArray(const unsigned char *arg0, Unsigned arg1, int arg2, int arg3);
#define _PyLong_NumBits _PyPyLong_NumBits
PyAPI_FUNC(Unsigned) _PyLong_NumBits(PyObject *arg0);
#define _PyLong_Sign _PyPyLong_Sign
PyAPI_FUNC(int) _PyLong_Sign(PyObject *arg0);
#define _PyObject_GetDictPtr _PyPyObject_GetDictPtr
PyAPI_FUNC(PyObject **) _PyObject_GetDictPtr(PyObject *arg0);
#define _PyPyGC_AddMemoryPressure _PyPyPyGC_AddMemoryPressure
PyAPI_FUNC(void) _PyPyGC_AddMemoryPressure(Signed arg0);
#define _PyPy_Free _PyPyPy_Free
extern void _PyPy_Free(void *arg0);
#define _PyPy_Malloc _PyPyPy_Malloc
extern void * _PyPy_Malloc(Signed arg0);
#define _PySet_Next _PyPySet_Next
PyAPI_FUNC(int) _PySet_Next(PyObject *arg0, Signed *arg1, PyObject **arg2);
#define _PySet_NextEntry _PyPySet_NextEntry
PyAPI_FUNC(int) _PySet_NextEntry(PyObject *arg0, Signed *arg1, PyObject **arg2, Signed *arg3);
#define _PyString_Eq _PyPyString_Eq
PyAPI_FUNC(int) _PyString_Eq(PyObject *arg0, PyObject *arg1);
#define _PyString_Join _PyPyString_Join
PyAPI_FUNC(PyObject *) _PyString_Join(PyObject *arg0, PyObject *arg1);
#define _PyString_Resize _PyPyString_Resize
PyAPI_FUNC(int) _PyString_Resize(PyObject **arg0, Signed arg1);
#define _PyTime_FromTime _PyPyTime_FromTime
PyAPI_FUNC(PyObject *) _PyTime_FromTime(int arg0, int arg1, int arg2, int arg3, PyObject *arg4, PyTypeObject *arg5);
#define _PyTuple_Resize _PyPyTuple_Resize
PyAPI_FUNC(int) _PyTuple_Resize(PyObject **arg0, Signed arg1);
#define _PyType_Lookup _PyPyType_Lookup
PyAPI_FUNC(PyObject *) _PyType_Lookup(PyTypeObject *arg0, PyObject *arg1);
#define _PyUnicode_AsDefaultEncodedString _PyPyUnicode_AsDefaultEncodedString
PyAPI_FUNC(PyObject *) _PyUnicode_AsDefaultEncodedString(PyObject *arg0, const char *arg1);
#define _Py_HashDouble _PyPy_HashDouble
PyAPI_FUNC(Signed) _Py_HashDouble(double arg0);
#define _Py_HashPointer _PyPy_HashPointer
PyAPI_FUNC(Signed) _Py_HashPointer(void *arg0);
#define _Py_InitPyPyModule _PyPy_InitPyPyModule
PyAPI_FUNC(PyObject *) _Py_InitPyPyModule(const char *arg0, PyMethodDef *arg1, const char *arg2, PyObject *arg3, int arg4);
#define _Py_NoneStruct _PyPy_NoneStruct
PyAPI_DATA(PyObject) _Py_NoneStruct;
#define _Py_TrueStruct _PyPy_TrueStruct
PyAPI_DATA(PyIntObject) _Py_TrueStruct;
#define _Py_ZeroStruct _PyPy_ZeroStruct
PyAPI_DATA(PyIntObject) _Py_ZeroStruct;
#define _Py_NotImplementedStruct _PyPy_NotImplementedStruct
PyAPI_DATA(PyObject) _Py_NotImplementedStruct;
#define _Py_EllipsisObject _PyPy_EllipsisObject
PyAPI_DATA(PyObject) _Py_EllipsisObject;
#define PyDateTimeAPI PyPyDateTimeAPI
PyAPI_DATA(PyDateTime_CAPI*) PyDateTimeAPI;
#define PyExc_ArithmeticError PyPyExc_ArithmeticError
PyAPI_DATA(PyObject*) PyExc_ArithmeticError;
#define PyExc_AssertionError PyPyExc_AssertionError
PyAPI_DATA(PyObject*) PyExc_AssertionError;
#define PyExc_AttributeError PyPyExc_AttributeError
PyAPI_DATA(PyObject*) PyExc_AttributeError;
#define PyExc_BaseException PyPyExc_BaseException
PyAPI_DATA(PyObject*) PyExc_BaseException;
#define PyExc_BufferError PyPyExc_BufferError
PyAPI_DATA(PyObject*) PyExc_BufferError;
#define PyExc_BytesWarning PyPyExc_BytesWarning
PyAPI_DATA(PyObject*) PyExc_BytesWarning;
#define PyExc_DeprecationWarning PyPyExc_DeprecationWarning
PyAPI_DATA(PyObject*) PyExc_DeprecationWarning;
#define PyExc_EOFError PyPyExc_EOFError
PyAPI_DATA(PyObject*) PyExc_EOFError;
#define PyExc_EnvironmentError PyPyExc_EnvironmentError
PyAPI_DATA(PyObject*) PyExc_EnvironmentError;
#define PyExc_Exception PyPyExc_Exception
PyAPI_DATA(PyObject*) PyExc_Exception;
#define PyExc_FloatingPointError PyPyExc_FloatingPointError
PyAPI_DATA(PyObject*) PyExc_FloatingPointError;
#define PyExc_FutureWarning PyPyExc_FutureWarning
PyAPI_DATA(PyObject*) PyExc_FutureWarning;
#define PyExc_GeneratorExit PyPyExc_GeneratorExit
PyAPI_DATA(PyObject*) PyExc_GeneratorExit;
#define PyExc_IOError PyPyExc_IOError
PyAPI_DATA(PyObject*) PyExc_IOError;
#define PyExc_ImportError PyPyExc_ImportError
PyAPI_DATA(PyObject*) PyExc_ImportError;
#define PyExc_ImportWarning PyPyExc_ImportWarning
PyAPI_DATA(PyObject*) PyExc_ImportWarning;
#define PyExc_IndentationError PyPyExc_IndentationError
PyAPI_DATA(PyObject*) PyExc_IndentationError;
#define PyExc_IndexError PyPyExc_IndexError
PyAPI_DATA(PyObject*) PyExc_IndexError;
#define PyExc_KeyError PyPyExc_KeyError
PyAPI_DATA(PyObject*) PyExc_KeyError;
#define PyExc_KeyboardInterrupt PyPyExc_KeyboardInterrupt
PyAPI_DATA(PyObject*) PyExc_KeyboardInterrupt;
#define PyExc_LookupError PyPyExc_LookupError
PyAPI_DATA(PyObject*) PyExc_LookupError;
#define PyExc_MemoryError PyPyExc_MemoryError
PyAPI_DATA(PyObject*) PyExc_MemoryError;
#define PyExc_NameError PyPyExc_NameError
PyAPI_DATA(PyObject*) PyExc_NameError;
#define PyExc_NotImplementedError PyPyExc_NotImplementedError
PyAPI_DATA(PyObject*) PyExc_NotImplementedError;
#define PyExc_OSError PyPyExc_OSError
PyAPI_DATA(PyObject*) PyExc_OSError;
#define PyExc_OverflowError PyPyExc_OverflowError
PyAPI_DATA(PyObject*) PyExc_OverflowError;
#define PyExc_PendingDeprecationWarning PyPyExc_PendingDeprecationWarning
PyAPI_DATA(PyObject*) PyExc_PendingDeprecationWarning;
#define PyExc_ReferenceError PyPyExc_ReferenceError
PyAPI_DATA(PyObject*) PyExc_ReferenceError;
#define PyExc_RuntimeError PyPyExc_RuntimeError
PyAPI_DATA(PyObject*) PyExc_RuntimeError;
#define PyExc_RuntimeWarning PyPyExc_RuntimeWarning
PyAPI_DATA(PyObject*) PyExc_RuntimeWarning;
#define PyExc_StandardError PyPyExc_StandardError
PyAPI_DATA(PyObject*) PyExc_StandardError;
#define PyExc_StopIteration PyPyExc_StopIteration
PyAPI_DATA(PyObject*) PyExc_StopIteration;
#define PyExc_SyntaxError PyPyExc_SyntaxError
PyAPI_DATA(PyObject*) PyExc_SyntaxError;
#define PyExc_SyntaxWarning PyPyExc_SyntaxWarning
PyAPI_DATA(PyObject*) PyExc_SyntaxWarning;
#define PyExc_SystemExit PyPyExc_SystemExit
PyAPI_DATA(PyObject*) PyExc_SystemExit;
#define PyExc_SystemError PyPyExc_SystemError
PyAPI_DATA(PyObject*) PyExc_SystemError;
#define PyExc_TabError PyPyExc_TabError
PyAPI_DATA(PyObject*) PyExc_TabError;
#define PyExc_TypeError PyPyExc_TypeError
PyAPI_DATA(PyObject*) PyExc_TypeError;
#define PyExc_UnboundLocalError PyPyExc_UnboundLocalError
PyAPI_DATA(PyObject*) PyExc_UnboundLocalError;
#define PyExc_UnicodeDecodeError PyPyExc_UnicodeDecodeError
PyAPI_DATA(PyObject*) PyExc_UnicodeDecodeError;
#define PyExc_UnicodeEncodeError PyPyExc_UnicodeEncodeError
PyAPI_DATA(PyObject*) PyExc_UnicodeEncodeError;
#define PyExc_UnicodeError PyPyExc_UnicodeError
PyAPI_DATA(PyObject*) PyExc_UnicodeError;
#define PyExc_UnicodeTranslateError PyPyExc_UnicodeTranslateError
PyAPI_DATA(PyObject*) PyExc_UnicodeTranslateError;
#define PyExc_UnicodeWarning PyPyExc_UnicodeWarning
PyAPI_DATA(PyObject*) PyExc_UnicodeWarning;
#define PyExc_UserWarning PyPyExc_UserWarning
PyAPI_DATA(PyObject*) PyExc_UserWarning;
#define PyExc_ValueError PyPyExc_ValueError
PyAPI_DATA(PyObject*) PyExc_ValueError;
#define PyExc_Warning PyPyExc_Warning
PyAPI_DATA(PyObject*) PyExc_Warning;
#define PyExc_ZeroDivisionError PyPyExc_ZeroDivisionError
PyAPI_DATA(PyObject*) PyExc_ZeroDivisionError;
#define PyType_Type PyPyType_Type
PyAPI_DATA(PyTypeObject) PyType_Type;
#define PyString_Type PyPyString_Type
PyAPI_DATA(PyTypeObject) PyString_Type;
#define PyUnicode_Type PyPyUnicode_Type
PyAPI_DATA(PyTypeObject) PyUnicode_Type;
#define PyBaseString_Type PyPyBaseString_Type
PyAPI_DATA(PyTypeObject) PyBaseString_Type;
#define PyDict_Type PyPyDict_Type
PyAPI_DATA(PyTypeObject) PyDict_Type;
#define PyDictProxy_Type PyPyDictProxy_Type
PyAPI_DATA(PyTypeObject) PyDictProxy_Type;
#define PyTuple_Type PyPyTuple_Type
PyAPI_DATA(PyTypeObject) PyTuple_Type;
#define PyList_Type PyPyList_Type
PyAPI_DATA(PyTypeObject) PyList_Type;
#define PySet_Type PyPySet_Type
PyAPI_DATA(PyTypeObject) PySet_Type;
#define PyFrozenSet_Type PyPyFrozenSet_Type
PyAPI_DATA(PyTypeObject) PyFrozenSet_Type;
#define PyInt_Type PyPyInt_Type
PyAPI_DATA(PyTypeObject) PyInt_Type;
#define PyBool_Type PyPyBool_Type
PyAPI_DATA(PyTypeObject) PyBool_Type;
#define PyFloat_Type PyPyFloat_Type
PyAPI_DATA(PyTypeObject) PyFloat_Type;
#define PyLong_Type PyPyLong_Type
PyAPI_DATA(PyTypeObject) PyLong_Type;
#define PyComplex_Type PyPyComplex_Type
PyAPI_DATA(PyTypeObject) PyComplex_Type;
#define PyByteArray_Type PyPyByteArray_Type
PyAPI_DATA(PyTypeObject) PyByteArray_Type;
#define PyMemoryView_Type PyPyMemoryView_Type
PyAPI_DATA(PyTypeObject) PyMemoryView_Type;
#define PyBaseObject_Type PyPyBaseObject_Type
PyAPI_DATA(PyTypeObject) PyBaseObject_Type;
#define PyNone_Type PyPyNone_Type
PyAPI_DATA(PyTypeObject) PyNone_Type;
#define PyNotImplemented_Type PyPyNotImplemented_Type
PyAPI_DATA(PyTypeObject) PyNotImplemented_Type;
#define PyCell_Type PyPyCell_Type
PyAPI_DATA(PyTypeObject) PyCell_Type;
#define PyModule_Type PyPyModule_Type
PyAPI_DATA(PyTypeObject) PyModule_Type;
#define PyProperty_Type PyPyProperty_Type
PyAPI_DATA(PyTypeObject) PyProperty_Type;
#define PySlice_Type PyPySlice_Type
PyAPI_DATA(PyTypeObject) PySlice_Type;
#define PyClass_Type PyPyClass_Type
PyAPI_DATA(PyTypeObject) PyClass_Type;
#define PyStaticMethod_Type PyPyStaticMethod_Type
PyAPI_DATA(PyTypeObject) PyStaticMethod_Type;
#define PyCFunction_Type PyPyCFunction_Type
PyAPI_DATA(PyTypeObject) PyCFunction_Type;
#define PyClassMethodDescr_Type PyPyClassMethodDescr_Type
PyAPI_DATA(PyTypeObject) PyClassMethodDescr_Type;
#define PyGetSetDescr_Type PyPyGetSetDescr_Type
PyAPI_DATA(PyTypeObject) PyGetSetDescr_Type;
#define PyMemberDescr_Type PyPyMemberDescr_Type
PyAPI_DATA(PyTypeObject) PyMemberDescr_Type;
#define PyMethodDescr_Type PyPyMethodDescr_Type
PyAPI_DATA(PyTypeObject) PyMethodDescr_Type;
#define PyWrapperDescr_Type PyPyWrapperDescr_Type
PyAPI_DATA(PyTypeObject) PyWrapperDescr_Type;
#define PyBufferable_Type PyPyBufferable_Type
PyAPI_DATA(PyTypeObject) PyBufferable_Type;

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */
