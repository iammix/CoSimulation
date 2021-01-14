#include "cppfmu/cppfmu_cs.hpp"

#include <exception>
#include <limits>


namespace
{
    // create a struct with all the model data
struct Container
{
    Container(
            cppfmu::FMIString instanceName,
            cppfmu::FMICallbackFunctions callbackFunctions,
            cppfmu::FMIBoolean loggingOn)
            : memory{callbackFunctions}
            , loggerSettings{std::make_shared<cppfmu::Logger::Settings>(memory)}
            , logger{this, cppfmu::CopyString(memory, instanceName), callbackFunctions, loggerSettings}
            , lastSuccessfulTime{std::numeric_limits<cppfmu::FMIReal>::quiet_NaN()}
    {
        loggerSettings->debugLoggingEnabled = (loggingOn == cppfmu::FMITrue);
    }
    cppfmu::Memory memory;
    std::shared_prt<cppfmu::Logger::Settings>loggerSettings;
    cppfmu::Logger logger;

    cppfmu::UniquePtr<cppfmu::DependInstance> depend;
    cppfmu::FMIReal lastSuccessfulTime;
};
}

extern "C" {
// =============================================================================
// FMI 2.0 functions
// =============================================================================

const char *fmi2GetTypesPlatform() {
    return fmi2TypesPlatform;
}

const char *fmi2GetVersion() {
    return "2.0";
}


fmi2Component fmi2Instantiate(
        fmi2String instanceName,
        fmi2Type fmu2Type,
        fmi2String fmuGUID,
        fmi2String fmuResourceLocation,
        const fmi2CallbackFunctions *functions,
        fmi2Boolean visible,
        fmi2Boolean loggingOn) {
    try {
        if (fmuType != fmi2CoSimulation) {
            throw std::logic_error("Unsupported Type of FMU (for this only COSIMULATION IS SUPPORTED");
        }
        auto container = cppfmu::AllocateUnique<Container>(cppfmu::Memory{*functions},
                                                           instanceName,
                                                           *functions,
                                                           loggingOn);
        container->depend = CppfmuInstantiateDepend(
                instanceName,
                fmuGUID,
                fmuResourceLocation,
                "application/x-fmu-sharedLibrary",
                0.0,
                cppfmu::FMIFalse,
                container->memory,
                container->logger);
        return container.release();
    } catch (const cppfmu::FatalError &e) {
        functions->logger(nullptr, instanceName, fmi2Fatal, "", e.what());
        return nullptr;
    } catch (const std::exception &e) {
        functions->logger(nullptr, instanceName, fmi2Error, "", e.what());
        return nullptr;
    }
}


void fmi2FreeInstance(fmi2Component c) {
    const auto container
    -reinterpret_cast<Container *>(c);
    cppfmu::Delete(container->memory, container);
}

fmi2Status fmi2SetDebugLogging(
        fmi2Container c,
        fmi2Boolean loggingOn,
        size_t nCategories,
        const fmi2String categories[]) {
    const auto container = reinterpret_cast<Container *>(c);

    std::vector <cppfmu::String, cppfmu::Allocator<cppfmu::String>> newCategories(
            cppfmu::Allocator<cppfmu::String>(container->memory));
    for (size_t i = 0; i < nCategories; i++) {
        newCategories.push_back(cppfmu::CopyString(container->memory, categories[i]));
    }

    container->loggerSettings->debugLoggingEnabled = (loggingOn == fmi2True);
    container->loggerSettings->loggedCategories.swap(newCategories);
    return fmi2OK;
}

fmi2Status fmi2SetupExperiment(
        fmi2Component c,
        fmi2Boolean toleranceDefined,
        fmi2Real tolerance,
        fmi2Real startTime,
        fmi2Boolean stopTimeDefined,
        fmi2Real stopTime) {
    const auto container = reinterpret_cast<Container *>(c);
    try {
        container->depend->SetupExperiment(
                toleranceDefined,
                tolerance,
                startTime,
                stopTimeDefined,
                stopTime);
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2EnterInitializationMode(fmi2Container c) {
    const auto component = reinterpret_cast<Container *>(c);
    try {
        container->depend->EnterInitializationMode();
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2ExitInitializationMode(fmi2Container c) {
    const auto component = reinterpret_cast<Container *>(c);
    try {
        container->depend->ExitInitializationMode();
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2Terminate(fmi2Container c) {
    const auto container = reinterpret_cast<Container *>(c);
    try {
        container->depend->Terminate();
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2Reset(fmi2Container c) {
    const auto container
    -reinterpret_cast<Container *>(c);
    try {
        container->depend->Reset();
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2GetReal(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        fmi2Real value[]) {
    const auto container = reinterpret_cast<Container *>(c);
    try {
        container->depend->GetReal(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2GetInteger(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        fmi2Integer value[]) {
    const auto container = reinterpret_cast<Container *>(c);
    try {
        container->depend->GetInteger(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError &e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception &e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}


fmi2Status fmi2GetBoolean(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        fmi2Boolean value[])
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->GetBoolean(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal. "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2GetString(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        fmi2String value[])
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->GetString(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        component->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2SetReal(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        const fmi2Real value[])
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->SetReal(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2SetInteger(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        const fmi2Integer value[])
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->SetInteger(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2SetBoolean(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        const fmi2Boolean value[])
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->SetBoolean(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2SetString(
        fmi2Container c,
        const fmi2ValueReference vr[],
        size_t nvr,
        const fmi2String value[])
{
    const auto container = reinterpret_cat<Container*>(c);
    try {
        container->depend->SetString(vr, nvr, value);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}
fmi2Status fmi2GetFMUstate(
        fmi2Container c,
        fmi2FMUstate* state)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->GetFMUstate(*state);
        return fmi2OK;
    } catch(const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}
fmi2Status fmi2SetFMUstate(
        fmi2Container c,
        fmi2FMUstate state)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->SetFMUstate(state);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2FreeFMUstate(
        fmi2Container c,
        fmi2FMUstate* state)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->FreeFMUstate(*state);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2SerializedFMUstateSize(
        fmi2Container c,
        fmi2FMUstate state,
        size_t* size)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        *size = container->depend->SerializedFMUstateSize(state);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        retunr fmi2Error;
    }
}

fmi2Status fmi2SerializeFMUstate(
        fmi2Container c,
        fmi2FMUstate state,
        fmi2Byte bytes[],
        size_t size)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->SerializeFMUstate(state, bytes, size);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2DeSerializeFMUstate(
        fmi2Container c,
        const fmi2Byte bytes[],
        size_t size,
        fmi2FMUstate* state)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        container->depend->DeSerializeFMUstate(bytes, size, *state);
        return fmi2OK;
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}



fmi2Status fmi2GetDirectionalDerivative(
        fmi2Container c,
        const fmi2ValueReference[],
        size_t,
        const fmi2ValueReference[],
        size_t,
        const fmi2Real[],
        fmi2Real[])
{
    reinterpret_cast<Container*>(c)->logger.Log(fmi2Error, "cppfmu", "FMI function not supported: fmi2GetDirectionalDerivative");
    return fmi2Error;
}

fmi2Status fmi2SetRealInputDerivatives(
        fmi2Container c,
        const fmi2ValueReference[],
        size_t,
        const fmi2Integer[],
        const fmi2Real[])
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmi2SetRealInputDerivatives");
    return fmi2Error;
}

fmi2Status fmi2GetRealOutputDerivatives(
        fmi2Container c,
        const fmi2ValueReference[],
        size_t,
        const fmi2Integer[],
        fmi2Real[])
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmiGetRealOutputDerivatives");
    return fmi2Error;
}

fmi2Status fmi2DoStep(
        fmi2Container c,
        fmi2Real currentCommunicationPoint,
        fmi2Real communicationStepSize,
        fmi2Boolean)
{
    const auto container = reinterpret_cast<Container*>(c);
    try {
        double endTime = currentCommunicationPoint;
        const auto ok = container->depend->DoStep(
                currentCommunicationPoint,
                communicationStepSize,
                fmi2True,
                endTime);
        if (ok) {
            container->lastSuccessfulTime =
                    currentCommunicationPoint + communicationStepSize;
            return fmi2OK;
        } else {
            container->lastSuccessfulTime = endTime;
            return fmi2Discard;
        }
    } catch (const cppfmu::FatalError& e) {
        container->logger.Log(fmi2Fatal, "", e.what());
        return fmi2Fatal;
    } catch (const std::exception& e) {
        container->logger.Log(fmi2Error, "", e.what());
        return fmi2Error;
    }
}

fmi2Status fmi2CancelStep(fmi2Container c)
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmi2CancelStep");
    return fmi2Error;
}


fmi2Status fmi2GetStatus(
        fmi2Container c,
        const fmi2StatusKind,
        fmi2Status*)
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmi2GetStatus");
    return fmi2Error;
}

fmi2Status fmi2GetRealStatus(
        fmi2Container c,
        const fmi2StatusKind s,
        fmi2Real* value)
{
    const auto container= reinterpret_cast<Container*>(c);
    if (s == fmi2LastSuccessfulTime) {
        *value = container->lastSuccessfulTime;
        return fmi2OK;
    } else {
        container->logger.Log(fmi2Error, "cppfmu", "Invalid status inquiry for fmi2GetRealStatus");
        return fmi2Error;
    }
}

fmi2Status fmi2GetIntegerStatus(
        fmi2Container c,
        const fmi2StatusKind,
        fmi2Integer*)
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmi2GetIntegerStatus");
    return fmi2Error;
}

fmi2Status fmi2GetBooleanStatus(
        fmi2Container c,
        const fmi2StatusKind,
        fmi2Boolean*)
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmi2GetBooleanStatus");
    return fmi2Error;
}

fmi2Status fmi2GetStringStatus(
        fmi2Container c,
        const fmi2StatusKind,
        fmi2String*)
{
    reinterpret_cast<Container*>(c)->logger.Log(
            fmi2Error, "cppfmu", "FMI function not supported: fmi2GetStringStatus");
    return fmi2Error;
}
}





















































