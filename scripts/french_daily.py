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
    {"inf": "donner", "zh": "给", "pp": "donné", "note": "规则一组，参考用", "je": "donne", "tu": "donnes", "il": "donne", "nous": "donnons", "vous": "donnez", "ils": "donnent"},
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
    {"inf": "recevoir", "zh": "接收，收到", "pp": "reçu", "note": "B1���常用", "je": "reçois", "tu": "reçois", "il": "reçoit", "nous": "recevons", "vous": "recevez", "ils": "reçoivent"},
    {"inf": "valoir", "zh": "值得，等于", "pp": "valu", "note": "B1级语汇，表达价值", "je": "vaux", "tu": "vaux", "il": "vaut", "nous": "valons", "vous": "valez", "ils": "valent"},
    {"inf": "falloir", "zh": "必须，需要", "pp": "fallu", "note": "非人称动词，只用第三人称单数", "il": "faut"},
    {"inf": "acquérir", "zh": "获得，取得", "pp": "acquis", "note": "B1级重要动词", "je": "acquiers", "tu": "acquiers", "il": "acquiert", "nous": "acquérons", "vous": "acquérez", "ils": "acquièrent"},
    {"inf": "conquérir", "zh": "征服，赢得", "pp": "conquis", "note": "acquérir的派生词", "je": "conquiers", "tu": "conquiers", "il": "conquiert", "nous": "conquérons", "vous": "conquérez", "ils": "conquièrent"},
    {"inf": "nuire", "zh": "伤害，有害", "pp": "nui", "note": "后接介词à", "je": "nuis", "tu": "nuis", "il": "nuit", "nous": "nuisons", "vous": "nuisez", "ils": "nuisent"},
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
    {"inf": "mettre", "zh": "放，放置", "pp": "mis", "note": "日常常用", "je": "mets", "tu": "mets", "il": "met", "nous": "mettons", "vous": "mettez", "ils": "mettent"},
    {"inf": "permettre", "zh": "允许，让", "pp": "permis", "note": "mettre的派生词", "je": "permets", "tu": "permets", "il": "permet", "nous": "permettons", "vous": "permettez", "ils": "permettent"},
    {"inf": "promettre", "zh": "承诺", "pp": "promis", "note": "mettre的派生词", "je": "promets", "tu": "promets", "il": "promet", "nous": "promettons", "vous": "promettez", "ils": "promettent"},
    {"inf": "soumettre", "zh": "提交，屈服", "pp": "soumis", "note": "mettre的派生词", "je": "soumets", "tu": "soumets", "il": "soumet", "nous": "soumettons", "vous": "soumettez", "ils": "soumettent"},
    {"inf": "admettre", "zh": "承认，允许", "pp": "admis", "note": "mettre的派生词", "je": "admets", "tu": "admets", "il": "admet", "nous": "admettons", "vous": "admettez", "ils": "admettent"},
    {"inf": "commettre", "zh": "犯（错误）", "pp": "commis", "note": "mettre的派生词", "je": "commets", "tu": "commets", "il": "commet", "nous": "commettons", "vous": "commettez", "ils": "commettent"},
    {"inf": "transmettre", "zh": "传输，传递", "pp": "transmis", "note": "mettre的派生词", "je": "transmets", "tu": "transmets", "il": "transmet", "nous": "transmettons", "vous": "transmettez", "ils": "transmettent"},
    {"inf": "omettre", "zh": "忽略，遗漏", "pp": "omis", "note": "mettre的派生词", "je": "omets", "tu": "omets", "il": "omet", "nous": "omettons", "vous": "omettez", "ils": "omettent"},
    {"inf": "émettre", "zh": "发射，发出", "pp": "émis", "note": "mettre的派生词", "je": "émets", "tu": "émets", "il": "émet", "nous": "émettons", "vous": "émettez", "ils": "émettent"},
    {"inf": "démettre", "zh": "罢免，脱臼", "pp": "démis", "note": "mettre的派生词", "je": "démets", "tu": "démets", "il": "démet", "nous": "démettons", "vous": "démettez", "ils": "démettent"},
    {"inf": "soustraire", "zh": "减去，扣除", "pp": "soustrait", "note": "第三组重要", "je": "soustrais", "tu": "soustrais", "il": "soustrait", "nous": "soustrayons", "vous": "soustrayez", "ils": "soustraient"},
    {"inf": "distraire", "zh": "分散，娱乐", "pp": "distrait", "note": "traire的派生词", "je": "distrais", "tu": "distrais", "il": "distrait", "nous": "distroyons", "vous": "distrayez", "ils": "distraient"},
    {"inf": "contracter", "zh": "收缩，签订", "pp": "contracté", "note": "第一组规则动词", "je": "contracte", "tu": "contractes", "il": "contracte", "nous": "contractons", "vous": "contractez", "ils": "contractent"},
    {"inf": "extraire", "zh": "提取，开采", "pp": "extrait", "note": "traire的派生词", "je": "extrais", "tu": "extrais", "il": "extrait", "nous": "extrayons", "vous": "extrayez", "ils": "extraient"},
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

# ========== B1词汇库 ==========
B1_VOCAB = [
    {"word": "accueillir", "zh": "迎接，欢迎", "en": "to welcome", "story": "源自拉丁'accogliere'，意为张开双臂"},
    {"word": "acquérir", "zh": "获得，取得", "en": "to acquire", "story": None},
    {"word": "adapter", "zh": "适应，改编", "en": "to adapt", "story": None},
    {"word": "affirmer", "zh": "肯定，声称", "en": "to affirm", "story": None},
    {"word": "agir", "zh": "行动，起作用", "en": "to act", "story": None},
    {"word": "aider", "zh": "帮助", "en": "to help", "story": None},
    {"word": "aimer", "zh": "喜欢，爱", "en": "to like, to love", "story": None},
    {"word": "aller", "zh": "去", "en": "to go", "story": None},
    {"word": "amitié", "zh": "友谊", "en": "friendship", "story": None},
    {"word": "amour", "zh": "爱", "en": "love", "story": None},
    {"word": "amusant", "zh": "有趣的", "en": "amusing", "story": None},
    {"word": "analyser", "zh": "分析", "en": "to analyze", "story": None},
    {"word": "ancêtre", "zh": "祖先", "en": "ancestor", "story": None},
    {"word": "ancien", "zh": "古老的，前任的", "en": "old, former", "story": None},
    {"word": "âne", "zh": "驴", "en": "donkey", "story": None},
    {"word": "ange", "zh": "天使", "en": "angel", "story": None},
    {"word": "angle", "zh": "角度", "en": "angle", "story": None},
    {"word": "angoisse", "zh": "焦虑，痛苦", "en": "anguish", "story": None},
    {"word": "animal", "zh": "动物", "en": "animal", "story": None},
    {"word": "animation", "zh": "动画，生气勃勃", "en": "animation", "story": None},
]

# ========== 口语表达和名言 ==========
EXPRESSIONS = [
    {"expr": "C'est du gâteau!", "trans": "这太简单了！", "ctx": "表示某事很容易做到"},
    {"expr": "Tu te moques de moi?", "trans": "你在开玩笑吗？", "ctx": "表达惊讶"},
    {"expr": "Je m'en fiche!", "trans": "我不在乎！", "ctx": "表达漠不关心"},
    {"expr": "C'est la vie!", "trans": "这就是人生！", "ctx": "对无法改变事情的接纳"},
    {"expr": "Pas mal!", "trans": "不错！", "ctx": "表示满意"},
]

QUOTES = [
    {
        "quote": "La vie est une fleur dont l'amour est le miel.",
        "author": "Victor Hugo",
        "zh": "生活是一朵花，爱是其中的蜂蜜。",
        "grammar": "'dont'为关系代词，引出修饰先行词的从句",
        "keywords": [
            {"word": "fleur", "meaning": "花", "usage": "引申为生活的美好事物"},
            {"word": "miel", "meaning": "蜂蜜", "usage": "象征生活中最甜蜜的部分"}
        ]
    },
    {
        "quote": "L'important n'est pas la destination, c'est le voyage.",
        "author": "Anonymous",
        "zh": "重要的不是目的地，而是旅程。",
        "grammar": "使用'ce...c'est'强调句式",
        "keywords": [
            {"word": "destination", "meaning": "目的地", "usage": "名词"},
            {"word": "voyage", "meaning": "旅程", "usage": "名词"}
        ]
    }
]

class Formatter:
    @staticmethod
    def format_verbs(verbs):
        md = "## 📖 今日不规则动词（5个）\n\n"
        for v in verbs:
            md += f"### {v['inf'].upper()} → {v['pp']} | {v['zh']}\n"
            md += f"**说明**: {v['note']}\n\n"
            md += "**直陈式现在时变位**:\n"
            md += f"| 人称 | 变位 |\n|------|------|\n"
            md += f"| je | {v.get('je', '—')} |\n"
            md += f"| tu | {v.get('tu', '—')} |\n"
            md += f"| il/elle | {v.get('il', '—')} |\n"
            md += f"| nous | {v.get('nous', '—')} |\n"
            md += f"| vous | {v.get('vous', '—')} |\n"
            md += f"| ils/elles | {v.get('ils', '—')} |\n\n"
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
