from enum import IntEnum, StrEnum
from typing import Literal


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
    def labels(cls, language: Literal["en", "ar", "de"] = "en") -> dict[int, str]:
        if language == "en":
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
        elif language == "ar":
            return {
                0: "الجعفري / الشيعة الإثنا عشرية",
                1: "جامعة العلوم الإسلامية، كراتشي",
                2: "الجمعية الإسلامية لأمريكا الشمالية",
                3: "رابطة العالم الإسلامي",
                4: "أم القرى، مكة المكرمة",
                5: "الهيئة المصرية العامة للمساحة",
                7: "معهد الجيوفيزياء، جامعة طهران",
                8: "منطقة الخليج",
                9: "الكويت",
                10: "قطر",
                11: "مجلس الشؤون الإسلامية في سنغافورة",
                12: "الاتحاد الإسلامي الفرنسي",
                13: "رئاسة الشؤون الدينية، تركيا",
                14: "الإدارة الروحية للمسلمين في روسيا",
                15: "لجنة رؤية الهلال العالمية (تتطلب أيضًا معلمة الشفق)",
                16: "دبي (تجريبي)",
                17: "(JAKIM) - إدارة التنمية الإسلامية الماليزية ",
                18: "تونس",
                19: "الجزائر",
                20: "KEMENAG - وزارة الشؤون الدينية لجمهورية إندونيسيا",
                21: "المغرب",
                22: "الجالية الإسلامية في لشبونة",
                23: "وزارة الأوقاف والشؤون الإسلامية والأماكن المقدسة، الأردن",
                99: "مخصص (انظر https://aladhan.com/calculation-methods)",
            }
        elif language == "de":
            return {
                0: "Jafari / Schia Ithna-Ashari",
                1: "Universität der Islamischen Wissenschaften, Karachi",
                2: "Islamische Gesellschaft von Nordamerika",
                3: "Muslimische Weltliga",
                4: "Umm Al-Qura Universität, Makkah",
                5: "Ägyptische Generaldirektion für Vermessung",
                7: "Institut für Geophysik, Universität Teheran",
                8: "Golfregion",
                9: "Kuwait",
                10: "Qatar",
                11: "Majlis Ugama Islam Singapura, Singapur",
                12: "Union Organization islamic de France",
                13: "Diyanet İşleri Başkanlığı, Türkei",
                14: "Spirituelle Verwaltung der Muslime in Russland",
                15: "Moonsighting Committee Worldwide (erfordert auch shafaq-Parameter)",
                16: "Dubai (experimentell)",
                17: "Jabatan Kemajuan Islam Malaysia (JAKIM)",
                18: "Tunesien",
                19: "Algerien",
                20: "KEMENAG - Kementerian Agama Republik Indonesien",
                21: "Marokko",
                22: "Comunidade Islamica de Lisboa",
                23: "Ministry of Awqaf, Islamic Affairs and Holy Places, Jordanien",
                99: "Benutzerdefiniert (siehe https://aladhan.com/calculation-methods)",
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
