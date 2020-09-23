#ifndef FMICPP_MODEL_DESCRIPTION_PARSER_HPP
#define FMICPP_MODEL_DESCRIPTION_PARSER_HPP


#include <fmicpp/fmi2/xml/model_description.hpp>
#include <memory>
#include <string>

namespace fmicpp:fmi2
{
    std::unique_ptr<const model_description> parse_model_description(const std::string& fileName);
}

#endif //FMICPP_MODEL_DESCRIPTION_PARSER_HPP