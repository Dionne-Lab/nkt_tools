#ifndef NKTPDLL_H
#define NKTPDLL_H

/*!
 * \file NKTPDLL.h
 * \author HCH
 * \date 23 June 2017
 * \brief NKTP DLL Interface, a communication DLL for interfacing to NKT Photonics products being controlled via the Interbus protocol.
 * The NKTPDLL abstracts the burden of telegram creation and communication handling when communicating/controlling the NKT Photonics products.
 * \see http://www.nktphotonics.com/lasers-fibers/en/support/software-drivers/
 */

#if defined(NKTPDLL_LIBRARY)
  #ifdef __cplusplus
    #define NKTPDLL_EXPORT extern "C" __declspec(dllexport)
  #else
    #define NKTPDLL_EXPORT __declspec(dllexport)
  #endif
#else
  #ifdef __cplusplus
    #define NKTPDLL_EXPORT extern "C" __declspec(dllimport)
  #else
    #define NKTPDLL_EXPORT __declspec(dllimport)
  #endif
#endif

#ifdef __cplusplus
namespace NKTPDLL
{
#endif

/*!
 * \brief The tPortResultTypes enum
 */
enum tPortResultTypes
{
    OPSuccess = 0,          //!< 0 - Successfull operation.
    OPFailed = 1,           //!< 1 - The ::openPorts function has failed.
    OPPortNotFound = 2,     //!< 2 - The specified portname could not be found.
    OPNoDevices = 3,        //!< 3 - No devices found on the specified port.
    OPApplicationBusy = 4   //!< 4 - The function is not allowed to be invoked from within a callback function.
};
typedef unsigned char PortResultTypes;

/*!
 * \brief The tPointToPointPortStatus enum
 */
enum tP2PPortResultTypes
{
    P2PSuccess = 0,             //!< 0 - Successfull operation.
    P2PInvalidPortname = 1,     //!< 1 - Invalid portname provided.
    P2PInvalidLocalIP = 2,      //!< 2 - Invalid local IP provided.
    P2PInvalidRemoteIP = 3,     //!< 3 - Invalid remote IP provided.
    P2PPortnameNotFound = 4,    //!< 4 - Portname not found.
    P2PPortnameExists = 5,      //!< 5 - Portname already exists.
    P2PApplicationBusy = 6      //!< 6 - The function is not allowed to be invoked from within a callback function.
};
typedef unsigned char P2PPortResultTypes;

/*!
 * \brief The tDeviceResultTypes enum
 */
enum tDeviceResultTypes
{
    DevResultSuccess = 0,           //!< 0 - Successfull operation.
    DevResultWaitTimeout = 1,       //!< 1 - The function ::deviceCreate, timed out waiting for the device being ready.
    DevResultFailed = 2,            //!< 2 - The function ::deviceCreate, failed.
    DevResultDeviceNotFound = 3,    //!< 3 - The specified device could not be found in the internal device list.
    DevResultPortNotFound = 4,      //!< 4 - The function ::deviceCreate, failed due to not being able to find the specified port.
    DevResultPortOpenError = 5,     //!< 5 - The function ::deviceCreate, failed due to port not being open.
    DevResultApplicationBusy = 6    //!< 6 - The function is not allowed to be invoked from within a callback function.
};
typedef unsigned char DeviceResultTypes;

/*!
 * \brief The tDeviceModeTypes enum
 */
enum tDeviceModeTypes
{
    DevModeDisabled = 0,        //!< 0 - The device is disabled. Not being polled and serviced.
    DevModeAnalyzeInit = 1,     //!< 1 - The analyze cycle has been started for the device.
    DevModeAnalyze = 2,         //!< 2 - The analyze cycle is in progress. All default registers being read to determine its state.
    DevModeNormal = 3,          //!< 3 - The analyze cycle has completed and the device is ready.
    DevModeLogDownload = 4,     //!< 4 - A log is being downloaded from the device.
    DevModeError = 5,           //!< 5 - The device is in an error state.
    DevModeTimeout = 6,         //!< 6 - The connection to the device has been lost.
    DevModeUpload = 7,          //!< 7 - The device is in upload mode and can not be used normally.
};
typedef unsigned char DeviceModeTypes;

/*!
 * \brief The tRegisterResultTypes enum
 */
enum tRegisterResultTypes
{
    RegResultSuccess = 0,               //!<  0 - Successfull operation.
    RegResultReadError = 1,             //!<  1 - Arises from a registerWrite function with index > 0, if the pre-read fails.
    RegResultFailed = 2,                //!<  2 - The function ::registerCreate has failed.
    RegResultBusy = 3,                  //!<  3 - The module has reported a BUSY error, the kernel automatically retries on busy but have given up.
    RegResultNacked = 4,                //!<  4 - The module has Nacked the register, which typically means non existing register.
    RegResultCRCErr = 5,                //!<  5 - The module has reported a CRC error, which means the received message has CRC errors.
    RegResultTimeout = 6,               //!<  6 - The module has not responded in time. A module should respond in max. 75ms
    RegResultComError = 7,              //!<  7 - The module has reported a COM error, which typically means out of sync or garbage error.
    RegResultTypeError = 8,             //!<  8 - The datatype does not seem to match the register datatype.
    RegResultIndexError = 9,            //!<  9 - The index seem to be out of range of the register length.
    RegResultPortClosed = 10,           //!< 10 - The specified port is closed error. Could happen if the USB is unplugged in the middel of a sequence.
    RegResultRegisterNotFound = 11,     //!< 11 - The specified register could not be found in the internal register list for the specified device.
    RegResultDeviceNotFound = 12,       //!< 12 - The specified device could not be found in the internal device list.
    RegResultPortNotFound = 13,         //!< 13 - The specified portname could not be found.
    RegResultPortOpenError = 14,        //!< 14 - The specified portname could not be opened. The port might be in use by another application.
    RegResultApplicationBusy = 15       //!< 15 - The function is not allowed to be invoked from within a callback function.
};
typedef unsigned char RegisterResultTypes;

/*!
 * \brief The tRegisterDataTypes enum
 */
enum  tRegisterDataTypes
{
    RegData_Unknown = 0,    //!<  0 - Unknown/Undefined data type.
    RegData_Mixed = 1,      //!<  1 - Mixed content data type.
    RegData_U8 = 2,         //!<  2 - 8 bit unsigned data type (unsigned char).
    RegData_S8 = 3,         //!<  3 - 8 bit signed data type (char).
    RegData_U16 = 4,        //!<  4 - 16 bit unsigned data type (unsigned short).
    RegData_S16 = 5,        //!<  5 - 16 bit signed data type (short).
    RegData_U32 = 6,        //!<  6 - 32 bit unsigned data type (unsigned long).
    RegData_S32 = 7,        //!<  7 - 32 bit signed data type (long).
    RegData_F32 = 8,        //!<  8 - 32 bit floating point data type (float).
    RegData_U64 = 9,        //!<  9 - 64 bit unsigned data type (unsigned long long).
    RegData_S64 = 10,       //!< 10 - 64 bit signed data type (long long).
    RegData_F64 = 11,       //!< 11 - 64 bit floating point data type (double).
    RegData_Ascii = 12,     //!< 12 - Zero terminated ascii string data type.
    RegData_Paramset = 13,  //!< 13 - Parameterset data type. ::ParameterSetType
    RegData_B8 = 14,        //!< 14 - 8 bit binary data type (unsigned char).
    RegData_H8 = 15,        //!< 15 - 8 bit hexadecimal data type (unsigned char).
    RegData_B16 = 16,       //!< 16 - 16 bit binary data type (unsigned short).
    RegData_H16 = 17,       //!< 17 - 16 bit hexadecimal data type (unsigned short).
    RegData_B32 = 18,       //!< 18 - 32 bit binary data type (unsigned long).
    RegData_H32 = 19,       //!< 19 - 32 bit hexadecimal data type (unsigned long).
    RegData_B64 = 20,       //!< 20 - 64 bit binary data type (unsigned long long).
    RegData_H64 = 21,       //!< 21 - 64 bit hexadecimal data type (unsigned long long).
    RegData_DateTime = 22,  //!< 22 - Datetime data type. ::DateTimeType
};
typedef unsigned char RegisterDataTypes;

/*!
 * \brief The tRegisterPriorityTypes enum
 */
enum tRegisterPriorityTypes
{
    RegPriority_Low = 0,    //!< 0 - The register is polled with low priority.
    RegPriority_High = 1    //!< 1 - The register is polled with high priority.
};
typedef unsigned char RegisterPriorityTypes;

/*!
 * \brief The tPortStatusTypes enum
 */
enum tPortStatusTypes
{
    PortStatusUnknown = 0,     //!<  0 - Unknown status.
    PortOpening = 1,           //!<  1 - The port is opening.
    PortOpened = 2,            //!<  2 - The port is now open.
    PortOpenFail = 3,          //!<  3 - The port open failed.
    PortScanStarted = 4,       //!<  4 - The port scanning is started.
    PortScanProgress = 5,      //!<  5 - The port scanning progress.
    PortScanDeviceFound = 6,   //!<  6 - The port scan found a device.
    PortScanEnded = 7,         //!<  7 - The port scanning ended.
    PortClosing = 8,           //!<  8 - The port is closing.
    PortClosed = 9,            //!<  9 - The port is now closed.
    PortReady = 10             //!< 10 - The port is open and ready.
};
typedef unsigned char PortStatusTypes;

/*!
 * \brief The tDeviceStatusTypes enum
 */
enum tDeviceStatusTypes
{
    DeviceModeChanged = 0,          //!<  0 - devData contains 1 unsigned byte ::DeviceModeTypes
    DeviceLiveChanged = 1,          //!<  1 - devData contains 1 unsigned byte, 0=live off, 1=live on.
    DeviceTypeChanged = 2,          //!<  2 - devData contains 1 unsigned byte with DeviceType (module type).
    DevicePartNumberChanged = 3,    //!<  3 - devData contains a zero terminated string with partnumber.
    DevicePCBVersionChanged = 4,    //!<  4 - devData contains 1 unsigned byte with PCB version number.
    DeviceStatusBitsChanged = 5,    //!<  5 - devData contains 1 unsigned long with statusbits.
    DeviceErrorCodeChanged = 6,     //!<  6 - devData contains 1 unsigned short with errorcode.
    DeviceBlVerChanged = 7,         //!<  7 - devData contains a zero terminated string with Bootloader version.
    DeviceFwVerChanged = 8,         //!<  8 - devData contains a zero terminated string with Firmware version.
    DeviceModuleSerialChanged = 9,  //!<  9 - devData contains a zero terminated string with Module serialnumber.
    DevicePCBSerialChanged = 10,    //!< 10 - devData contains a zero terminated string with PCB serialnumber.
    DeviceSysTypeChanged = 11       //!< 11 - devData contains 1 unsigned byte with SystemType (system type).
};
typedef unsigned char DeviceStatusTypes;

/*!
 * \brief The tRegisterStatusTypes enum
 */
enum tRegisterStatusTypes
{
    RegSuccess = 0,     //!< 0 - Register operation was successfull.
    RegBusy = 1,        //!< 1 - Register operation resulted in a busy.
    RegNacked = 2,      //!< 2 - Register operation resulted in a nack, seems to be non existing register.
    RegCRCErr = 3,      //!< 3 - Register operation resulted in a CRC error.
    RegTimeout = 4,     //!< 4 - Register operation resulted in a timeout.
    RegComError = 5     //!< 5 - Register operation resulted in a COM error. Out of sync. or garbage error.
};
typedef unsigned char RegisterStatusTypes;

/*!
 * \brief The tDateTime struct 24 hour format
 */
#pragma pack(1)
typedef struct tDateTimeStruct
{
    unsigned char Sec;      //!< Seconds
    unsigned char Min;      //!< Minutes
    unsigned char Hour;     //!< Hours
    unsigned char Day;      //!< Day
    unsigned char Month;    //!< Months
    unsigned char Year;     //!< Years
} DateTimeType;
#pragma pack()

/*!
 * \brief The tParamSetUnitTypes enum
 */
enum tParamSetUnitTypes
{
    // Unit codes
    UnitNone = 0,       //!<  0 - none/unknown
    UnitmV = 1,         //!<  1 - mV
    UnitV = 2,          //!<  2 - V
    UnituA = 3,         //!<  3 - µA
    UnitmA = 4,         //!<  4 - mA
    UnitA = 5,          //!<  5 - A
    UnituW = 6,         //!<  6 - µW
    UnitcmW = 7,        //!<  7 - mW/100
    UnitdmW = 8,        //!<  8 - mW/10
    UnitmW = 9,         //!<  9 - mW
    UnitW = 10,         //!< 10 - W
    UnitmC = 11,        //!< 11 - °C/1000
    UnitcC = 12,        //!< 12 - °C/100
    UnitdC = 13,        //!< 13 - °C/10
    Unitpm = 14,        //!< 14 - pm
    Unitdnm = 15,       //!< 15 - nm/10
    Unitnm = 16,        //!< 16 - nm
    UnitPerCent = 17,   //!< 17 - %
    UnitPerMille = 18,  //!< 18 - ‰
    UnitcmA = 19,       //!< 19 - mA/100
    UnitdmA = 20,       //!< 20 - mA/10
    UnitRPM = 21,       //!< 21 - RPM
    UnitdBm = 22,       //!< 22 - dBm
    UnitcBm = 23,       //!< 23 - dBm/10
    UnitmBm = 24,       //!< 24 - dBm/100
    UnitdB = 25,        //!< 25 - dB
    UnitcB = 26,        //!< 26 - dB/10
    UnitmB = 27,        //!< 27 - dB/100
    Unitdpm = 28,       //!< 28 - pm/10
    UnitcV = 29,        //!< 29 - V/100
    UnitdV = 30,        //!< 30 - V/10
    Unitlm = 31,        //!< 31 - lm (lumen)
    Unitdlm = 32,       //!< 32 - lm/10
    Unitclm = 33,       //!< 33 - lm/100
    Unitmlm = 34        //!< 34 - lm/1000
};
typedef unsigned char ParamSetUnitTypes;

/*!
 * \brief The tParameterSet struct
 * \note This is how calculation on parametersets is done internally by modules:\n
 * DAC_value = (value * (X/Y)) + Offset; Where value is either ParameterSetType::StartVal or ParameterSetType::FactoryVal\n
 * value = (ADC_value * (X/Y)) + Offset; Where value often is available via another measurement register\n
 */
#pragma pack(1)
typedef struct tParamSetStruct
{
    ParamSetUnitTypes Unit;         //!< Unit type as defined in ::tParamSetUnitTypes
    unsigned char ErrorHandler;     //!< Warning/Errorhandler not used.
    unsigned short StartVal;        //!< Setpoint for Settings parameterset, unused in Measurement parametersets.
    unsigned short FactoryVal;      //!< Factory Setpoint for Settings parameterset, unused in Measurement parametersets.
    unsigned short ULimit;          //!< Upper limit.
    unsigned short LLimit;          //!< Lower limit.
    signed short Numerator;         //!< Numerator(X) for calculation.
    signed short Denominator;       //!< Denominator(Y) for calculation.
    signed short Offset;            //!< Offset for calculation
} ParameterSetType;
#pragma pack()


/*******************************************************************************************************
 * Port functions
 *******************************************************************************************************/
/** \name Port functions
  *@{
  */

/*!
 * \brief Returns a comma separated string with all existing ports.
 * \param portnames Pointer to a preallocated string area where the function will store the comma separated string.
 * \param maxLen Size of preallocated string area. The returned string may be truncated to fit into the allocated area.
 */
NKTPDLL_EXPORT void getAllPorts(char *portnames, unsigned short *maxLen);
typedef void (__cdecl *GetAllPortsFuncPtr)(char *portnames, unsigned short *maxLen);


/*!
 * \brief Returns a comma separated string with all allready opened ports.
 * \param portnames Pointer to a preallocated string area where the function will store the comma separated string.
 * \param maxLen Size of preallocated string area. The returned string may be truncated to fit into the allocated area.
 */
NKTPDLL_EXPORT void getOpenPorts(char *portnames, unsigned short *maxLen);
typedef void (__cdecl *GetOpenPortsFuncPtr)(char *portnames, unsigned short *maxLen);

/*!
 * \brief Creates or Modifies a point to point port.
 * \param portname Zero terminated string giving the portname. ex. "AcoustikPort1"
 * \param hostAddress Zero terminated string giving the local ip address. ex. "192.168.1.67"
 * \param hostPort The local port number.
 * \param clientAddress Zero terminated string giving the remote ip address. ex. "192.168.1.100"
 * \param clientPort The remote port number.
 * \param protocol \arg 0 Specifies TCP protocol.
                   \arg 1 Specifies UDP protocol.
 * \param msTimeout Telegram timeout value in milliseconds, typically set to 100ms.
 * \return ::tP2PPortResultTypes
*/
NKTPDLL_EXPORT P2PPortResultTypes pointToPointPortAdd(const char *portname, const char *hostAddress, const unsigned short hostPort, const char *clientAddress, const unsigned short clientPort, const unsigned char protocol, const unsigned char msTimeout);
typedef P2PPortResultTypes (__cdecl *PointToPointPortAddFuncPtr)(const char *portname, const char *hostAddress, const unsigned short hostPort, const char *clientAddress, const unsigned short clientPort, const unsigned char protocol, const unsigned char msTimeout);

/*!
 * \brief Retrieve an already created point to point port setting.
 * \param portname Zero terminated string giving the portname (case sensitive). ex. "AcoustikPort1"
 * \param hostAddress Pointer to a preallocated string area where the function will store the zero terminated string, describing the local ip address.
 * \param hostMaxLen Pointer to an unsigned char giving the size of the preallocated hostAddress area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \param hostPort Pointer to a preallocated short where the function will store the local port number.
 * \param clientAddress Pointer to a preallocated string area where the function will store the zero terminated string, describing the remote ip address.
 * \param clientMaxLen Pointer to an unsigned char giving the size of the preallocated clientAddress area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \param clientPort Pointer to a preallocated short where the function will store the client port number.
 * \param protocol Pointer to a preallocated char where the function will store the protocol.
                   \arg 0 Specifies TCP protocol.
                   \arg 1 Specifies UDP protocol.
 * \param msTimeout Pointer to a preallocated char where the function will store the timeout value.
 * \return ::tP2PPortResultTypes
 */
NKTPDLL_EXPORT P2PPortResultTypes pointToPointPortGet(const char *portname, char *hostAddress, unsigned char *hostMaxLen, unsigned short *hostPort, char *clientAddress, unsigned char *clientMaxLen, unsigned short *clientPort, unsigned char *protocol, unsigned char *msTimeout);
typedef P2PPortResultTypes (__cdecl *PointToPointPortGetFuncPtr)(const char *portname, char *hostAddress, unsigned char *hostMaxLen, unsigned short *hostPort, char *clientAddress, unsigned char *clientMaxLen, unsigned short *clientPort, unsigned char *protocol, unsigned char *msTimeout);

/*!
 * \brief Delete an already created point to point port.
 * \param portname Zero terminated string giving the portname (case sensitive). ex. "AcoustikPort1"
 * \return ::tP2PPortResultTypes
 */
NKTPDLL_EXPORT P2PPortResultTypes pointToPointPortDel(const char *portname);
typedef P2PPortResultTypes (__cdecl *PointToPointPortDelFuncPtr)(const char *portname);


/*!
 * \brief Opens the provided portname(s), or all available ports if an empty string provided. Repeatedly calls is allowed to reopen and/or rescan for devices.\n
 * \param portnames Zero terminated comma separated string giving the portnames to open (case sensitive). An empty string opens all available ports.
 * \param autoMode \arg 0 the openPorts function only opens the port. Busscanning and device creation is NOT automatically handled.
 *                 \arg 1 the openPorts function will automatically start the busscanning and create the found devices in the internal devicelist. The port is automatically closed if no devices found.
 * \param liveMode \arg 0 the openPorts function disables the continuously monitoring of the registers. No callback possible on register changes. Use ::registerRead, ::registerWrite & ::registerWriteRead functions.
 *                 \arg 1 the openPorts function will keep all the found or created devices in live mode, which means the Interbus kernel keeps monitoring all the found devices and their registers.
 *                  Please note that this will keep the modules watchdog alive as long as the port is open.
 * \return ::tPortResultTypes
 * \note The function may timeout after 2 seconds waiting for port ready status and return ::OPFailed.\n
 *       In case autoMode is specified this timeout is extended to 20 seconds to allow for busscanning to complete.
 */
NKTPDLL_EXPORT PortResultTypes openPorts(const char *portnames, const char autoMode, const char liveMode);
typedef PortResultTypes (__cdecl *OpenPortsFuncPtr)(const char *portnames, const char autoMode, const char liveMode);


/*!
 * \brief Closes the provided portname(s), or all opened ports if an empty string provided.
 * \param portnames Zero terminated comma separated string giving the portnames to close (case sensitive). An empty string closes all open ports.
 * \return ::tPortResultTypes
 * \note The function may timeout after 2 seconds waiting for port close to complete and return ::OPFailed.
 */
NKTPDLL_EXPORT PortResultTypes closePorts(const char *portnames);
typedef PortResultTypes (__cdecl *ClosePortsFuncPtr)(const char *portnames);


/*!
 * \brief Sets legacy busscanning on or off.
 * \param legacyScanning \arg 0 the busscanning is set to normal mode and allows for rolling masterId. In this mode the masterId is changed for each message to allow for out of sync. detection.
 *                       \arg 1 the busscanning is set to legacy mode and fixes the masterId at address 66(0x42). Some older modules does not accept masterIds other than 66(ox42).
 * \sa ::getLegacyBusScanning
 */
NKTPDLL_EXPORT void setLegacyBusScanning(const char legacyScanning);
typedef void (__cdecl *SetLegacyBusScanningFuncPtr)(const char legacyScanning);


/*!
 * \brief Gets legacy busscanning status.
 * \return An unsigned char, with legacyScanning status. 0 the busscanning is currently in normal mode. 1 the busscanning is currently in legacy mode.
 * \sa ::setLegacyBusScanning
 */
NKTPDLL_EXPORT unsigned char getLegacyBusScanning();
typedef unsigned char (__cdecl *GetLegacyBusScanningFuncPtr)();


/*!
 * \brief Retrieve ::tPortStatusTypes for a given port.
 * \param portname Zero terminated string giving the portname (case sensitive). ex. "COM1"
 * \param portStatus Pointer to a ::PortStatusTypes where the function will store the port status.
 * \return ::tPortResultTypes
 */
NKTPDLL_EXPORT PortResultTypes getPortStatus(const char *portname, PortStatusTypes *portStatus);
typedef PortResultTypes (__cdecl *getPortStatusFuncPtr)(const char *portname, PortStatusTypes *portStatus);


/*!
 * \brief Retrieve error message for a given port. An empty string indicates no error.
 * \param portname Zero terminated string giving the portname (case sensitive). ex. "COM1"
 * \param errorMessage Pointer to a preallocated string area where the function will store the zero terminated error string.
 * \param maxLen Pointer to an unsigned short giving the size of the preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \return ::tPortResultTypes
 */
NKTPDLL_EXPORT PortResultTypes getPortErrorMsg(const char *portname, char *errorMessage, unsigned short *maxLen);
typedef PortResultTypes (__cdecl *getPortErrorMsgFuncPtr)(const char *portname, char *errorMessage, unsigned short *maxLen);


/*! @} */

/*******************************************************************************************************
 * Dedicated - Register read functions
 *******************************************************************************************************/
/** \name Dedicated - Register read functions.
 * It is not necessary to open the port, create the device or register before using those functions, since they will do a dedicated action.
 * Even though an already opened port would be preffered in time critical situations where a lot of reads or writes is required.
  *@{
  */

/*!
 * \brief Reads a register value and returns the result in readData area.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param readData Pointer to a preallocated data area where the function will store the register value.
 * \param readSize Size of preallocated data area, modified by the function to reflect the actual length of the returned register value. The returned register value may be truncated to fit into the allocated area.
 * \param index Data index. Typically -1, but could be used to extract data from a specific position in the register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \sa ::registerReadU8, ::registerReadS8 etc.
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerRead(const char *portname, const unsigned char devId, const unsigned char regId, void *readData, unsigned char *readSize, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, void *readData, unsigned char *readSize, const short index);

/*!
 * \brief Reads an unsigned char (8bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to an unsigned char where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadU8(const char *portname, const unsigned char devId, const unsigned char regId, unsigned char *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadU8FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, unsigned char *value, const short index);

/*!
 * \brief Reads a signed char (8bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to a signed char where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadS8(const char *portname, const unsigned char devId, const unsigned char regId, signed char *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadS8FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, signed char *value, const short index);

/*!
 * \brief Reads an unsigned short (16bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to an unsigned short where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadU16(const char *portname, const unsigned char devId, const unsigned char regId, unsigned short *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadU16FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, unsigned short *value, const short index);

/*!
 * \brief Reads a signed short (16bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to a signed short where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadS16(const char *portname, const unsigned char devId, const unsigned char regId, signed short *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadS16FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, signed short *value, const short index);

/*!
 * \brief Reads an unsigned long (32bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to an unsigned long where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadU32(const char *portname, const unsigned char devId, const unsigned char regId, unsigned long *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadU32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, unsigned long *value, const short index);

/*!
 * \brief Reads a signed long (32bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to a signed long where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadS32(const char *portname, const unsigned char devId, const unsigned char regId, signed long *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadS32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, signed long *value, const short index);

/*!
 * \brief Reads an unsigned long long (64bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to an unsigned long long where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadU64(const char *portname, const unsigned char devId, const unsigned char regId, unsigned long long *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadU64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, unsigned long long *value, const short index);

/*!
 * \brief Reads a signed long long (64bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to a signed long long where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadS64(const char *portname, const unsigned char devId, const unsigned char regId, signed long long *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadS64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, signed long long *value, const short index);

/*!
 * \brief Reads a float (32bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to a float where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadF32(const char *portname, const unsigned char devId, const unsigned char regId, float *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadF32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, float *value, const short index);

/*!
 * \brief Reads a double (64bit) register value and returns the result in value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value Pointer to a double where the function will store the register value.
 * \param index Value index. Typically -1, but could be used to extract a value in a multi value register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadF64(const char *portname, const unsigned char devId, const unsigned char regId, double *value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadF64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, double *value, const short index);

/*!
 * \brief Reads a Ascii string register value and returns the result in readStr area.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param readStr Pointer to a preallocated string area where the function will store the register value.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \param index Value index. Typically -1, but could be used to extract a string in a mixed type register. Index is byte counted.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerReadAscii(const char *portname, const unsigned char devId, const unsigned char regId, char *readStr, unsigned char *maxLen, const short index);
typedef RegisterResultTypes (__cdecl *RegisterReadAsciiFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, char *readStr, unsigned char *maxLen, const short index);

/*! @} */

/*******************************************************************************************************
 * Dedicated - Register write functions
 *******************************************************************************************************/
/** \name Dedicated - Register write functions.
 * It is not necessary to open the port, create the device or register before using those functions, since they will do a dedicated action.
 * Even though an already opened port would be preffered in time critical situations where a lot of reads or writes is required.
  *@{
  */

/*!
 * \brief Writes a register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeData Pointer to a data area from where the write value will be extracted.
 * \param writeSize Size of data area, ex. number of bytes to write. Write size is limited to max 240 bytes
 * \param index Data index. Typically -1, but could be used to write data at a specific position in the register. Index is byte counted.
 *                          Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                          indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \sa ::registerWriteU8, ::registerWriteS8 etc.
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWrite(const char *portname, const unsigned char devId, const unsigned char regId, const void *writeData, const unsigned char writeSize, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const void *writeData, const unsigned char writeSize, const short index);

/*!
 * \brief Writes an unsigned char (8bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteU8(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned char value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteU8FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned char value, const short index);

/*!
 * \brief Writes a signed char (8bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteS8(const char *portname, const unsigned char devId, const unsigned char regId, const signed char value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteS8FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed char value, const short index);

/*!
 * \brief Writes an unsigned short (16bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteU16(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned short value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteU16FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned short value, const short index);

/*!
 * \brief Writes a signed short (16bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteS16(const char *portname, const unsigned char devId, const unsigned char regId, const signed short value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteS16FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed short value, const short index);

/*!
 * \brief Writes an unsigned long (32bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteU32(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteU32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long value, const short index);

/*!
 * \brief Writes a signed long (32bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteS32(const char *portname, const unsigned char devId, const unsigned char regId, const signed long value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteS32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed long value, const short index);

/*!
 * \brief Writes an unsigned long long (64bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteU64(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long long value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteU64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long long value, const short index);

/*!
 * \brief Writes a signed long long (64bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteS64(const char *portname, const unsigned char devId, const unsigned char regId, const signed long long value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteS64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed long long value, const short index);

/*!
 * \brief Writes a float (32bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteF32(const char *portname, const unsigned char devId, const unsigned char regId, const float value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteF32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const float value, const short index);

/*!
 * \brief Writes a double (64bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param value The register value to write.
 * \param index Value index. Typically -1, but could be used to write a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteF64(const char *portname, const unsigned char devId, const unsigned char regId, const double value, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteF64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const double value, const short index);

/*!
 * \brief Writes a string register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeStr The zero terminated string to write. WriteStr will be limited to 239 characters and the terminating zero, totally 240 bytes.
 * \param writeEOL \arg 0 Do NOT append End Of Line character (a null character) to the string.
 *                 \arg 1 Append End Of Line character to the string.
 * \param index Value index. Typically -1, but could be used to write a value in a mixed type register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteAscii(const char *portname, const unsigned char devId, const unsigned char regId, const char* writeStr, const char writeEOL, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteAsciiFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const char* writeStr, const char writeEOL, const short index);

/*! @} */

/*******************************************************************************************************
 * Dedicated - Register write/read functions (A write immediately followed by a read)
 *******************************************************************************************************/
/** \name Dedicated - Register write/read functions (A write immediately followed by a read)
 * It is not necessary to open the port, create the device or register before using those functions, since they will do a dedicated action.
 * Even though an already opened port would be preffered in time critical situations where a lot of reads or writes is required.
 *@{
 */

/*!
 * \brief Writes and Reads a register value before returning.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeData Pointer to a data area from where the write value will be extracted.
 * \param writeSize Size of write data area, ex. number of bytes to write.
 * \param readData Pointer to a preallocated data area where the function will store the register read value.
 * \param readSize Size of preallocated read data area, modified by the function to reflect the actual length of the read register value. The read register value may be truncated to fit into the allocated area.
 * \param index Data index. Typically -1, but could be used to write/read data at/from a specific position in the register. Index is byte counted.
 *                          Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                          indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \sa ::registerWriteReadU8, ::registerWriteReadS8 etc.
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteRead(const char *portname, const unsigned char devId, const unsigned char regId, const void *writeData, const unsigned char writeSize, void *readData, unsigned char *readSize, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const void *writeData, const unsigned char writeSize, void *readData, unsigned char *readSize, const short index);

/*!
 * \brief Writes and Reads an unsigned char (8bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to an unsigned char where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadU8(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned char writeValue, unsigned char *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadU8FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned char writeValue, unsigned char *readValue, const short index);

/*!
 * \brief Writes and Reads a signed char (8bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to a signed char where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadS8(const char *portname, const unsigned char devId, const unsigned char regId, const signed char writeValue, signed char *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadS8FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed char writeValue, signed char *readValue, const short index);

/*!
 * \brief Writes and Reads an unsigned short (16bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to an unsigned short where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadU16(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned short writeValue, unsigned short *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadU16FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned short writeValue, unsigned short *readValue, const short index);

/*!
 * \brief Writes and Reads a signed short (16bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to a signed short where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadS16(const char *portname, const unsigned char devId, const unsigned char regId, const signed short writeValue, signed short *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadS16FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed short writeValue, signed short *readValue, const short index);

/*!
 * \brief Writes and Reads an unsigned long (32bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to an unsigned long where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadU32(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long writeValue, unsigned long *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadU32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long writeValue, unsigned long *readValue, const short index);

/*!
 * \brief Writes and Reads a signed long (32bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to a signed long where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadS32(const char *portname, const unsigned char devId, const unsigned char regId, const signed long writeValue, signed long *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadS32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed long writeValue, signed long *readValue, const short index);

/*!
 * \brief Writes and Reads an unsigned long long (64bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to an unsigned long long where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadU64(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long long writeValue, unsigned long long *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadU64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const unsigned long long writeValue, unsigned long long *readValue, const short index);

/*!
 * \brief Writes and Reads a signed long long (64bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to a signed long long where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadS64(const char *portname, const unsigned char devId, const unsigned char regId, const signed long long writeValue, signed long long *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadS64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const signed long long writeValue, signed long long *readValue, const short index);

/*!
 * \brief Writes and Reads a float (32bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to a float where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadF32(const char *portname, const unsigned char devId, const unsigned char regId, const float writeValue, float *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadF32FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const float writeValue, float *readValue, const short index);

/*!
 * \brief Writes and Reads a double (64bit) register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeValue The register value to write.
 * \param readValue Pointer to a double where the function will store the register read value.
 * \param index Value index. Typically -1, but could be used to write and read a value in a multi value register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadF64(const char *portname, const unsigned char devId, const unsigned char regId, const double writeValue, double *readValue, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadF64FuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const double writeValue, double *readValue, const short index);

/*!
 * \brief Writes and Reads a string register value.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param writeStr The zero terminated string to write. WriteStr will be limited to 239 characters and the terminating zero, totally 240 bytes.
 * \param writeEOL \arg 0 Do NOT append End Of Line character (a null character) to the string.
 *                 \arg 1 Append End Of Line character to the string.
 * \param readStr Pointer to a preallocated string area where the function will store the register read value.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \param index Value index. Typically -1, but could be used to write and read a string in a mixed type register. Index is byte counted.
 *                           Index >= 0 activates a read-modify-write sequence: The complete register content is being read, then the
 *                           indexed content is modified and finally the complete content is written to the register.
 * \return A status result value ::tRegisterResultTypes
 * \note It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated write followed by a dedicated read.
 */
NKTPDLL_EXPORT RegisterResultTypes registerWriteReadAscii(const char *portname, const unsigned char devId, const unsigned char regId, const char* writeStr, const char writeEOL, char *readStr, unsigned char *maxLen, const short index);
typedef RegisterResultTypes (__cdecl *RegisterWriteReadAsciiFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const char* writeStr, const char writeEOL, char *readStr, unsigned char *maxLen, const short index);


/*! @} */

/*******************************************************************************************************
 * Dedicated - Device functions
 *******************************************************************************************************/
/** \name Dedicated - Device functions
 * Dedicated - Device functions could be used directly.\n
 * It is not necessary to open the port, create the device or register before using those functions, since they will do a dedicated action.
 * Even though an already opened port would be preffered in time critical situations where a lot of reads is required.
 *@{
 */

/*!
 * \brief Returns the module type for a specific device id (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId Given device id to retrieve device type for (module type).
 * \param devType Pointer to an unsigned char where the function stores the device type.
 * \return A status result value ::tDeviceResultTypes
 * \note Register address 0x61\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetType(const char *portname, const unsigned char devId, unsigned char *devType);
typedef DeviceResultTypes (__cdecl *DeviceGetTypeFuncPtr)(const char *portname, const unsigned char devId, unsigned char *devType);

/*!
 * \brief Returns the system type for a specific device id (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId Given device id to retrieve system type for (system type).
 * \param sysType Pointer to an unsigned char where the function stores the system type.
 * \return A status result value ::tDeviceResultTypes
 * \note Register address 0x6B\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetSysType(const char *portname, const unsigned char devId, unsigned char *sysType);
typedef DeviceResultTypes (__cdecl *DeviceGetSysTypeFuncPtr)(const char *portname, const unsigned char devId, unsigned char *sysType);

/*!
 * \brief Returns the partnumber for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param partnumber Pointer to a preallocated string area where the function will store the partnumber.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \return A status result value ::RegisterResultTypes
 * \note Register address 0x8E <b>Not all modules have a partnumber register.</b>\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetPartNumberStr(const char *portname, const unsigned char devId, char *partnumber, unsigned char *maxLen);
typedef DeviceResultTypes (__cdecl *DeviceGetPartNumberStrFuncPtr)(const char *portname, const unsigned char devId, char *partnumber, unsigned char *maxLen);

/*!
 * \brief Returns the PCB version for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param PCBVersion Pointer to a preallocated unsigned char where the function will store the PCB version.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x62\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetPCBVersion(const char *portname, const unsigned char devId, unsigned char *PCBVersion);
typedef DeviceResultTypes (__cdecl *DeviceGetPCBVersionFuncPtr)(const char *portname, const unsigned char devId, unsigned char *PCBVersion);

/*!
 * \brief Returns the status bits for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param statusBits Pointer to a preallocated unsigned long where the function will store the status bits.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x66\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetStatusBits(const char *portname, const unsigned char devId, unsigned long *statusBits);
typedef DeviceResultTypes (__cdecl *DeviceGetStatusBitsFuncPtr)(const char *portname, const unsigned char devId, unsigned long *statusBits);

/*!
 * \brief Returns the error code for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param errorCode Pointer to a preallocated unsigned short where the function will store the error code.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x67\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetErrorCode(const char *portname, const unsigned char devId, unsigned short *errorCode);
typedef DeviceResultTypes (__cdecl *DeviceGetErrorCodeFuncPtr)(const char *portname, const unsigned char devId, unsigned short *errorCode);

/*!
 * \brief Returns the bootloader version for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param version Pointer to a preallocated unsigned short where the function will store the bootloader version.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x6D\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetBootloaderVersion(const char *portname, const unsigned char devId, unsigned short *version);
typedef DeviceResultTypes (__cdecl *DeviceGetBootloaderVersionFuncPtr)(const char *portname, const unsigned char devId, unsigned short *version);

/*!
 * \brief Returns the bootloader version (string) for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param versionStr Pointer to a preallocated string area where the function will store the bootloader version.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x6D\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetBootloaderVersionStr(const char *portname, const unsigned char devId, char *versionStr, unsigned char *maxLen);
typedef DeviceResultTypes (__cdecl *DeviceGetBootloaderVersionStrFuncPtr)(const char *portname, const unsigned char devId, char *versionStr, unsigned char *maxLen);

/*!
 * \brief Returns the firmware version for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param version Pointer to a preallocated unsigned short where the function will store the firmware version.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x64\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetFirmwareVersion(const char *portname, const unsigned char devId, unsigned short *version);
typedef DeviceResultTypes (__cdecl *DeviceGetFirmwareVersionFuncPtr)(const char *portname, const unsigned char devId, unsigned short *version);

/*!
 * \brief Returns the firmware version (string) for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param versionStr Pointer to a preallocated string area where the function will store the firmware version.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x64\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetFirmwareVersionStr(const char *portname, const unsigned char devId, char *versionStr, unsigned char *maxLen);
typedef DeviceResultTypes (__cdecl *DeviceGetFirmwareVersionStrFuncPtr)(const char *portname, const unsigned char devId, char *versionStr, unsigned char *maxLen);

/*!
 * \brief Returns the Module serialnumber (string) for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param serialNumber Pointer to a preallocated string area where the function will store the serialnumber version.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x65\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetModuleSerialNumberStr(const char *portname, const unsigned char devId, char *serialNumber, unsigned char *maxLen);
typedef DeviceResultTypes (__cdecl *DeviceGetModuleSerialNumberStrFuncPtr)(const char *portname, const unsigned char devId, char *serialNumber, unsigned char *maxLen);

/*!
 * \brief Returns the PCB serialnumber (string) for a given device (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param serialNumber Pointer to a preallocated string area where the function will store the serialnumber version.
 * \param maxLen Size of preallocated string area, modified by the function to reflect the actual length of the returned string. The returned string may be truncated to fit into the allocated area.
 * \return A status result value ::tRegisterResultTypes
 * \note Register address 0x6E\n
 *       It is not necessary to open the port, create the device or register before using this function, since it will do a dedicated read.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetPCBSerialNumberStr(const char *portname, const unsigned char devId, char *serialNumber, unsigned char *maxLen);
typedef DeviceResultTypes (__cdecl *DeviceGetPCBSerialNumberStrFuncPtr)(const char *portname, const unsigned char devId, char *serialNumber, unsigned char *maxLen);


/*! @} */

/*******************************************************************************************************
 * Callback - Device functions
 *******************************************************************************************************/
/** \name Callback - Device functions
 * Device functions primarly used in callback environments.
 *@{
 */

/*!
 * \brief Creates a device in the internal devicelist. If the ::openPorts function has been called with the liveMode = 1 the kernel immediatedly starts to monitor the device.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param waitReady
                 \arg 0 Don't wait for the device being ready.
                 \arg 1 Wait up to 2 seconds for the device to complete its analyze cycle (All standard registers being successfully read).
 * \return A status result value ::tDeviceResultTypes
 */
NKTPDLL_EXPORT DeviceResultTypes deviceCreate(const char *portname, const unsigned char devId, const char waitReady);
typedef DeviceResultTypes (__cdecl *DeviceCreateFuncPtr)(const char *portname, const unsigned char devId, const char waitReady);

/*!
 * \brief Checks if a specific device already exists in the internal devicelist.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param exists Pointer to an unsigned char where the function will store the exists status.
                 \arg 0 Device does not exists.
                 \arg 1 Device exists.
 * \return A status result value ::tDeviceResultTypes
 */
NKTPDLL_EXPORT DeviceResultTypes deviceExists(const char *portname, const unsigned char devId, unsigned char *exists);
typedef DeviceResultTypes (__cdecl *DeviceExistsFuncPtr)(const char *portname, const unsigned char devId, unsigned char *exists);

/*!
 * \brief Remove a specific device from the internal devicelist.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \return A status result value ::tDeviceResultTypes
 */
NKTPDLL_EXPORT DeviceResultTypes deviceRemove(const char *portname, const unsigned char devId);
typedef DeviceResultTypes (__cdecl *DeviceRemoveFuncPtr)(const char *portname, const unsigned char devId);

/*!
 * \brief Remove all devices from the internal devicelist. No confirmation given, the list is simply cleared.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \return A status result value ::tDeviceResultTypes
 */
NKTPDLL_EXPORT DeviceResultTypes deviceRemoveAll(const char *portname);
typedef DeviceResultTypes (__cdecl *DeviceRemoveAllFuncPtr)(const char *portname);

/*!
 * \brief Returns a list with device types (module types) from the internal devicelist.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param types Pointer to a preallocated area where the function stores the list of module types. The default list size is 256 bytes long (0-255) where each position indicates module address, containing 0 for no module or the module type for addresses having a module.\n
 *  ex. 00h 61h 62h 63h 64h 65h 00h 00h 00h 00h 00h 00h 00h 00h 00h 60h 00h 00h etc.\n
 * Indicates module type 61h at address 1, module type 62h at address 2 etc. and module type 60h at address 15
 * \param maxTypes Pointer to an unsigned char giving the maximum number of types to retrieve.
                   The returned list may be truncated to fit into the allocated area.
 * \return A status result value ::tDeviceResultTypes
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetAllTypes(const char *portname, unsigned char *types, unsigned char *maxTypes);
typedef DeviceResultTypes (__cdecl *DeviceGetAllTypesFuncPtr)(const char *portname, unsigned char *types, unsigned char *maxTypes);

/*!
 * \brief Returns the internal device mode for a specific device id (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId Given device id to retrieve device mode for.
 * \param devMode Pointer to an ::DeviceModeTypes where the function stores the device mode value ::tDeviceModeTypes
 * \return A status result value ::tDeviceResultTypes
 * \note Requires the port being already opened with the ::openPorts function and the device being already created, either automatically or with the ::deviceCreate function.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetMode(const char *portname, const unsigned char devId, unsigned char *devMode);
typedef DeviceResultTypes (__cdecl *DeviceGetModeFuncPtr)(const char *portname, const unsigned char devId, unsigned char *devMode);

/*!
 * \brief Returns the internal device live status for a specific device id (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId Given device id to retrieve liveMode.
 * \param liveMode Pointer to an unsigned char where the function stores the live status.
                   \arg 0 liveMode off
                   \arg 1 liveMode on
 * \return A status result value ::tDeviceResultTypes
 * \note Requires the port being already opened with the ::openPorts function and the device being already created, either automatically or with the ::deviceCreate function.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceGetLive(const char *portname, const unsigned char devId, unsigned char *liveMode);
typedef DeviceResultTypes (__cdecl *DeviceGetLiveFuncPtr)(const char *portname, const unsigned char devId, unsigned char *liveMode);

/*!
 * \brief Sets the internal device live status for a specific device id (module address).
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId Given device id to set liveMode on.
 * \param liveMode An unsigned char giving the new live status.
                   \arg 0 liveMode off
                   \arg 1 liveMode on
 * \return A status result value ::tDeviceResultTypes
 * \note Requires the port being already opened with the ::openPorts function and the device being already created, either automatically or with the ::deviceCreate function.
 */
NKTPDLL_EXPORT DeviceResultTypes deviceSetLive(const char *portname, const unsigned char devId, const unsigned char liveMode);
typedef DeviceResultTypes (__cdecl *DeviceSetLiveFuncPtr)(const char *portname, const unsigned char devId, const unsigned char liveMode);


/*! @} */

/*******************************************************************************************************
 * Callback - Register functions
 *******************************************************************************************************/
/** \name Callback - Register functions
  *@{
  */

/*!
 * \brief Creates a register in the internal registerlist. If the ::openPorts function has been called with the liveMode = 1 the kernel immediatedly starts to monitor the register.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param priority The ::tRegisterPriorityTypes (monitoring priority).
 * \param dataType The ::tRegisterDataTypes, not used internally but could be used in a common callback function to determine data type.
 * \return A status result value ::tRegisterResultTypes
 */
NKTPDLL_EXPORT RegisterResultTypes registerCreate(const char *portname, const unsigned char devId, const unsigned char regId, const RegisterPriorityTypes priority, const RegisterDataTypes dataType);
typedef RegisterResultTypes (__cdecl *RegisterCreateFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, const RegisterPriorityTypes priority, const RegisterDataTypes dataType);

/*!
 * \brief Checks if a specific register already exists in the internal registerlist.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \param exists Pointer to an unsigned char where the function will store the exists status.
                 \arg 0 Register does not exists.
                 \arg 1 Register exists.
 * \return A status result value ::tRegisterResultTypes
 */
NKTPDLL_EXPORT RegisterResultTypes registerExists(const char *portname, const unsigned char devId, const unsigned char regId, unsigned char *exists);
typedef RegisterResultTypes (__cdecl *RegisterExistsFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId, unsigned char *exists);

/*!
 * \brief Remove a specific register from the internal registerlist.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regId The register id (register address).
 * \return A status result value ::tRegisterResultTypes
 */
NKTPDLL_EXPORT RegisterResultTypes registerRemove(const char *portname, const unsigned char devId, const unsigned char regId);
typedef RegisterResultTypes (__cdecl *RegisterRemoveFuncPtr)(const char *portname, const unsigned char devId, const unsigned char regId);

/*!
 * \brief Remove all registers from the internal registerlist. No confirmation given, the list is simply cleared.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \return A status result value ::tRegisterResultTypes
 */
NKTPDLL_EXPORT RegisterResultTypes registerRemoveAll(const char *portname, const unsigned char devId);
typedef RegisterResultTypes (__cdecl *RegisterRemoveAllFuncPtr)(const char *portname, const unsigned char devId);

/*!
 * \brief Returns a list with register ids (register addresses) from the internal registerlist.
 * \param portname Zero terminated string giving the portname (case sensitive).
 * \param devId The device id (module address).
 * \param regs Pointer to a preallocated area where the function stores the list of register ids (register addresses).
 * \param maxRegs Pointer to an unsigned char giving the maximum number of register ids to retrieve.
                  Modified by the function to reflect the actual number of register ids returned. The returned list may be truncated to fit into the allocated area.
 * \return A status result value ::tRegisterResultTypes
 */
NKTPDLL_EXPORT RegisterResultTypes registerGetAll(const char *portname, const unsigned char devId, unsigned char *regs, unsigned char *maxRegs);
typedef RegisterResultTypes (__cdecl *RegisterGetAllFuncPtr)(const char *portname, const unsigned char devId, unsigned char *regs, unsigned char *maxRegs);


/*! @} */

/*******************************************************************************************************
 * Callback - Support functions
 *******************************************************************************************************/
/** \name Callback - Support functions
 *@{
 */

/*!
 * \brief Defines the PortStatusCallbackFuncPtr for the ::openPorts and ::closePorts functions.
 * \param portname Zero terminated string giving the current portname.
 * \param status The current port status as a ::PortStatusTypes with a ::tPortStatusTypes value.
 * \param curScanAdr When status is ::PortScanProgress or ::PortScanDeviceFound this indicates the current module address scanned or found.
 * \param maxScanAdr When status is ::PortScanProgress or ::PortScanDeviceFound this indicates the last module address to be scanned.
 * \param foundType When status is ::PortScanDeviceFound this value will represent the found module type.
 * \note Please note that due to risk of circular runaway leading to stack overflow, it is not allowed to call functions in the DLL from within the callback function.
 * If a call is made to a function in the DLL the function will therefore return an application busy error.
 */
typedef void (__cdecl *PortStatusCallbackFuncPtr)(const char* portname,           // current port name
                                                  const PortStatusTypes status,   // current port status
                                                  const unsigned char curScanAdr, // current scanned address or device found address
                                                  const unsigned char maxScanAdr, // total addresses to scan
                                                  const unsigned char foundType); // device found type

/*!
 * \brief Enables/Disables callback for port status changes.
 * \param callback The ::PortStatusCallbackFuncPtr function pointer. Disable callbacks by parsing in a zero value.
 */
NKTPDLL_EXPORT void setCallbackPtrPortInfo(PortStatusCallbackFuncPtr callback);
typedef void (__cdecl *SetCallbackPtrPortInfoFuncPtr)(PortStatusCallbackFuncPtr callback);


/*!
 * \brief Defines the DeviceStatusCallbackFuncPtr for the devices created with the ::deviceCreate function or created automatically via the ::openPorts function (Having autoMode = 1).
 * \param portname Zero terminated string giving the current portname.
 * \param devId The device id (module address).
 * \param status The current port status as a ::DeviceStatusTypes with a ::tDeviceStatusTypes value.
 * \note Please note that due to risk of circular runaway leading to stack overflow, it is not allowed to call functions in the DLL from within the callback function.
 * If a call is made to a function in the DLL the function will therefore return an application busy error.
 */
typedef void (__cdecl *DeviceStatusCallbackFuncPtr)(const char* portname,                     // current port name
                                                    const unsigned char devId,                // current device id
                                                    const DeviceStatusTypes status,           // current device status
                                                    const unsigned char devDataLen,           // number of bytes in devData
                                                    const void* devData);                     // device data as specified in status

/*!
 * \brief Enables/Disables callback for device status changes.
 * \param callback The ::DeviceStatusCallbackFuncPtr function pointer. Disable callbacks by parsing in a zero value.
 */
NKTPDLL_EXPORT void setCallbackPtrDeviceInfo(DeviceStatusCallbackFuncPtr callback);
typedef void (__cdecl *SetCallbackPtrDeviceInfoFuncPtr)(DeviceStatusCallbackFuncPtr callback);



/*!
 * \brief Defines the RegisterStatusCallbackFuncPtr for the registers created or connected with the ::registerCreate function.
 * \param portname Zero terminated string giving the current portname.
 * \param status The current register status as a ::RegisterStatusTypes with a ::tRegisterStatusTypes value.
 * \param regType The ::RegisterDataTypes, not used internally but could be used in a common callback function to determine data type.
 * \param regDataLen Number of databytes.
 * \param regData The register data.
 * \note Please note that due to risk of circular runaway leading to stack overflow, it is not allowed to to call functions in the DLL from within the callback function.
 * If a call is made to a function in the DLL the function will therefore return an application busy error.
 */
typedef void (__cdecl *RegisterStatusCallbackFuncPtr)(const char* portname,                       // current port name
                                                      const unsigned char devId,                  // current device id
                                                      const unsigned char regId,                  // current device id
                                                      const RegisterStatusTypes status,           // current register status
                                                      const RegisterDataTypes regType,            // current register type
                                                      const unsigned char regDataLen,             // number of bytes in regData
                                                      const void *regData);                       // register data

/*!
 * \brief Enables/Disables callback for register status changes.
 * \param callback The ::RegisterStatusCallbackFuncPtr function pointer. Disable callbacks by parsing in a zero value.
 */
NKTPDLL_EXPORT void setCallbackPtrRegisterInfo(RegisterStatusCallbackFuncPtr callback);
typedef void (__cdecl *SetCallbackPtrRegisterInfoFuncPtr)(RegisterStatusCallbackFuncPtr callback);

/*! @} */

/*******************************************************************************************************
 * LabView - Support functions
 *******************************************************************************************************/
/** \name LabView - Support functions
  *@{
  */

/*!
 * \brief lvPortStatusStruct, A LabView userevent data package
 */
#pragma pack(1)
typedef struct lvPortStatusStruct
{
    char portname[32];        //!< Zero terminated string giving the originating portname.
    PortStatusTypes status;   //!< The current port status as ::tPortStatusTypes
    unsigned char curScanAdr; //!< When status is ::PortScanProgress or ::PortScanDeviceFound this indicates the current module address scanned or found.
    unsigned char maxScanAdr; //!< When status is ::PortScanProgress or ::PortScanDeviceFound this indicates the last module address to be scanned.
    unsigned char foundType;  //!< When status is ::PortScanDeviceFound this value will represent the found module type.
} LabViewPortStatusType;
#pragma pack()

/*!
 * \brief Enables/Disables labView user events for port status changes. Disable events by parsing in a zero value.
 * \param lvUserEventRef A LabView "MagicCookie" to identify userevent type.
 */
NKTPDLL_EXPORT void setLVUserEventPortInfo(unsigned long *lvUserEventRef);
typedef void (__cdecl *SetLVUserEventPortInfoFuncPtr)(unsigned long *lvUserEventRef);


/*!
 * \brief lvDeviceStatusStruct, A LabView userevent data package
 */
#pragma pack(1)
typedef struct lvDeviceStatusStruct
{
    char portname[32];                  //!< Zero terminated string giving the originating portname.
    unsigned char devId;                //!< The originating device id (module address).
    DeviceStatusTypes status;           //!< The current port status as ::tDeviceStatusTypes
    unsigned char devDataLen;           //!< Number of databytes in devData
    unsigned char devData[255];         //!< device data as specified in status.
} LabViewDeviceStatusType;
#pragma pack()

/*!
 * \brief Enables/Disables labView user events for device status changes. Disable events by parsing in a zero value.
 * \param lvUserEventRef A LabView "MagicCookie" to identify userevent type.
 */
NKTPDLL_EXPORT void setLVUserEventDeviceInfo(unsigned long *lvUserEventRef);
typedef void (__cdecl *SetLVUserEventDeviceInfoFuncPtr)(unsigned long *lvUserEventRef);

/*!
 * \brief lvRegisterStatusStruct, A LabView userevent data package
 */
#pragma pack(1)
typedef struct lvRegisterStatusStruct
{
    char portname[32];                  //!< Zero terminated string giving the originating portname.
    unsigned char devId;                //!< The originating device id (module address).
    unsigned char regId;                //!< The originating register id.
    RegisterStatusTypes status;         //!< The current register status as a ::tRegisterStatusTypes value.
    RegisterDataTypes regType;          //!< The ::tRegisterDataTypes, not used internally but could be used in a common callback function to determine data type. Set when the register is created with ::registerCreate
    unsigned char regDataLen;           //!< Number of databytes.
    unsigned char regData[255];         //!< The register data.
} LabViewRegisterStatusType;
#pragma pack()

/*!
 * \brief Enables/Disables labView user events for register status changes. Disable events by parsing in a zero value.
 * \param lvUserEventRef A LabView "MagicCookie" to identify userevent type.
 */
NKTPDLL_EXPORT void setLVUserEventRegisterInfo(unsigned long *lvUserEventRef);
typedef void (__cdecl *SetLVUserEventRegisterInfoFuncPtr)(unsigned long *lvUserEventRef);

/*! @} */

#ifdef __cplusplus
} // namespace NKTPDLL
#endif

#endif // NKTPDLL_H
