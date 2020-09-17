#ifndef FMI2_CS_LIBRARY_HPP
#define FMI2_CS_LIBRARY_HPP

#include <fmicpp/fmi2/fmi2_library.hpp>

namespace fmicpp::fmi2
{
    class cs_library : public fmi2_library
    {
    private:
        fmi2SetRealInputDerivativesTYPE* fmi2SetRealInputDerivatives_;
        fmi2GetRealOutputDerivativesTYPE* fmi2GetRealOutputDerivatives_;
        fmi2DoStepTYPE* fmi2DoStep_;
        fmi2CancelStepTYPE* fmi2CancelStep_;
        fmi2GetStatusTYPE* fmi2GetStatus_;
        fmi2GetRealStatusTYPE* fmi2GetRealStatus_;
        fmi2GetIntegerStatusTYPE* fmi2GetInteger_;
    };
}

#endif //FMI2_CS_LIBRARY_HPP
