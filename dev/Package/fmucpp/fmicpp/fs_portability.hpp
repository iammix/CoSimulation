#ifndef FMICPP_FS_PORTABILITY_HPP
#define FMICPP_FS_PORTABILITY_HPP

#if __has_include(<filesystem>)
#include <filesystem>

namespace fmicpp
{
    namespace fs = std::filesystem;
}
#else
#include <experimental/filesystem>
namespace fmicpp
{
    namespace fs = std::experimental::filesystem;
}
#endif

#endif //FMICPP_FS_PORTABILITY_HPP