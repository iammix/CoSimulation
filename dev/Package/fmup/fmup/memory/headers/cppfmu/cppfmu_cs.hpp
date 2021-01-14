#ifndef CPPFMU_CS_HPP
#define CPPFMU_CS_HPP

#include "cppfmu_common.hpp"

#include <vector>

namespace cppfmu
{
    class DependInstance
    {
    public:
        virtual void SetupExperiment(
                FMIBoolean toleranceDefined,
                FMIReal tolerance,
                FMIReal tStart,
                FMIBoolean stopTimeDefined,
                FMIReal tStop);

        virtual void EnterInitializationMode();

        virtual void ExitInitializationMode();

        virtual void Terminate();
        virtual void Reset();

        virtual void SetReal(
                const FMIValueReference vr[],
                std::size_t nvr,
                const FMIReal value[]
                );

        virtual void SetInteger(
                const FMIValueReference vr[],
                std::size_t nvr,
                const FMIInteger value[]
                );

        virtual void SetBoolean(
                const FMIValueReference vr[],
                std:size_t nvr,
                const FMIBoolean value[]
                );

        virtual void SetString(
                const FMIValueReference vr[],
                std::size_t nvr,
                const FMIString value[]
                );

        virtual void GetReal(
                const FMIValueReference vr[],
                std::size_t nvr,
                FMIReal value[]) const;

        virtual void GetInteger(
                const FMIValueReference vr[],
                std::size_t nvr,
                FMIInteger value[]) const;

        virtual void GetBoolean(
                const FMIValueReference vr[],
                std::size_t nvr,
                FMIBoolean value[]) const;

        virtual void GetString(
                const FMIValueReference vr[],
                std::size_t nvr,
                FMIString value[]) const;

        virtual bool DoStep(
                FMIReal currentCommunicationPoint,
                FMIReal communicationStepSize,
                FMIBoolean newStep,
                FMIReal& endOfStep) = 0;

        virtual void GetFMUstate(fmi2FMUstate& state) = 0;
        virtual void SetFMUstate(const fmi2FMUstate& state) = 0;
        virtual void FreeFMUstate(fmi2FMUstate& state) = 0;

        virtual size_t SerializedFMUstateSize(const fmi2FMUstate& state) = 0;
        virtual void SerializeFMUstate(const fmi2FMUstate& state, fmi2Byte bytes[], size_t size) = 0;
        virtual void DeSerializeFMUstate(const fmi2Byte bytes[], size_t size, fmi2FMUstate& state) = 0;

        virtual ~DependInstance() CPPFMU_NOEXCEPT;
    };
}


cppfmu::UniquePtr<cppfmu::DependInstance> CppfmuInstatiateDepend(
        cppfmu::FMIString instanceName,
        cppfmu::FMIString fmuGUID,
        cppfmu::FMIString fmuResourceLocation,
        cppfmu::FMIString mineType,
        cppfmu::FMIReal timeout,
        cppfmu::FMIBoolean visible,
        cppfmu::FMIBoolean interactive,
        cppfmu::Memory memory,
        const cppfmu::Logger& logger);

#endif