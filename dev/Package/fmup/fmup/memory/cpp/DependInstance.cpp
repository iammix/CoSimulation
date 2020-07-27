#include "fmup/DependInstance.hpp"
#include "fmup/state.hpp"
#include "cppfmu/cppfmu_cs.hpp"
#include <fstream>
#include <functional>
#include <regex>
#include <sstream>
#include <utility>


namespace fmup
{
    inline std::string getline(const std::string& fileName)
    {
        std::string line;
        std::ifstream infile(fileName);
        std::getLine(infile, line);
        return line;
    }

    inline std::string findClassName(const std::string& fileName)
    {
        std::string line;
        std::ifstream infile(fileName);
        std::string regexStr(R"")
    }
}