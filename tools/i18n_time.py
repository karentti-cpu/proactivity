# -*- coding: utf-8 -*-
"""Time management in My day: important / urgent, a time for a line, adding
it to the phone's calendar, and getting organised for tomorrow.
Order of tuple values: he, en, fr, ru, ar
"""

TIMEM = {
'c.delete':  ('למחוק', 'Delete', 'Supprimer', 'Удалить', 'احذف'),
'tm.imp':    ('חשוב', 'Important', 'Important', 'Важно', 'مهمّ'),
'tm.urg':    ('דחוף', 'Urgent', 'Urgent', 'Срочно', 'عاجل'),
'tm.time':   ('שעה', 'Time', 'Heure', 'Время', 'الوقت'),
'tm.more':   ('עוד אפשרויות', 'More options', 'Plus d\'options', 'Ещё', 'خيارات أخرى'),
'tm.cal':    ('להוסיף ליומן', 'Add to calendar', 'Ajouter à l\'agenda', 'В календарь', 'أضف إلى التقويم'),
'tm.cal.need':('קודם בוחרים שעה', 'Pick a time first', 'Choisis d\'abord une heure', 'Сначала выбери время', 'اختر الوقت أولاً'),
'tm.cal.ok': ('נוסף ליומן. התזכורת תגיע רבע שעה לפני ✓', 'Added to the calendar. A reminder comes 15 minutes before ✓', 'Ajouté à l\'agenda. Un rappel 15 minutes avant ✓',
              'Добавлено в календарь. Напоминание за 15 минут ✓', 'أُضيف إلى التقويم. يصل التذكير قبل ربع ساعة ✓'),
'tm.timed':  ('לפי שעות', 'By time', 'Par heure', 'По времени', 'حسب الوقت'),
'tm.untimed':('בלי שעה', 'No set time', 'Sans heure', 'Без времени', 'بلا وقت'),
'tm.q2':     ('⭐ „{x}” חשוב ועוד לא דחוף. כדאי לקדם אותו עכשיו, לפני שיהפוך לדחוף.', '⭐ “{x}” is important and not yet urgent. Worth moving it forward now, before it becomes urgent.',
              '⭐ « {x} » est important et pas encore urgent. Mieux vaut l\'avancer maintenant, avant qu\'il ne devienne urgent.',
              '⭐ «{x}» — важно и пока не срочно. Стоит продвинуть сейчас, пока не стало срочным.',
              '⭐ «{x}» مهمّ وليس عاجلاً بعد. يستحقّ أن تتقدّم فيه الآن قبل أن يصبح عاجلاً.'),
'tm.first':  ('מה הכי חשוב היום? אפשר לסמן ⭐ ליד שורה.', 'What matters most today? Mark a line with ⭐.', 'Qu\'est-ce qui compte le plus aujourd\'hui ? Marque une ligne d\'une ⭐.',
              'Что сегодня важнее всего? Отметь строку ⭐.', 'ما الأهمّ اليوم؟ ضع ⭐ بجانب سطر.'),
'tm.tom':    ('להתארגן למחר', 'Get organised for tomorrow', 'S\'organiser pour demain', 'Подготовиться к завтра', 'الاستعداد للغد'),
'tm.tom.s':  ('מה מחכה מחר? פגישות, תורים ודברים חשובים. בבוקר הם כבר יחכו ב„היום שלי”.', 'What is coming tomorrow? Meetings, appointments and important things. In the morning they will be waiting in “My day”.',
              'Qu\'est-ce qui t\'attend demain ? Rendez-vous et choses importantes. Le matin, ils t\'attendront dans « Ma journée ».',
              'Что ждёт завтра? Встречи, записи и важные дела. Утром они уже будут в «Моём дне».',
              'ما الذي ينتظرك غداً؟ مواعيد وأمور مهمّة. في الصباح ستكون بانتظارك في «يومي».'),
'tm.tom.ph': ('למשל: רופא שיניים', 'e.g. dentist', 'ex. : dentiste', 'например: стоматолог', 'مثلاً: طبيب الأسنان'),
'tm.prep':   ('מה צריך להכין מראש?', 'What needs preparing in advance?', 'Qu\'est-ce qu\'il faut préparer à l\'avance ?', 'Что нужно подготовить заранее?', 'ما الذي يجب تحضيره مسبقاً؟'),
'tm.prep.ph':('למשל: להכין תיק ובגדים', 'e.g. pack the bag and lay out clothes', 'ex. : préparer le sac et les vêtements', 'например: собрать сумку и одежду', 'مثلاً: تجهيز الحقيبة والملابس'),
'tm.prep.ok':('נוסף ל„היום שלי”, להכין הערב ✓', 'Added to “My day”, to prepare tonight ✓', 'Ajouté à « Ma journée », à préparer ce soir ✓', 'Добавлено в «Мой день» — подготовить сегодня вечером ✓', 'أُضيف إلى «يومي» للتحضير الليلة ✓'),
'tm.tom.n':  ('מחכים למחר: {n}', 'Waiting for tomorrow: {n}', 'Prévu pour demain : {n}', 'На завтра: {n}', 'بانتظار الغد: {n}'),
'help.12.t': ('ניהול זמן', 'Managing time', 'Gérer son temps', 'Управление временем', 'إدارة الوقت'),
'help.12.b': ('ב„היום שלי” לוחצים ⋯ ליד שורה: מסמנים ⭐ חשוב או ⏰ דחוף, מוסיפים שעה, ושולחים ליומן של הטלפון עם תזכורת. בערב, ב„לתכנן את מחר”, כותבים מה מחכה מחר, והוא מופיע בבוקר.',
              'In “My day”, tap ⋯ next to a line: mark ⭐ important or ⏰ urgent, add a time, and send it to the phone\'s calendar with a reminder. In the evening, in “Plan tomorrow”, write what is coming tomorrow, and it shows up in the morning.',
              'Dans « Ma journée », touche ⋯ à côté d\'une ligne : marque ⭐ important ou ⏰ urgent, ajoute une heure et envoie-la à l\'agenda avec un rappel. Le soir, dans « Planifier demain », écris ce qui t\'attend demain : ce sera là au matin.',
              'В «Моём дне» нажми ⋯ рядом со строкой: отметь ⭐ важно или ⏰ срочно, добавь время и отправь в календарь телефона с напоминанием. Вечером в «Планируем завтра» запиши, что ждёт завтра, — утром это появится.',
              'في «يومي» اضغط ⋯ بجانب سطر: ضع ⭐ مهمّ أو ⏰ عاجل، وأضف وقتاً، وأرسله إلى تقويم الهاتف مع تذكير. وفي المساء، في «خطّط للغد»، اكتب ما ينتظرك غداً فيظهر في الصباح.'),
}
