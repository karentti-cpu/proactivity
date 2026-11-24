# -*- coding: utf-8 -*-
"""A tidier app: the next step on Today, More in three groups, a page for
details and settings, and a three-screen welcome tour.
Order of tuple values: he, en, fr, ru, ar
"""

TIDY = {
# ---- My details and settings (moved out of Progress) ----
'set.t':     ('הפרטים שלי והגדרות', 'My details and settings', 'Mes infos et réglages', 'Мои данные и настройки', 'بياناتي والإعدادات'),
'set.s':     ('שם, גיל, תזכורת וצבע. וגם גיבוי, התקנה בטלפון והזמנת חברים.',
              'Name, age, reminder and colour. Also backup, installing on the phone and inviting friends.',
              'Prénom, âge, rappel et couleur. Et aussi la sauvegarde, l\'installation sur le téléphone et les invitations.',
              'Имя, возраст, напоминание и цвет. А ещё резервная копия, установка на телефон и приглашения друзьям.',
              'الاسم والعمر والتذكير واللون. وأيضاً النسخة الاحتياطية والتثبيت على الهاتف ودعوة الأصدقاء.'),


# ---- Today: the next step, at the top ----
'nx.lab':    ('הצעד הבא', 'Next step', 'Prochain pas', 'Следующий шаг', 'الخطوة التالية'),
'nx.go':     ('להתחיל', 'Start', 'Commencer', 'Начать', 'ابدأ'),
'nx.pause':  ('נשימה של דקה, ורגע לעצמי לפני שהיום מתחיל', 'A minute of breathing, a moment for yourself before the day begins',
              'Une minute de respiration, un moment pour soi avant que la journée commence', 'Минута дыхания и миг для себя, прежде чем начнётся день',
              'دقيقة تنفّس ولحظة لنفسك قبل أن يبدأ اليوم'),
'nx.choose': ('לבחור איך אני רוצה להיות היום', 'Choose how you want to be today', 'Choisir comment tu veux être aujourd\'hui',
              'Выбрать, каким быть сегодня', 'اختر كيف تريد أن تكون اليوم'),
'nx.init':   ('לבחור דבר אחד ליזום היום, בלי שיבקשו', 'Pick one thing to start today, without being asked', 'Choisir une chose à lancer aujourd\'hui, sans qu\'on te le demande',
              'Выбрать одно дело, которое начнёшь сам, без просьб', 'اختر شيئاً واحداً تبادر به اليوم دون أن يُطلب منك'),
'nx.ahead':  ('לתכנן צעד אחד קטן למחר', 'Plan one small step for tomorrow', 'Prévoir un petit pas pour demain', 'Запланировать один маленький шаг на завтра',
              'خطّط لخطوة صغيرة واحدة للغد'),
'nx.day.t':  ('היום שלי', 'My day', 'Ma journée', 'Мой день', 'يومي'),
'nx.day':    ('לעשות את מה שבחרת ולסמן ✓. בערב נפתח הצעד „קדימה”.', 'Do what you chose and tick it ✓. In the evening the “Ahead” step opens.',
              'Fais ce que tu as choisi et coche ✓. Le soir, le pas « Anticiper » s\'ouvre.', 'Сделай выбранное и отметь ✓. Вечером откроется шаг «Вперёд».',
              'افعل ما اخترته وضع ✓. في المساء تُفتح خطوة «إلى الأمام».'),
'nx.day.go': ('ל„היום שלי”', 'To My day', 'Vers Ma journée', 'К «Моему дню»', 'إلى «يومي»'),
'nx.done.s': ('רוצים עוד? משחק קצר, או לבדוק איך אני מרגיש{|ה}.', 'Want more? A short game, or check how you feel.',
              'Envie de plus ? Un petit jeu, ou voir comment tu te sens.', 'Хочешь ещё? Короткая игра или проверить, как ты себя чувствуешь.',
              'تريد المزيد؟ لعبة قصيرة، أو تفقّد شعورك.'),

# ---- Today: the extras, in one card ----
'ex.t':      ('עוד בשבילך היום', 'More for you today', 'En plus pour toi aujourd\'hui', 'Ещё для тебя сегодня', 'المزيد لك اليوم'),

# ---- the welcome tour ----
'tr.1.t':    ('המסלול היומי', 'Your daily path', 'Ton chemin du jour', 'Твой путь на день', 'مسارك اليومي'),
'tr.1.b':    ('כל יום ארבעה צעדים קטנים: לעצור, לבחור, ליזום וקדימה. הכרטיס למעלה תמיד מראה מה הצעד הבא, ומספיק ללחוץ „להתחיל”.',
              'Four small steps every day: pause, choose, initiate and ahead. The card at the top always shows the next step; just tap “Start”.',
              'Quatre petits pas chaque jour : pause, choisir, initier et anticiper. La carte en haut montre toujours le prochain pas ; il suffit de toucher « Commencer ».',
              'Каждый день четыре маленьких шага: пауза, выбор, инициатива и вперёд. Карточка наверху всегда показывает следующий шаг — просто нажми «Начать».',
              'كل يوم أربع خطوات صغيرة: توقّف، اختر، بادر، وإلى الأمام. البطاقة في الأعلى تُظهر دائماً الخطوة التالية، ويكفي أن تضغط «ابدأ».'),
'tr.2.t':    ('היום שלי', 'My day', 'Ma journée', 'Мой день', 'يومي'),
'tr.2.b':    ('רשימה קצרה של מה עושים היום. מוסיפים מהמטרות או כותבים לבד, ומסמנים ✓ כשמסיימים.',
              'A short list of what you do today. Add from your goals or write your own, and tick ✓ when done.',
              'Une courte liste de ce que tu fais aujourd\'hui. Ajoute depuis tes objectifs ou écris toi-même, et coche ✓ quand c\'est fait.',
              'Короткий список дел на сегодня. Добавляй из целей или пиши сам и отмечай ✓, когда готово.',
              'قائمة قصيرة لما تفعله اليوم. أضف من أهدافك أو اكتب بنفسك، وضع ✓ عند الانتهاء.'),
'tr.3.t': ('תרגול לכל צעד', 'Practice for each step', 'De la pratique pour chaque pas', 'Практика для каждого шага', 'تمرين لكل خطوة'),
'tr.3.b': ('ב„תרגול” יש כלים ומשחקים לכל אחד מארבעת הצעדים. ב„התקדמות” רואים איך השבוע הולך. למעלה: ? לעזרה ו־⚙ לפרטים שלי.', 'In “Practice” there are tools and games for each of the four steps. “Progress” shows how the week is going. At the top: ? for help and ⚙ for your details.', "Dans « Pratique », des outils et des jeux pour chacun des quatre pas. « Progrès » montre comment va la semaine. En haut : ? pour l'aide et ⚙ pour tes infos.", 'В «Практике» — инструменты и игры для каждого из четырёх шагов. В «Прогрессе» видно, как идёт неделя. Вверху: ? — помощь, ⚙ — твои данные.', 'في «تمرين» أدوات وألعاب لكل خطوة من الخطوات الأربع. وفي «التقدّم» ترى كيف يسير الأسبوع. في الأعلى: ؟ للمساعدة و⚙ لبياناتك.'),
'tr.next':   ('הבא', 'Next', 'Suivant', 'Далее', 'التالي'),
'tr.go':     ('מתחילים', 'Let\'s go', 'C\'est parti', 'Поехали', 'لنبدأ'),
'tr.skip':   ('דילוג', 'Skip', 'Passer', 'Пропустить', 'تخطٍّ'),
'help.tour': ('לראות שוב את הסיור הקצר', 'See the short tour again', 'Revoir la courte visite', 'Посмотреть короткий тур ещё раз', 'شاهد الجولة القصيرة مرة أخرى'),

# ---- Practice: the tools by the four verbs ----
'prac.t':     ('תרגול', 'Practice', 'Pratique', 'Практика', 'تمرين'),
'prac.s':     ('ארבעה שרירים של פרואקטיביות. בוחרים שריר, ומתרגלים כמה דקות.', 'Four muscles of proactivity. Pick one and practise for a few minutes.',
               'Quatre muscles de la proactivité. Choisis-en un et entraîne-toi quelques minutes.', 'Четыре мышцы проактивности. Выбери одну и потренируйся несколько минут.',
               'أربع عضلات للمبادرة. اختر واحدة وتمرّن عليها بضع دقائق.'),
'vb.pause.s': ('לעצור רגע בין מה שקרה לבין מה שאני עושה: לנשום, להרגיש, להירגע.', 'A moment between what happened and what you do: breathe, feel, calm down.',
               'Un instant entre ce qui arrive et ce que tu fais : respirer, ressentir, te calmer.', 'Миг между тем, что случилось, и тем, что ты делаешь: дышать, чувствовать, успокоиться.',
               'لحظة بين ما حدث وما تفعله: تنفّس، اشعر، اهدأ.'),
'vb.choose.s':('לבחור תגובה לפי מה שחשוב לי, ולא לפי הרגל.', 'Choose a response by what matters to you, not by habit.',
               'Choisir ta réaction selon ce qui compte pour toi, pas par habitude.', 'Выбирать реакцию по тому, что важно, а не по привычке.',
               'اختر ردّك حسب ما يهمّك، لا حسب العادة.'),
'vb.init.s':  ('לעשות צעד בלי שיבקשו: משימה, מעשה טוב, חוזקה בפעולה.', 'Take a step without being asked: a task, a kind act, a strength in action.',
               'Faire un pas sans qu\'on te le demande : une tâche, un geste gentil, une force en action.', 'Сделать шаг без просьб: дело, доброе дело, сильная сторона в действии.',
               'خطوة دون أن يُطلب منك: مهمة، عمل طيب، نقطة قوة في الفعل.'),
'vb.ahead.s': ('להסתכל קדימה: לתכנן את מחר ולראות גם את הטוב.', 'Look ahead: plan tomorrow and see the good too.',
               'Regarder devant : prévoir demain et voir aussi le bon.', 'Смотреть вперёд: планировать завтра и замечать хорошее.',
               'انظر إلى الأمام: خطّط للغد وانتبه للخير أيضاً.'),
'prac.other': ('עוד כלים', 'More tools', 'Autres outils', 'Другие инструменты', 'أدوات أخرى'),
'prac.other.s':('שיעורים קצרים, גוף ובריאות, וכל המשחקים במקום אחד.', 'Short lessons, body and health, and all the games in one place.',
               'De courtes leçons, le corps et la santé, et tous les jeux au même endroit.', 'Короткие уроки, тело и здоровье и все игры в одном месте.',
               'دروس قصيرة، الجسم والصحة، وكل الألعاب في مكان واحد.'),
'prac.games': ('משחקים', 'Games', 'Jeux', 'Игры', 'ألعاب'),
'prac.ahead': ('לתכנן את מחר', 'Plan tomorrow', 'Prévoir demain', 'Спланировать завтра', 'خطّط للغد'),
'prac.back':  ('לתרגול', 'Back to Practice', 'Retour à Pratique', 'Назад к практике', 'العودة إلى التمرين'),
'prac.more':  ('עוד כלים כאן', 'More tools here', 'Plus d\'outils ici', 'Ещё инструменты', 'أدوات أخرى هنا'),
}
