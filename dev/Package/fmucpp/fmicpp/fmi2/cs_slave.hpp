#ifndef FMI2_CS_SLAVE_HPP
#define FMI2_CS_SLAVE_HPP

#include <fmicpp/fmi2/cs_library.hpp>
#include <fmicpp/fmi2/fmi2TypesPlatform.h>
#include <fmicpp/fmi2/xml/model_description.hpp>
#include <fmicpp/fmu_instance_base.hpp>
#include <fmicpp/fmu_resource.hpp>
#include <fmicpp/fmu_slave.hpp>

#include <memory>

namespace fmicpp::fmi2
{
    class cs_slave : public virtual fmu_slave<cs_model_description>,
            public fmu_instance_base<cs_library, cs_model_description>
    {
    public:
        cs_slave(fmi2Component c,
                 const std::shared_ptr<fmu_resource>& resource,
                 const std::shared_ptr<cs_library>& library,
                 const std::shared_ptr<const cs_model_description>& modelDescription);
        bool step(double stepSize) override;
        bool cancel_step() override;

        [[nodiscard]] std::shared_ptr<const cs_model_description> get_model_description() const override;
        [[nodiscard]] status last_status() const override;

        bool setup_experiment(double start = 0, double stop = 0, double tolerance = 0) override;
        bool enter_initialization_mode() override;
        bool exit_initialization_mode() override;

        bool reset() override;
        bool terminate() override;

        bool read_integer(fmi2ValueReference vr, fmi2Integer& ref) override;
        bool read_integer(const std::vector<fmi2ValueReference>& vr, std::vector<fmi2Integer>& ref) override;

        bool read_real(fmi2ValueReference vr, fmi2Real& ref) override;
        bool read_real(const std::vector<fmi2ValueReference>& vr, std::vector<fmi2Real>& ref) override;

        bool read_boolean(fmi2ValueReference vr, fmi2Boolean& ref) override;
        bool read_boolean(const std::vector<fmi2ValueReference>& vr, std::vector<fmi2Boolean>& ref) override;

        bool write_integer(fmi2ValueReference vr, fmi2Integer& value) override;
        bool write_integer(const std::vector<fmi2ValueReference>& vr, const std::vector<fmi2Ineger>& values) override;

        bool write_real(fmi2ValueReference vr, fmi2Real& value) override;
        bool write_real(const std::vector<fmi2ValueReference>& vr, const std::vector<fmi2Real>& values) override;

        bool write_string(fmi2ValueReference vr, fmi2String& value) override;
        bool write_string(const std::vector<fmi2ValueReference>& vr, const std::vector<fmi2String>& values) override;



        
    };
}

#endif //FMI2_CS_SLAVE_HPP
