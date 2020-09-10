#ifndef FMUCPP_TIME_UTIL_HPP
#define FMUCPP_TIME_UTIL_HPP

#include <chrono>

namespace
{

    template<typename function>
    inline float measure_time_sec(function&& fun)
    {
        auto t_start = std::chrono::high_resolution_clock::now();
        fun();
        auto t_stop = std::chrono::high_resolution_clock::now();
        return std::chrono::duration<float>(t_stop - t_start).count();
    }

} // namespace

#endif //FMUCPP_TIME_UTIL_HPP
