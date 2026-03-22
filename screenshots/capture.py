from playwright.sync_api import sync_playwright
import json

def capture_all():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        base = "https://iohel.com"
        out = "/home/joel/personal/projects/iohel.com/screenshots"

        configs = [
            ("homepage_desktop", base, 1440, 900, False),
            ("homepage_desktop_full", base, 1440, 900, True),
            ("homepage_mobile", base, 375, 812, False),
            ("homepage_mobile_full", base, 375, 812, True),
        ]

        # First pass: homepage at both sizes, collect links
        for name, url, w, h, full in configs:
            page = browser.new_page(viewport={'width': w, 'height': h})
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.screenshot(path=f"{out}/{name}.png", full_page=full)

            if name == "homepage_desktop":
                # Collect page info
                info = page.evaluate('''() => {
                    const h1 = document.querySelector('h1');
                    const nav = document.querySelector('nav');
                    const links = Array.from(document.querySelectorAll('a[href]')).map(a => ({
                        text: a.textContent.trim().substring(0, 50),
                        href: a.href
                    })).filter(l => l.href.startsWith(window.location.origin) && l.text);
                    const ctas = Array.from(document.querySelectorAll('a, button')).filter(el => {
                        const style = window.getComputedStyle(el);
                        return style.backgroundColor !== 'rgba(0, 0, 0, 0)' && style.backgroundColor !== 'transparent';
                    }).map(el => ({
                        tag: el.tagName,
                        text: el.textContent.trim().substring(0, 50),
                        href: el.href || ''
                    }));
                    const headings = Array.from(document.querySelectorAll('h1, h2, h3')).map(h => ({
                        tag: h.tagName,
                        text: h.textContent.trim().substring(0, 100),
                        top: h.getBoundingClientRect().top
                    }));
                    const fontSize = window.getComputedStyle(document.body).fontSize;
                    return {
                        title: document.title,
                        h1Text: h1 ? h1.textContent.trim() : null,
                        h1Top: h1 ? h1.getBoundingClientRect().top : null,
                        hasNav: !!nav,
                        navLinks: nav ? Array.from(nav.querySelectorAll('a')).map(a => a.textContent.trim()) : [],
                        links: links.slice(0, 30),
                        ctas: ctas,
                        headings: headings,
                        baseFontSize: fontSize,
                        viewportHeight: window.innerHeight,
                        bodyWidth: document.body.scrollWidth,
                    };
                }''')
                results['desktop_info'] = info

            if name == "homepage_mobile":
                info = page.evaluate('''() => {
                    const nav = document.querySelector('nav');
                    const hamburger = document.querySelector('[aria-label*="menu"], [aria-label*="Menu"], button.menu, .hamburger, [class*="mobile-menu"], [class*="burger"]');
                    return {
                        bodyScrollWidth: document.body.scrollWidth,
                        viewportWidth: window.innerWidth,
                        hasHorizontalScroll: document.body.scrollWidth > window.innerWidth,
                        hasHamburger: !!hamburger,
                        navVisible: nav ? window.getComputedStyle(nav).display !== 'none' : false,
                        h1Top: document.querySelector('h1') ? document.querySelector('h1').getBoundingClientRect().top : null,
                        baseFontSize: window.getComputedStyle(document.body).fontSize,
                        touchTargets: Array.from(document.querySelectorAll('a, button')).filter(el => {
                            const rect = el.getBoundingClientRect();
                            return rect.width > 0 && rect.height > 0 && (rect.width < 48 || rect.height < 48);
                        }).map(el => ({
                            tag: el.tagName,
                            text: el.textContent.trim().substring(0, 30),
                            width: Math.round(el.getBoundingClientRect().width),
                            height: Math.round(el.getBoundingClientRect().height),
                        })).slice(0, 10),
                    };
                }''')
                results['mobile_info'] = info

            page.close()

        # Find subpages to visit
        desktop_info = results.get('desktop_info', {})
        internal_links = desktop_info.get('links', [])

        # Pick interesting subpages
        subpages = []
        for link in internal_links:
            href = link['href']
            if href.rstrip('/') != base.rstrip('/') and '/posts/' in href or '/projects/' in href or '/archive' in href:
                subpages.append(href)
            if len(subpages) >= 2:
                break

        if not subpages:
            for link in internal_links:
                href = link['href']
                if href.rstrip('/') != base.rstrip('/'):
                    subpages.append(href)
                if len(subpages) >= 2:
                    break

        for i, url in enumerate(subpages):
            for suffix, w, h in [("desktop", 1440, 900), ("mobile", 375, 812)]:
                page = browser.new_page(viewport={'width': w, 'height': h})
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.screenshot(path=f"{out}/subpage{i+1}_{suffix}.png", full_page=False)

                if suffix == "desktop":
                    sub_info = page.evaluate('''() => {
                        return {
                            title: document.title,
                            url: window.location.href,
                            h1: document.querySelector('h1') ? document.querySelector('h1').textContent.trim().substring(0, 100) : null,
                            bodyScrollWidth: document.body.scrollWidth,
                        };
                    }''')
                    results[f'subpage{i+1}_info'] = sub_info
                page.close()

        browser.close()

    print(json.dumps(results, indent=2))

capture_all()
