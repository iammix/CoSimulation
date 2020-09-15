#ifndef FMICPP_FMU_INSTANCE_HPP
#define FMICPP_FMU_INSTANCE_HPP

#include <fmicpp/fmu_variable_accessor.hpp>
#include <fmicpp/status.hpp>
#include <fmicpp/types.hpp>

#include <memory>
#include <vector>

namespace fmicpp
{

    template<typename ModelDescription>
    class fmu_instance : public fmu_variable_accessor
    {

    protected:
        double simulationTime_ = 0.0;

    public:
        [[nodiscard]] virtual const double get_simulation_time() const
        {
            return simulationTime_;
        }

        [[nodiscard]] virtual fmicpp::status last_status() const = 0;

        virtual std::shared_ptr<const ModelDescription> get_model_description() const = 0;

        virtual bool setup_experiment(double startTime = 0.0, double stopTime = 0.0, double tolerance = 0.0) = 0;
        virtual bool enter_initialization_mode() = 0;
        virtual bool exit_initialization_mode() = 0;

        virtual bool reset() = 0;
        virtual bool terminate() = 0;

        virtual bool get_fmu_state(fmicppFMUstate& state) = 0;
        virtual bool set_fmu_state(fmicppFMUstate state) = 0;
        virtual bool free_fmu_state(fmicppFMUstate& state) = 0;

        virtual bool serialize_fmu_state(
                const fmicppFMUstate& state,
                std::vector<fmicppByte>& serializedState) = 0;
        virtual bool de_serialize_fmu_state(
                fmicppFMUstate& state,
                const std::vector<fmicppByte>& serializedState) = 0;

        virtual bool get_directional_derivative(
                const std::vector<fmicppValueReference>& vUnknownRef,
                const std::vector<fmicppValueReference>& vKnownRef,
                const std::vector<fmicppReal>& dvKnownRef,
                std::vector<fmicppReal>& dvUnknownRef) = 0;

        virtual ~fmu_instance() = default;
    };

}

#endif //FMICPP_FMU_INSTANCE_HPP
