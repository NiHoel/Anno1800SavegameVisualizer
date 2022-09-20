import copy
import csv
from datetime import datetime
import io
import json
import math
import numpy as np
import os
import PIL.Image  # non-standard but in matplotlib
import IPython.display
import pathlib
import random
import re
import shutil
import subprocess
import struct
import sys
import lxml.etree as ET
import zlib
import zipfile

from ipywidgets import *

A7PARAMS = {
    "languages": ["chinese", "english", "french", "german", "italian", "japanese", "korean", "polish", "russian",
                  "spanish", "taiwanese"],
    "island_sizes": {'campaign_colony01_atoll_01': [384, 384], 'campaign_colony01_burnt_island_01': [192, 192],
                     'campaign_colony01_la_isla_01': [320, 320], 'campaign_colony01_prosperity_01': [320, 320],
                     'campaign_colony01_prologue': [320, 320], 'campaign_colony01_prologue_deco': [384, 384],
                     'campaign_moderate_enemy01_01': [320, 320], 'campaign_moderate_player01_01': [320, 320],
                     'campaign_moderate_pyrphorians01': [192, 192], 'colony01_3rdparty04_01': [256, 256],
                     'colony01_3rdparty05_01': [128, 128], 'colony01_d_01': [128, 128], 'colony01_d_02': [128, 128],
                     'colony01_d_03': [128, 128], 'colony01_d_04': [128, 128], 'colony01_d_05': [128, 128],
                     'colony01_d_06': [128, 128], 'colony01_d_07': [64, 64], 'colony01_d_08': [128, 128],
                     'colony01_d_09': [128, 128], 'colony01_d_10': [128, 128], 'colony01_d_11': [128, 128],
                     'colony01_d_12': [128, 128], 'colony01_d_13': [128, 128], 'colony01_d_14': [128, 128],
                     'colony01_d_15': [128, 128], 'colony01_d_16': [128, 128], 'colony01_d_17': [128, 128],
                     'colony01_d_18': [128, 128], 'colony01_d_19': [128, 128], 'colony01_d_20': [128, 128],
                     'colony01_l_01': [320, 320], 'colony01_l_01_river_01': [320, 320], 'colony01_l_02': [384, 384],
                     'colony01_l_02_river_01': [384, 384], 'colony01_l_03': [384, 384],
                     'colony01_l_03_river_01': [384, 384], 'colony01_l_04': [320, 320],
                     'colony01_l_04_river_01': [320, 320], 'colony01_l_05': [320, 320],
                     'colony01_l_05_river_01': [320, 320], 'colony01_m_01': [320, 320],
                     'colony01_m_01_river_01': [320, 320], 'colony01_m_02': [320, 320],
                     'colony01_m_02_river_01': [320, 320], 'colony01_m_03': [320, 320],
                     'colony01_m_03_river_01': [320, 320], 'colony01_m_04': [320, 320],
                     'colony01_m_04_river_01': [320, 320], 'colony01_m_05': [320, 320],
                     'colony01_m_05_river_01': [320, 320], 'colony01_m_06': [320, 320],
                     'colony01_m_06_river_01': [320, 320], 'colony01_s_01': [192, 192], 'colony01_s_02': [192, 192],
                     'colony01_s_03': [192, 192], 'colony01_s_04': [192, 192], 'community_island': [320, 320],
                     'community_island_river_01': [320, 320], 'moderate_3rdparty02_01': [128, 128],
                     'moderate_3rdparty03_01': [192, 192], 'moderate_3rdparty07_01': [128, 128],
                     'moderate_3rdparty08_01': [128, 128], 'moderate_d_01': [64, 64], 'moderate_d_02': [64, 64],
                     'moderate_d_03': [128, 128], 'moderate_d_04': [64, 64], 'moderate_d_05': [128, 128],
                     'moderate_d_06': [128, 128], 'moderate_d_07': [128, 128], 'moderate_d_08': [128, 128],
                     'moderate_d_09': [128, 128], 'moderate_d_10': [128, 128], 'moderate_d_11': [128, 128],
                     'moderate_d_12': [128, 128], 'moderate_d_13': [128, 128], 'moderate_d_14': [128, 128],
                     'moderate_d_15': [128, 128], 'moderate_l_01': [384, 384], 'moderate_l_01_river_01': [384, 384],
                     'moderate_l_02': [320, 320], 'moderate_l_02_river_01': [320, 320], 'moderate_l_03': [384, 384],
                     'moderate_l_03_river_01': [384, 384], 'moderate_l_04': [384, 384],
                     'moderate_l_04_river_01': [384, 384], 'moderate_l_05': [384, 384],
                     'moderate_l_05_river_01': [384, 384], 'moderate_l_06': [384, 384],
                     'moderate_l_06_river_01': [384, 384], 'moderate_l_07': [320, 320],
                     'moderate_l_07_river_01': [320, 320], 'moderate_l_08': [320, 320],
                     'moderate_l_08_river_01': [320, 320], 'moderate_l_09': [320, 320],
                     'moderate_l_09_river_01': [320, 320], 'moderate_l_10': [384, 384],
                     'moderate_l_10_river_01': [384, 384], 'moderate_l_11': [384, 384],
                     'moderate_l_11_river_01': [384, 384], 'moderate_l_12': [384, 384],
                     'moderate_l_12_river_01': [384, 384], 'moderate_l_13': [320, 320],
                     'moderate_l_13_river_01': [320, 320], 'moderate_l_14': [384, 384],
                     'moderate_l_14_river_01': [384, 384], 'moderate_m_01': [320, 320],
                     'moderate_m_01_river_01': [320, 320], 'moderate_m_02': [320, 320],
                     'moderate_m_02_river_01': [320, 320], 'moderate_m_03': [320, 320],
                     'moderate_m_03_river_01': [320, 320], 'moderate_m_04': [320, 320],
                     'moderate_m_04_river_01': [320, 320], 'moderate_m_05': [320, 320],
                     'moderate_m_05_river_01': [320, 320], 'moderate_m_06': [320, 320],
                     'moderate_m_06_river_01': [320, 320], 'moderate_m_07': [320, 320],
                     'moderate_m_07_river_01': [320, 320], 'moderate_m_08': [320, 320],
                     'moderate_m_08_river_01': [320, 320], 'moderate_m_09': [320, 320],
                     'moderate_m_09_river_01': [320, 320], 'moderate_s_01': [128, 128], 'moderate_s_02': [192, 192],
                     'moderate_s_03': [192, 192], 'moderate_s_04': [128, 128], 'moderate_s_05': [128, 128],
                     'moderate_s_06': [192, 192], 'moderate_s_07': [128, 128], 'moderate_s_08': [128, 128],
                     'moderate_s_09': [128, 128], 'moderate_s_10': [192, 192], 'moderate_s_11': [128, 128],
                     'moderate_s_12': [128, 128], 'moderate_3rdparty06_01': [128, 128],
                     'colony03_3rdparty09_01': [192, 192], 'colony03_a01_01': [320, 320], 'colony03_a01_02': [320, 320],
                     'colony03_a01_02_mp': [320, 320], 'colony03_a01_03': [320, 320], 'colony03_a01_04': [320, 320],
                     'colony03_a01_05': [128, 128], 'colony03_a01_06': [128, 128], 'colony03_a01_07': [128, 128],
                     'colony03_a01_08': [128, 128], 'colony03_a02_01': [256, 256], 'colony03_a02_02': [256, 256],
                     'colony03_a02_03': [256, 256], 'colony03_a02_04': [256, 256], 'colony03_a03_01': [768, 768],
                     'colony03_d_01': [64, 64], 'colony03_d_02': [64, 64], 'colony03_d_03': [64, 64],
                     'colony03_d_04': [64, 64], 'colony03_d_05': [64, 64], 'colony03_d_06': [64, 64],
                     'colony03_d_07': [64, 64], 'colony03_d_08': [64, 64], 'colony03_d_09': [64, 64],
                     'colony03_d_10': [64, 64], 'colony03_d_11': [64, 64], 'colony03_d_12': [64, 64],
                     'colony03_d_13': [64, 64], 'colony03_d_14': [64, 64], 'colony03_d_15': [64, 64],
                     'colony03_d_16': [64, 64], 'colony03_d_17': [64, 64], 'colony03_d_18': [64, 64],
                     'colony02_3rdparty10_01': [320, 320], 'colony02_d_01': [128, 128], 'colony02_d_02': [128, 128],
                     'colony02_d_03': [128, 128], 'colony02_d_04': [128, 128], 'colony02_d_05': [128, 128],
                     'colony02_d_06': [128, 128], 'colony02_d_07': [128, 128], 'colony02_d_08': [128, 128],
                     'colony02_d_09': [128, 128], 'colony02_d_10': [128, 128], 'colony02_l_01': [320, 320],
                     'colony02_l_03': [320, 320], 'colony02_l_05': [384, 384], 'colony02_l_06': [384, 384],
                     'colony02_m_02': [320, 320], 'colony02_m_04': [320, 320], 'colony02_m_05': [320, 320],
                     'colony02_m_09': [256, 256], 'colony02_settlement_01': [192, 192],
                     'colony02_storyisland_01': [192, 192], 'colony02_storyisland_02': [192, 192],
                     'colony02_storyisland_03': [192, 192], 'colony02_s_01': [192, 192], 'colony02_s_02': [192, 192],
                     'colony02_s_03': [256, 256], 'colony02_s_05': [192, 192], 'scenario02_blocker_01': [192, 192],
                     'scenario02_d_01': [128, 128], 'scenario02_d_02': [128, 128], 'scenario02_d_03': [128, 128],
                     'scenario02_d_05': [128, 128], 'scenario02_d_06': [128, 128], 'scenario02_d_07': [128, 128],
                     'scenario02_d_08': [128, 128], 'scenario02_d_09': [128, 128], 'scenario02_d_10': [128, 128],
                     'scenario02_d_11': [128, 128], 'scenario02_l_01': [320, 320], 'scenario02_s_01': [192, 192],
                     'scenario02_s_02': [192, 192], 'scenario03_3rdparty04_01': [256, 256],
                     'scenario03_d_01': [128, 128], 'scenario03_d_01_aa': [128, 128], 'scenario03_d_02': [128, 128],
                     'scenario03_d_02_aa': [128, 128], 'scenario03_d_03': [128, 128], 'scenario03_d_04': [128, 128],
                     'scenario03_d_04_aa': [128, 128], 'scenario03_d_05': [128, 128], 'scenario03_d_07': [64, 64],
                     'scenario03_d_09': [128, 128], 'scenario03_d_10': [128, 128], 'scenario03_d_11': [128, 128],
                     'scenario03_d_12': [128, 128], 'scenario03_d_12_aa': [128, 128], 'scenario03_d_13': [128, 128],
                     'scenario03_d_14': [128, 128], 'scenario03_d_15': [128, 128], 'scenario03_d_16': [128, 128],
                     'scenario03_d_17': [128, 128], 'scenario03_d_17_aa': [128, 128], 'scenario03_d_18': [128, 128],
                     'scenario03_d_19': [128, 128], 'scenario03_d_20': [128, 128], 'scenario03_d_20_aa': [128, 128],
                     'scenario03_l_04': [320, 320], 'scenario03_m_01': [320, 320],
                     'scenario03_m_01_river_01': [320, 320], 'scenario03_storyisland_01': [128, 128],
                     'scenario03_storyisland_02': [128, 128], 'scenario03_storyisland_03': [192, 192],
                     'scenario03_storyisland_04': [192, 192], 'scenario03_storyisland_05': [192, 192],
                     'scenario03_s_01': [192, 192], 'scenario03_s_02': [192, 192], 'scenario03_s_03': [192, 192],
                     'scenario03_s_04': [192, 192], 'colony01_dggj_01': [128, 128], 'colony01_dggj_02': [64, 64],
                     'colony01_dggj_03': [64, 64], 'colony01_dggj_04': [128, 128], 'colony01_dggj_05': [128, 128],
                     'colony01_dggj_06': [128, 128], 'colony01_dggj_07': [128, 128], 'colony01_dggj_08': [128, 128],
                     'colony01_dggj_09': [128, 128], 'colony01_dggj_10': [128, 128], 'colony01_dggj_11': [128, 128],
                     'ggj_l_01': [384, 384]},
    "range_extension_buffs": {249968: 10, 269502: 12, 269511: 14, 269512: 16, 269513: 18, 269514: 20, 269515: 22,
                              269516: 24, 269517: 26, 269518: 28, 269519: 30, 269716: 32, 269717: 34, 269718: 36,
                              269719: 38, 269720: 40, 269721: 42, 269722: 44, 269723: 46, 269724: 48, 269725: 50,
                              269726: 52, 269727: 54, 269728: 56, 269729: 58, 269730: 60, 269231: 15},
    "session_names": {
        180023: {"brazilian": "The Old World", "chinese": "旧世界", "english": "The Old World", "french": "L'Ancien Monde",
                 "german": "Die Alte Welt", "italian": "Il Vecchio Mondo", "japanese": "旧世界", "korean": "구대륙",
                 "polish": "Stary Świat", "portuguese": "The Old World", "russian": "Старый Свет",
                 "spanish": "El Viejo Mundo", "taiwanese": "舊世界"},
        180025: {"brazilian": "The New World", "chinese": "新世界", "english": "The New World",
                 "french": "Le Nouveau Monde", "german": "Die Neue Welt", "italian": "Il Nuovo Mondo",
                 "japanese": "新世界", "korean": "신대륙", "polish": "Nowy Świat", "portuguese": "The New World",
                 "russian": "Новый Свет", "spanish": "El Nuevo Mundo", "taiwanese": "新世界"},
        110934: {"chinese": "崔老妮海角", "english": "Cape Trelawney", "french": "Cap Trelawney", "german": "Kap Trelawney",
                 "italian": "Capo Trelawney", "japanese": "トレローニー岬", "korean": "트릴로니 곶",
                 "polish": "Przylądek Trelawney", "russian": "Мыс Трелони", "spanish": "Cabo de Trelawney",
                 "taiwanese": "崔老妮海角"},
        180045: {"brazilian": "The Arctic", "chinese": "北极", "english": "The Arctic", "french": "L'Arctique",
                 "german": "Die Arktis", "italian": "L'Artico", "japanese": "北極圏", "korean": "북극", "polish": "Arktyka",
                 "portuguese": "The Arctic", "russian": "Арктика", "spanish": "El Ártico", "taiwanese": "北極"},
        112132: {"chinese": "安贝沙", "english": "Enbesa", "french": "Enbesa", "german": "Enbesa", "italian": "Enbesa",
                 "japanese": "エンベサ", "korean": "엔베사", "polish": "Enbesa", "russian": "Энбеса", "spanish": "Enbesa",
                 "taiwanese": "安貝沙"},
        655: {
            "chinese": "祖尔图纳",
            "english": "La Xultuna",
            "french": "La Xultuna",
            "german": "La Xultuna",
            "italian": "La Xultuna",
            "japanese": "ラ・シュルツーナ",
            "korean": "라 줄투나",
            "polish": "La Xultuna",
            "russian": "Ла-Зультуна",
            "spanish": "La Xultuna",
            "taiwanese": "祖爾圖納"
        },
        24734: {
            "chinese": "净化之岛",
            "english": "Isles of Purgation",
            "french": "Îles de la Pénitence",
            "german": "Inseln der Reinigung",
            "italian": "Isole della Purificazione",
            "japanese": "贖罪の島",
            "korean": "속죄의 섬",
            "polish": "Wyspy Oczyszczenia",
            "russian": "Острова Искупления",
            "spanish": "Isla Purgación",
            "taiwanese": "淨化之島"
        },
        100811: {
            "chinese": "邮政赛场",
            "english": "Grand Postal Arena",
            "french": "Arène des postes",
            "german": "Postpokal-Region",
            "italian": "Grande Arena postale",
            "japanese": "郵便アリーナ",
            "korean": "그랜드 포스탈 아레나",
            "polish": "Wielka Arena Pocztowa",
            "russian": "Почтовая Арена",
            "spanish": "Gran Arena Postal",
            "taiwanese": "郵政賽場"
        },
    },
    "scenarios": {
        "Scenario1": 655,
        "Scenario2": 24734,
        "Scenario3": 100811,
    },
    "city_names": {
                   1000: {'chinese': '欧德亨尔', 'english': 'Roderrenge', 'french': 'Roderrenge', 'german': 'Roderrenge',
                          'italian': 'Roderrenge', 'japanese': 'ロダーレンジ', 'korean': '로더렌게', 'polish': 'Roderrenge',
                          'portuguese': 'Roderrenge', 'russian': 'Родеррендж', 'spanish': 'Roderrenge',
                          'taiwanese': '歐德亨爾'},
                   1001: {'chinese': '赫辛霍夫', 'english': 'Röschenhof', 'french': 'Röschenhof', 'german': 'Röschenhof',
                          'italian': 'Röschenhof', 'japanese': 'レーシェンホーフ', 'korean': '료첸호프', 'polish': 'Röschenhof',
                          'portuguese': 'Röschenhof', 'russian': 'Решенхоф', 'spanish': 'Röschenhof',
                          'taiwanese': '赫辛霍夫'},
                   1002: {'chinese': '苟德福特', 'english': 'Goldfurt', 'french': 'Goldfurt', 'german': 'Goldfurt',
                          'italian': 'Goldfurt', 'japanese': 'ゴールドファート', 'korean': '골드푸르트', 'polish': 'Goldfurt',
                          'portuguese': 'Goldfurt', 'russian': 'Голдфурт', 'spanish': 'Goldfurt', 'taiwanese': '苟德福特'},
                   1003: {'chinese': '卡德拉岱府苟', 'english': 'Caldera De Fuego', 'french': 'Caldera De Fuego',
                          'german': 'Caldera De Fuego', 'italian': 'Caldera De Fuego', 'japanese': 'カルデラ・デ・フエゴ',
                          'korean': '카우데라 지 푸에구', 'polish': 'Caldera De Fuego', 'portuguese': 'Caldera Del Fuego',
                          'russian': 'Кальдера де Фуэго', 'spanish': 'Caldera de Fuego', 'taiwanese': '卡德拉岱府苟'},
                   1004: {'chinese': '帕拉玛林巴', 'english': 'Paramarimba', 'french': 'Paramarimba',
                          'german': 'Paramarimba', 'italian': 'Paramarimba', 'japanese': 'パラマリンバ', 'korean': '파라마림바',
                          'polish': 'Paramarimba', 'portuguese': 'Paramarimba', 'russian': 'Парамаримба',
                          'spanish': 'Paramarimba', 'taiwanese': '帕拉瑪林巴'},
                   1005: {'chinese': '贝罗维提卡', 'english': 'Belo Verticale', 'french': 'Belo Verticale',
                          'german': 'Belo Verticale', 'italian': 'Belo Verticale', 'japanese': 'ベロ・ベルティカレ',
                          'korean': '벨로베티케일', 'polish': 'Belo Verticale', 'portuguese': 'Belo Verticale',
                          'russian': 'Бэло Вертикале', 'spanish': 'Belo Verticale', 'taiwanese': '貝羅維提卡'},
                   1006: {'chinese': '萨森贝格', 'english': 'Sassenberg', 'french': 'Sassenberg', 'german': 'Sassenberg',
                          'italian': 'Sassenberg', 'japanese': 'ザッセンベルク', 'korean': '사센부르크', 'polish': 'Sassenberg',
                          'portuguese': 'Sassenberg', 'russian': 'Зассенберг', 'spanish': 'Sassenberg',
                          'taiwanese': '薩森貝格'},
                   1007: {'chinese': '圣塞巴斯蒂安', 'english': 'St. Sebastian', 'french': 'San Sebastian',
                          'german': 'St. Sebastian', 'italian': 'St. Sebastian', 'japanese': 'サン・セバスティアン',
                          'korean': '세인트 세바스찬', 'polish': 'St. Sebastian', 'portuguese': 'St. Sebastian',
                          'russian': 'Св. Себастьян', 'spanish': 'San Sebastián de los Mares', 'taiwanese': '聖塞巴斯蒂安'},
                   1008: {'chinese': '奥斯多芬', 'english': 'Osthoven', 'french': 'Osthoven', 'german': 'Osthoven',
                          'italian': 'Osthoven', 'japanese': 'オストフォーフェン', 'korean': '오스토펜', 'polish': 'Osthoven',
                          'portuguese': 'Osthoven', 'russian': 'Остхофен', 'spanish': 'Osthoven', 'taiwanese': '奧斯多芬'},
                   1009: {'chinese': '雷林根', 'english': 'Rallingen', 'french': 'Rallingen', 'german': 'Rallingen',
                          'italian': 'Rallingen', 'japanese': 'ラリンゲン', 'korean': '랄린겐', 'polish': 'Rallingen',
                          'portuguese': 'Rallingen', 'russian': 'Раллинген', 'spanish': 'Rallingen',
                          'taiwanese': '雷林根'},
                   1010: {'chinese': '美茵兹', 'english': 'Mayence', 'french': 'Mayence', 'german': 'Mayence',
                          'italian': 'Mayence', 'japanese': 'マインツ', 'korean': '메이엔스', 'polish': 'Mayence',
                          'portuguese': 'Mayence', 'russian': 'Майнц', 'spanish': 'Mayence', 'taiwanese': '美茵茲'},
                   1011: {'chinese': '查西维奇', 'english': 'Chuzzlewitch', 'french': 'Chuzzlewitch',
                          'german': 'Chuzzlewitch', 'italian': 'Chuzzlewitch', 'japanese': 'チャズルウィッチ', 'korean': '추즐위치',
                          'polish': 'Chuzzlewitch', 'portuguese': 'Chuzzlewitch', 'russian': 'Чаззлвитч',
                          'spanish': 'Chuzzlewitch', 'taiwanese': '查西維奇'},
                   1020: {'chinese': '阿尔巴托兹', 'english': 'Albatroz', 'french': 'Albatroz', 'german': 'Albatroz',
                          'italian': 'Albatroz', 'japanese': 'アルバトロス', 'korean': '알바트로즈', 'polish': 'Albatroz',
                          'portuguese': 'Albatroz', 'russian': 'Альбатрос', 'spanish': 'Albatroz',
                          'taiwanese': '阿爾巴托茲'},
                   1021: {'chinese': '汤布拉', 'english': 'Tombola', 'french': 'Tombola', 'german': 'Tombola',
                          'italian': 'Tombola', 'japanese': 'トンボラ', 'korean': '톰볼라', 'polish': 'Tombola',
                          'portuguese': 'Tombola', 'russian': 'Томбола', 'spanish': 'Tombola', 'taiwanese': '湯布拉'},
                   1022: {'chinese': '都都恩布拉库族', 'english': 'Dodo Embaraçoso', 'french': 'Dodo Embaraçoso',
                          'german': 'Dodo Embaraçoso', 'italian': 'Dodo Embaraçoso', 'japanese': 'ドド・エンバラコソ',
                          'korean': '도도 엠바라코소', 'polish': 'Dodo Embaraçoso', 'portuguese': 'Dodo Embaraçoso',
                          'russian': 'Додо Эмбарасосо', 'spanish': 'Dodo Embaraçoso', 'taiwanese': '都都恩布拉庫族'},
                   1023: {'chinese': '库帕拉府哈', 'english': 'Que Palavra', 'french': 'Que Palavra',
                          'german': 'Que Palavra', 'italian': 'Que Palavra', 'japanese': 'ケ・パラブラ', 'korean': '콰 팔라브라',
                          'polish': 'Que Palavra', 'portuguese': 'Que Palavra', 'russian': 'Ке Палавра',
                          'spanish': 'Que Palavra', 'taiwanese': '庫帕拉府哈'},
                   1024: {'chinese': '法兰达费甘特', 'english': 'Varanda Fumegante', 'french': 'Varanda Fumegante',
                          'german': 'Varanda Fumegante', 'italian': 'Varanda Fumegante', 'japanese': 'バランダ・フメガンテ',
                          'korean': '바란다 푸메간테', 'polish': 'Varanda Fumegante', 'portuguese': 'Varanda Fumegante',
                          'russian': 'Варанда Фумеганте', 'spanish': 'Varanda Fumegante', 'taiwanese': '法蘭達費甘特'},
                   1025: {'chinese': '竦比帕哈叟', 'english': 'Zumbi Paraíso', 'french': 'Zumbi Paraíso',
                          'german': 'Zumbi Paraíso', 'italian': 'Zumbi Paraíso', 'japanese': 'ズンビ・パライソ',
                          'korean': '줌비 파라이소', 'polish': 'Zumbi Paraíso', 'portuguese': 'Zumbi Paraíso',
                          'russian': 'Зумби Параисо', 'spanish': 'Zumbi Paraíso', 'taiwanese': '竦比帕哈叟'},
                   2430: {'chinese': '黎特瓦雷', 'english': 'Little Wallett', 'french': 'Little Wallett',
                          'german': 'Little Wallett', 'italian': 'Little Wallett', 'japanese': 'リトル・ウォレット',
                          'korean': '리틀 월렛', 'polish': 'Little Wallett', 'portuguese': 'Little Wallett',
                          'russian': 'Литтл Уоллет', 'spanish': 'Little Wallett', 'taiwanese': '黎特瓦雷'},
                   3477: {'chinese': '当迦芮', 'english': 'Dungaree', 'french': 'Dungaree', 'german': 'Dungaree',
                          'italian': 'Dungaree', 'japanese': 'ダンガリー', 'korean': '덩가리', 'polish': 'Dungaree',
                          'portuguese': 'Dungaree', 'russian': 'Дангари', 'spanish': 'Dungaree', 'taiwanese': '當迦芮'},
                   3478: {'chinese': '马格维奇', 'english': 'Magwich', 'french': 'Magwich', 'german': 'Magwich',
                          'italian': 'Magwich', 'japanese': 'マグウィッチ', 'korean': '매그위치', 'polish': 'Magwich',
                          'portuguese': 'Magwich', 'russian': 'Магвич', 'spanish': 'Magwich', 'taiwanese': '馬格維奇'},
                   3479: {'chinese': '郝薇香', 'english': 'Havisham', 'french': 'Havisham', 'german': 'Havisham',
                          'italian': 'Havisham', 'japanese': 'ハビシャム', 'korean': '하비샴', 'polish': 'Havisham',
                          'portuguese': 'Havisham', 'russian': 'Хэвишем', 'spanish': 'Havisham', 'taiwanese': '郝薇香'},
                   3480: {'chinese': '黎克维克', 'english': 'Lickwick', 'french': 'Lickwick', 'german': 'Lickwick',
                          'italian': 'Lickwick', 'japanese': 'リックウィック', 'korean': '릭윅', 'polish': 'Lickwick',
                          'portuguese': 'Lickwick', 'russian': 'Ликвик', 'spanish': 'Lickwick', 'taiwanese': '黎克維克'},
                   3481: {'chinese': '尼克比', 'english': 'Nickleby', 'french': 'Nickleby', 'german': 'Nickleby',
                          'italian': 'Nickleby', 'japanese': 'ニックルビー', 'korean': '니클비', 'polish': 'Nickleby',
                          'portuguese': 'Nickleby', 'russian': 'Никльби', 'spanish': 'Nickleby', 'taiwanese': '尼克比'},
                   3482: {'chinese': '柏西隋', 'english': 'Bristle', 'french': 'Bristle', 'german': 'Bristle',
                          'italian': 'Bristle', 'japanese': 'ブリストル', 'korean': '브리스틀', 'polish': 'Bristle',
                          'portuguese': 'Bristle', 'russian': 'Брисл', 'spanish': 'Bristle', 'taiwanese': '柏西隋'},
                   3483: {'chinese': '杜赫斯东', 'english': 'Droodstone', 'french': 'Droodstone', 'german': 'Droodstone',
                          'italian': 'Droodstone', 'japanese': 'ドゥルードストーン', 'korean': '드루드스톤', 'polish': 'Droodstone',
                          'portuguese': 'Droodstone', 'russian': 'Друдстоун', 'spanish': 'Droodstone',
                          'taiwanese': '杜赫斯東'},
                   3484: {'chinese': '斯加斯贝格', 'english': 'Skarsbag', 'french': 'Skarsbag', 'german': 'Skarsbag',
                          'italian': 'Skarsbag', 'japanese': 'スカースバッグ', 'korean': '스카스배그', 'polish': 'Skarsbag',
                          'portuguese': 'Skarsbag', 'russian': 'Скарсбэг', 'spanish': 'Skarsbag', 'taiwanese': '斯加斯貝格'},
                   3485: {'chinese': '诺特古平', 'english': 'Notköping', 'french': 'Notköping', 'german': 'Notköping',
                          'italian': 'Notköping', 'japanese': 'ノーショーピング', 'korean': '노코에핑', 'polish': 'Notköping',
                          'portuguese': 'Notköping', 'russian': 'Ноткепинг', 'spanish': 'Notköping',
                          'taiwanese': '諾特古平'},
                   3486: {'chinese': '赫凌比', 'english': 'Herringby', 'french': 'Herringby', 'german': 'Herringby',
                          'italian': 'Herringby', 'japanese': 'ヘリングビー', 'korean': '헤링비', 'polish': 'Herringby',
                          'portuguese': 'Herringby', 'russian': 'Херрингби', 'spanish': 'Herringby',
                          'taiwanese': '赫凌比'},
                   3487: {'chinese': '科拉斯奥德彭博', 'english': 'Coração de Pombo', 'french': 'Coração de Pombo',
                          'german': 'Coração de Pombo', 'italian': 'Coração de Pombo', 'japanese': 'コラソン・ジ・ポンボ',
                          'korean': '코라카오 데폼보', 'polish': 'Coração de Pombo', 'portuguese': 'Coração de Frango',
                          'russian': 'Корасан де Помбо', 'spanish': 'Coração de Pombo', 'taiwanese': '科拉斯奧德彭博'},
                   3488: {'chinese': '洛斯可可迪洛', 'english': 'Los Cocodrilos', 'french': 'Los Cocodrilos',
                          'german': 'Los Cocodrilos', 'italian': 'Los Cocodrilos', 'japanese': 'ロス・ココドリロス',
                          'korean': '루스 코코드릴루스', 'polish': 'Los Cocodrilos', 'portuguese': 'Peligro de Cocodrilo',
                          'russian': 'Лос Кокодрилос', 'spanish': 'Los Cocodrilos', 'taiwanese': '洛斯可可迪洛'},
                   3489: {'chinese': '阿巴亚', 'english': 'Abaja', 'french': 'Abaja', 'german': 'Abaja',
                          'italian': 'Abaja', 'japanese': 'アバヤ', 'korean': '아바야', 'polish': 'Abaja',
                          'portuguese': 'Abaja', 'russian': 'Абаха', 'spanish': 'Abaja', 'taiwanese': '阿巴亞'},
                   3490: {'chinese': '路尤兹', 'english': 'Luyuza', 'french': 'Luyuza', 'german': 'Luyuza',
                          'italian': 'Luyuza', 'japanese': 'ルユザ', 'korean': '루유자', 'polish': 'Luyuza',
                          'portuguese': 'Luyuza', 'russian': 'Луйуза', 'spanish': 'Luyuza', 'taiwanese': '路尤茲'},
                   3491: {'chinese': '帕里拉兹', 'english': 'Palraz', 'french': 'Palraz', 'german': 'Palraz',
                          'italian': 'Palraz', 'japanese': 'パルラズ', 'korean': '팔라즈', 'polish': 'Palraz',
                          'portuguese': 'Palraz', 'russian': 'Палрас', 'spanish': 'Palraz', 'taiwanese': '帕裡拉茲'},
                   3492: {'chinese': '卢卡图', 'english': 'Lucatu', 'french': 'Lucatu', 'german': 'Lucatu',
                          'italian': 'Lucatu', 'japanese': 'ルカトゥ', 'korean': '루카투', 'polish': 'Lucatu',
                          'portuguese': 'Lucatu', 'russian': 'Лукату', 'spanish': 'Lucatu', 'taiwanese': '盧卡圖'},
                   3493: {'chinese': '库里泰尔', 'english': 'Curital', 'french': 'Curital', 'german': 'Curital',
                          'italian': 'Curital', 'japanese': 'クリタル', 'korean': '쿠리탈', 'polish': 'Curital',
                          'portuguese': 'Curital', 'russian': 'Куритал', 'spanish': 'Curital', 'taiwanese': '庫裡泰爾'},
                   3494: {'chinese': '皮谷阿组', 'english': 'Piguazú', 'french': 'Piguazú', 'german': 'Piguazú',
                          'italian': 'Piguazú', 'japanese': 'ピグアズ', 'korean': '피구아주', 'polish': 'Piguazú',
                          'portuguese': 'Piguazú', 'russian': 'Пигуазу', 'spanish': 'Piguazú', 'taiwanese': '皮谷阿組'},
                   3495: {'chinese': '那拉西亚', 'english': 'Naracia', 'french': 'Naracia', 'german': 'Naracia',
                          'italian': 'Naracia', 'japanese': 'ナラシア', 'korean': '나라시아', 'polish': 'Naracia',
                          'portuguese': 'Naracia', 'russian': 'Нарасия', 'spanish': 'Naracia', 'taiwanese': '那拉西亞'},
                   3496: {'chinese': '克列亨恩', 'english': 'Querené', 'french': 'Querené', 'german': 'Querené',
                          'italian': 'Querené', 'japanese': 'クエレネ', 'korean': '퀘레네', 'polish': 'Querené',
                          'portuguese': 'Querené', 'russian': 'Керенье', 'spanish': 'Querené', 'taiwanese': '克列亨恩'},
                   3497: {'chinese': '瑟西维恶拉', 'english': 'Sechujalla', 'french': 'Sechujalla', 'german': 'Sechujalla',
                          'italian': 'Sechujalla', 'japanese': 'セチュジアラ', 'korean': '세추할라', 'polish': 'Sechujalla',
                          'portuguese': 'Sechujalla', 'russian': 'Сечухалла', 'spanish': 'Sechujalla',
                          'taiwanese': '瑟西維惡拉'},
                   6735: {'chinese': '嘎拉巴', 'english': 'Kalapää', 'french': 'Kalapää', 'german': 'Kalapää',
                          'italian': 'Kalapää', 'japanese': 'カラパー', 'korean': '칼라파야야', 'polish': 'Kalapää',
                          'portuguese': 'Kalapää', 'russian': 'Калапяа', 'spanish': 'Kalapää', 'taiwanese': '嘎拉巴'},
                   10686: {'chinese': '纳韦尔', 'english': 'Narwhal', 'french': 'Narwhal', 'german': 'Narwhal',
                           'italian': 'Narwhal', 'japanese': 'イッカク', 'korean': '나르활', 'polish': 'Narwhal',
                           'portuguese': 'Narwhal', 'russian': 'Нарвал', 'spanish': 'Narwhal', 'taiwanese': '納韋爾'},
                   10687: {'chinese': '史塔克费斯克', 'english': 'Stockfisk', 'french': 'Stockfisk', 'german': 'Stockfisk',
                           'italian': 'Stockfisk', 'japanese': 'ストックフィスク', 'korean': '스톡피스크', 'polish': 'Stockfisk',
                           'portuguese': 'Stockfisk', 'russian': 'Стокфиск', 'spanish': 'Stockfisk',
                           'taiwanese': '史塔克費斯克'},
                   10688: {'chinese': '拉科基伊', 'english': 'La Coquille', 'french': 'La Coquille',
                           'german': 'La Coquille', 'italian': 'La Coquille', 'japanese': 'ラ・コキーユ', 'korean': '라코퀼',
                           'polish': 'La Coquille', 'portuguese': 'La Coquille', 'russian': 'Ла Кокий',
                           'spanish': 'La Coquille', 'taiwanese': '拉科基伊'},
                   10689: {'chinese': '班由尼特', 'english': 'Bayonnet', 'french': 'Bayonnet', 'german': 'Bayonnet',
                           'italian': 'Bayonnet', 'japanese': 'バヨネット', 'korean': '베이오넷', 'polish': 'Bayonnet',
                           'portuguese': 'Bayonnet', 'russian': 'Байонет', 'spanish': 'Bayonnet', 'taiwanese': '班由尼特'},
                   10690: {'chinese': '康森', 'english': 'Koncerne', 'french': 'Koncerne', 'german': 'Koncerne',
                           'italian': 'Koncerne', 'japanese': 'コンセルネ', 'korean': '콘체르네', 'polish': 'Koncerne',
                           'portuguese': 'Koncerne', 'russian': 'Концерне', 'spanish': 'Koncerne', 'taiwanese': '康森'},
                   10691: {'chinese': '欧夏特', 'english': 'Altchâtel', 'french': 'Altchâtel', 'german': 'Altchâtel',
                           'italian': 'Altchâtel', 'japanese': 'アルトチャテル', 'korean': '알차텔', 'polish': 'Altchâtel',
                           'portuguese': 'Altchâtel', 'russian': 'Альтшатель', 'spanish': 'Altchâtel',
                           'taiwanese': '歐夏特'},
                   10692: {'chinese': '贝德汉诺威', 'english': 'Bad Hanover', 'french': 'Bad Hanover',
                           'german': 'Bad Hanover', 'italian': 'Bad Hanover', 'japanese': 'バート・ハノーバー',
                           'korean': '배드 하노버', 'polish': 'Bad Hanover', 'portuguese': 'Bad Hanover',
                           'russian': 'Бэд Ганновер', 'spanish': 'Bad Hanover', 'taiwanese': '貝德漢諾威'},
                   10693: {'chinese': '蒙特裴利根', 'english': 'Montpelican', 'french': 'Montpelican',
                           'german': 'Montpelican', 'italian': 'Montpelican', 'japanese': 'モントペリカン', 'korean': '몬트펠리칸',
                           'polish': 'Montpelican', 'portuguese': 'Montpelican', 'russian': 'Монтпеликан',
                           'spanish': 'Montpelican', 'taiwanese': '蒙特裴利根'},
                   10694: {'chinese': '史塔斯堡', 'english': 'Starsbourg', 'french': 'Starsbourg', 'german': 'Starsbourg',
                           'italian': 'Starsbourg', 'japanese': 'スタルスブール', 'korean': '스타스보르그', 'polish': 'Starsbourg',
                           'portuguese': 'Starsbourg', 'russian': 'Старсбург', 'spanish': 'Starsbourg',
                           'taiwanese': '史塔斯堡'},
                   10695: {'chinese': '汉玛维克', 'english': 'Hammervik', 'french': 'Hammervik', 'german': 'Hammervik',
                           'italian': 'Hammervik', 'japanese': 'ハマービック', 'korean': '함머빅', 'polish': 'Hammervik',
                           'portuguese': 'Hammervik', 'russian': 'Хаммервик', 'spanish': 'Hammervik',
                           'taiwanese': '漢瑪維克'},
                   10696: {'chinese': '葛丹', 'english': 'Gottdam', 'french': 'Gottdam', 'german': 'Gottdam',
                           'italian': 'Gottdam', 'japanese': 'ゴットダム', 'korean': '고트담', 'polish': 'Gottdam',
                           'portuguese': 'Gottdam', 'russian': 'Готтдэм', 'spanish': 'Gottdam', 'taiwanese': '葛丹'},
                   10697: {'chinese': '格罗安宁根', 'english': 'Groaningen', 'french': 'Groaningen', 'german': 'Groaningen',
                           'italian': 'Groaningen', 'japanese': 'グローニンゲン', 'korean': '그로아닌겐', 'polish': 'Groaningen',
                           'portuguese': 'Groaningen', 'russian': 'Гроанинген', 'spanish': 'Groaningen',
                           'taiwanese': '格羅安寧根'},
                   10698: {'chinese': '兹瓦兰', 'english': 'Zwollen', 'french': 'Zwollen', 'german': 'Zwollen',
                           'italian': 'Zwollen', 'japanese': 'ズウォレン', 'korean': '졸렌', 'polish': 'Zwollen',
                           'portuguese': 'Zwollen', 'russian': 'Цволлен', 'spanish': 'Zwollen', 'taiwanese': '茲瓦蘭'},
                   10699: {'chinese': '恩德霍芬', 'english': 'Rindhoven', 'french': 'Rindhoven', 'german': 'Rindhoven',
                           'italian': 'Rindhoven', 'japanese': 'リンドホーフェン', 'korean': '린드호벤', 'polish': 'Rindhoven',
                           'portuguese': 'Rindhoven', 'russian': 'Риндхофен', 'spanish': 'Rindhoven',
                           'taiwanese': '恩德霍芬'},
                   10700: {'chinese': '欧德维特', 'english': 'Oldtwerp', 'french': 'Oldtwerp', 'german': 'Oldtwerp',
                           'italian': 'Oldtwerp', 'japanese': 'オールドワープ', 'korean': '올드워프', 'polish': 'Oldtwerp',
                           'portuguese': 'Oldtwerp', 'russian': 'Олдтверпен', 'spanish': 'Oldtwerp',
                           'taiwanese': '歐德維特'},
                   10701: {'chinese': '玛诺堡恩', 'english': 'Manorborn', 'french': 'Manorborn', 'german': 'Manorborn',
                           'italian': 'Manorborn', 'japanese': 'メイナーボーン', 'korean': '마노르본', 'polish': 'Manorborn',
                           'portuguese': 'Manorborn', 'russian': 'Манорборн', 'spanish': 'Manorborn',
                           'taiwanese': '瑪諾堡恩'},
                   10702: {'chinese': '弗雷姆斯堡', 'english': 'Phlegmsburg', 'french': 'Phlegmsburg',
                           'german': 'Phlegmsburg', 'italian': 'Phlegmsburg', 'japanese': 'フレムズバーグ', 'korean': '플렘스부르크',
                           'polish': 'Phlegmsburg', 'portuguese': 'Phlegmsburg', 'russian': 'Флегмсбург',
                           'spanish': 'Phlegmsburg', 'taiwanese': '弗雷姆斯堡'},
                   10703: {'chinese': '格雷特沃德', 'english': 'Gretelwald', 'french': 'Gretelwald', 'german': 'Gretelwald',
                           'italian': 'Gretelwald', 'japanese': 'グリートウォルド', 'korean': '그레테왈트', 'polish': 'Gretelwald',
                           'portuguese': 'Gretelwald', 'russian': 'Гретельвальд', 'spanish': 'Gretelwald',
                           'taiwanese': '格雷特沃德'},
                   10704: {'chinese': '威利夫黑曲', 'english': 'Villefraîche', 'french': 'Villefraîche',
                           'german': 'Villefraîche', 'italian': 'Villefraîche', 'japanese': 'ヴィルフレッシュ',
                           'korean': '빌프레슈', 'polish': 'Villefraîche', 'portuguese': 'Villefraîche du Crème',
                           'russian': 'Вильфреш', 'spanish': 'Villefraîche', 'taiwanese': '威利夫黑曲'},
                   10705: {'chinese': '斯必泰佛特', 'english': 'Spittalfurt', 'french': 'Spittalfurt',
                           'german': 'Spittalfurt', 'italian': 'Spittalfurt', 'japanese': 'スピッタルフルト',
                           'korean': '스피탈푸르트', 'polish': 'Spittalfurt', 'portuguese': 'Spittalfurt',
                           'russian': 'Шпиттальфурт', 'spanish': 'Spittalfurt', 'taiwanese': '斯必泰佛特'},
                   10706: {'chinese': '巴特萨尔茨', 'english': 'Bad Salz', 'french': 'Bad Salz', 'german': 'Bad Salz',
                           'italian': 'Bad Salz', 'japanese': 'バート・ザルツ', 'korean': '배드 살즈', 'polish': 'Bad Salz',
                           'portuguese': 'Bad Salz', 'russian': 'Бэд Зальц', 'spanish': 'Bad Salz',
                           'taiwanese': '巴特薩爾茨'},
                   10707: {'chinese': '马德里盖尔', 'english': 'Madrigal', 'french': 'Madrigal', 'german': 'Madrigal',
                           'italian': 'Madrigal', 'japanese': 'マドリガル', 'korean': '마드리갈', 'polish': 'Madrigal',
                           'portuguese': 'Madrigal', 'russian': 'Мадригал', 'spanish': 'Madrigal',
                           'taiwanese': '馬德里蓋爾'},
                   10708: {'chinese': '席本布鲁肯', 'english': 'Siebenbrücken', 'french': 'Siebenbrücken',
                           'german': 'Siebenbrücken', 'italian': 'Siebenbrücken', 'japanese': 'ジーベンブルッケン',
                           'korean': '지벤브럭켄', 'polish': 'Siebenbrücken', 'portuguese': 'Siebenbrücken',
                           'russian': 'Зибенбрюкен', 'spanish': 'Siebenbrücken', 'taiwanese': '席本布魯肯'},
                   10709: {'chinese': '欧特文', 'english': 'Altwin', 'french': 'Altwin', 'german': 'Altwin',
                           'italian': 'Altwin', 'japanese': 'アルトウィン', 'korean': '알트윈', 'polish': 'Altwin',
                           'portuguese': 'Altwin', 'russian': 'Альтвин', 'spanish': 'Altwin', 'taiwanese': '歐特文'},
                   10710: {'chinese': '费什加德', 'english': 'Fishguard', 'french': 'Fishguard', 'german': 'Fishguard',
                           'italian': 'Fishguard', 'japanese': 'フィッシュガード', 'korean': '피시가드', 'polish': 'Fishguard',
                           'portuguese': 'Fishguard', 'russian': 'Фишгард', 'spanish': 'Fishguard',
                           'taiwanese': '費什加德'},
                   10711: {'chinese': '哈普尔', 'english': 'Heartpool', 'french': 'Heartpool', 'german': 'Heartpool',
                           'italian': 'Heartpool', 'japanese': 'ハートプール', 'korean': '하트풀', 'polish': 'Heartpool',
                           'portuguese': 'Heartpool', 'russian': 'Хартпул', 'spanish': 'Heartpool', 'taiwanese': '哈普爾'},
                   10712: {'chinese': '艾根德罕', 'english': 'Eggandham', 'french': 'Eggandham', 'german': 'Eggandham',
                           'italian': 'Eggandham', 'japanese': 'エガンドハム', 'korean': '에간담', 'polish': 'Eggandham',
                           'portuguese': 'Eggandham', 'russian': 'Эггэндхэм', 'spanish': 'Eggandham',
                           'taiwanese': '艾根德罕'},
                   10713: {'chinese': '肯佛德', 'english': 'Camford', 'french': 'Camford', 'german': 'Camford',
                           'italian': 'Camford', 'japanese': 'カムフォード', 'korean': '캠포드', 'polish': 'Camford',
                           'portuguese': 'Camford', 'russian': 'Кэмфорд', 'spanish': 'Camford', 'taiwanese': '肯佛德'},
                   10714: {'chinese': '斯瓦恩比', 'english': 'Swanbeak', 'french': 'Swanbeak', 'german': 'Swanbeak',
                           'italian': 'Swanbeak', 'japanese': 'スワンビーク', 'korean': '스완비크', 'polish': 'Swanbeak',
                           'portuguese': 'Swanbeak', 'russian': 'Суонбик', 'spanish': 'Swanbeak', 'taiwanese': '斯瓦恩比'},
                   12018: {'chinese': '亮沙岛', 'english': 'Bright Sands', 'french': 'Bright Sands',
                           'german': 'Bright Sands', 'italian': 'Bright Sands', 'japanese': 'ブライトサンズ',
                           'korean': '브라이트 샌즈', 'polish': 'Bright Sands', 'portuguese': 'Bright Sands',
                           'russian': 'Золотые пески', 'spanish': 'Arena Brillante', 'taiwanese': '亮沙島'},
                   12019: {'chinese': '繁荣岛', 'english': 'Prosperity', 'french': 'Prosperity', 'german': 'Prosperity',
                           'italian': 'Prosperity', 'japanese': 'プロスペリティ', 'korean': '프로스퍼리티', 'polish': 'Profuzja',
                           'portuguese': 'Prosperity', 'russian': 'Просперити', 'spanish': 'Prosperidad',
                           'taiwanese': '繁榮島'},
                   12231: {'chinese': '沟中死水岛', 'english': 'Ditchwater', 'french': 'Ditchwater', 'german': 'Ditchwater',
                           'italian': 'Ditchwater', 'japanese': 'ディッチウォーター', 'korean': '디치워터', 'polish': 'Ditchwater',
                           'portuguese': 'Ditchwater', 'russian': 'Хлябь', 'spanish': 'La Inapetente',
                           'taiwanese': '溝中死水島'},
                   13665: {'chinese': '那座岛', 'english': 'La Isla', 'french': 'La Isla', 'german': 'La Isla',
                           'italian': 'La Isla', 'japanese': 'ラ・イスラ', 'korean': '라 이슬라', 'polish': 'La Isla',
                           'portuguese': 'La Isla', 'russian': 'Ла Исла', 'spanish': 'La Isla', 'taiwanese': '那座島'},
                   16137: {'chinese': '海克伦斯霍', 'english': 'High Clarence Hall', 'french': 'High Clarence Hall',
                           'german': 'High Clarence Hall', 'italian': 'High Clarence Hall', 'japanese': 'ハイクラレンスホール',
                           'korean': '하이 클래런스 홀', 'polish': 'High Clarence Hall', 'portuguese': 'High Clarence Hall',
                           'russian': 'Хай-Кларенс-Холл', 'spanish': 'High Clarence Hall', 'taiwanese': '海克倫斯霍'},
                   16138: {'chinese': '握姆威监狱', 'english': 'Wormways Prison', 'french': 'Prison de Wormways',
                           'german': 'Wormways Prison', 'italian': 'Wormways Prison', 'japanese': 'ワームウェイズ刑務所',
                           'korean': '웜웨이즈 교도소', 'polish': 'Wormways Prison', 'portuguese': 'Wormways Prison',
                           'russian': 'Тюрьма Вормвейз', 'spanish': 'Prisión Wormways', 'taiwanese': '握姆威監獄'},
                   16140: {'chinese': '高山岛', 'english': 'High Mountain', 'french': 'High Mountain',
                           'german': 'High Mountain', 'italian': 'High Mountain', 'japanese': 'ハイ・マウンテン',
                           'korean': '하이 마운틴', 'polish': 'High Mountain', 'portuguese': 'High Mountain',
                           'russian': 'Хай-Маунтин', 'spanish': 'High Mountain', 'taiwanese': '高山島'},
                   16141: {'chinese': '异域风情岛', 'english': 'Emporium Exotique', 'french': 'Bazar exotique',
                           'german': 'Emporium Exotique', 'italian': 'Emporium Exotique', 'japanese': 'エンポリウム・エグゾティーク',
                           'korean': '엠포리엄 엑조틱', 'polish': 'Emporium Exotique', 'portuguese': 'Emporium Exotique',
                           'russian': 'Эмпориум Экзотик', 'spanish': 'Emporio Exótico', 'taiwanese': '異域風情島'},
                   16143: {'chinese': '艾尔普多岛', 'english': 'El Puerto', 'french': 'El Puerto', 'german': 'El Puerto',
                           'italian': 'El Puerto', 'japanese': 'エル・プエルト', 'korean': '엘 푸에르토', 'polish': 'El Puerto',
                           'portuguese': 'El Puerto', 'russian': 'Эль-Пуэрто', 'spanish': 'El Puerto',
                           'taiwanese': '艾爾普多島'},
                   17663: {'chinese': '卡希曲拉岛', 'english': 'Casuchilla', 'french': 'Casuchilla', 'german': 'Casuchilla',
                           'italian': 'Casuchilla', 'japanese': 'カスチーリャ', 'korean': '카슈칠라', 'polish': 'Casuchilla',
                           'russian': 'Касуча', 'spanish': 'Casuchilla', 'taiwanese': '卡希曲拉島'},
                   20117: {'chinese': '诺顿湾', 'english': 'Norton Bay', 'french': 'Baie de Norton',
                           'german': 'Norton Bay', 'italian': 'Norton Bay', 'japanese': 'ノートンベイ', 'korean': '노튼 베이',
                           'polish': 'Zatoka Nortona', 'russian': 'Нортон Бэй', 'spanish': 'Norton Bay',
                           'taiwanese': '諾頓灣'},
                   20118: {'chinese': '德登布里', 'english': 'Deddenbury', 'french': 'Deddenbury', 'german': 'Deddenbury',
                           'italian': 'Deddenbury', 'japanese': 'デドンベリー', 'korean': '디던버리', 'polish': 'Deddenbury',
                           'russian': 'Дедденбери', 'spanish': 'Deddenbury', 'taiwanese': '德登布里'},
                   20119: {'chinese': '德克桥', 'english': 'Dirkbridge', 'french': 'Dirkbridge', 'german': 'Dirkbridge',
                           'italian': 'Dirkbridge', 'japanese': 'ダークブリッジ', 'korean': '더크브리지', 'polish': 'Dirkbridge',
                           'russian': 'Деркбридж', 'spanish': 'Dirkbridge', 'taiwanese': '德克橋'},
                   20120: {'chinese': '肯泽林敦', 'english': 'Kenslington', 'french': 'Kenzlington',
                           'german': 'Kenzlington', 'italian': 'Kenzlington', 'japanese': 'ケンズリントン', 'korean': '켄즐링턴',
                           'polish': 'Kenzlington', 'russian': 'Кензлингтон', 'spanish': 'Kenzlington',
                           'taiwanese': '肯澤林敦'},
                   20121: {'chinese': '高德克林', 'english': 'Haute du Crème', 'french': 'Bourg-de-Crème',
                           'german': 'Haute du Crème', 'italian': 'Haute du Crème', 'japanese': 'オート・デュ・クレーム',
                           'korean': '오뜨두크레메', 'polish': 'Haute du Crème', 'russian': 'От Дю Крем',
                           'spanish': 'Haute du Crème', 'taiwanese': '高德克林'},
                   20122: {'chinese': '拉斯普布里', 'english': 'Raspbury', 'french': 'Raspbury', 'german': 'Raspbury',
                           'italian': 'Raspbury', 'japanese': 'ラズベリー', 'korean': '라즈버리', 'polish': 'Raspbury',
                           'russian': 'Распбери', 'spanish': 'Raspbury', 'taiwanese': '拉斯普布里'},
                   20123: {'chinese': '汉柏兰居', 'english': 'Hanberrenge', 'french': 'Hanberrenge',
                           'german': 'Hanberrenge', 'italian': 'Hanberrenge', 'japanese': 'ハンバーレンジ', 'korean': '한베레잉게',
                           'polish': 'Hanberrenge', 'russian': 'Хэнберрендж', 'spanish': 'Hanberrenge',
                           'taiwanese': '漢柏蘭居'},
                   20124: {'chinese': '诺兹桥', 'english': 'Nozbridge', 'french': 'Nozbridge', 'german': 'Nozbridge',
                           'italian': 'Nozbridge', 'japanese': 'ノズブリッジ', 'korean': '노즈브리지', 'polish': 'Nozbridge',
                           'russian': 'Нозбридж', 'spanish': 'Nozbridge', 'taiwanese': '諾茲橋'},
                   20125: {'chinese': '斯坎米德霍夫', 'english': 'Schmiedelhoof', 'french': 'Schmiedelhoof',
                           'german': 'Schmiedelhoof', 'italian': 'Schmiedelhoof', 'japanese': 'シュミーデルフーフ',
                           'korean': '스미델호프', 'polish': 'Schmiedelhoof', 'russian': 'Шмидельхоф',
                           'spanish': 'Schmiedelhoof', 'taiwanese': '斯坎米德霍夫'},
                   20126: {'chinese': '劳森堡', 'english': 'Lautssenberg', 'french': 'Lautssenberg',
                           'german': 'Lautssenberg', 'italian': 'Lautssenberg', 'japanese': 'ローテセンベルク',
                           'korean': '라우트센베르크', 'polish': 'Lautssenberg', 'russian': 'Лаутссенберг',
                           'spanish': 'Lautssenberg', 'taiwanese': '勞森堡'},
                   20127: {'chinese': '布黎泽维奇', 'english': 'Brizzlewich', 'french': 'Brizzlewich',
                           'german': 'Brizzlewich', 'italian': 'Brizzlewich', 'japanese': 'ブリズルウィク', 'korean': '브리즐위치',
                           'polish': 'Brizzlewich', 'russian': 'Бриззлвич', 'spanish': 'Brizzlewich',
                           'taiwanese': '布黎澤維奇'},
                   20128: {'chinese': '摩内托伊斯', 'english': 'Monetoise', 'french': 'Monetoise', 'german': 'Monetoise',
                           'italian': 'Monetoise', 'japanese': 'モントワーズ', 'korean': '모네토아스', 'polish': 'Monetoise',
                           'russian': 'Монетуаз', 'spanish': 'Monetoise', 'taiwanese': '摩內托伊斯'},
                   20130: {'chinese': '雅内萨克斯', 'english': 'Jennesaux', 'french': 'Jennesaux', 'german': 'Jennesaux',
                           'italian': 'Jennesaux', 'japanese': 'ジェンソー', 'korean': '젠느소', 'polish': 'Jennesaux',
                           'russian': 'Жаннесо', 'spanish': 'Jennesaux', 'taiwanese': '雅內薩克斯'},
                   20131: {'chinese': '北哈拚', 'english': 'North Haping', 'french': 'Northhaping',
                           'german': 'Northhaping', 'italian': 'Northhaping', 'japanese': 'ノーザッピン', 'korean': '노스하핑',
                           'polish': 'Northhaping', 'russian': 'Нордхэйпинг', 'spanish': 'Northhaping',
                           'taiwanese': '北哈拚'},
                   20132: {'chinese': '维尔维格', 'english': 'Weilweg', 'french': 'Weilweg', 'german': 'Weilweg',
                           'italian': 'Weilweg', 'japanese': 'ヴァイルヴェーク', 'korean': '바일베크', 'polish': 'Weilweg',
                           'russian': 'Вайльвег', 'spanish': 'Weilweg', 'taiwanese': '維爾維格'},
                   20133: {'chinese': '希普拉斯', 'english': 'Hiprath', 'french': 'Hiprath', 'german': 'Hiprath',
                           'italian': 'Hiprath', 'japanese': 'ヒプラス', 'korean': '히프라스', 'polish': 'Hiprath',
                           'russian': 'Хипрат', 'spanish': 'Hiprath', 'taiwanese': '希普拉斯'},
                   20134: {'chinese': '德芙维兰', 'english': 'Derfvelen', 'french': 'Derfvelen', 'german': 'Derfvelen',
                           'italian': 'Derfvelen', 'japanese': 'ダーフヴェレン', 'korean': '더프벨렌', 'polish': 'Derfvelen',
                           'russian': 'Дерфвелен', 'spanish': 'Derfvelen', 'taiwanese': '德芙維蘭'},
                   20135: {'chinese': '波尔波伊斯', 'english': 'Porpoise', 'french': 'Porpoise', 'german': 'Porpoise',
                           'italian': 'Porpoise', 'japanese': 'ポーポイエス', 'korean': '포르푸아즈', 'polish': 'Porpoise',
                           'russian': 'Порпуаз', 'spanish': 'Porpoise', 'taiwanese': '波爾波伊斯'},
                   20136: {'chinese': '罗森塔德', 'english': 'Rosenstad', 'french': 'Rosenstad', 'german': 'Rosenstad',
                           'italian': 'Rosenstad', 'japanese': 'ローゼンシュタット', 'korean': '로센스테드', 'polish': 'Rosenstad',
                           'russian': 'Розенштад', 'spanish': 'Rosenstad', 'taiwanese': '羅森塔德'},
                   20137: {'chinese': '柯洛索瓦', 'english': 'Korozova', 'french': 'Korozova', 'german': 'Korozova',
                           'italian': 'Korozova', 'japanese': 'コローゾワ', 'korean': '코로조바', 'polish': 'Korozova',
                           'russian': 'Корозова', 'spanish': 'Korozova', 'taiwanese': '柯洛索瓦'},
                   20138: {'chinese': '杰格斯柏', 'english': 'Dragsborg', 'french': 'Dragsborg', 'german': 'Dragsborg',
                           'italian': 'Dragsborg', 'japanese': 'ドラグスボルグ', 'korean': '드락스보르그', 'polish': 'Dragsborg',
                           'russian': 'Драгсборг', 'spanish': 'Dragsborg', 'taiwanese': '傑格斯柏'},
                   20139: {'chinese': '阿拉席诺', 'english': 'Arraceno', 'french': 'Arraceno', 'german': 'Arraceno',
                           'italian': 'Arraceno', 'japanese': 'アラセン', 'korean': '아라세노', 'polish': 'Arraceno',
                           'russian': 'Аррасено', 'spanish': 'Arraceno', 'taiwanese': '阿拉席諾'},
                   20140: {'chinese': '席鲁斯米亚', 'english': 'Silusmia', 'french': 'Silusmia', 'german': 'Silusmia',
                           'italian': 'Silusmia', 'japanese': 'シラスミア', 'korean': '실루스미아', 'polish': 'Silusmia',
                           'russian': 'Силусмия', 'spanish': 'Silusmia', 'taiwanese': '席魯斯米亞'},
                   20141: {'chinese': '毕撒波瓦', 'english': 'Bisaboa', 'french': 'Bisaboa', 'german': 'Bisaboa',
                           'italian': 'Bisaboa', 'japanese': 'ビサボア', 'korean': '비사보아', 'polish': 'Bisaboa',
                           'russian': 'Бисабоа', 'spanish': 'Bisaboa', 'taiwanese': '畢撒波瓦'},
                   20142: {'chinese': '拉玛琳', 'english': 'La Marine', 'french': 'La Marine', 'german': 'La Marine',
                           'italian': 'La Marine', 'japanese': 'ラ・マリン', 'korean': '라 마린느', 'polish': 'La Marine',
                           'russian': 'Ля Марин', 'spanish': 'La Marina', 'taiwanese': '拉瑪琳'},
                   20143: {'chinese': '哈地夫', 'english': 'Hardiff', 'french': 'Hardiff', 'german': 'Hardiff',
                           'italian': 'Hardiff', 'japanese': 'ハーディフ', 'korean': '하디프', 'polish': 'Hardiff',
                           'russian': 'Хардифф', 'spanish': 'Hardiff', 'taiwanese': '哈地夫'},
                   20144: {'chinese': '东嘴', 'english': 'Eastmouth', 'french': 'Eastmouth', 'german': 'Eastmouth',
                           'italian': 'Eastmouth', 'japanese': 'イーストマウス', 'korean': '이스트마우스', 'polish': 'Eastmouth',
                           'russian': 'Истмаут', 'spanish': 'Eastmouth', 'taiwanese': '東嘴'},
                   20145: {'chinese': '敦约克', 'english': 'Dunyorke', 'french': 'Dunyorke', 'german': 'Dunyorke',
                           'italian': 'Dunyorke', 'japanese': 'ダンヨーク', 'korean': '더뇨크', 'polish': 'Dunyorke',
                           'russian': 'Данйорк', 'spanish': 'Dunyorke', 'taiwanese': '敦約克'},
                   20146: {'chinese': '塞芬顿', 'english': 'Siphington', 'french': 'Siphington', 'german': 'Siphington',
                           'italian': 'Siphington', 'japanese': 'シフィントン', 'korean': '시핑턴', 'polish': 'Siphington',
                           'russian': 'Сифингтон', 'spanish': 'Siphington', 'taiwanese': '塞芬頓'},
                   20147: {'chinese': '纽巴妥', 'english': 'Nubottle', 'french': 'Nubottle', 'german': 'Nubottle',
                           'italian': 'Nubottle', 'japanese': 'ヌーボトル', 'korean': '누보틀', 'polish': 'Nubottle',
                           'russian': 'Ньюботтл', 'spanish': 'Nubottle', 'taiwanese': '紐巴妥'},
                   20148: {'chinese': '克里普福特', 'english': 'Klipfford', 'french': 'Klipfford', 'german': 'Klipfford',
                           'italian': 'Klipfford', 'japanese': 'クリップフォード', 'korean': '클립포드', 'polish': 'Klipfford',
                           'russian': 'Клипффорд', 'spanish': 'Klipfford', 'taiwanese': '克里普福特'},
                   20149: {'chinese': '老僧院', 'english': 'Old Abbey', 'french': 'Old Abbey', 'german': 'Old Abbey',
                           'italian': 'Old Abbey', 'japanese': 'オールド・アビー', 'korean': '올드 애베이', 'polish': 'Old Abbey',
                           'russian': 'Олд Эбби', 'spanish': 'Old Abbey', 'taiwanese': '老僧院'},
                   20150: {'chinese': '甜美会堂', 'english': 'Sweethall', 'french': 'Sweethall', 'german': 'Sweethall',
                           'italian': 'Sweethall', 'japanese': 'スウィートホール', 'korean': '스위트홀', 'polish': 'Sweethall',
                           'russian': 'Свитхолл', 'spanish': 'Sweethall', 'taiwanese': '甜美會堂'},
                   20151: {'chinese': '希尔蒙特', 'english': 'Hillmont', 'french': 'Hillmont', 'german': 'Hillmont',
                           'italian': 'Hillmont', 'japanese': 'ヒルモント', 'korean': '힐몬트', 'polish': 'Hillmont',
                           'russian': 'Хиллмонт', 'spanish': 'Hillmont', 'taiwanese': '希爾蒙特'},
                   20152: {'chinese': '卡特霍姆', 'english': 'Cartholme', 'french': 'Cartholme', 'german': 'Cartholme',
                           'italian': 'Cartholme', 'japanese': 'カーソーム', 'korean': '카스홈', 'polish': 'Cartholme',
                           'russian': 'Картхолм', 'spanish': 'Cartholme', 'taiwanese': '卡特霍姆'},
                   20153: {'chinese': '布莱曲顿', 'english': 'Brachton', 'french': 'Brachton', 'german': 'Brachton',
                           'italian': 'Brachton', 'japanese': 'ブラクトン', 'korean': '브래치튼', 'polish': 'Brachton',
                           'russian': 'Брэчтон', 'spanish': 'Brachton', 'taiwanese': '布萊曲頓'},
                   20154: {'chinese': '布朗威尔', 'english': 'Brownwell', 'french': 'Brownwell', 'german': 'Brownwell',
                           'italian': 'Brownwell', 'japanese': 'ブラウンウェル', 'korean': '브라운웰', 'polish': 'Brownwell',
                           'russian': 'Браунвелл', 'spanish': 'Brownwell', 'taiwanese': '布朗威爾'},
                   20155: {'chinese': '史堤普顿', 'english': 'Steepton', 'french': 'Steepton', 'german': 'Steepton',
                           'italian': 'Steepton', 'japanese': 'スティープトン', 'korean': '스팁튼', 'polish': 'Steepton',
                           'russian': 'Стиптон', 'spanish': 'Steepton', 'taiwanese': '史堤普頓'},
                   20156: {'chinese': '佛莱利', 'english': 'Fleighley', 'french': 'Fleighley', 'german': 'Fleighley',
                           'italian': 'Fleighley', 'japanese': 'フライクレイ', 'korean': '프렐리', 'polish': 'Fleighley',
                           'russian': 'Флейли', 'spanish': 'Fleighley', 'taiwanese': '佛萊利'},
                   20157: {'chinese': '敦斯波顿', 'english': 'Dunsbottom', 'french': 'Dunsbottom', 'german': 'Dunsbottom',
                           'italian': 'Dunsbottom', 'japanese': 'ダンスボトム', 'korean': '던스바텀', 'polish': 'Dunsbottom',
                           'russian': 'Дансботтом', 'spanish': 'Dunsbottom', 'taiwanese': '敦斯波頓'},
                   20158: {'chinese': '上丘', 'english': 'Upperhill', 'french': 'Upperhill', 'german': 'Upperhill',
                           'italian': 'Upperhill', 'japanese': 'アッパーヒル', 'korean': '어퍼힐', 'polish': 'Upperhill',
                           'russian': 'Апперхилл', 'spanish': 'Upperhill', 'taiwanese': '上丘'},
                   20159: {'chinese': '贝赫', 'english': 'Beigh', 'french': 'Beigh', 'german': 'Beigh',
                           'italian': 'Beigh', 'japanese': 'ベーク', 'korean': '베이', 'polish': 'Beigh', 'russian': 'Бей',
                           'spanish': 'Beigh', 'taiwanese': '貝赫'},
                   20160: {'chinese': '库克科恩', 'english': 'Cookcorn', 'french': 'Cookcorn', 'german': 'Cookcorn',
                           'italian': 'Cookcorn', 'japanese': 'クックコーン', 'korean': '쿡콘', 'polish': 'Cookcorn',
                           'russian': 'Куккорн', 'spanish': 'Cookcorn', 'taiwanese': '庫克科恩'},
                   20161: {'chinese': '品波特', 'english': 'Pingport', 'french': 'Pingport', 'german': 'Pingport',
                           'italian': 'Pingport', 'japanese': 'ピンポート', 'korean': '핑포트', 'polish': 'Pingport',
                           'russian': 'Пингпорт', 'spanish': 'Pingport', 'taiwanese': '品波特'},
                   20162: {'chinese': '波利', 'english': 'Porley', 'french': 'Porley', 'german': 'Porley',
                           'italian': 'Porley', 'japanese': 'ポーリー', 'korean': '폴레이', 'polish': 'Porley',
                           'russian': 'Порли', 'spanish': 'Porley', 'taiwanese': '波利'},
                   20163: {'chinese': '罗斯科夫', 'english': 'Rosscoff', 'french': 'Rosscoff', 'german': 'Rosscoff',
                           'italian': 'Rosscoff', 'japanese': 'ロスコフ', 'korean': '로스코프', 'polish': 'Rosscoff',
                           'russian': 'Росскофф', 'spanish': 'Rosscoff', 'taiwanese': '羅斯科夫'},
                   20164: {'chinese': '威尔沃', 'english': 'Willwough', 'french': 'Willwough', 'german': 'Willwough',
                           'italian': 'Willwough', 'japanese': 'ウィルウォー', 'korean': '윌와우', 'polish': 'Willwough',
                           'russian': 'Уилвоу', 'spanish': 'Willwough', 'taiwanese': '威爾沃'},
                   20165: {'chinese': '威斯顿', 'english': 'Westton', 'french': 'Westton', 'german': 'Westton',
                           'italian': 'Westton', 'japanese': 'ウェストン', 'korean': '웨스턴', 'polish': 'Westton',
                           'russian': 'Уэсттон', 'spanish': 'Westton', 'taiwanese': '威斯頓'},
                   20166: {'chinese': '南布里', 'english': 'Nanbury', 'french': 'Nanbury', 'german': 'Nanbury',
                           'italian': 'Nanbury', 'japanese': 'ナンベリー', 'korean': '낸버리', 'polish': 'Nanbury',
                           'russian': 'Нэнбери', 'spanish': 'Nanbury', 'taiwanese': '南布里'},
                   20168: {'chinese': '布雷人物特', 'english': 'Bretcaster', 'french': 'Bretcaster', 'german': 'Bretcaster',
                           'italian': 'Bretcaster', 'japanese': 'ブレットキャスター', 'korean': '브레트캐스터', 'polish': 'Bretcaster',
                           'russian': 'Бреткaстер', 'spanish': 'Bretcaster', 'taiwanese': '布雷卡司特'},
                   20169: {'chinese': '毕塞德', 'english': 'Beeside', 'french': 'Beeside', 'german': 'Beeside',
                           'italian': 'Beeside', 'japanese': 'ビーサイド', 'korean': '비사이드', 'polish': 'Beeside',
                           'russian': 'Бисайд', 'spanish': 'Beeside', 'taiwanese': '畢塞德'},
                   20170: {'chinese': '山德兰姆', 'english': 'Sandlem', 'french': 'Sandlem', 'german': 'Sandlem',
                           'italian': 'Sandlem', 'japanese': 'サンドレム', 'korean': '샌들렘', 'polish': 'Sandlem',
                           'russian': 'Сэндлем', 'spanish': 'Sandlem', 'taiwanese': '山德蘭姆'},
                   20171: {'chinese': '塔波巴克', 'english': 'Tarporbach', 'french': 'Tarporbach', 'german': 'Tarporbach',
                           'italian': 'Tarporbach', 'japanese': 'ターパーバッチ', 'korean': '타포바크', 'polish': 'Tarporbach',
                           'russian': 'Тарпорбах', 'spanish': 'Tarporbach', 'taiwanese': '塔波巴克'},
                   20172: {'chinese': '尹兰地尔诺', 'english': 'Yvlandyrnog', 'french': 'Yvlandyrnog',
                           'german': 'Yvlandyrnog', 'italian': 'Yvlandyrnog', 'japanese': 'イヴランダーニグ',
                           'korean': '어블란더르노그', 'polish': 'Yvlandyrnog', 'russian': 'Ивландюрног',
                           'spanish': 'Yvlandyrnog', 'taiwanese': '尹蘭地爾諾'},
                   20173: {'chinese': '古莱契尔', 'english': 'Grychurch', 'french': 'Grychurch', 'german': 'Grychurch',
                           'italian': 'Grychurch', 'japanese': 'グリチャーチ', 'korean': '그러히르흐', 'polish': 'Grychurch',
                           'russian': 'Грайчерч', 'spanish': 'Grychurch', 'taiwanese': '古萊契爾'},
                   20174: {'chinese': '芙兰利博恩', 'english': 'Framlichbourn', 'french': 'Framlichbourn',
                           'german': 'Framlichbourn', 'italian': 'Framlichbourn', 'japanese': 'フラムリッヒボルン',
                           'korean': '프람리치본', 'polish': 'Framlichbourn', 'russian': 'Фрамлихбоурн',
                           'spanish': 'Framlichbourn', 'taiwanese': '芙蘭利博恩'},
                   20175: {'chinese': '克特斯特', 'english': 'Kettester', 'french': 'Kettester', 'german': 'Kettester',
                           'italian': 'Kettester', 'japanese': 'ケッテスター', 'korean': '케테스터', 'polish': 'Kettester',
                           'russian': 'Кеттестер', 'spanish': 'Kettester', 'taiwanese': '克特斯特'},
                   20176: {'chinese': '巴格斯布里', 'english': 'Bugsbly', 'french': 'Bugsbly', 'german': 'Bugsbly',
                           'italian': 'Bugsbly', 'japanese': 'バグズブリー', 'korean': '벅스블리', 'polish': 'Bugsbly',
                           'russian': 'Багсбли', 'spanish': 'Bugsbly', 'taiwanese': '巴格斯布里'},
                   20177: {'chinese': '伊布斯毕契', 'english': 'Ipsbeach', 'french': 'Ipsbeach', 'german': 'Ipsbeach',
                           'italian': 'Ipsbeach', 'japanese': 'イプスビーチ', 'korean': '입스비치', 'polish': 'Ipsbeach',
                           'russian': 'Ипсбич', 'spanish': 'Ipsbeach', 'taiwanese': '伊布斯畢契'},
                   20178: {'chinese': '雷克多维', 'english': 'Lechtowe', 'french': 'Lechtowe', 'german': 'Lechtowe',
                           'italian': 'Lechtowe', 'japanese': 'レヒトヴェ', 'korean': '레크토', 'polish': 'Lechtowe',
                           'russian': 'Лехтове', 'spanish': 'Lechtowe', 'taiwanese': '雷克多維'},
                   20179: {'chinese': '玛尔穆尔', 'english': 'Marmoor', 'french': 'Marmoor', 'german': 'Marmoor',
                           'italian': 'Marmoor', 'japanese': 'マームーア', 'korean': '마무어', 'polish': 'Marmoor',
                           'russian': 'Мармор', 'spanish': 'Marmoor', 'taiwanese': '瑪爾穆爾'},
                   20180: {'chinese': '平镇', 'english': 'Peanzen', 'french': 'Peanzen', 'german': 'Peanzen',
                           'italian': 'Peanzen', 'japanese': 'ピーンゼン', 'korean': '핀전', 'polish': 'Peanzen',
                           'russian': 'Пеанцен', 'spanish': 'Peanzen', 'taiwanese': '平鎮'},
                   20181: {'chinese': '长石', 'english': 'Longrock', 'french': 'Longrock', 'german': 'Longrock',
                           'italian': 'Longrock', 'japanese': 'ロングロック', 'korean': '롱록', 'polish': 'Longrock',
                           'russian': 'Лонгрок', 'spanish': 'Longrock', 'taiwanese': '長石'},
                   20182: {'chinese': '失落磨坊', 'english': 'Lostmill', 'french': 'Lostmill', 'german': 'Lostmill',
                           'italian': 'Lostmill', 'japanese': 'ロストミル', 'korean': '로스트밀', 'polish': 'Lostmill',
                           'russian': 'Лостмилл', 'spanish': 'Lostmill', 'taiwanese': '失落磨坊'},
                   20183: {'chinese': '黑森夫特', 'english': 'Hessenfoot', 'french': 'Hessenfoot', 'german': 'Hessenfoot',
                           'italian': 'Hessenfoot', 'japanese': 'ヘッセンフット', 'korean': '헤센포오트', 'polish': 'Hessenfoot',
                           'russian': 'Хессенфут', 'spanish': 'Hessenfoot', 'taiwanese': '黑森夫特'},
                   20184: {'chinese': '茅斯穆尔', 'english': 'Mousemoor', 'french': 'Mousemoor', 'german': 'Mousemoor',
                           'italian': 'Mousemoor', 'japanese': 'マウスムーア', 'korean': '마우스무어', 'polish': 'Mousemoor',
                           'russian': 'Маусмур', 'spanish': 'Mousemoor', 'taiwanese': '茅斯穆爾'},
                   20185: {'chinese': '瑞姆普顿', 'english': 'Realmpton', 'french': 'Realmpton', 'german': 'Realmpton',
                           'italian': 'Realmpton', 'japanese': 'レルムトン', 'korean': '림튼', 'polish': 'Realmpton',
                           'russian': 'Рилмптон', 'spanish': 'Realmpton', 'taiwanese': '瑞姆普頓'},
                   20186: {'chinese': '美诺斯', 'english': 'Maynoss', 'french': 'Maynoss', 'german': 'Maynoss',
                           'italian': 'Maynoss', 'japanese': 'メイノス', 'korean': '메이노스', 'polish': 'Maynoss',
                           'russian': 'Мэйносс', 'spanish': 'Maynoss', 'taiwanese': '美諾斯'},
                   20187: {'chinese': '克兰姆顿', 'english': 'Clamton', 'french': 'Clamton', 'german': 'Clamton',
                           'italian': 'Clamton', 'japanese': 'クラムトン', 'korean': '클램튼', 'polish': 'Clamton',
                           'russian': 'Клэмтон', 'spanish': 'Clamton', 'taiwanese': '克蘭姆頓'},
                   20188: {'chinese': '拉劳镇', 'english': 'La Rouzan', 'french': 'La Rouzan', 'german': 'La Rouzan',
                           'italian': 'La Rouzan', 'japanese': 'ラ・ルザン', 'korean': '라 루장', 'polish': 'La Rouzan',
                           'russian': 'Ля Рузан', 'spanish': 'La Rouzan', 'taiwanese': '拉勞鎮'},
                   20189: {'chinese': '卡萨克斯', 'english': 'Cazaux', 'french': 'Cazaux', 'german': 'Cazaux',
                           'italian': 'Cazaux', 'japanese': 'カゾ', 'korean': '카조', 'polish': 'Cazaux', 'russian': 'Казо',
                           'spanish': 'Cazaux', 'taiwanese': '卡薩克斯'},
                   20190: {'chinese': '高登', 'english': 'Gourden', 'french': 'Gourden', 'german': 'Gourden',
                           'italian': 'Gourden', 'japanese': 'グールデン', 'korean': '구르뎅', 'polish': 'Gourden',
                           'russian': 'Гурден', 'spanish': 'Gourden', 'taiwanese': '高登'},
                   20191: {'chinese': '陶维列', 'english': 'Touville', 'french': 'Touville', 'german': 'Touville',
                           'italian': 'Touville', 'japanese': 'トゥヴィラ', 'korean': '투빌', 'polish': 'Touville',
                           'russian': 'Тувиль', 'spanish': 'Touville', 'taiwanese': '陶維列'},
                   20192: {'chinese': '普拉汀', 'english': 'Pratine', 'french': 'Pratine', 'german': 'Pratine',
                           'italian': 'Pratine', 'japanese': 'プラティン', 'korean': '프라틴느', 'polish': 'Pratine',
                           'russian': 'Пратин', 'spanish': 'Pratine', 'taiwanese': '普拉汀'},
                   20193: {'chinese': '拉尔蒙德', 'english': 'Larmande', 'french': 'Larmande', 'german': 'Larmande',
                           'italian': 'Larmande', 'japanese': 'ラルマンド', 'korean': '라르망드', 'polish': 'Larmande',
                           'russian': 'Ларманд', 'spanish': 'Larmande', 'taiwanese': '拉爾蒙德'},
                   20194: {'chinese': '鲁寇尔德', 'english': 'Ruchord', 'french': 'Ruchord', 'german': 'Ruchord',
                           'italian': 'Ruchord', 'japanese': 'ルショルド', 'korean': '뤼쇼르', 'polish': 'Ruchord',
                           'russian': 'Рюшор', 'spanish': 'Ruchord', 'taiwanese': '魯寇爾德'},
                   20195: {'chinese': '寇格纳克', 'english': 'Chourgnac', 'french': 'Chourgnac', 'german': 'Chourgnac',
                           'italian': 'Chourgnac', 'japanese': 'ショルニアック', 'korean': '슈르냑', 'polish': 'Chourgnac',
                           'russian': 'Шурньяк', 'spanish': 'Chourgnac', 'taiwanese': '寇格納克'},
                   20196: {'chinese': '瓦尔波内', 'english': 'Varbonne', 'french': 'Varbonne', 'german': 'Varbonne',
                           'italian': 'Varbonne', 'japanese': 'ヴァルボンヌ', 'korean': '바르본느', 'polish': 'Varbonne',
                           'russian': 'Варбонн', 'spanish': 'Varbonne', 'taiwanese': '瓦爾波內'},
                   20197: {'chinese': '陶尔兰克斯', 'english': 'Taurenx', 'french': 'Taurenx', 'german': 'Taurenx',
                           'italian': 'Taurenx', 'japanese': 'トーレンクス', 'korean': '토렝', 'polish': 'Taurenx',
                           'russian': 'Торан', 'spanish': 'Taurenx', 'taiwanese': '陶爾蘭克斯'},
                   20198: {'chinese': '瑞芙瑟弗欧伊斯', 'english': 'Rive-sur-Foix', 'french': 'Rive-sur-Foix',
                           'german': 'Rive-\u200bsur-\u200bFoix', 'italian': 'Rive-Sur-Foix', 'japanese': 'リーヴ・シュール・フア',
                           'korean': '리브쉬르푸아', 'polish': 'Rive-sur-Foix', 'russian': 'Рив-сюр-Фуа',
                           'spanish': 'Rive-sur-Foix', 'taiwanese': '瑞芙瑟弗歐伊斯'},
                   20199: {'chinese': '曼潘都', 'english': 'Manpendu', 'french': 'Manpendu', 'german': 'Manpendu',
                           'italian': 'Manpendu', 'japanese': 'マンポンデュ', 'korean': '망팽뒤', 'polish': 'Manpendu',
                           'russian': 'Манпандю', 'spanish': 'Manpendu', 'taiwanese': '曼潘都'},
                   20200: {'chinese': '维勒盖拉克', 'english': 'Vallegaillac', 'french': 'Vallegaillac',
                           'german': 'Vallegaillac', 'italian': 'Vallegaillac', 'japanese': 'ヴァイユギャラック',
                           'korean': '발르가이약', 'polish': 'Vallegaillac', 'russian': 'Вальгайак',
                           'spanish': 'Vallegaillac', 'taiwanese': '維勒蓋拉克'},
                   20201: {'chinese': '拉凡沃契', 'english': 'La Fanourge', 'french': 'La Fanourge',
                           'german': 'La Fanourge', 'italian': 'La Fanourge', 'japanese': 'ラ・ファヌーク', 'korean': '라 파누르주',
                           'polish': 'La Fanourge', 'russian': 'Ля Фанурж', 'spanish': 'La Fanourge',
                           'taiwanese': '拉凡沃契'},
                   20202: {'chinese': '圣西尔', 'english': 'Saint Sére', 'french': 'Saint-Sère', 'german': 'Saint Sére',
                           'italian': 'Saint Sére', 'japanese': 'サン・セーレ', 'korean': '생 세르', 'polish': 'Saint Sére',
                           'russian': 'Сен Сер', 'spanish': 'Saint Sére', 'taiwanese': '聖西爾'},
                   20203: {'chinese': '勒斯埃米斯', 'english': 'Les Emies', 'french': 'Les Émies', 'german': 'Les Emies',
                           'italian': 'Les Emies', 'japanese': 'レゼミ', 'korean': '레 제미', 'polish': 'Les Emies',
                           'russian': 'Ле Эми', 'spanish': 'Les Emies', 'taiwanese': '勒斯埃米斯'},
                   20204: {'chinese': '蒙罗萨勒斯', 'english': 'Monrouzailles', 'french': 'Monrouzailles',
                           'german': 'Monrouzailles', 'italian': 'Monrouzailles', 'japanese': 'モンローゼユ', 'korean': '몽루젤',
                           'polish': 'Monrouzailles', 'russian': 'Монрузай', 'spanish': 'Monrouzailles',
                           'taiwanese': '蒙羅薩勒斯'},
                   20205: {'chinese': '厄斯薛拉多', 'english': "Eze sur l'Adour", 'french': "Eze-sur-l'Adour",
                           'german': "Eze sur l'Adour", 'italian': "Eze sur l'Adour", 'japanese': 'エｾﾞ・シュール・ラドゥール',
                           'korean': '에즈 쉬르 라두르', 'polish': "Eze sur l'Adour", 'russian': "Эз сюр л'Адур",
                           'spanish': "Eze sur l'Adour", 'taiwanese': '厄斯薛拉多'},
                   20206: {'chinese': '蒙苏康', 'english': 'Monsuçon', 'french': 'Montsurron', 'german': 'Monsuçon',
                           'italian': 'Monsuçon', 'japanese': 'モンション', 'korean': '몽쉬꽁', 'polish': 'Monsuçon',
                           'russian': 'Монсюсон', 'spanish': 'Monsuçon', 'taiwanese': '蒙蘇康'},
                   20207: {'chinese': '查图萨拉辛', 'english': 'Château Sarrasin', 'french': 'Château-Sarrasin',
                           'german': 'Château Sarrasin', 'italian': 'Château Sarrasin', 'japanese': 'シャトー・サラザン',
                           'korean': '샤토 사라쟁', 'polish': 'Château Sarrasin', 'russian': 'Шато Саррасин',
                           'spanish': 'Château Sarrasin', 'taiwanese': '查圖薩拉辛'},
                   20208: {'chinese': '皮尔盖恩', 'english': 'Périganne', 'french': 'Périganne', 'german': 'Périganne',
                           'italian': 'Périganne', 'japanese': 'ペリギャンヌ', 'korean': '페리간느', 'polish': 'Périganne',
                           'russian': 'Периганн', 'spanish': 'Périganne', 'taiwanese': '皮爾蓋恩'},
                   20209: {'chinese': '勒斯库萨欧恩', 'english': 'Les Creusaône', 'french': 'Les Creussones',
                           'german': 'Les Creusaône', 'italian': 'Les Creusaône', 'japanese': 'レ・クレウゾーナ',
                           'korean': '레 크뢰손', 'polish': 'Les Creusaône', 'russian': 'Ле Кресан',
                           'spanish': 'Les Creusaône', 'taiwanese': '勒斯庫薩歐恩'},
                   20210: {'chinese': '波利恩伊丝', 'english': 'Pouilly-en-Esse', 'french': 'Pouilly-en-Esse',
                           'german': 'Pouilly-\u200ben-\u200bEsse', 'italian': 'Pouilly-En-Esse',
                           'japanese': 'プイイ・アネッセ', 'korean': '푸이엉에스', 'polish': 'Pouilly-en-Esse',
                           'russian': 'Пуйи-ан-Эсс', 'spanish': 'Pouilly-en-Esse', 'taiwanese': '波利恩伊絲'},
                   20211: {'chinese': '特宁瑞', 'english': 'Tenenrey', 'french': 'Tenenrey', 'german': 'Tenenrey',
                           'italian': 'Tenenrey', 'japanese': 'テネンレイ', 'korean': '텐느레', 'polish': 'Tenenrey',
                           'russian': 'Тенанре', 'spanish': 'Tenenrey', 'taiwanese': '特寧瑞'},
                   20212: {'chinese': '迪斯耶瑞斯', 'english': 'Disnières', 'french': 'Disnières', 'german': 'Disnières',
                           'italian': 'Disnières', 'japanese': 'ディズニエーレ', 'korean': '디스니에르', 'polish': 'Disnières',
                           'russian': 'Дисньер', 'spanish': 'Disnières', 'taiwanese': '迪斯耶瑞斯'},
                   20213: {'chinese': '维德路克斯', 'english': 'Verdreux', 'french': 'Verdreux', 'german': 'Verdreux',
                           'italian': 'Verdreux', 'japanese': 'ヴェルドロー', 'korean': '베르드뢰', 'polish': 'Verdreux',
                           'russian': 'Вердро', 'spanish': 'Verdreux', 'taiwanese': '維德路克斯'},
                   20214: {'chinese': '拉弗德', 'english': 'La Ferté', 'french': 'La Ferté', 'german': 'La Ferté',
                           'italian': 'La Ferté', 'japanese': 'ラ・フェルテ', 'korean': '라 페르테', 'polish': 'La Ferté',
                           'russian': 'Ля Ферте', 'spanish': 'La Ferté', 'taiwanese': '拉弗德'},
                   20215: {'chinese': '瑞米黛', 'english': 'Remiedai', 'french': 'Remiedai', 'german': 'Remiedai',
                           'italian': 'Remiedai', 'japanese': 'レミーダイ', 'korean': '르미데', 'polish': 'Remiedai',
                           'russian': 'Ремьеде', 'spanish': 'Remiedai', 'taiwanese': '瑞米黛'},
                   20216: {'chinese': '高德雷尔', 'english': 'Goutelaire', 'french': 'Goutelaire', 'german': 'Goutelaire',
                           'italian': 'Goutelaire', 'japanese': 'グートレア', 'korean': '구틀레르', 'polish': 'Goutelaire',
                           'russian': 'Гутелер', 'spanish': 'Goutelaire', 'taiwanese': '高德雷爾'},
                   20217: {'chinese': '格拉谢', 'english': 'Graicé', 'french': 'Graicé', 'german': 'Graicé',
                           'italian': 'Graicé', 'japanese': 'グレイセ', 'korean': '그레세', 'polish': 'Graicé',
                           'russian': 'Гресе', 'spanish': 'Graicé', 'taiwanese': '格拉謝'},
                   20218: {'chinese': '山达赖', 'english': 'Chendalai', 'french': 'Chendalai', 'german': 'Chendalai',
                           'italian': 'Chendalai', 'japanese': 'シエンダライ', 'korean': '샹달레', 'polish': 'Chendalai',
                           'russian': 'Шандале', 'spanish': 'Chendalai', 'taiwanese': '山達賴'},
                   20219: {'chinese': '拉巴黛勒', 'english': 'La Bataille', 'french': 'La Bataille',
                           'german': 'La Bataille', 'italian': 'La Bataille', 'japanese': 'ラ・バタイユ', 'korean': '라 바타이유',
                           'polish': 'La Bataille', 'russian': 'Ля Батай', 'spanish': 'La Bataille',
                           'taiwanese': '拉巴黛勒'},
                   20220: {'chinese': '欧布道曲', 'english': "Orb-d'Ouche", 'french': 'Breteuil-sur-Ouche',
                           'german': "Orb-\u200bd'Ouche", 'italian': "Orb-d'Ouche", 'japanese': 'オルブ・ドゥシュ',
                           'korean': '오르브두슈', 'polish': "Orb-d'Ouche", 'russian': "Орб-д'Уш", 'spanish': "Orb-d'Ouche",
                           'taiwanese': '歐布道曲'},
                   20221: {'chinese': '蒙特萨拉席克斯', 'english': 'Mont-Saraceaux', 'french': 'Mont-Saraceaux',
                           'german': 'Mont-\u200bSaraceaux', 'italian': 'Mont-Saraceaux', 'japanese': 'モン・サーラソー',
                           'korean': '몽사라소', 'polish': 'Mont-Saraceaux', 'russian': 'Мон-Сарасо',
                           'spanish': 'Mont-Saraceaux', 'taiwanese': '蒙特薩拉席克斯'},
                   20222: {'chinese': '卡拉瑟布隆玛', 'english': 'Caresse-Bromage', 'french': 'Ferté-Bromage',
                           'german': 'Caresse-\u200bBromage', 'italian': 'Caresse-Bromage', 'japanese': 'カレス・ブロマージュ',
                           'korean': '카레스브로마쥬', 'polish': 'Caresse-Bromage', 'russian': 'Карес-Бромаж',
                           'spanish': 'Caresse-Bromage', 'taiwanese': '卡拉瑟布隆瑪'},
                   20223: {'chinese': '瑟西杜寇格', 'english': 'Surcy-du-Courg', 'french': 'Surcy-du-Courg',
                           'german': 'Surcy-\u200bdu-\u200bCourg', 'italian': 'Surcy-du-Courg',
                           'japanese': 'シュルシュ・デュ・クー', 'korean': '쉬르시뒤쿠르', 'polish': 'Surcy-du-Courg',
                           'russian': 'Сюрси-дю-Кур', 'spanish': 'Surcy-du-Courg', 'taiwanese': '瑟西杜寇格'},
                   20224: {'chinese': '荣西', 'english': 'Roncy', 'french': 'Roncy', 'german': 'Roncy',
                           'italian': 'Roncy', 'japanese': 'ロンチー', 'korean': '롱시', 'polish': 'Roncy',
                           'russian': 'Ронси', 'spanish': 'Roncy', 'taiwanese': '榮西'},
                   20225: {'chinese': '彭杜拉丹格斯', 'english': 'Pont-du-Radanges', 'french': 'Pont-du-Radanges',
                           'german': 'Pont-\u200bdu-\u200bRadanges', 'italian': 'Pont-du-Radanges',
                           'japanese': 'ポン・デュ・ラダンジュ', 'korean': '퐁뒤라당주', 'polish': 'Pont-du-Radanges',
                           'russian': 'Пон-дю-Раданж', 'spanish': 'Pont-du-Radanges', 'taiwanese': '彭杜拉丹格斯'},
                   20226: {'chinese': '特雷库维斯', 'english': 'Trecuvées', 'french': 'Trecuvées', 'german': 'Trecuvées',
                           'italian': 'Trecuvées', 'japanese': 'トレクーヴェ', 'korean': '트레퀴베', 'polish': 'Trecuvées',
                           'russian': 'Трекюве', 'spanish': 'Trecuvées', 'taiwanese': '特雷庫維斯'},
                   20227: {'chinese': '毕乌维斯德', 'english': 'Beauviste', 'french': 'Beauviste', 'german': 'Beauviste',
                           'italian': 'Beauviste', 'japanese': 'ブーヴィステ', 'korean': '보비스트', 'polish': 'Beauviste',
                           'russian': 'Бовист', 'spanish': 'Beauviste', 'taiwanese': '畢烏維斯德'},
                   20228: {'chinese': '勒格兰席尔', 'english': 'Le Grand-Ciel', 'french': 'Le Grand-Ciel',
                           'german': 'Le Grand-\u200bCiel', 'italian': 'Le Grand-Ciel', 'japanese': 'ル・グラン・シエル',
                           'korean': '르 그랑시엘', 'polish': 'Le Grand-Ciel', 'russian': 'Ле Гран-Сьель',
                           'spanish': 'Le Grand-Ciel', 'taiwanese': '勒格蘭席爾'},
                   20229: {'chinese': '提尔皮德', 'english': 'Tierpied', 'french': 'Tierpied', 'german': 'Tierpied',
                           'italian': 'Tierpied', 'japanese': 'ティーエピエ', 'korean': '티에르피에', 'polish': 'Tierpied',
                           'russian': 'Тьепье', 'spanish': 'Tierpied', 'taiwanese': '提爾皮德'},
                   20230: {'chinese': '利欧那拜尔', 'english': 'Lyonabbaye', 'french': 'Lyonabbaye', 'german': 'Lyonabbaye',
                           'italian': 'Lyonabbaye', 'japanese': 'リヨナバイユ', 'korean': '리요나베이', 'polish': 'Lyonabbaye',
                           'russian': 'Лайонаббеи', 'spanish': 'Lyonabbaye', 'taiwanese': '利歐那拜爾'},
                   20231: {'chinese': '诺特冯', 'english': 'Notre-Font', 'french': 'Notre-Font',
                           'german': 'Notre-\u200bFont', 'italian': 'Notre-Font', 'japanese': 'ノートル・フォン',
                           'korean': '노트르퐁', 'polish': 'Notre-Font', 'russian': 'Нотр-Фон', 'spanish': 'Notre-Font',
                           'taiwanese': '諾特馮'},
                   20232: {'chinese': '劳索尔斯', 'english': "L'Ousores", 'french': "L'Ousores", 'german': "L'Ousores",
                           'italian': "L'Ousores", 'japanese': 'ルゾーレ', 'korean': '루소르', 'polish': "L'Ousores",
                           'russian': "Л'Усор", 'spanish': "L'Ousores", 'taiwanese': '勞索爾斯'},
                   20233: {'chinese': '雪沛勒塞布雷斯', 'english': 'Chapelle-Cyprés', 'french': 'Chapelle-Cyprés',
                           'german': 'Chapelle-\u200bCyprés', 'italian': 'Chapelle-Cyprés', 'japanese': 'シャペル・シプレ',
                           'korean': '샤펠시프레', 'polish': 'Chapelle-Cyprés', 'russian': 'Шапель-Сипре',
                           'spanish': 'Chapelle-Cyprés', 'taiwanese': '雪沛勒塞布雷斯'},
                   20234: {'chinese': '丹斯提曲', 'english': 'Denstricht', 'french': 'Denstricht', 'german': 'Denstricht',
                           'italian': 'Denstricht', 'japanese': 'ダンストリヒト', 'korean': '덴스트리흐트', 'polish': 'Denstricht',
                           'russian': 'Денстрихт', 'spanish': 'Denstricht', 'taiwanese': '丹斯提曲'},
                   20235: {'chinese': '波萧特', 'english': 'Borschot', 'french': 'Borschot', 'german': 'Borschot',
                           'italian': 'Borschot', 'japanese': 'ボルショト', 'korean': '보르쇼트', 'polish': 'Borschot',
                           'russian': 'Боршот', 'spanish': 'Borschot', 'taiwanese': '波蕭特'},
                   20236: {'chinese': '伊克劳斯', 'english': 'Eekloux', 'french': 'Eekloux', 'german': 'Eekloux',
                           'italian': 'Eekloux', 'japanese': 'イークルー', 'korean': '에이클라우크스', 'polish': 'Eekloux',
                           'russian': 'Эклю', 'spanish': 'Eekloux', 'taiwanese': '伊克勞斯'},
                   20237: {'chinese': '吉克兰', 'english': 'Gekeren', 'french': 'Gekeren', 'german': 'Gekeren',
                           'italian': 'Gekeren', 'japanese': 'ゲックレン', 'korean': '게케렌', 'polish': 'Gekeren',
                           'russian': 'Гекерен', 'spanish': 'Gekeren', 'taiwanese': '吉克蘭'},
                   20238: {'chinese': '杜丹梅', 'english': 'Du Damme', 'french': 'Du Damme', 'german': 'Du Damme',
                           'italian': 'Du Damme', 'japanese': 'ドゥ・ダメン', 'korean': '뒤 다머', 'polish': 'Du Damme',
                           'russian': 'Дю Дам', 'spanish': 'Du Damme', 'taiwanese': '杜丹梅'},
                   20239: {'chinese': '河敦弗特', 'english': 'Hottonfort', 'french': 'Hottonfort', 'german': 'Hottonfort',
                           'italian': 'Hottonfort', 'japanese': 'ホットンフォルト', 'korean': '호톤포르트', 'polish': 'Hottonfort',
                           'russian': 'Хоттонфорт', 'spanish': 'Hottonfort', 'taiwanese': '河敦弗特'},
                   20240: {'chinese': '司涅肯班', 'english': 'Sneekenbam', 'french': 'Sneekenbam', 'german': 'Sneekenbam',
                           'italian': 'Sneekenbam', 'japanese': 'シュニーケンバム', 'korean': '스네이켄밤', 'polish': 'Sneekenbam',
                           'russian': 'Снекенбам', 'spanish': 'Sneekenbam', 'taiwanese': '司涅肯班'},
                   20241: {'chinese': '司空格拉文', 'english': 'Schoongraven', 'french': 'Schoongraven',
                           'german': 'Schoongraven', 'italian': 'Schoongraven', 'japanese': 'ショーングラーヴェン',
                           'korean': '스홍라번', 'polish': 'Schoongraven', 'russian': 'Схонгравен',
                           'spanish': 'Schoongraven', 'taiwanese': '司空格拉文'},
                   20242: {'chinese': '卡勒伯格', 'english': 'Calemborg', 'french': 'Calemborg', 'german': 'Calemborg',
                           'italian': 'Calemborg', 'japanese': 'カーレンボルグ', 'korean': '칼렘보르흐', 'polish': 'Calemborg',
                           'russian': 'Калемборг', 'spanish': 'Calemborg', 'taiwanese': '卡勒伯格'},
                   20243: {'chinese': '切斯提米尔', 'english': 'Chiesstemeer', 'french': 'Chiesstemeer',
                           'german': 'Chiesstemeer', 'italian': 'Chiesstemeer', 'japanese': 'チェステミーア',
                           'korean': '히스테메이르', 'polish': 'Chiesstemeer', 'russian': 'Хистенмер',
                           'spanish': 'Chiesstemeer', 'taiwanese': '切斯提米爾'},
                   20244: {'chinese': '凯天维克', 'english': 'Cattenwijk', 'french': 'Cattenwijk', 'german': 'Cattenwijk',
                           'italian': 'Cattenwijk', 'japanese': 'キャッテンヴェーク', 'korean': '카텐베이크', 'polish': 'Cattenwijk',
                           'russian': 'Каттенвек', 'spanish': 'Cattenwijk', 'taiwanese': '凱天維克'},
                   20245: {'chinese': '乌尔迪布洛克', 'english': 'Woerdebroek', 'french': 'Woerdebroek',
                           'german': 'Woerdebroek', 'italian': 'Woerdebroek', 'japanese': 'ウォーデブルック', 'korean': '부르데브룩',
                           'polish': 'Woerdebroek', 'russian': 'Вердербрек', 'spanish': 'Woerdebroek',
                           'taiwanese': '烏爾迪布洛克'},
                   20246: {'chinese': '诺勒雪天', 'english': 'Knolleschoten', 'french': 'Knolleschoten',
                           'german': 'Knolleschoten', 'italian': 'Knolleschoten', 'japanese': 'クノルショーテン',
                           'korean': '크놀레스호턴', 'polish': 'Knolleschoten', 'russian': 'Кноллешотен',
                           'spanish': 'Knolleschoten', 'taiwanese': '諾勒雪天'},
                   20247: {'chinese': '登格斯沃德', 'english': 'Dungelswaard', 'french': 'Dungelswaard',
                           'german': 'Dungelswaard', 'italian': 'Dungelswaard', 'japanese': 'ドンゲルスヴァルド',
                           'korean': '뒹엘스바르트', 'polish': 'Dungelswaard', 'russian': 'Дюнгелсвард',
                           'spanish': 'Dungelswaard', 'taiwanese': '登格斯沃德'},
                   20248: {'chinese': '弗里寇普', 'english': 'Frickop', 'french': 'Frickop', 'german': 'Frickop',
                           'italian': 'Frickop', 'japanese': 'フリッコップ', 'korean': '프리코프', 'polish': 'Frickop',
                           'russian': 'Фриккоп', 'spanish': 'Frickop', 'taiwanese': '弗里寇普'},
                   20249: {'chinese': '布鲁根那乌兹', 'english': 'Bruggenknauz', 'french': 'Bruggenknauz',
                           'german': 'Bruggenknauz', 'italian': 'Bruggenknauz', 'japanese': 'ブルッゲンクナウツ',
                           'korean': '브루겡크나우츠', 'polish': 'Bruggenknauz', 'russian': 'Бруггенкнауц',
                           'spanish': 'Bruggenknauz', 'taiwanese': '布魯根那烏茲'},
                   20250: {'chinese': '瑞克丹姆', 'english': 'Reeukerdam', 'french': 'Reeukerdam', 'german': 'Reeukerdam',
                           'italian': 'Reeukerdam', 'japanese': 'リーウケルダム', 'korean': '레오이케르담', 'polish': 'Reeukerdam',
                           'russian': 'Реукердам', 'spanish': 'Reeukerdam', 'taiwanese': '瑞克丹姆'},
                   20251: {'chinese': '皮克维格', 'english': 'Pikerweg', 'french': 'Pikerweg', 'german': 'Pikerweg',
                           'italian': 'Pikerweg', 'japanese': 'ピーケルヴェク', 'korean': '피케르베크', 'polish': 'Pikerweg',
                           'russian': 'Пикервег', 'spanish': 'Pikerweg', 'taiwanese': '皮克維格'},
                   20252: {'chinese': '波尔薛分', 'english': 'Polshoven', 'french': 'Polshoven', 'german': 'Polshoven',
                           'italian': 'Polshoven', 'japanese': 'ポルショーヴェン', 'korean': '폴스호펜', 'polish': 'Polshoven',
                           'russian': 'Полсховен', 'spanish': 'Polshoven', 'taiwanese': '波爾薛分'},
                   20253: {'chinese': '维提库普', 'english': 'Uitkoop', 'french': 'Uitkoop', 'german': 'Uitkoop',
                           'italian': 'Uitkoop', 'japanese': 'アートコープ', 'korean': '아위트코프', 'polish': 'Uitkoop',
                           'russian': 'Эйткоп', 'spanish': 'Uitkoop', 'taiwanese': '維提庫普'},
                   20254: {'chinese': '巴巴克维恩', 'english': 'Babakkeveen', 'french': 'Babakkeveen',
                           'german': 'Babakkeveen', 'italian': 'Babakkeveen', 'japanese': 'ババックヴィーン', 'korean': '바바케베인',
                           'polish': 'Babakkeveen', 'russian': 'Бабаккевен', 'spanish': 'Babakkeveen',
                           'taiwanese': '巴巴克維恩'},
                   20255: {'chinese': '贾巴维克', 'english': 'Jabaghwijk', 'french': 'Jabaghwijk', 'german': 'Jabaghwijk',
                           'italian': 'Jabaghwijk', 'japanese': 'ヤバフヴェク', 'korean': '야바흐베이크', 'polish': 'Jabaghwijk',
                           'russian': 'Ябагвейк', 'spanish': 'Jabaghwijk', 'taiwanese': '賈巴維克'},
                   20256: {'chinese': '斯特瑞特', 'english': 'Schtrecht', 'french': 'Schtrecht', 'german': 'Schtrecht',
                           'italian': 'Schtrecht', 'japanese': 'シュトレヒト', 'korean': '스트레흐트', 'polish': 'Schtrecht',
                           'russian': 'Штрехт', 'spanish': 'Schtrecht', 'taiwanese': '斯特瑞特'},
                   20257: {'chinese': '密仙波许', 'english': 'Michienbosch', 'french': 'Michienbosch',
                           'german': 'Michienbosch', 'italian': 'Michienbosch', 'japanese': 'ミシェンボッシュ',
                           'korean': '미힌보스', 'polish': 'Michienbosch', 'russian': 'Мишинбош', 'spanish': 'Michienbosch',
                           'taiwanese': '密仙波許'},
                   20258: {'chinese': '雷文洛德', 'english': 'Ravenrode', 'french': 'Ravenrode', 'german': 'Ravenrode',
                           'italian': 'Ravenrode', 'japanese': 'ラーヴェンロード', 'korean': '라벤로더', 'polish': 'Ravenrode',
                           'russian': 'Равенрозе', 'spanish': 'Ravenrode', 'taiwanese': '雷文洛德'},
                   20259: {'chinese': '穆厄斯达特', 'english': 'Mührstädt', 'french': 'Mührstädt', 'german': 'Mührstädt',
                           'italian': 'Mührstädt', 'japanese': 'ミューアシュタット', 'korean': '뮈르슈테트', 'polish': 'Mührstädt',
                           'russian': 'Мюрштедт', 'spanish': 'Mührstädt', 'taiwanese': '穆厄斯達特'},
                   20260: {'chinese': '泽斯提恩', 'english': 'Zijdstein', 'french': 'Zijdstein', 'german': 'Zijdstein',
                           'italian': 'Zijdstein', 'japanese': 'ザイトシュタイン', 'korean': '제이츠테인', 'polish': 'Zijdstein',
                           'russian': 'Цийдштайн', 'spanish': 'Zijdstein', 'taiwanese': '澤斯提恩'},
                   20261: {'chinese': '德维霍斯特', 'english': 'Dievehorst', 'french': 'Dievehorst', 'german': 'Dievehorst',
                           'italian': 'Dievehorst', 'japanese': 'ディエヴェホルスト', 'korean': '디베호르스트', 'polish': 'Dievehorst',
                           'russian': 'Дифехорст', 'spanish': 'Dievehorst', 'taiwanese': '德維霍斯特'},
                   20262: {'chinese': '弗拉格布雷曲', 'english': 'Vlagtbrecht', 'french': 'Vlagtbrecht',
                           'german': 'Vlagtbrecht', 'italian': 'Vlagtbrecht', 'japanese': 'ヴラフトブレヒト',
                           'korean': '플라흐트브레흐트', 'polish': 'Vlagtbrecht', 'russian': 'Флагтбрехт',
                           'spanish': 'Vlagtbrecht', 'taiwanese': '弗拉格布雷曲'},
                   20263: {'chinese': '诺伊瑟尔', 'english': 'Noetxel', 'french': 'Noetxel', 'german': 'Noetxel',
                           'italian': 'Noetxel', 'japanese': 'ノエトゥクセル', 'korean': '눗크설', 'polish': 'Noetxel',
                           'russian': 'Нетксель', 'spanish': 'Noetxel', 'taiwanese': '諾伊瑟爾'},
                   20264: {'chinese': '欧麦斯门', 'english': 'Ommesthmen', 'french': 'Ommesthmen', 'german': 'Ommesthmen',
                           'italian': 'Ommesthmen', 'japanese': 'オメンスメン', 'korean': '오메스트먼', 'polish': 'Ommesthmen',
                           'russian': 'Омместмен', 'spanish': 'Ommesthmen', 'taiwanese': '歐麥斯門'},
                   20265: {'chinese': '那尔勒', 'english': 'Naarle', 'french': 'Naarle', 'german': 'Naarle',
                           'italian': 'Naarle', 'japanese': 'ナール', 'korean': '나를러', 'polish': 'Naarle',
                           'russian': 'Нарле', 'spanish': 'Naarle', 'taiwanese': '那爾勒'},
                   20266: {'chinese': '路特古拉文', 'english': 'Luttengraven', 'french': 'Luttengraven',
                           'german': 'Luttengraven', 'italian': 'Luttengraven', 'japanese': 'ルッタングラーヴェン',
                           'korean': '뤼텡라번', 'polish': 'Luttengraven', 'russian': 'Люттенгравен',
                           'spanish': 'Luttengraven', 'taiwanese': '路特古拉文'},
                   20267: {'chinese': '纽路特道普', 'english': 'Nieuw Luttendorp', 'french': 'Nieuw Luttendorp',
                           'german': 'Nieuw Luttendorp', 'italian': 'Nieuw Luttendorp', 'japanese': 'ニウ・ルッタンドルプ',
                           'korean': '니우뤼텐도르프', 'polish': 'Nieuw Luttendorp', 'russian': 'Ньив Люттендорп',
                           'spanish': 'Nieuw Luttendorp', 'taiwanese': '紐路特道普'},
                   20268: {'chinese': '沃斯德', 'english': 'Wosde', 'french': 'Wosde', 'german': 'Wosde',
                           'italian': 'Wosde', 'japanese': 'ワスド', 'korean': '보스더', 'polish': 'Wosde',
                           'russian': 'Восде', 'spanish': 'Wosde', 'taiwanese': '沃斯德'},
                   20269: {'chinese': '哈夫特布尔克', 'english': 'Haftbrink', 'french': 'Haftbrink', 'german': 'Haftbrink',
                           'italian': 'Haftbrink', 'japanese': 'ハフトブリンク', 'korean': '하프트브링크', 'polish': 'Haftbrink',
                           'russian': 'Хафтбринк', 'spanish': 'Haftbrink', 'taiwanese': '哈夫特布林克'},
                   20270: {'chinese': '杜文格鲁', 'english': 'Dwangeloo', 'french': 'Dwangeloo', 'german': 'Dwangeloo',
                           'italian': 'Dwangeloo', 'japanese': 'ドワンジェルー', 'korean': '드방엘로', 'polish': 'Dwangeloo',
                           'russian': 'Двангело', 'spanish': 'Dwangeloo', 'taiwanese': '杜文格魯'},
                   20271: {'chinese': '夸克洛特', 'english': 'Quaklotte', 'french': 'Quaklotte', 'german': 'Quaklotte',
                           'italian': 'Quaklotte', 'japanese': 'クヮークロッテ', 'korean': '크바클로터', 'polish': 'Quaklotte',
                           'russian': 'Кваклотте', 'spanish': 'Quaklotte', 'taiwanese': '夸克洛特'},
                   20272: {'chinese': '拉赫达乌克', 'english': 'Rahdabrück', 'french': 'Rahdabrück', 'german': 'Rahdabrück',
                           'italian': 'Rahdabrück', 'japanese': 'ラーダブック', 'korean': '라다브뤼크', 'polish': 'Rahdabrück',
                           'russian': 'Радабрюк', 'spanish': 'Rahdabrück', 'taiwanese': '拉赫達烏克'},
                   20273: {'chinese': '贝德格兰瑟', 'english': 'Bad Glanther', 'french': 'Bad Glanther',
                           'german': 'Bad Glanther', 'italian': 'Bad Glanther', 'japanese': 'バッド・グランター',
                           'korean': '바트 글란터', 'polish': 'Bad Glanther', 'russian': 'Бэд Глэнтер',
                           'spanish': 'Bad Glanther', 'taiwanese': '貝德格蘭瑟'},
                   20274: {'chinese': '高登哈夫特', 'english': 'Goldenhöfte', 'french': 'Goldenhöfte',
                           'german': 'Goldenhöfte', 'italian': 'Goldenhöfte', 'japanese': 'ゴールデンホフト', 'korean': '골덴회프테',
                           'polish': 'Goldenhöfte', 'russian': 'Гольденхефте', 'spanish': 'Goldenhöfte',
                           'taiwanese': '高登哈夫特'},
                   20275: {'chinese': '那赫德斯恩', 'english': 'Nachdessen', 'french': 'Nachdessen', 'german': 'Nachdessen',
                           'italian': 'Nachdessen', 'japanese': 'ナハデッセン', 'korean': '나흐데센', 'polish': 'Nachdessen',
                           'russian': 'Нахдессен', 'spanish': 'Nachdessen', 'taiwanese': '那赫德斯恩'},
                   20276: {'chinese': '约恩辛', 'english': 'Jønsing', 'french': 'Jønsing', 'german': 'Jønsing',
                           'italian': 'Jønsing', 'japanese': 'ヨンシング', 'korean': '옌싱', 'polish': 'Jønsing',
                           'russian': 'Йенсинг', 'spanish': 'Jønsing', 'taiwanese': '約恩辛'},
                   20277: {'chinese': '霍斯特雷普', 'english': 'Hostræp', 'french': 'Hostræp', 'german': 'Hostræp',
                           'italian': 'Hostræp', 'japanese': 'ホストラップ', 'korean': '호스트레프', 'polish': 'Hostræp',
                           'russian': 'Хостреп', 'spanish': 'Hostræp', 'taiwanese': '霍斯特雷普'},
                   20278: {'chinese': '黎德厄普', 'english': 'Lyderup', 'french': 'Lyderup', 'german': 'Lyderup',
                           'italian': 'Lyderup', 'japanese': 'リーダラップ', 'korean': '뤼데루프', 'polish': 'Lyderup',
                           'russian': 'Людеруп', 'spanish': 'Lyderup', 'taiwanese': '黎德厄普'},
                   20279: {'chinese': '蒙根科克', 'english': 'Mølgenkirke', 'french': 'Mølgenkirke',
                           'german': 'Mølgenkirke', 'italian': 'Mølgenkirke', 'japanese': 'モルゲンキアケ', 'korean': '묄겡키르케',
                           'polish': 'Mølgenkirke', 'russian': 'Мельгенкирке', 'spanish': 'Mølgenkirke',
                           'taiwanese': '蒙根科克'},
                   20280: {'chinese': '哈尔斯德', 'english': 'Hajsted', 'french': 'Hajsted', 'german': 'Hajsted',
                           'italian': 'Hajsted', 'japanese': 'ハイステッド', 'korean': '하이스테드', 'polish': 'Hajsted',
                           'russian': 'Хайстед', 'spanish': 'Hajsted', 'taiwanese': '哈爾斯德'},
                   20281: {'chinese': '斯克雷约特', 'english': 'Skærbjert', 'french': 'Skærbjert', 'german': 'Skærbjert',
                           'italian': 'Skærbjert', 'japanese': 'スケルビヤート', 'korean': '셰르비에르트', 'polish': 'Skærbjert',
                           'russian': 'Скербьерт', 'spanish': 'Skærbjert', 'taiwanese': '斯克雷約特'},
                   20282: {'chinese': '斯达维斯特', 'english': 'Stårvester', 'french': 'Stårvester', 'german': 'Stårvester',
                           'italian': 'Stårvester', 'japanese': 'ストルヴェステル', 'korean': '스타르베스테르', 'polish': 'Stårvester',
                           'russian': 'Сторвестер', 'spanish': 'Stårvester', 'taiwanese': '斯達維斯特'},
                   20283: {'chinese': '哈斯里萨德', 'english': 'Hässlesad', 'french': 'Hässlesad', 'german': 'Hässlesad',
                           'italian': 'Hässlesad', 'japanese': 'ハッスレサド', 'korean': '하슬레사드', 'polish': 'Hässlesad',
                           'russian': 'Хясслесад', 'spanish': 'Hässlesad', 'taiwanese': '哈斯里薩德'},
                   20284: {'chinese': '提弗科厄普', 'english': 'Tifkærup', 'french': 'Tifkærup', 'german': 'Tifkærup',
                           'italian': 'Tifkærup', 'japanese': 'ティフケラップ', 'korean': '티프캬이뤼프', 'polish': 'Tifkærup',
                           'russian': 'Тифкеруп', 'spanish': 'Tifkærup', 'taiwanese': '提弗科厄普'},
                   20285: {'chinese': '恩斯维勒', 'english': 'Øsvlev', 'french': 'Øsvlev', 'german': 'Øsvlev',
                           'italian': 'Øsvlev', 'japanese': 'ウスヴレフ', 'korean': '스블레브', 'polish': 'Øsvlev',
                           'russian': 'Эсвлев', 'spanish': 'Øsvlev', 'taiwanese': '恩斯維勒'},
                   20286: {'chinese': '塞勒弗欧姆', 'english': 'Thyrupholm', 'french': 'Thyrupholm', 'german': 'Thyrupholm',
                           'italian': 'Thyrupholm', 'japanese': 'チュラプホルム', 'korean': '트히뤼프홀름', 'polish': 'Thyrupholm',
                           'russian': 'Тюруфольм', 'spanish': 'Thyrupholm', 'taiwanese': '塞勒弗歐姆'},
                   20287: {'chinese': '亨斯格勒恩', 'english': 'Hunsglund', 'french': 'Hunsglund', 'german': 'Hunsglund',
                           'italian': 'Hunsglund', 'japanese': 'フンスグルント', 'korean': '휜스글륀드', 'polish': 'Hunsglund',
                           'russian': 'Хунсглунд', 'spanish': 'Hunsglund', 'taiwanese': '亨斯格勒恩'},
                   20288: {'chinese': '斯基约格', 'english': 'Skidbjerg', 'french': 'Skidbjerg', 'german': 'Skidbjerg',
                           'italian': 'Skidbjerg', 'japanese': 'スキドビョルク', 'korean': '스키드비에르그', 'polish': 'Skidbjerg',
                           'russian': 'Скидбьерг', 'spanish': 'Skidbjerg', 'taiwanese': '斯基約格'},
                   20289: {'chinese': '伊斯高拚', 'english': 'Essköping', 'french': 'Essköping', 'german': 'Essköping',
                           'italian': 'Essköping', 'japanese': 'イシャーピン', 'korean': '에스쾨핑그', 'polish': 'Essköping',
                           'russian': 'Эсскепинг', 'spanish': 'Essköping', 'taiwanese': '伊斯高拚'},
                   20290: {'chinese': '弗里克堡', 'english': 'Frykberg', 'french': 'Frykberg', 'german': 'Frykberg',
                           'italian': 'Frykberg', 'japanese': 'フリュクベリ', 'korean': '프리크베르그', 'polish': 'Frykberg',
                           'russian': 'Фрюкберг', 'spanish': 'Frykberg', 'taiwanese': '弗里克堡'},
                   20291: {'chinese': '阿弗斯宾', 'english': 'Arvsbyn', 'french': 'Arvsbyn', 'german': 'Arvsbyn',
                           'italian': 'Arvsbyn', 'japanese': 'アルプスビーン', 'korean': '아르빈', 'polish': 'Arvsbyn',
                           'russian': 'Арвсбюн', 'spanish': 'Arvsbyn', 'taiwanese': '阿弗斯賓'},
                   20292: {'chinese': '斯特雷森德', 'english': 'Stræksund', 'french': 'Stræksund', 'german': 'Stræksund',
                           'italian': 'Stræksund', 'japanese': 'ストライクスンド', 'korean': '스트라익쉰드', 'polish': 'Stræksund',
                           'russian': 'Стрексунд', 'spanish': 'Stræksund', 'taiwanese': '斯特雷森德'},
                   20293: {'chinese': '该隐瓦卡', 'english': 'Keinvakka', 'french': 'Keinvakka', 'german': 'Keinvakka',
                           'italian': 'Keinvakka', 'japanese': 'カインヴァッカ', 'korean': '케인바카', 'polish': 'Keinvakka',
                           'russian': 'Кейнвакка', 'spanish': 'Keinvakka', 'taiwanese': '該隱瓦卡'},
                   20294: {'chinese': '三德西', 'english': 'Sandisi', 'french': 'Sandisi', 'german': 'Sandisi',
                           'italian': 'Sandisi', 'japanese': 'サンディシ', 'korean': '산디시', 'polish': 'Sandisi',
                           'russian': 'Сандиси', 'spanish': 'Sandisi', 'taiwanese': '三德西'},
                   20295: {'chinese': '波达迪斯昆佐', 'english': 'Porta di Squinzo', 'french': 'Porta di Squinzo',
                           'german': 'Porta di Squinzo', 'italian': 'Porta di Squinzo', 'japanese': 'ポルタ・ディ・スクインゾ',
                           'korean': '포르타 디 스퀸초', 'polish': 'Porta di Squinzo', 'russian': 'Порта ди Скуинцо',
                           'spanish': 'Porta di Squinzo', 'taiwanese': '波達迪斯昆佐'},
                   20296: {'chinese': '斯寇拉斯罗', 'english': 'Scorastro', 'french': 'Scorastro', 'german': 'Scorastro',
                           'italian': 'Scorastro', 'japanese': 'スコラストロ', 'korean': '스코라스트로', 'polish': 'Scorastro',
                           'russian': 'Скорастро', 'spanish': 'Scorastro', 'taiwanese': '斯寇拉斯羅'},
                   20297: {'chinese': '瓦多卡瑟', 'english': 'Vadocasse', 'french': 'Vadocasse', 'german': 'Vadocasse',
                           'italian': 'Vadocasse', 'japanese': 'ヴァードカッセ', 'korean': '바도카세', 'polish': 'Vadocasse',
                           'russian': 'Вадокассе', 'spanish': 'Vadocasse', 'taiwanese': '瓦多卡瑟'},
                   20298: {'chinese': '欧恩特兰多', 'english': 'Ontranto', 'french': 'Ontranto', 'german': 'Ontranto',
                           'italian': 'Ontranto', 'japanese': 'オントラント', 'korean': '온트란토', 'polish': 'Ontranto',
                           'russian': 'Онтранто', 'spanish': 'Ontranto', 'taiwanese': '歐恩特蘭多'},
                   20299: {'chinese': '普罗锡提诺', 'english': 'Prosciuttino', 'french': 'Prosciuttino',
                           'german': 'Prosciuttino', 'italian': 'Prosciuttino', 'japanese': 'プロシュッティーノ',
                           'korean': '프로시우티노', 'polish': 'Prosciuttino', 'russian': 'Прошуттино',
                           'spanish': 'Prosciuttino', 'taiwanese': '普羅錫提諾'},
                   20300: {'chinese': '珈罗德罗', 'english': 'Chiarodero', 'french': 'Chiarodero', 'german': 'Chiarodero',
                           'italian': 'Chiarodero', 'japanese': 'キアーロデッロ', 'korean': '키아로데로', 'polish': 'Chiarodero',
                           'russian': 'Кьяродеро', 'spanish': 'Chiarodero', 'taiwanese': '珈羅德羅'},
                   20301: {'chinese': '格尔吉诺', 'english': 'Gorginno', 'french': 'Gorginno', 'german': 'Gorginno',
                           'italian': 'Gorginno', 'japanese': 'ゴルキッノ', 'korean': '고르진노', 'polish': 'Gorginno',
                           'russian': 'Горджинно', 'spanish': 'Gorginno', 'taiwanese': '格爾吉諾'},
                   20302: {'chinese': '格里曼', 'english': 'Grimmen', 'french': 'Grimmen', 'german': 'Grimmen',
                           'italian': 'Grimmen', 'japanese': 'グリッメン', 'korean': '그리멘', 'polish': 'Grimmen',
                           'russian': 'Гриммен', 'spanish': 'Grimmen', 'taiwanese': '格里曼'},
                   20303: {'chinese': '沃斯维恩', 'english': 'Wollsvenn', 'french': 'Wollsvenn', 'german': 'Wollsvenn',
                           'italian': 'Wollsvenn', 'japanese': 'ヴォルスヴェン', 'korean': '볼스벤', 'polish': 'Wollsvenn',
                           'russian': 'Вольсфен', 'spanish': 'Wollsvenn', 'taiwanese': '沃斯維恩'},
                   20304: {'chinese': '斯坦豪森', 'english': 'Stenhausen', 'french': 'Stenhausen', 'german': 'Stenhausen',
                           'italian': 'Stenhausen', 'japanese': 'シュテンハウゼン', 'korean': '슈텐하우젠', 'polish': 'Stenhausen',
                           'russian': 'Штенхаузен', 'spanish': 'Stenhausen', 'taiwanese': '斯坦豪森'},
                   20305: {'chinese': '克尔萨伯恩', 'english': 'Kulzaborn', 'french': 'Kulzaborn', 'german': 'Kulzaborn',
                           'italian': 'Kulzaborn', 'japanese': 'クルツァボルン', 'korean': '쿨차보른', 'polish': 'Kulzaborn',
                           'russian': 'Кульцаборн', 'spanish': 'Kulzaborn', 'taiwanese': '克爾薩伯恩'},
                   20306: {'chinese': '威森根', 'english': 'Wessungen', 'french': 'Wessungen', 'german': 'Wessungen',
                           'italian': 'Wessungen', 'japanese': 'ヴェッソンゲン', 'korean': '베숭겐', 'polish': 'Wessungen',
                           'russian': 'Вессунген', 'spanish': 'Wessungen', 'taiwanese': '威森根'},
                   20307: {'chinese': '帕尔巴德', 'english': 'Palbate', 'french': 'Palbate', 'german': 'Palbate',
                           'italian': 'Palbate', 'japanese': 'パルバーテ', 'korean': '팔바테', 'polish': 'Palbate',
                           'russian': 'Пальбате', 'spanish': 'Palbate', 'taiwanese': '帕爾巴德'},
                   20309: {'chinese': '萨罗席诺斯', 'english': 'Salocinos', 'french': 'Salocinos', 'german': 'Salocinos',
                           'italian': 'Salocinos', 'japanese': 'サーロチーノ', 'korean': '살로시노스', 'polish': 'Salocinos',
                           'russian': 'Салочинос', 'spanish': 'Salocinos', 'taiwanese': '薩羅席諾斯'},
                   20310: {'chinese': '敦盖洛曲', 'english': 'Don Galoche', 'french': 'Don Garoche',
                           'german': 'Don Galoche', 'italian': 'Don Galoche', 'japanese': 'ドン・ガローシェ', 'korean': '돈 갈로체',
                           'polish': 'Don Galoche', 'russian': 'Дон Галоке', 'spanish': 'Don Galoche',
                           'taiwanese': '敦蓋洛曲'},
                   20311: {'chinese': '拉斯柏南德拉斯', 'english': 'Las Bernanderas', 'french': 'Las Bernanderas',
                           'german': 'Las Bernanderas', 'italian': 'Las Bernanderas', 'japanese': 'ラス・ベルナンデラス',
                           'korean': '라스 베르난데라스', 'polish': 'Las Bernanderas', 'russian': 'Лас Бернандерас',
                           'spanish': 'Las Bernanderas', 'taiwanese': '拉斯柏南德拉斯'},
                   20312: {'chinese': '霍维利利欧', 'english': 'Hoyuelillo', 'french': 'Hoyuelillo', 'german': 'Hoyuelillo',
                           'italian': 'Hoyuelillo', 'japanese': 'オージョエリーロ', 'korean': '오유엘리요', 'polish': 'Hoyuelillo',
                           'russian': 'Ойюэлильо', 'spanish': 'Hoyuelillo', 'taiwanese': '霍維利利歐'},
                   20313: {'chinese': '拉斯坦纳斯', 'english': 'Lastañas', 'french': 'Lastañas', 'german': 'Lastañas',
                           'italian': 'Lastañas', 'japanese': 'ラスタニャス', 'korean': '라스타냐스', 'polish': 'Lastañas',
                           'russian': 'Ластаньяс', 'spanish': 'Lastañas', 'taiwanese': '拉斯坦納斯'},
                   20314: {'chinese': '艾尔帕格', 'english': 'Alpager', 'french': 'Alpager', 'german': 'Alpager',
                           'italian': 'Alpager', 'japanese': 'アルパゲル', 'korean': '알파헤르', 'polish': 'Alpager',
                           'russian': 'Альпахер', 'spanish': 'Alpager', 'taiwanese': '艾爾帕格'},
                   20315: {'chinese': '胡斯坦恩', 'english': 'Huestañén', 'french': 'Huestañén', 'german': 'Huestañén',
                           'italian': 'Huestañén', 'japanese': 'ウエスタニャン', 'korean': '우에스타녠', 'polish': 'Huestañén',
                           'russian': 'Уэстаньен', 'spanish': 'Huestañén', 'taiwanese': '胡斯坦恩'},
                   20316: {'chinese': '敦敦摩尔', 'english': 'Dundunmore', 'french': 'Dundunmore', 'german': 'Dundunmore',
                           'italian': 'Dundunmore', 'japanese': 'ダンドンモア', 'korean': '던던모어', 'polish': 'Dundunmore',
                           'russian': 'Данданмор', 'spanish': 'Dundunmore', 'taiwanese': '敦敦摩爾'},
                   20317: {'chinese': '克洛福特', 'english': 'Croghford', 'french': 'Croghford', 'german': 'Croghford',
                           'italian': 'Croghford', 'japanese': 'クロフフォード', 'korean': '크로그포드', 'polish': 'Croghford',
                           'russian': 'Крогхфорд', 'spanish': 'Croghford', 'taiwanese': '克洛福特'},
                   20318: {'chinese': '玛克劳', 'english': 'Maklow', 'french': 'Maklow', 'german': 'Maklow',
                           'italian': 'Maklow', 'japanese': 'マクロウ', 'korean': '마크로', 'polish': 'Maklow',
                           'russian': 'Маклоу', 'spanish': 'Maklow', 'taiwanese': '瑪克勞'},
                   20319: {'chinese': '塔瑞克', 'english': 'Tarrick', 'french': 'Tarrick', 'german': 'Tarrick',
                           'italian': 'Tarrick', 'japanese': 'タリック', 'korean': '타릭', 'polish': 'Tarrick',
                           'russian': 'Таррик', 'spanish': 'Tarrick', 'taiwanese': '塔瑞克'},
                   20320: {'chinese': '巴尔提维', 'english': 'Baltiway', 'french': 'Baltiway', 'german': 'Baltiway',
                           'italian': 'Baltiway', 'japanese': 'バルティウェイ', 'korean': '발티웨이', 'polish': 'Baltiway',
                           'russian': 'Болтиуэй', 'spanish': 'Baltiway', 'taiwanese': '巴爾提維'},
                   20330: {'chinese': '索科罗斯', 'english': 'Socorros', 'french': 'Socorros', 'german': 'Socorros',
                           'italian': 'Socorros', 'japanese': 'ソコロス', 'korean': '소코후스', 'polish': 'Socorros',
                           'russian': 'Сокоррос', 'spanish': 'Socorros', 'taiwanese': '索科羅斯'},
                   20331: {'chinese': '弗恩诺德芬多', 'english': 'Forno de Fundo', 'french': 'Forno de Fundo',
                           'german': 'Forno de Fundo', 'italian': 'Forno de Fundo', 'japanese': 'フォルノ・デ・フンド',
                           'korean': '포르누 지 푼두', 'polish': 'Forno de Fundo', 'russian': 'Форно де Фундо',
                           'spanish': 'Forno de Fundo', 'taiwanese': '弗恩諾德芬多'},
                   20332: {'chinese': '帕多魁多', 'english': 'Patoquieto', 'french': 'Patoquieto', 'german': 'Patoquieto',
                           'italian': 'Patoquieto', 'japanese': 'パトキエト', 'korean': '파토키에투', 'polish': 'Patoquieto',
                           'russian': 'Патокито', 'spanish': 'Patoquieto', 'taiwanese': '帕多魁多'},
                   20333: {'chinese': '布伊诺斯维恩多', 'english': 'Buenos Vientos', 'french': 'Buenos Vientos',
                           'german': 'Buenos Vientos', 'italian': 'Buenos Vientos', 'japanese': 'ブエノス・ヴィエントス',
                           'korean': '부에누스 비엔투스', 'polish': 'Buenos Vientos', 'russian': 'Буэнос Вьентос',
                           'spanish': 'Buenos Vientos', 'taiwanese': '布伊諾斯維恩多'},
                   20334: {'chinese': '索罗塔', 'english': 'Xolota', 'french': 'Xolota', 'german': 'Xolota',
                           'italian': 'Xolota', 'japanese': 'クソロータ', 'korean': '숄로타', 'polish': 'Xolota',
                           'russian': 'Ксолота', 'spanish': 'Xolota', 'taiwanese': '索羅塔'},
                   20335: {'chinese': '圣杜兰诺', 'english': 'San Duraño', 'french': 'San Duraño', 'german': 'San Duraño',
                           'italian': 'San Duraño', 'japanese': 'サンドゥーラノ', 'korean': '상 두라누', 'polish': 'San Duraño',
                           'russian': 'Сан Дураньо', 'spanish': 'San Duraño', 'taiwanese': '聖杜蘭諾'},
                   20336: {'chinese': '里约德胡安妮塔', 'english': 'Río de Juanita', 'french': 'Río de Juanita',
                           'german': 'Río de Juanita', 'italian': 'Río de Juanita', 'japanese': 'リオ・デ・フアニータ',
                           'korean': '히우 지 주아니타', 'polish': 'Río de Juanita', 'russian': 'Рио де Жуанита',
                           'spanish': 'Río de Juanita', 'taiwanese': '里約德胡安妮塔'},
                   20337: {'chinese': '塔塔吉纳', 'english': 'Tartagena', 'french': 'Tartagena', 'german': 'Tartagena',
                           'italian': 'Tartagena', 'japanese': 'タルタゲーナ', 'korean': '타르타제나', 'polish': 'Tartagena',
                           'russian': 'Тартахена', 'spanish': 'Tartagena', 'taiwanese': '塔塔吉納'},
                   20338: {'chinese': '普尔多山姆拉', 'english': 'Puerto Salmuera', 'french': 'Puerto Salmuera',
                           'german': 'Puerto Salmuera', 'italian': 'Puerto Salmuera', 'japanese': 'プエルト・サルムエラ',
                           'korean': '푸에르투 사우무에라', 'polish': 'Puerto Salmuera', 'russian': 'Пуэрто Сальмуэра',
                           'spanish': 'Puerto Salmuera', 'taiwanese': '普爾多山姆拉'},
                   20339: {'chinese': '圣塔敦督纳', 'english': 'Santa Tontuna', 'french': 'Santa Tontuna',
                           'german': 'Santa Tontuna', 'italian': 'Santa Tontuna', 'japanese': 'サンタ・トントゥナ',
                           'korean': '산타 톤투나', 'polish': 'Santa Tontuna', 'russian': 'Санта Тонтуна',
                           'spanish': 'Santa Tontuna', 'taiwanese': '聖塔敦督納'},
                   20340: {'chinese': '布加洛曼格斯', 'english': 'Bucaromangos', 'french': 'Bucaromangos',
                           'german': 'Bucaromangos', 'italian': 'Bucaromangos', 'japanese': 'ブーカロマンゴス',
                           'korean': '부카로망구스', 'polish': 'Bucaromangos', 'russian': 'Букаромангос',
                           'spanish': 'Bucaromangos', 'taiwanese': '布加洛曼格斯'},
                   20341: {'chinese': '萨欧玛特梨霍', 'english': 'São Martelinho', 'french': 'São Martelinho',
                           'german': 'São Martelinho', 'italian': 'São Martelinho', 'japanese': 'ソン・マルテリニョ',
                           'korean': '상 마르텔리뉴', 'polish': 'São Martelinho', 'russian': 'Сан-Мартелинью',
                           'spanish': 'São Martelinho', 'taiwanese': '薩歐瑪特梨霍'},
                   20342: {'chinese': '多尔达诺斯', 'english': 'Toledanos', 'french': 'Toledanos', 'german': 'Toledanos',
                           'italian': 'Toledanos', 'japanese': 'トレダノス', 'korean': '톨레다누스', 'polish': 'Toledanos',
                           'russian': 'Толеданос', 'spanish': 'Toledanos', 'taiwanese': '多爾達諾斯'},
                   20343: {'chinese': '弗特欧罗', 'english': 'Fuerteolor', 'french': 'Fuerteolor', 'german': 'Fuerteolor',
                           'italian': 'Fuerteolor', 'japanese': 'フエルテオロール', 'korean': '푸에르테올로르', 'polish': 'Fuerteolor',
                           'russian': 'Фуэртеолор', 'spanish': 'Fuerteolor', 'taiwanese': '弗特歐羅'},
                   20344: {'chinese': '卡拉加', 'english': 'Carraca', 'french': 'Carraca', 'german': 'Carraca',
                           'italian': 'Carraca', 'japanese': 'カラッカ', 'korean': '카하카', 'polish': 'Carraca',
                           'russian': 'Каррака', 'spanish': 'Carraca', 'taiwanese': '卡拉加'},
                   20345: {'chinese': '玛札林', 'english': 'Mazallín', 'french': 'Mazallín', 'german': 'Mazallín',
                           'italian': 'Mazallín', 'japanese': 'マサリン', 'korean': '마잘링', 'polish': 'Mazallín',
                           'russian': 'Масальин', 'spanish': 'Mazallín', 'taiwanese': '瑪札林'},
                   20346: {'chinese': '多斯吉姆拉斯', 'english': 'Dos Gemelas', 'french': 'Dos Gemelas',
                           'german': 'Dos Gemelas', 'italian': 'Dos Gemelas', 'japanese': 'ドス・ヘメラス',
                           'korean': '두스 제멜라스', 'polish': 'Dos Gemelas', 'russian': 'Дос Хемелас',
                           'spanish': 'Dos Gemelas', 'taiwanese': '多斯吉姆拉斯'},
                   20347: {'chinese': '克拉亨迪达', 'english': 'Calahundida', 'french': 'Calahundida',
                           'german': 'Calahundida', 'italian': 'Calahundida', 'japanese': 'カーラウンディーダ',
                           'korean': '칼라운지다', 'polish': 'Calahundida', 'russian': 'Калаундида',
                           'spanish': 'Calahundida', 'taiwanese': '克拉亨迪達'},
                   20348: {'chinese': '布恩纳科斯塔', 'english': 'Buenacosta', 'french': 'Buenacosta', 'german': 'Buenacosta',
                           'italian': 'Buenacosta', 'japanese': 'ブエナコスタ', 'korean': '부에나코스타', 'polish': 'Buenacosta',
                           'russian': 'Буэнакоста', 'spanish': 'Buenacosta', 'taiwanese': '布恩納科斯塔'},
                   20349: {'chinese': '玛雷伊纳', 'english': 'Mereiña', 'french': 'Mereiña', 'german': 'Mereiña',
                           'italian': 'Mereiña', 'japanese': 'メレイニャ', 'korean': '메레이나', 'polish': 'Mereiña',
                           'russian': 'Мерейнья', 'spanish': 'Mereiña', 'taiwanese': '瑪雷伊納'},
                   20350: {'chinese': '拉帕斯夸', 'english': 'La Pascua', 'french': 'La Pascua', 'german': 'La Pascua',
                           'italian': 'La Pascua', 'japanese': 'ラ・パスクア', 'korean': '라 파스쿠아', 'polish': 'La Pascua',
                           'russian': 'Ла Паскуа', 'spanish': 'La Pascua', 'taiwanese': '拉帕斯夸'},
                   20351: {'chinese': '波高丹帕', 'english': 'Bogotampa', 'french': 'Bogotampa', 'german': 'Bogotampa',
                           'italian': 'Bogotampa', 'japanese': 'ボゴタンパ', 'korean': '보고탐파', 'polish': 'Bogotampa',
                           'russian': 'Боготампа', 'spanish': 'Bogotampa', 'taiwanese': '波高丹帕'},
                   20352: {'chinese': '贝拉肯寇迪亚', 'english': 'Bella Concordia', 'french': 'Bella Concordia',
                           'german': 'Bella Concordia', 'italian': 'Bella Concordia', 'japanese': 'ベイヤ・コンコルディア',
                           'korean': '벨라 콩코르지아', 'polish': 'Bella Concordia', 'russian': 'Белья Конкордия',
                           'spanish': 'Bella Concordia', 'taiwanese': '貝拉肯寇迪亞'},
                   20353: {'chinese': '艾尔多巴西罗斯', 'english': 'Alto Barcilos', 'french': 'Alto Barcilos',
                           'german': 'Alto Barcilos', 'italian': 'Alto Barcilos', 'japanese': 'アウト・バルシロス',
                           'korean': '아우투 바르실루스', 'polish': 'Alto Barcilos', 'russian': 'Алто Барсилуш',
                           'spanish': 'Alto Barcilos', 'taiwanese': '艾爾多巴西羅斯'},
                   20354: {'chinese': '阿瑞西弗卡尔伯恩', 'english': 'Arrecife Carbón', 'french': 'Arrecife Carbón',
                           'german': 'Arrecife Carbón', 'italian': 'Arrecife Carbón', 'japanese': 'アレシフェ・カルボン',
                           'korean': '아헤시피 카르봉', 'polish': 'Arrecife Carbón', 'russian': 'Арресифе Карбон',
                           'spanish': 'Arrecife Carbón', 'taiwanese': '阿瑞西弗卡爾伯恩'},
                   20355: {'chinese': '瓜拉魁洛', 'english': 'Guaraquillo', 'french': 'Guaraquillo',
                           'german': 'Guaraquillo', 'italian': 'Guaraquillo', 'japanese': 'グアラキーヨ', 'korean': '구아라킬루',
                           'polish': 'Guaraquillo', 'russian': 'Гваракильо', 'spanish': 'Guaraquillo',
                           'taiwanese': '瓜拉魁洛'},
                   20356: {'chinese': '布兰卡瑞纳斯', 'english': 'Blancarenas', 'french': 'Blancarenas',
                           'german': 'Blancarenas', 'italian': 'Blancarenas', 'japanese': 'ブランカレナス', 'korean': '블랑카레나스',
                           'polish': 'Blancarenas', 'russian': 'Бланкаренас', 'spanish': 'Blancarenas',
                           'taiwanese': '布蘭卡瑞納斯'},
                   20357: {'chinese': '拉阿尔卡萨贝塔', 'english': 'La Alcazabeta', 'french': 'La Alcazabeta',
                           'german': 'La Alcazabeta', 'italian': 'La Alcazabeta', 'japanese': 'ラ・アルカサベータ',
                           'korean': '라 아우카자베타', 'polish': 'La Alcazabeta', 'russian': 'Ла Алькасабета',
                           'spanish': 'La Alcazabeta', 'taiwanese': '拉阿爾卡薩貝塔'},
                   20358: {'chinese': '萨拉曼魁萨', 'english': 'Salamanquesa', 'french': 'Salamanquesa',
                           'german': 'Salamanquesa', 'italian': 'Salamanquesa', 'japanese': 'サラマンケサ', 'korean': '살라망케자',
                           'polish': 'Salamanquesa', 'russian': 'Саламанкеса', 'spanish': 'Salamanquesa',
                           'taiwanese': '薩拉曼魁薩'},
                   20359: {'chinese': '欧维诺', 'english': 'Ovino', 'french': 'Ovino', 'german': 'Ovino',
                           'italian': 'Ovino', 'japanese': 'オヴィーノ', 'korean': '오비누', 'polish': 'Ovino',
                           'russian': 'Овино', 'spanish': 'Ovino', 'taiwanese': '歐維諾'},
                   20360: {'chinese': '丹皮魁特', 'english': 'Tampiquete', 'french': 'Tampiquete', 'german': 'Tampiquete',
                           'italian': 'Tampiquete', 'japanese': 'タンピケーテ', 'korean': '탐피케치', 'polish': 'Tampiquete',
                           'russian': 'Тампикете', 'spanish': 'Tampiquete', 'taiwanese': '丹皮魁特'},
                   20361: {'chinese': '欧利泽尔瓦', 'english': 'Orizalva', 'french': 'Orizalva', 'german': 'Orizalva',
                           'italian': 'Orizalva', 'japanese': 'オリサルヴァ', 'korean': '오리자우바', 'polish': 'Orizalva',
                           'russian': 'Уризалва', 'spanish': 'Orizalva', 'taiwanese': '歐利澤爾瓦'},
                   20362: {'chinese': '弗尔纳达拉兰亚', 'english': 'Ferna da Laranja', 'french': 'Ferna da Laranja',
                           'german': 'Ferna da Laranja', 'italian': 'Ferna da Laranja', 'japanese': 'フェルナ・ダ・ラランジャ',
                           'korean': '페르나 다 라란자', 'polish': 'Ferna da Laranja', 'russian': 'Ферна да Ларанжа',
                           'spanish': 'Ferna da Laranja', 'taiwanese': '弗爾納達拉蘭亞'},
                   20363: {'chinese': '莎莎维德', 'english': 'Salsa Verde', 'french': 'Salsa Verde',
                           'german': 'Salsa Verde', 'italian': 'Salsa Verde', 'japanese': 'サルサ・ヴェルデ',
                           'korean': '사우사 베르지', 'polish': 'Salsa Verde', 'russian': 'Сальса Верде',
                           'spanish': 'Salsa Verde', 'taiwanese': '莎莎維德'},
                   20364: {'chinese': '阿祖勒斯', 'english': 'Azures', 'french': 'Azures', 'german': 'Azures',
                           'italian': 'Azures', 'japanese': 'アズーレス', 'korean': '아수레스', 'polish': 'Azures',
                           'russian': 'Асурес', 'spanish': 'Azures', 'taiwanese': '阿祖勒斯'},
                   20365: {'chinese': '圣西弗斯特雷', 'english': 'San Silvestre', 'french': 'San Silvestre',
                           'german': 'San Silvestre', 'italian': 'San Silvestre', 'japanese': 'サン・シルヴェストレ',
                           'korean': '상 시우베스트리', 'polish': 'San Silvestre', 'russian': 'Сан Сильвестре',
                           'spanish': 'San Silvestre', 'taiwanese': '聖西弗斯特雷'},
                   20366: {'chinese': '贝拉诺瓦', 'english': 'Belanova', 'french': 'Belanova', 'german': 'Belanova',
                           'italian': 'Belanova', 'japanese': 'ベラノーヴァ', 'korean': '벨라노바', 'polish': 'Belanova',
                           'russian': 'Беланова', 'spanish': 'Belanova', 'taiwanese': '貝拉諾瓦'},
                   20367: {'chinese': '玛哈多尼亚', 'english': 'Mahadonia', 'french': 'Mahadonia', 'german': 'Mahadonia',
                           'italian': 'Mahadonia', 'japanese': 'マハドニア', 'korean': '마아도니아', 'polish': 'Mahadonia',
                           'russian': 'Маадония', 'spanish': 'Mahadonia', 'taiwanese': '瑪哈多尼亞'},
                   20368: {'chinese': '艾尔维斯乌', 'english': 'Alvestuz', 'french': 'Alvestuz', 'german': 'Alvestuz',
                           'italian': 'Alvestuz', 'japanese': 'アルヴェストゥス', 'korean': '아우베스투스', 'polish': 'Alvestuz',
                           'russian': 'Альвестус', 'spanish': 'Alvestuz', 'taiwanese': '艾爾維斯烏'},
                   20369: {'chinese': '甘索康普纳斯', 'english': 'Ganso Com Pernas', 'french': 'Ganso Com Pernas',
                           'german': 'Ganso Com Pernas', 'italian': 'Ganso Com Pernas', 'japanese': 'ガンソ・コン・ペールナス',
                           'korean': '간수 콩 페르나스', 'polish': 'Ganso Com Pernas', 'russian': 'Гансу ком Пернаш',
                           'spanish': 'Ganso Com Pernas', 'taiwanese': '甘索康普納斯'},
                   20370: {'chinese': '洛克萨', 'english': 'Loxa', 'french': 'Loxa', 'german': 'Loxa', 'italian': 'Loxa',
                           'japanese': 'ロクサ', 'korean': '로샤', 'polish': 'Loxa', 'russian': 'Лоша', 'spanish': 'Loxa',
                           'taiwanese': '洛克薩'},
                   20371: {'chinese': '塔亚亚', 'english': 'Tajarja', 'french': 'Tajarja', 'german': 'Tajarja',
                           'italian': 'Tajarja', 'japanese': 'タハルハ', 'korean': '타자르자', 'polish': 'Tajarja',
                           'russian': 'Тахарха', 'spanish': 'Tajarja', 'taiwanese': '塔亞亞'},
                   20372: {'chinese': '卡帕拉亚', 'english': 'Caparaia', 'french': 'Caparaia', 'german': 'Caparaia',
                           'italian': 'Caparaia', 'japanese': 'カパライア', 'korean': '카파라이아', 'polish': 'Caparaia',
                           'russian': 'Капарая', 'spanish': 'Caparaia', 'taiwanese': '卡帕拉亞'},
                   20373: {'chinese': '维拉诺约纳', 'english': 'Villaovejuna', 'french': 'Villaovejuna',
                           'german': 'Villaovejuna', 'italian': 'Villaovejuna', 'japanese': 'ヴィラオヴェフナ',
                           'korean': '빌라오베주나', 'polish': 'Villaovejuna', 'russian': 'Вильяовехуна',
                           'spanish': 'Villaovejuna', 'taiwanese': '維拉諾約納'},
                   20374: {'chinese': '梅斯康多', 'english': 'Mescondo', 'french': 'Mescondo', 'german': 'Mescondo',
                           'italian': 'Mescondo', 'japanese': 'メスコンド', 'korean': '메스콘두', 'polish': 'Mescondo',
                           'russian': 'Мескондо', 'spanish': 'Mescondo', 'taiwanese': '梅斯康多'},
                   20375: {'chinese': '拉卡巴纳', 'english': 'La Cabaña', 'french': 'La Cabaña', 'german': 'La Cabaña',
                           'italian': 'La Cabaña', 'japanese': 'ラ・カバーニャ', 'korean': '라 카바나', 'polish': 'La Cabaña',
                           'russian': 'Ла Кабанья', 'spanish': 'La Cabaña', 'taiwanese': '拉卡巴納'},
                   20376: {'chinese': '帕拉宾波', 'english': 'Parabimbo', 'french': 'Parabimbo', 'german': 'Parabimbo',
                           'italian': 'Parabimbo', 'japanese': 'パラビンボ', 'korean': '파라빔부', 'polish': 'Parabimbo',
                           'russian': 'Парабимбо', 'spanish': 'Parabimbo', 'taiwanese': '帕拉賓波'},
                   20377: {'chinese': '玛札帕', 'english': 'Mazapá', 'french': 'Mazapá', 'german': 'Mazapá',
                           'italian': 'Mazapá', 'japanese': 'マサパ', 'korean': '마자파', 'polish': 'Mazapá',
                           'russian': 'Масапа', 'spanish': 'Mazapá', 'taiwanese': '瑪札帕'},
                   20378: {'chinese': '波尼塔路西亚', 'english': 'Bonita Lucía', 'french': 'Bonita Lucía',
                           'german': 'Bonita Lucía', 'italian': 'Bonita Lucía', 'japanese': 'ボニータ・ルシア',
                           'korean': '보니타 루시아', 'polish': 'Bonita Lucía', 'russian': 'Бонита Лусия',
                           'spanish': 'Bonita Lucía', 'taiwanese': '波尼塔路西亞'},
                   20379: {'chinese': '巴西亚阿祖尔', 'english': 'Bahía Azúl', 'french': 'Bahía Azúl', 'german': 'Bahía Azúl',
                           'italian': 'Bahía Azúl', 'japanese': 'バイア・アズル', 'korean': '바이아 아줄', 'polish': 'Bahía Azúl',
                           'russian': 'Баия Асуль', 'spanish': 'Bahía Azúl', 'taiwanese': '巴西亞阿祖爾'},
                   20380: {'chinese': '波维玛', 'english': 'Bovima', 'french': 'Bovima', 'german': 'Bovima',
                           'italian': 'Bovima', 'japanese': 'ボヴィーマ', 'korean': '보비마', 'polish': 'Bovima',
                           'russian': 'Бовима', 'spanish': 'Bovima', 'taiwanese': '波維瑪'},
                   20381: {'chinese': '玛卡帕欧斯', 'english': 'Macapaos', 'french': 'Macapaos', 'german': 'Macapaos',
                           'italian': 'Macapaos', 'japanese': 'マカパオス', 'korean': '마카파우스', 'polish': 'Macapaos',
                           'russian': 'Макапауш', 'spanish': 'Macapaos', 'taiwanese': '瑪卡帕歐斯'},
                   20382: {'chinese': '克里皮纳斯', 'english': 'Curipinas', 'french': 'Curipinas', 'german': 'Curipinas',
                           'italian': 'Curipinas', 'japanese': 'クリピナス', 'korean': '쿠리피나스', 'polish': 'Curipinas',
                           'russian': 'Курипинас', 'spanish': 'Curipinas', 'taiwanese': '克里皮納斯'},
                   20383: {'chinese': '拉帕梅拉', 'english': 'La Palmera', 'french': 'La Palmera', 'german': 'La Palmera',
                           'italian': 'La Palmera', 'japanese': 'ラ・パルメラ', 'korean': '라 파우메라', 'polish': 'La Palmera',
                           'russian': 'Ла Пальмера', 'spanish': 'La Palmera', 'taiwanese': '拉帕梅拉'},
                   20384: {'chinese': '玛德瑞伊亚', 'english': 'Madereira', 'french': 'Madereira', 'german': 'Madereira',
                           'italian': 'Madereira', 'japanese': 'マデレイラ', 'korean': '마데레이라', 'polish': 'Madereira',
                           'russian': 'Мадерейра', 'spanish': 'Madereira', 'taiwanese': '瑪德瑞伊亞'},
                   20385: {'chinese': '关提欧伊斯特', 'english': 'Guanteoeste', 'french': 'Guanteoeste',
                           'german': 'Guanteoeste', 'italian': 'Guanteoeste', 'japanese': 'グアンテオステ',
                           'korean': '구안테오에스치', 'polish': 'Guanteoeste', 'russian': 'Гуантеоэсте',
                           'spanish': 'Guanteoeste', 'taiwanese': '關提歐伊斯特'},
                   20386: {'chinese': '皮帕班巴', 'english': 'Pipabamba', 'french': 'Pipabamba', 'german': 'Pipabamba',
                           'italian': 'Pipabamba', 'japanese': 'ピパバンバ', 'korean': '피파밤바', 'polish': 'Pipabamba',
                           'russian': 'Пипабамба', 'spanish': 'Pipabamba', 'taiwanese': '皮帕班巴'},
                   20387: {'chinese': '杜库潘', 'english': 'Tucupán', 'french': 'Tucupán', 'german': 'Tucupán',
                           'italian': 'Tucupán', 'japanese': 'トゥクパン', 'korean': '투쿠팡', 'polish': 'Tucupán',
                           'russian': 'Тукупан', 'spanish': 'Tucupán', 'taiwanese': '杜庫潘'},
                   20388: {'chinese': '克尔可纳', 'english': 'Corcona', 'french': 'Corcona', 'german': 'Corcona',
                           'italian': 'Corcona', 'japanese': 'コルコーナ', 'korean': '코르코나', 'polish': 'Corcona',
                           'russian': 'Коркона', 'spanish': 'Corcona', 'taiwanese': '克爾可納'},
                   20389: {'chinese': '哥斯大迪贾达', 'english': 'Costa Delgada', 'french': 'Costa Delgada',
                           'german': 'Costa Delgada', 'italian': 'Costa Delgada', 'japanese': 'コスタ・デルガーダ',
                           'korean': '코스타 데우가다', 'polish': 'Costa Delgada', 'russian': 'Кошта Делгада',
                           'spanish': 'Costa Delgada', 'taiwanese': '哥斯大迪賈達'},
                   20390: {'chinese': '多巴西亚', 'english': 'Do Bahía', 'french': 'Do Bahía', 'german': 'Do Bahía',
                           'italian': 'Do Bahía', 'japanese': 'ドゥ・バイア', 'korean': '두 바이아', 'polish': 'Do Bahía',
                           'russian': 'До Баия', 'spanish': 'Do Bahía', 'taiwanese': '多巴西亞'},
                   20391: {'chinese': '品加甘地斯', 'english': 'Pinchacantis', 'french': 'Pinchacantis',
                           'german': 'Pinchacantis', 'italian': 'Pinchacantis', 'japanese': 'ピンチャカンチース',
                           'korean': '핀샤칸치스', 'polish': 'Pinchacantis', 'russian': 'Пинкакантис',
                           'spanish': 'Pinchacantis', 'taiwanese': '品加甘地斯'},
                   20392: {'chinese': '罗敦敦伊亚', 'english': 'Rodondonia', 'french': 'Rodondonia', 'german': 'Rodondonia',
                           'italian': 'Rodondonia', 'japanese': 'ロドンドニア', 'korean': '호돈도니아', 'polish': 'Rodondonia',
                           'russian': 'Родондония', 'spanish': 'Rodondonia', 'taiwanese': '羅敦敦伊亞'},
                   20393: {'chinese': '阿伊亚普雷塔', 'english': 'Areia Preta', 'french': 'Areia Preta',
                           'german': 'Areia Preta', 'italian': 'Areia Preta', 'japanese': 'アレイア・プレタ',
                           'korean': '아레이아 프레타', 'polish': 'Areia Preta', 'russian': 'Арея Прету',
                           'spanish': 'Areia Preta', 'taiwanese': '阿伊亞普雷塔'},
                   20394: {'chinese': '瓦卡切契斯', 'english': 'Vacachinchis', 'french': 'Vacachinchis',
                           'german': 'Vacachinchis', 'italian': 'Vacachinchis', 'japanese': 'ヴァーカチンチス',
                           'korean': '바카신시스', 'polish': 'Vacachinchis', 'russian': 'Вакакинкис',
                           'spanish': 'Vacachinchis', 'taiwanese': '瓦卡切契斯'},
                   20395: {'chinese': '卡拉欧斯', 'english': 'Calaos', 'french': 'Calaos', 'german': 'Calaos',
                           'italian': 'Calaos', 'japanese': 'カラオス', 'korean': '칼라우스', 'polish': 'Calaos',
                           'russian': 'Калаос', 'spanish': 'Calaos', 'taiwanese': '卡拉歐斯'},
                   20396: {'chinese': '玛利洛', 'english': 'Marillo', 'french': 'Marillo', 'german': 'Marillo',
                           'italian': 'Marillo', 'japanese': 'マリーオ', 'korean': '마릴루', 'polish': 'Marillo',
                           'russian': 'Марильо', 'spanish': 'Marillo', 'taiwanese': '瑪利洛'},
                   20397: {'chinese': '瓜亚地', 'english': 'Guayatí', 'french': 'Guayatí', 'german': 'Guayatí',
                           'italian': 'Guayatí', 'japanese': 'グアジャティ', 'korean': '구아야치', 'polish': 'Guayatí',
                           'russian': 'Гвайяти', 'spanish': 'Guayatí', 'taiwanese': '瓜亞地'},
                   20398: {'chinese': '圣多培', 'english': 'Santopé', 'french': 'Santopé', 'german': 'Santopé',
                           'italian': 'Santopé', 'japanese': 'サントペ', 'korean': '산토페', 'polish': 'Santopé',
                           'russian': 'Сантопе', 'spanish': 'Santopé', 'taiwanese': '聖多培'},
                   20399: {'chinese': '亚拉卡固', 'english': 'Jaracagüe', 'french': 'Jaracagüe', 'german': 'Jaracagüe',
                           'italian': 'Jaracagüe', 'japanese': 'ハラカゲ', 'korean': '자라카기', 'polish': 'Jaracagüe',
                           'russian': 'Харакагуэ', 'spanish': 'Jaracagüe', 'taiwanese': '亞拉卡固'},
                   20400: {'chinese': '欧亚尔欧罗', 'english': 'Ojaruro', 'french': 'Ojaruro', 'german': 'Ojaruro',
                           'italian': 'Ojaruro', 'japanese': 'オジャルロ', 'korean': '오자루루', 'polish': 'Ojaruro',
                           'russian': 'Охаруро', 'spanish': 'Ojaruro', 'taiwanese': '歐亞爾歐羅'},
                   20401: {'chinese': '拉阿亚契', 'english': 'La Ayachí', 'french': 'La Ayachí', 'german': 'La Ayachí',
                           'italian': 'La Ayachí', 'japanese': 'ラ・アヤチ', 'korean': '라 아야시', 'polish': 'La Ayachí',
                           'russian': 'Ла Айячи', 'spanish': 'La Ayachí', 'taiwanese': '拉阿亞契'},
                   20402: {'chinese': '特恩贾德拉哈亚', 'english': 'Tangá de la Haya', 'french': 'Tangá de la Haya',
                           'german': 'Tangá de la Haya', 'italian': 'Tangá de la Haya', 'japanese': 'タンガ・デ・ラ・アヤ',
                           'korean': '탕가 지 라 아야', 'polish': 'Tangá de la Haya', 'russian': 'Танга де ла Гаага',
                           'spanish': 'Tangá de la Haya', 'taiwanese': '特恩賈德拉哈亞'},
                   20403: {'chinese': '里欧拉尔托', 'english': 'Rioralto', 'french': 'Rioralto', 'german': 'Rioralto',
                           'italian': 'Rioralto', 'japanese': 'リオラルト', 'korean': '히오라우투', 'polish': 'Rioralto',
                           'russian': 'Риоральто', 'spanish': 'Rioralto', 'taiwanese': '里歐拉爾托'},
                   20404: {'chinese': '波路路', 'english': 'Polulu', 'french': 'Polulu', 'german': 'Polulu',
                           'italian': 'Polulu', 'japanese': 'ポルル', 'korean': '폴룰루', 'polish': 'Polulu',
                           'russian': 'Полулу', 'spanish': 'Polulu', 'taiwanese': '波路路'},
                   20405: {'chinese': '圣多罗姆', 'english': 'Santolomé', 'french': 'Santolomé', 'german': 'Santolomé',
                           'italian': 'Santolomé', 'japanese': 'サントロメ', 'korean': '산톨로메', 'polish': 'Santolomé',
                           'russian': 'Сантоломе', 'spanish': 'Santolomé', 'taiwanese': '聖多羅姆'},
                   20406: {'chinese': '帕尔玛祖阿托', 'english': 'Palma Zuato', 'french': 'Palma Zuato',
                           'german': 'Palma Zuato', 'italian': 'Palma Zuato', 'japanese': 'パルマ・ズアート',
                           'korean': '파우마 주아투', 'polish': 'Palma Zuato', 'russian': 'Пальма Суато',
                           'spanish': 'Palma Zuato', 'taiwanese': '帕爾瑪祖阿托'},
                   20407: {'chinese': '欧纳托', 'english': 'Onato', 'french': 'Onato', 'german': 'Onato',
                           'italian': 'Onato', 'japanese': 'オニャーテ', 'korean': '오나투', 'polish': 'Onato',
                           'russian': 'Онато', 'spanish': 'Onato', 'taiwanese': '歐納托'},
                   20408: {'chinese': '尔伊斯皮诺', 'english': 'El Espino', 'french': 'El Espino', 'german': 'El Espino',
                           'italian': 'El Espino', 'japanese': 'エル・エスピーノ', 'korean': '이우 이스피누', 'polish': 'El Espino',
                           'russian': 'Эль Эспино', 'spanish': 'El Espino', 'taiwanese': '爾伊斯皮諾'},
                   20409: {'chinese': '拉霍切尔拉', 'english': 'La Horchella', 'french': 'La Horchella',
                           'german': 'La Horchella', 'italian': 'La Horchella', 'japanese': 'ラ・オルエイヤ',
                           'korean': '라 오르셸라', 'polish': 'La Horchella', 'russian': 'Ла Орчелья',
                           'spanish': 'La Horchella', 'taiwanese': '拉霍切爾拉'},
                   20410: {'chinese': '阿克德亚魁尔', 'english': 'Arc de Yagual', 'french': 'Arc de Yagual',
                           'german': 'Arc de Yagual', 'italian': 'Arc de Yagual', 'japanese': 'アルク・デ・ジャグアル',
                           'korean': '아르크 지 야구아우', 'polish': 'Arc de Yagual', 'russian': 'Арк де Ягуаль',
                           'spanish': 'Arc de Yagual', 'taiwanese': '阿克德亞魁爾'},
                   20411: {'chinese': '古拉西亚', 'english': 'Grasía', 'french': 'Grasía', 'german': 'Grasía',
                           'italian': 'Grasía', 'japanese': 'グラシャ', 'korean': '그라지아', 'polish': 'Grasía',
                           'russian': 'Грасиа', 'spanish': 'Grasía', 'taiwanese': '古拉西亞'},
                   20412: {'chinese': '塔卡雷', 'english': 'Tacaray', 'french': 'Tacaray', 'german': 'Tacaray',
                           'italian': 'Tacaray', 'japanese': 'タカライ', 'korean': '타카라이', 'polish': 'Tacaray',
                           'russian': 'Такарай', 'spanish': 'Tacaray', 'taiwanese': '塔卡雷'},
                   20413: {'chinese': '西寇鲁伊高', 'english': 'Higoluego', 'french': 'Higoluego', 'german': 'Higoluego',
                           'italian': 'Higoluego', 'japanese': 'イゴルエゴ', 'korean': '이골루에구', 'polish': 'Higoluego',
                           'russian': 'Иголуэго', 'spanish': 'Higoluego', 'taiwanese': '西寇魯伊高'},
                   20414: {'chinese': '杜皮里托', 'english': 'Tupirito', 'french': 'Tupirito', 'german': 'Tupirito',
                           'italian': 'Tupirito', 'japanese': 'トゥピーリト', 'korean': '투피리투', 'polish': 'Tupirito',
                           'russian': 'Тупирито', 'spanish': 'Tupirito', 'taiwanese': '杜皮里托'},
                   20415: {'chinese': '拉瓜瑞达', 'english': 'La Guarida', 'french': 'La Guarida', 'german': 'La Guarida',
                           'italian': 'La Guarida', 'japanese': 'ラ・グアリダ', 'korean': '라 구아리다', 'polish': 'La Guarida',
                           'russian': 'Ла Гварида', 'spanish': 'La Guarida', 'taiwanese': '拉瓜瑞達'},
                   20416: {'chinese': '卡寇梅拉', 'english': 'Kakomera', 'french': 'Kakomera', 'german': 'Kakomera',
                           'italian': 'Kakomera', 'japanese': 'カコメラ', 'korean': '카코메라', 'polish': 'Kakomera',
                           'russian': 'Какомера', 'spanish': 'Kakomera', 'taiwanese': '卡寇梅拉'},
                   20417: {'chinese': '伊斯品诺可', 'english': 'Espinoço', 'french': 'Espinoço', 'german': 'Espinoço',
                           'italian': 'Espinoço', 'japanese': 'エスピニョコ', 'korean': '이스피노수', 'polish': 'Espinoço',
                           'russian': 'Эспиносу', 'spanish': 'Espinoço', 'taiwanese': '伊斯品諾可'},
                   20418: {'chinese': '迪瓜兰', 'english': 'Tiguarán', 'french': 'Tiguarán', 'german': 'Tiguarán',
                           'italian': 'Tiguarán', 'japanese': 'ティグアラン', 'korean': '치구아랑', 'polish': 'Tiguarán',
                           'russian': 'Тигваран', 'spanish': 'Tiguarán', 'taiwanese': '迪瓜蘭'},
                   20419: {'chinese': '瓦拉勒古拉', 'english': 'Vallalegra', 'french': 'Vallalegra', 'german': 'Vallalegra',
                           'italian': 'Vallalegra', 'japanese': 'ヴァリャレグラ', 'korean': '발랄레그라', 'polish': 'Vallalegra',
                           'russian': 'Вальялегра', 'spanish': 'Vallalegra', 'taiwanese': '瓦拉勒古拉'},
                   20420: {'chinese': '弗兰契克斯', 'english': 'Fechiques', 'french': 'Fechiques', 'german': 'Fechiques',
                           'italian': 'Fechiques', 'japanese': 'フェシケース', 'korean': '페시케스', 'polish': 'Fechiques',
                           'russian': 'Фечикес', 'spanish': 'Fechiques', 'taiwanese': '弗蘭契克斯'},
                   20421: {'chinese': '艾尔布费洛', 'english': 'El Bufero', 'french': 'El Bufero', 'german': 'El Bufero',
                           'italian': 'El Bufero', 'japanese': 'エル・ブフェーロ', 'korean': '이우 부페루', 'polish': 'El Bufero',
                           'russian': 'Эль Буферо', 'spanish': 'El Bufero', 'taiwanese': '艾爾布費洛'},
                   20422: {'chinese': '特沛古兰德', 'english': 'Tepe Grande', 'french': 'Tepe Grande',
                           'german': 'Tepe Grande', 'italian': 'Tepe Grande', 'japanese': 'テペ・グランデ', 'korean': '테피 그란지',
                           'polish': 'Tepe Grande', 'russian': 'Тепе Гранде', 'spanish': 'Tepe Grande',
                           'taiwanese': '特沛古蘭德'},
                   20423: {'chinese': '卡兰席亚', 'english': 'Calensia', 'french': 'Calensia', 'german': 'Calensia',
                           'italian': 'Calensia', 'japanese': 'カレンシア', 'korean': '칼렌시아', 'polish': 'Calensia',
                           'russian': 'Каленсия', 'spanish': 'Calensia', 'taiwanese': '卡蘭席亞'},
                   20424: {'chinese': '穆阿', 'english': 'Múa', 'french': 'Múa', 'german': 'Múa', 'italian': 'Múa',
                           'japanese': 'ムア', 'korean': '무아', 'polish': 'Múa', 'russian': 'Муа', 'spanish': 'Múa',
                           'taiwanese': '穆阿'},
                   20425: {'chinese': '波克多罗', 'english': 'Poçodoro', 'french': 'Poçodoro', 'german': 'Poçodoro',
                           'italian': 'Poçodoro', 'japanese': 'ポッソドーロ', 'korean': '포소도루', 'polish': 'Poçodoro',
                           'russian': 'Посодору', 'spanish': 'Poçodoro', 'taiwanese': '波克多羅'},
                   20426: {'chinese': '法拉明郭', 'english': 'Falamingo', 'french': 'Falamingo', 'german': 'Falamingo',
                           'italian': 'Falamingo', 'japanese': 'ファラミンゴ', 'korean': '팔라밍구', 'polish': 'Falamingo',
                           'russian': 'Фаламинго', 'spanish': 'Falamingo', 'taiwanese': '法拉明郭'},
                   20427: {'chinese': '梅里迪塔', 'english': 'Meridita', 'french': 'Meridita', 'german': 'Meridita',
                           'italian': 'Meridita', 'japanese': 'メリディータ', 'korean': '메리지타', 'polish': 'Meridita',
                           'russian': 'Меридита', 'spanish': 'Meridita', 'taiwanese': '梅里迪塔'},
                   20428: {'chinese': '莫拉科劳', 'english': 'Morracolao', 'french': 'Morracolao', 'german': 'Morracolao',
                           'italian': 'Morracolao', 'japanese': 'モッラコラオ', 'korean': '모하콜라우', 'polish': 'Morracolao',
                           'russian': 'Морраколао', 'spanish': 'Morracolao', 'taiwanese': '莫拉科勞'},
                   20429: {'chinese': '普拉卡契卡', 'english': 'Placachica', 'french': 'Placachica', 'german': 'Placachica',
                           'italian': 'Placachica', 'japanese': 'プラカチカ', 'korean': '플라카시카', 'polish': 'Placachica',
                           'russian': 'Плакачика', 'spanish': 'Placachica', 'taiwanese': '普拉卡契卡'},
                   20430: {'chinese': '约安尼托', 'english': 'Juaneto', 'french': 'Juaneto', 'german': 'Juaneto',
                           'italian': 'Juaneto', 'japanese': 'フアネート', 'korean': '주아네투', 'polish': 'Juaneto',
                           'russian': 'Хуането', 'spanish': 'Juaneto', 'taiwanese': '約安尼托'},
                   20431: {'chinese': '拉鲁瓦', 'english': 'Larruva', 'french': 'Larruva', 'german': 'Larruva',
                           'italian': 'Larruva', 'japanese': 'ラルーヴァ', 'korean': '라후바', 'polish': 'Larruva',
                           'russian': 'Ларрува', 'spanish': 'Larruva', 'taiwanese': '拉魯瓦'},
                   20432: {'chinese': '卡契恩魁斯', 'english': 'Cachiniques', 'french': 'Cachiniques',
                           'german': 'Cachiniques', 'italian': 'Cachiniques', 'japanese': 'カシニケス', 'korean': '카시니케스',
                           'polish': 'Cachiniques', 'russian': 'Качиникес', 'spanish': 'Cachiniques',
                           'taiwanese': '卡契恩魁斯'},
                   20433: {'chinese': '拉布尔纳卡', 'english': 'La Burinaca', 'french': 'La Burinaca',
                           'german': 'La Burinaca', 'italian': 'La Burinaca', 'japanese': 'ラ・ブリナーカ', 'korean': '라 부리나카',
                           'polish': 'La Burinaca', 'russian': 'Ла Буринака', 'spanish': 'La Burinaca',
                           'taiwanese': '拉布林納卡'},
                   20434: {'chinese': '薛尔拜尔斯', 'english': 'Surebiales', 'french': 'Surebiales', 'german': 'Surebiales',
                           'italian': 'Surebiales', 'japanese': 'スレビアレス', 'korean': '수레비알리스', 'polish': 'Surebiales',
                           'russian': 'Суребиалес', 'spanish': 'Surebiales', 'taiwanese': '薛爾拜爾斯'},
                   20435: {'chinese': '弗特苏阿达', 'english': 'Forte Suatá', 'french': 'Forte Suatá',
                           'german': 'Forte Suatá', 'italian': 'Forte Suatá', 'japanese': 'フォールテ・スアタ',
                           'korean': '포르치 수아타', 'polish': 'Forte Suatá', 'russian': 'Форте Суата',
                           'spanish': 'Forte Suatá', 'taiwanese': '弗特蘇阿達'},
                   20436: {'chinese': '约亚诺', 'english': 'Yoyano', 'french': 'Yoyano', 'german': 'Yoyano',
                           'italian': 'Yoyano', 'japanese': 'ヨヤーノ', 'korean': '요야누', 'polish': 'Yoyano',
                           'russian': 'Йояно', 'spanish': 'Yoyano', 'taiwanese': '約亞諾'},
                   20437: {'chinese': '契提亚哥', 'english': 'Chantiago', 'french': 'Chantiago', 'german': 'Chantiago',
                           'italian': 'Chantiago', 'japanese': 'チャンティアゴ', 'korean': '샨치아구', 'polish': 'Chantiago',
                           'russian': 'Чантьяго', 'spanish': 'Chantiago', 'taiwanese': '契提亞哥'},
                   20438: {'chinese': '波魁敦', 'english': 'Boquetón', 'french': 'Boquetón', 'german': 'Boquetón',
                           'italian': 'Boquetón', 'japanese': 'ボケトン', 'korean': '보케통', 'polish': 'Boquetón',
                           'russian': 'Бокетон', 'spanish': 'Boquetón', 'taiwanese': '波魁敦'},
                   20439: {'chinese': '维约郭里诺', 'english': 'Viejo Gorrino', 'french': 'Viejo Gorrino',
                           'german': 'Viejo Gorrino', 'italian': 'Viejo Gorrino', 'japanese': 'ヴィエホ・ゴリーノ',
                           'korean': '비에주 고히누', 'polish': 'Viejo Gorrino', 'russian': 'Вьехо Горрино',
                           'spanish': 'Viejo Gorrino', 'taiwanese': '維約郭里諾'},
                   20440: {'chinese': '契魁林敦', 'english': 'Chiquirritón', 'french': 'Chiquirritón',
                           'german': 'Chiquirritón', 'italian': 'Chiquirritón', 'japanese': 'チキリトン', 'korean': '시키히통',
                           'polish': 'Chiquirritón', 'russian': 'Чикирритон', 'spanish': 'Chiquirritón',
                           'taiwanese': '契魁林敦'},
                   20441: {'chinese': '克鲁兹阿米塔', 'english': 'Cruz Amita', 'french': 'Cruz Amita', 'german': 'Cruz Amita',
                           'italian': 'Cruz Amita', 'japanese': 'クルース・アミタ', 'korean': '크루스 아미타', 'polish': 'Cruz Amita',
                           'russian': 'Крус Амита', 'spanish': 'Cruz Amita', 'taiwanese': '克魯茲阿米塔'},
                   20442: {'chinese': '伊纳祖可', 'english': 'Inazuco', 'french': 'Inazuco', 'german': 'Inazuco',
                           'italian': 'Inazuco', 'japanese': 'イナシコ', 'korean': '이나주쿠', 'polish': 'Inazuco',
                           'russian': 'Иназуку', 'spanish': 'Inazuco', 'taiwanese': '伊納祖可'},
                   20443: {'chinese': '拉法瓜瑟斯', 'english': 'Rafagaces', 'french': 'Rafagaces', 'german': 'Rafagaces',
                           'italian': 'Rafagaces', 'japanese': 'ラファガセス', 'korean': '하파가시스', 'polish': 'Rafagaces',
                           'russian': 'Рафагасес', 'spanish': 'Rafagaces', 'taiwanese': '拉法瓜瑟斯'},
                   20444: {'chinese': '波克托', 'english': 'Bocoto', 'french': 'Bocoto', 'german': 'Bocoto',
                           'italian': 'Bocoto', 'japanese': 'ボコト', 'korean': '보코토', 'polish': 'Bocoto',
                           'russian': 'Бокото', 'spanish': 'Bocoto', 'taiwanese': '波克托'},
                   20445: {'chinese': '阿瓜卡特', 'english': 'Aguacate', 'french': 'Aguacate', 'german': 'Aguacate',
                           'italian': 'Aguacate', 'japanese': 'アグアカテ', 'korean': '아구아카치', 'polish': 'Aguacate',
                           'russian': 'Агуакате', 'spanish': 'Aguacate', 'taiwanese': '阿瓜卡特'},
                   20446: {'chinese': '勒耶亚', 'english': 'Lleyeja', 'french': 'Lleyeja', 'german': 'Lleyeja',
                           'italian': 'Lleyeja', 'japanese': 'レイエイヤ', 'korean': '예예하', 'polish': 'Lleyeja',
                           'russian': 'Льейеха', 'spanish': 'Lleyeja', 'taiwanese': '勒耶亞'},
                   20447: {'chinese': '克索罗科托', 'english': 'Xolocorto', 'french': 'Xolocorto', 'german': 'Xolocorto',
                           'italian': 'Xolocorto', 'japanese': 'ソロコルト', 'korean': '숄로코르투', 'polish': 'Xolocorto',
                           'russian': 'Шолокорту', 'spanish': 'Xolocorto', 'taiwanese': '克索羅科托'},
                   20448: {'chinese': '塔卡拉霍帕斯', 'english': 'Tacarahuepas', 'french': 'Tacarahuepas',
                           'german': 'Tacarahuepas', 'italian': 'Tacarahuepas', 'japanese': 'タカラフエパス',
                           'korean': '타카라우에파스', 'polish': 'Tacarahuepas', 'russian': 'Такарауэпас',
                           'spanish': 'Tacarahuepas', 'taiwanese': '塔卡拉霍帕斯'},
                   20449: {'chinese': '圣塔涅霍', 'english': 'Santaneho', 'french': 'Santaneho', 'german': 'Santaneho',
                           'italian': 'Santaneho', 'japanese': 'サンタネホ', 'korean': '산타네우', 'polish': 'Santaneho',
                           'russian': 'Сантанео', 'spanish': 'Santaneho', 'taiwanese': '聖塔涅霍'},
                   20450: {'chinese': '库兰特普雷托', 'english': 'Curente Preto', 'french': 'Curente Preto',
                           'german': 'Curente Preto', 'italian': 'Curente Preto', 'japanese': 'クレンテ・プレート',
                           'korean': '쿠렌치 프레투', 'polish': 'Curente Preto', 'russian': 'Куренте Прето',
                           'spanish': 'Curente Preto', 'taiwanese': '庫蘭特普雷托'},
                   20451: {'chinese': '阿维尔梅哈', 'english': 'A Vermelha', 'french': 'A Vermelha', 'german': 'A Vermelha',
                           'italian': 'A Vermelha', 'japanese': 'ア・ヴェルメイア', 'korean': '아 베르말랴', 'polish': 'A Vermelha',
                           'russian': 'А Вермелья', 'spanish': 'A Vermelha', 'taiwanese': '阿維爾梅哈'},
                   20452: {'chinese': '古拉卡欧', 'english': 'Graçau', 'french': 'Graçau', 'german': 'Graçau',
                           'italian': 'Graçau', 'japanese': 'グラサウ', 'korean': '그라사우', 'polish': 'Graçau',
                           'russian': 'Грасау', 'spanish': 'Graçau', 'taiwanese': '古拉卡歐'},
                   20453: {'chinese': '多特瑞辛哈', 'english': 'Do Teresinha', 'french': 'Do Teresinha',
                           'german': 'Do Teresinha', 'italian': 'Do Teresinha', 'japanese': 'ドゥ・テレジニア',
                           'korean': '두 테레지냐', 'polish': 'Do Teresinha', 'russian': 'До Терезинья',
                           'spanish': 'Do Teresinha', 'taiwanese': '多特瑞辛哈'},
                   20454: {'chinese': '可曲丘', 'english': 'Cuchucho', 'french': 'Cuchucho', 'german': 'Cuchucho',
                           'italian': 'Cuchucho', 'japanese': 'コチョーチョ', 'korean': '쿠슈슈', 'polish': 'Cuchucho',
                           'russian': 'Кучучо', 'spanish': 'Cuchucho', 'taiwanese': '可曲丘'},
                   20455: {'chinese': '艾尔札拉欧', 'english': 'El Zarao', 'french': 'El Zarao', 'german': 'El Zarao',
                           'italian': 'El Zarao', 'japanese': 'エル・ザラオ', 'korean': '이우 자라우', 'polish': 'El Zarao',
                           'russian': 'Эль Сарао', 'spanish': 'El Zarao', 'taiwanese': '艾爾札拉歐'},
                   20456: {'chinese': '艾尔巴薛恩', 'english': 'El Bastión', 'french': 'El Bastión', 'german': 'El Bastión',
                           'italian': 'El Bastión', 'japanese': 'エル・バスティオン', 'korean': '이우 바스치옹',
                           'polish': 'El Bastión', 'russian': 'Эль Бастион', 'spanish': 'El Bastión',
                           'taiwanese': '艾爾巴薛恩'},
                   20457: {'chinese': '玛尔瑟利塔斯', 'english': 'Marcelitas', 'french': 'Marcelitas', 'german': 'Marcelitas',
                           'italian': 'Marcelitas', 'japanese': 'マルセリータス', 'korean': '마르셀리타스', 'polish': 'Marcelitas',
                           'russian': 'Марселитас', 'spanish': 'Marcelitas', 'taiwanese': '瑪爾瑟利塔斯'},
                   23284: {'chinese': '阿比百由赛德', 'english': 'Abyi Bayasayd', 'french': 'Abyi Bayasayd',
                           'german': 'Abyi Bayasayd', 'italian': 'Abyi Bayasayd', 'japanese': 'アブイ・バヤサイド',
                           'korean': '아비 바이야사이드', 'polish': 'Abyi Bayasayd', 'russian': 'Аби-Баясайд',
                           'spanish': 'Abyi Bayasayd', 'taiwanese': '阿比百由賽德'},
                   23289: {'chinese': '桑兹', 'english': 'Zounds', 'french': 'Zounds', 'german': 'Zounds',
                           'italian': 'Zounds', 'japanese': 'ゾーンズ', 'korean': '자운즈', 'polish': 'Zounds',
                           'russian': 'Зоундс', 'spanish': 'Zounds', 'taiwanese': '桑茲'},
                   23290: {'chinese': '温尤可米洪', 'english': 'Wenya Komihoam', 'french': 'Wenya Komihoam',
                           'german': 'Wenya Komihoam', 'italian': 'Wenya Komihoam', 'japanese': 'ウェンヤ・カミホーム',
                           'korean': '웨냐 코미홈', 'polish': 'Wenya Komihoam', 'russian': 'Венья-Комихоам',
                           'spanish': 'Wenya Komihoam', 'taiwanese': '溫尤可米洪'},
                   23291: {'chinese': '威凯特伯斯', 'english': 'Welkite Debos', 'french': 'Welkite Debos',
                           'german': 'Welkite Debos', 'italian': 'Welkite Debos', 'japanese': 'ウェルカイト・ダボス',
                           'korean': '윌카이트 디보스', 'polish': 'Welkite Debos', 'russian': 'Вельките-Дебос',
                           'spanish': 'Welkite Debos', 'taiwanese': '威凱特伯斯'},
                   23292: {'chinese': '百乐甘姆', 'english': 'Bayde Geyme', 'french': 'Bayde Geyme',
                           'german': 'Bayde Geyme', 'italian': 'Bayde Geyme', 'japanese': 'バイダ・ゲイム', 'korean': '바이드 게임',
                           'polish': 'Bayde Geyme', 'russian': 'Байде-Гэйме', 'spanish': 'Bayde Geyme',
                           'taiwanese': '百樂甘姆'},
                   23293: {'chinese': '艾菲索希克', 'english': 'Ifyil Sosik', 'french': 'Ifyil Sosik',
                           'german': 'Ifyil Sosik', 'italian': 'Ifyil Sosik', 'japanese': 'イフィル・ソシク',
                           'korean': '아이필 소시크', 'polish': 'Ifyil Sosik', 'russian': 'Ифил-Сосик',
                           'spanish': 'Ifyil Sosik', 'taiwanese': '艾菲索希克'},
                   23294: {'chinese': '波特阿必提', 'english': 'Port Abyi Lyti', 'french': 'Port Abyi Lyti',
                           'german': 'Port Abyi Lyti', 'italian': 'Port Abyi Lyti', 'japanese': 'ポート・アブイ・リティ',
                           'korean': '포트 아비 리티', 'polish': 'Port Abyi Lyti', 'russian': 'Порт Аби-Лити',
                           'spanish': 'Port Abyi Lyti', 'taiwanese': '波特阿必提'},
                   23295: {'chinese': '瑟解玛德银', 'english': 'Tsegaye Medhin', 'french': 'Tsegaye Medhin',
                           'german': 'Tsegaye Medhin', 'italian': 'Tsegaye Medhin', 'japanese': 'ツェガエ・メディン',
                           'korean': '체가예 메드힌', 'polish': 'Tsegaye Medhin', 'russian': 'Цегайе-Медин',
                           'spanish': 'Tsegaye Medhin', 'taiwanese': '瑟解瑪德銀'},
                   23296: {'chinese': '玛希特瑞德瑞撒', 'english': 'Masiteri Deressa', 'french': 'Masiteri Deressa',
                           'german': 'Masiteri Deressa', 'italian': 'Masiteri Deressa', 'japanese': 'マシテリ・デレッサ',
                           'korean': '마시테리 데레사', 'polish': 'Masiteri Deressa', 'russian': 'Маситери-Дересса',
                           'spanish': 'Masiteri Deressa', 'taiwanese': '瑪希特瑞德瑞撒'},
                   23297: {'chinese': '丹巴梅尼德', 'english': 'Dunbar Menideri', 'french': 'Dunbar Menideri',
                           'german': 'Dunbar Menideri', 'italian': 'Dunbar Menideri', 'japanese': 'ダンバー・メニデリ',
                           'korean': '던바 메니데리', 'polish': 'Dunbar Menideri', 'russian': 'Дунбар-Менидери',
                           'spanish': 'Dunbar Menideri', 'taiwanese': '丹巴梅尼德'},
                   23321: {'chinese': '叶拉拉颠涅波', 'english': 'Yilalla Denebo', 'french': 'Yilalla Denebo',
                           'german': 'Yilalla Denebo', 'italian': 'Yilalla Denebo', 'japanese': 'イラーラ・デネボ',
                           'korean': '일랄라 데네보', 'polish': 'Yilalla Denebo', 'russian': 'Йилалла-Денебо',
                           'spanish': 'Yilalla Denebo', 'taiwanese': '葉拉拉顛涅波'},
                   23322: {'chinese': '阿兰姆斯海', 'english': 'Alemtsehay', 'french': 'Alemtsehay', 'german': 'Alemtsehay',
                           'italian': 'Alemtsehay', 'japanese': 'アレムツェヘイ', 'korean': '알렘체하이', 'polish': 'Alemtsehay',
                           'russian': 'Алемтсехай', 'spanish': 'Alemtsehay', 'taiwanese': '阿蘭姆斯海'},
                   23323: {'chinese': '盖布拉汉娜', 'english': 'Gabre Hanna', 'french': 'Gabre Hanna',
                           'german': 'Gabre Hanna', 'italian': 'Gabre Hanna', 'japanese': 'ガブレ・ハンナ', 'korean': '가브레 해나',
                           'polish': 'Gabre Hanna', 'russian': 'Габрэ-Ханна', 'spanish': 'Gabre Hanna',
                           'taiwanese': '蓋布拉漢娜'},
                   23324: {'chinese': '多尤瑞瑟曲', 'english': 'Doyur Reesurtsh', 'french': 'Doyur Reesurtsh',
                           'german': 'Doyur Reesurtsh', 'italian': 'Doyur Reesurtsh', 'japanese': 'ドユール・リーサーチュ',
                           'korean': '도여르 리서트쉬', 'polish': 'Doyur Reesurtsh', 'russian': 'Доюр-Реесурч',
                           'spanish': 'Doyur Reesurtsh', 'taiwanese': '多尤瑞瑟曲'},
                   23325: {'chinese': '胡瑞慈第埃兹能', 'english': "Hoorayts De'eznamz", 'french': "Hoorayts De'eznamz",
                           'german': "Hoorayts De'eznamz", 'italian': "Hoorayts De'eznamz", 'japanese': 'フーライツ・ディーズネムズ',
                           'korean': '후라이츠 디즈넴즈', 'polish': "Hoorayts De'eznamz", 'russian': 'Хурайц-Дизнамз',
                           'spanish': "Hoorayts De'eznamz", 'taiwanese': '胡瑞慈第埃茲能'},
                   23326: {'chinese': '撒拉梅塔梅瑞恩', 'english': 'Salameta Maryam', 'french': 'Salameta Maryam',
                           'german': 'Salameta Maryam', 'italian': 'Salameta Maryam', 'japanese': 'サラメタ・マリアム',
                           'korean': '살라메타 마리엄', 'polish': 'Salameta Maryam', 'russian': 'Саламета-Марьям',
                           'spanish': 'Salameta Maryam', 'taiwanese': '撒拉梅塔梅瑞恩'},
                   23327: {'chinese': '那赞麻威德彼', 'english': "Nas'amawedabiya", 'french': "Nas' amawedabiya",
                           'german': "Nas'amawedabiya", 'italian': "Nas'amawedabiya", 'japanese': 'ナス・アマウェダビヤ',
                           'korean': '나스 아마웨다비야', 'polish': "Nas'amawedabiya", 'russian': 'Нас-Амаведабия',
                           'spanish': "Nas'amawedabiya", 'taiwanese': '那讚麻威德彼'},
                   23328: {'chinese': '阿米博蕾', 'english': 'Amebalaye', 'french': 'Amebalaye', 'german': 'Amebalaye',
                           'italian': 'Amebalaye', 'japanese': 'アメバライェ', 'korean': '아메발라예', 'polish': 'Amebalaye',
                           'russian': 'Амебалайе', 'spanish': 'Amebalaye', 'taiwanese': '阿米博蕾'},
                   23329: {'chinese': '阿立克廷', 'english': "Eli'keteme", 'french': "Eli'keteme", 'german': "Eli'keteme",
                           'italian': "Eli'keteme", 'japanese': 'エリケテメ', 'korean': '엘리케테메', 'polish': "Eli'keteme",
                           'russian': 'Эли-Кетеме', 'spanish': "Eli'keteme", 'taiwanese': '阿立克廷'},
                   23330: {'chinese': '瑞吉米塔拉拉', 'english': 'Ragemetarara', 'french': 'Ragemetarara',
                           'german': 'Ragemetarara', 'italian': 'Ragemetarara', 'japanese': 'ラゲメタララ',
                           'korean': '라거메타라라', 'polish': 'Ragemetarara', 'russian': 'Раджметарара',
                           'spanish': 'Ragemetarara', 'taiwanese': '瑞吉米塔菈菈'},
                   23331: {'chinese': '应赛特内姆西亚', 'english': 'Insutnaym Hea', 'french': 'Insutnaym Hea',
                           'german': 'Insutnaym Hea', 'italian': 'Insutnaym Hea', 'japanese': 'インサットネイム・ヒア',
                           'korean': '인수트나임 헤아', 'polish': 'Insutnaym Hea', 'russian': 'Инсутнайм-Хеа',
                           'spanish': 'Insutnaym Hea', 'taiwanese': '應賽特內姆西亞'},
                   23332: {'chinese': '巴巴耶纳', 'english': 'Baba Yaena', 'french': 'Baba Yaena', 'german': 'Baba Yaena',
                           'italian': 'Baba Yaena', 'japanese': 'ババ・ヤエナ', 'korean': '바바 예나', 'polish': 'Baba Yaena',
                           'russian': 'Баба-Йаена', 'spanish': 'Baba Yaena', 'taiwanese': '巴巴耶納'},
                   23333: {'chinese': '克黑达洽齐', 'english': "Keheda'tearchy", 'french': "Keheda'tearchy",
                           'german': "Keheda'tearchy", 'italian': "Keheda'tearchy", 'japanese': 'ケヘダ・テアチー',
                           'korean': '케헤다티어치', 'polish': "Keheda'tearchy", 'russian': 'Кехеда-Теарчи',
                           'spanish': "Keheda'tearchy", 'taiwanese': '克黑達洽齊'},
                   23334: {'chinese': '欧克拉托蜜欧', 'english': 'Okra Turmio', 'french': 'Okra Turmio',
                           'german': 'Okra Turmio', 'italian': 'Okra Turmio', 'japanese': 'オクラ・ターミオ',
                           'korean': '오크라 터미오', 'polish': 'Okra Turmio', 'russian': 'Окра-Турмио',
                           'spanish': 'Okra Turmio', 'taiwanese': '歐克拉托蜜歐'},
                   23335: {'chinese': '阿迪斯塔拉拉', 'english': 'Addis Tarara', 'french': 'Addis Tarara',
                           'german': 'Addis Tarara', 'italian': 'Addis Tarara', 'japanese': 'アディス・タララ',
                           'korean': '아디스 타라라', 'polish': 'Addis Tarara', 'russian': 'Аддис-Тарара',
                           'spanish': 'Addis Tarara', 'taiwanese': '阿迪斯塔拉拉'},
                   23336: {'chinese': '德德比安涅贝沙', 'english': 'Dedebi Anibesa', 'french': 'Dedebi Anibesa',
                           'german': 'Dedebi Anibesa', 'italian': 'Dedebi Anibesa', 'japanese': 'デデビ・アニベサ',
                           'korean': '데데비 아니베사', 'polish': 'Dedebi Anibesa', 'russian': 'Дедеби-Анибеса',
                           'spanish': 'Dedebi Anibesa', 'taiwanese': '德德比安涅貝沙'},
                   23337: {'chinese': '比丽希绮', 'english': 'Bilihi Ziyi', 'french': 'Bilihi Ziyi',
                           'german': 'Bilihi Ziyi', 'italian': 'Bilihi Ziyi', 'japanese': 'ビリヒ・ズィーイー',
                           'korean': '빌리히 지이', 'polish': 'Bilihi Ziyi', 'russian': 'Билихи-Зийи',
                           'spanish': 'Bilihi Ziyi', 'taiwanese': '比麗希綺'},
                   23338: {'chinese': '丢克努坎', 'english': 'Duknu Kem', 'french': 'Duknu Kem', 'german': 'Duknu Kem',
                           'italian': 'Duknu Kem', 'japanese': 'ドゥークヌー・ケム', 'korean': '듀크누 켐', 'polish': 'Duknu Kem',
                           'russian': 'Дукну-Кем', 'spanish': 'Duknu Kem', 'taiwanese': '丟克努坎'},
                   23339: {'chinese': '德布窝鲁鲁', 'english': 'Debu Wololo', 'french': 'Debu Wololo',
                           'german': 'Debu Wololo', 'italian': 'Debu Wololo', 'japanese': 'デーブ・ウォロロ',
                           'korean': '데부 월롤로', 'polish': 'Debu Wololo', 'russian': 'Дэбу-Вололо',
                           'spanish': 'Debu Wololo', 'taiwanese': '德布窩魯魯'},
                   23340: {'chinese': '艾由窝鲁鲁', 'english': 'Ayeou Wololo', 'french': 'Ayeou Wololo',
                           'german': 'Ayeou Wololo', 'italian': 'Ayeou Wololo', 'japanese': 'アーヨウ・ウォロロ',
                           'korean': '아예우 월롤로', 'polish': 'Ayeou Wololo', 'russian': 'Айеу-Вололо',
                           'spanish': 'Ayeou Wololo', 'taiwanese': '艾由窩魯魯'},
                   23341: {'chinese': '阿拉巴玛他', 'english': 'Alabamata', 'french': 'Alabamata', 'german': 'Alabamata',
                           'italian': 'Alabamata', 'japanese': 'アラバマタ', 'korean': '알라바마타', 'polish': 'Alabamata',
                           'russian': 'Алабамата', 'spanish': 'Alabamata', 'taiwanese': '阿拉巴瑪他'},
                   23342: {'chinese': '拉西拉萨提拉西', 'english': 'Lesilasa Tirasi', 'french': 'Lesilasa Tirasi',
                           'german': 'Lesilasa Tirasi', 'italian': 'Lesilasa Tirasi', 'japanese': 'レシラサ・ティラシ',
                           'korean': '레실라사 티라시', 'polish': 'Lesilasa Tirasi', 'russian': 'Лесиласа-Тираси',
                           'spanish': 'Lesilasa Tirasi', 'taiwanese': '拉西拉薩提拉西'},
                   23343: {'chinese': '德布列艾苏', 'english': 'Debre Iesu', 'french': 'Debre Iesu', 'german': 'Debre Iesu',
                           'italian': 'Debre Iesu', 'japanese': 'デブレ・イエス', 'korean': '데브레 예수', 'polish': 'Debre Iesu',
                           'russian': 'Дэбре-Иесу', 'spanish': 'Debre Iesu', 'taiwanese': '德布列艾蘇'},
                   23344: {'chinese': '德布列马耶姆', 'english': 'Debre Maryam', 'french': 'Debre Maryam',
                           'german': 'Debre Maryam', 'italian': 'Debre Maryam', 'japanese': 'デブレ・マリアム',
                           'korean': '데브레 마리엄', 'polish': 'Debre Maryam', 'russian': 'Дэбре-Марьям',
                           'spanish': 'Debre Maryam', 'taiwanese': '德布列馬耶姆'},
                   23345: {'chinese': '阿飞丽克阿那堤', 'english': 'Afirik Anati', 'french': 'Afirik Anati',
                           'german': 'Afirik Anati', 'italian': 'Afirik Anati', 'japanese': 'アフィリク・アナティ',
                           'korean': '아피리크 아나티', 'polish': 'Afirik Anati', 'russian': 'Афирик-Анати',
                           'spanish': 'Afirik Anati', 'taiwanese': '阿飛麗克阿那堤'},
                   23346: {'chinese': '德布列塔波里', 'english': 'Debre Tabori', 'french': 'Debre Tabori',
                           'german': 'Debre Tabori', 'italian': 'Debre Tabori', 'japanese': 'デブレ・タボリ',
                           'korean': '데브레 타보리', 'polish': 'Debre Tabori', 'russian': 'Дэбре-Табори',
                           'spanish': 'Debre Tabori', 'taiwanese': '德布列塔波里'},
                   23347: {'chinese': '艾伟地海呼', 'english': 'Iwedihalehu', 'french': 'Iwedihalehu',
                           'german': 'Iwedihalehu', 'italian': 'Iwedihalehu', 'japanese': 'イウェディハレフ',
                           'korean': '이웨디할레후', 'polish': 'Iwedihalehu', 'russian': 'Иведихалеху',
                           'spanish': 'Iwedihalehu', 'taiwanese': '艾偉地海呼'},
                   23348: {'chinese': '阿迪斯菲克利', 'english': 'Addis Fikiri', 'french': 'Addis Fikiri',
                           'german': 'Addis Fikiri', 'italian': 'Addis Fikiri', 'japanese': 'アディス・フィキリ',
                           'korean': '아디스 피키리', 'polish': 'Addis Fikiri', 'russian': 'Аддис-Фикири',
                           'spanish': 'Addis Fikiri', 'taiwanese': '阿迪斯菲克利'},
                   23349: {'chinese': '切瓦他威尼耶格祖', 'english': 'Chewatawini Yigizu', 'french': 'Chewatawini Yigizu',
                           'german': 'Chewatawini Yigizu', 'italian': 'Chewatawini Yigizu', 'japanese': 'チェワタウィニ・イギズ',
                           'korean': '츄와타위니 이기즈', 'polish': 'Chewatawini Yigizu', 'russian': 'Чеватаини-Йигизу',
                           'spanish': 'Chewatawini Yigizu', 'taiwanese': '切瓦他威尼耶格祖'},
                   23350: {'chinese': '艾梅瑟爵诺胡', 'english': 'Ameseginalehu', 'french': 'Ameseginalehu',
                           'german': 'Ameseginalehu', 'italian': 'Ameseginalehu', 'japanese': 'アメセギナレフ',
                           'korean': '아메세기날레후', 'polish': 'Ameseginalehu', 'russian': 'Амесегиналеху',
                           'spanish': 'Ameseginalehu', 'taiwanese': '艾梅瑟爵諾胡'},
                   23351: {'chinese': '区区加马吉', 'english': 'Jujuga Maji', 'french': 'Jujuga Maji',
                           'german': 'Jujuga Maji', 'italian': 'Jujuga Maji', 'japanese': 'ジュジュガ・マジ',
                           'korean': '쥬쥬가 마지', 'polish': 'Jujuga Maji', 'russian': 'Джуджуга-Маджи',
                           'spanish': 'Jujuga Maji', 'taiwanese': '區區加馬吉'},
                   23352: {'chinese': '瑟更', 'english': 'Seghene', 'french': 'Seghene', 'german': 'Seghene',
                           'italian': 'Seghene', 'japanese': 'セゲネ', 'korean': '세그헤네', 'polish': 'Seghene',
                           'russian': 'Сегхене', 'spanish': 'Seghene', 'taiwanese': '瑟更'},
                   23353: {'chinese': '阿迪斯非瑞西', 'english': 'Addis Feresi', 'french': 'Addis Feresi',
                           'german': 'Addis Feresi', 'italian': 'Addis Feresi', 'japanese': 'アディス・フェレシ',
                           'korean': '아디스 페레시', 'polish': 'Addis Feresi', 'russian': 'Аддис-Фереси',
                           'spanish': 'Addis Feresi', 'taiwanese': '阿迪斯非瑞西'},
                   23354: {'chinese': '阿迪斯裘迪西', 'english': 'Addis Jidisi', 'french': 'Addis Jidisi',
                           'german': 'Addis Jidisi', 'italian': 'Addis Jidisi', 'japanese': 'アディス・ジディシ',
                           'korean': '아디스 지디시', 'polish': 'Addis Jidisi', 'russian': 'Аддис-Джидиси',
                           'spanish': 'Addis Jidisi', 'taiwanese': '阿迪斯裘迪西'},
                   23355: {'chinese': '德布列里他廷', 'english': 'Debre Litating', 'french': 'Debre Litating',
                           'german': 'Debre Litating', 'italian': 'Debre Litating', 'japanese': 'デブレ・リタティング',
                           'korean': '데브레 리타팅', 'polish': 'Debre Litating', 'russian': 'Дэбре-Литатинг',
                           'spanish': 'Debre Litating', 'taiwanese': '德布列里他廷'},
                   23356: {'chinese': '尼盖赛纳非', 'english': 'Negele Senefi', 'french': 'Negele Senefi',
                           'german': 'Negele Senefi', 'italian': 'Negele Senefi', 'japanese': 'ネゲレ・セネフィ',
                           'korean': '네겔레 세네피', 'polish': 'Negele Senefi', 'russian': 'Негеле-Сенефи',
                           'spanish': 'Negele Senefi', 'taiwanese': '尼蓋賽納非'},
                   23357: {'chinese': '帖妮卡拉布纳', 'english': 'Tenikara Buna', 'french': 'Tenikara Buna',
                           'german': 'Tenikara Buna', 'italian': 'Tenikara Buna', 'japanese': 'テニカラ・ブナ',
                           'korean': '테니카라 부나', 'polish': 'Tenikara Buna', 'russian': 'Теникара-Буна',
                           'spanish': 'Tenikara Buna', 'taiwanese': '帖妮卡拉布納'},
                   23358: {'chinese': '夏米拉斯', 'english': 'Shamyrath', 'french': 'Shamyrath', 'german': 'Shamyrath',
                           'italian': 'Shamyrath', 'japanese': 'シャミラス', 'korean': '샤미라스', 'polish': 'Shamyrath',
                           'russian': 'Шамират', 'spanish': 'Shamyrath', 'taiwanese': '夏米拉斯'},
                   23359: {'chinese': '萨里阿尼贝沙', 'english': 'Sahle Anibesa', 'french': 'Sahle Anibesa',
                           'german': 'Sahle Anibesa', 'italian': 'Sahle Anibesa', 'japanese': 'サーレ・アニベサ',
                           'korean': '사흘 아니베사', 'polish': 'Sahle Anibesa', 'russian': 'Сахле-Анибеса',
                           'spanish': 'Sahle Anibesa', 'taiwanese': '薩里阿尼貝沙'},
                   23360: {'chinese': '阿列芒亚', 'english': 'Alemanya', 'french': 'Alemanya', 'german': 'Alemanya',
                           'italian': 'Alemanya', 'japanese': 'アレマーニャ', 'korean': '알레마냐', 'polish': 'Alemanya',
                           'russian': 'Алеманья', 'spanish': 'Alemanya', 'taiwanese': '阿列芒亞'},
                   23361: {'chinese': '史努奏顿埃多堡', 'english': 'Snoozleton Idleburgh', 'french': 'Snoozleton Idleburgh',
                           'german': 'Snoozleton Idleburgh', 'italian': 'Snoozleton Idleburgh',
                           'japanese': 'スヌーズルトン・アイドルバーグ', 'korean': '스누즐레턴 아이들버그', 'polish': 'Snoozleton Idleburgh',
                           'russian': 'Скучтаун', 'spanish': 'Snoozleton Idleburgh', 'taiwanese': '史努奏頓埃多堡'},
                   23518: {'chinese': '阿德马苏', 'english': 'Admassu', 'french': 'Admassu', 'german': 'Admassu',
                           'italian': 'Admassu', 'japanese': 'アドマッス', 'korean': '아드마수', 'polish': 'Admassu',
                           'russian': 'Адмассу', 'spanish': 'Admassu', 'taiwanese': '阿德馬蘇'},
                   23519: {'chinese': '亚斯美拉', 'english': 'Yäsmera', 'french': 'Yäsmera', 'german': 'Yäsmera',
                           'italian': 'Yäsmera', 'japanese': 'イェスメラ', 'korean': '야스메라', 'polish': 'Yäsmera',
                           'russian': 'Ясмера', 'spanish': 'Yäsmera', 'taiwanese': '亞斯美拉'},
                   23520: {'chinese': '贝塔拉罕', 'english': 'Bayta Lahem', 'french': 'Bayta Lahem',
                           'german': 'Bayta Lahem', 'italian': 'Bayta Lahem', 'japanese': 'バイタ・ラヘム', 'korean': '베이타 라헴',
                           'polish': 'Bayta Lahem', 'russian': 'Байта-Лахем', 'spanish': 'Bayta Lahem',
                           'taiwanese': '貝塔拉罕'},
                   23521: {'chinese': '丹姆乔突', 'english': 'Dagm Chaltu', 'french': 'Dagm Chaltu',
                           'german': 'Dagm Chaltu', 'italian': 'Dagm Chaltu', 'japanese': 'ダフム・チャルトゥ',
                           'korean': '다금 찰투', 'polish': 'Dagm Chaltu', 'russian': 'Дагм-Чалту',
                           'spanish': 'Dagm Chaltu', 'taiwanese': '丹姆喬突'},
                   23522: {'chinese': '埃贝托', 'english': 'Elbetel', 'french': 'Elbetel', 'german': 'Elbetel',
                           'italian': 'Elbetel', 'japanese': 'エルベテル', 'korean': '엘베텔', 'polish': 'Elbetel',
                           'russian': 'Эльбетел', 'spanish': 'Elbetel', 'taiwanese': '埃貝托'},
                   23523: {'chinese': '菲芮贺瓦特', 'english': 'Freyhiwot', 'french': 'Freyhiwot', 'german': 'Freyhiwot',
                           'italian': 'Freyhiwot', 'japanese': 'フレイヒウォト', 'korean': '프레이히웟', 'polish': 'Freyhiwot',
                           'russian': 'Фрейхивот', 'spanish': 'Freyhiwot', 'taiwanese': '菲芮賀瓦特'},
                   23524: {'chinese': '盖特哈坦姆', 'english': 'Getawh Habtom', 'french': 'Getawh Habtom',
                           'german': 'Getawh Habtom', 'italian': 'Getawh Habtom', 'japanese': 'ゲタフ・ハブトム',
                           'korean': '게타 하브톰', 'polish': 'Getawh Habtom', 'russian': 'Гетав-Хабтом',
                           'spanish': 'Getawh Habtom', 'taiwanese': '蓋特哈坦姆'},
                   23525: {'chinese': '都乐拿登', 'english': 'Dulanaden', 'french': 'Dulanaden', 'german': 'Dulanaden',
                           'italian': 'Dulanaden', 'japanese': 'ドゥルナデン', 'korean': '둘라나덴', 'polish': 'Dulanaden',
                           'russian': 'Дуланаден', 'spanish': 'Dulanaden', 'taiwanese': '都樂拿登'},
                   23526: {'chinese': '埃俄薛得', 'english': 'Elshaday', 'french': 'Elshaday', 'german': 'Elshaday',
                           'italian': 'Elshaday', 'japanese': 'エルシャダイ', 'korean': '엘샤다이', 'polish': 'Elshaday',
                           'russian': 'Эльшадэй', 'spanish': 'Elshaday', 'taiwanese': '埃俄薛得'},
                   23527: {'chinese': '柯提马科达', 'english': 'Ketemakda', 'french': 'Ketemakda', 'german': 'Ketemakda',
                           'italian': 'Ketemakda', 'japanese': 'ケテマクダ', 'korean': '케테마크다', 'polish': 'Ketemakda',
                           'russian': 'Кетемакда', 'spanish': 'Ketemakda', 'taiwanese': '柯提馬科達'},
                   23528: {'chinese': '忒玛斯坚', 'english': 'Temesgen', 'french': 'Temesgen', 'german': 'Temesgen',
                           'italian': 'Temesgen', 'japanese': 'テメスゲン', 'korean': '테메스겐', 'polish': 'Temesgen',
                           'russian': 'Темесген', 'spanish': 'Temesgen', 'taiwanese': '忒瑪斯堅'},
                   23529: {'chinese': '坎波洽尔', 'english': 'Kombolcharim', 'french': 'Kombolcharim',
                           'german': 'Kombolcharim', 'italian': 'Kombolcharim', 'japanese': 'コンボルキャリム',
                           'korean': '콤볼챠림', 'polish': 'Kombolcharim', 'russian': 'Комбольчарим',
                           'spanish': 'Kombolcharim', 'taiwanese': '坎波洽爾'},
                   23530: {'chinese': '尼盖梅突', 'english': 'Negele Metu', 'french': 'Negele Metu',
                           'german': 'Negele Metu', 'italian': 'Negele Metu', 'japanese': 'ネゲレ・メトゥ', 'korean': '네겔레 메투',
                           'polish': 'Negele Metu', 'russian': 'Негеле-Мет', 'spanish': 'Negele Metu',
                           'taiwanese': '尼蓋梅突'},
                   23531: {'chinese': '甘多罗罕', 'english': 'Gondorohan', 'french': 'Gondorohan', 'german': 'Gondorohan',
                           'italian': 'Gondorohan', 'japanese': 'ゴンドロハン', 'korean': '곤도로한', 'polish': 'Gondorohan',
                           'russian': 'Гондорохан', 'spanish': 'Gondorohan', 'taiwanese': '甘多羅罕'},
                   23532: {'chinese': '艾拉莱贝拉', 'english': 'Elal Ibella', 'french': 'Elal Ibella',
                           'german': 'Elal Ibella', 'italian': 'Elal Ibella', 'japanese': 'エラル・イベラ', 'korean': '엘랄 이벨라',
                           'polish': 'Elal Ibella', 'russian': 'Элаль-Ибелла', 'spanish': 'Elal Ibella',
                           'taiwanese': '艾拉萊貝拉'},
                   23533: {'chinese': '尤加瑟扣塔', 'english': 'Yirga Sekota', 'french': 'Yirga Sekota',
                           'german': 'Yirga Sekota', 'italian': 'Yirga Sekota', 'japanese': 'イルガ・セコタ',
                           'korean': '이르가 세코타', 'polish': 'Yirga Sekota', 'russian': 'Йирга-Секота',
                           'spanish': 'Yirga Sekota', 'taiwanese': '尤加瑟扣塔'},
                   23534: {'chinese': '尤加薛拉佛', 'english': 'Yirga Shilavo', 'french': 'Yirga Shilavo',
                           'german': 'Yirga Shilavo', 'italian': 'Yirga Shilavo', 'japanese': 'イルガ・シラヴォ',
                           'korean': '이르가 쉴라보', 'polish': 'Yirga Shilavo', 'russian': 'Йирга-Шилаво',
                           'spanish': 'Yirga Shilavo', 'taiwanese': '尤加薛拉佛'},
                   23535: {'chinese': '尤加玛伊克', 'english': 'Yirga Maïq', 'french': 'Yirga Maïk', 'german': 'Yirga Maïq',
                           'italian': 'Yirga Maïq', 'japanese': 'イルガ・マイク', 'korean': '이르가 마이크', 'polish': 'Yirga Maïq',
                           'russian': 'Йирга-Маик', 'spanish': 'Yirga Maïq', 'taiwanese': '尤加瑪伊克'},
                   23536: {'chinese': '玛伊克莱可土史尼克', 'english': 'Maïq Laiqtu Sneeq', 'french': 'Maïk Laiktu Sneek',
                           'german': 'Maïq Laiqtu Sneeq', 'italian': 'Maïq Laiqtu Sneeq', 'japanese': 'マイク・ライクトゥ・スニーク',
                           'korean': '마이크 라이크투 스니크', 'polish': 'Maïq Laiqtu Sneeq', 'russian': 'Маик-Лаикту-Сник',
                           'spanish': 'Maïq Laiqtu Sneeq', 'taiwanese': '瑪伊克萊可土史尼克'},
                   23537: {'chinese': '莱布纳蔻可比', 'english': 'Lebna Kokebi', 'french': 'Lebna Kokebi',
                           'german': 'Lebna Kokebi', 'italian': 'Lebna Kokebi', 'japanese': 'レブナ・コケビ',
                           'korean': '레브나 코케비', 'polish': 'Lebna Kokebi', 'russian': 'Лебна-Кокеби',
                           'spanish': 'Lebna Kokebi', 'taiwanese': '萊布納蔻可比'},
                   23538: {'chinese': '莱布纳玛蕊姆', 'english': 'Lebna Mahrem', 'french': 'Lebna Mahrem',
                           'german': 'Lebna Mahrem', 'italian': 'Lebna Mahrem', 'japanese': 'レブナ・マーレム',
                           'korean': '레브나 마흐렘', 'polish': 'Lebna Mahrem', 'russian': 'Лебна-Махрем',
                           'spanish': 'Lebna Mahrem', 'taiwanese': '萊布納瑪蕊姆'},
                   23539: {'chinese': '莱布纳玛布拉提', 'english': 'Lebna Mebrahtu', 'french': 'Lebna Mebrahtu',
                           'german': 'Lebna Mebrahtu', 'italian': 'Lebna Mebrahtu', 'japanese': 'レブナ・メブラートゥ',
                           'korean': '레브나 메브라투', 'polish': 'Lebna Mebrahtu', 'russian': 'Лебна-Мебрахту',
                           'spanish': 'Lebna Mebrahtu', 'taiwanese': '萊布納瑪布拉提'},
                   23540: {'chinese': '莱布纳涅孤西', 'english': 'Lebna Negusi', 'french': 'Lebna Negusi',
                           'german': 'Lebna Negusi', 'italian': 'Lebna Negusi', 'japanese': 'レブナ・ネグシ',
                           'korean': '레브나 네구시', 'polish': 'Lebna Negusi', 'russian': 'Лебна-Негуси',
                           'spanish': 'Lebna Negusi', 'taiwanese': '萊布納涅孤西'},
                   23541: {'chinese': '莱布纳萨多', 'english': 'Lebna Sador', 'french': 'Lebna Sador',
                           'german': 'Lebna Sador', 'italian': 'Lebna Sador', 'japanese': 'レブナ・サドール',
                           'korean': '레브나 사도르', 'polish': 'Lebna Sador', 'russian': 'Лебна-Садор',
                           'spanish': 'Lebna Sador', 'taiwanese': '萊布納薩多'},
                   23542: {'chinese': '莱布纳西美拉', 'english': 'Lebna Simera', 'french': 'Lebna Simera',
                           'german': 'Lebna Simera', 'italian': 'Lebna Simera', 'japanese': 'レブナ・シメラ',
                           'korean': '레브나 시메라', 'polish': 'Lebna Simera', 'russian': 'Лебна-Симера',
                           'spanish': 'Lebna Simera', 'taiwanese': '萊布納西美拉'},
                   23543: {'chinese': '莱布纳提居斯特', 'english': 'Lebna Tigist', 'french': 'Lebna Tigist',
                           'german': 'Lebna Tigist', 'italian': 'Lebna Tigist', 'japanese': 'レブナ・ティギスト',
                           'korean': '레브나 티지스트', 'polish': 'Lebna Tigist', 'russian': 'Лебна-Тигист',
                           'spanish': 'Lebna Tigist', 'taiwanese': '萊布納提居斯特'},
                   23544: {'chinese': '莱布纳伟瑞奇', 'english': 'Lebna Weriki', 'french': 'Lebna Weriki',
                           'german': 'Lebna Weriki', 'italian': 'Lebna Weriki', 'japanese': 'レブナ・ウェリキ',
                           'korean': '레브나 웨리키', 'polish': 'Lebna Weriki', 'russian': 'Лебна-Верики',
                           'spanish': 'Lebna Weriki', 'taiwanese': '萊布納偉瑞奇'},
                   23545: {'chinese': '莱布纳由鲁沙兰', 'english': 'Lebna Yorushalem', 'french': 'Lebna Yorushalem',
                           'german': 'Lebna Yorushalem', 'italian': 'Lebna Yorushalem', 'japanese': 'レブナ・ヨルシャレム',
                           'korean': '레브나 요루샬렘', 'polish': 'Lebna Yorushalem', 'russian': 'Лебна-Йорушалем',
                           'spanish': 'Lebna Yorushalem', 'taiwanese': '萊布納由魯沙蘭'},
                   23546: {'chinese': '姚泰桑', 'english': 'Yodtye Sine', 'french': 'Yodtye Sine', 'german': 'Yodtye Sine',
                           'italian': 'Yodtye Sine', 'japanese': 'ヨッディエ・シネ', 'korean': '요드티예 시네',
                           'polish': 'Yodtye Sine', 'russian': 'Йодтье-Сине', 'spanish': 'Yodtye Sine',
                           'taiwanese': '姚泰桑'},
                   23547: {'chinese': '康丘巴那', 'english': 'Konjo Bunna', 'french': 'Konjo Bunna',
                           'german': 'Konjo Bunna', 'italian': 'Konjo Bunna', 'japanese': 'コンジョ・ブンナ', 'korean': '콘죠 부나',
                           'polish': 'Konjo Bunna', 'russian': 'Коньо-Бунна', 'spanish': 'Konjo Bunna',
                           'taiwanese': '康丘巴那'},
                   23548: {'chinese': '茵爵耶嫩', 'english': 'Injah Yenen', 'french': 'Injah Yenen',
                           'german': 'Injah Yenen', 'italian': 'Injah Yenen', 'japanese': 'インジャー・イエネン',
                           'korean': '인자 예넨', 'polish': 'Injah Yenen', 'russian': 'Инджа-Йенен',
                           'spanish': 'Injah Yenen', 'taiwanese': '茵爵耶嫩'},
                   23549: {'chinese': '达帝帖居', 'english': 'Daadhi Tej', 'french': 'Daadhi Tej', 'german': 'Daadhi Tej',
                           'italian': 'Daadhi Tej', 'japanese': 'ダーディ・テジ', 'korean': '다드히 테즈', 'polish': 'Daadhi Tej',
                           'russian': 'Даадхи-Тэж', 'spanish': 'Daadhi Tej', 'taiwanese': '達帝帖居'},
                   23550: {'chinese': '瑞库英格鲁', 'english': 'Rakoon Ingiruu', 'french': 'Rakoon Ingiruu',
                           'german': 'Rakoon Ingiruu', 'italian': 'Rakoon Ingiruu', 'japanese': 'ラコーン・インギルー',
                           'korean': '라쿤 인지루', 'polish': 'Rakoon Ingiruu', 'russian': 'Ракун-Ингируу',
                           'spanish': 'Rakoon Ingiruu', 'taiwanese': '瑞庫英格魯'},
                   23551: {'chinese': '德汗西德鲁', 'english': 'Dehan Hideru', 'french': 'Dehan Hideru',
                           'german': 'Dehan Hideru', 'italian': 'Dehan Hideru', 'japanese': 'デハン・ヒデル',
                           'korean': '드한 히데루', 'polish': 'Dehan Hideru', 'russian': 'Дэхан-Хидеру',
                           'spanish': 'Dehan Hideru', 'taiwanese': '德汗西德魯'},
                   23552: {'chinese': '阿坎裘突', 'english': 'Akkam Jirtuu', 'french': 'Akkam Jirtuu',
                           'german': 'Akkam Jirtuu', 'italian': 'Akkam Jirtuu', 'japanese': 'アッカム・ジルトゥー',
                           'korean': '아캄 지르투', 'polish': 'Akkam Jirtuu', 'russian': 'Аккам-Джиртуу',
                           'spanish': 'Akkam Jirtuu', 'taiwanese': '阿坎裘突'},
                   23553: {'chinese': '贝尔海里', 'english': 'Bale Haile', 'french': 'Bale Haile', 'german': 'Bale Haile',
                           'italian': 'Bale Haile', 'japanese': 'バレ・ハイレ', 'korean': '발레 하일레', 'polish': 'Bale Haile',
                           'russian': 'Бале-Хайле', 'spanish': 'Bale Haile', 'taiwanese': '貝爾海里'},
                   23554: {'chinese': '巴希尔榜加', 'english': 'Bahir Bonga', 'french': 'Bahir Bonga',
                           'german': 'Bahir Bonga', 'italian': 'Bahir Bonga', 'japanese': 'バヒル・ボンガ', 'korean': '바히르 봉가',
                           'polish': 'Bahir Bonga', 'russian': 'Бахир-Бонга', 'spanish': 'Bahir Bonga',
                           'taiwanese': '巴希爾榜加'},
                   23555: {'chinese': '珂博赞门', 'english': 'Kobo Zemen', 'french': 'Kobo Zemen', 'german': 'Kobo Zemen',
                           'italian': 'Kobo Zemen', 'japanese': 'コボ・ゼーメン', 'korean': '코보 제멘', 'polish': 'Kobo Zemen',
                           'russian': 'Кобо-Земен', 'spanish': 'Kobo Zemen', 'taiwanese': '珂博贊門'},
                   23556: {'chinese': '库提他提', 'english': 'Kuti Totit', 'french': 'Kuti Totit', 'german': 'Kuti Totit',
                           'italian': 'Kuti Totit', 'japanese': 'クティ・トティト', 'korean': '쿠티 토팃', 'polish': 'Kuti Totit',
                           'russian': 'Кути-Тотит', 'spanish': 'Kuti Totit', 'taiwanese': '庫提他提'},
                   23557: {'chinese': '提希塔威哈', 'english': 'Tizita Wiha', 'french': 'Tizita Wiha',
                           'german': 'Tizita Wiha', 'italian': 'Tizita Wiha', 'japanese': 'ティジタ・ウィハ',
                           'korean': '티지타 위하', 'polish': 'Tizita Wiha', 'russian': 'Тизита-Виха',
                           'spanish': 'Tizita Wiha', 'taiwanese': '提希塔威哈'},
                   23558: {'chinese': '祖拉托提提', 'english': 'Zula Totiti', 'french': 'Zula Totiti',
                           'german': 'Zula Totiti', 'italian': 'Zula Totiti', 'japanese': 'ズーラ・トティティ',
                           'korean': '줄라 토팃', 'polish': 'Zula Totiti', 'russian': 'Зула-Тотити',
                           'spanish': 'Zula Totiti', 'taiwanese': '祖拉托提提'},
                   23559: {'chinese': '祖拉他法奇', 'english': 'Zula Tafachi', 'french': 'Zula Tafachi',
                           'german': 'Zula Tafachi', 'italian': 'Zula Tafachi', 'japanese': 'ズーラ・タファチ',
                           'korean': '줄라 타파치', 'polish': 'Zula Tafachi', 'russian': 'Зула-Тафачи',
                           'spanish': 'Zula Tafachi', 'taiwanese': '祖拉他法奇'},
                   23560: {'chinese': '祖拉涅布瑞', 'english': 'Zula Nebiri', 'french': 'Zula Nebiri',
                           'german': 'Zula Nebiri', 'italian': 'Zula Nebiri', 'japanese': 'ズーラ・ネビリ', 'korean': '줄라 네비리',
                           'polish': 'Zula Nebiri', 'russian': 'Зула-Небири', 'spanish': 'Zula Nebiri',
                           'taiwanese': '祖拉涅布瑞'},
                   23561: {'chinese': '祖拉科起比', 'english': 'Zula Kokebi', 'french': 'Zula Kokebi',
                           'german': 'Zula Kokebi', 'italian': 'Zula Kokebi', 'japanese': 'ズーラ・コケビ', 'korean': '줄라 코케비',
                           'polish': 'Zula Kokebi', 'russian': 'Зула-Кокеби', 'spanish': 'Zula Kokebi',
                           'taiwanese': '祖拉科起比'},
                   23562: {'chinese': '祖拉依尼堀', 'english': 'Zula Iniku', 'french': 'Zula Iniku', 'german': 'Zula Iniku',
                           'italian': 'Zula Iniku', 'japanese': 'ズーラ・イニク', 'korean': '줄라 이니쿠', 'polish': 'Zula Iniku',
                           'russian': 'Зула-Инику', 'spanish': 'Zula Iniku', 'taiwanese': '祖拉依尼堀'},
                   23563: {'chinese': '祖拉爵那', 'english': 'Zula Genat', 'french': 'Zula Genat', 'german': 'Zula Genat',
                           'italian': 'Zula Genat', 'japanese': 'ズーラ・ゲナト', 'korean': '줄라 게낫', 'polish': 'Zula Genat',
                           'russian': 'Зула-Генат', 'spanish': 'Zula Genat', 'taiwanese': '祖拉爵那'},
                   23564: {'chinese': '祖拉布拉比罗', 'english': 'Zula Birabiro', 'french': 'Zula Birabiro',
                           'german': 'Zula Birabiro', 'italian': 'Zula Birabiro', 'japanese': 'ズーラ・ビラビロ',
                           'korean': '줄라 비라비로', 'polish': 'Zula Birabiro', 'russian': 'Зула-Бирабиро',
                           'spanish': 'Zula Birabiro', 'taiwanese': '祖拉布拉比羅'},
                   23565: {'chinese': '祖拉拜棱', 'english': 'Zula Bilen', 'french': 'Zula Bilen', 'german': 'Zula Bilen',
                           'italian': 'Zula Bilen', 'japanese': 'ズーラ・ビレン', 'korean': '줄라 빌렌', 'polish': 'Zula Bilen',
                           'russian': 'Зула-Билен', 'spanish': 'Zula Bilen', 'taiwanese': '祖拉拜稜'},
                   23566: {'chinese': '沙巴', 'english': 'Shaba Ayele', 'french': 'Shaba Ayele', 'german': 'Shaba Ayele',
                           'italian': 'Shaba Ayele', 'japanese': 'シャバ・アイェレ', 'korean': '샤바 아옐레',
                           'polish': 'Shaba Ayele', 'russian': 'Шаба-Айеле', 'spanish': 'Shaba Ayele',
                           'taiwanese': '沙巴'},
                   23567: {'chinese': '潭亚阿米贝沙', 'english': 'Tenya Amibesa', 'french': 'Tenya Amibesa',
                           'german': 'Tenya Amibesa', 'italian': 'Tenya Amibesa', 'japanese': 'テーニャ・アミベサ',
                           'korean': '테냐 아밀베사', 'polish': 'Tenya Amibesa', 'russian': 'Тенья-Амибеса',
                           'spanish': 'Tenya Amibesa', 'taiwanese': '潭亞阿米貝沙'},
                   23568: {'chinese': '帖撒拉区区雷胡', 'english': 'Teselachichalehu', 'french': 'Teselachichalehu',
                           'german': 'Teselachichalehu', 'italian': 'Teselachichalehu', 'japanese': 'テセラチチャレフ',
                           'korean': '테셀라치찰레후', 'polish': 'Teselachichalehu', 'russian': 'Теселачичалеху',
                           'spanish': 'Teselachichalehu', 'taiwanese': '帖撒拉區區雷胡'},
                   23569: {'chinese': '赛托齐尼梅德盖非', 'english': 'Setochini Medegefi', 'french': 'Setochini Medegefi',
                           'german': 'Setochini Medegefi', 'italian': 'Setochini Medegefi', 'japanese': 'セトチニ・メデゲフィ',
                           'korean': '세토치니 메데게피', 'polish': 'Setochini Medegefi', 'russian': 'Сеточини-Медегефи',
                           'spanish': 'Setochini Medegefi', 'taiwanese': '賽托齊尼梅德蓋非'},
                   23570: {'chinese': '瑟麦亚米尼奇夏', 'english': 'Semayami Nikisha', 'french': 'Semayami Nikisha',
                           'german': 'Semayami Nikisha', 'italian': 'Semayami Nikisha', 'japanese': 'セマヤミ・ニキーシャ',
                           'korean': '세마야미 니키샤', 'polish': 'Semayami Nikisha', 'russian': 'Семайами-Никиша',
                           'spanish': 'Semayami Nikisha', 'taiwanese': '瑟麥亞米尼奇夏'},
                   23571: {'chinese': '依冷的表', 'english': "Elam's Watch", 'french': "Veille d'Elam",
                           'german': 'Elams Wacht', 'italian': 'Orologio di Elam', 'japanese': 'エラムズウォッチ',
                           'korean': '엘람의 시계', 'polish': 'Straż Elama', 'russian': 'Дозор Элама',
                           'spanish': 'Reloj de Elam', 'taiwanese': '依冷的錶'},
                   23572: {'chinese': '沙巴的歌', 'english': "Shaba's Song", 'french': 'Chant de Shaba',
                           'german': 'Sebas Lied', 'italian': 'Canzone di Shaba', 'japanese': 'シャバズソング',
                           'korean': '샤바의 노래', 'polish': 'Pieśń Shaby', 'russian': 'Песнь Шабы',
                           'spanish': 'Canción de Shaba', 'taiwanese': '沙巴的歌'},
                   23573: {'chinese': '依冷的归来', 'english': "Elam's Return", 'french': "Retour d'Elam",
                           'german': 'Elams Rückkehr', 'italian': 'Ritorno di Elam', 'japanese': 'エラムズリターン',
                           'korean': '엘람의 귀환', 'polish': 'Powrót Elama', 'russian': 'Возвращение Элама',
                           'spanish': 'Regreso de Elam', 'taiwanese': '依冷的歸來'},
                   23574: {'chinese': '依冷的鹰', 'english': 'Hawk of Elam', 'french': "Faucon d'Elam",
                           'german': 'Falke von Elam', 'italian': 'Falco di Elam', 'japanese': 'ホーク・オブ・エラム',
                           'korean': '엘람의 매', 'polish': 'Jastrząb Elama', 'russian': 'Ястреб Элама',
                           'spanish': 'Halcón de Elam', 'taiwanese': '依冷的鷹'},
                   23575: {'chinese': '斐尼克斯的栖身处', 'english': "Phoenix's Roost", 'french': 'Nichoir du Phénix',
                           'german': 'Nest des Phönix', 'italian': 'Trespolo della fenice', 'japanese': 'フェニックスルースト',
                           'korean': '불사조의 횃대', 'polish': 'Grzęda Feniksa', 'russian': 'Гнездо Феникса',
                           'spanish': 'Gallo de Phoenix', 'taiwanese': '斐尼克斯的棲身處'},
                   103792: {'chinese': '青草点', 'english': 'Grassy Point', 'french': 'Grassy Point', 'german': 'Grasland',
                            'italian': 'Prato Erboso', 'japanese': 'グラッシーポイント', 'korean': '그래시 포인트',
                            'polish': 'Trawiasty Przylądek', 'russian': 'Грасси-Пойнт', 'spanish': 'Punto Césped',
                            'taiwanese': '青草點'},
                   103793: {'chinese': '《信差日报》', 'english': 'The Daily Courier', 'french': 'La Gazette',
                            'german': 'Der Tageskurier', 'italian': 'Daily Courier', 'japanese': 'デイリー・クーリエ',
                            'korean': '데일리 커리어', 'polish': 'Kurier Codzienny', 'russian': '"Курьер"',
                            'spanish': 'El Correo Diario', 'taiwanese': '《信差日報》'},
                   103794: {'chinese': '九头蛇岛', 'english': 'Hydra Island', 'french': "Île de l'Hydre",
                            'german': 'Wasserschlangeninsel', 'italian': "Isola dell'Idra", 'japanese': 'ヒュドラ島',
                            'korean': '히드라 섬', 'polish': 'Wyspa Hydry', 'russian': 'Хайдра-Айленд',
                            'spanish': 'Isla Hidra', 'taiwanese': '九頭蛇島'},
                   103795: {'chinese': '小教堂岛', 'english': 'Chapel Island', 'french': 'Île de la Pénitence',
                            'german': 'Kapellen-Eiland', 'italian': 'Isola della Cappella', 'japanese': 'チャペル島',
                            'korean': '채플 섬', 'polish': 'Wyspa Kaplicy', 'russian': 'Чапел-Айленд',
                            'spanish': 'Isla Capilla', 'taiwanese': '小教堂島'},
                   103796: {'chinese': '乔治城', 'english': 'Jorgtown', 'french': 'Jorgtown', 'german': 'Jorgtown',
                            'italian': 'Jorgtown', 'japanese': 'ヨーグタウン', 'korean': '요그타운', 'polish': 'Jorgtown',
                            'russian': 'Йоргтаун', 'spanish': 'Villajorge', 'taiwanese': '喬治城'},
                   103797: {'chinese': '老奈特的藏身处', 'english': "Old Nate's Hideaway", 'french': 'Refuge du Vieux Nate',
                            'german': 'Old Nates Versteck', 'italian': 'Rifugio del vecchio Nate',
                            'japanese': 'オールド・ネイトの隠れ家', 'korean': '올드 네이트의 은신처', 'polish': "Kryjówka Starego Nate'a",
                            'russian': 'Убежище старины Нейта', 'spanish': 'Escondite del viejo Nate',
                            'taiwanese': '老奈特的藏身處'},
                   112147: {'chinese': '皇家瀑布', 'english': 'Crown Falls', 'french': 'Crown Falls',
                            'german': 'Crown Falls', 'italian': 'Cascate della Corona', 'japanese': 'クラウンフォールズ',
                            'korean': '크라운 폴스', 'polish': 'Crown Falls', 'russian': 'Каскады величия',
                            'spanish': 'Cascada Coronada', 'taiwanese': '皇家瀑布'},
                   113747: {'chinese': '沙尔马甘地', 'english': 'Salmagundi', 'french': 'Salmagundi', 'german': 'Salmagundi',
                            'italian': 'Salmagundi', 'japanese': 'サルマガンディー', 'korean': '살마건디', 'polish': 'Salmagundi',
                            'russian': 'Салмагунди', 'spanish': 'Ensaladilla', 'taiwanese': '沙爾馬甘地'},
                   114313: {'chinese': '伊格鲁维克', 'english': 'Igluvik', 'french': 'Igluvik', 'german': 'Igluvik',
                            'italian': 'Igluvik', 'japanese': 'イグルービク', 'korean': '이글루빅', 'polish': 'Igluvik',
                            'russian': 'Иглувик', 'spanish': 'Igluvik', 'taiwanese': '伊格魯維克'},
                   114314: {'chinese': '峡湾之地', 'english': 'Fjordland', 'french': 'Fjordland', 'german': 'Fjordland',
                            'italian': 'Fjordland', 'japanese': 'フィヨルドランド', 'korean': '피오르드랜드', 'polish': 'Fjordland',
                            'russian': 'Фьордланд', 'spanish': 'Fjordland', 'taiwanese': '峽灣之地'},
                   114315: {'chinese': '维克贾瑞', 'english': 'Vikjarek', 'french': 'Vikjarek', 'german': 'Vikjarek',
                            'italian': 'Vikjarek', 'japanese': 'ビキジャレク', 'korean': '비캬레크', 'polish': 'Vikjarek',
                            'russian': 'Викьярек', 'spanish': 'Vikjarek', 'taiwanese': '維克賈瑞'},
                   114316: {'chinese': '纳阿克', 'english': 'Naak', 'french': 'Naak', 'german': 'Naak', 'italian': 'Naak',
                            'japanese': 'ナーク', 'korean': '나아크', 'polish': 'Naak', 'russian': 'Наак', 'spanish': 'Naak',
                            'taiwanese': '納阿克'},
                   114317: {'chinese': '坠望', 'english': 'Hopefell', 'french': 'Hopefell', 'german': 'Hopefell',
                            'italian': 'Hopefell', 'japanese': 'ホプフェル', 'korean': '호프펠', 'polish': 'Hopefell',
                            'russian': 'Хоупфелл', 'spanish': 'Desesperanza', 'taiwanese': '墜望'},
                   114318: {'chinese': '海雀湾', 'english': 'Auk Bay', 'french': 'Auk Bay', 'german': 'Auk Bay',
                            'italian': 'Auk Bay', 'japanese': 'アウクベイ', 'korean': '바다오리 만', 'polish': 'Zatoka Alek',
                            'russian': 'Ок-Бэй', 'spanish': 'Bahía Auk', 'taiwanese': '海雀灣'},
                   114319: {'chinese': '北极海角', 'english': 'Cape Polaris', 'french': 'Cape Polaris',
                            'german': 'Cape Polaris', 'italian': 'Cape Polaris', 'japanese': 'ケープポラリス',
                            'korean': '극광 곶', 'polish': 'Przylądek Polaris', 'russian': 'Кейп-Полярис',
                            'spanish': 'Cabo de Polaris', 'taiwanese': '北極海角'},
                   114320: {'chinese': '白色水湾', 'english': 'White Inlet', 'french': 'White Inlet',
                            'german': 'White Inlet', 'italian': 'White Inlet', 'japanese': 'ホワイトインレット',
                            'korean': '백색 만', 'polish': 'Biała Zatoka', 'russian': 'Уайт-инлет',
                            'spanish': 'Ensenada Blanca', 'taiwanese': '白色水灣'},
                   114321: {'chinese': '施皮茨贝格', 'english': 'Spitzberg', 'french': 'Spitzberg', 'german': 'Spitzberg',
                            'italian': 'Spitzberg', 'japanese': 'スピツバーグ', 'korean': '스피츠버그', 'polish': 'Spitzberg',
                            'russian': 'Шпицберг', 'spanish': 'Spitzberg', 'taiwanese': '施皮茨貝格'},
                   114322: {'chinese': '冰霜要塞', 'english': 'Fort Frost', 'french': 'Fort Frost', 'german': 'Fort Frost',
                            'italian': 'Fort Frost', 'japanese': 'フォートフロスト', 'korean': '포트 프로스트',
                            'polish': 'Fort Frost', 'russian': 'Форт-Фрост', 'spanish': 'Fuerte Frío',
                            'taiwanese': '冰霜要塞'},
                   115244: {'chinese': '风暴海角', 'english': 'Cape Storm', 'french': 'Cape Storm', 'german': 'Cape Storm',
                            'italian': 'Cape Storm', 'japanese': 'ケープストーム', 'korean': '폭풍 곶',
                            'polish': 'Przylądek Sztormów', 'russian': 'Кейп-Сторм', 'spanish': 'Cabo de las Tormentas',
                            'taiwanese': '風暴海角'},
                   115245: {'chinese': '奇基图兀克', 'english': 'Qikigtuuk', 'french': 'Qikigtuuk', 'german': 'Qikigtuuk',
                            'italian': 'Qikigtuuk', 'japanese': 'キキグツーク', 'korean': '키키투우크', 'polish': 'Qikigtuuk',
                            'russian': 'Кикигтуук', 'spanish': 'Qikigtuuk', 'taiwanese': '奇基圖兀克'},
                   115246: {'chinese': '阿库维克', 'english': 'Akuvik', 'french': 'Akuvik', 'german': 'Akuvik',
                            'italian': 'Akuvik', 'japanese': 'アクビク', 'korean': '아쿠비크', 'polish': 'Akuvik',
                            'russian': 'Акувик', 'spanish': 'Akuvik', 'taiwanese': '阿庫維克'},
                   115247: {'chinese': '冰冷港口', 'english': 'Cold Harbour', 'french': 'Cold Harbour',
                            'german': 'Cold Harbour', 'italian': 'Cold Harbour', 'japanese': 'コールドハーバー',
                            'korean': '한랭지 항구', 'polish': 'Zimna Przystań', 'russian': 'Колд-Харбор',
                            'spanish': 'Puerto Helado', 'taiwanese': '冰冷港口'},
                   115248: {'chinese': '极匹萨', 'english': 'Kipisa', 'french': 'Kipisa', 'german': 'Kipisa',
                            'italian': 'Kipisa', 'japanese': 'キピサ', 'korean': '키피사', 'polish': 'Kipisa',
                            'russian': 'Киписа', 'spanish': 'Kipisa', 'taiwanese': '極匹薩'},
                   115249: {'chinese': '阿普帕鲁克', 'english': 'Uppaluk', 'french': 'Uppaluk', 'german': 'Uppaluk',
                            'italian': 'Uppaluk', 'japanese': 'ウッパルク', 'korean': '우팔루크', 'polish': 'Uppaluk',
                            'russian': 'Уппалук', 'spanish': 'Uppaluk', 'taiwanese': '阿普帕魯克'},
                   115250: {'chinese': '温斯克', 'english': 'Winsk', 'french': 'Winsk', 'german': 'Winsk',
                            'italian': 'Winsk', 'japanese': 'ウィンスク', 'korean': '윈스크', 'polish': 'Winsk',
                            'russian': 'Винск', 'spanish': 'Winsk', 'taiwanese': '溫斯克'},
                   115251: {'chinese': '布邬塔克', 'english': 'Buutak', 'french': 'Buutak', 'german': 'Buutak',
                            'italian': 'Buutak', 'japanese': 'ブータク', 'korean': '부우타크', 'polish': 'Buutak',
                            'russian': 'Буутак', 'spanish': 'Buutak', 'taiwanese': '布鄔塔克'},
                   115252: {'chinese': '希尼弗斯搭鲁', 'english': 'Snifsdalur', 'french': 'Snifsdalur',
                            'german': 'Snifsdalur', 'italian': 'Snifsdalur', 'japanese': 'スニフスダル', 'korean': '스니프달루르',
                            'polish': 'Snifsdalur', 'russian': 'Снифсдалур', 'spanish': 'Snifsdalur',
                            'taiwanese': '希尼弗斯搭魯'},
                   115253: {'chinese': '比亚纳峡湾', 'english': 'Bjarnafjord', 'french': 'Bjarnafjord',
                            'german': 'Bjarnafjord', 'italian': 'Bjarnafjord', 'japanese': 'ビャルナフィヨルド',
                            'korean': '비야나피오르드', 'polish': 'Bjarnafjord', 'russian': 'Бьярнафьорд',
                            'spanish': 'Bjarnafjord', 'taiwanese': '比亞納峽灣'},
                   115254: {'chinese': '长青湖', 'english': 'Lake Evergreen', 'french': 'Lake Evergreen',
                            'german': 'Lake Evergreen', 'italian': 'Lake Evergreen', 'japanese': 'レイクエバーグリーン',
                            'korean': '에버그린 호수', 'polish': 'Zimozielone Jezioro', 'russian': 'Лейк-Эвергрин',
                            'spanish': 'Lago Perenne', 'taiwanese': '長青湖'},
                   115255: {'chinese': '香草冰川', 'english': 'Vanilla Glacier', 'french': 'Vanilla Glacier',
                            'german': 'Vanilla Glacier', 'italian': 'Vanilla Glacier', 'japanese': 'バニラグレイシア',
                            'korean': '바닐라 빙하', 'polish': 'Waniliowy Lodowiec', 'russian': 'Ванилла-Гласье',
                            'spanish': 'Glaciar Vainilla', 'taiwanese': '香草冰川'},
                   115256: {'chinese': '鹰川', 'english': 'Eagle River', 'french': 'Eagle River', 'german': 'Eagle River',
                            'italian': 'Eagle River', 'japanese': 'イーグルリバー', 'korean': '이글 리버', 'polish': 'Orla Rzeka',
                            'russian': 'Игл-Ривер', 'spanish': 'Río Águila', 'taiwanese': '鷹川'},
                   115257: {'chinese': '伊努克维客', 'english': 'Inukvik', 'french': 'Inukvik', 'german': 'Inukvik',
                            'italian': 'Inukvik', 'japanese': 'イヌクビク', 'korean': '이누크비크', 'polish': 'Inukvik',
                            'russian': 'Инуквик', 'spanish': 'Inukvik', 'taiwanese': '伊努克維客'},
                   116355: {'chinese': '威廉王岛', 'english': 'King William Island', 'french': 'King William Island',
                            'german': 'King William Island', 'italian': 'Isola di Re William', 'japanese': 'キングウィリアム島',
                            'korean': '킹윌리엄섬', 'polish': 'Wyspa Króla Wilhelma', 'russian': 'Остров Кинг-Вильям',
                            'spanish': 'Isla del Rey William', 'taiwanese': '威廉王島'},
                   117363: {'chinese': '基维图乌', 'english': 'Kivitöö', 'french': 'Kivitöö', 'german': 'Kivitöö',
                            'italian': 'Kivitöö', 'japanese': 'キビトー', 'korean': '키비퇴', 'polish': 'Kivitöö',
                            'russian': 'Кивитоо', 'spanish': 'Kivitöö', 'taiwanese': '基維圖烏'},
                   117364: {'chinese': '突起镇', 'english': 'Post Town', 'french': 'Post Town', 'german': 'Post Town',
                            'italian': 'Post Town', 'japanese': 'ポストタウン', 'korean': '포스트 타운', 'polish': 'Post Town',
                            'russian': 'Пост-Таун', 'spanish': 'Pueblo Postal', 'taiwanese': '突起鎮'},
                   117365: {'chinese': '座头鲸海湾', 'english': 'Humpback Bay', 'french': 'Humpback Bay',
                            'german': 'Humpback Bay', 'italian': 'Humpback Bay', 'japanese': 'ハンプバックベイ',
                            'korean': '혹등고래 만', 'polish': 'Zatoka Humbaków', 'russian': 'Хампбэк-Бэй',
                            'spanish': 'Bahía Jorobada', 'taiwanese': '座頭鯨海灣'},
                   117366: {'chinese': '海豹水湾', 'english': 'Seal Inlet', 'french': 'Seal Inlet', 'german': 'Seal Inlet',
                            'italian': 'Seal Inlet', 'japanese': 'シールインレット', 'korean': '바다표범 만', 'polish': 'Zatoka Fok',
                            'russian': 'Сил-Инлет', 'spanish': 'Ensenada de las Focas', 'taiwanese': '海豹水灣'},
                   117367: {'chinese': '恒冬港口', 'english': 'Port Longwinter', 'french': 'Port Longwinter',
                            'german': 'Port Longwinter', 'italian': 'Port Longwinter', 'japanese': 'ポートロングウィンター',
                            'korean': '포트 롱윈터', 'polish': 'Port Longwinter', 'russian': 'Порт-Лонгвинтер',
                            'spanish': 'Puerto Invernal', 'taiwanese': '恆冬港口'},
                   117368: {'chinese': '楚科奇岛', 'english': 'Chuckchi Island', 'french': 'Chuckchi Island',
                            'german': 'Chuckchi Island', 'italian': 'Isola di Chuckchi', 'japanese': 'チュクチ島',
                            'korean': '척치 섬', 'polish': 'Wyspa Chuckchi', 'russian': 'Остров Чукчей',
                            'spanish': 'Isla Chuckchi', 'taiwanese': '楚科奇島'},
                   117369: {'chinese': '萨阿密水湾', 'english': 'Saami Inlet', 'french': 'Saami Inlet',
                            'german': 'Saami Inlet', 'italian': 'Saami Inlet', 'japanese': 'サーミインレット', 'korean': '사미 만',
                            'polish': 'Zatoka Saami', 'russian': 'Саами-Инлет', 'spanish': 'Ensenada Saami',
                            'taiwanese': '薩阿密水灣'},
                   117370: {'chinese': '绿刃', 'english': 'Greenknife', 'french': 'Greenknife', 'german': 'Greenknife',
                            'italian': 'Greenknife', 'japanese': 'グリーンナイフ', 'korean': '그린나이프', 'polish': 'Greenknife',
                            'russian': 'Гриннайф', 'spanish': 'Tajoverde', 'taiwanese': '綠刃'},
                   117371: {'chinese': '阿尔卑斯', 'english': 'Alpine', 'french': 'Alpine', 'german': 'Alpine',
                            'italian': 'Alpine', 'japanese': 'アルパイン', 'korean': '알파인', 'polish': 'Alpine',
                            'russian': 'Алпайн', 'spanish': 'Alpino', 'taiwanese': '阿爾卑斯'},
                   117372: {'chinese': '布兰克点', 'english': 'Point Blanc', 'french': 'Point Blanc',
                            'german': 'Point Blanc', 'italian': 'Point Blanc', 'japanese': 'ポイントブランク',
                            'korean': '포인트 블랑', 'polish': 'Point Blanc', 'russian': 'Пойнт-Блан',
                            'spanish': 'Punta Blanca', 'taiwanese': '布蘭克點'},
                   117373: {'chinese': '努奇亚特', 'english': 'Nuqiat', 'french': 'Nuqiat', 'german': 'Nuqiat',
                            'italian': 'Nuqiat', 'japanese': 'ヌキアト', 'korean': '누키앗', 'polish': 'Nuqiat',
                            'russian': 'Нукиат', 'spanish': 'Nuqiat', 'taiwanese': '努奇亞特'},
                   117374: {'chinese': '驯鹿站', 'english': 'Caribou Station', 'french': 'Caribou Station',
                            'german': 'Caribou Station', 'italian': 'Caribou Station', 'japanese': 'カリブーステーション',
                            'korean': '카리부 스테이션', 'polish': 'Stacja Karibu', 'russian': 'Карибу-Стейшн',
                            'spanish': 'Estación Caribú', 'taiwanese': '馴鹿站'},
                   117375: {'chinese': '奥古斯都王子岛', 'english': 'Prince Augustus Island',
                            'french': 'Prince Augustus Island', 'german': 'Prince Augustus Island',
                            'italian': 'Isola del Principe Augusto', 'japanese': 'プリンスオーガスタス島',
                            'korean': '프린스 아우구스투스 섬', 'polish': 'Wyspa Księcia Augusta',
                            'russian': 'Остров Принс-Августус', 'spanish': 'Isla del Príncipe Augustus',
                            'taiwanese': '奧古斯都王子島'},
                   117376: {'chinese': '诺德维特岛', 'english': 'Nordveit Island', 'french': 'Nordveit Island',
                            'german': 'Nordveit Island', 'italian': 'Isola di Nordveit', 'japanese': 'ノルドベイド島',
                            'korean': '노르드베이트 섬', 'polish': 'Wyspa Nordveit', 'russian': 'Остров Нордвеит',
                            'spanish': 'Isla Nordveit', 'taiwanese': '諾德維特島'},
                   117377: {'chinese': '焦虑岛', 'english': 'Tensing Island', 'french': 'Tensing Island',
                            'german': 'Tensing Island', 'italian': 'Isola di Tensing', 'japanese': 'テンシング島',
                            'korean': '텐싱 섬', 'polish': 'Wyspa Tensing', 'russian': 'Остров Тенсинг',
                            'spanish': 'Isla Tensing', 'taiwanese': '焦慮島'},
                   117378: {'chinese': '固执港口', 'english': 'Port Defiant', 'french': 'Port Defiant',
                            'german': 'Port Defiant', 'italian': 'Port Defiant', 'japanese': 'ポートデファイアント',
                            'korean': '포트 데피안트', 'polish': 'Port Defiant', 'russian': 'Порт-Дифайент',
                            'spanish': 'Puerto Desafío', 'taiwanese': '固執港口'},
                   117379: {'chinese': '卡亚努克', 'english': 'Qaanuq', 'french': 'Qaanuq', 'german': 'Qaanuq',
                            'italian': 'Qaanuq', 'japanese': 'カーヌク', 'korean': '카아누크', 'polish': 'Qaanuq',
                            'russian': 'Кваанук', 'spanish': 'Qaanuq', 'taiwanese': '卡亞努克'},
                   117380: {'chinese': '绝望湾', 'english': 'Desperation Bay', 'french': 'Desperation Bay',
                            'german': 'Desperation Bay', 'italian': 'Desperation Bay', 'japanese': 'デスパレーションベイ',
                            'korean': '절망의 만', 'polish': 'Zatoka Desperacji', 'russian': 'Десперейшн-Бэй',
                            'spanish': 'Bahía de las Lágrimas', 'taiwanese': '絕望灣'},
                   117381: {'chinese': '忧愁要塞', 'english': 'Fort Worry', 'french': 'Fort Worry', 'german': 'Fort Worry',
                            'italian': 'Fort Worry', 'japanese': 'フォートウォリー', 'korean': '포트 워리', 'polish': 'Fort Worry',
                            'russian': 'Форт-Ворри', 'spanish': 'Fuerte Desazón', 'taiwanese': '憂愁要塞'},
                   117382: {'chinese': '灰色海滩', 'english': 'Grey Beach', 'french': 'Grey Beach', 'german': 'Grey Beach',
                            'italian': 'Grey Beach', 'japanese': 'グレービーチ', 'korean': '회색 해안', 'polish': 'Szara Plaża',
                            'russian': 'Грей-Бич', 'spanish': 'Playa Gris', 'taiwanese': '灰色海灘'},
                   117383: {'chinese': '最终避风港', 'english': 'Last Haven', 'french': 'Last Haven', 'german': 'Last Haven',
                            'italian': 'Last Haven', 'japanese': 'ラストヘイブン', 'korean': '라스트 헤이븐',
                            'polish': 'Ostatnia Przystań', 'russian': 'Ласт-Хейвен', 'spanish': 'Último Refugio',
                            'taiwanese': '最終避風港'},
                   117384: {'chinese': '邓克雷吉', 'english': 'Duncraigie', 'french': 'Duncraigie', 'german': 'Duncraigie',
                            'italian': 'Duncraigie', 'japanese': 'ダンクレイジー', 'korean': '던크레이기', 'polish': 'Duncraigie',
                            'russian': 'Данкрейджи', 'spanish': 'Duncraigie', 'taiwanese': '鄧克雷吉'},
                   117385: {'chinese': '澳俞提图克', 'english': 'Auyuittuq', 'french': 'Auyuittuq', 'german': 'Auyuittuq',
                            'italian': 'Auyuittuq', 'japanese': 'オーユイタック', 'korean': '아우유이투크', 'polish': 'Auyuittuq',
                            'russian': 'Ауюиттук', 'spanish': 'Auyuittuq', 'taiwanese': '澳俞提圖克'},
                   117386: {'chinese': '培瑞格瑞港口', 'english': 'Port Peregrine', 'french': 'Port Peregrine',
                            'german': 'Port Peregrine', 'italian': 'Port Peregrine', 'japanese': 'ポートペレグリン',
                            'korean': '포트 페레그린', 'polish': 'Port Peregrine', 'russian': 'Порт-Перегрин',
                            'spanish': 'Puerto Peregrino', 'taiwanese': '培瑞格瑞港口'},
                   117387: {'chinese': '雪靴港口', 'english': 'Fort Snowshoe', 'french': 'Fort Snowshoe',
                            'german': 'Fort Snowshoe', 'italian': 'Fort Snowshoe', 'japanese': 'フォートスノーショア',
                            'korean': '포트 스노우슈', 'polish': 'Fort Snowshoe', 'russian': 'Форт-Сноушу',
                            'spanish': 'Fuerte Raqueta', 'taiwanese': '雪靴港口'},
                   117388: {'chinese': '狼溪', 'english': 'Wolf Creek', 'french': 'Wolf Creek', 'german': 'Wolf Creek',
                            'italian': 'Wolf Creek', 'japanese': 'ウルフクリーク', 'korean': '늑대 만', 'polish': 'Wilczy Potok',
                            'russian': 'Вульф-Крик', 'spanish': 'Arroyo Lupino', 'taiwanese': '狼溪'},
                   120367: {'chinese': '奇杜西·安尼托尼', 'english': 'Kidusi Anitoni', 'french': 'Kidusi Anitoni',
                            'german': 'Kidusi Anitoni', 'italian': 'Kidusi Anitoni', 'japanese': 'キドゥーシ・アニトーニ',
                            'korean': '키두시 아니토니', 'polish': 'Kidusi Anitoni', 'russian': 'Кидуси-Анитони',
                            'spanish': 'Kidusi Anitoni', 'taiwanese': '奇杜西．安尼東尼'},
                   120368: {'chinese': '安尔雷布', 'english': 'Angereb', 'french': 'Angereb', 'german': 'Angereb',
                            'italian': 'Angereb', 'japanese': 'アンゲレブ', 'korean': '앙게레브', 'polish': 'Angereb',
                            'russian': 'Ангереб', 'spanish': 'Angereb', 'taiwanese': '安爾雷布'},
                   120369: {'chinese': '瓦哈德瑟', 'english': 'Waha Desher', 'french': 'Waha Desher',
                            'german': 'Waha Desher', 'italian': 'Waha Desher', 'japanese': 'ワハ・デッシャー',
                            'korean': '와하 데셔', 'polish': 'Waha Desher', 'russian': 'Ваха-Дешер',
                            'spanish': 'Waha Desher', 'taiwanese': '瓦哈德瑟'},
                   120370: {'chinese': '塔伯里姆', 'english': 'Taborime', 'french': 'Taborimé', 'german': 'Taborime',
                            'italian': 'Taborime', 'japanese': 'タボリメ', 'korean': '타보림', 'polish': 'Taborime',
                            'russian': 'Таборим', 'spanish': 'Taborime', 'taiwanese': '塔伯里姆'},
                   120371: {'chinese': '小克拉伦斯岛', 'english': 'Little Clarence', 'french': 'Little Clarence',
                            'german': 'Little Clarence', 'italian': 'Little Clarence', 'japanese': 'リトルクラレンス',
                            'korean': '리틀 클래런스', 'polish': 'Little Clarence', 'russian': 'Литтл-Кларенс',
                            'spanish': 'Little Clarence', 'taiwanese': '小克拉倫斯島'},
                   131069: {'chinese': '游牧民牧场', 'english': 'Nomadic Pasture Land', 'french': 'Terre de pâture nomade',
                            'german': 'Nomadisches Weideland', 'italian': 'Pascoli dei nomadi', 'japanese': '遊牧民の牧草地',
                            'korean': '방랑 목초지', 'polish': 'Pastwisko koczowników', 'russian': 'Пастбищные угодья',
                            'spanish': 'Tierra de pasto nómada', 'taiwanese': '游牧民牧場'},
                   137954: {'chinese': '祖尔图纳', 'english': 'La Xultuna', 'french': 'La Xultuna', 'german': 'La Xultuna',
                            'italian': 'La Xultuna', 'japanese': 'ラ・シュルツーナ', 'korean': '라 줄투나', 'polish': 'La Xultuna',
                            'russian': 'Ла-Зультуна', 'spanish': 'La Xultuna', 'taiwanese': '祖爾圖納'},
                   143868: {'chinese': '普拉塔荒地', 'english': 'Deserto de Prata', 'french': 'Deserto de Prata',
                            'german': 'Deserto de Prata', 'italian': 'Deserto de Prata', 'japanese': 'プラータ砂漠',
                            'korean': '데세르토 데 프라타', 'polish': 'Deserto de Prata', 'russian': 'Дезерту-де-Прата',
                            'spanish': 'Deserto de Prata', 'taiwanese': '普拉塔荒地'},
                   143912: {'chinese': '卢托岛', 'english': 'Ilha de Luto', 'french': 'Isla de Luto',
                            'german': 'Isla de Luto', 'italian': 'Isla de Luto', 'japanese': 'イスラ・デ・ルト',
                            'korean': '비탄의 섬', 'polish': 'Isla de Luto', 'russian': 'Изла-де-Луту',
                            'spanish': 'Isla de Luto', 'taiwanese': '盧托島'},
                   143913: {'chinese': '多洛尔岛', 'english': 'Ilha do Vazio', 'french': 'Isla del Dolor',
                            'german': 'Isla del Dolor', 'italian': 'Isla del Dolor', 'japanese': 'イスラ・デル・ドロル',
                            'korean': '고통의 섬', 'polish': 'Isla de Dolor', 'russian': 'Изла-дель-Долор',
                            'spanish': 'Isla del Dolor', 'taiwanese': '多洛爾島'}},
    "third_parties": [19, 22, 86, 20, 16, 21, 100, 101, 99, 97],
    "streets": {
        1: {'id': 1, 'name': 'Dirt Street', 'guid': 1000178, 'road': True, 'paved': False, 'speed': 1, 'harbour': False,
            'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        2: {'id': 2, 'name': 'Stone Street', 'guid': 1010035, 'road': True, 'paved': True, 'speed': 1.5,
            'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        3: {'id': 3, 'name': 'Rails', 'guid': 1010136, 'road': False, 'paved': False, 'speed': 1, 'harbour': False,
            'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 115, 'G': 94, 'B': 66}},
        4: {'id': 4, 'name': 'Crossing Rails-Street', 'guid': 1010165, 'road': True, 'paved': False, 'speed': 1,
            'harbour': False, 'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        6: {'id': 6, 'name': 'Crossing Rails-FastStreet', 'guid': 1010183, 'road': True, 'paved': True, 'speed': 1.5,
            'harbour': False, 'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        7: {'id': 7, 'name': 'RailsUnderBuilding', 'guid': 1010584, 'road': False, 'paved': False, 'speed': 1,
            'harbour': False, 'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 115, 'G': 94, 'B': 66}},
        63: {'id': 63, 'name': 'Crossing Rails-Quay', 'guid': 80138, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': True, 'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 176, 'G': 176, 'B': 176}},
        10: {'id': 10, 'name': 'Dirt Bridge Groundplate', 'guid': 101383, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': True, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        19: {'id': 19, 'name': 'Stone Bridge Groundplate', 'guid': 101588, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': False, 'rail': False, 'bridge': True, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        25: {'id': 25, 'name': 'Simple Street Colony01', 'guid': 101308, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        26: {'id': 26, 'name': 'Fast Street Colony01', 'guid': 101309, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        41: {'id': 41, 'name': 'Snow Street', 'guid': 112113, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        5: {'id': 5, 'name': 'AF | Rails', 'guid': 119035, 'road': False, 'paved': False, 'speed': 1, 'harbour': False,
            'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
            'color': {'A': 255, 'R': 115, 'G': 94, 'B': 66}},
        45: {'id': 45, 'name': 'AF | Crossing Rails-Street', 'guid': 273697, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': True, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        46: {'id': 46, 'name': 'AF | Crossing Rails-FastStreet', 'guid': 273698, 'road': True, 'paved': True,
             'speed': 1.5, 'harbour': False, 'rail': True, 'bridge': False, 'irrigation': False, 'canal': False,
             'dirt_canal': False, 'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        47: {'id': 47, 'name': 'AF | Crossing Rails-Pipe', 'guid': 273699, 'road': False, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': True, 'bridge': False, 'irrigation': True, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 115, 'G': 94, 'B': 66}},
        51: {'id': 51, 'name': 'Canal', 'guid': 112842, 'road': False, 'paved': False, 'speed': 1, 'harbour': False,
             'rail': False, 'bridge': False, 'irrigation': True, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 100, 'G': 149, 'B': 237}},
        54: {'id': 54, 'name': 'Crossing Canal-Street', 'guid': 117786, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': True, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        53: {'id': 53, 'name': 'Crossing Canal-FastStreet', 'guid': 127913, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': True, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        27: {'id': 27, 'name': 'AF | Fast Street', 'guid': 119029, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        52: {'id': 52, 'name': 'AF | Dirt Street', 'guid': 114523, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        44: {'id': 44, 'name': 'Quay Street Moderate', 'guid': 601443, 'road': True, 'paved': False, 'speed': 1,
             'harbour': True, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 176, 'G': 176, 'B': 176}},
        43: {'id': 43, 'name': 'Quay Street SA', 'guid': 131865, 'road': True, 'paved': False, 'speed': 1,
             'harbour': True, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 176, 'G': 176, 'B': 176}},
        76: {'id': 76, 'name': 'Courtyard Groundplate', 'guid': 24774, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': False,
             'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        70: {'id': 70, 'name': 'Canal System #1 (beautiful pond)', 'guid': 601933, 'road': False, 'paved': False,
             'speed': 1, 'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': True,
             'dirt_canal': False, 'color': {'A': 255, 'R': 100, 'G': 149, 'B': 237}},
        71: {'id': 71, 'name': '- Crossing Canal-Street', 'guid': 451, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': True, 'dirt_canal': False,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        72: {'id': 72, 'name': '- Crossing Canal-FastStreet', 'guid': 452, 'road': True, 'paved': True, 'speed': 1.5,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': True, 'dirt_canal': False,
             'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}},
        73: {'id': 73, 'name': 'Canal System #2 (sewers)', 'guid': 453, 'road': False, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': True,
             'color': {'A': 255, 'R': 99, 'G': 103, 'B': 67}},
        74: {'id': 74, 'name': '- Crossing DirtCanal-Street', 'guid': 510, 'road': True, 'paved': False, 'speed': 1,
             'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False, 'dirt_canal': True,
             'color': {'A': 255, 'R': 220, 'G': 187, 'B': 124}},
        75: {'id': 75, 'name': '- Crossing DirtCanal-FastStreet', 'guid': 511, 'road': True, 'paved': True,
             'speed': 1.5, 'harbour': False, 'rail': False, 'bridge': False, 'irrigation': False, 'canal': False,
             'dirt_canal': True, 'color': {'A': 255, 'R': 169, 'G': 169, 'B': 169}}},
    "directions": {0: "Up", 1: "Left", 2: "Down", 3: "Right"},
    "direction_offsets": {601460: -1, 601463: 1, 131777: 1, 131778: 1},
    "farm_modules": {1010262: 1010270, 1010263: 1010271, 1010264: 1010272, 1010265: 1010273, 1010267: 1010275,
                     1010269: 1010277, 100654: 100656, 100655: 100657, 101331: 101332, 1010470: 100455, 1010471: 100454,
                     100448: 100455, 1010329: 1010334, 1010330: 1010335, 1010331: 1010336, 1010332: 1010337,
                     1010333: 1010338, 101251: 101253, 101263: 101280, 101269: 101281, 101270: 101282, 101272: 101283,
                     1010561: 100524, 102282: 100455, 102283: 100454, 110935: 111104, 114141: 111104, 112676: 112677,
                     112682: 112683, 112690: 113751, 249947: 249950, 269850: 1010270, 269851: 1010270, 114448: 114490,
                     114447: 114488, 114450: 114492, 114451: 114494, 114452: 114495, 114453: 114496, 114439: 114499,
                     114456: 114498, 601470: 601463, 24836: 100524, 24844: 24845, 24794: 1010334, 24798: 1010334,
                     25003: 101282, 25005: 101253, 25006: 1010338, 25009: 1010337, 25019: 1010273, 25020: 25890,
                     25128: 1010270, 24768: 24770, 962: 964, 963: 2274, 4258: 4259, 24658: 1010277},
    "decentered_buildings": {114751: [[-2.0, -1.5], [-2.0, 1.5], [2.0, 1.5], [2.0, -1.5]],
                             1010278: [[-2.0, -2.5], [-2.0, 2.5], [9.0, 2.5], [9.0, -2.5]],
                             1010310: [[-2.0, -3.0], [-2.0, 3.0], [8.0, 3.0], [8.0, -3.0]],
                             1010560: [[-2.0, -3.5], [-2.0, 2.5], [8.0, 2.5], [8.0, -3.5]],
                             1010304: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [6.5, 2.5], [6.5, -2.5]],
                             1010305: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [6.5, 2.5], [6.5, -2.5]],
                             1010307: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [6.5, 2.5], [6.5, -2.5]],
                             1010308: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [6.5, 2.5], [6.5, -2.5]],
                             1010309: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [6.5, 2.5], [6.5, -2.5]],
                             1010311: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [4.5, 2.5], [4.5, -2.5]],
                             1010500: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                       [6.5, 2.5], [1.5, 2.5]],
                             1010501: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                       [6.5, 2.5], [1.5, 2.5]],
                             1010503: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                       [6.5, 2.5], [1.5, 2.5]],
                             1010504: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                       [6.5, 2.5], [1.5, 2.5]],
                             1010505: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                       [6.5, 2.5], [1.5, 2.5]],
                             1010507: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                       [6.5, 2.5], [1.5, 2.5]],
                             1010545: [[-2.0, -2.0], [-2.0, 2.0], [1.25, 2.0], [1.25, -1.910036]],
                             1010546: [[-2.0, -2.0], [-2.0, 2.0], [1.0, 2.0], [1.0, -2.0]],
                             1010547: [[-1.5, 3.5], [-1.5, -3.5], [7.5, -3.5], [7.5, 3.5]],
                             100945: [[2.5, -2.0], [-2.5, -2.0], [-2.5, 2.0], [2.5, 2.0], [2.5, -2.0], [-2.5, -2.0],
                                      [-2.5, 2.0], [2.5, 2.0]],
                             1010517: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, 2.5], [9.0, 2.5],
                                       [9.0, -2.5], [7.0, -2.5]],
                             100510: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [9.0, 2.5], [9.0, -2.5],
                                      [8.0, -2.5], [8.0, 2.5]],
                             100511: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [8.0, -2.5]],
                             269867: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [8.0, -2.5]],
                             1010540: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, 2.5], [9.0, 2.5],
                                       [9.0, -2.5], [7.0, -2.5]],
                             100514: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [9.0, 2.5], [9.0, -2.5],
                                      [8.0, -2.5], [8.0, 2.5]],
                             100515: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [8.0, -2.5]],
                             269879: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [8.0, -2.5]],
                             1010519: [[7.0, 2.0], [7.0, -2.0], [-3.0, -2.0], [-3.0, 2.0]],
                             1010520: [[-2.0, 3.0], [-2.0, -3.0], [15.0, -3.0], [15.0, 3.0]],
                             1010521: [[-2.0, -3.5], [-2.0, 3.5], [15.0, 3.5], [15.0, -3.5]],
                             1010524: [[-2.0, -2.0], [-2.0, 2.0], [4.0, 2.0], [4.0, -2.0]],
                             100519: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             100429: [[-2.0, -4.0], [-2.0, 4.0], [23.0, 4.0], [23.0, -4.0]],
                             100781: [[-3.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-3.0, -3.5]],
                             101404: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             101403: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             100783: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             101642: [[-2.0, -2.5], [-2.0, 2.5], [13.0, 2.5], [13.0, -2.5]],
                             102474: [[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [-1.5, 2.0], [1.5, 2.0],
                                      [1.5, -2.0], [-1.5, -2.0]],
                             102475: [[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [-1.0, 1.0], [1.0, 1.0],
                                      [1.0, -1.0], [-1.0, -1.0]],
                             25931: [[-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [-1.5, 0.5], [0.5, 0.5], [1.5, 0.5],
                                     [1.5, -0.5], [0.5, -0.5]],
                             1010339: [[-3.0, -2.0], [-3.0, 4.0], [11.0, 4.0], [11.0, -2.0]],
                             101262: [[-2.0, -2.5], [-2.0, 2.5], [9.0, 2.5], [9.0, -2.5]],
                             101311: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                      [6.5, 2.5], [6.5, -2.5]],
                             101278: [[7.0, 2.0], [7.0, -2.0], [-3.0, -2.0], [-3.0, 2.0]],
                             101277: [[-2.0, 3.0], [-2.0, -3.0], [15.0, -3.0], [15.0, 3.0]],
                             101290: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [7.0, 2.5]],
                             101291: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             101292: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             101293: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [7.0, 2.5]],
                             101294: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             101295: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             101571: [[-2.0, -2.0], [-2.0, 2.0], [4.0, 2.0], [4.0, -2.0]],
                             101344: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             101329: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             101405: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             101406: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             102284: [[-2.0, -4.0], [-2.0, 4.0], [23.0, 4.0], [23.0, -4.0]],
                             100682: [[5.0, 3.5], [5.0, -4.5], [-5.0, -4.5], [-5.0, 3.5]],
                             100683: [[-5.0, -2.0], [5.0, -2.0], [5.0, 2.088846], [2.0, 2.09586], [2.0, 5.0],
                                      [-2.0, 5.0], [-2.0, 2.0], [-5.0, 2.0]],
                             100686: [[4.0, -5.0], [4.0, 5.0], [-5.0, 5.0], [-5.0, -5.0]],
                             102450: [[-2.0, -2.0], [-2.0, 2.0], [4.0, 2.0], [4.0, -2.0]],
                             101185: [[-0.5, 0.5], [0.0, 0.5], [0.0, -0.5], [-0.5, -0.5]],
                             100774: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                      [6.5, 2.5], [6.5, -2.5]],
                             100761: [[4.0, -5.0], [4.0, 5.0], [-5.0, 5.0], [-5.0, -5.0]],
                             100861: [[7.0, 2.0], [7.0, -2.0], [-3.0, -2.0], [-3.0, 2.0]],
                             1003925: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [-0.75, -1.0],
                                       [-0.75, -0.75], [-1.0, -0.75], [-1.0, -1.0]],
                             1000029: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                       [6.5, 2.5], [6.5, -2.5]],
                             614: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                   [6.5, 2.5], [1.5, 2.5]],
                             1000038: [[-2.0, -2.5], [-2.0, 2.5], [9.0, 2.5], [9.0, -2.5]],
                             1000254: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, 2.5], [9.0, 2.5],
                                       [9.0, -2.5], [7.0, -2.5]],
                             101629: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [7.0, 2.5]],
                             102182: [[4.0, -2.0], [4.0, 1.0], [-2.0, 1.0], [-2.0, -2.0]],
                             102190: [[-5.0, 3.0], [3.0, 3.0], [3.0, -3.0], [-5.0, -3.0]],
                             101343: [[-3.0, 4.0], [3.0, 4.0], [3.0, -3.0], [-2.912423, -3.0]],
                             101399: [[-3.0, 4.0], [3.0, 4.0], [3.0, -3.0], [-2.912423, -3.0]],
                             101122: [[2.5, 4.0], [-6.0, 4.0], [-6.0, -5.0], [2.5, -5.0]],
                             101335: [[-3.0, 2.0], [3.0, 2.0], [3.0, -4.0], [-3.0, -4.0]],
                             101040: [[-3.0, 2.0], [3.0, 2.0], [3.0, -4.0], [-3.0, -4.0]],
                             101186: [[-3.0, 2.0], [3.0, 1.89823], [3.0, -4.0], [-3.0, -4.0]],
                             101135: [[-3.0, 2.0], [3.0, 1.89823], [3.0, -4.0], [-3.0, -4.0]],
                             101233: [[0.0, 2.0], [0.0, -2.0], [4.0, -2.0], [4.0, 2.0]],
                             101407: [[0.0, 2.0], [0.0, -2.0], [4.0, -2.0], [4.0, 2.0]],
                             2466: [[-3.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-3.0, 1.0]],
                             2235: [[0.5, 1.5], [-1.5, 1.5], [-1.5, -0.5], [0.5, -0.5]],
                             101117: [[0.0, -3.0], [2.0, -3.0], [2.0, -0.9379623], [0.0, -0.9712749]],
                             112666: [[-2.0, 3.0], [-2.0, -3.0], [15.0, -3.0], [15.0, 3.0]],
                             112674: [[-2.0, 3.0], [5.0, 3.0], [5.0, -2.0], [-2.0, -2.0]],
                             116029: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                      [6.5, 2.5], [6.5, -2.5]],
                             116038: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                      [6.5, 2.5], [1.5, 2.5]],
                             112659: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [7.0, -2.5]],
                             112660: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [9.0, 2.5], [9.0, -2.5],
                                      [8.0, -2.5], [8.0, 2.5]],
                             112661: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [8.0, -2.5]],
                             112865: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [7.0, -2.5]],
                             112866: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [9.0, 2.5], [9.0, -2.5],
                                      [8.0, -2.5], [8.0, 2.5]],
                             112867: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [8.0, -2.5]],
                             112670: [[7.0, 2.0], [7.0, -2.0], [-3.0, -2.0], [-3.0, 2.0]],
                             116030: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             112863: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, 2.5], [9.0, 2.5],
                                      [9.0, -2.5], [7.0, -2.5]],
                             116037: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                      [6.5, 2.5], [6.5, -2.5]],
                             269086: [[-1.5, -0.5], [-1.5, -1.5], [1.5, -1.5], [1.5, -0.5], [1.5, 0.5], [-1.5, 0.5],
                                      [-1.5, 1.5], [1.5, 1.5]],
                             269784: [[1.5, 0.5], [1.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [-1.5, 0.5],
                                      [-1.5, -0.5], [-0.5, -0.5]],
                             269809: [[1.5, 0.5], [1.5, -1.5], [0.5, -1.5], [0.5, 0.5], [-0.5, 0.5], [-1.5, 0.5],
                                      [-1.5, -1.5], [-0.5, -1.5]],
                             119259: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             119281: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             270172: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             119031: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             119032: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             119033: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5]],
                             114440: [[-2.0, -3.0], [-2.0, 3.0], [11.0, 3.0], [11.0, -3.0]],
                             118729: [[-2.0, -2.5], [-2.0, 2.5], [14.0, 2.5], [14.0, -2.5]],
                             117743: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             117744: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             114544: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             120274: [[-1.5, -0.5], [-1.5, 2.5], [1.5, 2.5], [1.5, -0.5]],
                             120273: [[-1.5, -0.5], [-1.5, 2.5], [1.5, 2.5], [1.5, -0.5]],
                             120271: [[-1.5, -0.5], [-1.5, 2.5], [1.5, 2.5], [1.5, -0.5]],
                             125193: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             114626: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -3.5], [9.0, -3.5],
                                      [9.0, 3.5], [7.0, 3.5]],
                             114627: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             114628: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             114629: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -3.5], [9.0, -3.5],
                                      [9.0, 3.5], [7.0, 3.5]],
                             114630: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             114631: [[-2.0, 3.5], [8.0, 3.5], [8.0, -3.5], [-2.0, -3.5], [8.0, -2.5], [9.0, -2.5],
                                      [9.0, 2.5], [8.0, 2.5]],
                             117870: [[7.0, 2.0], [7.0, -2.0], [-3.0, -2.0], [-3.0, 2.0]],
                             117871: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             125028: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             123720: [[-0.5, -1.0], [-0.5, 1.0], [1.0, 1.0], [1.0, -1.0], [-2.25, 2.0], [-2.25, -2.0],
                                      [2.0, -2.0], [2.0, 2.0]],
                             119408: [[1.0, 1.901508], [1.0, -3.0], [-1.0, -3.0], [-1.0, 2.0]],
                             129024: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             129025: [[-1.5, -0.5], [-1.5, 1.5], [1.5, 1.5], [1.5, -0.5]],
                             119425: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -3.5], [9.0, -3.5],
                                      [9.0, 3.5], [7.0, 3.5]],
                             131065: [[-1.0, 3.0], [-1.0, -3.0], [3.0, -3.0], [3.0, 3.0]],
                             125191: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             125192: [[-2.0, 3.0], [4.0, 3.0], [4.0, -4.0], [-2.0, -4.0]],
                             114758: [[-2.0, 3.5], [7.0, 3.5], [7.0, -3.5], [-2.0, -3.5], [7.0, -3.5], [9.0, -3.5],
                                      [9.0, 3.5], [7.0, 3.5]],
                             125016: [[-0.5, 0.75], [0.5, 0.75], [0.5, -0.401974], [-0.5, -0.3759235]],
                             125017: [[0.75, 0.75], [-0.5, 0.75], [-0.5, -0.5], [0.75, -0.5]],
                             125019: [[-0.25, 0.5], [-0.25, 0.0], [0.25, 0.0], [0.25, 0.5]],
                             125020: [[-0.25, 0.5], [-0.25, 1.25], [0.5, 1.25], [0.5, 0.5]],
                             125021: [[-0.25, 0.5], [-0.25, 0.0], [0.25, 0.0], [0.25, 0.5]],
                             125022: [[0.75, 0.5], [0.75, 0.0], [0.25, 0.0], [0.25, 0.5]],
                             125027: [[0.0, -0.25], [0.0, -1.25], [-1.0, -1.25], [-1.0, -0.25]],
                             119958: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             119959: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             129382: [[-2.5, 0.5], [2.5, 0.5], [2.5, -3.5], [-2.5, -3.5]],
                             129384: [[-1.5, -0.5], [-1.5, 1.5], [1.5, 1.5], [1.5, -0.5]],
                             132509: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132510: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132511: [[-0.5, -1.0], [-0.5, 2.0], [1.5, 2.0], [1.5, -1.0]],
                             132512: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132513: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132514: [[1.5, 0.0], [1.5, 1.0], [-0.5, 1.0], [-0.5, 0.0]],
                             132515: [[0.0, 1.0], [2.0, 1.0], [2.0, -1.0], [0.0, -1.0]],
                             132517: [[-0.5, 1.0], [2.5, 1.0], [2.5, -1.0], [-0.5, -1.0]],
                             132518: [[-0.5, -0.5], [2.5, -0.5], [2.5, 1.5], [-0.5, 1.5]],
                             132519: [[-0.5, 0.5], [1.5, 0.5], [1.5, -0.5], [-0.5, -0.5]],
                             132521: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132522: [[-0.5, 0.5], [1.5, 0.5], [1.5, -0.5], [-0.5, -0.5]],
                             132523: [[-0.5, 0.5], [1.5, 0.5], [1.5, -0.5], [-0.5, -0.5]],
                             132524: [[1.0, 1.0], [-1.0, 1.0], [-1.0, -2.0], [1.0, -2.0]],
                             132542: [[1.5, -2.5], [1.5, 0.5], [-2.5, 0.5], [-2.5, -2.5]],
                             132543: [[1.5, -1.5], [1.5, 1.5], [-3.5, 1.5], [-3.5, -1.5]],
                             132374: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132375: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132376: [[-0.5, -1.0], [-0.5, 2.0], [1.5, 2.0], [1.5, -1.0]],
                             132377: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132378: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132379: [[1.5, 0.0], [1.5, 1.0], [-0.5, 1.0], [-0.5, 0.0]],
                             132380: [[0.0, 1.0], [2.0, 1.0], [2.0, -1.0], [0.0, -1.0]],
                             132382: [[-0.5, 1.0], [2.5, 1.0], [2.5, -1.0], [-0.5, -1.0]],
                             132383: [[-0.5, -0.5], [2.5, -0.5], [2.5, 1.5], [-0.5, 1.5]],
                             132384: [[-0.5, 0.5], [1.5, 0.5], [1.5, -0.5], [-0.5, -0.5]],
                             132386: [[-0.5, 1.0], [1.5, 1.0], [1.5, -1.0], [-0.5, -1.0]],
                             132387: [[-0.5, 0.5], [1.5, 0.5], [1.5, -0.5], [-0.5, -0.5]],
                             132388: [[-0.5, 0.5], [1.5, 0.5], [1.5, -0.5], [-0.5, -0.5]],
                             132389: [[1.0, 1.0], [-1.0, 1.0], [-1.0, -2.0], [1.0, -2.0]],
                             132532: [[1.5, -2.5], [1.5, 0.5], [-2.5, 0.5], [-2.5, -2.5]],
                             132539: [[1.5, -1.5], [1.5, 1.5], [-3.5, 1.5], [-3.5, -1.5]],
                             133890: [[-2.0, -4.0], [-2.0, 4.0], [23.0, 4.0], [23.0, -4.0]],
                             24844: [[-2.0, -3.0], [-2.0, 3.0], [7.0, 3.0], [7.0, -3.0]],
                             25569: [[-3.0, 4.0], [3.0, 4.0], [3.0, -3.0], [-2.912423, -3.0]],
                             144009: [[-3.0, 4.0], [3.0, 4.0], [3.0, -3.0], [-2.912423, -3.0]],
                             144010: [[-3.0, 4.0], [3.0, 4.0], [3.0, -3.0], [-2.912423, -3.0]],
                             25168: [[-0.5, -0.5], [-1.5, -0.5], [-1.5, 0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5],
                                     [1.5, 0.5], [1.5, -0.5]],
                             1375: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                    [6.5, 2.5], [1.5, 2.5]],
                             1372: [[-1.5, 1.5], [-1.5, -1.5], [1.5, -1.5], [1.5, 1.5], [1.5, -2.5], [6.5, -2.5],
                                    [6.5, 2.5], [1.5, 2.5]],
                             2399: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                    [6.5, 2.5], [6.5, -2.5]],
                             2400: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                    [6.5, 2.5], [6.5, -2.5]],
                             137764: [[-1.5, -1.5], [-0.5, -1.5], [-0.5, 0.5], [-1.5, 0.5], [1.5, 0.5], [0.5, 0.5],
                                      [0.5, -1.5], [1.5, -1.5]],
                             137765: [[-1.5, 0.5], [-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5],
                                      [1.5, -0.5], [1.5, 0.5]],
                             137789: [[-1.5, 0.5], [-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5],
                                      [1.5, -0.5], [1.5, 0.5]],
                             137790: [[-1.5, 0.5], [-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5],
                                      [1.5, 0.5], [1.5, -0.5]],
                             137772: [[0.0, -0.5], [0.0, 0.5], [-1.0, 0.5], [-1.0, -0.5], [1.0, -0.5], [1.0, 0.5],
                                      [2.0, 0.5], [2.0, -0.5]],
                             137773: [[-1.0, -0.5], [-2.0, -0.5], [-2.0, 0.5], [-1.0, 0.5], [1.0, -0.5], [1.0, 0.5],
                                      [2.0, 0.5], [2.0, -0.5]],
                             137774: [[-1.0, 0.5], [-2.0, 0.5], [-2.0, -0.5], [-1.0, -0.5], [2.0, -0.5], [3.0, -0.5],
                                      [3.0, 0.5], [2.0, 0.5]],
                             25083: [[-1.5, -0.5], [-1.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5], [0.5, 0.5],
                                     [1.5, 0.5], [1.5, -0.5]],
                             25095: [[-1.5, 0.5], [-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5],
                                     [1.5, -0.5], [1.5, 0.5]],
                             25108: [[-1.5, 0.5], [-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5],
                                     [1.5, -0.5], [1.5, 0.5]],
                             25139: [[-1.5, 0.5], [-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5],
                                     [1.5, -0.5], [1.5, 0.5]],
                             388: [[-1.5, -1.5], [-0.5, -1.5], [-0.5, 1.5], [-1.5, 1.5], [0.5, 1.5], [1.5, 1.5],
                                   [1.5, -1.5], [0.5, -1.5]], 392: [[-0.5, 1.0], [-0.5, -1.0], [1.5, -1.0], [1.5, 1.0]],
                             393: [[-0.5, -1.5], [0.5, -1.5], [0.5, -0.5], [-0.5, -0.5], [0.5, 0.5], [-0.5, 0.5],
                                   [-0.5, 1.5], [0.5, 1.5]],
                             678: [[0.5, -0.5], [1.5, -0.5], [1.5, 0.5], [0.5, 0.5], [-0.5, 0.5], [-1.5, 0.5],
                                   [-1.5, -0.5], [-0.5, -0.5]],
                             677: [[-1.5, -0.5], [-0.5, -0.5], [-0.5, 0.5], [-1.5, 0.5], [0.5, -0.5], [0.5, 0.5],
                                   [1.5, 0.5], [1.5, -0.5]],
                             24652: [[-2.0, -2.5], [-2.0, 2.5], [9.0, 2.5], [9.0, -2.5]],
                             138779: [[6.0, -6.0], [-6.0, -6.0], [-6.0, 6.0], [6.0, 6.0], [-7.0, 7.0], [-7.0, -7.0],
                                      [7.0, -7.0], [7.0, 7.0]],
                             138780: [[6.0, -6.0], [-6.0, -6.0], [-6.0, 6.0], [6.0, 6.0], [-7.0, 7.0], [-7.0, -7.0],
                                      [7.0, -7.0], [7.0, 7.0]],
                             139546: [[0.0, 4.0], [-1.0, 4.0], [-1.0, -8.0], [0.0, -8.0]],
                             24055: [[-2.0, -2.5], [-2.0, 2.5], [9.0, 2.5], [9.0, -2.5]],
                             24125: [[-1.5, 3.5], [-1.5, -3.5], [7.5, -3.5], [7.5, 3.5]],
                             24126: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                     [6.5, 2.5], [6.5, -2.5]],
                             24128: [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [1.5, -2.5], [1.5, 2.5],
                                     [6.5, 2.5], [6.5, -2.5]],
                             24129: [[-2.0, -2.0], [-2.0, 2.0], [1.0, 2.0], [1.0, -2.0]],
                             24135: [[-2.0, -3.0], [-2.0, 3.0], [7.0, 3.0], [7.0, -3.0]],
                             101303: [[-2.0, -3.0], [-2.0, 3.0], [8.0, 3.0], [8.0, -3.0]]},
    "ships": {101121: 3, 100438: 2, 100437: 1, 100440: 3, 100439: 3, 100441: 4, 102437: 3, 100442: 3, 100443: 2,
              1010062: 6, 100853: 1, 118718: 8, 119354: 3, 119360: 6, 80068: 4, 80067: 8, 102429: 1, 102430: 3,
              102431: 3, 102432: 2, 102420: 1, 102421: 3, 102419: 3, 102422: 2, 102423: 2, 102425: 3, 102428: 2,
              102427: 3, 102455: 6, 100660: 2, 100825: 3, 100828: 3, 101198: 2, 101432: 3, 100591: 3, 101387: 2,
              102237: 2, 102238: 2, 101153: 4, 101199: 2, 101151: 2, 119856: 3, 100679: 2, 101400: 2, 101960: 3,
              101143: 2, 101964: 2, 102454: 2, 102325: 2, 101218: 3, 101981: 3, 102245: 3, 101965: 2, 101248: 3,
              102452: 2, 101978: 2, 102453: 2, 101995: 2, 101982: 3, 101983: 1, 102252: 1, 100563: 1, 100564: 2,
              100565: 3, 100566: 3, 100567: 4, 100568: 3, 100569: 2, 100624: 6, 102367: 1, 102368: 2, 102369: 3,
              102370: 3, 102371: 4, 102372: 3, 102373: 2, 102374: 6, 102417: 6, 102375: 1, 102377: 3, 102378: 3,
              102380: 3, 102381: 2, 102631: 1, 102632: 1, 102633: 1, 102635: 3, 102636: 3, 102637: 3, 102638: 3,
              102639: 3, 102640: 3, 102641: 2, 102642: 2, 102643: 2, 102644: 3, 102645: 3, 102646: 3, 102689: 1,
              102610: 1, 102611: 2, 102612: 3, 102613: 3, 102614: 4, 102615: 3, 102616: 2, 102617: 6, 102577: 4,
              102578: 4, 102579: 4, 102580: 4, 102581: 4, 102582: 4, 102583: 4, 102584: 4, 102585: 4, 102586: 4,
              102587: 4, 102588: 4, 102589: 4, 102590: 4, 102591: 4, 102592: 4, 102593: 4, 102594: 4, 110688: 4,
              102298: 4, 102304: 6, 102305: 3, 102385: 3, 102387: 3, 102388: 2, 102389: 2, 102391: 3, 102571: 2,
              102393: 2, 102397: 3, 102403: 1, 102501: 2, 102506: 3, 102514: 4, 102519: 3, 102549: 4, 102556: 1,
              102563: 6, 102574: 2, 102630: 6, 102650: 3, 102656: 3, 102658: 1, 102669: 4, 102861: 6, 102880: 3,
              102881: 3, 102882: 1, 102886: 2, 103038: 3, 103039: 3, 103040: 3, 103041: 3, 103063: 3, 103070: 3,
              103087: 3, 103091: 1, 103108: 4, 110703: 4, 110704: 3, 110711: 4, 110811: 6, 110816: 3, 110827: 2,
              110829: 2, 111164: 3, 111165: 3, 111166: 2, 111168: 3, 111196: 4, 111201: 3, 112168: 4, 118928: 4,
              111253: 2, 111879: 3, 111880: 3, 111927: 6, 111928: 2, 112084: 6, 113710: 6, 111877: 6, 111878: 3,
              113878: 3, 111881: 3, 114072: 3, 80018: 4, 80023: 3, 80024: 2, 80025: 3, 80026: 4, 80029: 4, 101206: 3,
              116649: 2, 117461: 2, 117462: 2, 114125: 4, 114157: 2, 114140: 4, 114166: 4, 119093: 3, 119094: 3,
              119095: 2, 119232: 3, 131012: 3, 119903: 4, 131349: 4, 131350: 4, 131351: 4, 129684: 3, 132094: 4,
              132404: 6, 132706: 6, 133226: 4, 133046: 3, 24817: 3, 143875: 4, 143763: 2, 144085: 2, 143706: 4,
              143764: 6, 144195: 1, 144196: 1}
}


def get_documents_path():
    import ctypes.wintypes
    CSIDL_PERSONAL = 5  # My Documents
    SHGFP_TYPE_CURRENT = 0  # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

    return pathlib.Path(buf.value)  # .resolve() would turn letters for network drives into server names


def get_savegame_folder():
    accounts = (get_documents_path() / "Anno 1800/accounts")
    for folder in accounts.glob("*"):
        return folder
    return accounts


def get_temp_path():
    p = os.environ['TEMP']
    if p is None:
        return pathlib.Path(os.getcwd()) / "temp_files"
    else:
        return pathlib.Path(p) / "Anno1800SavegameVisualizer"


TEMP_PATH = get_temp_path()
try:
    shutil.rmtree(TEMP_PATH)
except:
    pass

LANG = "english"

lang_widget = Dropdown(options=A7PARAMS["languages"], value=LANG)


def set_language(lang: str):
    global LANG
    LANG = lang_widget.value


lang_widget.observe(set_language)
display(lang_widget)


def execute(args):
    exit_code = subprocess.call(args)

    if exit_code == 0:
        return

    executable = pathlib.Path(args[0]).stem + ".exe"
    print(subprocess.list2cmdline(args))
    # if exit_code < 1000:
    raise Exception(
        "Executing {} failed. Please ensure that the file is not corrupt or try running this application in a different directory.".format(
            executable))
    # else:
    #     raise Exception(
    #         "Windows blocked the execution of {exe}. Go into the tools directory and double click {exe}. A warning appears. Click 'More Information' and 'Run anyway'. Then re-run the code (Shift + Enter).".format(
    #             exe=executable))


def hex_to_bool(h: str) -> bool:
    '''
    Converts the binary representation of a boolean 
    ('00', '01') to a Python boolean.

    Args:
        h (str or node): '00' or '01' or a node of an lxml tree.

    Returns: 
        bool: True or False or None (if node has no text).

    Example: 
        $ hex_to_bool('01') 
            -> True
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        return bool(int(h))
    else:
        return None


def hex_to_utf16(h: str) -> str:
    '''
    Converts a hexadecimal UTF-16 encoded string to a human-
    readable string. 

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns: 
        str: A human-readable text string or None (if node has no text).

    Example: 
        $ hex_to_utf16('4F006C006400200057006F0072006C006400') 
            -> 'Old World'
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        return bytes.fromhex(h).decode('utf-16-le')
    else:
        return None


def hex_to_utf8(h: str) -> str:
    '''
    Converts a hexadecimal UTF-8 encoded string to a human-
    readable string. 

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns: 
        str: A human-readable text string or None (if node has no text).

    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        return bytes.fromhex(h).decode('utf-8')
    else:
        return None


def hex_to_int(h: str) -> int:
    '''
    Converts the hexadecimal representation of a 
    Byte, Short, 32-bit, or 64-bit integer to an int.
    The precise type is determined based on the length of the string. 

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns: 
        int: Parsed int value or None (if node has no text).

    Example: 
        $ hex_to_int('4DBF0200') 
            -> 180045
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        if l == 2:
            return struct.unpack('<B', bytearray.fromhex(h))[0]
        elif l == 4:
            return struct.unpack('<h', bytearray.fromhex(h))[0]
        elif l == 8:
            return struct.unpack('<i', bytearray.fromhex(h))[0]
        elif l == 16:
            return struct.unpack('<q', bytearray.fromhex(h))[0]
        else:
            raise ValueError("Invalid length of {} characters".format(l))

    else:
        return None


def hex_to_float(h: str) -> int:
    '''
    Converts the hexadecimal representation of a 
    single or double precision IEEE floating point number to a float.
    The precise type is determined based on the length of the string. 

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.

    Returns: 
        int: Parsed float value or None (if node has no text).

    Example: 
        $ hex_to_float('DB0FC93F') 
            -> 1.5707963705062866
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        if l == 8:
            return struct.unpack('<f', bytearray.fromhex(h))[0]
        elif l == 16:
            return struct.unpack('<d', bytearray.fromhex(h))[0]
        else:
            raise ValueError("Invalid length of {} characters".format(l))

    else:
        return None


def hex_to_float_list(h: str, stride: int = 4) -> [float]:
    '''
    Converts the hexadecimal representation of a densly packed array of
    single or double precision IEEE floating point numbers to a list of floats. 

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.
        stride (int): 4 or 8 - number of bytes a single value occupies.

    Returns: 
        list: A list of floats or None (if node has no text).
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        s = stride * 2  # two chars encode one byte

        if not l % s == 0:
            raise ValueError("Invalid length of {} characters".format(l))

        arr = []
        for r in range(int(l / s)):
            arr.append(hex_to_float(h[s * r:s * (r + 1)]))

        return arr

    else:
        return None


def hex_to_int_list(h: str, stride: int = 4, limit_elements: int = 0) -> [int]:
    '''
    Converts the hexadecimal representation of a densly packed array of
    bytes, shorts, 32-bit, or 64-bit integers to a list of ints. 

    Args:
        h (str or node): A hexadecimal string or a node of an lxml tree.
        stride (int): 1,2,4, or 8 - number of bytes a single value occupies.
        limit_elements (int): The returned list has at most limit_elements many entries, default: 0 = unlimited

    Returns: 
        list: A list of ints or None (if node has no text).
    '''

    if isinstance(h, ET._Element):
        h = h.text

    if has_value(h):
        l = len(h)
        s = stride * 2  # two chars encode one byte

        if not l % s == 0:
            raise ValueError("Invalid length of {} characters".format(l))

        arr = []
        if limit_elements == 0:
            limit_elements = int(len(h) / s)
        for r in range(limit_elements):
            arr.append(hex_to_int(h[s * r:s * (r + 1)]))

        return arr

    else:
        return None


def show(ad_config):
    ad_json = json.dumps(ad_config)
    path = TEMP_PATH / "ad_files" / "{}.ad".format(hash(ad_json))
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(ad_json)

    subprocess.Popen([os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", "open", str(path)])
    # subprocess.Popen([os.getcwd() + "/tools/Anno Designer/AnnoDesigner.exe", str(path)])


def save(ad_config, path):
    ad_json = json.dumps(ad_config)
    if not path.endswith(".ad"):
        path = pathlib.Path(path).with_suffix(".ad")
    else:
        path = pathlib.Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(ad_json)


def has_value(node):
    if node is None:
        return False

    if isinstance(node, ET._Element):
        node = node.text

    return not node is None and not len(node) == 0 and not node[0] == '\n'


def is_road(idx):
    s = A7PARAMS["streets"]
    if not idx in s:
        return False

    return s[idx]["road"]


def vary_color(color, random_value: float = None):
    """
    color: dict with keys "R", "G", "B", "A" (optional)
    random_value must be within [0,1]
    if random_value is not provided a pseudo random number is drawn

    Converts color into Cielab space (L*a*b*) and selects a new L from [L - 20, L + 20] determined by random_value

    Returns an RGB(A) color
    """

    XN = 95.0489
    YN = 100
    ZN = 108.8840

    srgb2xyz = np.array([0.4124, 0.3576, 0.1805,
                         0.2126, 0.7152, 0.0722,
                         0.0193, 0.1192, 0.9504]).reshape(3, 3)

    xyz2srgb = np.array([3.2406, -1.5372, -0.4986,
                         -0.9689, 1.8758, 0.0415,
                         0.0557, -0.2040, 1.0570]).reshape(3, 3)

    inv_gamma = lambda u: u / 12.92 if u <= 0.04045 else math.pow((u + 0.055) / 1.055, 2.4)
    gamma = lambda u: 12.92 * u if u <= 0.0031308 else 1.055 * math.pow(u, 1. / 2.4) - 0.055

    lin = np.array([
        inv_gamma(color["R"] / 255),
        inv_gamma(color["G"] / 255),
        inv_gamma(color["B"] / 255),
    ])

    xyz = 100 * srgb2xyz @ lin

    f = lambda t: math.pow(t, 1 / 3) if t > (6 / 29) * (6 / 29) * (6 / 29) else t / (3 * (6 / 29) * (6 / 29)) + 4. / 29.

    L = 116. * f(xyz[1] / YN) - 16.
    a = 500. * (f(xyz[0] / XN) - f(xyz[1] / YN))
    b = 200. * (f(xyz[1] / YN) - f(xyz[2] / ZN))

    if random_value is None:
        L = random.uniform(max(L - 20, 10), min(L + 20, 90))
    else:
        min_L = max(L - 20, 10)
        max_L = min(L + 20, 90)
        L = min_L + random_value * (max_L - min_L)

    inv_f = lambda t: math.pow(t, 3) if t > (6 / 29) else 3 * (6 / 29) * (6 / 29) * (6 / 29) * (t - 4 / 29)

    xyz = np.array([
        XN * inv_f((L + 16) / 116 + a / 500),
        YN * inv_f((L + 16) / 116),
        ZN * inv_f((L + 16) / 116 - b / 200)
    ])

    lin = xyz2srgb @ (0.01 * xyz)
    g = lambda x: max(0, min(255, int(gamma(x) * 255)))

    return {
        "A": color.get("A"),
        "R": g(lin[0]),
        "G": g(lin[1]),
        "B": g(lin[2]),
    }


class Interpreter:
    """
    Stores the XML tree of the savegame along with parsing rules
    to turn the hexadecimal values into meaningful ints, floats and strings
    """

    def __init__(self, savegame_path: str, keep_files=False, decode_all=False, progress_bar=None):
        path = pathlib.Path(savegame_path)
        if not path.exists():
            raise Exception("File or path do not exist: {}".format(path))

        self.tree = self.extract(savegame_path, keep_files, decode_all, progress_bar=progress_bar)
        self.node_to_rule = dict()
        self.tag_rules = dict()
        self.rules_cached = False

    def __cache_rules__(self):
        try:
            self.rule_tree = ET.parse(os.getcwd() + "/tools/FileDBReader/FileFormats/a7s_all.xml")
            for rule_node in self.rule_tree.findall(".//Converts/Convert"):
                path = rule_node.get("Path")

                if path is None:
                    continue

                match = re.fullmatch("\\.?//([^/\\[\\]\\(\\)@.*]+)", path)
                if match is None:
                    for node in self.tree.xpath(path):
                        if not node in self.node_to_rule:
                            self.node_to_rule[node] = rule_node
                else:
                    tag = match[1]
                    if not tag in self.tag_rules:
                        self.tag_rules[tag] = rule_node

            self.rules_cached = True
        except:
            pass

    @staticmethod
    def extract(path: str, keep_files=False, decode_all=False, progress_bar=None):
        """
        Returns an XML tree of the savegame located at path.
        """
        if progress_bar is None:
            print("Unpacking ...")
        else:
            progress_bar.value = 0.01
        path = pathlib.Path(path)
        out_path = TEMP_PATH / path.stem
        # print(out_path)
        # out_path = path.parent / path.stem
        out_path.mkdir(parents=True, exist_ok=True)
        tools_path = pathlib.Path(os.getcwd() + "/tools")
        execute(
            [str(tools_path / "RDAConsole.exe"), "extract", "-f", str(path), "-o", str(out_path), "-y", "-n"])

        # db_reader_path = pathlib.Path(distutils.spawn.find_executable("FileDBReader.exe"))

        tree = None
        files = list(out_path.glob("*.a7s"))  # necessary to iterate twice

        if len(files) < 4:
            raise Exception("Savegame could not be decoded or disk is full")
        elif len(files) > 4:
            raise Exception("The temporary directory got messed up with other files: " + str(out_path))

        # print(len([f for f in files]))
        if progress_bar is None:
            print("Decoding ...")
        else:
            progress_bar.value = 0.1

        total_size = 0
        for file in files:
            total_size += file.stat().st_size

        processed_size = 0
        for file in files:

            if not file.with_suffix(".xml").exists():
                content = open(file, 'rb').read()
                content = zlib.decompress(content)
                with open(file.with_suffix(".bin"), 'wb') as f:
                    f.write(content)

                execute([str(tools_path / "FileDBReader/FileDBReader.exe"), "decompress", "-i",
                         str(tools_path / (
                             "FileDBReader/FileFormats/a7s_all.xml" if decode_all else "FileDBReader/FileFormats/a7s_hex.xml")),
                         "-f",
                         str(file.with_suffix(".bin")), "-y"])

            if progress_bar is not None:
                progress_bar.value = 0.1 + 0.6 * (processed_size / total_size + file.stat().st_size / total_size * 0.8)

            parser = ET.XMLParser(huge_tree=True)
            data = ET.parse(str(file.with_suffix(".xml")), parser)
            if tree is None:
                tree = data
            else:
                tree.getroot().extend(data.getroot())

            processed_size += file.stat().st_size

            if progress_bar is not None:
                progress_bar.value = 0.1 + 0.6 * processed_size / total_size

        if not keep_files:
            shutil.rmtree(out_path)

        if progress_bar is not None:
            progress_bar.value = 0.7

        return tree

    def parse(self, node):
        if not has_value(node):
            return None

        rule = self.node_to_rule.get(node)
        if rule is None:
            rule = self.tag_rules.get(node.tag)

        if rule is None:
            l = len(node.text)
            if l == 2 or l == 4 or l == 8 or l == 16:
                return hex_to_int(node)
            else:
                return node.text

        else:
            return self.parse_with_rule(node, rule)

    def parse_with_rule(self, node, rule):
        rule_type = rule.get("Type").lower()
        is_list = not rule.get("Structure") is None and rule.get("Structure").lower() == "list"

        if rule_type == "string":
            if rule.get("Encoding").lower() == "utf-16":
                return hex_to_utf16(node)
            else:
                return hex_to_utf8(node)
        elif rule_type == "single":
            if is_list:
                return hex_to_float_list(node, 4)
            else:
                return hex_to_float(node)
        elif rule_type == "double":
            if is_list:
                return hex_to_float_list(node, 8)
            else:
                return hex_to_float(node)

        if not is_list:
            return hex_to_int(node)

        stride = 1
        if "16" in rule_type:
            stride = 2
        elif "32" in rule_type:
            stride = 4
        elif "64" in rule_type:
            stride = 8

        return hex_to_int_list(node, stride)

    @staticmethod
    def merge(lhs, rhs):
        """
        Utility method for inspect()
        """

        if lhs is None:
            return rhs
        elif rhs is None:
            return lhs

        attr = dict()
        if isinstance(lhs, dict) and isinstance(rhs, dict):
            multi_keys = dict()

            for key in (lhs.keys() | rhs.keys()):
                k = key.split(" ")
                count = int(k[1]) if len(k) > 1 else 1

                if k[0] in multi_keys:
                    other_key = multi_keys[k[0]]
                    new_key = "{} {}".format(k[0], count + int(other_key.split(" ")[1]))
                    if key in lhs:
                        new_value = Interpreter.merge(lhs.get(key), rhs.get(other_key))
                    else:
                        new_value = Interpreter.merge(lhs.get(other_key), rhs.get(key))
                    del attr[other_key]
                    attr[new_key] = new_value

                elif k[0] in attr:
                    new_key = "{} {}".format(k[0], count + 1)
                    if key in lhs:
                        new_value = Interpreter.merge(lhs.get(key), rhs.get(k[0]))
                    else:
                        new_value = Interpreter.merge(lhs.get(k[0]), rhs.get(key))
                    del attr[k[0]]
                    attr[new_key] = new_value

                else:
                    if len(k) > 1:
                        multi_keys[k[0]] = key
                    in_both = key in lhs and key in rhs

                    if in_both:
                        new_key = "{} {}".format(k[0], 2 * count)
                        attr[new_key] = Interpreter.merge(lhs.get(key), rhs.get(key))
                    else:
                        attr[key] = lhs.get(key) if key in lhs else rhs.get(key)

            return attr

        if isinstance(lhs, dict):
            attr = copy.deepcopy(lhs)
            attr[""] = rhs
            return attr
        elif isinstance(rhs, dict):
            attr = copy.deepcopy(rhs)
            attr[""] = lhs
            return attr

        if not isinstance(lhs, set):
            lhs = set([lhs])
        if not isinstance(rhs, set):
            rhs = set([rhs])

        return lhs | rhs

    def aggregate(self, node, depth):
        """
        Utility method for inspect()
        """

        attr = dict()
        duplicates = dict()
        if has_value(node):
            val = str(self.parse(node))
            if len(val) > 20:
                val = val[0:17] + "..."
            return val

        if depth == 0:
            return "{...}"

        for n in node:
            n_dic = self.aggregate(n, depth - 1)

            if n.tag in attr:
                attr[n.tag] = Interpreter.merge(attr.get(n.tag), n_dic)

                if n.tag in duplicates:
                    duplicates[n.tag] += 1
                else:
                    duplicates[n.tag] = 2
            else:
                attr[n.tag] = n_dic

        for key in duplicates:
            attr["{} {}".format(key, duplicates[key])] = attr[key]
            del attr[key]

        return attr

    def print_dic_tree(self, t, depth=0):
        """
        Utility method for inspect()
        """

        for key in t:
            s = "\t" * depth + key + ":"
            if isinstance(t[key], dict):
                print(s)
                self.print_dic_tree(t[key], depth + 1)
            elif isinstance(t[key], set):
                values = [v for v in t[key]]
                print("{} {}".format(s, values[0:10]))
            else:
                print("{} {}".format(s, t.get(key)))

    def inspect(self, node, depth=1):
        """
        Print an aggregated view of the tree starting in node up to depth. The values of nodes are decoded as
        ints, floats, etc. according to the saved rules
        """
        if node is None:
            return

        if not self.rules_cached:
            self.__cache_rules__();

        if type(node) is ET._ElementTree:
            node = node.getroot()

        agg = self.aggregate(node, depth)
        if isinstance(agg, dict):
            self.print_dic_tree(agg)
        else:
            print(self.parse(node))


class ADConfig:
    """
    Provides access for the information stored in the Anno Designer (AD) directory:
    * presets: json of all buildings readily available in AD
    * colors: json (coloring information for groups of buildings)
    """

    def __init__(self):
        self.presets = json.load(open(os.getcwd() + "/tools/Anno Designer/presets.json", encoding="utf8"))
        self.colors = json.load(open(os.getcwd() + "/tools/Anno Designer/colors.json", encoding="utf8"))
        self.special_templates = ["RoofColDef", "DefColFace", "RoofColFace"]
        self.resident_icons = dict()
        self.roof_colors = dict()
        self.island_outlines = dict()

        self.default_color = {
            "A": 255,
            "R": 255,
            "G": 0,
            "B": 0
        }

        self.templates_by_guid = dict()
        self.scenario_templates = dict()
        for session in A7PARAMS["scenarios"].values():
            self.scenario_templates[session] = dict()

        for b in self.presets["Buildings"]:
            if b.get("Guid") is None or b.get("Guid") == "0" or not b.get("Header") == "(A7) Anno 1800":
                continue

            t = copy.deepcopy(b)
            t["Icon"] = t["IconFileName"]
            t["Radius"] = t["InfluenceRadius"]
            for key in ["Header", "Faction", "Group", "Localization", "IconFileName"]:
                if key in t:
                    del t[key]

            for c in self.colors["AvailableSchemes"][0]["Colors"]:
                applies = (c["TargetTemplate"] == t["Template"] and
                           (c["TargetIdentifiers"] is None or
                            len(c["TargetIdentifiers"]) == 0 or
                            t["Identifier"] in c["TargetIdentifiers"]))

                if applies:
                    t["Color"] = copy.deepcopy(c["Color"])

            guid = int(b.get("Guid"))

            if t.get("Template") in self.special_templates:
                template = t.get("Template")

                if template == "RoofColDef":
                    self.roof_colors[guid] = copy.deepcopy(t.get("Color"))
                elif template == "DefColFace":
                    self.resident_icons[guid] = t.get("Icon")

                continue

            if t["Template"] in A7PARAMS["scenarios"]:
                self.scenario_templates[A7PARAMS["scenarios"][t["Template"]]][guid] = t
            else:
                self.templates_by_guid[guid] = t

        self.replaced_guids = dict()

        with open(os.getcwd() + "/tools/replaced_guids.csv", encoding="utf8") as f:
            nr = 0
            for line in csv.reader(f):
                nr += 1
                if nr <= 4:
                    continue

                guid = int(line[0])

                if guid not in self.templates_by_guid:
                    # raise Exception("GUID {} specified as the target of replacement but not found in presets.json".format(guid))
                    continue

                t = self.get_template(guid)

                for g in line[3:]:
                    r_guid = int(g)
                    if not self.has_template(r_guid):
                        self.templates_by_guid[r_guid] = t

        self.scenario_templates[655][101259] = self.scenario_templates[655][24136]  # replace boxing arena by water pump
        for guid in [893, 895, 896]:  # reward ornaments have scenario template but can be build everywhere
            if guid not in self.templates_by_guid:
                self.templates_by_guid[guid] = self.scenario_templates[655][guid]

        with zipfile.ZipFile(os.getcwd() + "/tools/island_outlines.zip") as archive:
            for file in archive.infolist():
                path = pathlib.Path(file.filename)
                self.island_outlines[path.stem] = json.loads(archive.read(file))

    def get_template(self, guid: int, session: int = None) -> json:
        if session in self.scenario_templates and guid in self.scenario_templates[session]:
            t = self.scenario_templates[session][guid]
        else:
            t = self.templates_by_guid.get(guid)

        if t is None:
            return None

        if not "Color" in t:
            t["Color"] = copy.deepcopy(self.default_color)

        return t

    def has_template(self, guid: int, session: int = None) -> bool:
        if session in self.scenario_templates and guid in self.scenario_templates[session]:
            return True
        return guid in self.templates_by_guid

    def get_island_outline(self, island_name: str):
        if island_name in self.island_outlines:
            return self.island_outlines[island_name].get("Objects")

        return None

    def has_island_outline(self, island_name: str):
        return island_name in self.island_outlines


class Ship:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * guid: int (ship type)
    * identifier: int
    * name: str
    * position: np.array of floats (x,y,z) where
        the x-axis points north east
        the y-axis is perpendicular to the water surface
        the z-axis points north west
    * goods: dict(int : guid, int: amount)
    """

    def __init__(self, node: ET._Element, guid, identifier, world):
        self.node = node
        self.guid = guid
        self.identifier = identifier
        self.world = world
        # self.slots = A7PARAMS["ships"][guid]
        self.position = hex_to_float_list(node.find("Position"))
        self.name = hex_to_utf16(node.find("Nameable/VehicleName"))

    def __str__(self):
        return "{} (type: {})".format(self.name, self.guid)


class StationVisit:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * ship_guid: int
    * station: Station
    * execution_time: int (in ms since game start)
    * goods: dict(int : guid, int: amount)
    """

    def __init__(self, node: ET._Element, ship_guid, station):
        self.node = node
        self.ship_guid = ship_guid
        self.station = station
        self.execution_time = hex_to_int(node.find("ExecutionTime"))
        finalized = hex_to_int(node.find("Finalized"))
        self.finalized = False if finalized is None or finalized == 0 else True
        self.goods = dict()

        for g in node.findall("TradedGoods/None"):
            self.goods[hex_to_int(g.find("GoodGuid"))] = hex_to_int(g.find("GoodAmount"))

    def __str__(self):
        return "Visit {} at {} ms".format(self.station.__str__(), self.execution_time)


class Station:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * identifier: int
    * island : Island | NPCIsland
    * route: Route
    * goods: dict(int : guid, int: amount)
    * visits: dict(int : ship guid, [StationVisit])
    """

    def __init__(self, node: ET._Element, island, route):
        self.node = node
        self.identifier = hex_to_int(node.find("StationID"))
        self.island = island
        self.route = route
        self.goods = dict()
        self.visits = dict()  # Map ship guid -> [StationVisit]

        for g in node.findall("GoodInfos/None"):
            self.goods[hex_to_int(g.find("ProductGUID"))] = hex_to_int(g.find("Amount"))

        for v in island.node.findall("PassiveTrade/History/TradeRouteEntries/None/"):
            r = hex_to_int(v.find("RouteID"))
            if not r == route.identifier:
                continue

            # The Guid of the ship, so we cannot distinguish which one
            s = hex_to_int(v.find("TraderShip"))
            if s not in self.visits:
                self.visits[s] = [StationVisit(v, s, self)]
            else:
                self.visits[s].append(StationVisit(v, s, self))

        for visits in self.visits.values():
            visits.sort(key=lambda x: x.execution_time)

    def get_ships_types(self):
        return self.visits.keys()

    def get_visits(self, ship: int):
        """

        :param ship:
        :return: Ordered list of finalized StationVisits
        """
        if not ship in self.visits:
            return []
        return self.visits[ship]

    def __str__(self):
        return "Station {} on route {}".format(self.island.name, self.route.name)


class Route:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * identifier: int
    * name: str
    * ships: dict(int, Ship)
    * stations: [Station]
    """

    def __init__(self, node: ET._Element, world):
        self.node = node
        self.world = world
        self.identifier = hex_to_int(node.find("ID"))
        self.name = hex_to_utf16(node.find("Name"))
        self.ships = dict()
        self.stations = []
        self.visit_counts = dict()

        ships = hex_to_int_list(node.find("Ships"), 8)
        if ships is not None:
            for s in ships:
                if s in world.ships:
                    self.ships[s] = world.ships[s]

        for s in node.findall("Stations/None"):
            area = hex_to_int(s.find("AreaID"))
            if area is None:
                continue

            island = world.get_island_by_id(area)
            if island is None:
                continue

            self.stations.append(Station(s, island, self))
            island.add_route(self)
            if island in self.visit_counts:
                self.visit_counts[island] += 1
            else:
                self.visit_counts[island] = 1

    def get_ship_guids_and_count(self):
        guids = dict()

        for s in self.ships.values():
            if s.guid in guids:
                guids[s.guid] += 1
            else:
                guids[s.guid] = 1

        return guids

    def round_trip_time(self, ship_guid: int = None):
        if ship_guid is None:
            weight = 0
            time = 0
            for guid, w in self.get_ship_guids_and_count().items():
                t = self.round_trip_time(guid)
                if t is not None:
                    weight += w
                    time += t * w

            if weight == 0:
                return None
            return time / weight

        intervals = []
        for s in self.stations:
            if self.visit_counts[s.island] > 1:
                continue

            visits = s.get_visits(ship_guid)

            l = len(visits) - len(self.ships)
            if l <= 0:
                continue

            l_ = min(l, len(self.ships))
            durations = [a.execution_time - b.execution_time for a, b in zip(visits[-l_:], visits[:l_])]
            intervals.append(sum(durations) / l)

        if len(intervals) == 0:
            return None

        return min(intervals)

    def __str__(self):
        return "Route {}".format(self.name)


class NPCIsland:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * session: Session
    * identifier: int
    * name: str
    * manager: ET._Element
    * routes: set(Route) (all trade routes with a station on this island)
    """

    def __init__(self, node: ET._Element, identifier: int, name: str, session):
        self.node = node
        self.identifier = identifier
        self.name = name
        self.session = session
        self.manager = None
        self.island_template = None
        self.rectangle = None
        self.island_template_name = None
        self.buildings = dict()
        self.routes = set()

    def __set_area_manager__(self, manager: ET._Element):
        self.manager = manager

    def __set_island_template__(self, template: ET._Element, rect: np.array, name: str):
        self.island_template = template
        self.rectangle = rect
        self.island_template_name = name
        self.rotation = hex_to_int(template.find("./Rotation90"))
        if self.rotation is None:
            self.rotation = 0

    def add_route(self, route: Route):
        self.routes.add(route)

    def __str__(self):
        s = "{} (NPC) in {}".format(self.name, self.session)
        if not self.island_template_name is None:
            s += "\tIsland type: {}".format(self.island_template_name)

        return s


class Island:
    """
    Defines the following attributes:
    * node: ET._Element (stores city name, owner, shares, statistics history, trade, and takover data)
    * session: Session
    * identifier: int
    * name: str
    * count_residences: int
    * count_production_buildings: int
    * count_modules: int
    * count_other_buildings: int
    * routes: set(Route) (all trade routes with a station on this island)
    * manager: ET._Element (stores information for buildings, population, irrigation, railway, incidents,
                            electricity, consumption, items, happiness)

    To iterate all buildings, use:
    for i in self.buildings.values()
    """

    def __init__(self, node: ET._Element, identifier: int, name: str, session):
        self.node = node
        self.identifier = identifier
        self.name = name
        self.session = session
        self.buildings = dict()
        self.routes = set()

        self.count_residences = 0
        self.count_production_buildings = 0
        self.count_modules = 0
        self.count_other_buildings = 0

        self.__store_coverage_computed__ = False
        self.__building_grid__ = None

    def __set_area_manager__(self, manager: ET._Element):
        self.manager = manager

        for obj in manager.find("./AreaObjectManager/GameObject/objects"):
            try:
                identifier = hex_to_int(obj.find("ID"))
                store_index = Store.get_index(self.session.world.ad_config, hex_to_int(obj.find("guid").text))
                if store_index > 0:
                    self.buildings[identifier] = Store(obj, store_index, self)
                    self.count_production_buildings += 1
                elif (not obj.find("./BuildingModule/ParentFactoryID") is None and
                      not hex_to_int(obj.find("./BuildingModule/ParentFactoryID")) == 0):
                    self.buildings[identifier] = Module(obj, self)
                    self.count_modules += 1
                elif not obj.find("./Residence7/*") is None:
                    self.buildings[identifier] = Residence(obj, self)
                    self.count_residences += 1
                elif has_value(obj.find("./ModuleOwner/BuildingModules")):
                    self.buildings[identifier] = Farm(obj, self)
                    self.count_production_buildings += 1
                elif not obj.find("./Factory7/*") is None:
                    self.buildings[identifier] = Factory(obj, self)
                    self.count_production_buildings += 1
                elif hex_to_int(obj.find("guid")) in [114751, 117547, 100780]:
                    self.buildings[identifier] = Powerplant(obj, self)
                    self.count_other_buildings += 1
                elif obj.find("./ItemContainer/SocketContainer/SocketItems") is not None:
                    self.buildings[identifier] = Guildhouse(obj, self)
                    self.count_other_buildings += 1
                else:
                    self.buildings[identifier] = Building(obj, self)
                    self.count_other_buildings += 1

            except:
                pass

        for b in self.buildings.values():
            if isinstance(b, Farm):

                for k in ["additional_module", "fertilizer_module"]:
                    setattr(b, k, self.buildings.get(getattr(b, k)))

        for b in self.buildings.values():
            if isinstance(b, Module):
                parent = self.buildings.get(b.main_building)
                b.main_building = parent

                if isinstance(parent, Farm) and not parent.additional_module == b and not parent.fertilizer_module == b:
                    parent.modules.append(b)

    def __set_island_template__(self, template: ET._Element, rect: np.array, name: str):
        self.island_template = template
        self.rectangle = rect
        self.island_template_name = name
        self.rotation = hex_to_int(template.find("./Rotation90"))
        if self.rotation is None:
            self.rotation = 0

    def __str__(self):
        s = "{} in {}\tIsland type: {}".format(self.name, self.session, self.island_template_name)
        if self.count_residences > 0:
            s += "\tResidences : " + str(self.count_residences)
        if self.count_production_buildings > 0:
            s += "\tProduction Buildings : " + str(self.count_production_buildings)
        if self.count_modules > 0:
            s += "\tModules : " + str(self.count_modules)
        if self.count_other_buildings > 0:
            s += "\tOther Buildings : " + str(self.count_other_buildings)

        return s

    def add_route(self, route):
        self.routes.add(route)

    def get_building_grid(self):
        """
        Returns an np.array of objects where each cell points to the building that occupies the corresponding tile
        """

        if not self.__building_grid__ is None:
            return self.__building_grid__

        grid = np.empty(shape=(self.rectangle[1] - self.rectangle[0]), dtype=object)

        for b in self.buildings.values():
            if b.size is None:
                continue

            if b.guid == 117741:  # Enbesa river slot
                continue

            s = b.rotated_size

            if s is None:
                continue

            p = b.get_relative_position()

            to_int = lambda x: int(round(x))
            for x in range(to_int(p[0]), to_int(p[0] + s[0])):
                for y in range(to_int(p[1]), to_int(p[1] + s[1])):
                    grid[x, y] = b

        self.__building_grid__ = grid
        return grid

    def get_streets(self):
        """
        Returns an np.array of int where each cell corresponds to a tile
        Uses the special id for roads, canals, quays, etc.
        """

        rect = self.rectangle
        array = self.session.get_streets()[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
        # array = np.transpose(array)
        array = np.flip(array)
        return array

    def __mark_in_range__(self, grid: np.array, b, r: float, update_mode: int):
        r += 1
        n_tiles = []
        c_tiles = []
        p = b.get_relative_position()
        s = b.rotated_size

        if s is None:
            return

        streets = copy.deepcopy(self.get_streets())
        to_int = lambda x: int(round(x))
        for x in range(to_int(p[0]), to_int(p[0] + s[0])):
            for y in range(to_int(p[1]), to_int(p[1] + s[1])):
                if x == p[0] or y == p[1] or x == p[0] + s[0] - 1 or y == p[1] + s[1] - 1:
                    n_tiles.append(np.array([x, y]))
                    streets[x, y] = 3

        at = lambda container, pos: container[pos[0]][pos[1]]

        while r > 0:
            c_tiles = n_tiles
            n_tiles = []

            r -= 1

            for center in c_tiles:
                for direction in [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]:
                    n = center + direction
                    neighbor = at(grid, n)
                    street = A7PARAMS["streets"].get(at(streets, n))

                    if not neighbor is None and isinstance(neighbor, Residence):
                        neighbor.stores[update_mode - 1] = max(neighbor.stores[update_mode - 1], 1 if r >= 1 else r)

                    elif not street is None and street["road"]:
                        n_tiles.append(n)

                        if r >= 1:
                            streets[n[0], n[1]] = 0

    def calculate_coverage(self):
        if not self.__store_coverage_computed__:
            grid = self.get_building_grid()

            for b in self.buildings.values():
                if isinstance(b, Store):
                    self.__mark_in_range__(grid, b, 63.667, b.index)

                """if self.is_th(obj):
                    #print("TH", pos(obj))
                    p = pos(obj) - self.tl
                    center = p + np.array([1.5, 1.5])
                    for x in range(p[0] - r_th, p[0] + r_th+2) :
                        for y in range(p[1] - r_th, p[1] + r_th+2) :
                            h = self.area[x][y]

                            if h is None:
                                continue


                            if np.linalg.norm(center - h.center) <= r_th :
                                h.th = True """

            self.__store_coverage_computed__ = True

    def get_layout(self, options: dict = {}):
        """
        Returns a configuration object for Anno Designer
    
        options is a dict with strings as keys and lists of strings as values. 
        Each key represents an attribute of an Anno Designer object.
        The list of strings represents rules how the value of the attribute is set.
        The list is traversed left to right until the first rule matches.
    
        The following keys are valid:
        * "exclude": Exclude certain object types (some are class names, so no quotation marks)
                    "outline" (island outline)
                    "blueprints"
                    Possible values are: Farm, Factory, Powerplant, Residence, Store,
                        "StorageBuilding", "Farmfield", "SupportBuilding", "PublicServiceBuilding",
                        "OrnamentalBuilding", "OrnamentalBuilding_Park", ... (basically all Anno Designer templates)
    
        * "label" : Uses a stat of the building as the label. Possible values are:
                    "residents", "productivity", "count_modules", 
                    "upgrades" (guids of buffs affecting the building), "guid", 
                    "identifier" (save specific, internal object number)
    
        * "color" : "store_coverage": Mix blue, green, and red if department, furniture and drug store reach a residence
                    "roof": use roof colors for residences
                    "main_building": Use the same color for a farm and its modules
                    "vary_farms": Slightly vary luminosity of farms
                    "random" : Use random colors for all buildings and modules
    
        * "icon" : "residents": use resident portraits as icons for residences
                   "no_1x1_ornaments" : don't show icons on 1x1 buildings or ornaments
                   "no_1x1_modules": don't show icons on 1x1 modules
    
        Usage:
        get_layout(options = {"color" : ["vary_farms", "main_building"], "exclude": [Store], "icon": ["no_1x1", "no_1x1_modules"]})
        """

        objects = []

        e_options = options.get("exclude", {})
        l_options = options.get("label", {})
        c_options = options.get("color", {})
        i_options = options.get("icon", {})

        exclude_blueprints = ("blueprints" in e_options)

        if "store_coverage" in c_options:
            self.calculate_coverage()

        ad_config = self.session.world.ad_config

        # process buildings
        for b in self.buildings.values():
            if isinstance(b, Module) or (exclude_blueprints and b.is_blueprint) or type(b) in e_options:
                continue

            if b.guid == 117741:  # Enbesa river slot
                continue

            obj = b.generate_ad_object()

            if obj is None:
                continue

            if obj["Template"] in e_options:
                continue

            if "residents" in i_options and b.guid in ad_config.resident_icons:
                obj["Icon"] = ad_config.resident_icons[b.guid]

            if "no_1x1_ornaments" in i_options and obj["Size"] == "1,1":
                obj["Icon"] = None

            l: str
            for l in l_options:
                if not l in b.__dict__:
                    continue

                val = getattr(b, l)

                if not val is None:
                    if l == "productivity":
                        val = "{:.0%}".format(val)

                    obj["Label"] = str(val)
                    break

            main_building = False

            if isinstance(b, Residence) and obj["Size"] == "3,3" and "store_coverage" in c_options:
                c = 255 * np.array(b.stores)
                obj["Color"] = {
                    "A": 255,
                    "R": int(c[2]),
                    "G": int(c[1]),
                    "B": int(c[0])
                }

            elif isinstance(b, Store) and "store_coverage" in c_options:
                obj["Color"] = {
                    "A": 255,
                    "R": 255 if b.index == 3 else 0,
                    "G": 255 if b.index == 2 else 0,
                    "B": 255 if b.index == 1 else 0
                }

            elif "roof" in c_options and b.guid in ad_config.roof_colors:
                obj["Color"] = ad_config.roof_colors[b.guid]

            elif "random" in c_options:
                val = hash(abs(b.identifier).to_bytes(8, byteorder='little'))
                red = abs(val % 256)
                val = int(val / 256)
                green = abs(val % 256)
                val = int(val / 256)
                blue = abs(val % 256)

                obj["Color"] = {
                    "A": obj["Color"]["A"],
                    # "R": random.randrange(0, 255),
                    "R": red,
                    "G": green,
                    "B": blue,
                }

            elif isinstance(b, Farm) and "vary_farms" in c_options:
                h = hash(abs(b.identifier).to_bytes(8, byteorder='little'))
                obj["Color"] = vary_color(obj["Color"], (h % 1001) / 1000)

            if "main_building" in c_options:
                main_building = True

            if isinstance(b, Farm) and not Module in e_options:
                for m in b.modules + [b.additional_module, b.fertilizer_module]:
                    if m is None:
                        continue

                    m_obj = m.generate_ad_object()

                    if m_obj is None:
                        continue

                    if main_building:
                        m_obj["Color"] = obj["Color"]

                    if "no_1x1_modules" in i_options and m_obj["Size"] == "1,1":
                        m_obj["Icon"] = None

                    for l in l_options:
                        if not l in m.__dict__:
                            continue

                        val = getattr(m, l)

                        if not val is None:
                            if l == "productivity":
                                val = "{:.0%}".format(val)

                            m_obj["Label"] = str(val)
                            break

                    objects.append(m_obj)

            objects.append(obj)

        # process streets
        grid = np.copy(self.get_building_grid())

        streets = self.get_streets()
        ad_config = self.session.world.ad_config
        for x in range(len(streets)):
            for y in range(len(streets[0])):
                street = A7PARAMS["streets"].get(streets[x, y])
                if street is None:
                    continue

                if not grid[x, y] is None and not street.get("road"):
                    continue

                obj = ad_config.get_template(street.get("guid"), self.session.guid)
                if obj is None:
                    obj = {
                        "Guid": street.get("guid"),
                        "Identifier": "Road",
                        "Template": "Road",
                        "Size": "1,1",
                        "Position": "{},{}".format(x, y),
                        "Road": True if street.get("road") else False
                    }

                    if street.get("rail"):
                        obj["Identifier"] = "Rail"
                        obj["Template"] = "Rail"
                        obj["Icon"] = "A7_rails"

                obj["Borderless"] = True
                obj["Color"] = street.get("color")

                objects.append(obj)

        # process outline
        if ("outline" not in e_options and
                ad_config.has_island_outline(self.island_template_name) and
                self.island_template_name in A7PARAMS["island_sizes"]):

            trafo = lambda x: [x[1], size[0] - x[0] - 1]
            size = np.array(A7PARAMS["island_sizes"][self.island_template_name])

            if self.rotation == 1:
                trafo = lambda x: [size[0] - x[0] - 1, size[1] - x[1] - 1]
            elif self.rotation == 2:
                trafo = lambda x: [size[1] - x[1] - 1, x[0]]
            elif self.rotation == 3:
                trafo = lambda x: x

            for obj in ad_config.get_island_outline(self.island_template_name):
                pos = trafo([int(x) for x in obj["Position"].split(",")])
                if grid[pos[0], pos[1]] is not None or A7PARAMS["streets"].get(streets[pos[0], pos[1]]) is not None:
                    continue

                obj = copy.deepcopy(obj)
                obj["Position"] = "{},{}".format(pos[0], pos[1])
                obj["Road"] = False
                objects.append(obj)

        return {
            "FileVersion": 4,
            "LayoutVersion": "1.0.0.0",
            "Modified": str(datetime.now().isoformat()),
            "Objects": objects
        }


class Session:
    """
    Defines the following attributes:
    * node: ET._Element
    * world: World
    * guid: int
    * name: str
    * dimensions: np.array storing x and y dimension
    * streets: np.array of size dimensions[0] x dimensions[1]
    * map_template: ET._Element

    To iterate all islands, use:
    for i in self.islands.values()
    """

    def __init__(self, node: ET._Element, identifier: int, world, extract_NPC_islands=False):
        manager = node.find("./SessionData/BinaryData/Content/GameSessionManager")

        self.node = node
        self.world = world
        self.guid = hex_to_int(node.find("./SessionDesc/SessionGUID"))
        self.name = None
        if self.guid in A7PARAMS["session_names"]:
            self.name = A7PARAMS["session_names"][self.guid][LANG]
        self.street_node = manager.find("./WorldManager/StreetMap")
        self.__streets__ = None
        self.dimensions = np.array(
            [hex_to_int(self.street_node.find(".//x")), hex_to_int(self.street_node.find(".//y"))])

        self.islands = dict()
        self.islands_by_name = dict()

        i_id = None
        for i in manager.findall("./AreaInfo/None"):
            if has_value(i):
                i_id = hex_to_int(i)
                continue

            owner = hex_to_int(i.find("Owner/id"))

            if owner is None:
                continue

            name = hex_to_utf16(i.find("./CityName"))
            if name is None:
                name = hex_to_int(i.find("./CityNameGuid"))

                if name is None or not name in A7PARAMS["city_names"]:
                    continue

                name = A7PARAMS["city_names"][name][LANG]

            if owner < 4:
                island = Island(i, i_id, name, self)
            elif extract_NPC_islands:
                island = NPCIsland(i, i_id, name, self)
            else:
                continue

            self.islands_by_name[name] = island
            self.islands[i_id] = island

        for i in manager.find("./AreaManagers"):

            identifier = int(i.tag.split("_")[1])
            if identifier in self.islands:
                self.islands[identifier].__set_area_manager__(i)

        self.map_template = manager.find("./MapTemplate")
        for elem in self.map_template.findall("./TemplateElement/Element"):
            path = hex_to_utf16(elem.find("./MapFilePath"))
            position = hex_to_int_list(elem.find("./Position"))

            if path is None or position is None:
                continue

            position = np.array(position)
            path = pathlib.Path(path)
            size = np.array([200, 200])
            if path.stem in A7PARAMS["island_sizes"]:
                size = np.array(A7PARAMS["island_sizes"][path.stem])

            for i in self.islands.values():
                if len(i.buildings) == 0:
                    continue

                is_inside = True
                for b in i.buildings.values():
                    x = b.position[0]
                    y = b.position[2]

                    if x < position[0] or x > position[0] + size[0] or y < position[1] or y > position[1] + size[1]:
                        is_inside = False
                        break

                if is_inside:
                    i.__set_island_template__(elem, np.array([position, position + size]), path.stem)
                    break

    def get_island(self, name: str) -> Island:
        '''
        Args:
            name (str): Case sensitive name of the island.

        Returns: 
            Island: Corresponding Island or None if not in savegame.
                    If multiple islands have the same name, the first
                    one encountered is returned

        Example:island.world
            get_island("Crown Falls")
        '''

        return self.islands_by_name.get(name)

    def get_island_by_id(self, idx: int) -> Island:
        return self.islands.get(idx)

    def get_streets(self):
        if self.__streets__ is None:
            arr = self.street_node.find("./StreetID/val")
            if arr is None:
                arr = self.street_node.find("./IDVar")
            street_arr = hex_to_int_list(arr, 1, limit_elements=self.dimensions[0] * self.dimensions[1])

            if street_arr is None:
                self.__streets__ = np.zeros(shape=self.dimensions, dtype=int)
            else:
                self.__streets__ = np.array(street_arr).reshape(self.dimensions)

        return self.__streets__

    def __str__(self):
        if self.guid in A7PARAMS["session_names"]:
            return A7PARAMS["session_names"][self.guid][LANG]
        else:
            return "Unknown Session"


class Building:
    """
    Defines the following attributes:
    * node: ET._Element
    * island: Island
    * guid: int
    * identifier: int
    * is_blueprint: bool
    * upgrades: list of int (GUIDs of applied effects)
    * productivity: float (if available)
    * position: np.array of floats (x,y,z) where
            the x-axis points north east
            the y-axis is perpendicular to the water surface
            the z-axis points north west
    * direction: float (rotation angle in radians around y-axis, in multiples of pi / 2)
    * size: np.array of int where
            the x-axis points south east
            the y-axis points south west

    * streets: np.array of size dimensions[0] x dimensions[1]
    * map_template: ET._Element
    """

    def __init__(self, node: ET._Element, island):
        self.node = node
        self.island = island
        self.guid = hex_to_int(node.find("guid"))
        self.identifier = hex_to_int(node.find("ID"))
        self.is_blueprint = not node.find("StateBits") is None
        self.position = np.array(hex_to_float_list(node.find("Position")))
        self.size = None
        self.direction = hex_to_float(self.node.find("Direction"))
        if self.direction is None:
            self.direction = 0
        self.discrete_rotation = int(round(self.direction / math.pi * 2) % 4)

        self.bounding_rectangle = None
        if self.guid in A7PARAMS["decentered_buildings"]:
            corners = np.array(A7PARAMS["decentered_buildings"][self.guid]).transpose()

            if len(corners[0]) >= 8:
                # skip second building blocker of mines
                diag0 = np.linalg.norm(np.max(corners[:, 0:4], axis=1) - np.min(corners[:, 0:4], axis=1))
                diag1 = np.linalg.norm(np.max(corners[:, 4:8], axis=1) - np.min(corners[:, 4:8], axis=1))

                if diag1 > diag0 + 0.1:
                    corners = corners[:, 0:4]

            m_rot = np.array([
                [math.cos(self.direction), -math.sin(self.direction)],
                [math.sin(self.direction), math.cos(self.direction)]
            ])

            to_int = lambda arr: np.array([int(round(val)) for val in arr])
            self.size = to_int((np.max(corners, axis=1) - np.min(corners, axis=1))[::-1])
            corners = m_rot @ corners
            self.bounding_rectangle = np.array([np.min(corners, axis=1), np.max(corners, axis=1)])
            self.rotated_size = to_int((self.bounding_rectangle[1] - self.bounding_rectangle[0])[::-1])
        else:

            t = island.session.world.ad_config.get_template(self.guid, self.island.session.guid)
            if not t is None and not t["BuildBlocker"] is None:
                sz = t["BuildBlocker"]
                self.size = np.array([sz["z"], sz["x"]])

            if not self.size is None:
                rotated = self.discrete_rotation % 2 == 1
                self.rotated_size = np.array([self.size[1], self.size[0]]) if rotated else self.size
            else:
                raise Exception(self.guid, t, self, node)

        self.upgrades = []

        upgrades = node.find("./UpgradeList/UpgradeGUIDs")
        if has_value(upgrades):
            self.upgrades = hex_to_int_list(upgrades)

        self.productivity = hex_to_float(node.find(".//CurrentProductivity"))  # under Powerplant or Factory7

    def get_relative_position(self):
        """
        Returns the integer 2D coordinates of the northern corenr of the bounding box
        relative to the northern edge of the island
        Uses the same coordinate system as the size attribute
        """

        tl = self.island.rectangle[1]
        if self.bounding_rectangle is None:
            return np.array([int(tl[1] - round(self.position[2] + self.rotated_size[0] / 2)),
                             int(tl[0] - round(self.position[0] + self.rotated_size[1] / 2))])

        rect = self.position[::2] + self.bounding_rectangle[1]
        return np.array([int(round(val)) for val in (tl - rect)[::-1]])

    def generate_ad_object(self):
        """
        generates a representation of this object suitable for the Anno Designer
        """

        if self.rotated_size is None:
            return None

        ad_config = self.island.session.world.ad_config
        if not ad_config.has_template(self.guid, self.island.session.guid):
            return None
        obj = copy.deepcopy(ad_config.get_template(self.guid, self.island.session.guid))

        del obj["BuildBlocker"]

        rot = self.discrete_rotation
        if self.guid in A7PARAMS["direction_offsets"]:
            rot += A7PARAMS["direction_offsets"][self.guid]
        rot = rot % 4
        obj["Direction"] = A7PARAMS["directions"][rot]

        pos = self.get_relative_position()
        obj["Size"] = "{},{}".format(self.rotated_size[0], self.rotated_size[1])
        obj["Position"] = "{},{}".format(pos[0], pos[1])

        return obj


class Residence(Building):
    """
    Defines the following attributes:
    * residents: int
    * stores: 3-item list of int (values are either 0, 0.666 or 1)
              denoting the fulfillment of Department, Furniture and Drug store
    """

    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)
        self.residents = hex_to_int(node.find("./Residence7/ResidentCount"))
        self.stores = [0, 0, 0]


class Farm(Building):
    """
    Defines the following attributes:
    * modules: np.array of floats (nx2) array denoting the positions of modules
    * count_modules: int
    * module_size: np.array of int (see Building.size)
    * additional_module: Module (tractor barn or silo, if constructed)
    * fertilizer_module: Module (if constructed)
    """

    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)
        modules = hex_to_float_list(node.find("./ModuleOwner/BuildingModules"))
        if modules is None:
            self.module_centers = np.array([])
        else:
            self.module_centers = np.array(modules).reshape(-1, 2)
        self.modules = []
        self.count_modules = len(self.module_centers)

        module_guid = A7PARAMS["farm_modules"].get(self.guid)
        if not module_guid is None:
            t = self.island.session.world.ad_config.get_template(module_guid, self.island.session.guid)
            if not t is None and not t["BuildBlocker"] is None:
                sz = t["BuildBlocker"]
                self.module_size = np.array([sz["z"], sz["x"]])

        self.additional_module = hex_to_int(node.find("./ModuleOwner/AdditionalModule/ObjectID"))
        self.fertilizer_module = hex_to_int(node.find("./ModuleOwner/FertilizerModule/ObjectID"))


class Module(Building):
    """
    Defines the following attributes:
    * main_building: Farm
    """

    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)
        self.main_building = hex_to_int(node.find("./BuildingModule/ParentFactoryID"))


class Factory(Building):
    def __init__(self, node, island):
        super().__init__(node, island)


class Powerplant(Building):
    def __init__(self, node: ET._Element, island):
        super().__init__(node, island)

    def generate_ad_object(self):
        obj = super().generate_ad_object()
        if obj is None:
            return None
        inf_range = int(obj["InfluenceRange"])
        inf_range -= 2
        for upgrade in self.upgrades:
            if upgrade in A7PARAMS["range_extension_buffs"]:
                inf_range += A7PARAMS["range_extension_buffs"][upgrade]

        obj["InfluenceRange"] = int(inf_range * 1.5)
        obj["PavedStreet"] = True

        return obj


class Guildhouse(Building):
    """
    Defines the following attributes:
    * items: list of int (GUIDs of equipped items)
    """

    def __init__(self, node, island):
        super().__init__(node, island)
        self.items = []
        for guid in node.findall("ItemContainer/SocketContainer/SocketItems/None/GUID"):
            self.items.append(hex_to_int(guid))


class Store(Building):
    """
    Defines the following attributes:
    * index: int (store index, see get_index)
    """

    def __init__(self, node: ET._Element, index, island):
        super().__init__(node, island)
        self.index = index

    @staticmethod
    def get_index(ad_config: ADConfig, guid: int):
        """ Returns 
        0 = No Store, 
        1 = Department Store, 
        2 = Furniture Store,
        3 = Drug Store"""

        if not ad_config.has_template(guid):
            return 0

        t = ad_config.get_template(guid)["Identifier"]

        if "DepartmentStore" in t:
            return 1
        elif "FurnitureStore" in t:
            return 2
        elif "Pharmacy" in t:
            return 3

        return 0


class World:
    """
    Defines the following attributes:
    * interpreter: Interpreter (contains XML tree of savegame and applies rules to decode values)
    * node: ET._Element
    * playtime: int (elapsed in-game time in milliseconds)
    * seed: int
    * profile_name: str
    * ad_config: ADConfig (stores building information read from the presets.json and color.json of Anno Designer)

    To iterate all sessions, use:
    for s in self.sessions.values()

    To iterate all trade routes, use:
    for r in self.trade_routes
    """

    def __init__(self, interpreter, extract_routes=False, progress_bar=None):
        if progress_bar is None:
            print("Analyzing ...")

        self.interpreter = interpreter
        self.node = interpreter.tree.getroot()
        node = self.node
        self.sessions = dict()
        self.ships = dict()
        self.trade_routes = []
        self.playtime = hex_to_int(node.find("MetaGameManager/GameCount"))
        self.seed = hex_to_int(node.find("CorporationProfile/GameSetup/GameSeed"))
        self.profile_name = hex_to_utf16(node.find("CorporationProfile/GameSetup/SavegameFolderW"))

        self.ad_config = ADConfig()

        s_id = None
        session_nodes = node.findall("./MetaGameManager/GameSessions/None")
        count_sessions = len(session_nodes) / 2

        for i in session_nodes:
            if has_value(i):
                s_id = hex_to_int(i)
                continue

            session = Session(i, s_id, self, extract_routes)
            self.sessions[session.guid] = session

            if progress_bar is not None:
                progress_bar.value = 0.7 + 0.3 * len(self.sessions) / count_sessions

        if extract_routes:
            for s in node.findall(
                    "./MetaGameManager/GameSessions/None/SessionData/BinaryData/Content/GameSessionManager/AreaManagers/*/AreaObjectManager/GameObject/objects/None"):
                guid = hex_to_int(s.find("guid"))
                idx = hex_to_int(s.find("MetaPersistent/MetaID"))
                if guid is None or idx is None or guid not in A7PARAMS["ships"]:
                    continue

                self.ships[idx] = Ship(s, guid, idx, self)

            for i in node.findall("./MetaGameManager/SessionTradeRouteManager/RouteMap/None"):
                if not has_value(i):
                    self.trade_routes.append(Route(i, self))

        if progress_bar is None:
            print("Finished. Go ahead!")
        else:
            progress_bar.value = 1

    def get_session(self, name: str) -> Session:
        '''
        Args:
            name (str): Case sensitive name of the session (in any language), 
                        e.g. "Old World", "New World", "Cape Trelawney", "The Arctic", "Enbesa"

        Returns: 
            Session: Corresponding Session or None if not in savegame.

        Throws:
            ValueError: Invalid name provided.

        Example:
            get_session("Cape Trelawney")
        '''

        found = False
        for guid in A7PARAMS["session_names"]:
            if name in A7PARAMS["session_names"][guid].values():
                found = True
                break

        if not found:
            raise ValueError("{} is not a session".format(name))

        return self.sessions.get(guid)

    def get_island(self, name: str) -> Island:
        '''
        Args:
            name (str): Case sensitive name of the island.

        Returns: 
            Island: Corresponding Island or None if not in savegame.
                    If multiple islands have the same name, the first
                    one encountered is returned

        Example:
            get_island("Crown Falls")
        '''

        for s in self.sessions.values():
            i = s.get_island(name)

            if not i is None:
                return i

    def get_island_by_id(self, idx: int) -> Island:
        for s in self.sessions.values():
            i = s.get_island_by_id(idx)

            if not i is None:
                return i

    def print_island_summary(self):
        for s_guid in self.sessions:
            if not s_guid in A7PARAMS["session_names"] or len(self.sessions[s_guid].islands) == 0:
                continue

            print(A7PARAMS["session_names"][s_guid][LANG], ":",
                  ", ".join([i.name for i in self.sessions[s_guid].islands.values()]))

    def __str__(self):
        return "Profile: {}\tSeed: {}\tPlaytime: {:.1f}h".format(self.profile_name, self.seed, self.playtime / 3600)

    # def show_island_dropdown(self):
    #     options = []
    #
    #     for s in self.sessions.values():
    #         for i in s.islands.values():
    #             options.append((i.name, i))
    #
    #     widget = Dropdown(options=options)
    #
    #     def set_island(*args):
    #         self.selected_island = widget.value
    #
    #     widget.observe(set_island)
    #     display(widget)
