from enum import Enum


class CalculationMethod(Enum):
    JAFARI = 0
    KARACHI = 1
    ISNA = 2
    MWL = 3
    MAKKAH = 4
    EGYPT = 5
    TEHRAN = 7
    GULF = 8
    KUWAIT = 9
    QATAR = 10
    SINGAPORE = 11
    FRANCE = 12
    TURKEY = 13
    RUSSIA = 14
    MOONSIGHTING = 15
    DUBAI = 16
    JAKIM = 17
    TUNISIA = 18
    ALGERIA = 19
    KEMENAG = 20
    MOROCCO = 21
    PORTUGAL = 22
    JORDAN = 23
    CUSTOM = 99


class School(Enum):
    SHAFI = 0
    HANAFI = 1


class MidnightMode(Enum):
    STANDARD = 0
    JAFARI = 1


class LatitudeAdjustmentMethod(Enum):
    MIDDLE_OF_THE_NIGHT = 1
    ONE_SEVENTH = 2
    ANGLE_BASED = 3


class Shafaq(Enum):
    GENERAL = "general"
    AHMER = "ahmer"
    ABYAD = "abyad"


class CalendarMethod(Enum):
    HJCoSA = "HJCoSA"
    UAQ = "UAQ"
    DIYANET = "DIYANET"
    MATHEMATICAL = "MATHEMATICAL"
