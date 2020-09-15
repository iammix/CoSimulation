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
                return
            }
    }
}

