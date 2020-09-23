#ifndef FMICPP_ENUMS_HPP
#define FMICPP_ENUMS_HPP


namespace fmicpp::fmi2
{
    enum class causality
    {
        parameter,
        calculatedParameter,
        input,
        output,
        local,
        independent,
        unknown
    };
    enum class variability
    {
        constant,
        fixed,
        tunable,
        discrete,
        continuous,
        unknown
    };

    enum class initial
    {
        exact,
        approx,
        calculated,
        unknown
    };
    causality parse_causality(const std::string& str);
    variability parse_variability(const std::string& str);
    initial parse_initial(const std::string& str);

    std::string to_string(causality causality);
    std::string to_string(variability variability);
    std::string to_string(initial initial);
}

#endif //FMICPP_ENUMS_HPP
