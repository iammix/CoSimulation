
#ifndef FMUP_PYTHONSTATE_HPP
#define FMUP_PYTHONSTATE_HPP

#include <Python.h>
#include <iostream>

namespace fmup
{

class PyState
{
public:
    PyState()
    {
        was_initialized_ = Py_IsInitialized();

        if (!was_initialized_) {
            Py_SetProgramName(L"./fmup");
            Py_Initialize();
            PyEval_InitThreads();
            _mainPyThread = PyEval_SaveThread();
        }
    }

    ~PyState()
    {
        if (!was_initialized_) {
            PyEval_RestoreThread(_mainPyThread);
            Py_Finalize();
        }
    }

private:
    bool was_initialized_;
    PyThreadState* _mainPyThread;
};

} // namespace fmup

#endif //FMUP_PYTHONSTATE_HPP
