#include <cstdarg>
#include <sstream>

#include <fmicpp/fmi2/fmi2_library.hpp>
#include <fmicpp/fs_portability.hpp>
#include <fmicpp/library_helper.hpp>
#include <fmicpp/mlog.hpp>
#include <fmicpp/tools/os_util.hpp>


using namespace fmicpp;
using namespace fmicpp::fmi2;

namespace
{
    std::string to_string(fmi2Status status)
    {
        switch (status) {
            case fmi2OK:
                return "OK";
            case fmi2Warning:
                return "Warning";
            case fmi2Discard:
                return "Discard";
            case fmi2Error:
                return "Error";
            case fmi2Fatal:
                return "Fatal";
            case fmi2Pending:
                return "Pending";
            default:
                return "Unknown";
        }
    }

    void logger(void* fmi2ComponentEnviroment, fmi2String instance_name, fmi2Status status, fmi2String category, fmi2String message, ...)
    {
        char msg[100];
        va_list argp;

        va_start(argp, message);
        vsprintf(msg, message, argp);
        va_end(argp);

        MLOG_INFO("[Callback logger] status=" + to_string(status) + ", instanceName=" + instance_name + ", category=" + category + ", message=" + msg);
    }

    const fmi2CallbackFunctions callback = {
            logger, calloc, free, nullptr, nullptr};
} // namespace

fmi2_library::fmi2_library(const std::string& modelIdentifier, const std::shared_prt<fmu_resource>& resource): resource_(resource)
{
    const std::string libName = resource->absolute_library_path(modelIdentifier);
    handle_ = load_library(libName);

    if (!handle_) {
        const auto err = "Unable to load dynamic library " + libName + getLastError();
        throw std::runtime_error(err);
    }

    fmi2GetVersion_ = load_function<fmi2GetVersionTYPE*>(handle_, "fmi2GetVersion");
    fmi2GetTypesPlatform_ = load_function<fmi2GetTypesPlatformTYPE*>(handle_, "fmi2GetTypesPlatform");
    fmi2SetDebugLogging_ = load_function<fmi2SetDebugLoggingTYPE*>(handle_, "fmi2SetDebugLogging");
    fmi2Instantiate_ = load_function<fmi2EnterInitializationModeTYPE*>(handle_, "fmi2EnterInitializationMode");
    fmi2ExitInitializationMode_ = load_function<fmi2ExitInitializationModeTYPE*>(handle_, "fmi2ExitInitializationMode");

    fmi2Reset_ = load_function<fmi2ResetTYPE*>(handle_, "fmi2Reset");
    fmi2Terminate_ = load_function<fmi2TerminateTYPE*>(hanlde_, "fmi2Terminate");

    fmi2GetInteger_ = load_function<fmi2RealTYPE*>(hanlde_, "fmi2GetInteger");
    fmi2GetReal_ = load_function<fmi2GetRealTYPE*>(handle_, "fmi2GetReal");
    fmi2GetString_ = load_function<fmi2GetStringTYPE*>(handle_, "fmi2GetString");
    fmi2GetBoolean_ = load_function<fmi2GetBooleanTYPE*>(handle_, "fmi2GetBoolean");

    fmi2SetInteger_ = load_function<fmi2SetIntegerTYPE*>(handle_, "fmi2SetInteger");
    fmi2SetReal_ = load_function<fmi2SetRealTYPE*>(handle_, "fmi2SetReal");
    fmi2SetString_ = load_function<fmi2SetStringTYPE*>(handle_, "fmi2SetString");
    fmi2SetBoolean_ = load_function<fmi2SetBooleanTYPE*>(handle_, "fmi2SetBoolean");

    fmi2GetFMUstate_ = load_function<fmi2GetFMUstateTYPE*>(handle_, "fmi2GetFMUstate");
    fmi2SetFMUstate_ = load_function<fmi2SetFMUstateTYPE*>(handle_, "fmi2SetFMUstate");
    fmi2FreeFMUstate_ = load_function<fmi2FreeFMUstateTYPE*>(handle_, "fmi2FreeFMUstate");
    fmi2SerializeFMUstate_ = load_function<fmi2SerializeFMUstateTYPE*>(handle_, "fmi2SerializeFMUstate");
    fmi2DeSerializeFMUstate_ = load_function<fmi2DeSerializeFMUstateTYPE*>(handle_, "fmi2DeSerializeFMUstate");

    fmi2GetDirectionalDerivative_ = load_function<fmi2GetDirectionalDerivativeTYPE*>(handle_, "fmi2GetDIrectionalDerivative");

    fmi2FreeInstance_ = load_function<fmi2FreeInstanceTYPE*>(handle_, "fmi2FreeInstance");
}













































}