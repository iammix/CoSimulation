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

bool cs_slave::step(const double stepSize)
{
    if (library_->step(c_, simulationTime_, stepSize, false)) {
        simulationTIme_ += stepSize;
        return true;
    }
    return false;
}

bool cs_slave::cancel_step()
{
    return library_->cancel_step(c_);
}

std::shared_ptr<const cs_model_description> cs_slave::get_model_description() const
{
    return fmu_instance_base::get_model_description();
}


bool cs_slave::setup_experiment(double start, double stop, double tolerance)
{
    return fmu_instance_base::setup_experiment(start, stop, tolerance);
}

bool cs_slave::enter_initialization_mode()
{
    return fmu_instance_base::enter_initialization_mode();
}

bool cs_slave::exit_initialization_mode()
{
    return fmu_instance_base::exit_initialization_mode();
}

bool cs_slave::reset()
{
    return fmu_instance_base::reset();
}




















































































