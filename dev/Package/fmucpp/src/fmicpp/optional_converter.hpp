#ifndef FMUCPP_OPTIONAL_CONVERTER_H
#define FMUCPP_OPTIONAL_CONVERTER_H


#include <boost/optional.hpp>
#include <optional>

namespace
{
    template<class T>
    std::optional<T> convert(boost::optional<T> opt)
    {
        if (!opt) {
            return std::nullopt;
        } else {
            return *opt;
        }
    }
} // namespace

#endif //FMUCPP_OPTIONAL_CONVERTER_H
