
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Inter"', 'sans-serif'],      // Body Text
                display: ['"Plus Jakarta Sans"', 'sans-serif'], // Headings
            },
            animation: {
                'fade-in-up': 'fadeInUp 0.5s ease-out',
            },
            keyframes: {
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            }
        }
    }
}
