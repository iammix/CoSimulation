#ifndef FMICPP_FMU_RESOURCE_HPP
#define FMICPP_FMU_RESOURCE_HPP
#include <fmicpp/fs_portability.hpp>
#include <string>

namespace fmicpp
{
    class fmu_resource
    {
    private:
        const fs::path path_;
    public:
        explicit fmu_resource(fs::path path);
        [[nodiscard]] std::string resource_path() const;
        [[nodiscard]] std::string model_description_path() const;
        [[nodiscard]] std::string absolute_library_path(const std::string& modelIdentifier) const;
        [[nodiscard]] std::string get_model_description_xml() const;

        ~fmu_resource();
    };
}
#endif //FMICPP_FMU_RESOURCE_HPP
