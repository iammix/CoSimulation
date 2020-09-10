#include <fmicpp/fmi2/cs_library.hpp>
#include <fmicpp/libray_helper.hpp>

using namespace fmicpp;
using namespace fmicpp::fmi2;

cs_library::cs_library(const std::string& modelIdentifier,
                       const std::shared_ptr<fmu_resource>& resource): fmi2_library(modelIdentifier, resource)
{
    fmi2SetRealInputDerivatives_ = load_function <fmi2SetRealInputDerivativesTYPE*>(handle_,"fmi2SetRealInputDerivatives");
    fmi2GetRealOutputDerivatives_ = load_function<fmi2GetRealOutputDerivativesTYPE*>(handle_,"fmi2GetRealOutputDerivatives");
}