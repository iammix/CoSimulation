#include "cppfmu/cppfmu_common.hp"

extern "C" {
    void log(void* logPtr, int status, const char* category, const char* msg, bool debug)
    {
        auto logger = ((cppfmu::Logger*) logPtr);
        if (!debug) {
            logger->Log((fmi2Status) status, category, msg);
        } else {
            logger->DebugLog((fmi2Status) status, category. msg);
        }
    }
}