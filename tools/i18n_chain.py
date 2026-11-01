# -*- coding: utf-8 -*-
"""The goal chain: pick an area -> three short questions -> a target that
follows from the answers -> the ladder -> "start the target".

Also the micro-tips that fire on actions around the app.

Areas are ga.<id>. The "which kind" options are per area, gk.<area>.<n>;
study has an adult variant gk.study.a.<n> because "homework" means nothing to a
35-year-old. Frequency and obstacle options are shared by every area.
Order of tuple values: he, en, fr, ru, ar
"""

CHAIN = {

# ================= the nine areas =================
'ga.sport':   ('ספורט וכושר', 'Sport and fitness', 'Sport et forme', 'Спорт и форма', 'رياضة ولياقة'),
'ga.study':   ('לימודים', 'Studies', 'Études', 'Учёба', 'دراسة'),
'ga.time':    ('ניהול זמן', 'Time management', 'Gestion du temps', 'Управление временем', 'إدارة الوقت'),
'ga.goals':   ('מטרות', 'Goals', 'Objectifs', 'Цели', 'أهداف'),
'ga.habits':  ('הרגלים', 'Habits', 'Habitudes', 'Привычки', 'عادات'),
'ga.init':    ('יוזמה ופרואקטיביות', 'Initiative and proactivity', 'Initiative et proactivité', 'Инициатива и проактивность', 'مبادرة واستباقية'),
'ga.sleep':   ('שינה ושגרה', 'Sleep and routine', 'Sommeil et routine', 'Сон и режим', 'نوم وروتين'),
'ga.social':  ('קשרים חברתיים', 'Social life', 'Vie sociale', 'Общение', 'علاقات اجتماعية'),
'ga.learn':   ('ללמוד דברים חדשים', 'Learning new things', 'Apprendre de nouvelles choses', 'Учиться новому', 'تعلّم أشياء جديدة'),

# ================= the chain screens =================
'gc.t':        ('מה בא לך לשפר?', 'What do you want to improve?', 'Tu veux améliorer quoi ?', 'Что хочешь улучшить?', 'ما الذي تريد تحسينه؟'),
'gc.s':        ('מטרה היא יעד שחשוב לך לאורך זמן. כל צעד קטן חשוב בדרך. שלוש שאלות קצרות, ונבנה אותה יחד.',
                  'A goal is a target that matters to you over time. Every small step on the way counts. Three short questions, and we build it together.',
                  'Un objectif, c\'est un cap qui compte pour toi dans la durée. Chaque petit pas compte sur le chemin. Trois questions courtes, et on le construit ensemble.',
                  'Цель — это ориентир, важный для тебя надолго. Каждый маленький шаг на пути важен. Три коротких вопроса — и построим её вместе.',
                  'الهدف غاية تهمّك على المدى الطويل. كل خطوة صغيرة مهمّة في الطريق. ثلاثة أسئلة قصيرة، ونبنيه معاً.'),
'gc.kind.q':   ('מה בדיוק?', 'What exactly?', 'Quoi, exactement ?', 'Что именно?', 'ماذا بالضبط؟'),
'gc.kind.s':   ('כמה שיותר ספציפי, ככה קל יותר להתחיל.',
                'The more specific, the easier it is to start.',
                'Plus c\'est précis, plus c\'est facile de commencer.',
                'Чем конкретнее, тем легче начать.',
                'كلّما كان أدقّ، كان البدء أسهل.'),
'gc.other':    ('משהו אחר', 'Something else', 'Autre chose', 'Что-то другое', 'شيء آخر'),
'gc.other.ph': ('{כתוב|כתבי} מה', 'Write what', 'Écris quoi', 'Напиши что', '{اكتب|اكتبي} ماذا'),
'gc.freq.q':   ('כמה פעמים בשבוע?', 'How many times a week?', 'Combien de fois par semaine ?', 'Сколько раз в неделю?', 'كم مرة في الأسبوع؟'),
'gc.freq.s':   ('מספר שאפשר באמת לעמוד בו. תמיד אפשר להעלות.',
                'A number you can actually keep. You can always raise it.',
                'Un nombre que tu peux vraiment tenir. Tu pourras toujours l\'augmenter.',
                'Число, которое реально выдержать. Всегда можно поднять.',
                'رقم يمكنك الالتزام به فعلاً. يمكنك دائماً رفعه.'),
'gc.obst.q':   ('מה הכי מפריע לך כרגע?', 'What gets in the way most right now?', 'Qu\'est-ce qui te bloque le plus ?', 'Что больше всего мешает сейчас?', 'ما الذي يعيقك أكثر الآن؟'),
'gc.obst.s':   ('לפי זה נבחר את הצעד הראשון.',
                'This decides the first step.',
                'C\'est ça qui décide de la première étape.',
                'От этого зависит первый шаг.',
                'بناءً عليه نختار الخطوة الأولى.'),
'gc.name':     ('איך לקרוא למטרה?', 'What do you call this goal?', 'Comment appeler cet objectif ?', 'Как назвать цель?', 'ماذا {تسمّي|تسمّين} هذا الهدف؟'),
'gc.result.t': ('הנה היעד שלך', 'Here is your target', 'Voici ton objectif', 'Вот твоя цель', 'ها هو هدفك'),
'gc.result.s': ('נבנה ממה שאמרת. אפשר לערוך כל שורה.',
                'Built from what you said. Every line can be edited.',
                'Construit à partir de tes réponses. Chaque ligne est modifiable.',
                'Собрана из твоих ответов. Каждую строку можно изменить.',
                'مبنيّ ممّا قلته. يمكن تعديل كل سطر.'),
'gc.start':    ('התחל את היעד', 'Start the target', 'Lancer l\'objectif', 'Начать цель', 'ابدأ الهدف'),
'gc.start.n':  ('המעקב, הרצף והמשימות מתחילים רק כשלוחצים כאן. עד אז זה רק יעד כתוב.',
                'Tracking, the streak and the tasks only begin when you press this. Until then it is just a written target.',
                'Le suivi, la série et les tâches ne démarrent que quand tu appuies ici. Avant, ce n\'est qu\'un objectif écrit.',
                'Отслеживание, серия и задачи начинаются только по нажатию. До этого это просто записанная цель.',
                'المتابعة والسلسلة والمهام تبدأ فقط عند الضغط هنا. حتى ذلك الحين هو مجرد هدف مكتوب.'),
'gc.later':    ('לשמור בלי להתחיל', 'Save without starting', 'Enregistrer sans lancer', 'Сохранить, не начиная', 'حفظ دون بدء'),
'gc.new':      ('יעד חדש', 'New target', 'Nouvel objectif', 'Новая цель', 'هدف جديد'),
'gc.free':     ('או {כתוב|כתבי} יעד במילים שלך', 'Or write a target in your own words', 'Ou écris un objectif avec tes mots', 'Или напиши цель своими словами', 'أو {اكتب|اكتبي} هدفاً بكلماتك'),
'gc.notstarted': ('מוכן להתחלה',
                  'Ready to start',
                  'Prêt à démarrer',
                  'Готова к старту',
                  'جاهز للبدء'),
'gc.started':  ('פעיל מאז {d}', 'Active since {d}', 'Actif depuis le {d}', 'Активна с {d}', 'نشط منذ {d}'),
'gc.started.t':('התחלת. מעכשיו זה נספר.', 'You started. From now on it counts.', 'C\'est lancé. À partir de maintenant, ça compte.', 'Ты начал{|а}. С этого момента считается.', 'بدأت. من الآن يُحتسب.'),
'gc.dup':      ('כבר יש יעד כזה', 'You already have a target like that', 'Tu as déjà un objectif comme ça', 'Такая цель уже есть', 'لديك هدف مثله بالفعل'),
'gc.plan.q':   ('רוצה גם תוכנית?', 'Want a plan to go with it?', 'Tu veux un plan qui va avec ?', 'Хочешь план к ней?', 'تريد خطة معه؟'),

# ---- shared frequency options ----
'gf.1': ('פעם בשבוע', 'Once a week', 'Une fois par semaine', 'Раз в неделю', 'مرة في الأسبوع'),
'gf.2': ('פעמיים בשבוע', 'Twice a week', 'Deux fois par semaine', 'Два раза в неделю', 'مرتين في الأسبوع'),
'gf.3': ('3 פעמים בשבוע', '3 times a week', '3 fois par semaine', '3 раза в неделю', '3 مرات في الأسبوع'),
'gf.4': ('4 פעמים בשבוע', '4 times a week', '4 fois par semaine', '4 раза в неделю', '4 مرات في الأسبوع'),
'gf.5': ('כמעט כל יום', 'Almost every day', 'Presque tous les jours', 'Почти каждый день', 'كل يوم تقريباً'),

# ---- shared obstacle options ----
'go.start':   ('קשה לי להתחיל', 'I find it hard to start', 'J\'ai du mal à commencer', 'Мне трудно начать', 'يصعب عليّ البدء'),
'go.delay':   ('אני דוחה את זה', 'I keep putting it off', 'Je repousse tout le temps', 'Я всё время откладываю', 'أؤجّله باستمرار'),
'go.time':    ('אין לי זמן', 'I do not have time', 'Je n\'ai pas le temps', 'У меня нет времени', 'ليس لديّ وقت'),
'go.keep':    ('קשה לי להתמיד', 'I find it hard to keep going', 'J\'ai du mal à tenir', 'Мне трудно продолжать', 'يصعب عليّ الاستمرار'),
'go.what':    ('לא {יודע|יודעת} מה לעשות', 'I do not know what to do', 'Je ne sais pas quoi faire', 'Не знаю, что делать', 'لا أعرف ماذا أفعل'),
'go.other':   ('משהו אחר', 'Something else', 'Autre chose', 'Что-то другое', 'شيء آخر'),

# ---- "which kind" per area ----
'gk.sport.1': ('חדר כושר', 'Gym', 'Salle de sport', 'Зал', 'نادي رياضي'),
'gk.sport.2': ('ריצה', 'Running', 'Course à pied', 'Бег', 'ركض'),
'gk.sport.3': ('כדורסל', 'Basketball', 'Basket', 'Баскетбол', 'كرة سلة'),
'gk.sport.4': ('כדורגל', 'Football', 'Foot', 'Футбол', 'كرة قدم'),
'gk.sport.5': ('שחייה', 'Swimming', 'Natation', 'Плавание', 'سباحة'),
'gk.sport.6': ('אימון בבית', 'Home workout', 'Sport à la maison', 'Тренировка дома', 'تمرين في البيت'),

'gk.study.1': ('מקצוע מסוים', 'A specific subject', 'Une matière précise', 'Конкретный предмет', 'مادة معيّنة'),
'gk.study.2': ('שיעורי בית בזמן', 'Homework on time', 'Devoirs à l\'heure', 'Домашка вовремя', 'الواجبات في وقتها'),
'gk.study.3': ('הכנה למבחנים', 'Exam prep', 'Préparation aux contrôles', 'Подготовка к контрольным', 'التحضير للامتحانات'),
'gk.study.4': ('לקרוא יותר', 'Reading more', 'Lire plus', 'Больше читать', 'قراءة أكثر'),
'gk.study.5': ('שפה', 'A language', 'Une langue', 'Язык', 'لغة'),
'gk.study.6': ('ריכוז בשיעור', 'Focus in class', 'Concentration en cours', 'Внимание на уроке', 'تركيز في الصف'),

'gk.study.a.1': ('קורס או תואר', 'A course or a degree', 'Un cours ou un diplôme', 'Курс или диплом', 'دورة أو شهادة'),
'gk.study.a.2': ('מיומנות מקצועית', 'A professional skill', 'Une compétence pro', 'Профессиональный навык', 'مهارة مهنية'),
'gk.study.a.3': ('שפה', 'A language', 'Une langue', 'Язык', 'لغة'),
'gk.study.a.4': ('לקרוא יותר', 'Reading more', 'Lire plus', 'Больше читать', 'قراءة أكثر'),
'gk.study.a.5': ('הסמכה או מבחן', 'A certification or exam', 'Une certification ou un examen', 'Сертификат или экзамен', 'شهادة أو امتحان'),
'gk.study.a.6': ('תכנות', 'Coding', 'Programmation', 'Программирование', 'برمجة'),

'gk.time.1': ('לקום בזמן', 'Getting up on time', 'Me lever à l\'heure', 'Вставать вовремя', 'الاستيقاظ في الوقت'),
'gk.time.2': ('להתחיל משימות', 'Getting started on tasks', 'Démarrer les tâches', 'Начинать задачи', 'البدء بالمهام'),
'gk.time.3': ('פחות זמן מסך', 'Less screen time', 'Moins d\'écran', 'Меньше экрана', 'وقت أقل أمام الشاشة'),
'gk.time.4': ('לתכנן את היום', 'Planning the day', 'Planifier la journée', 'Планировать день', 'تخطيط اليوم'),
'gk.time.5': ('לסיים מה שהתחלתי', 'Finishing what I start', 'Finir ce que je commence', 'Заканчивать начатое', 'إنهاء ما بدأته'),
'gk.time.6': ('להגיע בזמן', 'Being on time', 'Être à l\'heure', 'Приходить вовремя', 'الوصول في الوقت'),

'gk.goals.1': ('מטרה אחת גדולה', 'One big goal', 'Un grand objectif', 'Одна большая цель', 'هدف واحد كبير'),
'gk.goals.2': ('לפרק לצעדים', 'Breaking things into steps', 'Découper en étapes', 'Разбивать на шаги', 'التقسيم إلى خطوات'),
'gk.goals.3': ('לעקוב אחרי התקדמות', 'Tracking progress', 'Suivre mes progrès', 'Отслеживать прогресс', 'متابعة التقدّم'),
'gk.goals.4': ('לבחור כיוון', 'Picking a direction', 'Choisir une direction', 'Выбрать направление', 'اختيار اتجاه'),
'gk.goals.5': ('לסיים פרויקט', 'Finishing a project', 'Terminer un projet', 'Закончить проект', 'إنهاء مشروع'),
'gk.goals.6': ('פחות הסחות', 'Fewer distractions', 'Moins de distractions', 'Меньше отвлекаться', 'تشتّت أقل'),

'gk.habits.1': ('שגרת בוקר', 'A morning routine', 'Une routine du matin', 'Утренний ритуал', 'روتين صباحي'),
'gk.habits.2': ('שגרת ערב', 'An evening routine', 'Une routine du soir', 'Вечерний ритуал', 'روتين مسائي'),
'gk.habits.3': ('לשתות מים', 'Drinking water', 'Boire de l\'eau', 'Пить воду', 'شرب الماء'),
'gk.habits.4': ('לקרוא כל יום', 'Reading daily', 'Lire chaque jour', 'Читать каждый день', 'القراءة يومياً'),
'gk.habits.5': ('לכתוב יומן', 'Journaling', 'Tenir un journal', 'Вести дневник', 'كتابة يوميات'),
'gk.habits.6': ('פחות טלפון', 'Less phone', 'Moins de téléphone', 'Меньше телефона', 'هاتف أقل'),

'gk.init.1': ('להגיד מה אני {חושב|חושבת}', 'Speaking up', 'Dire ce que je pense', 'Высказываться', 'قول ما أفكّر به'),
'gk.init.2': ('להתחיל בלי שיבקשו', 'Starting without being asked', 'Commencer sans qu\'on me le demande', 'Начинать без просьбы', 'البدء دون أن يُطلب'),
'gk.init.3': ('לפנות לאנשים', 'Reaching out to people', 'Aller vers les gens', 'Обращаться к людям', 'التواصل مع الناس'),
'gk.init.4': ('לנסות משהו חדש', 'Trying something new', 'Essayer quelque chose de nouveau', 'Пробовать новое', 'تجربة شيء جديد'),
'gk.init.5': ('לקחת אחריות', 'Taking the lead', 'Prendre les choses en main', 'Брать на себя', 'تحمّل المسؤولية'),
'gk.init.6': ('לשאול שאלות', 'Asking questions', 'Poser des questions', 'Задавать вопросы', 'طرح الأسئلة'),

'gk.sleep.1': ('ללכת לישון בזמן', 'Going to bed on time', 'Me coucher à l\'heure', 'Ложиться вовремя', 'النوم في الوقت'),
'gk.sleep.2': ('לקום בשעה קבועה', 'Waking up at a fixed time', 'Me lever à heure fixe', 'Вставать в одно время', 'الاستيقاظ في وقت ثابت'),
'gk.sleep.3': ('בלי טלפון לפני השינה', 'No phone before bed', 'Pas de téléphone avant de dormir', 'Без телефона перед сном', 'بلا هاتف قبل النوم'),
'gk.sleep.4': ('שגרת הרגעה בערב', 'A wind-down routine', 'Une routine pour décompresser', 'Вечернее расслабление', 'روتين تهدئة مسائي'),
'gk.sleep.5': ('שעות קבועות', 'Consistent hours', 'Des horaires réguliers', 'Стабильный график', 'ساعات ثابتة'),
'gk.sleep.6': ('פחות קפאין', 'Less caffeine', 'Moins de caféine', 'Меньше кофеина', 'كافيين أقل'),

'gk.social.1': ('ליזום מפגש עם חברים', 'Initiating time with friends', 'Proposer des sorties aux amis', 'Звать друзей', 'المبادرة للقاء الأصدقاء'),
'gk.social.2': ('להכיר אנשים חדשים', 'Meeting new people', 'Rencontrer de nouvelles personnes', 'Знакомиться с новыми людьми', 'التعرّف على أشخاص جدد'),
'gk.social.3': ('זמן עם המשפחה', 'Family time', 'Du temps en famille', 'Время с семьёй', 'وقت مع العائلة'),
'gk.social.4': ('להקשיב יותר', 'Listening more', 'Écouter plus', 'Больше слушать', 'الإصغاء أكثر'),
'gk.social.5': ('להצטרף לקבוצה', 'Joining a group', 'Rejoindre un groupe', 'Вступить в группу', 'الانضمام لمجموعة'),
'gk.social.6': ('לשמור על קשר', 'Keeping in touch', 'Garder le contact', 'Поддерживать связь', 'البقاء على تواصل'),

'gk.learn.1': ('שפה', 'A language', 'Une langue', 'Язык', 'لغة'),
'gk.learn.2': ('כלי נגינה', 'An instrument', 'Un instrument', 'Инструмент', 'آلة موسيقية'),
'gk.learn.3': ('תכנות', 'Coding', 'Programmation', 'Программирование', 'برمجة'),
'gk.learn.4': ('בישול', 'Cooking', 'Cuisine', 'Готовка', 'طبخ'),
'gk.learn.5': ('ציור', 'Drawing', 'Dessin', 'Рисование', 'رسم'),
'gk.learn.6': ('משהו אחר', 'Something else', 'Autre chose', 'Что-то другое', 'شيء آخر'),

# ================= composing the target =================
# title = kind + frequency
# the "this week" rung
'gw.line':   ('{freq}: {kind}', '{freq}: {kind}', '{freq} : {kind}', '{freq}: {kind}', '{freq}: {kind}'),

# the "today" rung, per area
'gd.sport':  ('אימון אחד של 20–30 דקות', 'One 20–30 minute session', 'Une séance de 20–30 minutes', 'Одна тренировка на 20–30 минут', 'تمرين واحد من 20–30 دقيقة'),
'gd.study':  ('20 דקות מרוכזות על {kind}', '20 focused minutes on {kind}', '20 minutes concentrées sur {kind}', '20 сосредоточенных минут на {kind}', '20 دقيقة تركيز على {kind}'),
'gd.time':   ('לבחור משימה אחת ולהתחיל אותה', 'Pick one task and start it', 'Choisir une tâche et la commencer', 'Выбрать одну задачу и начать', 'اختيار مهمة واحدة والبدء بها'),
'gd.goals':  ('לכתוב את הצעד הבא', 'Write down the next step', 'Écrire la prochaine étape', 'Записать следующий шаг', 'كتابة الخطوة التالية'),
'gd.habits': ('לעשות את זה פעם אחת היום', 'Do it once today', 'Le faire une fois aujourd\'hui', 'Сделать это один раз сегодня', 'فعله مرة واحدة اليوم'),
'gd.init':   ('דבר אחד ביוזמה שלך',
                  'One thing on your own initiative',
                  'Une chose de ta propre initiative',
                  'Одно дело по своей инициативе',
                  'شيء واحد بمبادرتك'),
'gd.sleep':  ('ללכת לישון בשעה שקבעת', 'Go to bed at the time you set', 'Me coucher à l\'heure fixée', 'Лечь в назначенное время', 'النوم في الوقت الذي حدّدته'),
'gd.social': ('הודעה או שיחה אחת', 'One message or one conversation', 'Un message ou une conversation', 'Одно сообщение или разговор', 'رسالة أو محادثة واحدة'),
'gd.learn':  ('15 דקות תרגול', '15 minutes of practice', '15 minutes de pratique', '15 минут практики', '15 دقيقة تدريب'),

# the "right now" rung, chosen by the obstacle - this is where the answer
# actually changes what the user is told to do next
'gn.start':  ('5 דקות עכשיו. מספיק להתחיל — ההמשך מגיע לבד.',
                  '5 minutes now. Starting is enough — the rest follows.',
                  '5 minutes maintenant. Commencer suffit — la suite vient toute seule.',
                  '5 минут сейчас. Достаточно начать — дальше пойдёт само.',
                  '5 دقائق الآن. يكفي أن تبدأ — والباقي يأتي وحده.'),
'gn.delay':  ('לקבוע יום ושעה, ולכתוב אותם.', 'Set a day and an hour, and write them down.', 'Fixer un jour et une heure, et les noter.', 'Назначить день и час — и записать.', 'تحديد يوم وساعة، وكتابتهما.'),
'gn.time':   ('להקטין: מה הגרסה של 10 דקות?', 'Shrink it: what is the 10-minute version?', 'Réduire : c\'est quoi la version 10 minutes ?', 'Уменьшить: какая версия на 10 минут?', 'تصغيره: ما نسخة الـ10 دقائق؟'),
'gn.keep':   ('להצמיד את זה למשהו שכבר קורה כל יום.', 'Attach it to something that already happens every day.', 'L\'accrocher à quelque chose qui arrive déjà chaque jour.', 'Привязать к тому, что уже происходит каждый день.', 'ربطه بشيء يحدث يومياً بالفعل.'),
'gn.what':   ('לכתוב את הצעד הראשון הכי קטן שיש.', 'Write the very smallest first step.', 'Écrire la toute plus petite première étape.', 'Записать самый маленький первый шаг.', 'كتابة أصغر خطوة أولى ممكنة.'),
'gn.other':  ('לבחור מתי מתחילים.', 'Decide when you start.', 'Décider quand tu commences.', 'Решить, когда начинаешь.', 'اختيار موعد البدء.'),

# the offered plan, per area: sport goes to the training plan that
# already exists; the rest open the lesson that fits
'gp.sport':  ('תוכנית אימון שמתאימה לגיל שלך', 'A training plan that fits your age', 'Un programme adapté à ton âge', 'План тренировок под твой возраст', 'خطة تمرين تناسب عمرك'),
'gp.study':  ('איך הופכים לימוד להרגל', 'How studying becomes a habit', 'Comment réviser devient une habitude', 'Как учёба становится привычкой', 'كيف تتحوّل الدراسة إلى عادة'),
'gp.time':   ('דחיינות: מאיפה מתחילים', 'Procrastination: where to start', 'Procrastination : par où commencer', 'Прокрастинация: с чего начать', 'التسويف: من أين نبدأ'),
'gp.goals':  ('איך מציבים מטרה שבאמת קורית', 'How to set a goal that actually happens', 'Fixer un objectif qui se réalise', 'Как поставить цель, которая случится', 'كيف تضع هدفاً يتحقّق فعلاً'),
'gp.habits': ('איך מטרה הופכת להרגל', 'How a goal turns into a habit', 'Transformer un objectif en habitude', 'Как цель становится привычкой', 'كيف يتحوّل الهدف إلى عادة'),
'gp.init':   ('פרואקטיבי מול ריאקטיבי', 'Proactive vs reactive', 'Proactif ou réactif', 'Проактивный или реактивный', 'مبادر أم متفاعل'),
'gp.sleep':  ('איך מטרה הופכת להרגל', 'How a goal turns into a habit', 'Transformer un objectif en habitude', 'Как цель становится привычкой', 'كيف يتحوّل الهدف إلى عادة'),
'gp.social': ('איך מפסיקים לחכות למוטיבציה', 'How to stop waiting for motivation', 'Arrêter d\'attendre la motivation', 'Как перестать ждать мотивацию', 'كيف تتوقّف عن انتظار الحماس'),
'gp.learn':  ('איך מתחילים כשאין כוח', 'How to start with no energy', 'Démarrer sans énergie', 'Как начать без сил', 'كيف تبدأ وأنت بلا طاقة'),

# ================= micro-tips =================
# Fired once per action type per day, at most. Short, tied to what just
# happened, never a lecture.
'tip.lab':        ('פרואקטיביות קטנה', 'A small proactive moment', 'Un petit moment proactif', 'Маленькая проактивность', 'مبادرة صغيرة'),
'tip.task.done':  ('יזמת בעצמך. זו בדיוק פרואקטיביות.',
                  'You took the initiative yourself. That is exactly what proactive means.',
                  "Tu as pris l'initiative toi-même. C'est exactement ça, être proactif.",
                  'Ты проявил{|а} инициативу сам{|а}. Это и есть проактивность.',
                  'بادرت بنفسك. هذه هي المبادرة بالضبط.'),
'tip.goal.new':   ('יעד טוב מתחיל בצעד שאפשר לבצע.',
                   'A good target starts with a step you can actually take.',
                   'Un bon objectif commence par une étape faisable.',
                   'Хорошая цель начинается с шага, который можно сделать.',
                   'الهدف الجيد يبدأ بخطوة يمكن تنفيذها.'),
'tip.goal.start': ('מ"אני רוצה" ל"אני עושה" — זה בדיוק המעבר.',
                   'From "I want to" to "I am doing" — that is the whole shift.',
                   'De « je veux » à « je fais » — c\'est exactement ça, le passage.',
                   'От «хочу» к «делаю» — вот и весь переход.',
                   'من «أريد» إلى «أفعل» — هذا هو الانتقال بالضبط.'),
'tip.goal.done':  ('זאת בדיוק פרואקטיביות: זיהית משהו שרצית לשנות, ופעלת.',
                   'That is exactly proactivity: you spotted something you wanted to change, and acted.',
                   'C\'est exactement ça, la proactivité : tu as repéré un truc à changer, et tu as agi.',
                   'Это и есть проактивность: ты заметил{|а}, что хочешь изменить, и сделал{|а}.',
                   'هذه هي المبادرة بالضبط: لاحظت شيئاً أردت تغييره، وتصرّفت.'),
'tip.task.skip':  ('כלל 5 הדקות: מספיק להתחיל, וההמשך מגיע לבד.',
                  'The 5-minute rule: starting is enough, and the rest follows.',
                  'La règle des 5 minutes : commencer suffit, la suite vient toute seule.',
                  'Правило 5 минут: достаточно начать — дальше пойдёт само.',
                  'قاعدة الـ5 دقائق: يكفي أن تبدأ، والباقي يأتي وحده.'),
'tip.streak':     ('רצף נבנה מחזרה. כל פעם {שאתה חוזר|שאת חוזרת}, הוא מתחזק.',
                  'A streak is built by coming back. Every return makes it stronger.',
                  'Une série se construit en revenant. Chaque retour la renforce.',
                  'Серия строится на возвращении. Каждое возвращение делает её сильнее.',
                  'السلسلة تُبنى بالعودة. كل عودة تجعلها أقوى.'),
'tip.lesson':     ('לדעת זה חצי. החצי השני הוא הדבר הקטן שתעשה{|י} עכשיו.',
                   'Knowing is half of it. The other half is the small thing you do now.',
                   'Savoir, c\'est la moitié. L\'autre moitié, c\'est le petit truc que tu fais maintenant.',
                   'Знать — половина дела. Вторая половина — то маленькое, что ты сделаешь сейчас.',
                   'المعرفة نصف الأمر. النصف الآخر هو الشيء الصغير الذي {ستفعله|ستفعلينه} الآن.'),
}
