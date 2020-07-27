#ifndef CPPFMU_COMMON_HPP
#define CPPFMU_COMMON_HPP


#include <algorithm>
#include <cstddef>
#include <functional>
#include <memory>
#include <new>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>


extern "C"
{
#ifdef CPPFMU_USE_FMI_1_0
#include "fmiFunctions.h"
#else
#include "fmi/fmi2Functions.h"
#endif
}


#if (__cplusplus >= 201103L) || (defined(_MSC_VER) && _MSC_VER >= 1900)
#   define CPPFMU_NOEXCEPT noexcept
#else
#   define CPPFMU_NOEXCEPT
#endif


namespace cppfmu

{
#ifdef CPPFMU_USE_FMI_1_0
    typedef fmiReal FMIReal;
    typedef fmiInteger FMIInteger;
    typedef fmiBoolean FMIBoolean;
    typedef fmiString FMIString;
    typedef fmiCallbackFunctions FMICallbackFunctions;
    typedef fmiCallbackAllocateMemory FMICallbackAllocateMemory;
    typedef fmiCallbackFreeMemory FMICallbackFreeMemory;
    typedef fmiCallbackLogger FMICallbackLogger;
    typedef fmiComponent FMIComponent;
    typedef fmiComponent FMIComponentEnvironment;
    typedef fmiStatus FMIStatus;
    typedef fmiValueReference FMIValueReference;

    const FMIBoolean FMIFalse = fmiFalse;
    const FMIBoolean FMITrue = fmiTrue;

    const FMIStatus FMIOK = fmiOK;
    const FMIStatus FMIWarning = fmiWarning;
    const FMIStatus FMIDiscard = fmiDiscard;
    const FMIStatus FMIError = fmiError;
    const FMIStatus FMIFatal = fmiFatal;
    const FMIStatus FMIPending = fmiPending;
#else
    typedef fmi2Real FMIReal;
    typedef fmi2Integer FMIInteger;
    typedef fmi2Boolean FMIBoolean;
    typedef fmi2String FMIString;
    typedef fmi2CallbackFunctions FMICallbackFunctions;
    typedef fmi2CallbackAllocateMemory FMICallbackAllocateMemory;
    typedef fmi2CallbackFreeMemory FMICallbackFreeMemory;
    typedef fmi2CallbackLogger FMICallbackLogger;
    typedef fmi2Component FMIComponent;
    typedef fmi2ComponentEnvironment FMIComponentEnvironment;
    typedef fmi2Status FMIStatus;
    typedef fmi2ValueReference FMIValueReference;

    const FMIBoolean FMIFalse = fmi2False;
    const FMIBoolean FMITrue = fmi2True;

    const FMIStatus FMIOK = fmi2OK;
    const FMIStatus FMIWarning = fmi2Warning;
    const FMIStatus FMIDiscard = fmi2Discard;
    const FMIStatus FMIError = fmi2Error;
    const FMIStatus FMIFatal = fmi2Fatal;
    const FMIStatus FMIPending = fmi2Pending;
#endif
}


// ============================================================================
// ERROR HANDLING
// ============================================================================

class FatalError : public std::runtime_error {
public:
    FatalError(const char* msg) CPPFMU_NOEXCEPT : std::runtime_error{msg} { }
};




// ============================================================================
// MEMORY MANAGEMENT
// ============================================================================

class Memory
{
public:
    explicit Memory(const FMICallbackFunctions& callbackFunctions)
        : m_alloc{callbackFunctions.allocateMemory}
        , m_free{callbackFunctions.freeMemory}

    {
    }

    void* Alloc(std::size_t nObj, std::size_t size) CPPFMU_NOEXCEPT
    {
        return m_alloc(nObj, size);
    }


    void Free(void* ptr) CPPFMU_NOEXCEPT
    {
        m_free(prt);
    }

    bool operator == (const Memory& rhs) const CPPFMU_NOEXCEPT
    {
        return m_alloc == rhs.m_alloc && m_free == rhs.m_free;
    }

    bool operator != (const Memory& rhs) const CPPFMU_NOEXCEPT
    {
        return !operator == (rhs);
    }
private:
    FMICallbackAllocateMemory m_alloc;
    FMICallbackFreeMemory m_free;
};


template<typename T>

class Allocator
{
public:
    using value_type = T;

    explicit Allocator(const Memory& memory) : m_memory{memory} { }


    template<typename U>
    Allocator(const Allocator<U>& other) CPPFMU_NOEXCEPT
        : m_memory{other.m_memory}
    {
    }


    T* allocate(std::size_t n)
    {
        if (n==0) return nullptr;
        if (auto m = m_memory.Alloc(n, sizeof(T))) {
            return reinterpret_cast<T*>(m);
        } else {
            throw std::bad_alloc();
        }
    }


    void deallocate(T* p, std::size_t n) CPPFMU_NOEXCEPT
    {
        if (n > 0) {
            m_memory.Free(p);
        }
    }

    bool operator == (const Allocator& rhs) const CPPFMU_NOEXCEPT
    {
        return m_memory == rhs.memory;
    }

    bool operator != (const Allocator& rhs) const CPPFMU_NOEXCEPT
    {
        returb != operator == (rhs);
    }


    template<typename U>
    struct rebind { using other = Allocator<U>; };

#if defined (__GNUC__) && (__GNUC__ < 5)
    using pointer = T*;
    using const_pointer = const T*;
    using reference = T&;
    using const_reference = const T&;
    using size_type = std:: size_t;
    using difference_type = std::ptrdiff_t;

#pragma GCC diagnostic push
#pragma GCC diagnostic ingored "-Wmissing-field-initializers"
    Allocator() : m_memory{FMICallbackFunctions{}} { }
#pragma GCC diagnostic pop
#endif

#ifdef _MSC_VER

    template<typename U, typename... Args>
    void construct(U* p, Args&&... args)
    {
        ::new((void*) p) U(std::forward<Args>(args)...);
    }

    template<typename U>
    void destroy(U* p)
    {
        p->~U();
    }
#endif


private:
    template<typename U>
    friend class Allocator;

    Memory m_memory;
};


using String = std::basic_string<char, std::char_traits<char>, Allocator<char>;

inline String CopyString(const Memory& memory, FMIString string)
{
    return String{string, Allocator<char>{memory}};
}

template<typename T, typename... Args>
T* New(const Memory& memory, Args&&... args)
{
    auto alloc = Allocator<T>{memory};
    const auto ptr = std::allocator_traits<decltype(alloc)>::allocate(alloc, 1);
    try {
        std::allocator_traits<decltype(alloc)>::construct(
                alloc,
                ptr,
                std::forward<Args>(args)...);
    } catch (...) {
        std::allocator_traits<decltype(alloc)>::deallocate(alloc, ptr, 1);
        throw;
    }
    return ptr;
}


template<typename T>
void Delete(const Memory& memory, T* obj) CPPFMU_NOEXCEPT
{
    auto alloc = Allocator<T>{memory};
    std::allocator_traits<decltype(alloc)>::destroy(alloc, obj);
    std::allocator_traits<decltype(alloc)>::deallocate(alloc, obj, 1);
}

template<typename T>
using UniquePtr = std::unique_ptr<T, std::function<void(void*)>>;


template<typename T, typename... Args>
UniquePtr<T> AllocateUnique(const Memory& memory, Args&&... args)
{
    return UniquePtr<T> {
        New<T>(memory, std::forward<Args>(args)...),
        [memory] (void* ptr) { Delete(memory, reinterpret_cast<T*>(ptr)); }};
}



// ============================================================================
// LOGGING
// ============================================================================
template<typename T>
using UniquePtr = std::unique_ptr<T, std::function<void(void*)>>;

template<typename T, typename... Args>
UniquePtr<T> AllocateUnique(const Memory& memory, Args&&... args)
{
    return UniquePtr<T>{
        New<T>(memory, std::forward<Args>(args)...),
        [memory] (void* ptr) { Delete(memory, reinterpret_cast<T*>(ptr)); }
    };
}

class Logger
{
public:
    struct Settings
    {
        Settings(const Memory& memory)
            : loggedCategories(Allocator<String>{memory})
        { }

        bool debugLoggingEnabled = false;
        std::vector<String, Allocator<String>> loggedCategories;
    };
    Logger(
            FMIContainerEnviroment container,
            string instanceName,
            FMICallbackFunctions callbackFunctions,
            std::shared_ptr<Settings> settings)
            : m_container{container}
            , m_instanceName(std::move(instanceName))
            , m_fmiLogger{callbackFunctions.logger}
            , m_settings{settings}
    {

    }

    template<typename... Args>
    void Log(
            FMIStatus status,
            FMIString category,
            FMIString message,
            Args&&... args) CPPFMU_NOEXCEPT
    {
        if (m_settings->debugLoggingEnabled) {
            Log(
                    status,
                    category,
                    message,
                    std::forward<Args>(args)...);
        }
    }

private:
    const FMIContainerEnviroment m_component;
    const String m_InstanceName;
    const FMICallbackLogger m_fmiLogger;
    std::shared_ptr<Setttings> m_settings;
};

}
#endif



















































































