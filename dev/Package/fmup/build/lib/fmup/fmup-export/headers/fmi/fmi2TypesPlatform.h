#ifndef fmi2TypesPlatform_h
#define fmi2TypesPlatform_h

/* Standard header file to define the argument types of the
   functions of the Functional Mock-up Interface 2.0.
*/


#define fmi2TypesPlatform "default"

/* Type definitions of variables passed as arguments
   Version "default" means:

   fmi2Component           : an opaque object pointer
   fmi2ComponentEnvironment: an opaque object pointer
   fmi2FMUstate            : an opaque object pointer
   fmi2ValueReference      : handle to the value of a variable
   fmi2Real                : double precision floating-point data type
   fmi2Integer             : basic signed integer data type
   fmi2Boolean             : basic signed integer data type
   fmi2Char                : character data type
   fmi2String              : a pointer to a vector of fmi2Char characters
                             ('\0' terminated, UTF8 encoded)
   fmi2Byte                : smallest addressable unit of the machine, typically one byte.
*/

// Create Pointers
   typedef void*           fmi2Component;
   typedef void*           fmi2ComponentEnvironment;
   typedef void*           fmi2FMUstate;
   typedef unsigned int    fmi2ValueReference;
   typedef double          fmi2Real   ;
   typedef int             fmi2Integer;
   typedef int             fmi2Boolean;
   typedef char            fmi2Char;
   typedef const fmi2Char* fmi2String;
   typedef char            fmi2Byte;

/* Values for fmi2Boolean  */
#define fmi2True  1
#define fmi2False 0


#endif
