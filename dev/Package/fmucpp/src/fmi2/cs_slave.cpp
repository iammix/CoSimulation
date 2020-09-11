#include <fmicpp/fmi2/cs_slave.hpp>
#include <fmicpp/fmi2/status_converter.hpp>

using namespace fmicpp::fmi2;

cs_slave::cs_slave(fmi2Component c,
                   const std::shared_ptr<fmicpp::fmu_resource>& resource,
                   const std::shared_ptr<cs_library>& library,
                   const std::shared_ptr<const cs_model_description>& modelDescription)
                   : fmu_instance_base<cs_library, cs_model_description>(c, resource, library, modelDescription))
{

}

fmicpp::status cs_slave::last_status() const
{
    return convert(library_->last_status());
}


























































