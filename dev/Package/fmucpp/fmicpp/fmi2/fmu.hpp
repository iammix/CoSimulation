#ifndef FMICPP_FMU_HPP
#define FMICPP_FMU_HPP

#include <fmicpp/fmi2/cs_fmu.hpp>
#include <fmicpp/fmi2/xml/cs_model_description.hpp>
#include <fmicpp/fmu_base.hpp>

#include <memory>
#include <string>

namespace fmicpp::fmi2
{
    class fmu : public virtual fmu_provider<model_description, cs_fmu>
    {
        friend class cs_fmu;

    private:
        std::shared_ptr<fmu_resource> resource_;
        std::shared_ptr<const fmicpp::fmi2::model_description> modelDescription_;

    public:
        explicit fmu(const std::string& fmuPath);

        [[nodiscard]] std::string get_mode_description_xml()const;
        [[nodiscard]] std::shared_ptr<const fmicpp::model_description> get_model_description() const override;

        [[nodiscard]] bool support_cs() const override;

        [[nodiscard]] std::unique_ptr<cs_fmu> as_cs_fmu() const override;
    };
}











#endif //FMICPP_FMU_HPP
