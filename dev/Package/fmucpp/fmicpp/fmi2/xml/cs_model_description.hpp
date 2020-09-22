#ifndef FMICPP_CS_MODEL_DESCRIPTION_HPP
#define FMICPP_CS_MODEL_DESCRIPTION_HPP

#include <fmicpp/fmi2/xml/specific_model_description.hpp>

namespace
{
    struct cs_model_description : specific_model_description<cs_attributes>
    {
        cs_model_description(const model_description_base& base, const cs_attributes& attributes)
            : specific_model_description(base, attributes)
        {}
    };
}









#endif //FMICPP_CS_MODEL_DESCRIPTION_HPP
