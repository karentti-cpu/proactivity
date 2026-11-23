# -*- coding: utf-8 -*-
"""SVG icon sprite + CSS for the Proacty app."""

# Line icons, 24x24, stroke-based, currentColor. Replaces every emoji.
ICONS = {
'gear':     '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
'help':     '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
'home':     '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
'target':   '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
'activity': '<path d="M3 12h4l3 8 4-16 3 8h4"/>',
'brain':    '<path d="M12 5.5A3 3 0 0 0 6.5 7 3 3 0 0 0 5 12a3 3 0 0 0 1.5 5A3 3 0 0 0 12 18.5zM12 5.5A3 3 0 0 1 17.5 7 3 3 0 0 1 19 12a3 3 0 0 1-1.5 5A3 3 0 0 1 12 18.5z"/>',
'check':    '<path d="m4.5 12.5 5 5 10-11"/>',
'plus':     '<path d="M12 5v14M5 12h14"/>',
'trash':    '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
'camera':   '<path d="M4 8h3l1.5-2.5h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
'play':     '<path d="M8 5.5v13l11-6.5z"/>',
'clock':    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.5l3.5 2"/>',
'flame':    '<path d="M12 3s5 4.2 5 9a5 5 0 0 1-10 0c0-1.6.7-3 1.5-4 .2 1.3 1 2 1.8 2 1.2 0 1.7-1.1 1.7-3 0-1.6-.5-3-.5-4z"/>',
'star':     '<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9L3.5 9.7l5.9-.8z"/>',
'chevron':  '<path d="m9 5 7 7-7 7"/>',
'lock':     '<rect x="4.5" y="10" width="15" height="10.5" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
'x':        '<path d="M6 6l12 12M18 6 6 18"/>',
'edit':     '<path d="M4 20h4L18.5 9.5a2.1 2.1 0 0 0-3-3L5 17v3z"/><path d="m14 7 3 3"/>',
'book':     '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H19v18H5.5A1.5 1.5 0 0 1 4 19.5z"/><path d="M8 3v18"/>',
'users':    '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.2a3.5 3.5 0 0 1 0 5.6M17.5 14.4A6.5 6.5 0 0 1 21.5 20"/>',
'moon':     '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/>',
'wallet':   '<path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H18v3"/><rect x="3" y="7.5" width="18" height="12.5" rx="2"/><circle cx="16.5" cy="14" r="1.3"/>',
'apple':    '<path d="M12 8c-1-2-3-2.5-4.5-1.5C5.5 7.8 5 11 6.5 15c1 2.7 2.5 4.5 4 4.5.8 0 1-.5 1.5-.5s.7.5 1.5.5c1.5 0 3-1.8 4-4.5 1.5-4 1-7.2-1-8.5C15 5.5 13 6 12 8z"/><path d="M12 8V5.5A2.5 2.5 0 0 1 14.5 3"/>',
'palette':  '<path d="M12 3a9 9 0 0 0 0 18c1.2 0 1.8-.8 1.8-1.6 0-1.4-1.2-1.6-1.2-2.6 0-.8.7-1.3 1.7-1.3H16a5 5 0 0 0 5-5c0-4.1-4-7.5-9-7.5z"/><circle cx="7.5" cy="11" r="1.1"/><circle cx="10.5" cy="7.5" r="1.1"/><circle cx="15" cy="8.5" r="1.1"/>',
'shield':   '<path d="M12 3 5 6v6c0 4.2 2.9 7.6 7 9 4.1-1.4 7-4.8 7-9V6z"/>',
'trending': '<path d="M3 16.5 9 10l4 4 8-8"/><path d="M15 6h6v6"/>',
'sparkles': '<path d="m12 3 1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15.5 19.4 18l2.5.9-2.5.9-.9 2.5-.9-2.5-2.5-.9 2.5-.9z"/>',
'compass':  '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5.2-5.2 2 2-5.2z"/>',
'sun':      '<circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M19.1 4.9l-1.8 1.8M6.7 17.3l-1.8 1.8"/>',
'sliders':  '<path d="M4 8h10M18 8h2M4 16h4M12 16h8"/><circle cx="16" cy="8" r="2"/><circle cx="10" cy="16" r="2"/>',
'seedling': '<path d="M12 21v-8"/><path d="M12 13C12 9 9 6.5 4.5 6.5 4.5 11 7.5 13 12 13z"/><path d="M12 13c0-3.3 2.5-5.5 6.5-5.5 0 3.8-2.5 5.5-6.5 5.5z"/>',
'ruler':    '<rect x="2.5" y="8" width="19" height="8" rx="1.5"/><path d="M7 8v3M11 8v4M15 8v3M19 8v4"/>',
'rocket':   '<path d="M12 3c3.5 2 5.5 5.5 5.5 9.5L14 16h-4l-3.5-3.5C6.5 8.5 8.5 5 12 3z"/><circle cx="12" cy="10" r="1.8"/><path d="M10 16.5 8 21l3.2-1.6M14 16.5 16 21l-3.2-1.6"/>',
'drop':     '<path d="M12 3.5C12 3.5 6 10 6 14a6 6 0 0 0 12 0c0-4-6-10.5-6-10.5z"/>',
'shirt':    '<path d="M8 3 4 5.5 6 10l2-1v11h8V9l2 1 2-4.5L16 3a4 4 0 0 1-8 0z"/>',
'wind':     '<path d="M3 8h10a3 3 0 1 0-3-3"/><path d="M3 12h15a3 3 0 1 1-3 3"/><path d="M3 16h6"/>',
'zap':      '<path d="M13 3 5 13.5h6L11 21l8-10.5h-6z"/>',
'gem':      '<path d="m5 4 -2.5 5L12 21 21.5 9 19 4z"/><path d="M2.5 9h19M8.5 4 12 21 15.5 4"/>',
'gauge':    '<path d="M4.5 17a8.5 8.5 0 1 1 15 0"/><path d="m12 12 4-3"/><circle cx="12" cy="13" r="1.3"/>',
'arrow':    '<path d="M5 12h14M13 6l6 6-6 6"/>',
'user':     '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
'refresh':  '<path d="M20 11a8 8 0 0 0-14-4.5L4 9"/><path d="M4 4v5h5"/><path d="M4 13a8 8 0 0 0 14 4.5L20 15"/><path d="M20 20v-5h-5"/>',
'flag':     '<path d="M5 21V4"/><path d="M5 5h11l-2 3.5L16 12H5z"/>',
'image':    '<rect x="3" y="4.5" width="18" height="15" rx="2"/><circle cx="8.5" cy="10" r="1.7"/><path d="m4 17 5-4.5 4 3.5 3-2.5 4 3.5"/>',
'globe':    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 3.8 5.7 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/>',
'dumbbell': '<path d="M3 9.5v5M6 7.5v9M18 7.5v9M21 9.5v5M6 12h12"/>',
'face':     '<circle cx="12" cy="12" r="9"/><path d="M9 10h.01M15 10h.01"/><path d="M8.8 14.5a4.2 4.2 0 0 0 6.4 0"/>',
'fridge':   '<rect x="5.5" y="2.5" width="13" height="19" rx="2"/><path d="M5.5 10h13"/><path d="M8.5 6.5v1.5M8.5 12.5V15"/>',
'chef':     '<path d="M7 21h10v-4H7z"/><path d="M7 17c-2.2 0-4-1.8-4-4a3.5 3.5 0 0 1 3-3.5A4 4 0 0 1 12 5a4 4 0 0 1 6 4.5A3.5 3.5 0 0 1 21 13c0 2.2-1.8 4-4 4"/>',
'link':     '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.5 1.5"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.5-1.5"/>',
'share':    '<circle cx="18" cy="5.5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="18.5" r="2.5"/><path d="m8.2 10.8 7.6-4.1M8.2 13.2l7.6 4.1"/>',
'copy':     '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/>',
'gift':     '<rect x="3.5" y="9" width="17" height="11" rx="1.5"/><path d="M3.5 13h17M12 9v11M12 9c-2-4-6-4-6-1.5S10 9 12 9zm0 0c2-4 6-4 6-1.5S14 9 12 9z"/>',
}

# Paint servers for the avatar. They live in the sprite so every avatar on the
# page shares one definition; the aura reads the accent through the cascade.
DEFS = (
    '<linearGradient id="av-metal" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#DCE2EB"/><stop offset="1" stop-color="#78838F"/></linearGradient>'
    '<radialGradient id="av-aura">'
    '<stop offset="0" style="stop-color:var(--acc);stop-opacity:.6"/>'
    '<stop offset=".55" style="stop-color:var(--acc);stop-opacity:.2"/>'
    '<stop offset="1" style="stop-color:var(--acc);stop-opacity:0"/></radialGradient>'
)

def sprite():
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" '
             'style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">',
             '<defs>' + DEFS + '</defs>']
    for name, body in ICONS.items():
        parts.append(
            f'<symbol id="i-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{body}</symbol>')
    parts.append('</svg>')
    return ''.join(parts)
