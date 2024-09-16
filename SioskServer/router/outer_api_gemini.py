import google.generativeai as genai

class CallingGemini:
    def __init__(self) -> None:
        GOOGLE_API_KEY='AIzaSyAMXx8dgR60VY7rO2BcSN-RymAomxfksco'
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-pro')

    def creating_response(self, ques):
        try:
            tunned_ques = f"답변 조건: 1. 너가 AI인걸 드러내고 대답해서는 안돼 2. 모든 질문은 1문장 이내로 해줘 | 질문: '{ques}'"
            response = self.model.generate_content(tunned_ques)
            candidate = response._result.candidates[0]
            part = candidate.content.parts[0]
            text = part.text
            return text
        except IndexError:
            return "예쁘고 고운말을 써주세요"