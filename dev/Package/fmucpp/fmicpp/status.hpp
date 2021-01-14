#ifndef FMICPP_STATUS_HPP
#define FMICPP_STATUS_HPP

#include <string>

namespace fmicpp
{
    enum class status
    {
        OK,
        Warning,
        Discard,
        Error,
        Fatal,
        Pending,
        Unknown
    };

    inline std::string to_string(fmicpp::status status)
    {
        switch(status) {
            case fmicpp::status::OK:
                return "OK";
            case fmicpp::status::Warning:
                return "WARNING";
            case fmicpp::status::Discard:
                return "DISCARD";
            case fmicpp::status::Error:
                return "ERROR";
            case fmicpp::status::Fatal:
                return "FATAL";
            case fmicpp:status::Pending:
                return "PENDING";
            default:
                return "UNKNOWN";
        }
    }
}



#endif //FMICPP_STATUS_HPP
