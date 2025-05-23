import random
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.lang import Builder
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import LabelBase
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from kivy.metrics import dp
import random
# إصلاح مشكلة ظهور الخيارات الفارغة في السؤال الأخير بعد استخدام "تغيير السؤال" أو "50:50"
from kivy.utils import platform

def get_random_option_color():
    # Return a random color for the correct answer rectangle (e.g., green, blue, purple, etc.)
    colors = [
        [0, 0.7, 0, 1],      # Green
        [0, 0.5, 1, 1],      # Blue
        [0.6, 0, 0.8, 1],    # Purple
        [1, 0.5, 0, 1],      # Orange
        [0.8, 0.2, 0.2, 1],  # Red
        [0.2, 0.8, 0.8, 1],  # Cyan
        [0.8, 0.8, 0, 1],    # Yellow
    ]
    return random.choice(colors)

# تعريف دالة لمعالجة النصوص العربية
def arabic_text(text):
    try:
        if any('\u0600' <= char <= '\u06FF' for char in text):
            reshaped_text = reshape(text)
            return get_display(reshaped_text)
        return text
    except:
        return text

# تسجيل خط عربي
font_path = 'fonts/arial.ttf'  # يمكنك استبداله بخطك المفضل
if not os.path.exists(font_path):
    font_path = 'mofid.ttf'
LabelBase.register(name='Arabic', fn_regular=font_path)

# تعريف واجهة المستخدم
Builder.load_string('''
#:import arabic_text __main__.arabic_text
#:import dp kivy.metrics.dp

<MainScreen>:
    orientation: 'vertical'
    spacing: dp(15)
    padding: dp(15)
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0, 0.3, 0.6, 1
        Rectangle:
            pos: self.pos[0], self.pos[1] + self.height*0.8
            size: self.width, self.height*0.2
    
    BoxLayout:
        size_hint: 1, 0.15
        padding: dp(10)
        canvas.before:
            Color:
                rgba: 0, 0.2, 0.4, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: root.title_text
            font_name: 'Arabic'
            font_size: dp(28)
            bold: True
            color: 1, 0.8, 0, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.width, None
    
    BoxLayout:
        size_hint: 1, 0.5
        padding: dp(20)
        canvas.before:
            Color:
                rgba: 0, 0.15, 0.3, 0.9
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        Label:
            id: question_label
            text: root.question_text
            font_name: 'Arabic'
            font_size: dp(24)
            color: 1, 1, 1, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.width, None
            markup: True
    
    GridLayout:
        cols: 2
        size_hint: 1, 0.6
        spacing: dp(15)
        padding: dp(15)
        
        Button:
            id: option1
            text: ''
            on_press: root.check_answer(1)
            font_name: 'Arabic'
            font_size: dp(20)
            background_normal: ''
            background_color: root.option1_color if root.option1_color else (0, 0.3, 0.6, 1)
            color: 1, 1, 1, 1
            bold: True
        
        Button:
            id: option2
            text: ''
            on_press: root.check_answer(2)
            font_name: 'Arabic'
            font_size: dp(20)
            background_normal: ''
            background_color: root.option2_color if root.option2_color else (0, 0.3, 0.6, 1)
            color: 1, 1, 1, 1
            bold: True
        
        Button:
            id: option3
            text: ''
            on_press: root.check_answer(3)
            font_name: 'Arabic'
            font_size: dp(20)
            background_normal: ''
            background_color: root.option3_color if root.option3_color else (0, 0.3, 0.6, 1)
            color: 1, 1, 1, 1
            bold: True
        
        Button:
            id: option4
            text: ''
            on_press: root.check_answer(4)
            font_name: 'Arabic'
            font_size: dp(20)
            background_normal: ''
            background_color: root.option4_color if root.option4_color else (0, 0.3, 0.6, 1)
            color: 1, 1, 1, 1
            bold: True
    
    BoxLayout:
        size_hint: 1, 0.15
        spacing: dp(15)
        padding: dp(10)
        
        Button:
            id: contact_me_btn
            text: arabic_text('التواصل مع الأستاذ')
            on_press: root.contact_me()
            font_name: 'Arabic'
            font_size: dp(18)
            background_normal: ''
            background_color: (0.8, 0.5, 0, 1) if root.audience_available else (0.5, 0.5, 0.5, 1)
            color: 1, 1, 1, 1
            bold: True
            disabled: not root.audience_available
        
        Button:
            id: fifty_fifty_btn
            text: '50:50'
            on_press: root.fifty_fifty()
            font_name: 'Arabic'
            font_size: dp(18)
            background_normal: ''
            background_color: (0.8, 0.5, 0, 1) if root.fifty_available else (0.5, 0.5, 0.5, 1)
            color: 1, 1, 1, 1
            bold: True
            disabled: not root.fifty_available
        
        Button:
            id: change_question_btn
            text: arabic_text('تغيير السؤال')
            on_press: root.change_question()
            font_name: 'Arabic'
            font_size: dp(18)
            background_normal: ''
            background_color: (0.8, 0.5, 0, 1) if root.change_available else (0.5, 0.5, 0.5, 1)
            color: 1, 1, 1, 1
            bold: True
            disabled: not root.change_available
    
    BoxLayout:
        size_hint: 1, 0.1
        padding: dp(10)
        canvas.before:
            Color:
                rgba: 0, 0.2, 0.4, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            id: prize_label
            text: root.prize_text
            font_name: 'Arabic'
            font_size: dp(22)
            color: 1, 0.8, 0, 1
            halign: 'center'
            bold: True

<AudienceHelpPopup>:
    size_hint: 0.8, 0.7
    background_color: 0, 0.1, 0.3, 0.9
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0, 0.2, 0.4, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        
        Label:
            text: arabic_text('التواصل مع الأستاذ')
            font_name: 'Arabic'
            font_size: dp(28)
            color: 1, 0.8, 0, 1
            halign: 'center'
            size_hint_y: 0.15
        
        Image:
            id: audience_image
            source: 'assets/contact_me.png'
            size_hint: 1, 0.7
        
        Button:
            text: arabic_text('إغلاق')
            on_press: root.dismiss()
            size_hint: 1, 0.15
            font_name: 'Arabic'
            font_size: dp(20)
            background_normal: ''
            background_color: 0.8, 0.5, 0, 1
            color: 1, 1, 1, 1
            bold: True

<GameOverPopup>:
    size_hint: 0.7, 0.5
    background_color: 0, 0.1, 0.3, 0.9
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0, 0.2, 0.4, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        
        Label:
            text: arabic_text('انتهت اللعبة!')
            font_name: 'Arabic'
            font_size: dp(28)
            color: 1, 0.8, 0, 1
            halign: 'center'
            size_hint_y: 0.3
        
        Label:
            id: result_label
            text: ''
            font_name: 'Arabic'
            font_size: dp(24)
            color: 1, 1, 1, 1
            halign: 'center'
            size_hint_y: 0.4
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.3
            spacing: dp(10)
            
            Button:
                text: arabic_text('إعادة اللعبة')
                on_press: root.restart_game()
                font_name: 'Arabic'
                font_size: dp(20)
                background_normal: ''
                background_color: 0.8, 0.5, 0, 1
                color: 1, 1, 1, 1
                bold: True
            
            Button:
                text: arabic_text('إنهاء اللعبة')
                on_press: root.dismiss()
                font_name: 'Arabic'
                font_size: dp(20)
                background_normal: ''
                background_color: 0.7, 0, 0, 1
                color: 1, 1, 1, 1
                bold: True

<WinPopup>:
    size_hint: 0.8, 0.6
    background_color: 0, 0.1, 0.3, 0.9
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0, 0.2, 0.4, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        
        Label:
            text: arabic_text('مبرووووك!')
            font_name: 'Arabic'
            font_size: dp(32)
            color: 1, 0.8, 0, 1
            halign: 'center'
            size_hint_y: 0.2
        
        Image:
            source: 'assets/win.png'
            size_hint: 1, 0.5
        
        Label:
            id: result_label
            text: arabic_text('لقد فزت بمليون ريال!')
            font_name: 'Arabic'
            font_size: dp(28)
            color: 1, 1, 1, 1
            halign: 'center'
            size_hint_y: 0.2
        
        Button:
            text: arabic_text('إغلاق')
            on_press: root.dismiss()
            size_hint: 1, 0.15
            font_name: 'Arabic'
            font_size: dp(20)
            background_normal: ''
            background_color: 0.8, 0.5, 0, 1
            color: 1, 1, 1, 1
            bold: True
''')

# تعريف أسئلة اللعبة
    
QUESTIONS = [
    
    {
        'question': 'ما معنى كلمة "un bénévole"؟',
        'options': ['فقير', 'معاق', 'يتيم', 'متطوع'],
        'answer': 4  # الإجابة الصحيحة: 'متطوع' (الخيار الرابع)
    },
    {
        'question': 'ما ترجمة "une nourriture"؟',
        'options': ['غذاء', 'شراب', 'دواء', 'ملابس'],
        'answer': 1  # الإجابة الصحيحة: 'غذاء'
    },
    {
        'question': 'ما معنى "le réconfort"؟',
        'options': ['راحة', 'حزن', 'غضب', 'توتر'],
        'answer': 1  # الإجابة الصحيحة: 'راحة'
    },
    {
        'question': '"les fonds" تعني:',
        'options': ['كتب', 'أموال', 'سيارات', 'منازل'],
        'answer': 2  # الإجابة الصحيحة: 'أموال'
    },
    {
        'question': 'ما ترجمة "un handicapé"؟',
        'options': ['معاق', 'طبيب', 'مهندس', 'طالب'],
        'answer': 1  # الإجابة الصحيحة: 'معاق'
    },
    {
        'question': '"un orphelin" تعني:',
        'options': ['يتيم', 'غني', 'قوي', 'سعيد'],
        'answer': 1  # الإجابة الصحيحة: 'يتيم'
    },
    {
        'question': 'ما معنى "une association"؟',
        'options': ['جمعية', 'مدرسة', 'مستشفى', 'فندق'],
        'answer': 1  # الإجابة الصحيحة: 'جمعية'
    },
    {
        'question': '"un donneur" تعني:',
        'options': ['لص', 'محتاج', 'متبرع', 'جندي'],
        'answer': 3  # الإجابة الصحيحة: 'متبرع'
    },
    {
        'question': 'ما ترجمة "une initiative"؟',
        'options': ['مبادرة', 'مشكلة', 'أزمة', 'فرصة'],
        'answer': 1  # الإجابة الصحيحة: 'مبادرة'
    },
    {
        'question': '"une équipe" تعني:',
        'options': ['فريق', 'فرد', 'عائلة', 'مدينة'],
        'answer': 1  # الإجابة الصحيحة: 'فريق'
    },
    {
        'question': 'ما معنى "l’engagement"؟',
        'options': ['التزام', 'حرية', 'راحة', 'فرح'],
        'answer': 1  # الإجابة الصحيحة: 'التزام'
    },
    {
        'question': '"un témoignage" تعني:',
        'options': ['سر', 'كذبة', 'شهادة', 'لغز'],
        'answer': 3  # الإجابة الصحيحة: 'شهادة'
    },
    {
        'question': 'ما ترجمة "le bonheur"؟',
        'options': ['قلق', 'حزن', 'غضب', 'سعادة'],
        'answer': 4  # الإجابة الصحيحة: 'سعادة'
    },
    {
        'question': '"améliorer" تعني:',
        'options': ['تكرار', 'تدمير', 'إهمال', 'تحسين'],
        'answer': 1  # الإجابة الصحيحة: 'تحسين'
    },
    {
        'question': 'ما معنى "collecter"؟',
        'options': ['جمع', 'بيع', 'شراء', 'فقدان'],
        'answer': 1  # الإجابة الصحيحة: 'جمع'
    },
    {
        'question': '"distribuer" تعني:',
        'options': ['توزيع', 'سرقة', 'إخفاء', 'كسر'],
        'answer': 1  # الإجابة الصحيحة: 'توزيع'
    },
    {
        'question': 'ما ترجمة "scolariser"؟',
        'options': ['لعب', 'تعليم', 'عمل', 'سفر'],
        'answer': 2  # الإجابة الصحيحة: 'تعليم'
    },
    {
        'question': '"avoir faim" تعني:',
        'options': ['جوع', 'عطش', 'نوم', 'مرض'],
        'answer': 1  # الإجابة الصحيحة: 'جوع'
    },
    {
        'question': 'ما معنى "apprendre"؟',
        'options': ['تعلم', 'نسيان', 'كره', 'ركض'],
        'answer': 1  # الإجابة الصحيحة: 'تعلم'
    },
    {
        'question': '"lire" تعني:',
        'options': ['قراءة', 'كتابة', 'رسم', 'غناء'],
        'answer': 1  # الإجابة الصحيحة: 'قراءة'
    },
    {
        'question': 'ما ترجمة "humanitaire"؟',
        'options': ['إنساني', 'اقتصادي', 'سياسي', 'عسكري'],
        'answer': 1  # الإجابة الصحيحة: 'إنساني'
    },
    {
        'question': '"au profit de" تعني:',
        'options': ['ضد', 'لصالح', 'بدون', 'حول'],
        'answer': 2  # الإجابة الصحيحة: 'لصالح'
    },
    {
        'question': 'ما معنى "psychologique"؟',
        'options': ['نفسي', 'جسدي', 'روحي', 'عقلي'],
        'answer': 1  # الإجابة الصحيحة: 'نفسي'
    },
    {
        'question': '"sanitaire" تعني:',
        'options': ['ملوث', 'خطير', 'صحي', 'نظيف'],
        'answer': 3  # الإجابة الصحيحة: 'صحي'
    },
    {
        'question': 'ما ترجمة "fier"؟',
        'options': ['فخور', 'خجول', 'غاضب', 'حزين'],
        'answer': 1  # الإجابة الصحيحة: 'فخور'
    },
    {
        'question': '"heureux" تعني:',
        'options': ['سعيد', 'غاضب', 'متعب', 'جائع'],
        'answer': 1  # الإجابة الصحيحة: 'سعيد'
    },
    {
        'question': 'ما معنى "une catastrophe"؟',
        'options': ['هدية', 'فرصة', 'كارثة', 'مفاجأة'],
        'answer': 3  # الإجابة الصحيحة: 'كارثة'
    },
    {
        'question': '"un outil" تعني:',
        'options': ['أداة', 'لعبة', 'كتاب', 'سيارة'],
        'answer': 1  # الإجابة الصحيحة: 'أداة'
    },
    {
        'question': 'ما ترجمة "un téléphone portable"؟',
        'options': ['هاتف محمول', 'حاسوب', 'تلفزيون', 'راديو'],
        'answer': 1  # الإجابة الصحيحة: 'هاتف محمول'
    },
    {
        'question': '"un effet" تعني:',
        'options': ['أثر', 'صوت', 'ضوء', 'لون'],
        'answer': 1  # الإجابة الصحيحة: 'أثر'
    },
    {
        'question': 'ما مرادف "un volontaire"؟',
        'options': ['un bénévole', 'un pauvre', 'un enfant', 'un médecin'],
        'answer': 1  # الإجابة الصحيحة: 'un bénévole'
    },
    {
        'question': 'مرادف "un démuni" :',
        'options': ['un riche', 'un défavorisé', 'un étudiant', 'un artiste'],
        'answer': 2  # الإجابة الصحيحة: 'un défavorisé'
    },
    {
        'question': 'ما مرادف "une nourriture"؟',
        'options': ['un vêtement', 'un aliment', 'un livre', 'un arbre'],
        'answer': 2  # الإجابة الصحيحة: 'un aliment'
    },
    {
        'question': 'مرادف "le soutien" :',
        'options': ['l\'aide', 'le problème', 'le danger', 'le jeu'],
        'answer': 1  # الإجابة الصحيحة: 'l\'aide'
    },
    {
        'question': 'ما مرادف "améliorer"؟',
        'options': ['détruire', 'changer en mieux', 'ignorer', 'vendre'],
        'answer': 2  # الإجابة الصحيحة: 'changer en mieux'
    },
    {
        'question': 'مرادف "collecter" :',
        'options': ['rassembler', 'disperser', 'cacher', 'manger'],
        'answer': 1  # الإجابة الصحيحة: 'rassembler'
    },
    {
        'question': 'ما مرادف "un témoignage"؟',
        'options': ['une expérience personnelle', 'une erreur', 'une question', 'une réponse'],
        'answer': 1  # الإجابة الصحيحة: 'une expérience personnelle'
    },
    {
        'question': 'مرادف "le bonheur" :',
        'options': ['la tristesse', 'la joie', 'la colère', 'la peur'],
        'answer': 2  # الإجابة الصحيحة: 'la joie'
    },
    {
        'question': 'ما مرادف "humanitaire"؟',
        'options': ['lucratif', 'caritatif', 'dangereux', 'petit'],
        'answer': 2  # الإجابة الصحيحة: 'caritatif'
    },
    {
        'question': 'مرادف "fier" :',
        'options': ['triste', 'satisfait', 'fatigué', 'Malade'],
        'answer': 2  # الإجابة الصحيحة: 'satisfait'
    },

    {
        'question': 'depuis trois minutes, nous…… le petit-déjeuner.',
        'options': ['vient de prendre', 'venons de prendre', 'viens de prendre', 'viennent de prendre'],
        'answer': 2  # venons de prendre
    },
    {
        'question': 'Sumi et Pierre ……. de sortir il y a deux instants.',
        'options': ['viens', 'vient', 'venons', 'viennent'],
        'answer': 4  # viennent
    },
    {
        'question': 'la cloche ……… de sortir il y a cinq minutes.',
        'options': ['viens de sonner', 'vient de sonner', 'venons de sonner', 'viennent de sonner'],
        'answer': 2  # vient de sonner
    },
    {
        'question': 'vous venez de partir ……',
        'options': ['demain', 'hier', 'maintenant', 'il y a quelques instants'],
        'answer': 4  # il y a quelques instants
    },
    {
        'question': 'je n\'ai pas faim, je…… Depuis deux heures.',
        'options': ['viens de manger', 'vient de manger', 'venons de manger', 'venez de manger'],
        'answer': 1  # viens de manger
    },
    {
        'question': 'cette chanteuse ……… son nouvel album.',
        'options': ['viens d\'enregier', 'vient d\'enregier', 'venons d\'enregier', 'viennent d\'enregier'],
        'answer': 2  # vient d'enregier
    },
    {
        'question': 'le sécuriste……… un nouveau film adapté d\'un roman célèbre.',
        'options': ['venons d\'écrire', 'viens d\'écrire', 'venez d\'écrire', 'vient d\'écrire'],
        'answer': 4  # vient d'écrire
    },
    {
        'question': 'les enfants ……… ses devoirs.',
        'options': ['venez de faire', 'viens de faire', 'viennent de faire', 'vient de faire'],
        'answer': 3  # viennent de faire
    },
    {
        'question': 'on ……… la tour Eiffel depuis deux heures.',
        'options': ['viens de voir', 'venons de voir', 'vient de voir', 'viennent de voir'],
        'answer': 3  # vient de voir
    },
    {
        'question': 'Il…… beau et le ciel était bleu.',
        'options': ['faire', 'faisait', 'faisais', 'faisaient'],
        'answer': 2  # faisait
    },
    {
        'question': 'les enfants …… toujours des lettres aux amis.',
        'options': ['envoyais', 'envoyait', 'envoyaient', 'envoyions'],
        'answer': 3  # envoyaient
    },
    {
        'question': 'l\'année passée, je ……… des photos sur insurgram.',
        'options': ['publiais', 'publiait', 'publiaient', 'publiez'],
        'answer': 1  # publiais
    },
    {
        'question': 'vous ……… déjà de la musique ?',
        'options': ['écoutaient', 'écoutait', 'écoutions', 'écoutiez'],
        'answer': 4  # écoutiez
    },
    {
        'question': 'Quand elle avait quinze ans, ses parents ……… à Paris.',
        'options': ['habitaient', 'habitiez', 'habitions', 'habitait'],
        'answer': 1  # habitaient
    },
    {
        'question': 'elle …… l\'habitude de visiter sa grand-mère.',
        'options': ['avais', 'avait', 'avaient', 'aviez'],
        'answer': 2  # avait
    },
    {
        'question': 'tu …… toujours malade.',
        'options': ['étaient', 'était', 'étais', 'étions'],
        'answer': 3  # étais
    },
    {
        'question': 'ma mère ne …… pas quitter son lit.',
        'options': ['pouviez', 'pouvait', 'pouvions', 'pouvais'],
        'answer': 2  # pouvait
    },
    {
        'question': 'tu connais cet homme ? – oui, je …. Connais bien.',
        'options': ['le', 'la', 'l\'', 'les'],
        'answer': 1  # le
    },
    {
        'question': 'vous lavez les légumes? – oui, nous …. lavons soigneusement.',
        'options': ['le', 'la', 'l\'', 'les'],
        'answer': 4  # les
    },
    {
        'question': 'ils regardent la télévision? – oui, ils …. regardent chaque jour.',
        'options': ['le', 'la', 'l\'', 'les'],
        'answer': 2  # la
    },
    {
        'question': 'tu as téléphoné à tes parents? – oui, je …. ai téléphoné hier.',
        'options': ['lui', 'leur', 'en', 'les'],
        'answer': 2  # leur
    },
    {
        'question': 'le médecin conseille au malade de faire un régime ? – oui, il …. conseille de faire un régime.',
        'options': ['lui', 'leur', 'en', 'les'],
        'answer': 1  # lui
    },
    {
        'question': 'Je rencontre Samia, elle …… dit qu\'elle viendra demain.',
        'options': ['lui', 'leur', 'en', 'me'],
        'answer': 4  # me
    },
    {
        'question': 'la fille parle de son plat préféré ? – oui, elle …. parle.',
        'options': ['lui', 'leur', 'en', 'y'],
        'answer': 3  # en
    },
    {
        'question': 'tu penses à ton projet ? – oui, j\' …. pense tout le temps.',
        'options': ['lui', 'leur', 'en', 'y'],
        'answer': 4  # y
    },
    {
        'question': 'Salim prend du pain ? – oui, il …. prend.',
        'options': ['lui', 'leur', 'en', 'y'],
        'answer': 3  # en
    },
    {
        'question': 'tu vois Karine ? – oui, je… Vois tous les jours.',
        'options': ['le', 'la', 'l\'', 'les'],
        'answer': 2  # la
    },
    {
        'question': 'Sandra mange du gâteau ? – non, elle n\' …. mange jamais.',
        'options': ['le', 'la', 'en', 'y'],
        'answer': 3  # en
    },
    {
        'question': 'Sami s\'intéresse à sa santé ? – oui, il s\' …. intéresse beaucoup.',
        'options': ['le', 'la', 'en', 'y'],
        'answer': 4  # y
    },
    {
        'question': 'hier, ils sont ……… Au club.',
        'options': ['allé', 'allée', 'allés', 'allées'],
        'answer': 3  # allés
    },
    {
        'question': 'hier, elles sont ……… Au club.',
        'options': ['arrivé', 'arrivée', 'arrivés', 'arrivées'],
        'answer': 4  # arrivées
    },
    {
        'question': 'Sami et Rima sont ……… à la maison.',
        'options': ['resté', 'restée', 'restés', 'restées'],
        'answer': 3  # restés
    },
    {
        'question': 'Nada et Rima sont … au 2ème étages de l\'école.',
        'options': ['monté', 'montée', 'montés', 'montées'],
        'answer': 4  # montées
    },
    {
        'question': 'nous nous sommes ……… au cinéma.',
        'options': ['amusé', 'amusée', 'amusés', 'amusées'],
        'answer': 3  # amusés
    },
    {
        'question': 'vous ……… mangé les pommes.',
        'options': ['avez', 'êtes', 'avons', 'allez'],
        'answer': 1  # avez
    },
    {
        'question': 'j\' ……… joué du foot.',
        'options': ['ai', 'suis', 'as', 'es'],
        'answer': 1  # ai
    },
    {
        'question': 'les amis ……… sont promenés au parc.',
        'options': ['se', 'me', 'te', 'nous'],
        'answer': 1  # se
    },
    {
        'question': 'hier, elle a ……… un film au cinéma.',
        'options': ['vu', 'vue', 'vus', 'vues'],
        'answer': 1  # vu
    },
    {
        'question': '…… vous êtes entrés rapidement à la maison.',
        'options': ['maintenant', 'demain', 'aujourd\'hui', 'avant- hier'],
        'answer': 4  # avant-hier
    },
    {
        'question': 'déjà, on ……… chanté en français.',
        'options': ['est', 'sont', 'a', 'ont'],
        'answer': 3  # a
    },
    {
        'question': 'Ma fille est ……… en 2017.',
        'options': ['né', 'née', 'nés', 'nées'],
        'answer': 2  # née
    },
    {
        'question': 'les parents ……… la télé avec ses enfants, hier au soir.',
        'options': ['sont regardé', 'sont régadés', 'ont regardé', 'a regardé'],
        'answer': 3  # ont regardé
    },
    {
        'question': 'quelles solutions a-t-on ……… pour ce problème.',
        'options': ['proposé', 'proposée', 'proposés', 'proposées'],
        'answer': 4  # proposées
    },
    {
        'question': 'ces effort, le gouvernement les a ……… pour protéger l\'environnement.',
        'options': ['pris', 'prise', 'prises', 'prendre'],
        'answer': 1  # pris
    },
    {
        'question': 'le prof nous a ……… des idées pour préserver l\'eau.',
        'options': ['proposé', 'proposée', 'proposés', 'proposées'],
        'answer': 1  # proposé
    },
    {
        'question': 'mon père est ……… Pour m\'acheter des livres.',
        'options': ['parti', 'partie', 'partis', 'parties'],
        'answer': 1  # parti
    },
    {
        'question': 'notre ami nous a ……… à protéger l\'environnement.',
        'options': ['invité', 'invitée', 'invités', 'invitées'],
        'answer': 1  # invité
    },
    {
        'question': 'les habitants se sont ……… des solutions adaptées par les responsables.',
        'options': ['contenté', 'contenté', 'contentés', 'contentées'],
        'answer': 3  # contentés
    },
    {
        'question': 'beaucoup d\'espèces animales sont ……… à cause de la pollution.',
        'options': ['mort', 'morte', 'morts', 'mortes'],
        'answer': 3  # mortes
    },
    {
        'question': 'la population a ……… aux responsables de résoudre le problème de pollution.',
        'options': ['demandé', 'demandée', 'demandés', 'demandées'],
        'answer': 1  # demandé
    }

    ,{
        'question': 'il …… Une pomme maintenant.',
        'options': ['prend', 'prenez', 'prenons', 'prends'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'chaque jour, nous …… des bonbons.',
        'options': ['veulent', 'veux', 'voulez', 'voulons'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'on ……… Toujours le tee-shirt bleu.',
        'options': ['mettons', 'met', 'mettent', 'mettez'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'chaque matin, vous ……. du sport ?',
        'options': ['faisons', 'fait', 'faites', 'fais'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'les enfants …… des contes tout weekend.',
        'options': ['lit', 'lisent', 'lisons', 'lis'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'tu …… au club tout samedi ?',
        'options': ['vais', 'vont', 'vas', 'va'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'en ce moment, nous…….Thistoire du petit charpon rouge et le loup.',
        'options': ['lit', 'lisent', 'lisons', 'lis'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': '…… nous étudions le Maths.',
        'options': ['hier', 'demain', 'maintenant', 'le mois passé'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'ils ……  tôt du club.',
        'options': ['viennent', 'vient', 'venez', 'viens'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'elles …… faire toujours du sport.',
        'options': ['doivent', 'doit', 'dois', 'devez'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'nous …… le devoir du français.',
        'options': ['finissez', 'finissons', 'finissent', 'finit'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'vous ……… vos camarads.',
        'options': ['appelle', 'appelons', 'appelez', 'appelles'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'mon frère …… tard.',
        'options': ['dort', 'dors', 'dormons', 'dormez'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': '…… vivent à Damas.',
        'options': ['mon ami', 'l\'enfant', 'mes parents', 'Rami'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': '…… cueille des oranges.',
        'options': ['nous', 'vous', 'tu', 'je'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'les élèves…… des lettres aux amis.',
        'options': ['envoyons', 'envoyez', 'envoie', 'envoient'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'tout le monde ……… Thistoire du petit Prince.',
        'options': ['connaît', 'connais', 'connaissons', 'connaissent'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'la mère …… une lettre à son fils.',
        'options': ['écris', 'écrit', 'écrivez', 'écrivent'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'mon fils …… le plus courageux de ses copains.',
        'options': ['êtes', 'est', 'sont', 'sommes'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'les héros du film BLANCHE-NEIGE …… très aimables.',
        'options': ['sont', 'est', 'suis', 'es'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'Ma famille…… une voiture rouge.',
        'options': ['ai', 'as', 'a', 'ont'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': '…….., nous sortons vite du cinéma.',
        'options': ['aujourd\'hui', 'hier', 'demain', 'avant - hier'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'les habitants …….. des arbres dans le parc.',
        'options': ['planter', 'plantons', 'plantent', 'plante'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'le bruit des voitures …… la pollution sonore.',
        'options': ['cause', 'causent', 'causez', 'causons'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'Dans deux jours, Mon fils …… ses études.',
        'options': ['a terminé', 'terminera', 'terminer', 'terminent'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'ils ……… les préparations pour le mariage, dans deux jours.',
        'options': ['finiront', 'ont fini', 'finissaient', 'vont finir'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'On …… demain après les cours.',
        'options': ['s\'est vu', 'vous verrez', 'se verra', 'nous verrons'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'Lundi prochain, mes parents et moi ……… le musée.',
        'options': ['visiter', 'visitaient', 'visiterons', 'visiterez'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': '…… féras le cours avec ta voisine ?',
        'options': ['tu', 'je', 'nous', 'vous'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': '…… vit avec sa famille dans mon quartier.',
        'options': ['les gens', 'mon ami', 'nous', 'vous'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': '…… devrez présenter votre projet demain.',
        'options': ['les élèves', 'le professeur', 'nous', 'vous'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'cette fille …… au maraton le weekend prochain ?',
        'options': ['ira', 'iront', 'irai', 'iras'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': '…….., je participerai au festival.',
        'options': ['le lendemain', 'maintenant', 'aujourd\'hui', 'hier'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'le mois prochain, nous …… rencontrer à Paris.',
        'options': ['avons pu', 'pourrons', 'pouvions', 'pouvoir'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'il ……du café.',
        'options': ['prendrai', 'prendrons', 'prendrez', 'prendra'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'nous ……à Damas, la semaine prochaine.',
        'options': ['étions', 'sommes', 'serons', 'avons été'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'j\'…..une voiture, dans quelques jours.',
        'options': ['avais', 'aurai', 'ai', 'ai eu'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'il …… avec ses amis.',
        'options': ['s\'amuse', 'nous amusons', 'vous amusez', 's\'amusent'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'je ….. douché avec chaque jour.',
        'options': ['me', 'nous', 'vous', 'te'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'mes amies ….. dans la forêt.',
        'options': ['me promène', 'se promènent', 'te promènes', 'se promène'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'mes amies se sont ……… pour sortir.',
        'options': ['préparé', 'préparée', 'préparés', 'préparées'],
        'answer': 4  # كان 3 فأصبح 4
    },
    {
        'question': 'il ……… lavé à l\'eau froid.',
        'options': ['me suis', 's\'est', 'se sont', 't\'es'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'nous…… levons tard, ce matin.',
        'options': ['me', 'nous', 'vous', 'se'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'vous vous …… couchés trop tard.',
        'options': ['sommes', 'sont', 'êtes', 'est'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'hier, elle s\'est ……… rapidement.',
        'options': ['habillé', 'habillée', 'habillés', 'habillées'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'on ………occupé de notre mission.',
        'options': ['se sont', 's\'est', 't\'es', 'me suis'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'actuellement, Sami ….. aux activités caritatives.',
        'options': ['s\'intéresse', 's\'intéressent', 'l\'intéresses', 's\'intéresser'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'dans deux heures, je…… à la campagne.',
        'options': ['vais partir', 'va partir', 'vas partir', 'vont partir'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'dans quelques seconds, la scène ………',
        'options': ['va finir', 'vient de finir', 'finira', 'finissait'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'désolé, elles ………dans 5 minutes.',
        'options': ['vas sortir', 'vont sortir', 'vais sortir', 'va sortir'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'on va lire le conte ……… 10 minutes.',
        'options': ['après', 'avant', 'depuis', 'il y a'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'tu ………L\'affiche de fête du printemps.',
        'options': ['vais écrire', 'vont sortir', 'vas écrire', 'va sortir'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'l\'émission ……… dans cinq minutes.',
        'options': ['vont commencer', 'va commencer', 'vas commencer', 'allons commencer'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'prochainement, cet auteur ……… son nouveau roman.',
        'options': ['va publier', 'vais publier', 'vas publier', 'vont publier'],
        'answer': 1  # كان 0 فأصبح 1
    },
    {
        'question': 'nous ……… l\'histoire de Blanche-neige et les sept nains.',
        'options': ['vas lire', 'vais lire', 'allons lire', 'allez lire'],
        'answer': 3  # كان 2 فأصبح 3
    },
    {
        'question': 'vous…… bienfôt dans un appartement plus grand.',
        'options': ['allons déménager', 'allez déménager', 'vas déménager', 'vont déménager'],
        'answer': 2  # كان 1 فأصبح 2
    },
    {
        'question': 'dépêche-toi ! le train va partir ………',
        'options': ['dans quelques jours', 'le mois prochain', 'hier', 'dans un instant'],
        'answer': 4  # كان 3 فأصبح 4
    }

]


# قائمة الجوائز المالية
PRIZES = [
    100, 200, 300, 500, 700,
    1000, 2000, 4000, 8000, 16000,
    32000, 64000, 125000, 250000, 500000, 1000000
]

class AudienceHelpPopup(ModalView):
    pass

class GameOverPopup(ModalView):
    def __init__(self, **kwargs):
        super(GameOverPopup, self).__init__(**kwargs)
        self.main_screen = None
    
    def restart_game(self):
        if self.main_screen:
            self.main_screen.start_game()
        self.dismiss()
    
    def dismiss(self):
        super(GameOverPopup, self).dismiss()

class WinPopup(ModalView):
    def __init__(self, **kwargs):
        super(WinPopup, self).__init__(**kwargs)
        self.main_screen = None
    
    def dismiss(self):
        if self.main_screen:
            self.main_screen.start_game()
        super(WinPopup, self).dismiss()

class MainScreen(BoxLayout):
    question_text = StringProperty('')
    prize_text = StringProperty('')
    title_text = StringProperty('من سيربح المليون مع محمد  الشيخ french 9')
    background_color = ListProperty([0, 0.1, 0.3, 1])
    audience_available = BooleanProperty(True)
    fifty_available = BooleanProperty(True)
    change_available = BooleanProperty(True)
    
    # ألوان خيارات الإجابة
    option1_color = ListProperty([])
    option2_color = ListProperty([])
    option3_color = ListProperty([])
    option4_color = ListProperty([])
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.title_text = arabic_text(self.title_text)
        self.questions = self.load_questions()
        self.current_question_index = 0
        self.current_prize_index = 0
        self.load_sounds()
        self.start_game()
    
    def load_sounds(self):
        try:
            self.sound_correct = SoundLoader.load('assets/sounds/correct.mp3')
            self.sound_wrong = SoundLoader.load('assets/sounds/kalat.mp3')  # صوت عند الإجابة الخاطئة
            self.sound_applause = SoundLoader.load('assets/sounds/applause.mp3')
            self.sound_1000 = SoundLoader.load('assets/sounds/one1000.mp3')
            self.sound_38000 = SoundLoader.load('assets/sounds/when38.mp3')
            self.sound_64000_clap = SoundLoader.load('assets/sounds/clap.mp3')
            self.sound_64000_sah = SoundLoader.load('assets/sounds/sah.mp3')
            self.sound_win = SoundLoader.load('assets/sounds/win.mp3')
        except:
            # إذا حدث خطأ في تحميل الأصوات
            self.sound_correct = None
            self.sound_wrong = None
            self.sound_applause = None
            self.sound_1000 = None
            self.sound_38000 = None
            self.sound_64000_clap = None
            self.sound_64000_sah = None
            self.sound_win = None
    
    def load_questions(self):
        shuffled_questions = random.sample(QUESTIONS, len(QUESTIONS))
        for q in shuffled_questions:
            q['question'] = arabic_text(q['question'])
            q['options'] = [arabic_text(opt) for opt in q['options']]
        return shuffled_questions
    
    def start_game(self):
        self.current_question_index = 0
        self.current_prize_index = 0
        self.audience_available = True
        self.fifty_available = True
        self.change_available = True
        self.update_prize_text()
        self.next_question()
    
    def update_prize_text(self):
        self.prize_text = arabic_text(f'الجائزة الحالية: {PRIZES[self.current_prize_index]:,} ريال')
        
        # تشغيل الأصوات الخاصة بالمبالغ المالية
        current_prize = PRIZES[self.current_prize_index]
        if current_prize == 1000 and self.sound_1000:
            self.sound_1000.play()
        elif current_prize == 38000 and self.sound_38000:
            self.sound_38000.play()
        elif current_prize == 64000 and self.sound_64000_clap:
            self.sound_64000_clap.play()
    
    def next_question(self):
        if self.current_question_index >= len(self.questions):
            self.show_game_over(arabic_text('تهانينا! لقد أكملت جميع الأسئلة!'))
            return
        
        # إعادة تعيين ألوان الخيارات
        self.option1_color = []
        self.option2_color = []
        self.option3_color = []
        self.option4_color = []
        
        question_data = self.questions[self.current_question_index]
        self.question_text = question_data['question']
        
        for i in range(1, 5):
            self.ids[f'option{i}'].text = question_data['options'][i-1]
            self.ids[f'option{i}'].disabled = False
        
        self.current_question_index += 1
    
    def check_answer(self, answer_num):
        question_data = self.questions[self.current_question_index - 1]
        correct_answer = question_data['answer']
        
        if answer_num == correct_answer:
            self.handle_correct_answer(answer_num)
        else:
            self.handle_wrong_answer(answer_num, correct_answer)
    
    def handle_correct_answer(self, answer_num):
        current_prize = PRIZES[self.current_prize_index]
        
        # تشغيل الصوت المناسب للإجابة الصحيحة
        if current_prize >= 64000 and self.sound_64000_sah:
            self.sound_64000_sah.play()
        elif self.sound_correct:
            self.sound_correct.play()
        
        # تعيين لون الخيار الصحيح
        setattr(self, f'option{answer_num}_color', [0, 0.7, 0, 1])
        
        self.current_prize_index = min(self.current_prize_index + 1, len(PRIZES) - 1)
        self.update_prize_text()
        
        # التحقق إذا وصل إلى مليون ريال
        if PRIZES[self.current_prize_index] == 1000000:
            self.handle_win()
            return
        
        if self.sound_applause and self.current_prize_index in [5, 10, 15]:
            self.sound_applause.play()
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def handle_win(self):
        if self.sound_win:
            self.sound_win.play()
        
        popup = WinPopup()
        popup.main_screen = self
        popup.open()
    
    def handle_wrong_answer(self, answer_num, correct_answer):
        if self.sound_wrong:
            self.sound_wrong.play()
        
        # تعيين ألوان الإجابات (الخطأ برتقالي والصحيح أخضر)
        setattr(self, f'option{answer_num}_color', [1, 0.5, 0, 1])  # برتقالي
        setattr(self, f'option{correct_answer}_color', [0, 0.7, 0, 1])  # أخضر
        
        for i in range(1, 5):
            self.ids[f'option{i}'].disabled = True
        
        final_prize = PRIZES[max(0, self.current_prize_index - 1)] if self.current_prize_index > 0 else 0
        Clock.schedule_once(
            lambda dt: self.show_game_over(arabic_text(f'انتهت اللعبة! جائزتك النهائية: {final_prize:,} ريال')),
            6
        )
    
    def show_game_over(self, message):
        popup = GameOverPopup()
        popup.ids.result_label.text = message
        popup.main_screen = self
        popup.open()
    
    def fifty_fifty(self):
        if not self.fifty_available:
            return
        
        question_data = self.questions[self.current_question_index - 1]
        correct_answer = question_data['answer']
        
        wrong_options = [i for i in range(1, 5) if i != correct_answer]
        to_remove = random.sample(wrong_options, 2)
        
        for option in to_remove:
            self.ids[f'option{option}'].text = ''
            self.ids[f'option{option}'].disabled = True
        
        self.fifty_available = False
    
    def contact_me(self):
        if not self.audience_available:
            return
        
        popup = AudienceHelpPopup()
        popup.open()
    
    def change_question(self):
        if not self.change_available:
            return
        
        self.next_question()
        self.change_available = False

class MillionaireApp(App):
    def build(self):
        self.title = 'من سيربح المليون مع محمد الشيخ'
        return MainScreen()

if __name__ == '__main__':
    MillionaireApp().run()