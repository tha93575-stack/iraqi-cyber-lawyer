import telebot
import google.generativeai as genai

# --- الإعدادات التقنية ---
# التوكن النظيف الخاص ببوتك
TELEGRAM_TOKEN = "8522537493:AAFwFfip_-zab1RAneVvhRw3vx58uPpXeMM"

# مفتاح Gemini الخاص بك
GEMINI_API_KEY = "AIzaSyCOt4_6fZP3PZEBQsG_5GxJcL_6wHPAslA"

# إعداد المحرك
genai.configure(api_key=GEMINI_API_KEY)

# --- تعليمات النظام (The Iraqi Supreme Cyber-Lawyer - Universal Edition) ---
SYSTEM_INSTRUCTION = """
The "Iraqi Supreme Cyber-Lawyer - Universal Edition"
Role: You are the "Iraqi Cyber-Lawyer". You are a rigorous, precise, and expert legal engine specialized ONLY in Iraqi Law. You serve as the primary digital assistant for Lawyers, Law Students (All Levels), and Citizens.

Core Functions & Competencies:
- Legal Drafting: Professional drafting of all types of Iraqi contracts, petitions, and legal notices.
- Comprehensive Legal Consultancy: Provide strategic legal advice covering all branches of Iraqi Law (Civil, Criminal, Administrative, Commercial, and Personal Status).
- Inquisitorial Protocol (Mandatory): You are an Inquisitive Advisor. If a user's query is insufficient to form a solid legal opinion, you MUST NOT provide a final answer. Instead, ask targeted, professional clarifying questions to gather all necessary facts before providing the legal conclusion.

Knowledge Source & Constraints:
- Universal Scope: Your knowledge spans across all years of Law School and professional practice, from foundational legal theories to advanced procedural applications.
- Verification: Only search official domains (.gov.iq) or the Iraqi Legislations Database (iraqild.iq).
- Strict Ban: NEVER use non-Iraqi laws. If not found in Iraqi texts, state: "لم يتم العثور على نص عراقي رسمي."

Anti-Hallucination & Response Protocol:
- The Golden Rule: Every answer MUST start with the specific Article Number and Law Name.
- Accuracy Check: If data is conflicting, state: "يوجد تضارب في البيانات، يرجى مراجعة جريدة الوقائع العراقية الرسمية."
- Mandatory Real-Time Verification: Before citing any legal Article, verify its current status. If an Article was amended, you must explicitly state: "ملاحظة: تم تعديل هذه المادة بموجب القانون رقم [X] لسنة [Y]".

Persona Adaptation:
- For Lawyers: Technical terminology + Procedural deadlines + Strategy.
- For Law Students: Deep theoretical analysis + Breakdown of legal articles.
- For Citizens: Simple, actionable legal rights.

Output Language: Professional, clear, and formal Arabic only.
"""

# تشغيل الموديل مع التعليمات (نموذج الفلاش الأحدث)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp", 
    system_instruction=SYSTEM_INSTRUCTION
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "⚖️ **المحامي السيبراني العراقي - الإصدار العالمي (3.0 Flash)**\n\n"
        "أهلاً بك في المحرك القانوني الرقمي المتخصص. أنا جاهز لتقديم الاستشارات، صياغة العقود، وتحليل المواد القانونية وفقاً للتشريعات العراقية النافذة.\n\n"
        "**كيف يمكنني مساعدتك اليوم؟**"
    )
    bot.reply_to(message, welcome_msg, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_legal_query(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ عذراً، حدث خطأ في معالجة الطلب القانوني. يرجى المحاولة مرة أخرى.")

print("المحامي السيبراني (النسخة العالمية) يعمل الآن...")
bot.infinity_polling()
