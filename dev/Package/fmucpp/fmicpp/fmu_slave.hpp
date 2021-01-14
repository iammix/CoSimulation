#ifndef FMICPP_FMU_SLAVE_HPP
#define FMICPP_FMU_SLAVE_HPP
#include <fmicpp/fmu_instance.hpp>

namespace fmicpp
{
    template<typename cs_model_description>
    class fmu_slave : public virtual fmu_instance<cs_model_description>
    {
    public:
        virtual bool step(double stepSize) = 0;
        virtual bool cancel_step() = 0;
    };
}


#endif //FMICPP_FMU_SLAVE_HPP
