#ifdef fmi2TypesPlatform_h
#define fmi2TypesPlatform_h



#define fmi2TypesPlatform "default"


// Create Pointers

    typedef void*   fmi2Componet;
    typedef void*   fmi2ComponetEnviroment;
    typedef void*   fmi2FMUstate;
    typedef unsigned int   fmi2ValueReference;
    typedef double   fmi2Real;
    typedef int   fmi2Integer;
    typedef int   fmi2Boolean;
    typedef char   fmi2Char;
    typedef const fmi2Char* fmi2String;
    typedef char    fmi2Byte;

#define fmi2True 1
#define fmi2False 0

#endif