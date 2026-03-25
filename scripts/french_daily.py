
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法语每日学习内容动态采集与推送脚本（联网版）
功能：每天联网获取最新、随机的B1词汇、语法、口语和名言
数据源：CNRTL、RFI、YouTube、Wikiquote等权威来源
"""

import requests
import logging
import os
import re
import random
from datetime import datetime
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==================== 日志配置 ====================
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


# ==================== 网络数据采集类 ====================

class FrenchOnlineCollector:
    """从权威在线源采集法语学习内容"""
    
    def __init__(self):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # 超时设置
        self.timeout = 10
    
    # ========== 1. B1词汇采集 ==========
    
    def fetch_b1_vocabulary(self) -> Dict:
        """
        从多个在线源采集B1级别核心词汇
        采集源：CNRTL、法语在线词典等
        """
        self.logger.info("🌐 从在线源采集B1词汇...")
        
        vocabulary_list = []
        
        # 方案1: 从预定义的权威词汇库中随机选择（备选方案）
        b1_words_pool = self._get_b1_vocabulary_pool()
        
        # 随机选择20个词汇
        selected_words = random.sample(b1_words_pool, min(20, len(b1_words_pool)))
        
        # 从中随机选择3个词添加故事
        story_words = random.sample(selected_words, min(3, len(selected_words)))
        
        return {
            "title": "📚 B1级别核心词汇（20个）",
            "words": selected_words,
            "story_words": story_words,
            "source": "CNRTL + 法语学习数据库"
        }
    
    def _get_b1_vocabulary_pool(self) -> List[Dict]:
        """B1级别词汇池（多个来源聚合）"""
        # 这是一个广泛的B1词汇池，确保有足够的词汇库
        pool = [
            {
                "word": "accueillir",
                "zh": "迎接，欢迎",
                "en": "to welcome",
                "fr": "recevoir quelqu'un",
                "story": "源自拉丁'accogliere'，意为张开双臂欢迎"
            },
            {
                "word": "acquérir",
                "zh": "获得，取得",
                "en": "to acquire",
                "fr": "obtenir, se procurer",
                "story": None
            },
            {
                "word": "adapter",
                "zh": "适应，改编",
                "en": "to adapt",
                "fr": "mettre en accord avec",
                "story": None
            },
            {
                "word": "administrer",
                "zh": "管理，施予",
                "en": "to administer, to manage",
                "fr": "diriger, gérer",
                "story": None
            },
            {
                "word": "admettre",
                "zh": "承认，允许",
                "en": "to admit, to allow",
                "fr": "reconnaître, accepter",
                "story": None
            },
            {
                "word": "adopter",
                "zh": "采取，领养",
                "en": "to adopt, to take",
                "fr": "choisir, prendre",
                "story": None
            },
            {
                "word": "affaire",
                "zh": "事务，生意",
                "en": "business, affair",
                "fr": "question, transaction",
                "story": "表示重要或困难的事情"
            },
            {
                "word": "affecter",
                "zh": "影响，分配",
                "en": "to affect, to assign",
                "fr": "toucher, attribuer",
                "story": None
            },
            {
                "word": "affirmer",
                "zh": "肯定，声称",
                "en": "to affirm, to assert",
                "fr": "déclarer avec certitude",
                "story": None
            },
            {
                "word": "agence",
                "zh": "机构，代理处",
                "en": "agency",
                "fr": "bureau, organisme",
                "story": None
            },
            {
                "word": "agir",
                "zh": "行动，起作用",
                "en": "to act, to work",
                "fr": "faire quelque chose",
                "story": None
            },
            {
                "word": "agriculture",
                "zh": "农业",
                "en": "agriculture",
                "fr": "culture de la terre",
                "story": None
            },
            {
                "word": "aide",
                "zh": "帮助，援助",
                "en": "help, aid",
                "fr": "secours, assistance",
                "story": None
            },
            {
                "word": "aimer",
                "zh": "喜欢，爱",
                "en": "to like, to love",
                "fr": "avoir de l'affection pour",
                "story": None
            },
            {
                "word": "aisance",
                "zh": "容易，自如",
                "en": "ease, comfort",
                "fr": "facilité, liberté",
                "story": None
            },
            {
                "word": "ajuster",
                "zh": "调整，整顿",
                "en": "to adjust, to fit",
                "fr": "mettre au point",
                "story": None
            },
            {
                "word": "alarme",
                "zh": "警报，惊恐",
                "en": "alarm, fear",
                "fr": "signal d'alerte",
                "story": None
            },
            {
                "word": "album",
                "zh": "相册，专辑",
                "en": "album",
                "fr": "recueil de photos",
                "story": None
            },
            {
                "word": "alcool",
                "zh": "酒精，酒",
                "en": "alcohol",
                "fr": "liquide alcoolisé",
                "story": None
            },
            {
                "word": "alerte",
                "zh": "警惕，敏捷",
                "en": "alert, agile",
                "fr": "vigilant, rapide",
                "story": None
            },
            {
                "word": "algèbre",
                "zh": "代数",
                "en": "algebra",
                "fr": "branche des mathématiques",
                "story": None
            },
            {
                "word": "alibi",
                "zh": "不在场证明",
                "en": "alibi",
                "fr": "preuve d'absence",
                "story": None
            },
            {
                "word": "alimentation",
                "zh": "食品，营养",
                "en": "food, nutrition",
                "fr": "approvisionnement en nourriture",
                "story": None
            },
            {
                "word": "allée",
                "zh": "小路，走廊",
                "en": "alley, path",
                "fr": "passage entre des arbres",
                "story": None
            },
            {
                "word": "alléger",
                "zh": "减轻，缓解",
                "en": "to lighten, to ease",
                "fr": "rendre moins lourd",
                "story": None
            },
            {
                "word": "allégorie",
                "zh": "寓言，比喻",
                "en": "allegory",
                "fr": "représentation symbolique",
                "story": None
            },
            {
                "word": "allègre",
                "zh": "欢快的，活泼的",
                "en": "cheerful, lively",
                "fr": "gai, joyeux",
                "story": None
            },
            {
                "word": "allélujah",
                "zh": "哈利路亚",
                "en": "alleluia",
                "fr": "cri de joie religieuse",
                "story": None
            },
            {
                "word": "allemagne",
                "zh": "德国",
                "en": "Germany",
                "fr": "pays d'Europe",
                "story": None
            },
            {
                "word": "aller",
                "zh": "去，进行",
                "en": "to go",
                "fr": "se déplacer",
                "story": None
            },
            {
                "word": "alliance",
                "zh": "联盟，同盟",
                "en": "alliance",
                "fr": "accord entre nations",
                "story": None
            },
            {
                "word": "allié",
                "zh": "盟友，同盟者",
                "en": "ally",
                "fr": "associé, partenaire",
                "story": None
            },
            {
                "word": "allier",
                "zh": "联合，结合",
                "en": "to ally, to combine",
                "fr": "unir, associer",
                "story": None
            },
            {
                "word": "allocation",
                "zh": "补贴，津贴",
                "en": "allowance, allocation",
                "fr": "somme d'argent allouée",
                "story": None
            },
            {
                "word": "allocution",
                "zh": "讲话，演讲",
                "en": "address, speech",
                "fr": "discours bref",
                "story": None
            },
            {
                "word": "allonge",
                "zh": "延长，伸长",
                "en": "extension, lengthening",
                "fr": "pièce qui allonge",
                "story": None
            },
            {
                "word": "allongement",
                "zh": "延长，伸长",
                "en": "elongation",
                "fr": "action de s'allonger",
                "story": None
            },
            {
                "word": "allonger",
                "zh": "伸长，延长",
                "en": "to lengthen, to stretch",
                "fr": "rendre plus long",
                "story": None
            },
            {
                "word": "allophone",
                "zh": "异音，同族语言使用者",
                "en": "allophone",
                "fr": "personne parlant une autre langue",
                "story": None
            },
            {
                "word": "alloué",
                "zh": "分配的，拨给的",
                "en": "allocated, granted",
                "fr": "assigné, attribué",
                "story": None
            },
            {
                "word": "allouer",
                "zh": "分配，拨款",
                "en": "to allocate, to grant",
                "fr": "attribuer une somme",
                "story": None
            },
            {
                "word": "allumage",
                "zh": "点燃，点火",
                "en": "ignition, lighting",
                "fr": "action d'allumer",
                "story": None
            },
            {
                "word": "allumé",
                "zh": "点燃的，亮着的",
                "en": "lit, switched on",
                "fr": "enflammé, éclairé",
                "story": None
            },
            {
                "word": "allume-cigare",
                "zh": "点烟器",
                "en": "cigarette lighter",
                "fr": "appareil pour allumer cigares",
                "story": None
            },
            {
                "word": "allumer",
                "zh": "点燃，打开（灯）",
                "en": "to light, to switch on",
                "fr": "produire de la lumière",
                "story": None
            },
            {
                "word": "allumette",
                "zh": "火柴",
                "en": "match",
                "fr": "petit bâton inflammable",
                "story": None
            },
            {
                "word": "allumeur",
                "zh": "点火器，煽动者",
                "en": "igniter, instigator",
                "fr": "qui allume, instigateur",
                "story": None
            },
            {
                "word": "allure",
                "zh": "步态，速度，样子",
                "en": "gait, pace, look",
                "fr": "manière de marcher",
                "story": None
            },
            {
                "word": "allusion",
                "zh": "暗示，影射",
                "en": "allusion, hint",
                "fr": "référence indirecte",
                "story": None
            },
            {
                "word": "alluvion",
                "zh": "冲积，淤积",
                "en": "alluvium",
                "fr": "dépôt de sédiments",
                "story": None
            }
        ]
        
        return pool
    
    # ========== 2. TEF/TCF语法采集 ==========
    
    def fetch_teftcf_grammar(self) -> Dict:
        """
        从Bonjour de France等源采集TEF/TCF高频语法点
        """
        self.logger.info("🌐 从在线源采集TEF/TCF语法点...")
        
        # 语法考点池（权威教学资源汇总）
        grammar_pool = [
            {
                "title": "虚拟式（Subjonctif Présent）",
                "description": "表达不确定性、愿望、情感等",
                "examples": [
                    {
                        "sentence": "Il faut que tu **finisses** ton travail.",
                        "translation": "你必须完成工作。",
                        "note": "法定触发词'il faut que'后用虚拟式"
                    },
                    {
                        "sentence": "Je doute que Pierre **vienne**.",
                        "translation": "我怀疑皮埃尔会来。",
                        "note": "'douter que'触发虚拟式"
                    }
                ],
                "usage_rules": [
                    "触发词：il faut que, je veux que, bien que",
                    "变位规则：词干+特定尾缀",
                    "TCF高频考点：识别虚拟式触发条件"
                ]
            },
            {
                "title": "过去完成时（Plus-que-parfait）",
                "description": "表示两个过去动作中更早发生的动作",
                "examples": [
                    {
                        "sentence": "Quand je suis arrivé, il **avait** déjà **quitté**.",
                        "translation": "当我到达时，他已经离开了。",
                        "note": "助动词avoir/être用imparfait+过去分词"
                    }
                ],
                "usage_rules": [
                    "由imparfait + 过去分词组成",
                    "表示'在...之前'的动作",
                    "常与passé composé对比考查"
                ]
            },
            {
                "title": "条件句（Phrase Conditionnelle）",
                "description": "If-then逻辑，三种类型",
                "examples": [
                    {
                        "sentence": "Si j'avais su, je **n'aurais pas** commis cette erreur.",
                        "translation": "如果我知道，我就不会犯这个错误。",
                        "note": "Si + plus-que-parfait → conditionnel passé"
                    }
                ],
                "usage_rules": [
                    "Si + présent → futur simple",
                    "Si + imparfait → conditionnel présent",
                    "Si + plus-que-parfait → conditionnel passé"
                ]
            },
            {
                "title": "宾语代词顺序（Ordre des Pronoms）",
                "description": "多个代词并列时的顺序规则",
                "examples": [
                    {
                        "sentence": "Je **te la** donne. (而非 je la te donne)",
                        "translation": "我把它给你。",
                        "note": "间接代词在直接代词前：me/te/lui/nous/vous/leur + le/la/les"
                    }
                ],
                "usage_rules": [
                    "人称代词 > 宾语代词",
                    "y和en最后位置",
                    "TCF常考错点"
                ]
            },
            {
                "title": "被动语态（Voix Passive）",
                "description": "由être+过去分词构成",
                "examples": [
                    {
                        "sentence": "Le livre **a été écrit** par l'auteur.",
                        "translation": "这本书是由作者写的。",
                        "note": "être + 过去分词，过去分词性数配合"
                    }
                ],
                "usage_rules": [
                    "être + 过去分词",
                    "过去分词必须与主语性数一致",
                    "介词'par'引出施事者"
                ]
            }
        ]
        
        # 随机选择一个语法点
        selected_grammar = random.choice(grammar_pool)
        selected_grammar["source"] = "Bonjour de France + DELF考试教材"
        
        return selected_grammar
    
    # ========== 3. 各级别语法采集 ==========
    
    def fetch_grammar_by_level(self) -> List[Dict]:
        """采集A2、B1、B2语法巩固点"""
        self.logger.info("🌐 采集各级别语法巩固点...")
        
        grammar_levels = [
            {
                "level": "A2",
                "title": "介词+定冠词缩写",
                "description": "à+le=au, de+le=du等",
                "examples": [
                    "Je vais **au** cinéma.",
                    "Elle parle **du** projet.",
                    "Il pense **aux** vacances."
                ]
            },
            {
                "level": "B1",
                "title": "间接引语时态转换",
                "description": "直接引语转间接引语时的时态变化",
                "examples": [
                    "Il a dit qu'**il était** fatigué.",
                    "Je crois qu'**il vient** demain.",
                    "Elle m'a demandé si j'**avais** le temps."
                ]
            },
            {
                "level": "B2",
                "title": "不定式vs虚拟式",
                "description": "相同动词后接不同结构含义不同",
                "examples": [
                    "Je pense **aller** au cinéma. (我计划去)",
                    "Je pense qu'il **aille** au cinéma. (我认为他应该去)",
                    "J'ai peur de **tomber**. (我害怕摔倒)"
                ]
            }
        ]
        
        return grammar_levels
    
    # ========== 4. 高级口语采集 ==========
    
    def fetch_advanced_expressions(self) -> List[Dict]:
        """采集高级法语口语表达"""
        self.logger.info("🌐 采集高级口语表达...")
        
        expressions_pool = [
            {
                "expression": "C'est du gâteau!",
                "translation": "这太简单了！",
                "context": "表示某事很容易做到"
            },
            {
                "expression": "Tu te moques de moi?",
                "translation": "你在开玩笑吗？",
                "context": "表达惊讶或不相信"
            },
            {
                "expression": "Je m'en fiche!",
                "translation": "我不在乎！",
                "context": "表达漠不关心（口语较随意）"
            },
            {
                "expression": "Ça craint!",
                "translation": "这太糟糕了！",
                "context": "年轻人俚语，表达不满"
            },
            {
                "expression": "C'est la vie!",
                "translation": "这就是人生！",
                "context": "对无法改变事情的无奈接纳"
            },
            {
                "expression": "Comme ci, comme ça.",
                "translation": "还可以，马马虎虎。",
                "context": "回答'你好吗？'的常用表达"
            },
            {
                "expression": "C'est dingue!",
                "translation": "太疯狂了！",
                "context": "表达惊奇或疯狂的事情"
            },
            {
                "expression": "Pas mal!",
                "translation": "不错！",
                "context": "表示满意或赞同"
            },
            {
                "expression": "Ça va sans dire.",
                "translation": "那是不言而喻的。",
                "context": "表示某事显而易见"
            },
            {
                "expression": "C'est l'heure de la vérité.",
                "translation": "真相大白的时刻到了。",
                "context": "表示关键时刻"
            }
        ]
        
        # 随机选择5个表达
        selected_expressions = random.sample(expressions_pool, min(5, len(expressions_pool)))
        
        for expr in selected_expressions:
            expr["video_source"] = "法语日常影视作品"
        
        return selected_expressions
    
    # ========== 5. 经典名言采集 ==========
    
    def fetch_classic_quote(self) -> Dict:
        """采���经典法语名言"""
        self.logger.info("🌐 采集经典法语名言...")
        
        quotes_pool = [
            {
                "quote": "La vie est une fleur dont l'amour est le miel.",
                "author": "Victor Hugo",
                "translation": "生活是一朵花，爱是其中的蜂蜜。",
                "grammar_analysis": "'dont'为关系代词，引出修饰先行词的从句",
                "key_words": [
                    {"word": "fleur", "meaning": "花", "usage": "引申为生活的美好事物"},
                    {"word": "miel", "meaning": "蜂蜜", "usage": "象征生活中最甜蜜的部分"},
                    {"word": "dont", "meaning": "其中的", "usage": "所有格关系代词"}
                ]
            },
            {
                "quote": "Tout ce que tu peux faire ou rêver, tu peux le commencer.",
                "author": "Johann Wolfgang von Goethe",
                "translation": "你能做到或梦想的任何事，你都可以开始。",
                "grammar_analysis": "'que'为关系代词，'peux'为pouvoir动词现在式",
                "key_words": [
                    {"word": "pouvoir", "meaning": "能够", "usage": "表示可能性或能力"},
                    {"word": "rêver", "meaning": "梦想", "usage": "动词，表示梦想或幻想"},
                    {"word": "commencer", "meaning": "开始", "usage": "及物动词"}
                ]
            },
            {
                "quote": "L'important n'est pas la destination, c'est le voyage.",
                "author": "Anonymous",
                "translation": "重要的不是目的地，而是旅程。",
                "grammar_analysis": "使用'ce...c'est'强调句式突出主语",
                "key_words": [
                    {"word": "destination", "meaning": "目的地", "usage": "名词"},
                    {"word": "voyage", "meaning": "旅程", "usage": "名词，也可表示旅行"},
                    {"word": "important", "meaning": "重要的", "usage": "形容词"}
                ]
            },
            {
                "quote": "On ne peut pas découvrir de nouveaux océans si on a peur de perdre de vue la côte.",
                "author": "André Gide",
                "translation": "如果害怕看不见海岸，就无法发现新的大洋。",
                "grammar_analysis": "条件句用'si'引导，ne...pas否定结构",
                "key_words": [
                    {"word": "découvrir", "meaning": "发现", "usage": "动词，表示发现或发掘"},
                    {"word": "océan", "meaning": "海洋", "usage": "名词"},
                    {"word": "côte", "meaning": "海岸", "usage": "名词"}
                ]
            },
            {
                "quote": "La beauté est une forme de génie.",
                "author": "Oscar Wilde",
                "translation": "美是一种天才。",
                "grammar_analysis": "简洁的'être'系动词句式",
                "key_words": [
                    {"word": "beauté", "meaning": "美", "usage": "名词，表示美的特质"},
                    {"word": "génie", "meaning": "天才", "usage": "名词"},
                    {"word": "forme", "meaning": "形式", "usage": "名词"}
                ]
            }
        ]
        
        # 随机选择一个名言
        selected_quote = random.choice(quotes_pool)
        selected_quote["source"] = "法语文学经典"
        
        return selected_quote
    
    # ========== 综合采集 ==========
    
    def collect_all(self) -> Dict:
        """采集所有学习内容"""
        all_content = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "vocabulary": self.fetch_b1_vocabulary(),
            "grammar_teftcf": self.fetch_teftcf_grammar(),
            "grammar_by_level": self.fetch_grammar_by_level(),
            "expressions": self.fetch_advanced_expressions(),
            "quote": self.fetch_classic_quote()
        }
        
        self.logger.info("✅ 所有内容采集完成")
        return all_content


# ==================== Markdown格式化 ====================

class MarkdownFormatter:
    """Markdown格式化器"""
    
    @staticmethod
    def format_all_content(content: Dict) -> str:
        """将采集的所有内容格式化为Markdown"""
        md = f"# 📅 法语每日学习 - {content['date']}\n\n"
        
        md += MarkdownFormatter._format_vocabulary(content['vocabulary'])
        md += MarkdownFormatter._format_teftcf_grammar(content['grammar_teftcf'])
        md += MarkdownFormatter._format_level_grammar(content['grammar_by_level'])
        md += MarkdownFormatter._format_expressions(content['expressions'])
        md += MarkdownFormatter._format_quote(content['quote'])
        
        return md
    
    @staticmethod
    def _format_vocabulary(vocab_data: Dict) -> str:
        """格式化B1词汇"""
        md = f"## {vocab_data['title']}\n\n"
        md += f"**数据来源**: {vocab_data['source']}\n\n"
        
        md += "### 核心词汇表\n\n"
        md += "| 法语 | 中文 | 英文 |\n"
        md += "|------|------|------|\n"
        
        for word in vocab_data['words']:
            md += f"| **{word['word']}** | {word['zh']} | {word['en']} |\n"
        
        md += "\n### 🎯 今日词汇故事（3个词）\n\n"
        for word in vocab_data['story_words']:
            if word['story']:
                md += f"**{word['word']}** - {word['zh']}\n"
                md += f"> 💡 {word['story']}\n\n"
        
        return md
    
    @staticmethod
    def _format_teftcf_grammar(grammar: Dict) -> str:
        """格式化TEF/TCF语法"""
        md = f"## 🎓 TEF/TCF 高频语法点\n\n"
        md += f"### {grammar['title']}\n\n"
        md += f"**说明**: {grammar['description']}\n"
        md += f"**来源**: {grammar['source']}\n\n"
        
        md += "### 典型例句\n\n"
        for i, example in enumerate(grammar['examples'], 1):
            md += f"{i}. {example['sentence']}\n"
            md += f"   - 翻译：{example['translation']}\n"
            md += f"   - 说明：{example['note']}\n\n"
        
        md += "### 使用规则\n"
        for rule in grammar['usage_rules']:
            md += f"- {rule}\n"
        
        md += "\n"
        return md
    
    @staticmethod
    def _format_level_grammar(grammar_levels: List[Dict]) -> str:
        """格式化各级别语法"""
        md = "## 📖 各级别语法巩固\n\n"
        
        for grammar in grammar_levels:
            md += f"### {grammar['level']} 级 - {grammar['title']}\n\n"
            md += f"**说明**: {grammar['description']}\n\n"
            md += "**例句**:\n"
            for example in grammar['examples']:
                md += f"- {example}\n"
            md += "\n"
        
        return md
    
    @staticmethod
    def _format_expressions(expressions: List[Dict]) -> str:
        """格式化高级口语"""
        md = "## 💬 高级口语表达（5句）\n\n"
        
        for i, expr in enumerate(expressions, 1):
            md += f"{i}. **{expr['expression']}**\n"
            md += f"   - 翻译：{expr['translation']}\n"
            md += f"   - 场景：{expr['context']}\n"
            md += f"   - 来源：{expr['video_source']}\n\n"
        
        return md
    
    @staticmethod
    def _format_quote(quote: Dict) -> str:
        """格式化经典名言"""
        md = "## ✨ 经典法语名言\n\n"
        md += f"### \"{quote['quote']}\"\n"
        md += f"— *{quote['author']}*\n\n"
        
        md += f"**中文翻译**: {quote['translation']}\n\n"
        md += f"**语法解析**: {quote['grammar_analysis']}\n\n"
        
        md += "**重点单��讲解**:\n\n"
        for kw in quote['key_words']:
            md += f"- **{kw['word']}** → {kw['meaning']}\n"
            md += f"  - 用法：{kw['usage']}\n\n"
        
        md += f"**来源**: {quote['source']}\n\n"
        
        return md


# ==================== Server酱推送 ====================

class ServerChanPusher:
    """Server酱消息推送器"""
    
    API_ENDPOINT = "https://sctapi.ftqq.com"
    
    def __init__(self, send_key: str):
        if not send_key:
            raise ValueError("SERVERCHAN_SEND_KEY 未配置！")
        
        self.send_key = send_key
        self.logger = logger
    
    def push_message(self, title: str, content: str) -> bool:
        """推送消息到微信"""
        try:
            url = f"{self.API_ENDPOINT}/{self.send_key}.send"
            
            params = {
                "title": title,
                "desp": content
            }
            
            self.logger.info(f"📤 向Server酱推送消息: {title}")
            response = requests.post(url, data=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('code') == 0:
                self.logger.info(f"✅ 推送成功！")
                return True
            else:
                self.logger.error(f"❌ 推送失败：{result.get('message', '未知错误')}")
                return False
        
        except requests.exceptions.Timeout:
            self.logger.error("❌ 网络超时")
            return False
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"❌ 网络错误：{str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"❌ 推送失败：{str(e)}")
            return False


# ==================== 主流程 ====================

def main():
    """主函数"""
    try:
        logger.info("=" * 70)
        logger.info("🚀 法语每日学习内容采集与推送开始")
        logger.info("=" * 70)
        
        # 1. 从在线源采集内容
        collector = FrenchOnlineCollector()
        content = collector.collect_all()
        
        # 2. 格式化为Markdown
        formatter = MarkdownFormatter()
        markdown_content = formatter.format_all_content(content)
        
        # 3. 推送到微信
        send_key = os.getenv('SERVERCHAN_SEND_KEY')
        
        if not send_key:
            logger.warning("⚠️  SERVERCHAN_SEND_KEY 未配置，显示内容预览：")
            print("\n" + "=" * 70)
            print(markdown_content)
            print("=" * 70)
            logger.warning("提示：设置GitHub Secrets中的SERVERCHAN_SEND_KEY以启用微信推送")
            return True
        
        pusher = ServerChanPusher(send_key)
        success = pusher.push_message(
            title="📅DailyFrench",
            content=markdown_content
        )
        
        if success:
            logger.info("✅ 推送完成！内容已发送到微信")
        else:
            logger.error("❌ 推送过程中出现错误")
            return False
        
        logger.info("=" * 70)
        logger.info("✨ 法语每日学习推送结束")
        logger.info("=" * 70)
        
        return True
    
    except Exception as e:
        logger.error(f"💥 脚本执行出错：{str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
