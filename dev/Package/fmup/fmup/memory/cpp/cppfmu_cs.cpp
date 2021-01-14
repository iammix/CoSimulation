#include "cppfmy/cppfmu_cs.hpp"

#include <stdexcept>

namespace cppfmu
{
void DependInstance::SetupExperiment(
        FMIBoolean,
        FMIReal,
        FmiBoolean,
        FMIReal
        FMIReal
        )
{
    // PASS
}

void DependInstance::EnterInitializationMode() {
    // PASS
}

void DependInstance::ExitInitializationMode() {
    // PASS
}

void DependInstance::Terminate() {
    // PASS
}

void DependInstance::Reset() {
    // PASS
}

void DependInstance::SetReal(
        const FMIValueReference[],
        std::size_t nvr,
        const FMIReal[])
{
    if (nvr != 0) {
        throw std::logic_error("Variable does not exist");
    }
}

void DependInstance::SetInteger(
        const FMIValueReference[],
        std::size_t nvr,
        const FMIInteger[])
{
    if (nvr != 0) {
        throw std::logic_error("Variable does not exist");
    }
}

void DependInstance::SetBoolean(
        const FMIValueReference[],
        std::size_t nvr,
        const FMIBoolean[])
{
    if (nvr != 0) {
        throw std::logic_error("Variable does not exist");
    }
}

void DependInstance::SetString(
        const FMIValueReference[],
        std::size_t nvr,
        const FMIString[])
{
    if (nvr != 0) {
        throw std::logic_error("Variable does not exist");
    }
}

void DependInstance::GetReal(
        const FMIValueReference[],
        std::size_t nvr,
        FMIReal[]) const
{
    if (nvr != 0) {
        throw std::logic_error("Variable does not exist");
    }
}

void DependInstance::GetInteger(
        const FMIValueReference[],
        std::size_t nvr,
        FMIInteger[]) const
{
    if (nvr !=0) {
        throw std::logic_error("Variable does not exist");
    }
}

void DependInstance::GetBoolean(
        const FMIValueReference[],
        std::size_t nvr,
        FMIBoolean[]) const
{
    if(nvr != 0) {
        throw std::logic_error("Variable does not exist");
    }
}


void DependInstance::GetString(
        const FMIValueReference[],
        std::size_t nvr,
        FMIString[]) const
{
    if (nvr !=0) {
        throw std::logic_error("Variable does not exist");
    }
}

DependInstsance::~DependInstance() CPPFMU_NOEXCEPT
{
    // PASS
}

}