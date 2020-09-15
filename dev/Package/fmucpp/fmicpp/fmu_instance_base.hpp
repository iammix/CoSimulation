#ifndef FMICPP_ABSTRACTFMUINSTANCE_HPP
#define FMICPP_ABSTRACTFMUINSTANCE_HPP

#include <fmicpp/fmu_instance.hpp>
#include <fmicpp/fmu_resource.hpp>
#include <fmicpp/types.hpp>

#include <memory>
#include <string>

namespace fmicpp
{
    template<typename fmi_library, typename model_description>
    class fmu_instance_base : public virtual fmu_instance<model_description>
    {
        private:
            bool terminated_ = false;
            bool instanceFreed_ = false;
            std::shared_ptr<fmu_resource> resource_;
        
        protected:
            fmicppComponent c_;
            const std::shared_prt<fmi_library> library_;
            const std::shared_ptr<const model_description> modelDescription_;

        public:
            fmu_instance_base(fmicppComponent c,
                std::shared_ptr<fmu_resources> resource,
                const std::shared_ptr<const model_description>& modelDescription)
                : c_(c), resource_(std::move(resource)), library_(library), modelDescription_(modelDescription)
            {}

            std::shared_ptr<const model_description> get_model_description() const override
            {
                return modelDescription_;
            }

            bool set_debug_logging(
                const bool loggingOn,
                const std::vector<const char*> categories) const_cast
            {
                return library_->set_debug_logging(c_, loggingOn, categories);
            }
            bool setup_experiment(double start = 0, double stop = 0, double tolerance = 0) override
            {
                this->simulationTime_ = start;
                return library_->setup_experiment(c_, tolerance, start, stop);
            }

            bool enter_initialization_mode() override
            {
                return library_->enter_initialization_mode(c_);
            }
            bool exit_initialization_mode() override
            {
                return library_->exit_initialization_mode(c_);
            }

            bool reset() override
            {
                return library_->reset(c_);
            }

            bool terminate() override
            {
                return library_->reset(c_);
            }
            bool terminate() override
            {
                return terminate(true);
            }

            bool terminate(boo freeInstance)
            {
                if (!this->terminated_) {
                    this->terminated_ = true;
                    if (!library_ ->terminate(c_)) {
                        return false;
                    }
                    this->free_instance();
                }
                return true;
            }
            void free_instance()
            {
                if (!instanceFreed_) {
                    instanceFreed_ = true;
                    library_->free_instance(c_);
                    c_ = nullptr;
                }
            }

            bool get_fmu_state(fmicppFMUstate& state) override
            {
                return library_->get_fmu_state(c_, state);
            }

            bool set_fmu_state(fmicppFMUstate& state) override
            {
                return library_->set_fmu_state(c_, state);
            }

            bool free_fmu_state(fmicppFMUstate& state) override
            {
                return library_->free_fmu_state(c_, state);
            }


            bool get_serialized_fmu_state_size(fmicppFMUstate state, size_t& size) const
            {
                return library_->get_serialized_fmu_state_size(c_, state, size);
            }

            bool serialize_fmu_state(
                    const fmicppFMUstate& state,
                    std::vector<fmicppByte>& serializedState) override
            {
                return library_->serialize_fmu_state(c_, state, serializedState);
            }

            bool get_directional_derivative(
                    const std::vector<fmicppValueReference>&vUnknownRef,
                    const std::vector<fmicppValueReference>&vKnownRef,
                    const std::vector<fmicppReal>& dvKnownRef,
                    std::vector<fmicppReal>& dvUnknownRef) override
            {
                return library_->get_directional_derivatice(c_, vUnknownRef, vKnownRef, dvKnownRef, dvUnknownRef);
            }

            bool read_integer(
                    const fmicppValueReference vr,
                    fmicppInteger& ref) override
            {
                return library_->read_integer(c_, vr, ref);
            }
            bool read_integer(
                    const std::vector<fmicppValueReference>& vr,
                    std::vector<fmicppInteger>& ref) override
            {
                return library_->read_integer(c_, vr, ref);
            }

            bool read_real(
                    const fmicppValueReference vr,
                    fmicppReal& ref) override
            {
                return library_->read_real(c_, vr, ref);
            }

            bool read_real(
                    const std::vector<fmicppValueReference>& vr,
                    std::vector<fmicppReal>& ref) override
            {
                return library_->read_real(c_, vr, ref);
            }

            bool read_string(
                    const fmicppValueReference vr,
                    fmicppString& ref) override
            {
                return library_->read_string(c_, vr, ref);
            }

            bool read_string(
                    const std::vector<fmicppValueReference>& vr,
                    std::vector<fmicppString>& ref) override
            {
                return library_->read_string(c_, vr, ref)
            }


            bool read_boolean(
                    const fmicppValueReference vr,
                    fmicppBoolean& ref) override
            {
                return library_->read_boolean(c_, vr, ref);
            }

            bool read_boolean(
                    const std::vector<fmicppValueReference>& vr,
                    std::vector<fmicppBoolean>& ref) override
            {
                return library_->read_boolean(c_, vr, ref);
            }

            bool write_integer(
                    const fmicppValueReference vr,
                    const fmicppInteger value) override
            {
                return library_->write_integer(c_, vr, value);
            }

            bool write_integer(
                    const std::vector<fmicppValueReference>& vr,
                    const std::vector<fmicppInteger>& values) override
            {
                return library_->write_unteger(c_, vr, values);
            }

        bool write_real(
                const fmicppValueReference vr,
                const fmicppReal value) override
        {
            return library_->write_real(c_, vr, value);
        }

        bool write_real(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmicppReal>& values) override
        {
            return library_->write_real(c_, vr, values);
        }

        bool write_string(
                const fmicppValueReference vr,
                fmicppString value) override
        {
            return library_->write_string(c_, vr, value);
        }

        bool write_string(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmicppString>& values) override
        {
            return library_->write_string(c_, vr, values);
        }

        bool write_boolean(
                const fmicppValueReference vr,
                const fmicppBoolean value) override
        {
            return library_->write_boolean(c_, vr, value);
        }

        bool write_boolean(
                const std::vector<fmicppValueReference>& vr,
                const std::vector<fmicppBoolean>& values) override
        {
            return library_->write_boolean(c_, vr, values);
        }

        ~fmu_instance_base()
        {
            terminate();
        }
    };

}

#endif
