// ============================================
// LENDFLOW — Global JavaScript
// ============================================

// --- Dark Mode (runs before Alpine to prevent FOUC) ---
(function() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }
})();

// --- Alpine.js Initialization ---
document.addEventListener('alpine:init', () => {

  // Theme Store
  Alpine.store('theme', {
    dark: document.documentElement.classList.contains('dark'),
    toggle() {
      this.dark = !this.dark;
      document.documentElement.classList.toggle('dark', this.dark);
      localStorage.setItem('theme', this.dark ? 'dark' : 'light');
    },
  });

  // Toast Notification Store
  Alpine.store('toasts', {
    items: [],
    show(title, type = 'info', message = '', duration = 5000) {
      const id = Date.now();
      this.items.push({ id, title, message, type, visible: true });
      if (duration > 0) {
        setTimeout(() => this.dismiss(id), duration);
      }
    },
    dismiss(id) {
      const item = this.items.find(t => t.id === id);
      if (item) item.visible = false;
      setTimeout(() => {
        this.items = this.items.filter(t => t.id !== id);
      }, 300);
    },
  });
});

// --- Global Helpers ---
window.showToast = (title, type, message) => {
  Alpine.store('toasts').show(title, type, message);
};

// --- Password Strength Calculator ---
window.passwordStrength = () => ({
  password: '',
  score: 0,
  label: '',
  color: '',

  calculate() {
    const p = this.password;
    let s = 0;
    if (p.length >= 8) s++;
    if (p.length >= 12) s++;
    if (/[a-z]/.test(p) && /[A-Z]/.test(p)) s++;
    if (/\d/.test(p)) s++;
    if (/[^a-zA-Z0-9]/.test(p)) s++;
    this.score = Math.min(s, 4);

    const levels = [
      { label: '', color: '' },
      { label: 'Weak', color: '#ef4444' },
      { label: 'Fair', color: '#f59e0b' },
      { label: 'Good', color: '#3b82f6' },
      { label: 'Strong', color: '#10b981' },
    ];
    this.label = levels[this.score].label;
    this.color = levels[this.score].color;
  },
});

// --- OTP Input Handler ---
window.otpInput = (length = 6) => ({
  digits: Array(length).fill(''),
  get code() { return this.digits.join(''); },
  get isComplete() { return this.digits.every(d => d !== ''); },

  handleInput(index, event) {
    const val = event.target.value.replace(/\D/g, '');
    this.digits[index] = val.charAt(0) || '';

    if (val && index < length - 1) {
      this.$nextTick(() => {
        const inputs = this.$el.querySelectorAll('input[data-otp]');
        inputs[index + 1]?.focus();
      });
    }
  },

  handleKeydown(index, event) {
    if (event.key === 'Backspace' && !this.digits[index] && index > 0) {
      const inputs = this.$el.querySelectorAll('input[data-otp]');
      inputs[index - 1]?.focus();
    }
  },

  handlePaste(event) {
    event.preventDefault();
    const text = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, length);
    text.split('').forEach((char, i) => {
      this.digits[i] = char;
    });
    const inputs = this.$el.querySelectorAll('input[data-otp]');
    const focusIndex = Math.min(text.length, length - 1);
    inputs[focusIndex]?.focus();
  },
});

// --- Countdown Timer ---
window.countdownTimer = (seconds = 60) => ({
  remaining: seconds,
  total: seconds,
  interval: null,
  get display() {
    const m = Math.floor(this.remaining / 60);
    const s = this.remaining % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  },
  get progress() {
    return ((this.total - this.remaining) / this.total) * 100;
  },
  get isExpired() { return this.remaining <= 0; },

  start() {
    this.remaining = this.total;
    clearInterval(this.interval);
    this.interval = setInterval(() => {
      this.remaining--;
      if (this.remaining <= 0) {
        clearInterval(this.interval);
      }
    }, 1000);
  },

  init() { this.start(); },
  destroy() { clearInterval(this.interval); },
});
