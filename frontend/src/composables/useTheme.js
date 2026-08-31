import { ref, watch, onMounted, onUnmounted } from 'vue';

const getInitialTheme = () => {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('theme');
    if (stored === 'dark' || stored === 'light') {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  return 'light';
};

const theme = ref(getInitialTheme());

export function useTheme() {
  const isDarkMode = ref(theme.value === 'dark');

  const applyTheme = (newTheme) => {
    if (typeof document === 'undefined') return;
    const root = document.documentElement;
    root.classList.toggle('dark', newTheme === 'dark');
    root.dataset.theme = newTheme;
    root.style.colorScheme = newTheme;
    localStorage.setItem('theme', newTheme);
    isDarkMode.value = newTheme === 'dark';
  };

  watch(theme, (newVal) => {
    applyTheme(newVal);
  }, { immediate: true });

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
  };

  const setTheme = (val) => {
    if (val === 'dark' || val === 'light') {
      theme.value = val;
    }
  };

  onMounted(() => {
    if (typeof window === 'undefined') return;
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleSystemChange = (e) => {
      const stored = localStorage.getItem('theme');
      if (!stored) {
        theme.value = e.matches ? 'dark' : 'light';
      }
    };

    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleSystemChange);
    } else {
      mediaQuery.addListener(handleSystemChange);
    }
  });

  return {
    theme,
    isDarkMode,
    toggleTheme,
    setTheme,
  };
}
