class PromptUtil:
    @staticmethod
    def get_summary_prompt(content: str) -> str:
        return f"다음 웹툰/웹소설의 줄거리를 스포일러를 방지하면서 흥미진진하게 3줄로 요약해줘:\n\n{content}"

    @staticmethod
    def get_moderate_prompt(content: str) -> str:
        return f"다음 텍스트에 부적절한 내용(비속어, 선정성, 폭력성)이 포함되어 있는지 판단하고 이유를 알려줘:\n\n{content}"

    @staticmethod
    def get_tts_recommend_prompt(content: str) -> str:
        return f"이 원고의 분위기에 가장 잘 어울리는 성우 목소리와 배경음악 톤을 추천해줘:\n\n{content}"

    # ==========================================
    # 🌟 [추가] 릴레이 소설 전용 프롬프트
    # ==========================================
    @staticmethod
    def get_relay_moderate_prompt(text: str) -> str:
        return f"""
        당신은 웹소설 검수 AI입니다.
        다음 릴레이 소설 원고를 검수해 주십시오. 
        심한 욕설, 폭력성, 선정적인 내용이 없다면 오직 'PASS' 라고만 출력하고,
        부적절한 내용이 있다면 'REJECT: [구체적인 사유]' 형식으로 출력하십시오.
        
        [원문]
        {text}
        """

    @staticmethod
    def get_relay_summary_prompt(text: str) -> str:
        return f"""
        당신은 웹소설 플랫폼의 콘텐츠 검수 AI입니다.
        아래 주어진 릴레이 소설의 원문에서 욕설, 폭력성, 선정성 등 부적절한 내용을 완전히 제거하십시오.
        그리고 다음 회차 작성자가 앞뒤 문맥을 파악할 수 있도록, 핵심 사건만 2~3줄로 건전하게 요약해주십시오.
        반드시 요약된 결과 텍스트만 출력하십시오.
        
        [원문]
        {text}
        """
