import re
from app.utils.logger import get_logger

logger = get_logger(__name__)

PRONOUNS = {"he", "she", "it", "they", "him", "her", "them", "his", "their"}


def has_pronoun(text: str) -> bool:
    tokens = re.findall(r"\b\w+\b", text.lower())
    return any(token in PRONOUNS for token in tokens)


def extract_entity_from_question(question: str) -> str | None:
    """
    提取当前问题里的明确主体。
    求职项目版本：只做轻量实体识别，不追求完美 NER。
    """


    # 1. 处理常见小写名字：只作为 demo 兜底
    known_subjects = {"chris": "Chris"}

    tokens = re.findall(r"\b\w+\b", question.lower())
    for token in tokens:
        if token in known_subjects:
            return known_subjects[token]
    
    # 2. 先找大写实体，比如 LangChain
    words = re.findall(r"\b[A-Z][a-z]+\b", question)
    if words:
        return words[0]



    return None


def rewrite_query(question: str, latest_subject: str | None):
    # print("DEBUG question =", question)
    # print("DEBUG latest_subject before =", latest_subject)

    logger.info(f"question = {question}")
    logger.info(f"atest_subject before = {latest_subject}")

    lower_q = question.lower()

    # 1️⃣ 如果没有代词 → 直接更新 subject（如果能提取）
    if not has_pronoun(question):
        new_subject = extract_entity_from_question(question)

        if new_subject:
            latest_subject = new_subject  # ✅ 只在这里更新

        logger.info(f"latest_subject after = {latest_subject}")
        # print("DEBUG no pronoun → return original")
        return question, latest_subject

    # 2️⃣ 有代词，但没有 subject → 无法 rewrite
    if not latest_subject:
        
        logger.info(f"latest_subject after = {latest_subject}")
        # print("DEBUG no subject → return original")
        return question, latest_subject

    # 3️⃣ 做 pronoun 替换
    rewritten = question

    rewritten = re.sub(r"\bhe\b", latest_subject, rewritten, flags=re.IGNORECASE)
    rewritten = re.sub(r"\bshe\b", latest_subject, rewritten, flags=re.IGNORECASE)
    rewritten = re.sub(r"\bit\b", latest_subject, rewritten, flags=re.IGNORECASE)
    rewritten = re.sub(r"\bthey\b", latest_subject, rewritten, flags=re.IGNORECASE)

    rewritten = re.sub(r"\bhis\b", f"{latest_subject}'s", rewritten, flags=re.IGNORECASE)
    rewritten = re.sub(r"\btheir\b", f"{latest_subject}'s", rewritten, flags=re.IGNORECASE)

    logger.info(f"rewritten = {rewritten}")
    logger.info(f"latest_subject after = {latest_subject}")

    # print("DEBUG rewritten =", rewritten)
    # print("DEBUG latest_subject after =", latest_subject)

    return rewritten, latest_subject