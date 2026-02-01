from enum import IntEnum, StrEnum


class CalculationMethod(IntEnum):
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

    @classmethod
    def labels(cls) -> dict[int, str]:
        return {
            0: "Jafari / Shia Ithna-Ashari",
            1: "University of Islamic Sciences, Karachi",
            2: "Islamic Society of North America",
            3: "Muslim World League",
            4: "Umm Al-Qura University, Makkah",
            5: "Egyptian General Authority of Survey",
            7: "Institute of Geophysics, University of Tehran",
            8: "Gulf Region",
            9: "Kuwait",
            10: "Qatar",
            11: "Majlis Ugama Islam Singapura, Singapore",
            12: "Union Organization islamic de France",
            13: "Diyanet İşleri Başkanlığı, Turkey",
            14: "Spiritual Administration of Muslims of Russia",
            15: "Moonsighting Committee Worldwide (also requires shafaq parameter)",
            16: "Dubai (experimental)",
            17: "Jabatan Kemajuan Islam Malaysia (JAKIM)",
            18: "Tunisia",
            19: "Algeria",
            20: "KEMENAG - Kementerian Agama Republik Indonesia",
            21: "Morocco",
            22: "Comunidade Islamica de Lisboa",
            23: "Ministry of Awqaf, Islamic Affairs and Holy Places, Jordan",
            99: "Custom (see https://aladhan.com/calculation-methods)",
        }


class School(IntEnum):
    SHAFI = 0
    HANAFI = 1


class MidnightMode(IntEnum):
    STANDARD = 0
    JAFARI = 1


class LatitudeAdjustmentMethod(IntEnum):
    MIDDLE_OF_THE_NIGHT = 1
    ONE_SEVENTH = 2
    ANGLE_BASED = 3


class Shafaq(StrEnum):
    GENERAL = "general"
    AHMER = "ahmer"
    ABYAD = "abyad"


class CalendarMethod(StrEnum):
    HJCoSA = "HJCoSA"
    UAQ = "UAQ"
    DIYANET = "DIYANET"
    MATHEMATICAL = "MATHEMATICAL"
