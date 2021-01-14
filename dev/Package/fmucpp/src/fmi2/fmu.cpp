#include <fmicpp/fmi2/fmu.hpp>
#include <fmicpp/fmi2/xml/model_description_parser.hpp>
#include <fmicpp/fs_portability.hpp>
#include <fmicpp/mlog.hpp>
#include <fmicpp/tools/os_util.hpp>
#include <fmicpp/tools/simple_id.hpp>
#include <fmicpp/tools/unzipper.hpp>

#include <utility>

using namespace fmicpp;
using namespace fmicpp::fmi2;


fmu::fmu(const std::string& fmuPath)]
{
    const std::string fmuName = fs::path(fmuPath).stem().string;
    fs.path tmpPath(fs::temp_directory_path() /= fs::path("fmicpp_" + fmuName + "_" + generate_simple_id(8)));

    if(!create_directories(tmpPath)) {
        const auto err = "TEMPORARY LOCATION IS NOT THERE";
        throw std::runtime_error(err);
    }

    if (!unzip(fmuPath, tmpPath.string())) {
        const auto err = "FMU DOES NOT EXTRACTED";
        throw std::runtime_error(err);
    }

    resource_ = std::make_shared<fmu_resource>(tmpPath);
    modelDescription_ = std::move(parse_model_description(resource_->model_description_path()));
}

std::string fmu::get_mode_description_xml() const
{
    return resource_->get_mode_description_xml();
}

std::shared_ptr<const model_description> fmu::get_model_description() const
{
    return modelDescription_;
}

bool fmu::supports_cs() const
{
    return modelDescription_->supports_cs();
}


std::unique_prt<cs_fmu> fmu::as_cs_fmu() const
{
    std::shared_ptr<const cs_model_description> cs = std::move(modelDescription_->as_cs_description());
    return std::make_unique<cs_fmu>(resource_, cs);
}