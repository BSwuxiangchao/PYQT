# -*- coding: utf-8 -*-


class DefaultProducts:
    @staticmethod
    def VidPid2Name(vid, pid, name):
        return name.decode('ascii')

    @staticmethod
    def VidPid2Prefix(vid, pid):
        return ''

class OrbbecProducts:
    """
    ORBBEC(@R) 产品相关名称，序列号的映射
    """

    __ORBBEC_VENDOR_ID = "0x2bc5"

    # 类的静态成员变量
    __PID2NAMEDICT_2BC5 = {
        "0x401": "Astra",
        "0x402": "Astra S",
        "0x403": "Astra Pro",
        "0x404": "Astra Mini",
        "0x405": "Orion",
        "0x406": "Hurley",
        "0x407": "Astra Mini S"
    }
    __NAME_UNKNOWN = "Unknown"

    __PIDPREFIXDICT_2BC5 = {
        "0x401": 'A',
        "0x402": 'B',
        "0x403": 'C',
        "0x404": 'D',
        "0x407": 'E'
    }
    __PID_PREFIX_UNKNOWN = ''

    @staticmethod
    def isThisType(vid, pid):
        hex_pid = hex(pid)
        hex_vid = hex(vid)
        if OrbbecProducts.__ORBBEC_VENDOR_ID == hex_vid and hex_pid in OrbbecProducts.__PID2NAMEDICT_2BC5:
            return True

        return False

    @staticmethod
    def __Pid2Name2bc5(pid):
        hex_pid = hex(pid)
        print(pid, hex_pid)
        if hex_pid in OrbbecProducts.__PID2NAMEDICT_2BC5:
            return OrbbecProducts.__PID2NAMEDICT_2BC5[hex_pid]

        return OrbbecProducts.__NAME_UNKNOWN

    @staticmethod
    def VidPid2Name(vid, pid, name):
        hex_vid = hex(vid)

        if "0x2bc5" == hex_vid:
            return OrbbecProducts.__Pid2Name2bc5(pid)

        return OrbbecProducts.__NAME_UNKNOWN

    @staticmethod
    def __GetPidPrefix2bc5(pid):
        hex_pid = hex(pid)
        if hex_pid in OrbbecProducts.__PIDPREFIXDICT_2BC5:
            return OrbbecProducts.__PIDPREFIXDICT_2BC5[hex_pid]

        return OrbbecProducts.__PID_PREFIX_UNKNOWN

    @staticmethod
    def VidPid2Prefix(vid, pid):
        hex_vid = hex(vid)

        if "0x2bc5" == hex_vid:
            return OrbbecProducts.__GetPidPrefix2bc5(pid)

        return OrbbecProducts.__NAME_UNKNOWN


class PrimeSenseProducts():
    # Todo...
    pass


class MicrosoftProducts():
    # Todo...
    pass


class XtionProducts():
    # Todo...
    pass