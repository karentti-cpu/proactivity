# -*- coding: utf-8 -*-
"""The daily path at the top of the home page, and the greeting by time of day.
Order of tuple values: he, en, fr, ru, ar
"""

PATH = {
'a.greet.m': ('בוקר טוב, {name} ☀️', 'Good morning, {name} ☀️', 'Bonjour, {name} ☀️', 'Доброе утро, {name} ☀️', 'صباح الخير، {name} ☀️'),
'a.greet.n': ('צהריים טובים, {name}', 'Good afternoon, {name}', 'Bon après-midi, {name}', 'Добрый день, {name}', 'نهارك سعيد، {name}'),
'a.greet.e': ('ערב טוב, {name} 🌙', 'Good evening, {name} 🌙', 'Bonsoir, {name} 🌙', 'Добрый вечер, {name} 🌙', 'مساء الخير، {name} 🌙'),
'path.t':    ('המסלול שלי היום', 'My path today', 'Mon parcours du jour', 'Мой путь сегодня', 'مساري اليوم'),
'path.pause':('לעצור', 'Pause', 'Pause', 'Пауза', 'توقّف'),
'path.today':('לעשות', 'Do', 'Agir', 'Дела', 'افعل'),
'path.feel': ('להרגיש', 'Feel', 'Ressentir', 'Чувства', 'اشعر'),
'path.game': ('לשחק', 'Play', 'Jouer', 'Игра', 'العب'),
'path.n':    ('{n} מתוך 4', '{n} of 4', '{n} sur 4', '{n} из 4', '{n} من 4'),
'path.next': ('הצעד הבא: {s}', 'Next step: {s}', 'Prochain pas : {s}', 'Следующий шаг: {s}', 'الخطوة التالية: {s}'),
'path.full': ('יום מלא! 🎉', 'A full day! 🎉', 'Journée complète ! 🎉', 'Полный день! 🎉', 'يوم مكتمل! 🎉'),
'path.fullxp':('יום מלא! 🎉 +20 XP', 'A full day! 🎉 +20 XP', 'Journée complète ! 🎉 +20 XP', 'Полный день! 🎉 +20 XP', 'يوم مكتمل! 🎉 +20 XP'),
'path.streak':('🔥 {n} ימים מלאים ברצף', '🔥 {n} full days in a row', '🔥 {n} journées complètes d\'affilée', '🔥 {n} полных дней подряд', '🔥 {n} أيام مكتملة متتالية'),
'wk.full':   ('ימים מלאים', 'full days', 'journées complètes', 'полных дней', 'أيام مكتملة'),
}
