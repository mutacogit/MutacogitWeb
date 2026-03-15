import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

menu_overlay = """
    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu" class="fixed inset-0 z-[100] bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl transform translate-x-full transition-transform duration-300 ease-in-out md:hidden flex flex-col justify-center items-center">
        <!-- Close Button -->
        <button id="mobile-menu-close" class="absolute top-6 right-6 text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white focus:outline-none p-2 transition-transform hover:rotate-90">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
        
        <div class="flex flex-col space-y-8 text-center w-full px-6">
            <a href="index.html" class="text-2xl font-serif tracking-wide text-gray-800 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Ana Sayfa</a>
            <a href="hakkimizda.html" class="text-2xl font-serif tracking-wide text-gray-800 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Hakkımızda</a>
            <a href="ekibimiz.html" class="text-2xl font-serif tracking-wide text-gray-800 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Ekibimiz</a>
            <a href="dukkan.html" class="text-2xl font-serif tracking-wide text-gray-800 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Dükkan</a>
            <a href="atolyelerimiz.html" class="text-2xl font-serif tracking-wide text-gray-800 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Atölyelerimiz</a>
            <a href="bize-ulasin.html" class="text-2xl font-serif tracking-wide text-gray-800 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Bize Ulaşın</a>
        </div>
    </div>
"""

menu_script = """
        // Mobile Menu Logic
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenuCloseBtn = document.getElementById('mobile-menu-close');
        const mobileMenu = document.getElementById('mobile-menu');

        if (mobileMenuBtn && mobileMenuCloseBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileMenu.classList.remove('translate-x-full');
                document.body.style.overflow = 'hidden'; // Prevent scrolling when menu is open
            });

            mobileMenuCloseBtn.addEventListener('click', () => {
                mobileMenu.classList.add('translate-x-full');
                document.body.style.overflow = '';
            });
            
            // Close menu when clicking on a link
            const mobileLinks = mobileMenu.querySelectorAll('a');
            mobileLinks.forEach(link => {
                link.addEventListener('click', () => {
                    mobileMenu.classList.add('translate-x-full');
                    document.body.style.overflow = '';
                });
            });
        }
"""

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the mobile button to have id="mobile-menu-btn"
    if 'id="mobile-menu-btn"' not in content:
        # Looking for button inside .md:hidden
        content = re.sub(
            r'(<div class="md:hidden[^>]*>\s*<button\s*)(class=")',
            r'\g<1>id="mobile-menu-btn" \g<2>',
            content
        )

    # 2. Add the mobile menu overlay after </nav>
    if 'id="mobile-menu"' not in content:
        content = content.replace('</nav>', '</nav>\n' + menu_overlay)
    
    # 3. Add script logic
    if 'Mobile Menu Logic' not in content:
        if '</script>' in content:
            # Find the last </script> tag
            parts = content.rsplit('</script>', 1)
            content = parts[0] + menu_script + '\n    </script>' + parts[1]
        else:
             content = content.replace('</body>', '<script>\n' + menu_script + '\n</script>\n</body>')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

for f in html_files:
    process_file(f)
    print(f"Processed {f}")

print("Done")
