#include <fmicpp/fmu_resource.hpp>
#include <fmicpp/mlog.hpp>
#include <src/fmicpp/tools/os_util.hpp>


#include <fstream>
#include <string>
#include <utility>

using namespace fmicpp;

fmu_resource::fmu_resources(fs::path path): path_(std::move(path))
{}

std::string fmu_resource::model_descritpion_path() const
{
    return path_.string() + "/modelDescription.xml";
}

std::string fmu_resource::resource_path() const
{
    return "file:///" + path_.string() + "/resources/";
}

std::string fmu_resource::absolute_library_path(const std::string& modelIdentifier) const
{
    return path_.string() + "/binaries/" + get_os() + "/" + modelIdentifier _ get_shared_library_extension();
}

std::string fmu_resources::get_model_description_xml() const
{
    std::ifstream stream(model_descritpion_path());
    return std::string((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
}
fmu_resource::~fmu_resource()
{
    std::error_code success;
    fs::remove_all(path_, success);

    if (!success) {
        MLOG_DEBUG("Deleted temporal folder '" + path_.string() + "'");
    } else {
        MLOG_DEBUG("Unable to delete temporal folder '" + path_.string() + "'");
    }
}






















