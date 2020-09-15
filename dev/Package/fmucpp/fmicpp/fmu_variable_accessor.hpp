#ifndef FMICPP_FMU_VARIABLE_ACCESSOR_HPP
#define FMICPP_FMU_VARIABLE_ACCESSOR_HPP


#include <fmicpp/types.hpp>
#include <vector>

namespace fmicpp
{
    class fmu_reader
    {
    public:
        virtual bool read_integer(fmicppValueReference vr, fmicppInteger& ref) = 0;
        virtual bool read_integer(const std::vector<fmicppValueReference>& vr, std::vector<fmicppInteger>& ref) = 0;

        virtual bool read_real(fmicppValueReference vr, fmicppReal& ref) = 0;
        virtual bool read_real(const std::vector<fmicppValueReference>& vr, std::vector<fmicppString>& ref) =  0;
        virtual bool read_string(fmicppValueReference vr,fmicppString& ref) = 0;
        virtual bool read_string(const std::vector<fmicppValueReference>& vr, std::vector<fmicppString>& ref) = 0;
        virtual bool read_boolean(fmicppValueReference vr, fmicppBoolean& ref) = 0;
        virtual bool read_boolean(const std::vector<fmicppValueReference>& vr, std::vector<fmicppBoolean>& ref) = 0;
    };


    class fmu_writer
    {
    public:
        virtual bool write_integer(fmicppValueReference vr, fmicppInteger value) = 0;
        virtual bool write_integer(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmicppReal>& values) = 0;

        virtual bool write_real(fmicppValueReference vr, fmicppReal value) = 0;
        virtual bool write_real(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmicppReal>& values) = 0;

        virtual bool write_string(fmicppValueReference vr, fmicppString value) = 0;
        virtual bool write_string(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmiString>& values) = 0;

        virtual bool write_boolean(fmicppValueReference vr, fmicppBoolean value) = 0;
        virtual bool write_boolean(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmicppBoolean>& values) = 0;
    };



    class fmu_variable_accessor : public fmu_reader, public fmu_writer
    {

    };
}


#endif //FMICPP_FMU_VARIABLE_ACCESSOR_HPP