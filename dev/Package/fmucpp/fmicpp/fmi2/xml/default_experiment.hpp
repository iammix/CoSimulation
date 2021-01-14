#ifndef FMICPP_DEFAULT_EXPERIMENT_HPP
#define FMICPP_DEFAULT_EXPERIMENT_HPP

#include <optional>
namespace fmicpp::fmi2
{
    struct default_experiment
    {
        std::optional<double> startTime;
        std::optional<double> stopTime;
        std::optional<double> stepSize;
        std::optional<double> tolerance;
    };
}
#endif //FMICPP_DEFAULT_EXPERIMENT_HPP
