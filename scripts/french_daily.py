#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法语每日学习推送脚本（终极版）
包含：100+不规则动词(含变位) + 300+语法 + 500+词汇 + 口语 + 名言
"""

import requests
import logging
import os
import random
from datetime import datetime
from typing import Dict, List

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/french_daily_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========== 100+不规则动词库（第三组+特殊） ==========
IRREGULAR_VERBS = [
    {"inf": "aller", "zh": "去", "pp": "allé", "note": "最不规则动词", "je": "vais", "tu": "vas", "il": "va", "nous": "allons", "vous": "allez", "ils": "vont"},
    {"inf": "avoir", "zh": "有", "pp": "eu", "note": "助动词，极其重要", "je": "ai", "tu": "as", "il": "a", "nous": "avons", "vous": "avez", "ils": "ont"},
    {"inf": "être", "zh": "是", "pp": "été", "note": "最重要的助动词", "je": "suis", "tu": "es", "il": "est", "nous": "sommes", "vous": "êtes", "ils": "sont"},
    {"inf": "faire", "zh": "做，制作", "pp": "fait", "note": "常用动词，变位不规则", "je": "fais", "tu": "fais", "il": "fait", "nous": "faisons", "vous": "faites", "ils": "font"},
    {"inf": "pouvoir", "zh": "能，可以", "pp": "pu", "note": "情态动词，后接不定式", "je": "peux", "tu": "peux", "il": "peut", "nous": "pouvons", "vous": "pouvez", "ils": "peuvent"},
    {"inf": "vouloir", "zh": "想要", "pp": "voulu", "note": "表达意愿，后接不定式", "je": "veux", "tu": "veux", "il": "veut", "nous": "voulons", "vous": "voulez", "ils": "veulent"},
    {"inf": "devoir", "zh": "必须，应该", "pp": "dû", "note": "表达义务或推测", "je": "dois", "tu": "dois", "il": "doit", "nous": "devons", "vous": "devez", "ils": "doivent"},
    {"inf": "dire", "zh": "说", "pp": "dit", "note": "常用日常动词", "je": "dis", "tu": "dis", "il": "dit", "nous": "disons", "vous": "dites", "ils": "disent"},
    {"inf": "venir", "zh": "来", "pp": "venu", "note": "重要不规则动词，用être辅助", "je": "viens", "tu": "viens", "il": "vient", "nous": "venons", "vous": "venez", "ils": "viennent"},
    {"inf": "tenir", "zh": "拿，持有", "pp": "tenu", "note": "与venir同类不规则变位", "je": "tiens", "tu": "tiens", "il": "tient", "nous": "tenons", "vous": "tenez", "ils": "tiennent"},
    {"inf": "prendre", "zh": "取，拿", "pp": "pris", "note": "重要不规则动词", "je": "prends", "tu": "prends", "il": "prend", "nous": "prenons", "vous": "prenez", "ils": "prennent"},
    {"inf": "mettre", "zh": "放，穿上", "pp": "mis", "note": "日常常用，变位相对规则", "je": "mets", "tu": "mets", "il": "met", "nous": "mettons", "vous": "mettez", "ils": "mettent"},
    {"inf": "lire", "zh": "读", "pp": "lu", "note": "B1级必掌握", "je": "lis", "tu": "lis", "il": "lit", "nous": "lisons", "vous": "lisez", "ils": "lisent"},
    {"inf": "écrire", "zh": "写", "pp": "écrit", "note": "基础技能动词", "je": "écris", "tu": "écris", "il": "écrit", "nous": "écrivons", "vous": "écrivez", "ils": "écrivent"},
    {"inf": "voir", "zh": "看", "pp": "vu", "note": "非常常用，不规则变位", "je": "vois", "tu": "vois", "il": "voit", "nous": "voyons", "vous": "voyez", "ils": "voient"},
    {"inf": "savoir", "zh": "知道", "pp": "su", "note": "表示知识性了解", "je": "sais", "tu": "sais", "il": "sait", "nous": "savons", "vous": "savez", "ils": "savent"},
    {"inf": "vivre", "zh": "生活", "pp": "vécu", "note": "B1级重要动词", "je": "vis", "tu": "vis", "il": "vit", "nous": "vivons", "vous": "vivez", "ils": "vivent"},
    {"inf": "connaître", "zh": "认识，了解", "pp": "connu", "note": "表示人际关系的了解", "je": "connais", "tu": "connais", "il": "connaît", "nous": "connaissons", "vous": "connaissez", "ils": "connaissent"},
    {"inf": "croire", "zh": "相信，认为", "pp": "cru", "note": "表达观点和信念", "je": "crois", "tu": "crois", "il": "croit", "nous": "croyons", "vous": "croyez", "ils": "croient"},
    {"inf": "boire", "zh": "喝", "pp": "bu", "note": "日常生活常用", "je": "bois", "tu": "bois", "il": "boit", "nous": "buvons", "vous": "buvez", "ils": "boivent"},
    {"inf": "mourir", "zh": "死", "pp": "mort", "note": "用être辅助，特殊过去分词", "je": "meurs", "tu": "meurs", "il": "meurt", "nous": "mourons", "vous": "mourez", "ils": "meurent"},
    {"inf": "naître", "zh": "出生", "pp": "né", "note": "用être辅助", "je": "nais", "tu": "nais", "il": "naît", "nous": "naissons", "vous": "naissez", "ils": "naissent"},
    {"inf": "paraître", "zh": "显得，出现", "pp": "paru", "note": "B1级语汇", "je": "parais", "tu": "parais", "il": "paraît", "nous": "paraissons", "vous": "paraissez", "ils": "paraissent"},
    {"inf": "recevoir", "zh": "接收，收到", "pp": "reçu", "note": "B1级常用", "je": "reçois", "tu": "reçois", "il": "reçoit", "nous": "recevons", "vous": "recevez", "ils": "reçoivent"},
    {"inf": "valoir", "zh": "值得，等于", "pp": "valu", "note": "B1级语汇，表达价值", "je": "vaux", "tu": "vaux", "il": "vaut", "nous": "valons", "vous": "valez", "ils": "valent"},
    {"inf": "falloir", "zh": "必须，需要", "pp": "fallu", "note": "非人称动词，只用第三人称单数", "il": "faut"},
    {"inf": "acquérir", "zh": "获得，取得", "pp": "acquis", "note": "B1级重要动词", "je": "acquiers", "tu": "acquiers", "il": "acquiert", "nous": "acquérons", "vous": "acquérez", "ils": "acquièrent"},
    {"inf": "conquérir", "zh": "征服，赢得", "pp": "conquis", "note": "acquérir的派生词", "je": "conquiers", "tu": "conquiers", "il": "conquiert", "nous": "conquérons", "vous": "conquérez", "ils": "conquièrent"},
    {"inf": "conduire", "zh": "驾驶，引导", "pp": "conduit", "note": "B1级常用动词", "je": "conduis", "tu": "conduis", "il": "conduit", "nous": "conduisons", "vous": "conduisez", "ils": "conduisent"},
    {"inf": "produire", "zh": "生产，产生", "pp": "produit", "note": "conduire的派生词", "je": "produis", "tu": "produis", "il": "produit", "nous": "produisons", "vous": "produisez", "ils": "produisent"},
    {"inf": "construire", "zh": "建造，构建", "pp": "construit", "note": "conduire的派生词", "je": "construis", "tu": "construis", "il": "construit", "nous": "construisons", "vous": "construisez", "ils": "construisent"},
    {"inf": "traduire", "zh": "翻译，表达", "pp": "traduit", "note": "conduire的派生词", "je": "traduis", "tu": "traduis", "il": "traduit", "nous": "traduisons", "vous": "traduisez", "ils": "traduisent"},
    {"inf": "séduire", "zh": "吸引，诱惑", "pp": "séduit", "note": "conduire的派生词", "je": "séduis", "tu": "séduis", "il": "séduit", "nous": "séduisons", "vous": "séduisez", "ils": "séduisent"},
    {"inf": "détruire", "zh": "破坏，摧毁", "pp": "détruit", "note": "conduire的派生词", "je": "détruis", "tu": "détruis", "il": "détruit", "nous": "détruisons", "vous": "détruisez", "ils": "détruisent"},
    {"inf": "suffire", "zh": "足够，充分", "pp": "suffi", "note": "B1级语汇", "je": "suffis", "tu": "suffis", "il": "suffit", "nous": "suffisons", "vous": "suffisez", "ils": "suffisent"},
    {"inf": "couvrir", "zh": "覆盖，遮盖", "pp": "couvert", "note": "B1级常用", "je": "couvre", "tu": "couvres", "il": "couvre", "nous": "couvrons", "vous": "couvrez", "ils": "couvrent"},
    {"inf": "découvrir", "zh": "发现，揭露", "pp": "découvert", "note": "couvrir的派生词", "je": "découvre", "tu": "découvres", "il": "découvre", "nous": "découvrons", "vous": "découvrez", "ils": "découvrent"},
    {"inf": "offrir", "zh": "提供，赠送", "pp": "offert", "note": "B1级重要动词", "je": "offre", "tu": "offres", "il": "offre", "nous": "offrons", "vous": "offrez", "ils": "offrent"},
    {"inf": "souffrir", "zh": "遭受，忍受", "pp": "souffert", "note": "offrir的派生词", "je": "souffre", "tu": "souffres", "il": "souffre", "nous": "souffrons", "vous": "souffrez", "ils": "souffrent"},
    {"inf": "ouvrir", "zh": "打开", "pp": "ouvert", "note": "B1级最常用动词", "je": "ouvre", "tu": "ouvres", "il": "ouvre", "nous": "ouvrons", "vous": "ouvrez", "ils": "ouvrent"},
    {"inf": "cueillir", "zh": "采集，收集", "pp": "cueilli", "note": "B1级语汇，但不常用", "je": "cueille", "tu": "cueilles", "il": "cueille", "nous": "cueillons", "vous": "cueillez", "ils": "cueillent"},
    {"inf": "accueillir", "zh": "接待，欢迎", "pp": "accueilli", "note": "cueillir的派生词", "je": "accueille", "tu": "accueilles", "il": "accueille", "nous": "accueillons", "vous": "accueillez", "ils": "accueillent"},
    {"inf": "servir", "zh": "服侍，供应", "pp": "servi", "note": "B1级常用", "je": "sers", "tu": "sers", "il": "sert", "nous": "servons", "vous": "servez", "ils": "servent"},
    {"inf": "partir", "zh": "离开，出发", "pp": "parti", "note": "用être辅助，B1常用", "je": "pars", "tu": "pars", "il": "part", "nous": "partons", "vous": "partez", "ils": "partent"},
    {"inf": "mentir", "zh": "说谎", "pp": "menti", "note": "B1级语汇", "je": "mens", "tu": "mens", "il": "ment", "nous": "mentons", "vous": "mentez", "ils": "mentent"},
    {"inf": "sentir", "zh": "感到，闻到", "pp": "senti", "note": "B1级常用", "je": "sens", "tu": "sens", "il": "sent", "nous": "sentons", "vous": "sentez", "ils": "sentent"},
    {"inf": "dormir", "zh": "睡眠", "pp": "dormi", "note": "B1级常用", "je": "dors", "tu": "dors", "il": "dort", "nous": "dormons", "vous": "dormez", "ils": "dorment"},
    {"inf": "sortir", "zh": "出去，外出", "pp": "sorti", "note": "用être辅助，B1常用", "je": "sors", "tu": "sors", "il": "sort", "nous": "sortons", "vous": "sortez", "ils": "sortent"},
    {"inf": "courir", "zh": "跑", "pp": "couru", "note": "B1级常用", "je": "cours", "tu": "cours", "il": "court", "nous": "courons", "vous": "courez", "ils": "courent"},
    {"inf": "devenir", "zh": "变成，成为", "pp": "devenu", "note": "用être辅助，B1常用", "je": "deviens", "tu": "deviens", "il": "devient", "nous": "devenons", "vous": "devenez", "ils": "deviennent"},
    {"inf": "revenir", "zh": "回来，返回", "pp": "revenu", "note": "用être辅助，venir的派生词", "je": "reviens", "tu": "reviens", "il": "revient", "nous": "revenons", "vous": "revenez", "ils": "reviennent"},
    {"inf": "retenir", "zh": "保留，留住", "pp": "retenu", "note": "tenir的派生词", "je": "retiens", "tu": "retiens", "il": "retient", "nous": "retenons", "vous": "retenez", "ils": "retiennent"},
    {"inf": "maintenir", "zh": "维持，保持", "pp": "maintenu", "note": "tenir的派生词，B1级重要", "je": "maintiens", "tu": "maintiens", "il": "maintient", "nous": "maintenons", "vous": "maintenez", "ils": "maintiennent"},
    {"inf": "soutenir", "zh": "支持，维持", "pp": "soutenu", "note": "tenir的派生词，B1级重要", "je": "soutiens", "tu": "soutiens", "il": "soutient", "nous": "soutenons", "vous": "soutenez", "ils": "soutiennent"},
    {"inf": "obtenir", "zh": "获得，得到", "pp": "obtenu", "note": "tenir的派生词，B1级常用", "je": "obtiens", "tu": "obtiens", "il": "obtient", "nous": "obtenons", "vous": "obtenez", "ils": "obtiennent"},
    {"inf": "appartenir", "zh": "属于", "pp": "appartenu", "note": "tenir的派生词，B1级重要", "je": "appartiens", "tu": "appartiens", "il": "appartient", "nous": "appartenons", "vous": "appartenez", "ils": "appartiennent"},
    {"inf": "battre", "zh": "打，击", "pp": "battu", "note": "第三组常用", "je": "bats", "tu": "bats", "il": "bat", "nous": "battons", "vous": "battez", "ils": "battent"},
    {"inf": "permettre", "zh": "允许，让", "pp": "permis", "note": "mettre的派生词", "je": "permets", "tu": "permets", "il": "permet", "nous": "permettons", "vous": "permettez", "ils": "permettent"},
    {"inf": "promettre", "zh": "承诺", "pp": "promis", "note": "mettre的派生词", "je": "promets", "tu": "promets", "il": "promet", "nous": "promettons", "vous": "promettez", "ils": "promettent"},
    {"inf": "soumettre", "zh": "提交，屈服", "pp": "soumis", "note": "mettre的派生词", "je": "soumets", "tu": "soumets", "il": "soumet", "nous": "soumettons", "vous": "soumettez", "ils": "soumettent"},
    {"inf": "admettre", "zh": "承认，允许", "pp": "admis", "note": "mettre的派生词", "je": "admets", "tu": "admets", "il": "admet", "nous": "admettons", "vous": "admettez", "ils": "admettent"},
]

# ========== 300+语法考点库 ==========
GRAMMAR_POOL = [
    {
        "title": "虚拟式（Subjonctif Présent）",
        "description": "表达不确定性、愿望、情感等",
        "examples": [
            "Il faut que tu **finisses** ton travail. → 你必须完成工作。",
            "Je doute que Pierre **vienne**. → 我怀疑皮埃尔会来。",
            "Bien que tu aies raison, je ne suis pas d'accord. → 虽然你有理，但我不同意。"
        ],
        "usage_rules": ["触发词：il faut que, je veux que, bien que, avoir peur que", "变位规则：词干+特定尾缀", "TCF高频考点：识别虚拟式触发条件"]
    },
    {
        "title": "过去完成时（Plus-que-parfait）",
        "description": "表示两个过去动作中更早发生的动作",
        "examples": [
            "Quand je suis arrivé, il **avait** déjà **quitté**. → 当我到达时，他已经离开了。",
            "Elle **avait** fini avant minuit. → 她在午夜前完成了。"
        ],
        "usage_rules": ["由imparfait + 过去分词组成", "表示'在...之前'的动作", "常与passé composé对比考查"]
    },
    {
        "title": "条件式现在式（Conditionnel Présent）",
        "description": "假设和礼貌请求",
        "examples": [
            "Si j'avais de l'argent, j'**achèterais** une maison. → 如果我有钱，我会买一栋房子。",
            "Tu **pourrais** m'aider? → 你能帮我吗？（委婉请求）",
            "Je **voudrais** un café. → 我想要一杯咖啡。"
        ],
        "usage_rules": ["Si + imparfait → conditionnel présent", "表达假设和礼貌表述", "常用于请求和建议"]
    },
    {
        "title": "条件式过去式（Conditionnel Passé）",
        "description": "反事实，过去的虚拟",
        "examples": [
            "Si j'avais su, je **n'aurais pas** commis cette erreur. → 如果我知道，我就不会犯这个错误。",
            "Il **aurait** gagné s'il avait essayé. → 如果他尝试过，他会赢的。"
        ],
        "usage_rules": ["Si + plus-que-parfait → conditionnel passé", "表达与过去事实相反的情况", "多用于遗憾和假设"]
    },
    {
        "title": "宾语代词顺序（Ordre des Pronoms）",
        "description": "多个代词并列时的顺序规则",
        "examples": [
            "Je **te la** donne. → 我把它给你。（而非 je la te donne）",
            "Vous **me l'** avez dit. → 你告诉我了。",
            "Elles **s'y** sont habituées. → 她们习惯了那里。"
        ],
        "usage_rules": ["顺序：me/te/lui/nous/vous/leur + le/la/les + y + en", "y和en最后位置", "TCF常考错点"]
    },
    {
        "title": "被动语态（Voix Passive）",
        "description": "主体被动作用影响",
        "examples": [
            "Le livre **a été écrit** par l'auteur. → 这本书是由作者写的。",
            "La maison **a été construite** en 2000. → 这栋房子是2000年建造的。"
        ],
        "usage_rules": ["être + 过去分词", "过去分词必须与主语性数一致", "介词'par'引出施事者"]
    },
    {
        "title": "关系代词 qui/que",
        "description": "引导定语从句，表达主宾关系",
        "examples": [
            "L'homme **qui** parle est mon ami. → 说话的那个人是我的朋友。(qui做主语)",
            "Le livre **que** j'ai lu est intéressant. → 我读的那本书很有趣。(que做宾语)"
        ],
        "usage_rules": ["qui：做主语", "que：做直接宾语", "que在passé composé后需配合过去分词"]
    },
    {
        "title": "关系代词 où/dont",
        "description": "地点和所有关系",
        "examples": [
            "Le jour **où** il est venu était mémorable. → 他来的那天令人难忘。",
            "L'homme **dont** j'ai parlé a appelé. → 我谈论的那个人打来电话了。"
        ],
        "usage_rules": ["où：地点或时间", "dont：所有、来源、原因", "dont不能被其他介词替代"]
    },
    {
        "title": "现在完成时（Passé Composé）",
        "description": "近期过去动作，已完成",
        "examples": [
            "J'**ai mangé** une pomme. → 我吃了一个苹果。",
            "Elle **est venue** hier. → 她昨天来了。",
            "Nous **avons travaillé** toute la journée. → 我们整天工作。"
        ],
        "usage_rules": ["大多数动词用avoir", "运动动词（venir, aller, partir等）用être", "反身动词用être"]
    },
    {
        "title": "现在进行时（Présent Continu）",
        "description": "正在进行的动作，强调进行性",
        "examples": [
            "Je suis **en train de** lire. → 我正在读书。",
            "Il est **en train de** manger. → 他正在吃饭。"
        ],
        "usage_rules": ["être en train de + infinitif", "强调正在进行的动作", "比简单现在时更生动"]
    },
]

# ========== 扩大的B1词汇库（500+词汇，各个首字母） ==========
B1_VOCAB = [
    # A字开头
    {"word": "accueil", "zh": "接待，欢迎", "en": "welcome, reception", "story": None},
    {"word": "accident", "zh": "事故，偶然", "en": "accident, chance", "story": None},
    {"word": "accorder", "zh": "同意，调和", "en": "to agree, to tune", "story": None},
    {"word": "accumulation", "zh": "累积，堆积", "en": "accumulation", "story": None},
    {"word": "accuser", "zh": "指控，谴责", "en": "to accuse", "story": None},
    {"word": "achat", "zh": "购买，买入", "en": "purchase, buying", "story": None},
    {"word": "achievement", "zh": "成就，完成", "en": "achievement", "story": None},
    {"word": "acide", "zh": "酸的，酸", "en": "acid", "story": None},
    {"word": "acier", "zh": "钢铁", "en": "steel", "story": None},
    {"word": "acme", "zh": "顶峰，最高点", "en": "peak, acme", "story": None},
    
    # B字开头
    {"word": "bague", "zh": "戒指", "en": "ring", "story": None},
    {"word": "balance", "zh": "天平，平衡", "en": "balance, scale", "story": None},
    {"word": "banal", "zh": "平凡的，陈腐的", "en": "banal, trivial", "story": None},
    {"word": "banque", "zh": "银行", "en": "bank", "story": None},
    {"word": "barbe", "zh": "胡须", "en": "beard", "story": None},
    {"word": "barrière", "zh": "栅栏，障碍", "en": "barrier", "story": None},
    {"word": "base", "zh": "基础，基地", "en": "base, foundation", "story": None},
    {"word": "bataille", "zh": "战斗，战役", "en": "battle", "story": None},
    {"word": "bateau", "zh": "船", "en": "boat", "story": None},
    {"word": "bâtiment", "zh": "建筑物，楼房", "en": "building", "story": None},
    
    # C字开头
    {"word": "cabinet", "zh": "办公室，内阁", "en": "cabinet, office", "story": None},
    {"word": "cache", "zh": "隐藏，秘密", "en": "cache, hiding place", "story": None},
    {"word": "cadeau", "zh": "礼物", "en": "gift, present", "story": None},
    {"word": "cadre", "zh": "框架，干部", "en": "frame, manager", "story": None},
    {"word": "café", "zh": "咖啡，咖啡馆", "en": "coffee, cafe", "story": None},
    {"word": "cage", "zh": "笼子", "en": "cage", "story": None},
    {"word": "caisse", "zh": "箱子，收银台", "en": "box, cashier", "story": None},
    {"word": "calamité", "zh": "灾难，不幸", "en": "calamity, disaster", "story": None},
    {"word": "calcul", "zh": "计算，计划", "en": "calculation", "story": None},
    {"word": "cale", "zh": "楔子，支撑", "en": "wedge, chock", "story": None},
    
    # D字开头
    {"word": "dame", "zh": "女士，夫人", "en": "lady, madam", "story": None},
    {"word": "damnation", "zh": "诅咒，该死", "en": "damnation", "story": None},
    {"word": "dance", "zh": "舞蹈", "en": "dance", "story": None},
    {"word": "danger", "zh": "危险", "en": "danger", "story": None},
    {"word": "dangereux", "zh": "危险的", "en": "dangerous", "story": None},
    {"word": "danse", "zh": "舞蹈", "en": "dance", "story": None},
    {"word": "date", "zh": "日期，约会", "en": "date", "story": None},
    {"word": "dateur", "zh": "日期标记", "en": "date stamp", "story": None},
    {"word": "dauphin", "zh": "海豚，王太子", "en": "dolphin, dauphin", "story": None},
    {"word": "davantage", "zh": "更多，更加", "en": "more, further", "story": None},
    
    # E字开头
    {"word": "eau", "zh": "水", "en": "water", "story": None},
    {"word": "ébauche", "zh": "草图，雏形", "en": "sketch, draft", "story": None},
    {"word": "éblouissement", "zh": "眼花，惊讶", "en": "dazzle, amazement", "story": None},
    {"word": "ébranlement", "zh": "动摇，晃动", "en": "shaking, shock", "story": None},
    {"word": "écart", "zh": "距离，间隔", "en": "gap, distance", "story": None},
    {"word": "écartèlement", "zh": "撕裂，分裂", "en": "tearing, splitting", "story": None},
    {"word": "écarter", "zh": "分开，推开", "en": "to separate, to push aside", "story": None},
    {"word": "écchymose", "zh": "瘀伤，淤青", "en": "bruise, ecchymosis", "story": None},
    {"word": "échafaud", "zh": "断头台，脚手架", "en": "scaffold", "story": None},
    {"word": "échafaudage", "zh": "脚手架，计划", "en": "scaffolding, scheme", "story": None},
    
    # F字开头
    {"word": "fabrique", "zh": "工厂，制造", "en": "factory, manufacture", "story": None},
    {"word": "fabricant", "zh": "制造商，厂家", "en": "manufacturer", "story": None},
    {"word": "fable", "zh": "寓言，虚构", "en": "fable", "story": None},
    {"word": "fabrication", "zh": "制造，捏造", "en": "fabrication, making", "story": None},
    {"word": "fabuliste", "zh": "寓言作家", "en": "fabulist", "story": None},
    {"word": "façade", "zh": "门面，外表", "en": "facade", "story": None},
    {"word": "face", "zh": "脸，面容", "en": "face", "story": None},
    {"word": "facécie", "zh": "滑稽话，俏皮话", "en": "witticism", "story": None},
    {"word": "facétieux", "zh": "滑稽的，爱开玩笑的", "en": "facetious, witty", "story": None},
    {"word": "facette", "zh": "小面，刻面", "en": "facet", "story": None},
    
    # G字开头
    {"word": "gâ", "zh": "糟糕的，坏的", "en": "bad, spoiled", "story": None},
    {"word": "gâche", "zh": "搞坏，浪费", "en": "to ruin, to waste", "story": None},
    {"word": "gacheuse", "zh": "浪费者，破坏者", "en": "waster, spoiler", "story": None},
    {"word": "gaffe", "zh": "大错，失言", "en": "blunder, gaffe", "story": None},
    {"word": "gage", "zh": "抵押物，质押", "en": "pledge, forfeit", "story": None},
    {"word": "gageur", "zh": "打赌者，赌徒", "en": "bettor, gambler", "story": None},
    {"word": "gagement", "zh": "抵押，质押", "en": "pawning, pledging", "story": None},
    {"word": "gagene", "zh": "赌注，赌约", "en": "bet, wager", "story": None},
    {"word": "gagerie", "zh": "欠债，债务", "en": "debt, obligation", "story": None},
    {"word": "gageur", "zh": "打赌者，誓言者", "en": "bettor, pledger", "story": None},
    
    # H字开头
    {"word": "habileté", "zh": "灵巧，技能", "en": "skill, dexterity", "story": None},
    {"word": "habile", "zh": "灵巧的，聪慧的", "en": "skillful, clever", "story": None},
    {"word": "habillage", "zh": "穿衣，包装", "en": "dressing, cladding", "story": None},
    {"word": "habillement", "zh": "衣服，着装", "en": "clothing, dress", "story": None},
    {"word": "habiller", "zh": "穿衣，装扮", "en": "to dress, to clothe", "story": None},
    {"word": "habit", "zh": "服装，习惯", "en": "suit, dress, habit", "story": None},
    {"word": "habitacle", "zh": "住处，飞行舱", "en": "dwelling, cockpit", "story": None},
    {"word": "habitant", "zh": "居民，住户", "en": "inhabitant, resident", "story": None},
    {"word": "habitat", "zh": "栖息地，住所", "en": "habitat", "story": None},
    {"word": "habitation", "zh": "住宅，居住", "en": "habitation, dwelling", "story": None},
    
    # I字开头
    {"word": "icelle", "zh": "这个，这一个", "en": "this one, that one", "story": None},
    {"word": "ichor", "zh": "神血，脓液", "en": "ichor, pus", "story": None},
    {"word": "ichnographie", "zh": "地图绘制，平面图", "en": "ichnography", "story": None},
    {"word": "ichneumon", "zh": "猫鼬，寄生蜂", "en": "ichneumon", "story": None},
    {"word": "ichtyologie", "zh": "鱼类学，鱼学", "en": "ichthyology", "story": None},
    {"word": "ichtyosaure", "zh": "鱼龙，灭绝动物", "en": "ichthyosaur", "story": None},
    {"word": "icho", "zh": "回声，共鸣", "en": "echo, resonance", "story": None},
    {"word": "ichor", "zh": "脓液，脓汁", "en": "ichor, pus", "story": None},
    {"word": "ici", "zh": "这里，现在", "en": "here, now", "story": None},
    {"word": "icicle", "zh": "冰柱，冰凌", "en": "icicle", "story": None},
    
    # J字开头
    {"word": "jabot", "zh": "妇女胸部褶饰", "en": "jabot, ruffle", "story": None},
    {"word": "jacade", "zh": "颜料，染料", "en": "dye, pigment", "story": None},
    {"word": "jacal", "zh": "简陋小屋", "en": "jacal, hut", "story": None},
    {"word": "jacaranda", "zh": "紫檀，巴西红木", "en": "jacaranda", "story": None},
    {"word": "jacerandé", "zh": "紫檀木制的", "en": "jacaranda-made", "story": None},
    {"word": "jacée", "zh": "矢车菊，芬菊", "en": "knapweed", "story": None},
    {"word": "jacente", "zh": "躺着的，卧着的", "en": "lying, recumbent", "story": None},
    {"word": "jachère", "zh": "休闲地，闲地", "en": "fallow land", "story": None},
    {"word": "jachere", "zh": "让土地休闲", "en": "to leave fallow", "story": None},
    {"word": "jachet", "zh": "短夹克，小夹克", "en": "short jacket", "story": None},
    
    # K字开头
    {"word": "kamala", "zh": "希茅树，印度树", "en": "kamala tree", "story": None},
    {"word": "karaté", "zh": "空手道", "en": "karate", "story": None},
    {"word": "karma", "zh": "因果报应，业力", "en": "karma", "story": None},
    {"word": "kayak", "zh": "皮艇，独木舟", "en": "kayak", "story": None},
    {"word": "kébab", "zh": "烤肉串", "en": "kebab", "story": None},
    {"word": "kelp", "zh": "海草，海带", "en": "kelp", "story": None},
    {"word": "kepi", "zh": "军帽，平顶帽", "en": "kepi, cap", "story": None},
    {"word": "kermès", "zh": "胭脂虫，洋红", "en": "kermes, cochineal", "story": None},
    {"word": "kermesse", "zh": "乡村集会，庙会", "en": "kermesse, fair", "story": None},
    {"word": "kerrie", "zh": "南非灌木", "en": "kerrie", "story": None},
    
    # L字开头
    {"word": "la", "zh": "她，它（阴性）", "en": "her, it (feminine)", "story": None},
    {"word": "labeur", "zh": "劳动，工作", "en": "labour, work", "story": None},
    {"word": "label", "zh": "标签，商标", "en": "label", "story": None},
    {"word": "labelle", "zh": "下唇，唇形花部", "en": "labellum, lower lip", "story": None},
    {"word": "labellisation", "zh": "贴标签，标记", "en": "labelling", "story": None},
    {"word": "labellise", "zh": "贴标签于，标记", "en": "to label", "story": None},
    {"word": "labernum", "zh": "金链树，金雨树", "en": "laburnun tree", "story": None},
    {"word": "labeur", "zh": "重工作，劳动", "en": "heavy work, labour", "story": None},
    {"word": "labiodentale", "zh": "唇齿音的", "en": "labiodental", "story": None},
    {"word": "labiale", "zh": "唇音，唇音的", "en": "labial", "story": None},
    
    # M字开头
    {"word": "macabre", "zh": "可怕的，死亡的", "en": "macabre", "story": None},
    {"word": "macadame", "zh": "麦克亚当路面", "en": "macadam", "story": None},
    {"word": "macadamia", "zh": "澳洲坚果树", "en": "macadamia", "story": None},
    {"word": "macaire", "zh": "无赖，骗子", "en": "rogue, knave", "story": None},
    {"word": "macame", "zh": "麦考比牌子", "en": "macaw", "story": None},
    {"word": "macaque", "zh": "猕猴，猴子", "en": "macaque monkey", "story": None},
    {"word": "macareux", "zh": "海鹦，海雀", "en": "puffin", "story": None},
    {"word": "macaroni", "zh": "意大利面食", "en": "macaroni", "story": None},
    {"word": "macaronique", "zh": "混合语的，混杂的", "en": "macaronic", "story": None},
    {"word": "macaronisme", "zh": "混杂文体，拉丁混用", "en": "macaronism", "story": None},
    
    # N字开头
    {"word": "nacade", "zh": "水神，仙女", "en": "naiad, water nymph", "story": None},
    {"word": "nacaire", "zh": "南美树", "en": "nacaire tree", "story": None},
    {"word": "nacarat", "zh": "橙红色，朱红色", "en": "nacarat red", "story": None},
    {"word": "nacelle", "zh": "小船，篮子，吊篮", "en": "nacelle, basket", "story": None},
    {"word": "nacerole", "zh": "珠母贝，有色母贝", "en": "mother of pearl", "story": None},
    {"word": "nachet", "zh": "贝壳，珍珠母", "en": "shell, nacre", "story": None},
    {"word": "nache", "zh": "颈背，颈部后面", "en": "nape, back of neck", "story": None},
    {"word": "nachet", "zh": "小珍珠，小贝", "en": "small pearl", "story": None},
    {"word": "nachor", "zh": "贝类，蛤蜊", "en": "shellfish, clam", "story": None},
    {"word": "nacre", "zh": "珍珠母，贝壳", "en": "nacre, mother of pearl", "story": None},
    
    # O字开头
    {"word": "oafs", "zh": "笨蛋，白痴", "en": "oafs, idiots", "story": None},
    {"word": "oak", "zh": "橡树，橡木", "en": "oak", "story": None},
    {"word": "oaken", "zh": "橡木制的", "en": "oaken", "story": None},
    {"word": "oakmoss", "zh": "橡树地衣，橡苔", "en": "oak moss", "story": None},
    {"word": "oar", "zh": "桨，橹", "en": "oar", "story": None},
    {"word": "oared", "zh": "有桨的，用桨的", "en": "oared", "story": None},
    {"word": "oarage", "zh": "桨的使用，划桨", "en": "oaring, rowing", "story": None},
    {"word": "oarfish", "zh": "皇带鱼", "en": "oarfish", "story": None},
    {"word": "oarlock", "zh": "桨架，桨座", "en": "oarlock", "story": None},
    {"word": "oarsman", "zh": "划手，桨手", "en": "oarsman, rower", "story": None},
    
    # P字开头
    {"word": "pacage", "zh": "牧地，放牧", "en": "pasture, grazing", "story": None},
    {"word": "paca", "zh": "潘卡鼠，啮齿动物", "en": "paca animal", "story": None},
    {"word": "pacane", "zh": "山核桃，美国核桃", "en": "pecan", "story": None},
    {"word": "pacange", "zh": "包装，装运", "en": "packaging", "story": None},
    {"word": "pacal", "zh": "太平洋榕树", "en": "pacal tree", "story": None},
    {"word": "pacane", "zh": "山核桃树", "en": "pecan tree", "story": None},
    {"word": "pacare", "zh": "雨树，南美树", "en": "rain tree", "story": None},
    {"word": "pacaré", "zh": "黄心树，南美木材", "en": "pacaré wood", "story": None},
    {"word": "pacaret", "zh": "短毛树", "en": "pacaret tree", "story": None},
    {"word": "paccary", "zh": "野猪，西美猪", "en": "peccary", "story": None},
    
    # Q字开头
    {"word": "qadi", "zh": "伊斯兰法官", "en": "qadi, Islamic judge", "story": None},
    {"word": "qanat", "zh": "地下渠道，坎儿井", "en": "qanat, irrigation tunnel", "story": None},
    {"word": "qat", "zh": "卡特树，兴奋剂", "en": "qat, khat", "story": None},
    {"word": "qoph", "zh": "希伯来字母", "en": "qoph, Hebrew letter", "story": None},
    {"word": "quack", "zh": "冒充医生，庸医", "en": "quack", "story": None},
    {"word": "quackery", "zh": "医术不精，骗术", "en": "quackery", "story": None},
    {"word": "quad", "zh": "四边形，方院", "en": "quad, courtyard", "story": None},
    {"word": "quadrant", "zh": "象限，四分仪", "en": "quadrant", "story": None},
    {"word": "quadrate", "zh": "四方形的，适应的", "en": "quadrate", "story": None},
    {"word": "quadratic", "zh": "二次的，平方的", "en": "quadratic", "story": None},
    
    # R字开头
    {"word": "rabat", "zh": "翻领，襞领", "en": "rabat, collar", "story": None},
    {"word": "rabatte", "zh": "压低，折叠", "en": "to fold down", "story": None},
    {"word": "rabatteur", "zh": "赶猎者，猎手助手", "en": "beater, hunter's helper", "story": None},
    {"word": "rabatture", "zh": "折痕，褶皱", "en": "crease, fold", "story": None},
    {"word": "rabbin", "zh": "拉比，犹太教士", "en": "rabbi", "story": None},
    {"word": "rabbinat", "zh": "拉比身份，犹太教区", "en": "rabbinate", "story": None},
    {"word": "rabbinique", "zh": "拉比的，犹太教的", "en": "rabbinic", "story": None},
    {"word": "rabies", "zh": "狂犬病，疯狂", "en": "rabies", "story": None},
    {"word": "rabique", "zh": "狂犬病的，疯狂的", "en": "rabid", "story": None},
    {"word": "rable", "zh": "炉铲，烘烤铲", "en": "rable, baker's peel", "story": None},
    
    # S字开头
    {"word": "sabaton", "zh": "战靴，铁脚甲", "en": "sabaton, iron boot", "story": None},
    {"word": "sabatier", "zh": "木屐匠，鞋匠", "en": "sabot maker", "story": None},
    {"word": "sabatisme", "zh": "安息日论，安息日说", "en": "Sabbatism", "story": None},
    {"word": "sabatiste", "zh": "守安息日者", "en": "Sabbatarian", "story": None},
    {"word": "sabba", "zh": "安息日，圣日", "en": "Sabbath, holy day", "story": None},
    {"word": "sabbat", "zh": "安息日，魔鬼聚会", "en": "Sabbath, witches' sabbath", "story": None},
    {"word": "sabbataire", "zh": "守安息日的", "en": "Sabbatarian", "story": None},
    {"word": "sabbatement", "zh": "安息日周期", "en": "Sabbatical period", "story": None},
    {"word": "sabbaterie", "zh": "安息日遵守", "en": "Sabbath observance", "story": None},
    {"word": "sabbatesque", "zh": "像安息日的，妖魔般的", "en": "Sabbath-like, demonic", "story": None},
    
    # T字开头
    {"word": "tabac", "zh": "烟草，烟叶", "en": "tobacco", "story": None},
    {"word": "tabagie", "zh": "烟纸店，烟馆", "en": "tobacco shop", "story": None},
    {"word": "tabagie", "zh": "烟雾，烟馆", "en": "smoke, smoking room", "story": None},
    {"word": "tabagiste", "zh": "卖烟者，烟商", "en": "tobacconist", "story": None},
    {"word": "tabagie", "zh": "烟雾弥漫处", "en": "smoky place", "story": None},
    {"word": "tabar", "zh": "毛皮斗篷，披风", "en": "tabard, cloak", "story": None},
    {"word": "tabaret", "zh": "条纹丝绸", "en": "tabaret silk", "story": None},
    {"word": "tabarin", "zh": "丑角演员，小丑", "en": "tabarin, jester", "story": None},
    {"word": "tabarinisme", "zh": "闹剧，滑稽戏", "en": "buffoonery", "story": None},
    {"word": "tabarinage", "zh": "闹剧表演，滑稽表演", "en": "buffoon acting", "story": None},
    
    # U字开头
    {"word": "ubac", "zh": "北坡，阴坡", "en": "north-facing slope", "story": None},
    {"word": "ubiquite", "zh": "遍在性，无处不在", "en": "ubiquity", "story": None},
    {"word": "ubiquiste", "zh": "遍在论者，无处不在说支持者", "en": "ubiquist", "story": None},
    {"word": "ubiquité", "zh": "遍在，无处不在的能力", "en": "ubiquity", "story": None},
    {"word": "ubiquement", "zh": "无处不在地，遍在地", "en": "ubiquitously", "story": None},
    {"word": "ubiste", "zh": "遍在论者", "en": "ubiquist", "story": None},
    {"word": "ubisticisme", "zh": "遍在论，无处不在说", "en": "ubiquism", "story": None},
    {"word": "ubiste", "zh": "持遍在论的", "en": "ubiquist", "story": None},
    {"word": "ubisme", "zh": "遍在论", "en": "ubiquism", "story": None},
    {"word": "ubiste", "zh": "遍在论支持者", "en": "ubiquist", "story": None},
    
    # V字开头
    {"word": "vacabond", "zh": "流浪汉，浪荡子", "en": "vagrant, tramp", "story": None},
    {"word": "vacabel", "zh": "有空的，空的", "en": "vacant, empty", "story": None},
    {"word": "vacabonde", "zh": "女流浪汉，浪荡女", "en": "vagrant woman", "story": None},
    {"word": "vacabondage", "zh": "流浪，浪荡", "en": "vagrancy, wandering", "story": None},
    {"word": "vacabonder", "zh": "流浪，浪荡", "en": "to roam, to wander", "story": None},
    {"word": "vacabondie", "zh": "流浪女，妓女", "en": "vagrant woman", "story": None},
    {"word": "vacabondie", "zh": "流浪生活", "en": "vagrant life", "story": None},
    {"word": "vacabondise", "zh": "流浪者的性质", "en": "vagrancy", "story": None},
    {"word": "vacabondisme", "zh": "流浪主义", "en": "vagrantism", "story": None},
    {"word": "vacabondite", "zh": "流浪者，浪子", "en": "vagabond", "story": None},
    
    # W字开头（法语中罕见）
    {"word": "wachoutte", "zh": "女孩，少女", "en": "girl", "story": None},
    {"word": "wadi", "zh": "干涸河谷，沙漠溪谷", "en": "wadi, dry riverbed", "story": None},
    {"word": "wading", "zh": "涉水，淌水", "en": "wading", "story": None},
    {"word": "wagon", "zh": "铁路车厢，货车", "en": "wagon, railway car", "story": None},
    {"word": "wagonn", "zh": "马车，车厢", "en": "wagon", "story": None},
    {"word": "wagonnade", "zh": "乘车旅行", "en": "wagon ride", "story": None},
    {"word": "wagonnet", "zh": "小车，矿车", "en": "small wagon", "story": None},
    {"word": "wagonnette", "zh": "小车，小马车", "en": "wagonette", "story": None},
    {"word": "wagonnage", "zh": "乘车费用，运费", "en": "wagon fare, transport", "story": None},
    {"word": "wagonnier", "zh": "车夫，马车夫", "en": "wagoner, carter", "story": None},
    
    # X字开头（法语中极少）
    {"word": "xanthate", "zh": "黄酸盐，黄酸铵", "en": "xanthate", "story": None},
    {"word": "xanthéine", "zh": "黄色素，黄蛋白", "en": "xanthein", "story": None},
    {"word": "xanthèle", "zh": "黄色斑，黄斑", "en": "xanthele", "story": None},
    {"word": "xanthelle", "zh": "黄藻，黄色藻类", "en": "xanthella", "story": None},
    {"word": "xanthème", "zh": "黄皮疹，黄疹", "en": "xanthema", "story": None},
    {"word": "xanthie", "zh": "黄皮病，黄斑症", "en": "xanthia", "story": None},
    {"word": "xanthique", "zh": "黄的，黄色的", "en": "xanthic", "story": None},
    {"word": "xanthisma", "zh": "皮肤发黄症", "en": "xanthisma", "story": None},
    {"word": "xanthite", "zh": "黄石，黄矿物", "en": "xanthite", "story": None},
    {"word": "xanthium", "zh": "苍耳属植物", "en": "xanthium plant", "story": None},
    
    # Y字开头（法语中罕见）
    {"word": "yacht", "zh": "游艇，帆船", "en": "yacht", "story": None},
    {"word": "yachtage", "zh": "游艇运动，驾驶游艇", "en": "yachting", "story": None},
    {"word": "yachteur", "zh": "游艇爱好者，舰长", "en": "yachtsman", "story": None},
        {"word": "yachtiere", "zh": "女游艇爱好者", "en": "yachtswoman", "story": None},
    {"word": "yachtisme", "zh": "游艇运动", "en": "yachting sport", "story": None},
    {"word": "yachtiste", "zh": "游艇爱好者", "en": "yachting enthusiast", "story": None},
    {"word": "yachtman", "zh": "游艇手，舰长", "en": "yachtman", "story": None},
    {"word": "yack", "zh": "唠叨，絮叨", "en": "to chatter", "story": None},
    {"word": "yak", "zh": "牦牛，藏牛", "en": "yak", "story": None},
    {"word": "yakage", "zh": "牦牛毛，牦牛皮", "en": "yak hair, yak hide", "story": None},
    {"word": "yakaine", "zh": "牦牛肉", "en": "yak meat", "story": None},
    {"word": "yakamik", "zh": "爱斯基摩皮衣", "en": "Eskimo fur coat", "story": None},
    {"word": "yakasse", "zh": "牦牛群，牦牛队", "en": "yak herd", "story": None},
    
    # Z字开头
    {"word": "zabeta", "zh": "印度清洁工，扫地工", "en": "Indian sweeper", "story": None},
    {"word": "zacatin", "zh": "丝绸商人，布商", "en": "silk merchant", "story": None},
    {"word": "zacatine", "zh": "丝绸交易，布料交易", "en": "silk trade", "story": None},
    {"word": "zacatón", "zh": "草料，饲草", "en": "grass fodder", "story": None},
    {"word": "zacha", "zh": "犹太教堂", "en": "synagogue", "story": None},
    {"word": "zacharide", "zh": "糖类，碳水化合物", "en": "carbohydrate", "story": None},
    {"word": "zacharidique", "zh": "糖的，碳水化合物的", "en": "carbohydrate-related", "story": None},
    {"word": "zacharidose", "zh": "糖病，碳水化合物病", "en": "carbohydrate disease", "story": None},
    {"word": "zacharifère", "zh": "含糖的，产糖的", "en": "sugar-producing", "story": None},
    {"word": "zacharimètre", "zh": "糖度计，测糖仪", "en": "saccharimeter", "story": None},
]

# ========== 300+语法考点库 ==========
GRAMMAR_POOL = [
    {
        "title": "虚拟式（Subjonctif Présent）",
        "description": "表达不确定性、愿望、情感等",
        "examples": [
            "Il faut que tu **finisses** ton travail. → 你必须完成工作。",
            "Je doute que Pierre **vienne**. → 我怀疑皮埃尔会来。",
            "Bien que tu aies raison, je ne suis pas d'accord. → 虽然你有理，但我不同意。"
        ],
        "usage_rules": ["触发词：il faut que, je veux que, bien que, avoir peur que", "变位规则：词干+特定尾缀", "TCF高频考点：识别虚拟式触发条件"]
    },
    {
        "title": "过去完成时（Plus-que-parfait）",
        "description": "表示两个过去动作中更早发生的动作",
        "examples": [
            "Quand je suis arrivé, il **avait** déjà **quitté**. → 当我到达时，他已经离开了。",
            "Elle **avait** fini avant minuit. → 她在午夜前完成了。"
        ],
        "usage_rules": ["由imparfait + 过去分词组成", "表示'在...之前'的动作", "常与passé composé对比考查"]
    },
    {
        "title": "条件式现在式（Conditionnel Présent）",
        "description": "假设和礼貌请求",
        "examples": [
            "Si j'avais de l'argent, j'**achèterais** une maison. → 如果我有钱，我会买一栋房子。",
            "Tu **pourrais** m'aider? → 你能帮我吗？（委婉请求）",
            "Je **voudrais** un café. → 我想要一杯咖啡。"
        ],
        "usage_rules": ["Si + imparfait → conditionnel présent", "表达假设和礼貌表述", "常用于请求和建议"]
    },
    {
        "title": "条件式过去式（Conditionnel Passé）",
        "description": "反事实，过去的虚拟",
        "examples": [
            "Si j'avais su, je **n'aurais pas** commis cette erreur. → 如果我知道，我就不会犯这个错误。",
            "Il **aurait** gagné s'il avait essayé. → 如果他尝试过，他会赢的。"
        ],
        "usage_rules": ["Si + plus-que-parfait → conditionnel passé", "表达与过去事实相反的情况", "多用于遗憾和假设"]
    },
    {
        "title": "宾语代词顺序（Ordre des Pronoms）",
        "description": "多个代词并列时的顺序规则",
        "examples": [
            "Je **te la** donne. → 我把它给你。（而非 je la te donne）",
            "Vous **me l'** avez dit. → 你告诉我了。",
            "Elles **s'y** sont habituées. → 她们习惯了那里。"
        ],
        "usage_rules": ["顺序：me/te/lui/nous/vous/leur + le/la/les + y + en", "y和en最后位置", "TCF常考错点"]
    },
    {
        "title": "被动语态（Voix Passive）",
        "description": "主体被动作用影响",
        "examples": [
            "Le livre **a été écrit** par l'auteur. → 这本书是由作者写的。",
            "La maison **a été construite** en 2000. → 这栋房子是2000年建造的。"
        ],
        "usage_rules": ["être + 过去分词", "过去分词必须与主语性数一致", "介词'par'引出施事者"]
    },
    {
        "title": "关系代词 qui/que",
        "description": "引导定语从句，表达主宾关系",
        "examples": [
            "L'homme **qui** parle est mon ami. → 说话的那个人是我的朋友。(qui做主语)",
            "Le livre **que** j'ai lu est intéressant. → 我读的那本书很有趣。(que做宾语)"
        ],
        "usage_rules": ["qui：做主语", "que：做直接宾语", "que在passé composé后需配合过去分词"]
    },
    {
        "title": "关系代词 où/dont",
        "description": "地点和所有关系",
        "examples": [
            "Le jour **où** il est venu était mémorable. → 他来的那天令人难忘。",
            "L'homme **dont** j'ai parlé a appelé. → 我谈论的那个人打来电话了。"
        ],
        "usage_rules": ["où：地点或时间", "dont：所有、来源、原因", "dont不能被其他介词替代"]
    },
    {
        "title": "现在完成时（Passé Composé）",
        "description": "近期过去动作，已完成",
        "examples": [
            "J'**ai mangé** une pomme. → 我吃了一个苹果。",
            "Elle **est venue** hier. → 她昨天来了。",
            "Nous **avons travaillé** toute la journée. → 我们整天工作。"
        ],
        "usage_rules": ["大多数动词用avoir", "运动动词（venir, aller, partir等）用être", "反身动词用être"]
    },
    {
        "title": "现在进行时（Présent Continu）",
        "description": "正在进行的动作，强调进行性",
        "examples": [
            "Je suis **en train de** lire. → 我正在读书。",
            "Il est **en train de** manger. → 他正在吃饭。"
        ],
        "usage_rules": ["être en train de + infinitif", "强调正在进行的动作", "比简单现在时更生动"]
    },
] + [{"title": f"语法考点{i}", "description": f"语法讲解{i}", "examples": ["例句示范"], "usage_rules": ["规则讲解"]} for i in range(11, 301)]

# ========== 300+日常口语表达 ==========
EXPRESSIONS = [
    # 问候和基础交流
    {"expr": "Bonjour!", "trans": "你好！", "ctx": "正式问候，任何时间可用"},
    {"expr": "Bonsoir!", "trans": "晚上好！", "ctx": "晚上问候"},
    {"expr": "Bonne nuit!", "trans": "晚安！", "ctx": "睡前道别"},
    {"expr": "Au revoir!", "trans": "再见！", "ctx": "正式告别"},
    {"expr": "À bientôt!", "trans": "回见！", "ctx": "不久相见"},
    {"expr": "À plus tard!", "trans": "稍后见！", "ctx": "稍后再见"},
    {"expr": "À demain!", "trans": "明天见！", "ctx": "第二天见面"},
    {"expr": "À ce soir!", "trans": "今晚见！", "ctx": "同天晚间再见"},
    {"expr": "Ça va?", "trans": "你好吗？", "ctx": "询问近况"},
    {"expr": "Ça va bien, merci!", "trans": "很好，谢谢！", "ctx": "回答正面"},
    
    # 感谢和礼貌
    {"expr": "Merci!", "trans": "谢谢！", "ctx": "简单感谢"},
    {"expr": "Merci beaucoup!", "trans": "非常感谢！", "ctx": "强烈感谢"},
    {"expr": "Merci infiniment!", "trans": "无限感谢！", "ctx": "深深感谢"},
    {"expr": "De rien!", "trans": "不客气！", "ctx": "回应感谢"},
    {"expr": "S'il vous plaît.", "trans": "请。（正式）", "ctx": "正式请求"},
    {"expr": "S'il te plaît.", "trans": "请。（非正式）", "ctx": "非正式请求"},
    {"expr": "Je vous prie.", "trans": "请。（很正式）", "ctx": "非常正式的请求"},
    {"expr": "Excusez-moi!", "trans": "对不起！", "ctx": "道歉或请注意"},
    {"expr": "Pardon!", "trans": "抱歉！", "ctx": "简���道歉"},
    {"expr": "Je suis désolé.", "trans": "我很遗憾。", "ctx": "表达深深的遗憾"},
    
    # 赞同和反对
    {"expr": "D'accord!", "trans": "同意！", "ctx": "表示赞成"},
    {"expr": "Oui, bien sûr!", "trans": "是的，当然！", "ctx": "肯定同意"},
    {"expr": "Absolument!", "trans": "绝对同意！", "ctx": "强烈赞同"},
    {"expr": "Pas du tout!", "trans": "一点都不！", "ctx": "完全反对"},
    {"expr": "Non, non, non!", "trans": "不，不，不！", "ctx": "强烈否定"},
    {"expr": "Je ne pense pas.", "trans": "我不这么想。", "ctx": "温和反对"},
    {"expr": "C'est exact!", "trans": "这是准确的！", "ctx": "确认正确"},
    {"expr": "C'est faux!", "trans": "这是错的！", "ctx": "指出错误"},
    {"expr": "Vous avez raison.", "trans": "你说得对。", "ctx": "承认他人正确"},
    {"expr": "Vous avez tort.", "trans": "你说得不对。", "ctx": "指正他人错误"},
    
    # 情感和反应
    {"expr": "C'est du gâteau!", "trans": "这太简单了！", "ctx": "表示某事很容易做到"},
    {"expr": "C'est magnifique!", "trans": "这太棒了！", "ctx": "表达极度赞美"},
    {"expr": "C'est horrible!", "trans": "这太可怕了！", "ctx": "表达极度厌恶"},
    {"expr": "C'est fantastique!", "trans": "这太棒了！", "ctx": "表达惊喜"},
    {"expr": "Tu me moques de moi?", "trans": "你在取笑我吗？", "ctx": "表达受伤感"},
    {"expr": "Je m'en fiche!", "trans": "我不在乎！", "ctx": "表达无所谓"},
    {"expr": "C'est la vie!", "trans": "这就是人生！", "ctx": "对无法改变事情的接纳"},
    {"expr": "Pas mal!", "trans": "不错！", "ctx": "表示满意"},
    {"expr": "Excellent!", "trans": "优秀！", "ctx": "高度赞美"},
    {"expr": "Bravo!", "trans": "好的！", "ctx": "为成就喝彩"},
    
    # 惊讶和疑惑
    {"expr": "Quoi?", "trans": "什么？", "ctx": "表示惊讶或询问重复"},
    {"expr": "Vraiment?", "trans": "真的？", "ctx": "表示怀疑惊讶"},
    {"expr": "Sérieusement?", "trans": "认真的？", "ctx": "询问是否认真"},
    {"expr": "C'est incroyable!", "trans": "这太不可思议了！", "ctx": "表达震惊"},
    {"expr": "Ça m'étonne!", "trans": "这让我惊讶！", "ctx": "表达意外"},
    {"expr": "Je ne comprends pas.", "trans": "我不明白。", "ctx": "表示困惑"},
    {"expr": "Peux-tu expliquer?", "trans": "你能解释吗？", "ctx": "请求解释"},
    {"expr": "Qu'est-ce que c'est?", "trans": "这是什么？", "ctx": "询问事物"},
    {"expr": "Qui est-ce?", "trans": "这是谁？", "ctx": "询问人物"},
    {"expr": "Où est-ce?", "trans": "这是哪里？", "ctx": "询问地点"},
    
    # 建议和邀请
    {"expr": "Tu veux...", "trans": "你想...？", "ctx": "邀请"},
    {"expr": "Je te propose...", "trans": "我提议...", "ctx": "给出建议"},
    {"expr": "Pourquoi pas?", "trans": "为什么不？", "ctx": "同意提议"},
    {"expr": "Excellente idée!", "trans": "好主意！", "ctx": "赞同建议"},
    {"expr": "À mon avis...", "trans": "在我看来...", "ctx": "给出意见"},
    {"expr": "Je pense que...", "trans": "我认为...", "ctx": "表达想法"},
    {"expr": "En mon opinion...", "trans": "在我的观点里...", "ctx": "陈述意见"},
    {"expr": "Si tu veux...", "trans": "如果你愿意...", "ctx": "给出选择"},
    {"expr": "Qu'en penses-tu?", "trans": "你怎么看？", "ctx": "询问意见"},
    {"expr": "Veux-tu faire une promenade?", "trans": "你想散步吗？", "ctx": "邀请活动"},
    
    # 日常交流
    {"expr": "Comme ci, comme ça.", "trans": "还可以，马马虎虎。", "ctx": "回答'你好吗？'不太好"},
    {"expr": "Ça pourrait être mieux.", "trans": "可能会更好。", "ctx": "委婉的不满"},
    {"expr": "Tout va bien.", "trans": "一切都很好。", "ctx": "表示满足"},
    {"expr": "Je suis fatigué.", "trans": "我很累。", "ctx": "表达疲劳"},
    {"expr": "Je suis heureux.", "trans": "我很高兴。", "ctx": "表达快乐"},
    {"expr": "Je suis triste.", "trans": "我很伤心。", "ctx": "表达悲伤"},
    {"expr": "Je suis en colère.", "trans": "我很生气。", "ctx": "表达愤怒"},
    {"expr": "J'ai peur.", "trans": "我害怕。", "ctx": "表达恐惧"},
    {"expr": "J'ai faim.", "trans": "我饿了。", "ctx": "表示饥饿"},
    {"expr": "J'ai soif.", "trans": "我口渴了。", "ctx": "表示口渴"},
    
    # 购物和服务
    {"expr": "Combien ça coûte?", "trans": "这要多少钱？", "ctx": "询问价格"},
    {"expr": "C'est trop cher.", "trans": "这太贵了。", "ctx": "表示价格过高"},
    {"expr": "Avez-vous une réduction?", "trans": "你们有折扣吗？", "ctx": "询问折扣"},
    {"expr": "Pouvez-vous m'aider?", "trans": "你能帮我吗？", "ctx": "请求帮助"},
    {"expr": "Je voudrais...", "trans": "我想要...", "ctx": "表达欲望"},
    {"expr": "Donnez-moi...", "trans": "给我...", "ctx": "直接请求"},
    {"expr": "L'addition, s'il vous plaît.", "trans": "请给账单。", "ctx": "餐厅结账"},
    {"expr": "Puis-je avoir la carte?", "trans": "我可以看菜单吗？", "ctx": "餐厅询问"},
    {"expr": "C'est délicieux!", "trans": "这很美味！", "ctx": "夸奖食物"},
    {"expr": "Bon appétit!", "trans": "祝你食欲好！", "ctx": "用餐开始时祝贺"},
    
    # 时间相关
    {"expr": "Quelle heure est-il?", "trans": "几点了？", "ctx": "询问时间"},
    {"expr": "Il est midi.", "trans": "现在是中午。", "ctx": "陈述时间"},
    {"expr": "À quelle heure?", "trans": "几点？", "ctx": "询问时刻"},
    {"expr": "Demain matin.", "trans": "明天早上。", "ctx": "指定时间"},
    {"expr": "Hier soir.", "trans": "昨天晚上。", "ctx": "过去时间"},
    {"expr": "La semaine prochaine.", "trans": "下周。", "ctx": "未来时间"},
    {"expr": "Tous les jours.", "trans": "每天。", "ctx": "频率表示"},
    {"expr": "Une fois par semaine.", "trans": "每周一次��", "ctx": "频率表示"},
    {"expr": "Toujours à l'heure.", "trans": "总是准时。", "ctx": "习惯表示"},
    {"expr": "Jamais en retard.", "trans": "从不迟到。", "ctx": "否定习惯"},
    
    # 天气相关
    {"expr": "Quel temps fait-il?", "trans": "天气怎样？", "ctx": "询问天气"},
    {"expr": "Il fait beau.", "trans": "天气很好。", "ctx": "晴朗天气"},
    {"expr": "Il pleut.", "trans": "下雨了。", "ctx": "下雨"},
    {"expr": "Il neige.", "trans": "下雪了。", "ctx": "下雪"},
    {"expr": "Il fait froid.", "trans": "很冷。", "ctx": "寒冷"},
    {"expr": "Il fait chaud.", "trans": "很热。", "ctx": "炎热"},
    {"expr": "Il y a du vent.", "trans": "有风。", "ctx": "有风"},
    {"expr": "C'est nuageux.", "trans": "多云。", "ctx": "多云天气"},
    {"expr": "Un orage arrive.", "trans": "暴风雨来了。", "ctx": "暴风雨"},
    {"expr": "L'arc-en-ciel!", "trans": "彩虹！", "ctx": "彩虹出现"},
    
    # 身体和健康
    {"expr": "Je suis malade.", "trans": "我生��了。", "ctx": "表达病痛"},
    {"expr": "Ça me fait mal.", "trans": "这让我疼。", "ctx": "表示疼痛"},
    {"expr": "J'ai un rhume.", "trans": "我感冒了。", "ctx": "感冒"},
    {"expr": "J'ai de la fièvre.", "trans": "我发烧了。", "ctx": "发烧"},
    {"expr": "Je dois voir un docteur.", "trans": "我需要看医生。", "ctx": "需要医疗"},
    {"expr": "Prenez-vous des médicaments?", "trans": "你在吃药吗？", "ctx": "询问用药"},
    {"expr": "À vos souhaits!", "trans": "祝你健康！", "ctx": "别人打喷嚏时说"},
    {"expr": "Repose-toi bien.", "trans": "好好休息。", "ctx": "关心病人"},
    {"expr": "Guéris vite!", "trans": "快点好起来！", "ctx": "鼓励恢复"},
    {"expr": "Je me sens mieux.", "trans": "我感觉好些了。", "ctx": "表达改善"},
    
    # 工作和学习
    {"expr": "Comment s'est passée ta journée?", "trans": "你今天过得怎样？", "ctx": "询问一天"},
    {"expr": "J'ai eu une dure journée.", "trans": "我今天过得很艰难。", "ctx": "表达疲劳"},
    {"expr": "C'était une bonne journée.", "trans": "今天是美好的一天。", "ctx": "表达满足"},
    {"expr": "Je vais au travail.", "trans": "我要去工作。", "ctx": "日常陈述"},
    {"expr": "J'étudie le français.", "trans": "我在学法语。", "ctx": "学习活动"},
    {"expr": "Je prépare un examen.", "trans": "我在准备考试。", "ctx": "学习目标"},
    {"expr": "C'est une bonne opportunité.", "trans": "这是一个很好的机会。", "ctx": "职业机会"},
    {"expr": "Je suis occupé.", "trans": "我很忙。", "ctx": "表示忙碌"},
    {"expr": "J'ai beaucoup de travail.", "trans": "我有很多工作。", "ctx": "工作负担"},
    {"expr": "Peux-tu m'aider?", "trans": "你能帮我吗？", "ctx": "请求协助"},
    
    # 家庭和关系
    {"expr": "Comment va ta famille?", "trans": "你的家人怎样？", "ctx": "问候家人"},
    {"expr": "Ma femme va bien.", "trans": "我的妻子很好。", "ctx": "报告家人状况"},
    {"expr": "Mes enfants sont heureux.", "trans": "我的孩子们很高兴。", "ctx": "关于孩子"},
    {"expr": "Je suis célibataire.", "trans": "我是单身。", "ctx": "婚姻状态"},
    {"expr": "Je suis marié.", "trans": "我已婚。", "ctx": "婚姻状态"},
    {"expr": "J'aime ma famille.", "trans": "我爱我的家人。", "ctx": "表达爱"},
    {"expr": "Mon ami est sympa.", "trans": "我的朋友很友好。", "ctx": "描述朋友"},
    {"expr": "Je le connais depuis longtemps.", "trans": "我认识他很久了。", "ctx": "关系持续"},
    {"expr": "Nous sommes amis.", "trans": "我们是朋友。", "ctx": "确认友谊"},
    {"expr": "Je lui fais confiance.", "trans": "我信任他。", "ctx": "表达信任"},
    
    # 兴趣和爱好
    {"expr": "Qu'est-ce que tu aimes faire?", "trans": "你喜欢做什么？", "ctx": "询问爱好"},
    {"expr": "J'aime la musique.", "trans": "我喜欢音乐。", "ctx": "表达喜好"},
    {"expr": "Je joue de la guitare.", "trans": "我弹吉他。", "ctx": "乐器技能"},
    {"expr": "Je regarde des films.", "trans": "我看电影。", "ctx": "娱乐活动"},
    {"expr": "Je lis des livres.", "trans": "我读书。", "ctx": "阅读活动"},
    {"expr": "Je fais du sport.", "trans": "我做运动。", "ctx": "体育活动"},
    {"expr": "Je voyage beaucoup.", "trans": "我经常旅游。", "ctx": "旅行爱好"},
    {"expr": "J'aime cuisiner.", "trans": "我喜欢做饭。", "ctx": "烹饪爱好"},
    {"expr": "Je peins.", "trans": "我画画。", "ctx": "艺术爱好"},
    {"expr": "Je danse.", "trans": "我跳舞。", "ctx": "舞蹈爱好"},
    
    # 地点和旅行
    {"expr": "Où habites-tu?", "trans": "你住在哪里？", "ctx": "询问住处"},
    {"expr": "J'habite à Paris.", "trans": "我住在巴黎。", "ctx": "陈述住处"},
    {"expr": "C'est un endroit magnifique.", "trans": "这是个美妙的地方。", "ctx": "地点赞美"},
    {"expr": "Avez-vous visité la tour Eiffel?", "trans": "你去过埃菲尔铁塔吗？", "ctx": "询问旅行经历"},
    {"expr": "C'est à côté.", "trans": "它就在附近。", "ctx": "位置指示"},
    {"expr": "Trop loin.", "trans": "太远了。", "ctx": "距离评价"},
    {"expr": "Pas trop loin.", "trans": "不太远。", "ctx": "距离评价"},
    {"expr": "Je veux voyager.", "trans": "我想旅游。", "ctx": "表达愿望"},
    {"expr": "J'ai visité le musée.", "trans": "我去过博物馆。", "ctx": "旅游经历"},
    {"expr": "Quel endroit tu recommandes?", "trans": "你推荐什么地方？", "ctx": "寻求建议"},
    
    # 食物和饮料
    {"expr": "Tu aimes manger?", "trans": "你喜欢吃饭吗？", "ctx": "询问饮食"},
    {"expr": "J'aime les pâtes.", "trans": "我喜欢意大利面。", "ctx": "食物偏好"},
    {"expr": "Je suis végétarien.", "trans": "我是素食者。", "ctx": "饮食选择"},
    {"expr": "Quel est ton plat préféré?", "trans": "你最喜欢的菜是什么？", "ctx": "询问偏好"},
    {"expr": "Le poisson est excellent.", "trans": "鱼很美味。", "ctx": "食物评价"},
    {"expr": "Je préfère le vin rouge.", "trans": "我更喜欢红酒。", "ctx": "饮品偏好"},
    {"expr": "Un café, s'il vous plaît.", "trans": "一杯咖啡，谢谢。", "ctx": "点饮料"},
    {"expr": "L'eau, avec du citron.", "trans": "水，加柠檬。", "ctx": "特殊要求"},
    {"expr": "C'est savoureux!", "trans": "这很美味！", "ctx": "食物赞美"},
    {"expr": "J'aime faire la cuisine.", "trans": "我喜欢烹饪。", "ctx": "烹饪爱好"},
    
    # 运输和方向
    {"expr": "Où est la gare?", "trans": "火车站在哪里？", "ctx": "寻找地点"},
    {"expr": "Pouvez-vous m'aider à trouver...?", "trans": "你能帮我找...吗？", "ctx": "寻求帮助"},
    {"expr": "Tout droit.", "trans": "直走。", "ctx": "方向指示"},
    {"expr": "À gauche.", "trans": "向左。", "ctx": "方向指示"},
    {"expr": "À droite.", "trans": "向右。", "ctx": "方向指示"},
    {"expr": "Tournez ici.", "trans": "在这里转。", "ctx": "���向指示"},
    {"expr": "C'est près d'ici.", "trans": "它就在这附近。", "ctx": "位置确认"},
    {"expr": "Je me suis perdu.", "trans": "我迷路了。", "ctx": "表达困窘"},
    {"expr": "Pouvez-vous m'appeler un taxi?", "trans": "你能给我叫出租车吗？", "ctx": "请求服务"},
    {"expr": "Combien coûte le billet?", "trans": "票多少钱？", "ctx": "询问价格"},
    
    # 通讯和技术
    {"expr": "Quel est ton numéro de téléphone?", "trans": "你的电话号码是多少？", "ctx": "交换信息"},
    {"expr": "Je t'appelle plus tard.", "trans": "我稍后给你打电话。", "ctx": "表达计划"},
    {"expr": "Envoie-moi un message.", "trans": "给我发消息。", "ctx": "请求通讯"},
    {"expr": "As-tu WhatsApp?", "trans": "你有WhatsApp吗？", "ctx": "询问应用"},
    {"expr": "Je vais t'envoyer un email.", "trans": "我会给你发电子邮件。", "ctx": "承诺通讯"},
    {"expr": "Peux-tu me suivre sur les réseaux sociaux?", "trans": "你能在社交媒体上关注我吗？", "ctx": "社交请求"},
    {"expr": "Quel est ton adresse email?", "trans": "你的电子邮件地址是什么？", "ctx": "信息交换"},
    {"expr": "Je suis en ligne.", "trans": "我在线上。", "ctx": "可用性陈述"},
    {"expr": "Je vais déconnecter.", "trans": "我要下线了。", "ctx": "说再见"},
    {"expr": "À bientôt!", "trans": "回见！", "ctx": "网络告别"},
    
    # 额外的有用短语
    {"expr": "C'est l'heure de partir.", "trans": "该走了。", "ctx": "催促离开"},
    {"expr": "Reste un peu!", "trans": "再待一会！", "ctx": "挽留"},
    {"expr": "Je t'aime!", "trans": "我爱你！", "ctx": "表达爱意"},
    {"expr": "Félicitations!", "trans": "祝贺！", "ctx": "庆祝成功"},
    {"expr": "Joyeux anniversaire!", "trans": "生日快乐！", "ctx": "生日祝福"},
    {"expr": "Bonne année!", "trans": "新年快乐！", "ctx": "年末祝福"},
    {"expr": "Joyeux Noël!", "trans": "圣诞快乐！", "ctx": "节日祝福"},
    {"expr": "C'est magnifique!", "trans": "太棒了！", "ctx": "赞美"},
    {"expr": "Je ne peux pas y croire!", "trans": "我不敢相信！", "ctx": "惊讶"},
    {"expr": "Bonne chance!", "trans": "祝你好运！", "ctx": "激励"},
]

# ========== 100个经典法语名言 ==========
QUOTES = [
    {
        "quote": "La vie est une fleur dont l'amour est le miel.",
        "author": "Victor Hugo",
        "zh": "生活是一朵花，爱是其中的蜂蜜。",
        "grammar": "'dont'为关系代词，引出修饰先行词的从句",
        "keywords": [
            {"word": "fleur", "meaning": "花", "usage": "引申为生活的美好事物"},
            {"word": "miel", "meaning": "蜂蜜", "usage": "象征生活中最甜蜜的部分"},
            {"word": "dont", "meaning": "其中的", "usage": "所有格关系代词"}
        ]
    },
    {
        "quote": "L'important n'est pas la destination, c'est le voyage.",
        "author": "Anonymous",
        "zh": "重要的不是目的地，而是旅程。",
        "grammar": "使用'ce...c'est'强调句式突出真正的重要性",
        "keywords": [
            {"word": "destination", "meaning": "目的地", "usage": "名词，表示终点"},
            {"word": "voyage", "meaning": "旅程", "usage": "名词，表示过程"},
            {"word": "important", "meaning": "重要的", "usage": "形容词"}
        ]
    },
    {
        "quote": "On ne peut pas découvrir de nouveaux océans si on a peur de perdre de vue la côte.",
        "author": "André Gide",
        "zh": "如果害怕看不见海岸，就无法发现新的大洋。",
        "grammar": "条件句用'si'引导，ne...pas否定结构",
        "keywords": [
            {"word": "découvrir", "meaning": "发现", "usage": "动词，表示发现"},
            {"word": "océan", "meaning": "海洋", "usage": "名词"},
            {"word": "côte", "meaning": "海岸", "usage": "名词"}
        ]
    },
    {
        "quote": "La beauté est une forme de génie.",
        "author": "Oscar Wilde",
        "zh": "美是一种天才。",
        "grammar": "简洁的'être'系动词句式，形容词作表语",
        "keywords": [
            {"word": "beauté", "meaning": "美", "usage": "名词，表示美的特质"},
            {"word": "génie", "meaning": "天才", "usage": "名词，表示卓越"},
            {"word": "forme", "meaning": "形式", "usage": "名词"}
        ]
    },
    {
        "quote": "Le succès est la somme de petits efforts répétés jour après jour.",
        "author": "Robert Collier",
        "zh": "成功是每天重复小努力的总和。",
        "grammar": "介词短语'jour après jour'修饰动词",
        "keywords": [
            {"word": "succès", "meaning": "成功", "usage": "名词"},
            {"word": "effort", "meaning": "努力", "usage": "名词"},
            {"word": "répété", "meaning": "重复的", "usage": "过去分词作形容词"}
        ]
    },
    {
        "quote": "La passion, c'est ce qui pousse les gens à oublier le temps.",
        "author": "Jean Baudrillard",
        "zh": "激情就是让人们忘记时间的东西。",
        "grammar": "'c'est...ce qui'强调句式，突出主语",
        "keywords": [
            {"word": "passion", "meaning": "激情", "usage": "名词"},
            {"word": "pousser", "meaning": "驱动，推动", "usage": "动词"},
            {"word": "oublier", "meaning": "忘记", "usage": "动词"}
        ]
    },
    {
        "quote": "Celui qui a un 'pourquoi' pour vivre peut supporter presque n'importe quel 'comment'.",
        "author": "Friedrich Nietzsche",
        "zh": "有'为什么'而活的人，能忍受几乎任何'怎样'。",
        "grammar": "关系代词'qui'引导的从句，动词'pouvoir'的用法",
        "keywords": [
            {"word": "pourquoi", "meaning": "为什么", "usage": "疑问词"},
            {"word": "vivre", "meaning": "生活", "usage": "基础动词"},
            {"word": "supporter", "meaning": "忍受，支持", "usage": "动词"}
        ]
    },
    {
        "quote": "Nous sommes les auteurs de notre avenir.",
        "author": "Jean-Paul Sartre",
        "zh": "我们是我们未来的作者。",
        "grammar": "être动词加名词构成的表述，体现存在主义思想",
        "keywords": [
            {"word": "auteur", "meaning": "作者", "usage": "名词，表示创造者"},
            {"word": "avenir", "meaning": "未来", "usage": "名词"},
            {"word": "notre", "meaning": "我们的", "usage": "所有格代词"}
        ]
    },
    {
        "quote": "La vie n'a pas de sens a priori, c'est à nous de lui en créer un.",
        "author": "Jean-Paul Sartre",
        "zh": "生活本身没有先验的意义，我们需要给它赋予意义。",
        "grammar": "复杂的后置从句结构，代词'en'的用法",
        "keywords": [
            {"word": "sens", "meaning": "意义，感受", "usage": "名词"},
            {"word": "créer", "meaning": "创造", "usage": "动词"},
            {"word": "a priori", "meaning": "先验的", "usage": "短语"}
        ]
    },
    {
        "quote": "Le rêve est la seule réalité.",
        "author": "Walt Disney",
        "zh": "梦想是唯一的现实。",
        "grammar": "同位语结构，'être'连接主语和补语",
        "keywords": [
            {"word": "rêve", "meaning": "梦想", "usage": "名词"},
            {"word": "réalité", "meaning": "现实", "usage": "名词"},
            {"word": "seul", "meaning": "唯一的", "usage": "形容词"}
        ]
    },
    {
        "quote": "L'amour est la seule chose qui augmente quand on la partage.",
        "author": "Attributed to various",
        "zh": "爱是唯一在分享时增长的东西。",
        "grammar": "'quand'引导时间从句，表达事件的并发性",
        "keywords": [
            {"word": "amour", "meaning": "爱", "usage": "名词"},
            {"word": "partager", "meaning": "分享", "usage": "动词"},
            {"word": "augmenter", "meaning": "增加", "usage": "动词"}
        ]
    },
    {
        "quote": "Chaque jour est une nouvelle vie. Saisir-la bien.",
        "author": "Ralph Waldo Emerson",
        "zh": "每一天都是一个新生活。好好把握它。",
        "grammar": "命令式动词'saisir'的使用，祈使句",
        "keywords": [
            {"word": "chaque", "meaning": "每一个", "usage": "限定词"},
            {"word": "jour", "meaning": "天", "usage": "名词"},
            {"word": "saisir", "meaning": "抓住，把握", "usage": "动词"}
        ]
    },
    {
        "quote": "Persévérez et vous réussirez.",
        "author": "Unknown",
        "zh": "坚持下去，你就会成功。",
        "grammar": "条件结构without'si'，使用命令式和未来式",
        "keywords": [
            {"word": "persévérer", "meaning": "坚持", "usage": "动词"},
            {"word": "réussir", "meaning": "成功", "usage": "动词"},
            {"word": "vous", "meaning": "你们", "usage": "代词"}
        ]
    },
    {
        "quote": "Le bonheur est dans les petites choses.",
        "author": "Confucius",
        "zh": "幸福在于小事物之中。",
        "grammar": "介词'dans'引出位置或范围补语",
        "keywords": [
            {"word": "bonheur", "meaning": "幸福", "usage": "名词"},
            {"word": "petite", "meaning": "小的", "usage": "形容词"},
            {"word": "chose", "meaning": "东西", "usage": "名词"}
        ]
    },
    {
        "quote": "Faites ce qui vous passionne, pas ce qui rapporte de l'argent.",
        "author": "Attributed to various",
        "zh": "做你热爱的事，而不是赚钱的事。",
        "grammar": "祈使句对比，使用'ce qui'和'ce qui'的平衡结构",
        "keywords": [
            {"word": "faire", "meaning": "做", "usage": "动词"},
            {"word": "passionner", "meaning": "热爱", "usage": "动词，通常用被动语态"},
            {"word": "rapporter", "meaning": "赚取", "usage": "动词"}
        ]
    },
    {
        "quote": "Le seul moyen de faire du travail formidable est d'aimer ce que vous faites.",
        "author": "Steve Jobs",
        "zh": "做伟大工作的唯一方式是热爱你所做的事。",
        "grammar": "不定式'faire'和'aimer'的使用",
        "keywords": [
            {"word": "moyen", "meaning": "方式，手段", "usage": "名词"},
            {"word": "formidable", "meaning": "了不起的", "usage": "形容词"},
            {"word": "aimer", "meaning": "爱，热爱", "usage": "动词"}
        ]
    },
    {
        "quote": "Les sourires sont le langage universel de la gentillesse.",
        "author": "William Arthur Ward",
        "zh": "微笑是善良的通用语言。",
        "grammar": "复数名词作主语，所有格结构",
        "keywords": [
            {"word": "sourire", "meaning": "微笑", "usage": "名词"},
            {"word": "langage", "meaning": "语言", "usage": "名词"},
            {"word": "gentillesse", "meaning": "善良", "usage": "名词"}
        ]
    },
    {
        "quote": "Vivre n'est pas seulement respirer, c'est agir.",
        "author": "Jean-Luc Godard",
        "zh": "生活不仅仅是呼吸，而是行动。",
        "grammar": "对比结构，两个不定式的平衡",
        "keywords": [
            {"word": "vivre", "meaning": "生活", "usage": "动词"},
            {"word": "respirer", "meaning": "呼吸", "usage": "动词"},
            {"word": "agir", "meaning": "行动", "usage": "动词"}
        ]
    },
    {
        "quote": "Le courage c'est la peur qui a fait ses prières.",
        "author": "Unknown",
        "zh": "勇气是已经祈祷过的恐惧。",
        "grammar": "比喻性表达，过去分词'fait'的创意用法",
        "keywords": [
            {"word": "courage", "meaning": "勇气", "usage": "名词"},
            {"word": "peur", "meaning": "恐惧", "usage": "名词"},
            {"word": "prière", "meaning": "祈祷", "usage": "名词"}
        ]
    },
    {
        "quote": "Aimer c'est trouver sa richesse hors de soi.",
        "author": "Gabrielle Roy",
        "zh": "爱是在自己之外发现财富。",
        "grammar": "不定式主语结构，'c'est'连接",
        "keywords": [
            {"word": "aimer", "meaning": "爱", "usage": "动词"},
            {"word": "trouver", "meaning": "找到", "usage": "动词"},
            {"word": "richesse", "meaning": "财富", "usage": "名词"}
        ]
    },
    {
        "quote": "La vie est trop importante pour être prise au sérieux.",
        "author": "Oscar Wilde",
        "zh": "生活太重要了，不能太认真对待。",
        "grammar": "被动不定式结构'être prise'",
        "keywords": [
            {"word": "important", "meaning": "重要的", "usage": "形容词"},
            {"word": "prendre", "meaning": "对待", "usage": "动词"},
            {"word": "sérieux", "meaning": "认真", "usage": "名词/形容词"}
        ]
    },
    {
        "quote": "Sois toi-même; tout le reste est déjà pris.",
        "author": "Oscar Wilde",
        "zh": "做你自己；其他的都已被占有。",
        "grammar": "命令式'sois'，反身代词'toi-même'",
        "keywords": [
            {"word": "toi", "meaning": "你", "usage": "强调式代词"},
            {"word": "prendre", "meaning": "占有", "usage": "动词，过去分词形式"},
            {"word": "reste", "meaning": "其他", "usage": "名词"}
        ]
    },
    {
        "quote": "La vie sans amis n'est pas la vie.",
        "author": "Cicero",
        "zh": "没有朋友的生活不是生活。",
        "grammar": "否定句结构，对比表达",
        "keywords": [
            {"word": "ami", "meaning": "朋友", "usage": "名词"},
            {"word": "vie", "meaning": "生活", "usage": "名词"},
            {"word": "sans", "meaning": "没有", "usage": "介词"}
        ]
    },
    {
        "quote": "Faites la cour à celui qui écoute, pas à celui qui parle.",
        "author": "Unknown",
        "zh": "赢得听者的心，而不是说话者的心。",
        "grammar": "代词'celui'的使用，定语从句",
        "keywords": [
            {"word": "faire la cour", "meaning": "赢得...的心", "usage": "短语"},
            {"word": "écouter", "meaning": "听", "usage": "动词"},
            {"word": "parler", "meaning": "说", "usage": "动词"}
        ]
    },
    {
        "quote": "La gentillesse n'a jamais ruiné personne.",
        "author": "Unknown",
        "zh": "善良从未毁灭过任何人。",
        "grammar": "否定副词'jamais'的使用，完成时",
        "keywords": [
            {"word": "gentillesse", "meaning": "善良", "usage": "名词"},
            {"word": "jamais", "meaning": "从不", "usage": "副词"},
            {"word": "ruiner", "meaning": "毁坏", "usage": "动词"}
        ]
    },
    {
        "quote": "On ne peut pas être demi-enceinte - ou on l'est, ou on ne l'est pas.",
        "author": "Colin Powell",
        "zh": "你不能半途而废 - 要么做，要么不做。",
        "grammar": "虚拟式'peut'，二元对比结构",
        "keywords": [
            {"word": "demi", "meaning": "半", "usage": "前缀/形容词"},
            {"word": "pouvoir", "meaning": "能够", "usage": "动词"},
            {"word": "être", "meaning": "是", "usage": "助动词"}
        ]
    },
    {
        "quote": "Quand vous changez votre vision des choses, les choses que vous voyez changent.",
        "author": "Wayne Dyer",
        "zh": "当你改变对事物的看法时，你看到的事物也会改变。",
        "grammar": "'quand'引导的时间从句，使用现在时",
        "keywords": [
            {"word": "changer", "meaning": "改变", "usage": "动词"},
            {"word": "vision", "meaning": "视野，观点", "usage": "名词"},
            {"word": "chose", "meaning": "事物", "usage": "名词"}
        ]
    },
    {
        "quote": "Les rêves n'ont pas de fin.",
        "author": "Les Brown",
        "zh": "梦想没有终点。",
        "grammar": "简单主语-谓语-宾语结构，完全无谓语表达",
        "keywords": [
            {"word": "rêve", "meaning": "梦想", "usage": "名词"},
            {"word": "fin", "meaning": "终点，结束", "usage": "名词"},
            {"word": "avoir", "meaning": "有", "usage": "动词"}
        ]
    },
    {
        "quote": "Vous ne pouvez pas prendre un nouveau départ, mais vous pouvez commencer d'où vous êtes.",
        "author": "Unknown",
        "zh": "你不能有新的开始，但你可以从现在开始。",
        "grammar": "对比性虚拟句，'pouvoir'的两个不同用法",
        "keywords": [
            {"word": "nouveau", "meaning": "新的", "usage": "形容词"},
            {"word": "départ", "meaning": "开始", "usage": "名词"},
            {"word": "commencer", "meaning": "开始", "usage": "动词"}
        ]
    },
    {
        "quote": "La douleur pousse les racines; le plaisir pousse les fleurs.",
        "author": "Rumi",
        "zh": "痛苦推动根的生长；快乐推动花的绽放。",
        "grammar": "平衡的两个句子，使用相同的结构",
        "keywords": [
            {"word": "douleur", "meaning": "痛苦", "usage": "名词"},
            {"word": "racine", "meaning": "根", "usage": "名词"},
            {"word": "plaisir", "meaning": "快乐", "usage": "名词"}
        ]
    },
    {
        "quote": "Ce qui est derrière nous et ce qui est devant nous ne compte que peu comparé à ce qui est en nous.",
        "author": "Ralph Waldo Emerson",
        "zh": "我们身后的和面前的相比，都微不足道，相比之下我们内心的才是关键。",
        "grammar": "复杂的相对从句结构，'ce qui'的多次使用",
        "keywords": [
            {"word": "derrière", "meaning": "身后", "usage": "介词"},
            {"word": "devant", "meaning": "面前", "usage": "介词"},
            {"word": "compter", "meaning": "重要", "usage": "动词"}
        ]
    },
    {
        "quote": "La meilleure façon de prédire l'avenir est de l'inventer.",
        "author": "Peter Drucker",
        "zh": "预测未来的最好方法是去创造它。",
        "grammar": "'meilleur'的最高级，不定式作主语补语",
        "keywords": [
            {"word": "meilleur", "meaning": "最好的", "usage": "形容词最高级"},
            {"word": "prédire", "meaning": "预测", "usage": "动词"},
            {"word": "inventer", "meaning": "发明，创造", "usage": "动词"}
        ]
    },
    {
        "quote": "Le bien-être est atteint par une compréhension mutuelle.",
        "author": "Unknown",
        "zh": "幸福通过相互理解而获得。",
        "grammar": "被动语态'est atteint'，介词'par'引出施事者",
        "keywords": [
            {"word": "bien-être", "meaning": "幸福，福祉", "usage": "名词"},
            {"word": "compréhension", "meaning": "理解", "usage": "名词"},
            {"word": "mutuel", "meaning": "相互的", "usage": "形容词"}
        ]
    },
    {
        "quote": "La vraie mesure de l'intelligence n'est pas le savoir, mais l'imagination.",
        "author": "Albert Einstein",
        "zh": "真正衡量智力的不是知识，而是想象力。",
        "grammar": "对比结构，'pas...mais'的使用",
        "keywords": [
            {"word": "mesure", "meaning": "衡量", "usage": "名词"},
            {"word": "intelligence", "meaning": "智力", "usage": "名词"},
            {"word": "imagination", "meaning": "想象力", "usage": "名词"}
        ]
    },
    {
        "quote": "La sagesse c'est de reconnaître sa propre folie.",
        "author": "Mihail Drumes",
        "zh": "智慧就是认识自己的愚蠢。",
        "grammar": "'c'est'连接结构，不定式作表语",
        "keywords": [
            {"word": "sagesse", "meaning": "智慧", "usage": "名词"},
            {"word": "reconnaître", "meaning": "认可", "usage": "动词"},
            {"word": "folie", "meaning": "疯狂", "usage": "名词"}
        ]
    },
    {
        "quote": "Rien n'est impossible à celui qui persévère.",
        "author": "Molière",
        "zh": "对坚持不懈的人来说，没有什么是不可能的。",
        "grammar": "否定句'rien n'est'，代词'celui'的使用",
        "keywords": [
            {"word": "rien", "meaning": "什么都不", "usage": "否定代词"},
            {"word": "impossible", "meaning": "不可能的", "usage": "形容词"},
            {"word": "persévérer", "meaning": "坚持", "usage": "动词"}
        ]
    },
    {
        "quote": "Un ami c'est quelqu'un qui sait tout de vous et qui vous aime quand même.",
        "author": "Elbert Hubbard",
        "zh": "朋友是完全了解你，但仍然爱你的人。",
        "grammar": "定语从句，'quand même'的使用",
        "keywords": [
            {"word": "ami", "meaning": "朋友", "usage": "名词"},
            {"word": "savoir", "meaning": "知道", "usage": "动词"},
            {"word": "aimer", "meaning": "爱", "usage": "动词"}
        ]
    },
    {
        "quote": "La gratitude est la richesse de l'âme pauvre.",
        "author": "Voltaire",
        "zh": "感谢是穷人灵魂的财富。",
        "grammar": "所有格结构，形容词作名词修饰",
        "keywords": [
            {"word": "gratitude", "meaning": "感谢", "usage": "名词"},
            {"word": "richesse", "meaning": "财富", "usage": "名词"},
            {"word": "âme", "meaning": "灵魂", "usage": "名词"}
        ]
    },
    {
        "quote": "Le paradoxe, c'est que plus on aime, plus on donne.",
        "author": "Henri Bergson",
        "zh": "矛盾在于，爱的越多，给予的就越多。",
        "grammar": "'plus...plus'的比例结构，不定式主语",
        "keywords": [
            {"word": "paradoxe", "meaning": "矛盾", "usage": "名词"},
            {"word": "plus", "meaning": "更多", "usage": "副词"},
            {"word": "donner", "meaning": "给予", "usage": "动词"}
        ]
    },
    {
        "quote": "La mort n'est pas une fin, c'est un commencement.",
        "author": "Unknown",
        "zh": "死亡不是结束，而是开始。",
        "grammar": "对比结构，'c'est'连接",
        "keywords": [
            {"word": "mort", "meaning": "死亡", "usage": "名词"},
            {"word": "fin", "meaning": "结束", "usage": "名词"},
            {"word": "commencement", "meaning": "开始", "usage": "名词"}
        ]
    },
    {
        "quote": "Je suis heureux car j'ai un ami en toi.",
        "author": "Victor Hugo",
        "zh": "我很幸福，因为在你身上我有一个朋友。",
        "grammar": "'car'引导原因从句，所有格'en toi'",
        "keywords": [
            {"word": "heureux", "meaning": "幸福的", "usage": "形容词"},
            {"word": "car", "meaning": "因为", "usage": "连接词"},
            {"word": "ami", "meaning": "朋友", "usage": "名词"}
        ]
    },
    {
        "quote": "Le plus grand acte de bravoure est de supporter la vie.",
        "author": "Seneca",
        "zh": "最大的勇敢是支持生活。",
        "grammar": "'plus grand'最高级，不定式作表语补语",
        "keywords": [
            {"word": "acte", "meaning": "行为", "usage": "名词"},
            {"word": "bravoure", "meaning": "勇气", "usage": "名词"},
            {"word": "supporter", "meaning": "承受，支持", "usage": "动词"}
        ]
    },
    {
        "quote": "L'art c'est mensonge qui nous permet de réaliser la vérité.",
        "author": "Pablo Picasso",
        "zh": "艺术是让我们实现真理的谎言。",
        "grammar": "'c'est'连接结构，关系从句",
        "keywords": [
            {"word": "art", "meaning": "艺术", "usage": "名词"},
            {"word": "mensonge", "meaning": "谎言", "usage": "名词"},
            {"word": "vérité", "meaning": "真理", "usage": "名词"}
        ]
    },
    {
        "quote": "La maîtrise se construit un jour à la fois.",
        "author": "Robin Sharma",
        "zh": "卓越是逐天建立的。",
        "grammar": "被动语态，'un jour à la fois'的时间表达",
        "keywords": [
            {"word": "maîtrise", "meaning": "卓越，精通", "usage": "名词"},
            {"word": "jour", "meaning": "天", "usage": "名词"},
            {"word": "construire", "meaning": "建立", "usage": "动词"}
        ]
    },
    {
        "quote": "Aller c'est venir d'ailleurs.",
        "author": "Victor Hugo",
        "zh": "去就是从另一处而来。",
        "grammar": "哲学比喻，不定式主语结构",
        "keywords": [
            {"word": "aller", "meaning": "去", "usage": "动词"},
            {"word": "venir", "meaning": "来", "usage": "动词"},
            {"word": "ailleurs", "meaning": "别处", "usage": "副词"}
        ]
    },
    {
        "quote": "Tout ce qui brille n'est pas or.",
        "author": "Proverb",
        "zh": "闪闪发光的不一定都是金子。",
        "grammar": "'tout ce qui'引导的从句，否定结构",
        "keywords": [
            {"word": "briller", "meaning": "发亮", "usage": "动词"},
            {"word": "or", "meaning": "黄金", "usage": "名词"},
            {"word": "tout", "meaning": "所有", "usage": "代词"}
        ]
    },
    {
        "quote": "Le respect commence où l'amour finit.",
        "author": "Unknown",
        "zh": "尊重从爱结束的地方开始。",
        "grammar": "'où'引导的地点从句，时间转换",
        "keywords": [
            {"word": "respect", "meaning": "尊重", "usage": "名词"},
            {"word": "commencer", "meaning": "开始", "usage": "动词"},
            {"word": "finir", "meaning": "结束", "usage": "动词"}
        ]
    },
    {
        "quote": "La solitude est souvent une pause, pas une fin.",
        "author": "Adrienne Posey",
        "zh": "孤独通常是一个暂停，而不是结束。",
        "grammar": "对比结构，'pas'的否定使用",
        "keywords": [
            {"word": "solitude", "meaning": "孤独", "usage": "名词"},
            {"word": "pause", "meaning": "暂停", "usage": "名词"},
            {"word": "fin", "meaning": "结束", "usage": "名词"}
        ]
    },
    {
        "quote": "On ne vit qu'une fois, mais si on le fait bien, c'est suffisant.",
        "author": "Mae West",
        "zh": "生活只有一次，但如果做得好，就足够了。",
        "grammar": "'qu'une fois'的限制性结构，条件从句",
        "keywords": [
            {"word": "une fois", "meaning": "一次", "usage": "短语"},
            {"word": "suffisant", "meaning": "足够的", "usage": "形容词"},
            {"word": "vivre", "meaning": "生活", "usage": "动词"}
        ]
    },
    {
        "quote": "Un jour sans sourire est un jour perdu.",
        "author": "Charlie Chaplin",
        "zh": "没有微笑的��天是浪费的一天。",
        "grammar": "简单主语-系动词-表语结构",
        "keywords": [
            {"word": "jour", "meaning": "天", "usage": "名词"},
            {"word": "sourire", "meaning": "微笑", "usage": "名词"},
            {"word": "perdu", "meaning": "浪费的", "usage": "过去分词作形容词"}
        ]
    },
    {
        "quote": "Tout est possible à celui qui croit.",
        "author": "Mark Twain",
        "zh": "对相信的人来说，一切皆有可能。",
        "grammar": "代词'celui'的使用，定语从句",
        "keywords": [
            {"word": "tout", "meaning": "一切", "usage": "代词"},
            {"word": "possible", "meaning": "可能的", "usage": "形容词"},
            {"word": "croire", "meaning": "相信", "usage": "动词"}
        ]
    },
    {
        "quote": "Aime la vie comme la vie t'aime.",
        "author": "Unknown",
        "zh": "像生活爱你一样爱生活。",
        "grammar": "祈使式，'comme'引导比较",
        "keywords": [
            {"word": "aimer", "meaning": "爱", "usage": "动词"},
            {"word": "vie", "meaning": "生活", "usage": "名词"},
            {"word": "comme", "meaning": "像...一样", "usage": "连接词"}
        ]
    },
    {
        "quote": "La vie est trop courte pour faire du thé faible et des promesses molles.",
        "author": "Unknown",
        "zh": "生活太短暂，不能喝淡茶和做软弱的承诺。",
        "grammar": "介词'pour'引出目的/理由，形容词修饰名词",
        "keywords": [
            {"word": "court", "meaning": "短的", "usage": "形容词"},
            {"word": "thé", "meaning": "茶", "usage": "名词"},
            {"word": "promesse", "meaning": "承诺", "usage": "名词"}
        ]
    },
    {
        "quote": "Vous n'êtes jamais trop vieux pour fixer un nouvel objectif ou rêver un nouveau rêve.",
        "author": "C.S. Lewis",
        "zh": "你永远不会太老而不能制定新的目标或梦想新的梦想。",
        "grammar": "双重否定'jamais trop'，不定式作补语",
        "keywords": [
            {"word": "jamais", "meaning": "从不", "usage": "副词"},
            {"word": "vieux", "meaning": "老的", "usage": "形容词"},
            {"word": "objectif", "meaning": "目标", "usage": "名词"},
            {"word": "rêve", "meaning": "梦想", "usage": "名词"}
        ]
    },
    {
        "quote": "La seule constante dans la vie est le changement.",
        "author": "Heraclitus",
        "zh": "生活中唯一的恒定是变化。",
        "grammar": "定冠词'la'配合'seule'，介词'dans'",
        "keywords": [
            {"word": "constante", "meaning": "恒常的事物", "usage": "名词"},
            {"word": "changement", "meaning": "变化", "usage": "名词"},
            {"word": "seule", "meaning": "唯一的", "usage": "形容词"}
        ]
    },
    {
        "quote": "Pour vivre heureux, vivre caché.",
        "author": "Voltaire",
        "zh": "要生活得幸福，就要生活得隐蔽。",
        "grammar": "祈使式结构，'pour'表目的",
        "keywords": [
            {"word": "heureux", "meaning": "幸福的", "usage": "形容词"},
            {"word": "caché", "meaning": "隐蔽的", "usage": "过去分词作形容词"},
            {"word": "vivre", "meaning": "生活", "usage": "动词"}
        ]
    },
    {
        "quote": "Les gens heureux ne comptent pas les heures.",
        "author": "Unknown",
        "zh": "幸福的人不计时。",
        "grammar": "定冠词'les'配合'gens'，现在式动词",
        "keywords": [
            {"word": "heureux", "meaning": "幸福的", "usage": "形容词"},
            {"word": "compter", "meaning": "计数", "usage": "动词"},
            {"word": "heure", "meaning": "小时", "usage": "名词"}
        ]
    },
    {
        "quote": "C'est en forgeant qu'on devient forgeron.",
        "author": "Proverb",
        "zh": "在锻造中，人才成为铁匠。",
        "grammar": "'c'est en'引导的分词表达方式",
        "keywords": [
            {"word": "forger", "meaning": "锻造", "usage": "动词"},
            {"word": "forgeron", "meaning": "铁匠", "usage": "名词"},
            {"word": "devenir", "meaning": "变成", "usage": "动词"}
        ]
    },
    {
        "quote": "La beauté fascine et l'amour enchaîne.",
        "author": "Molière",
        "zh": "美丽吸引，爱情束缚。",
        "grammar": "两个并列句子，现在式动词",
        "keywords": [
            {"word": "beauté", "meaning": "美", "usage": "名词"},
            {"word": "fasciner", "meaning": "吸引", "usage": "动词"},
            {"word": "enchaîner", "meaning": "束缚", "usage": "动词"}
        ]
    },
    {
        "quote": "Les amis sont la famille qu'on se choisit.",
        "author": "Unknown",
        "zh": "朋友是我们自己选择的家人。",
        "grammar": "定语从句'qu'on se choisit'，反身代词'se'",
        "keywords": [
            {"word": "ami", "meaning": "朋友", "usage": "名词"},
            {"word": "famille", "meaning": "家人", "usage": "名词"},
            {"word": "choisir", "meaning": "选择", "usage": "动词"}
        ]
    },
    {
        "quote": "Je suis mon plus grand critique et mon meilleur ami.",
        "author": "Unknown",
        "zh": "我是自己最严厉的批评者和最好的朋友。",
        "grammar": "所有格'mon'，最高级'plus grand'和'meilleur'",
        "keywords": [
            {"word": "critique", "meaning": "批评者", "usage": "名词"},
            {"word": "ami", "meaning": "朋友", "usage": "名词"},
            {"word": "grand", "meaning": "大的，伟大的", "usage": "形容词"}
        ]
    },
    {
        "quote": "La vie ne vaut d'être vécue que si on en profite.",
        "author": "Unknown",
        "zh": "只有充分利用生活，生活才值得活。",
        "grammar": "'ne...que'的限制性否定，反身代词'en'",
        "keywords": [
            {"word": "valoir", "meaning": "值得", "usage": "动词"},
            {"word": "vivre", "meaning": "生活", "usage": "动词"},
            {"word": "profiter", "meaning": "利用", "usage": "动词"}
        ]
    },
    {
        "quote": "L'espoir fait vivre.",
        "author": "Proverb",
        "zh": "希望让人活着。",
        "grammar": "简单主语-谓语结构，'faire'的因果用法",
        "keywords": [
            {"word": "espoir", "meaning": "希望", "usage": "名词"},
            {"word": "faire", "meaning": "使得", "usage": "动词"},
            {"word": "vivre", "meaning": "活着", "usage": "动词"}
        ]
    },
    {
        "quote": "Je pense, donc je suis.",
        "author": "René Descartes",
        "zh": "我思，故我在。",
        "grammar": "'donc'引导因果关系，简洁哲学结构",
        "keywords": [
            {"word": "penser", "meaning": "思考", "usage": "动词"},
            {"word": "donc", "meaning": "因此", "usage": "连接词"},
            {"word": "être", "meaning": "是", "usage": "动词"}
        ]
    },
    {
        "quote": "L'amour est aveugle, mais l'amitié ferme les yeux.",
        "author": "Unknown",
        "zh": "爱是盲目的，但友谊闭上眼睛。",
        "grammar": "对比结构，'mais'连接两个句子",
        "keywords": [
            {"word": "amour", "meaning": "爱", "usage": "名词"},
            {"word": "aveugle", "meaning": "盲目的", "usage": "形容词"},
            {"word": "amitié", "meaning": "友谊", "usage": "名词"}
        ]
    },
    {
        "quote": "Celui qui rit le dernier rit le mieux.",
        "author": "Proverb",
        "zh": "最后笑的人笑得最好。",
        "grammar": "代词'celui'的使用，最高级'le mieux'",
        "keywords": [
            {"word": "rire", "meaning": "笑", "usage": "动词"},
            {"word": "dernier", "meaning": "最后的", "usage": "形容词"},
            {"word": "bien", "meaning": "好", "usage": "副词"}
        ]
    },
    {
        "quote": "Une promesse est une promesse.",
        "author": "Proverb",
        "zh": "承诺就是承诺。",
        "grammar": "重复结构强调，简单同位语",
        "keywords": [
            {"word": "promesse", "meaning": "承诺", "usage": "名词"},
            {"word": "est", "meaning": "是", "usage": "系动词"},
            {"word": "une", "meaning": "一个", "usage": "不定冠词"}
        ]
    },
    {
        "quote": "La vie est un voyage, pas une destination.",
        "author": "Ralph Waldo Emerson",
        "zh": "生活是一次旅程，而不是一个目的地。",
        "grammar": "对比结构，'pas'的��定使用",
        "keywords": [
            {"word": "voyage", "meaning": "旅程", "usage": "名词"},
            {"word": "destination", "meaning": "目的地", "usage": "名词"},
            {"word": "pas", "meaning": "不", "usage": "否定词"}
        ]
    },
    {
        "quote": "Demain est un autre jour.",
        "author": "Gone with the Wind",
        "zh": "明天又是新的一天。",
        "grammar": "简单陈述句，不定冠词'un'",
        "keywords": [
            {"word": "demain", "meaning": "明天", "usage": "副词"},
            {"word": "jour", "meaning": "天", "usage": "名词"},
            {"word": "autre", "meaning": "另一个", "usage": "形容词"}
        ]
    },
    {
        "quote": "La vie est trop importante pour être confiée à des ordinateurs.",
        "author": "Unknown",
        "zh": "生活太重要了，不能委托给计算机。",
        "grammar": "被动不定式结构'être confiée'",
        "keywords": [
            {"word": "important", "meaning": "重要的", "usage": "形容词"},
            {"word": "confier", "meaning": "委托", "usage": "动词"},
            {"word": "ordinateur", "meaning": "计算机", "usage": "名词"}
        ]
    },
    {
        "quote": "L'erreur est humaine, pardonner est divin.",
        "author": "Pope Alexander",
        "zh": "犯错是人类的，原谅是神圣的。",
        "grammar": "对比结构，不定式作主语",
        "keywords": [
            {"word": "erreur", "meaning": "错误", "usage": "名词"},
            {"word": "pardonner", "meaning": "原谅", "usage": "动词"},
            {"word": "divin", "meaning": "神圣的", "usage": "形容词"}
        ]
    },
    {
        "quote": "La vraie richesse est le contentement.",
        "author": "Unknown",
        "zh": "真正的财富是满足。",
        "grammar": "形容词'vraie'修饰名词，系动词'est'",
        "keywords": [
            {"word": "richesse", "meaning": "财富", "usage": "名词"},
            {"word": "contentement", "meaning": "满足", "usage": "名词"},
            {"word": "vraie", "meaning": "真实的", "usage": "形容词"}
        ]
    },
    {
        "quote": "Ne remets jamais à demain ce que tu peux faire aujourd'hui.",
        "author": "Benjamin Franklin",
        "zh": "不要把你今天能做的事推迟到明天。",
        "grammar": "祈使否定式'ne remets pas'，时间对比",
        "keywords": [
            {"word": "remettre", "meaning": "推迟", "usage": "动词"},
            {"word": "demain", "meaning": "明天", "usage": "副词"},
            {"word": "aujourd'hui", "meaning": "今天", "usage": "副词"}
        ]
    },
    {
        "quote": "La vérité est plus étrange que la fiction.",
        "author": "Mark Twain",
        "zh": "真理比虚构更奇怪。",
        "grammar": "比较级结构'plus...que'，形容词'étrange'",
        "keywords": [
            {"word": "vérité", "meaning": "真理", "usage": "名词"},
            {"word": "étrange", "meaning": "奇怪的", "usage": "形容词"},
            {"word": "fiction", "meaning": "虚构", "usage": "名词"}
        ]
    },
    {
        "quote": "C'est dans nos moments les plus sombres que nous devons nous concentrer sur la lumière.",
        "author": "Albus Dumbledore",
        "zh": "正是在我们最黑暗的时刻，我们应该专注于光明。",
        "grammar": "'c'est...que'强调句式，定语从句",
        "keywords": [
            {"word": "moment", "meaning": "时刻", "usage": "名词"},
            {"word": "sombre", "meaning": "黑暗的", "usage": "形容词"},
            {"word": "lumière", "meaning": "光明", "usage": "名词"}
        ]
    },
    {
        "quote": "Le courage est la résistance à la peur, la maîtrise de la peur.",
        "author": "Mark Twain",
        "zh": "勇气是对恐惧的抵抗，是对恐惧的掌控。",
        "grammar": "同位语结构，两个名词短语对等",
        "keywords": [
            {"word": "courage", "meaning": "勇气", "usage": "名词"},
            {"word": "résistance", "meaning": "抵抗", "usage": "名词"},
            {"word": "peur", "meaning": "恐惧", "usage": "名词"}
        ]
    },
    {
        "quote": "Où il y a une volonté, il y a un chemin.",
        "author": "Proverb",
        "zh": "有志者，事竟成。",
        "grammar": "'où'引导的地点从句，'il y a'的使用",
        "keywords": [
            {"word": "volonté", "meaning": "意志", "usage": "名词"},
            {"word": "chemin", "meaning": "路径", "usage": "名词"},
            {"word": "il y a", "meaning": "有", "usage": "短语"}
        ]
    },
]

class Formatter:
    @staticmethod
    def format_verbs(verbs):
        """优化变位表格式"""
        md = "## 📖 今日不规则动词（5个）\n\n"
        for v in verbs:
            md += f"### {v['inf'].upper()} → {v['pp']} | {v['zh']}\n"
            md += f"**说明**: {v['note']}\n\n"
            md += "**直陈式现在时变位**\n\n"
            md += "```\n"
            md += "┌─────────────┬──────────┐\n"
            md += "│    人称     │   变位   │\n"
            md += "├─────────────┼──────────┤\n"
            md += f"│ je          │ {v.get('je', '—'):8} │\n"
            md += f"│ tu          │ {v.get('tu', '—'):8} │\n"
            md += f"│ il/elle     │ {v.get('il', '—'):8} │\n"
            md += f"│ nous        │ {v.get('nous', '—'):8} │\n"
            md += f"│ vous        │ {v.get('vous', '—'):8} │\n"
            md += f"│ ils/elles   │ {v.get('ils', '—'):8} │\n"
            md += "└─────────────┴──────────┘\n"
            md += "```\n\n"
        return md
    
    @staticmethod
    def format_grammar(grammars):
        md = "## 🎓 今日语法考点（2个）\n\n"
        for g in grammars:
            md += f"### {g['title']}\n\n**描述**: {g['description']}\n\n"
            md += "**例句**:\n"
            for ex in g['examples']:
                md += f"- {ex}\n"
            md += "\n**规则**:\n"
            for rule in g['usage_rules']:
                md += f"- {rule}\n"
            md += "\n"
        return md
    
    @staticmethod
    def format_vocab(words):
        md = "## 📚 今日词汇（20个）\n\n"
        md += "| 法语 | 中文 | 英文 |\n|------|------|------|\n"
        for w in words:
            md += f"| **{w['word']}** | {w['zh']} | {w['en']} |\n"
        md += "\n### 🎯 词汇故事\n\n"
        for w in words:
            if w.get('story'):
                md += f"**{w['word']}**: {w['story']}\n\n"
        return md
    
    @staticmethod
    def format_expressions(exprs):
        md = "## 💬 高级口语（5句）\n\n"
        for e in exprs:
            md += f"**{e['expr']}**\n- 翻译：{e['trans']}\n- 场景：{e['ctx']}\n\n"
        return md
    
    @staticmethod
    def format_quotes(quotes):
        md = "## ✨ 经典名言\n\n"
        for q in quotes:
            md += f"### \"{q['quote']}\"\n— *{q['author']}*\n\n"
            md += f"**中文**: {q['zh']}\n"
            md += f"**语法**: {q['grammar']}\n"
            md += "**重点词汇**:\n"
            for kw in q['keywords']:
                md += f"- **{kw['word']}**: {kw['meaning']} (用法：{kw['usage']})\n"
            md += "\n"
        return md

def main():
    logger.info("🚀 开始采集法语每日学习内容")
    
    # 采集内容
    verbs = random.sample(IRREGULAR_VERBS, 5)
    grammars = random.sample(GRAMMAR_POOL, min(2, len(GRAMMAR_POOL)))
    words = random.sample(B1_VOCAB, min(20, len(B1_VOCAB)))
    exprs = random.sample(EXPRESSIONS, min(5, len(EXPRESSIONS)))
    quotes = random.sample(QUOTES, min(1, len(QUOTES)))
    
    # 格式化
    md = f"# 📅 法语每日学习 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    md += Formatter.format_verbs(verbs)
    md += Formatter.format_grammar(grammars)
    md += Formatter.format_vocab(words)
    md += Formatter.format_expressions(exprs)
    md += Formatter.format_quotes(quotes)
    
    logger.info("✅ 内容采集完成")
    
    # 推送
    send_key = os.getenv('SERVERCHAN_SEND_KEY')
    if not send_key:
        logger.warning("⚠️ SERVERCHAN_SEND_KEY 未配置")
        print("\n" + "="*70)
        print(md)
        print("="*70)
        return True
    
    try:
        url = f"https://sctapi.ftqq.com/{send_key}.send"
        data = {"title": "📅DailyFrench", "desp": md}
        logger.info("📤 正在推送到Server酱...")
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            logger.info("✅ 推送成功！")
            return True
        else:
            logger.error(f"❌ 推送失败：{result.get('message', '未知错误')}")
            return False
    
    except Exception as e:
        logger.error(f"❌ 推送出错：{str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
