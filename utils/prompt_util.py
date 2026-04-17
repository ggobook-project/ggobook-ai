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
