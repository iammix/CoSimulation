#ifndef SRC_STATUS_CONVERTER_HPP
#define SRC_STATUS_CONVERTER_HPP

#include <fmicpp/fmi2/fmi2FunctionTypes.h>
#include <fmicpp/status.hpp>

namespace fmicpp::fmi2
{
    inline status convert(fmi2Status status)
    {
        switch(status) {
            case fmi2OK:
                return status::OK;
            case fmi2Warning:
                return status::Warning;
            case fmi2Discard:
                return status::Discard;
            case fmi2Error:
                return status::Error;
            case fmi2Fatal:
                return status::Fatal;
            case fmi2Pending:
                return status::Pending;
            default:
                return status::Unknown;
        }
    }

}// namespace fmicpp::fmi2



#endif //SRC_STATUS_CONVERTER_HPP
