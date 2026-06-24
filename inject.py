import os
import re

domain = "example.com"
if os.path.exists("CNAME"):
    with open("CNAME") as f:
        domain = f.read().strip()
print("Domain:", domain)

ANALYTICS = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-E6ML8EDW0H"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-E6ML8EDW0H");</script>'
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8426936740213369" crossorigin="anonymous"></script>'

HEADER_CSS = '''
/* ––– PACDI Mobil Header Optimizasyonu ––– */
.site-header { transition: padding 0.3s, background 0.3s; }
@media (max-width: 640px) {
    .site-header { padding: 0.5rem 0.8rem !important; }
    .site-title { font-size: 0.9rem !important; }
    .site-title small { font-size: 0.5rem !important; display: inline !important; margin-left: 0.2rem; }
    .header-actions { gap: 0.3rem !important; }
    .pdf-btn, .theme-toggle { font-size: 0.6rem !important; padding: 0.2rem 0.5rem !important; }
    .lang-btn { font-size: 0.6rem !important; padding: 0.2rem 0.5rem !important; }
    #progress-bar { height: 3px !important; }
}
.site-header.shrink { padding: 0.3rem 0.8rem !important; background: rgba(50,50,118,0.95) !important; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.site-header.shrink .site-title { font-size: 0.85rem !important; }
.site-header.shrink .site-title small { font-size: 0.45rem !important; }
.site-header.shrink .pdf-btn, .site-header.shrink .theme-toggle, .site-header.shrink .lang-btn { font-size: 0.55rem !important; padding: 0.15rem 0.4rem !important; }
'''

HEADER_JS = '''
<script>
(function() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    var lastScrollY = 0;
    window.addEventListener('scroll', function() {
        var currentScrollY = window.scrollY;
        if (currentScrollY > 80) {
            header.classList.add('shrink');
        } else {
            header.classList.remove('shrink');
        }
        lastScrollY = currentScrollY;
    });
})();
</script>
'''

SKIP = ['legal.html', 'impressum.html', 'datenschutz.html', '404.html', 'master-template.html', 'test.html']
updated = 0

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', '.github']]
    for fname in files:
        if not fname.endswith('.html') or fname.startswith('google4d'):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if '</head>' not in content:
                continue

            orig = content
            relpath = fpath.replace('./', '').replace('.\\', '')
            if relpath == 'index.html':
                url = 'https://' + domain + '/'
            else:
                url = 'https://' + domain + '/' + relpath

            head_insert = ''
            if 'G-E6ML8EDW0H' not in content:
                head_insert += '    ' + ANALYTICS + '\n'
            if 'ca-pub-8426936740213369' not in content and fname not in SKIP:
                head_insert += '    ' + ADSENSE + '\n'
            if 'canonical' not in content:
                head_insert += '    <link rel="canonical" href="' + url + '" />\n'

            if 'PACDI Mobil Header Optimizasyonu' not in content:
                if '<style>' in content and '</style>' in content:
                    content = content.replace('</style>', HEADER_CSS + '\n</style>', 1)
                else:
                    head_insert += '    <style>\n' + HEADER_CSS + '    </style>\n'

            if head_insert:
                content = content.replace('</head>', head_insert + '</head>', 1)

            if 'header.classList.add' not in content:
                content = content.replace('</body>', HEADER_JS + '\n</body>', 1)

            if content != orig:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print('Updated:', fpath)

        except Exception as e:
            print('Error:', fpath, str(e))

print('Total updated:', updated)