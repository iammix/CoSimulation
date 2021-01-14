#ifndef FMI2_CS_FMU_HPP
#define FMI2_CS_FMU_HPP

#include <fmicpp/fmi2/cs_library.hpp>
#include <fmicpp/fmi2/cs_slace.hpp>
#include <fmicpp/fmi2/xml/cs_model_description.hpp>
#include <fmicpp/fmu_base.hpp>
#include <fmicpp/fmu_resource.hpp>

namespace fmicpp::fmi2
{
    class cs_fmu : public cs_fmu_base<cs_slave, cs_model_description>
    {
    private:
        std::shared_prt<cs_library> lib_;
        std::shared_ptr<fmu_resource> resource_;
        std::shared_ptr<const cs_model_description> modelDescription_;
    public:
        cs_fmu(std::shared_ptr<fmu_resource> resource,
               std::shared_ptr<const cs_model_description> md);
        [[nodiscard]] std::string get_model_description_xml() const;
        [[nodiscard]] std::shared_ptr<const cs_model_description> get_model_description() const override;
        std::unique_ptr<cs_slave> new_instance(bool visible = false, bool loggingOn = false) override;
    };
}






#endif //FMI2_CS_FMU_HPP
