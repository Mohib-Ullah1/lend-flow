# Frontend Implementation Guide — White-Label Digital Lending Platform

> **Stack**: Django Templates + HTMX 2.0 + Alpine.js 3 + Tailwind CSS 3.4 + Chart.js 4 + D3.js + Lottie
> **Design Philosophy**: Glass-morphic, depth-layered, cinematic micro-interactions, editorial typography
> **Target**: 60fps animations, Lighthouse 95+, WCAG 2.2 AA, sub-1s FCP

---

## Table of Contents

1. [Design Philosophy & Visual Language](#1-design-philosophy--visual-language)
2. [Architecture Overview](#2-architecture-overview)
3. [Project Structure (Extended)](#3-project-structure-extended)
4. [Advanced Design System (Tailwind)](#4-advanced-design-system-tailwind)
5. [Premium CSS Foundation](#5-premium-css-foundation)
6. [Component Library (30+ Components)](#6-component-library-30-components)
7. [Layout System (Glass-Morphic)](#7-layout-system-glass-morphic)
8. [Auth Pages (Cinematic)](#8-auth-pages-cinematic)
9. [Borrower Portal (Trust-First)](#9-borrower-portal-trust-first)
10. [Admin Dashboard (Command Center)](#10-admin-dashboard-command-center)
11. [Investor Portal (Data-Dense)](#11-investor-portal-data-dense)
12. [Command Palette (Cmd+K)](#12-command-palette-cmdk)
13. [Advanced HTMX Patterns](#13-advanced-htmx-patterns)
14. [Alpine.js Advanced Patterns](#14-alpinejs-advanced-patterns)
15. [Charts & Data Visualization (Premium)](#15-charts--data-visualization-premium)
16. [Micro-Interactions & Animation System](#16-micro-interactions--animation-system)
17. [White-Label Theming Engine](#17-white-label-theming-engine)
18. [Advanced Forms & Validation](#18-advanced-forms--validation)
19. [Real-Time Engine (WebSockets + SSE)](#19-real-time-engine-websockets--sse)
20. [Notification Center](#20-notification-center)
21. [Responsive & Mobile-Native Feel](#21-responsive--mobile-native-feel)
22. [Accessibility (WCAG 2.2 AA)](#22-accessibility-wcag-22-aa)
23. [Performance & Core Web Vitals](#23-performance--core-web-vitals)
24. [Implementation Phases](#24-implementation-phases)

---

## 1. Design Philosophy & Visual Language

### Core Aesthetic: "Quiet Luxury Fintech"

Think Linear.app meets Mercury.com — ultra-clean surfaces, deliberate whitespace, subtle depth through layered glass effects, and typography that breathes confidence.

### Visual Principles

| Principle | Implementation |
|-----------|---------------|
| **Depth via Layers** | Glass-morphic cards with `backdrop-blur`, layered shadows, subtle borders with opacity |
| **Motion with Purpose** | Every animation communicates state change; never decorative-only |
| **Data Density without Clutter** | Generous padding, monospace numbers, sparkline micro-charts inline |
| **Trust Through Polish** | Smooth 60fps transitions, no layout shift, pixel-perfect alignment |
| **Editorial Typography** | Large display headings (tracking-tight), small muted labels, clear hierarchy |
| **Color Restraint** | Neutral canvas, brand color used sparingly for actions and accents only |
| **Grain & Texture** | Subtle noise overlay on hero sections for tactile depth |
| **Gradient Mesh** | Soft multi-stop gradients for backgrounds and hero areas |

### Inspiration Reference

```
Mercury.com     — Clean banking dashboard, monospace numbers, trust
Linear.app      — Glass sidebar, command palette, keyboard-first
Stripe Dashboard — Data density, beautiful charts, micro-interactions
Vercel          — Dark mode excellence, gradient mesh, typography
Raycast         — Command palette UX, snappy animations
```

---

## 2. Architecture Overview

### Why Django Templates + HTMX (Not a SPA)?

| Concern | Our Approach |
|---------|-------------|
| **Speed** | Server-rendered HTML = instant first paint, no JS bundle bloat |
| **Interactivity** | HTMX for AJAX partials, Alpine.js for client-side state |
| **SEO** | Full SSR out of the box |
| **Complexity** | No build step for JS, no API duplication, no state management |
| **Real-time** | Django Channels WebSockets + Server-Sent Events for live updates |
| **Charts** | Chart.js 4 + D3.js loaded on-demand per page |
| **Animations** | CSS-first with Lottie for complex illustrations |

### Request Flow

```
Browser Request
    → Django View (full page or HTMX partial)
        → Template (base layout + blocks)
            → Tailwind CSS (design tokens via CSS custom properties)
            → HTMX 2.0 (partials, forms, infinite scroll, polling)
            → Alpine.js 3 (modals, tabs, command palette, local state)
            → Chart.js 4 / D3.js (data viz, loaded per-page)
            → WebSocket (real-time: activity feed, notifications, status)
            → View Transitions API (smooth page navigations)
```

---

## 3. Project Structure (Extended)

```
templates/
├── base/
│   ├── _base.html                     # Root: <html>, meta, fonts, scripts
│   ├── _base_borrower.html            # Borrower: centered layout, bottom nav
│   ├── _base_admin.html               # Admin: glass sidebar + topbar
│   ├── _base_investor.html            # Investor: data-dense layout
│   └── _base_auth.html               # Auth: split-screen cinematic
├── components/
│   ├── buttons/
│   │   ├── _primary.html              # Gradient + glow hover
│   │   ├── _secondary.html            # Ghost with border
│   │   ├── _danger.html               # Red destructive
│   │   ├── _icon_button.html          # Circle icon
│   │   ├── _button_group.html         # Segmented control
│   │   └── _loading_button.html       # Spinner state
│   ├── cards/
│   │   ├── _stat_card.html            # KPI with sparkline + trend
│   │   ├── _stat_card_glass.html      # Glass-morphic variant
│   │   ├── _loan_card.html            # Loan summary with progress ring
│   │   ├── _profile_card.html         # Avatar + info
│   │   ├── _metric_card.html          # Large number + subtitle
│   │   └── _feature_card.html         # Icon + title + desc
│   ├── forms/
│   │   ├── _text_input.html           # Floating label variant
│   │   ├── _select.html               # Custom styled
│   │   ├── _combobox.html             # Searchable dropdown
│   │   ├── _file_upload.html          # Drag & drop with preview
│   │   ├── _date_picker.html          # Calendar popup
│   │   ├── _currency_input.html       # $ prefix, auto-format
│   │   ├── _phone_input.html          # Country code + mask
│   │   ├── _toggle.html               # iOS-style switch
│   │   ├── _radio_cards.html          # Card-style radio group
│   │   ├── _range_slider.html         # Dual-thumb range
│   │   ├── _otp_input.html            # 6-digit MFA code
│   │   └── _form_section.html         # Grouped fields with header
│   ├── tables/
│   │   ├── _data_table.html           # Full-featured: sort, filter, select
│   │   ├── _table_pagination.html     # Cursor-based
│   │   ├── _table_filters.html        # Dropdown filters bar
│   │   ├── _expandable_row.html       # Click-to-expand detail
│   │   └── _table_empty.html          # Illustrated empty state
│   ├── feedback/
│   │   ├── _toast.html                # Slide-in notification
│   │   ├── _alert_banner.html         # Full-width info bar
│   │   ├── _empty_state.html          # Illustration + CTA
│   │   ├── _loading_spinner.html      # Branded spinner
│   │   ├── _skeleton.html             # Shimmer loader
│   │   ├── _progress_bar.html         # Animated fill
│   │   ├── _progress_ring.html        # SVG circular progress
│   │   ├── _confetti.html             # Celebration on approval
│   │   └── _count_up.html            # Animated number counter
│   ├── navigation/
│   │   ├── _sidebar.html              # Glass sidebar with sections
│   │   ├── _sidebar_item.html         # Nav item with active indicator
│   │   ├── _topbar.html               # Sticky top bar
│   │   ├── _breadcrumbs.html          # Slash-separated
│   │   ├── _mobile_nav.html           # Bottom tab bar
│   │   ├── _tab_nav.html              # Underline tabs
│   │   ├── _pill_tabs.html            # Pill-style tabs
│   │   └── _command_palette.html      # Cmd+K search
│   ├── modals/
│   │   ├── _modal.html                # Glass modal with backdrop blur
│   │   ├── _drawer.html               # Slide-in side panel
│   │   ├── _confirm_dialog.html       # Destructive confirm
│   │   └── _lightbox.html             # Image/document preview
│   ├── badges/
│   │   ├── _status_badge.html         # Dot + label
│   │   ├── _risk_badge.html           # Grade with color ring
│   │   ├── _count_badge.html          # Notification count
│   │   └── _tag.html                  # Removable tag
│   ├── charts/
│   │   ├── _sparkline.html            # Inline mini chart
│   │   ├── _area_chart.html           # Gradient area
│   │   ├── _bar_chart.html            # Rounded bars
│   │   ├── _donut_chart.html          # With center label
│   │   ├── _gauge_chart.html          # Semi-circle gauge
│   │   ├── _heatmap.html             # Calendar heatmap (D3)
│   │   └── _funnel_chart.html         # Conversion funnel
│   ├── data/
│   │   ├── _key_value.html            # Label: Value pair
│   │   ├── _definition_list.html      # dl/dt/dd styled
│   │   ├── _timeline.html             # Vertical event timeline
│   │   └── _comparison_bar.html       # Horizontal stacked bar
│   └── layout/
│       ├── _page_header.html          # Title + subtitle + actions
│       ├── _section.html              # Card wrapper with header
│       ├── _split_view.html           # 2/3 + 1/3 layout
│       └── _grid_container.html       # Responsive grid wrapper
├── borrower/
│   ├── onboarding/
│   │   ├── step1_personal.html
│   │   ├── step2_employment.html
│   │   ├── step3_documents.html
│   │   ├── step4_review.html
│   │   ├── _progress_stepper.html     # Vertical stepper variant
│   │   └── _success.html             # Celebration with Lottie
│   ├── dashboard.html
│   ├── applications/
│   │   ├── new.html                   # Multi-step application
│   │   ├── detail.html                # Status tracker
│   │   └── list.html
│   ├── loans/
│   │   ├── detail.html                # With repayment timeline
│   │   ├── list.html
│   │   └── _payment_modal.html
│   ├── payments/
│   │   ├── schedule.html              # Visual calendar view
│   │   └── history.html
│   └── profile/
│       ├── settings.html
│       └── documents.html
├── admin/
│   ├── dashboard.html                 # Command center
│   ├── applications/
│   │   ├── list.html                  # Kanban + table toggle
│   │   ├── detail.html                # Full review workspace
│   │   ├── _review_panel.html         # Side panel for quick review
│   │   ├── _kanban_board.html         # Drag-and-drop columns
│   │   └── _bulk_actions.html
│   ├── borrowers/
│   │   ├── list.html
│   │   ├── detail.html                # 360-degree borrower view
│   │   └── _risk_profile.html
│   ├── loans/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── _restructure_modal.html
│   ├── collections/
│   │   ├── queue.html                 # Priority-sorted
│   │   ├── borrower_timeline.html     # Full contact history
│   │   └── _action_panel.html
│   ├── ledger/
│   │   ├── journal_entries.html
│   │   ├── reconciliation.html
│   │   └── _entry_detail.html
│   ├── reports/
│   │   ├── index.html
│   │   ├── _report_builder.html       # Visual report config
│   │   └── _scheduled_reports.html
│   └── settings/
│       ├── institution.html
│       ├── products.html              # Visual product builder
│       ├── workflows.html             # Flow diagram editor
│       ├── users.html
│       ├── branding.html              # Live theme preview
│       └── webhooks.html
├── investor/
│   ├── dashboard.html                 # Portfolio overview
│   ├── portfolio/
│   │   ├── overview.html
│   │   ├── performance.html           # Time-series analysis
│   │   └── diversification.html       # Allocation charts
│   ├── marketplace.html               # Browse loans to invest
│   ├── reports.html
│   └── _investment_modal.html
└── auth/
    ├── login.html                     # Split-screen + mesh gradient
    ├── register.html
    ├── forgot_password.html
    ├── reset_password.html
    ├── mfa_setup.html
    ├── mfa_verify.html
    └── _social_buttons.html

static/
├── css/
│   ├── tailwind.css                   # Tailwind input + custom layers
│   ├── premium.css                    # Grain textures, glass effects, mesh gradients
│   └── dist/
│       └── styles.css                 # Compiled + purged output
├── js/
│   ├── app.js                         # Alpine.js stores + global init
│   ├── htmx-config.js                # HTMX extensions + error handling
│   ├── command-palette.js             # Cmd+K implementation
│   ├── view-transitions.js            # Page transition orchestrator
│   ├── charts/
│   │   ├── chart-theme.js             # Shared chart config + dark mode
│   │   ├── dashboard-charts.js
│   │   ├── portfolio-charts.js
│   │   ├── sparkline.js               # Inline sparklines
│   │   └── heatmap.js                # D3 calendar heatmap
│   ├── websocket.js                   # WS connection manager + reconnect
│   └── utils/
│       ├── currency.js                # Format + parse currency
│       ├── dates.js                   # Relative time + format
│       ├── count-up.js               # Animated number counter
│       └── confetti.js               # Celebration particles
├── lottie/
│   ├── success.json                   # Checkmark animation
│   ├── loading.json                   # Branded loader
│   ├── empty-state.json              # No data illustration
│   └── onboarding-complete.json      # Celebration
├── images/
│   ├── logo.svg
│   ├── logo-mark.svg                 # Icon-only version
│   ├── noise.png                     # Grain texture (64x64, tiled)
│   ├── mesh-gradient-light.webp      # Auth page background
│   ├── mesh-gradient-dark.webp
│   ├── illustrations/
│   │   ├── onboarding.svg
│   │   ├── empty-loans.svg
│   │   ├── approved.svg
│   │   └── investment.svg
│   └── icons/                         # Custom SVG icon set
└── fonts/
    ├── Inter-Variable.woff2          # Primary UI font
    └── JetBrainsMono-Variable.woff2  # Monospace for numbers
```

---

## 4. Advanced Design System (Tailwind)

### tailwind.config.js

```js
const defaultTheme = require('tailwindcss/defaultTheme')
const plugin = require('tailwindcss/plugin')

module.exports = {
  content: ['./templates/**/*.html', './static/js/**/*.js'],
  darkMode: 'class',
  theme: {
    extend: {
      // === COLORS ===
      colors: {
        brand: {
          50:  'var(--color-brand-50,  #f0f5ff)',
          100: 'var(--color-brand-100, #e0eaff)',
          200: 'var(--color-brand-200, #c7d7fe)',
          300: 'var(--color-brand-300, #a4bcfd)',
          400: 'var(--color-brand-400, #8098f9)',
          500: 'var(--color-brand-500, #6172f3)',
          600: 'var(--color-brand-600, #444ce7)',
          700: 'var(--color-brand-700, #3538cd)',
          800: 'var(--color-brand-800, #2d31a6)',
          900: 'var(--color-brand-900, #2b2f83)',
          950: 'var(--color-brand-950, #1f235b)',
        },
        surface: {
          DEFAULT: 'var(--surface)',
          secondary: 'var(--surface-secondary)',
          tertiary: 'var(--surface-tertiary)',
          elevated: 'var(--surface-elevated)',
          glass: 'var(--surface-glass)',
          'glass-heavy': 'var(--surface-glass-heavy)',
        },
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
          inverted: 'var(--text-inverted)',
        },
        border: {
          DEFAULT: 'var(--border)',
          strong: 'var(--border-strong)',
          subtle: 'var(--border-subtle)',
        },
        success: {
          50: '#ecfdf5', 100: '#d1fae5', 200: '#a7f3d0',
          500: '#10b981', 600: '#059669', 700: '#047857',
        },
        warning: {
          50: '#fffbeb', 100: '#fef3c7', 200: '#fde68a',
          500: '#f59e0b', 600: '#d97706', 700: '#b45309',
        },
        danger: {
          50: '#fef2f2', 100: '#fee2e2', 200: '#fecaca',
          500: '#ef4444', 600: '#dc2626', 700: '#b91c1c',
        },
      },

      // === TYPOGRAPHY ===
      fontFamily: {
        sans: ['InterVariable', 'Inter', ...defaultTheme.fontFamily.sans],
        mono: ['JetBrains Mono Variable', 'JetBrains Mono', ...defaultTheme.fontFamily.mono],
        display: ['InterVariable', 'Inter', ...defaultTheme.fontFamily.sans],
      },
      fontSize: {
        '2xs':     ['0.625rem', { lineHeight: '1rem' }],
        'display': ['3.5rem',   { lineHeight: '1.1', letterSpacing: '-0.04em', fontWeight: '700' }],
        'h1':      ['2.25rem',  { lineHeight: '1.2', letterSpacing: '-0.03em', fontWeight: '700' }],
        'h2':      ['1.75rem',  { lineHeight: '1.25', letterSpacing: '-0.02em', fontWeight: '600' }],
        'h3':      ['1.25rem',  { lineHeight: '1.4', letterSpacing: '-0.01em', fontWeight: '600' }],
      },
      letterSpacing: {
        'display': '-0.04em',
        'heading': '-0.02em',
      },

      // === SHADOWS (Layered for Depth) ===
      boxShadow: {
        'xs':       '0 1px 2px 0 rgb(0 0 0 / 0.03)',
        'card':     '0 1px 2px rgb(0 0 0 / 0.04), 0 1px 3px rgb(0 0 0 / 0.03)',
        'card-hover': '0 4px 8px -2px rgb(0 0 0 / 0.06), 0 2px 4px -2px rgb(0 0 0 / 0.04)',
        'elevated': '0 8px 24px -4px rgb(0 0 0 / 0.08), 0 2px 8px -2px rgb(0 0 0 / 0.04)',
        'float':    '0 12px 32px -8px rgb(0 0 0 / 0.12), 0 4px 12px -4px rgb(0 0 0 / 0.06)',
        'modal':    '0 24px 48px -12px rgb(0 0 0 / 0.18), 0 8px 16px -8px rgb(0 0 0 / 0.08)',
        'glow':     '0 0 20px -5px var(--color-brand-500)',
        'glow-lg':  '0 0 40px -10px var(--color-brand-500)',
        'inner-ring': 'inset 0 0 0 1px var(--border-subtle)',
      },

      // === BORDER RADIUS ===
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.25rem',
        '4xl': '1.5rem',
      },

      // === BACKDROP BLUR ===
      backdropBlur: {
        'xs': '2px',
        'glass': '12px',
        'heavy': '24px',
      },

      // === ANIMATIONS ===
      animation: {
        'fade-in':       'fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'fade-up':       'fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        'fade-down':     'fadeDown 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'scale-in':      'scaleIn 0.2s cubic-bezier(0.16, 1, 0.3, 1)',
        'scale-up':      'scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-in-right':'slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-in-left': 'slideInLeft 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-in-bottom':'slideInBottom 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'shimmer':       'shimmer 2s ease-in-out infinite',
        'pulse-soft':    'pulseSoft 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow':     'spin 3s linear infinite',
        'bounce-subtle': 'bounceSubtle 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'gradient-shift':'gradientShift 8s ease infinite',
        'count-up':      'countUp 0.8s cubic-bezier(0.16, 1, 0.3, 1)',
        'draw-line':     'drawLine 0.6s ease-out forwards',
        'progress-fill': 'progressFill 1s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'glow-pulse':    'glowPulse 2s ease-in-out infinite',
        'float':         'float 6s ease-in-out infinite',
      },
      keyframes: {
        fadeIn:         { from: { opacity: '0' }, to: { opacity: '1' } },
        fadeUp:         { from: { opacity: '0', transform: 'translateY(12px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        fadeDown:       { from: { opacity: '0', transform: 'translateY(-8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        scaleIn:        { from: { opacity: '0', transform: 'scale(0.95)' }, to: { opacity: '1', transform: 'scale(1)' } },
        scaleUp:        { from: { opacity: '0', transform: 'scale(0.9)' }, to: { opacity: '1', transform: 'scale(1)' } },
        slideInRight:   { from: { opacity: '0', transform: 'translateX(16px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
        slideInLeft:    { from: { opacity: '0', transform: 'translateX(-16px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
        slideInBottom:  { from: { opacity: '0', transform: 'translateY(100%)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        shimmer:        { '0%, 100%': { backgroundPosition: '-200% 0' }, '50%': { backgroundPosition: '200% 0' } },
        pulseSoft:      { '0%, 100%': { opacity: '1' }, '50%': { opacity: '0.7' } },
        bounceSubtle:   { '0%': { transform: 'scale(1)' }, '50%': { transform: 'scale(1.05)' }, '100%': { transform: 'scale(1)' } },
        gradientShift:  { '0%, 100%': { backgroundPosition: '0% 50%' }, '50%': { backgroundPosition: '100% 50%' } },
        drawLine:       { from: { 'stroke-dashoffset': '100%' }, to: { 'stroke-dashoffset': '0' } },
        progressFill:   { from: { width: '0%' }, to: { width: 'var(--progress)' } },
        glowPulse:      { '0%, 100%': { boxShadow: '0 0 20px -5px var(--color-brand-500)' }, '50%': { boxShadow: '0 0 30px -2px var(--color-brand-400)' } },
        float:          { '0%, 100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-10px)' } },
      },

      // === SPACING ===
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '100': '25rem',
        '112': '28rem',
        '128': '32rem',
      },

      // === Z-INDEX ===
      zIndex: {
        'dropdown': '50',
        'sticky': '100',
        'modal-backdrop': '200',
        'modal': '210',
        'command-palette': '300',
        'toast': '400',
      },
    },
  },

  plugins: [
    require('@tailwindcss/forms')({ strategy: 'class' }),
    require('@tailwindcss/typography'),

    // Custom utility classes
    plugin(function({ addUtilities, addComponents }) {
      addUtilities({
        '.text-balance': { 'text-wrap': 'balance' },
        '.text-pretty':  { 'text-wrap': 'pretty' },
        '.gpu':          { transform: 'translateZ(0)', 'will-change': 'transform' },
        '.no-scrollbar':  { '-ms-overflow-style': 'none', 'scrollbar-width': 'none', '&::-webkit-scrollbar': { display: 'none' } },
        '.mask-fade-b':  { 'mask-image': 'linear-gradient(to bottom, black 80%, transparent)' },
        '.font-tabular': { 'font-variant-numeric': 'tabular-nums' },
      })
    }),
  ],
}
```

---

## 5. Premium CSS Foundation

### static/css/tailwind.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ============================================
   DESIGN TOKENS (CSS Custom Properties)
   ============================================ */

@layer base {

  /* --- LIGHT MODE --- */
  :root {
    /* Surfaces */
    --surface:            #ffffff;
    --surface-secondary:  #fafafa;
    --surface-tertiary:   #f5f5f4;
    --surface-elevated:   #ffffff;
    --surface-glass:      rgba(255, 255, 255, 0.72);
    --surface-glass-heavy: rgba(255, 255, 255, 0.88);

    /* Text */
    --text-primary:   #0a0a0a;
    --text-secondary: #525252;
    --text-muted:     #a3a3a3;
    --text-inverted:  #fafafa;

    /* Borders */
    --border:        rgba(0, 0, 0, 0.06);
    --border-strong: rgba(0, 0, 0, 0.12);
    --border-subtle: rgba(0, 0, 0, 0.03);

    /* Misc */
    --ring-color: var(--color-brand-500, #6172f3);
    --shadow-color: 0deg 0% 0%;
    --grain-opacity: 0.03;
    --mesh-opacity: 0.4;
  }

  /* --- DARK MODE --- */
  .dark {
    --surface:            #09090b;
    --surface-secondary:  #111113;
    --surface-tertiary:   #1a1a1e;
    --surface-elevated:   #18181b;
    --surface-glass:      rgba(9, 9, 11, 0.72);
    --surface-glass-heavy: rgba(9, 9, 11, 0.88);

    --text-primary:   #fafafa;
    --text-secondary: #a1a1aa;
    --text-muted:     #52525b;
    --text-inverted:  #09090b;

    --border:        rgba(255, 255, 255, 0.06);
    --border-strong: rgba(255, 255, 255, 0.12);
    --border-subtle: rgba(255, 255, 255, 0.03);

    --grain-opacity: 0.02;
    --mesh-opacity: 0.3;
  }

  /* --- BASE RESETS --- */
  *, *::before, *::after {
    border-color: var(--border);
  }

  html {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    scroll-behavior: smooth;
  }

  body {
    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
    background: var(--surface-secondary);
    color: var(--text-primary);
  }

  /* Tabular numbers for financial data */
  .font-mono, [data-financial] {
    font-variant-numeric: tabular-nums;
    font-feature-settings: 'tnum';
  }

  /* Selection color */
  ::selection {
    background: var(--color-brand-200, #c7d7fe);
    color: var(--color-brand-900, #2b2f83);
  }
  .dark ::selection {
    background: var(--color-brand-800, #2d31a6);
    color: var(--color-brand-100, #e0eaff);
  }
}

/* ============================================
   PREMIUM EFFECTS
   ============================================ */

@layer components {

  /* Grain texture overlay */
  .grain::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url('/static/images/noise.png');
    background-repeat: repeat;
    background-size: 128px;
    opacity: var(--grain-opacity);
    pointer-events: none;
    z-index: 9999;
    mix-blend-mode: overlay;
  }

  /* Glass card */
  .glass {
    background: var(--surface-glass);
    backdrop-filter: blur(12px) saturate(1.5);
    -webkit-backdrop-filter: blur(12px) saturate(1.5);
    border: 1px solid var(--border);
  }

  .glass-heavy {
    background: var(--surface-glass-heavy);
    backdrop-filter: blur(24px) saturate(1.8);
    -webkit-backdrop-filter: blur(24px) saturate(1.8);
    border: 1px solid var(--border-strong);
  }

  /* Gradient mesh background */
  .mesh-gradient {
    background:
      radial-gradient(ellipse at 20% 50%, var(--color-brand-100, #e0eaff) 0%, transparent 50%),
      radial-gradient(ellipse at 80% 20%, rgba(167, 139, 250, 0.15) 0%, transparent 40%),
      radial-gradient(ellipse at 40% 80%, rgba(52, 211, 153, 0.1) 0%, transparent 40%),
      var(--surface-secondary);
  }
  .dark .mesh-gradient {
    background:
      radial-gradient(ellipse at 20% 50%, rgba(97, 114, 243, 0.08) 0%, transparent 50%),
      radial-gradient(ellipse at 80% 20%, rgba(167, 139, 250, 0.06) 0%, transparent 40%),
      radial-gradient(ellipse at 40% 80%, rgba(52, 211, 153, 0.04) 0%, transparent 40%),
      var(--surface-secondary);
  }

  /* Glow button */
  .btn-glow {
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
  }
  .btn-glow::before {
    content: '';
    position: absolute;
    inset: -1px;
    background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-600), var(--color-brand-400));
    border-radius: inherit;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s;
    filter: blur(8px);
  }
  .btn-glow:hover::before {
    opacity: 0.6;
  }

  /* Shimmer skeleton */
  .skeleton {
    background: linear-gradient(
      90deg,
      var(--surface-tertiary) 25%,
      var(--surface-secondary) 37%,
      var(--surface-tertiary) 63%
    );
    background-size: 400% 100%;
    animation: shimmer 1.8s ease-in-out infinite;
    border-radius: 0.5rem;
  }

  /* Inner glow border (premium card effect) */
  .inner-glow {
    box-shadow:
      inset 0 1px 0 0 rgba(255, 255, 255, 0.05),
      0 1px 2px rgba(0, 0, 0, 0.04),
      0 1px 3px rgba(0, 0, 0, 0.03);
  }
  .dark .inner-glow {
    box-shadow:
      inset 0 1px 0 0 rgba(255, 255, 255, 0.03),
      0 1px 2px rgba(0, 0, 0, 0.2),
      0 1px 3px rgba(0, 0, 0, 0.15);
  }

  /* Gradient text */
  .text-gradient {
    background: linear-gradient(135deg, var(--color-brand-500), var(--color-brand-700));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Dot grid pattern background */
  .dot-grid {
    background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
    background-size: 24px 24px;
  }

  /* Animated gradient border */
  .gradient-border {
    position: relative;
    border: none !important;
  }
  .gradient-border::before {
    content: '';
    position: absolute;
    inset: 0;
    padding: 1px;
    border-radius: inherit;
    background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-600), rgba(167,139,250,0.5), var(--color-brand-400));
    background-size: 300% 300%;
    animation: gradientShift 8s ease infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
  }

  /* Stagger animation children */
  .stagger-children > * {
    animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
  }
  .stagger-children > *:nth-child(1) { animation-delay: 0ms; }
  .stagger-children > *:nth-child(2) { animation-delay: 50ms; }
  .stagger-children > *:nth-child(3) { animation-delay: 100ms; }
  .stagger-children > *:nth-child(4) { animation-delay: 150ms; }
  .stagger-children > *:nth-child(5) { animation-delay: 200ms; }
  .stagger-children > *:nth-child(6) { animation-delay: 250ms; }
  .stagger-children > *:nth-child(7) { animation-delay: 300ms; }
  .stagger-children > *:nth-child(8) { animation-delay: 350ms; }
}

/* ============================================
   HTMX INTEGRATION
   ============================================ */

@layer utilities {
  /* HTMX loading indicator */
  .htmx-indicator { opacity: 0; transition: opacity 0.15s ease; }
  .htmx-request .htmx-indicator { opacity: 1; }
  .htmx-request.htmx-indicator { opacity: 1; }

  /* Swap transitions */
  .htmx-swapping { opacity: 0; transition: opacity 0.1s ease-out; }
  .htmx-settling { opacity: 1; transition: opacity 0.2s ease-in; }
  .htmx-added { animation: fadeUp 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
}

/* ============================================
   REDUCED MOTION
   ============================================ */

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .skeleton { animation: none; background: var(--surface-tertiary); }
}

/* ============================================
   SCROLLBAR
   ============================================ */

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
.dark ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); }
.dark ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ============================================
   VIEW TRANSITIONS
   ============================================ */

@view-transition {
  navigation: auto;
}

::view-transition-old(root) {
  animation: 0.15s ease-out both fadeOut;
}
::view-transition-new(root) {
  animation: 0.2s ease-in both fadeIn;
}
```

### static/css/premium.css (Additional Effects)

```css
/* Animated mesh gradient for auth pages */
.auth-mesh {
  background: linear-gradient(-45deg,
    #6172f3, #8098f9, #a78bfa, #34d399,
    #6172f3, #f472b6, #818cf8, #6172f3
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

/* Frosted sidebar */
.sidebar-glass {
  background: var(--surface-glass-heavy);
  backdrop-filter: blur(20px) saturate(1.8);
  border-right: 1px solid var(--border);
}

/* Card hover lift */
.card-lift {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
}
.card-lift:hover {
  transform: translateY(-2px);
  box-shadow:
    0 8px 24px -4px rgb(0 0 0 / 0.08),
    0 2px 8px -2px rgb(0 0 0 / 0.04);
}

/* Ring progress (for loan cards) */
.ring-progress {
  transform: rotate(-90deg);
  transform-origin: center;
}
.ring-progress circle {
  transition: stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Status dot with pulse */
.status-dot-live {
  position: relative;
}
.status-dot-live::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  background: inherit;
  animation: pulseSoft 2s ease-in-out infinite;
  opacity: 0.4;
}
```

---

## 6. Component Library (30+ Components)

### Stat Card with Sparkline

```html
<!-- components/cards/_stat_card.html -->
{% comment %}
  Usage: {% include "components/cards/_stat_card.html" with title="Total Disbursed" value="$2.4M" change="+12.5%" trend="up" sparkline_data="10,15,12,18,22,19,25" %}
{% endcomment %}

<div class="group relative overflow-hidden rounded-2xl border border-border bg-surface p-5 shadow-card transition-all duration-300 hover:shadow-card-hover card-lift">
  <!-- Content -->
  <div class="flex items-start justify-between">
    <div class="space-y-1.5">
      <p class="text-[13px] font-medium text-text-secondary">{{ title }}</p>
      <p class="text-[28px] font-bold tracking-tight text-text-primary font-tabular"
         {% if animate_value %}x-data="countUp({{ raw_value }})" x-text="display"{% endif %}>
        {{ value }}
      </p>
    </div>

    {% if change %}
    <span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold
      {% if trend == 'up' %}bg-success-50 text-success-700 dark:bg-success-500/10 dark:text-success-500
      {% else %}bg-danger-50 text-danger-700 dark:bg-danger-500/10 dark:text-danger-500{% endif %}">
      <svg class="h-3 w-3 {% if trend == 'down' %}rotate-180{% endif %}" viewBox="0 0 12 12" fill="none">
        <path d="M6 2.5v7M6 2.5L2.5 6M6 2.5L9.5 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      {{ change }}
    </span>
    {% endif %}
  </div>

  <!-- Sparkline -->
  {% if sparkline_data %}
  <div class="mt-3 h-10 w-full opacity-50 group-hover:opacity-80 transition-opacity">
    <canvas class="sparkline" data-values="{{ sparkline_data }}" data-color="{% if trend == 'up' %}#10b981{% else %}#ef4444{% endif %}" height="40"></canvas>
  </div>
  {% endif %}

  <!-- Ambient glow on hover -->
  <div class="pointer-events-none absolute -bottom-8 -right-8 h-32 w-32 rounded-full bg-brand-500/[0.04] transition-all duration-500 group-hover:scale-[2] group-hover:bg-brand-500/[0.06]"></div>
</div>
```

### Glass Stat Card (Hero Variant)

```html
<!-- components/cards/_stat_card_glass.html -->
<div class="relative overflow-hidden rounded-3xl p-6 glass inner-glow card-lift">
  <div class="relative z-10">
    <div class="flex items-center gap-3 mb-4">
      <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-500/10">
        {% include "components/icons/_icon.html" with name=icon class="h-5 w-5 text-brand-500" %}
      </div>
      <p class="text-sm font-medium text-text-secondary">{{ title }}</p>
    </div>
    <p class="text-4xl font-bold tracking-tight text-text-primary font-tabular">{{ value }}</p>
    {% if subtitle %}
    <p class="mt-1 text-sm text-text-muted">{{ subtitle }}</p>
    {% endif %}
  </div>
  <!-- Gradient orb -->
  <div class="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-gradient-to-br from-brand-400/20 to-brand-600/10 blur-2xl"></div>
</div>
```

### Loan Card with Progress Ring

```html
<!-- components/cards/_loan_card.html -->
<div class="group rounded-2xl border border-border bg-surface p-5 shadow-card transition-all duration-300 hover:shadow-card-hover card-lift">
  <!-- Header -->
  <div class="flex items-start justify-between mb-4">
    <div>
      <p class="text-sm font-semibold text-text-primary">{{ loan.product.name }}</p>
      <p class="text-xs text-text-muted mt-0.5">{{ loan.id|truncatechars:12 }}</p>
    </div>
    {% include "components/badges/_status_badge.html" with status=loan.status %}
  </div>

  <!-- Progress Ring + Amount -->
  <div class="flex items-center gap-4 mb-4">
    <div class="relative h-16 w-16 flex-shrink-0">
      <svg class="h-16 w-16" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="28" fill="none" stroke="var(--border)" stroke-width="4"/>
        <circle cx="32" cy="32" r="28" fill="none" stroke="var(--color-brand-500, #6172f3)" stroke-width="4"
                stroke-dasharray="175.93" stroke-dashoffset="{{ remaining_pct }}"
                stroke-linecap="round" class="ring-progress transition-all duration-700"/>
      </svg>
      <div class="absolute inset-0 flex items-center justify-center">
        <span class="text-xs font-bold text-text-primary font-tabular">{{ paid_pct }}%</span>
      </div>
    </div>
    <div class="flex-1 space-y-1">
      <div class="flex justify-between text-sm">
        <span class="text-text-muted">Outstanding</span>
        <span class="font-semibold text-text-primary font-mono">${{ loan.outstanding_principal|floatformat:0 }}</span>
      </div>
      <div class="flex justify-between text-sm">
        <span class="text-text-muted">Principal</span>
        <span class="font-medium text-text-secondary font-mono">${{ loan.principal_amount|floatformat:0 }}</span>
      </div>
    </div>
  </div>

  <!-- Next Payment -->
  <div class="flex items-center justify-between rounded-xl bg-surface-secondary p-3">
    <div>
      <p class="text-2xs font-medium uppercase tracking-wider text-text-muted">Next Payment</p>
      <p class="text-sm font-semibold text-text-primary font-mono">${{ next_payment.amount_due|floatformat:2 }}</p>
    </div>
    <div class="text-right">
      <p class="text-2xs font-medium uppercase tracking-wider text-text-muted">Due Date</p>
      <p class="text-sm font-medium text-text-primary">{{ next_payment.due_date|date:"M d" }}</p>
    </div>
  </div>
</div>
```

### Status Badge (Premium)

```html
<!-- components/badges/_status_badge.html -->
{% with colors_map="approved:emerald,active:emerald,paid:emerald,verified:emerald,rejected:red,defaulted:red,overdue:red,failed:red,submitted:blue,disbursed:violet,under_review:amber,pending:amber,in_progress:amber,draft:zinc,cancelled:zinc" %}

{% comment %} Resolve color from status {% endcomment %}
<span class="inline-flex items-center gap-1.5 rounded-lg px-2 py-1 text-[11px] font-semibold uppercase tracking-wide
  {% if status == 'approved' or status == 'active' or status == 'paid' or status == 'verified' %}
    bg-emerald-500/10 text-emerald-600 dark:text-emerald-400
  {% elif status == 'rejected' or status == 'defaulted' or status == 'overdue' or status == 'failed' %}
    bg-red-500/10 text-red-600 dark:text-red-400
  {% elif status == 'submitted' or status == 'disbursed' %}
    bg-blue-500/10 text-blue-600 dark:text-blue-400
  {% elif status == 'under_review' or status == 'pending' or status == 'in_progress' %}
    bg-amber-500/10 text-amber-600 dark:text-amber-400
  {% else %}
    bg-zinc-500/10 text-zinc-600 dark:text-zinc-400
  {% endif %}">
  <!-- Animated dot -->
  <span class="relative flex h-1.5 w-1.5">
    {% if status == 'active' or status == 'in_progress' or status == 'under_review' %}
    <span class="absolute inline-flex h-full w-full animate-ping rounded-full opacity-75
      {% if status == 'active' %}bg-emerald-400{% elif status == 'under_review' or status == 'in_progress' %}bg-amber-400{% endif %}"></span>
    {% endif %}
    <span class="relative inline-flex h-1.5 w-1.5 rounded-full
      {% if status == 'approved' or status == 'active' or status == 'paid' or status == 'verified' %}bg-emerald-500
      {% elif status == 'rejected' or status == 'defaulted' or status == 'overdue' %}bg-red-500
      {% elif status == 'submitted' or status == 'disbursed' %}bg-blue-500
      {% elif status == 'under_review' or status == 'pending' or status == 'in_progress' %}bg-amber-500
      {% else %}bg-zinc-400{% endif %}"></span>
  </span>
  {{ status|title }}
</span>
{% endwith %}
```

### Risk Grade Badge (Ring Variant)

```html
<!-- components/badges/_risk_badge.html -->
<div class="relative inline-flex h-10 w-10 items-center justify-center">
  <!-- Background ring -->
  <svg class="absolute inset-0 h-10 w-10" viewBox="0 0 40 40">
    <circle cx="20" cy="20" r="17" fill="none" stroke="var(--border)" stroke-width="2.5"/>
    <circle cx="20" cy="20" r="17" fill="none" stroke-width="2.5" stroke-linecap="round"
            stroke-dasharray="106.81" stroke-dashoffset="{{ grade_offset }}"
            class="ring-progress
              {% if grade == 'A+' or grade == 'A' %}stroke-emerald-500
              {% elif grade == 'B' %}stroke-blue-500
              {% elif grade == 'C' %}stroke-amber-500
              {% elif grade == 'D' %}stroke-orange-500
              {% else %}stroke-red-500{% endif %}"/>
  </svg>
  <span class="relative text-xs font-bold
    {% if grade == 'A+' or grade == 'A' %}text-emerald-600 dark:text-emerald-400
    {% elif grade == 'B' %}text-blue-600 dark:text-blue-400
    {% elif grade == 'C' %}text-amber-600 dark:text-amber-400
    {% elif grade == 'D' %}text-orange-600 dark:text-orange-400
    {% else %}text-red-600 dark:text-red-400{% endif %}">
    {{ grade }}
  </span>
</div>
```

### Data Table (Premium)

```html
<!-- components/tables/_data_table.html -->
<div class="overflow-hidden rounded-2xl border border-border bg-surface shadow-card">
  <!-- Toolbar -->
  <div class="flex flex-col gap-3 border-b border-border px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
    <div class="flex items-center gap-3">
      <!-- Search -->
      <div class="relative">
        <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
        <input type="search"
               placeholder="Search..."
               class="w-full rounded-xl border-0 bg-surface-secondary py-2 pl-9 pr-4 text-sm text-text-primary ring-1 ring-inset ring-border placeholder:text-text-muted transition-shadow focus:bg-surface focus:ring-2 focus:ring-brand-500/30 sm:w-64"
               hx-get="{{ filter_url }}"
               hx-trigger="input changed delay:300ms"
               hx-target="#table-body"
               hx-indicator="#table-loading"
               name="q" />
      </div>

      <!-- Filter chips -->
      {% if active_filters %}
      <div class="hidden sm:flex items-center gap-1.5">
        {% for filter in active_filters %}
        <span class="inline-flex items-center gap-1 rounded-lg bg-brand-500/10 px-2.5 py-1 text-xs font-medium text-brand-700 dark:text-brand-300">
          {{ filter.label }}
          <button hx-get="{{ filter.remove_url }}" hx-target="#table-body" class="ml-0.5 hover:text-brand-900">
            <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </span>
        {% endfor %}
      </div>
      {% endif %}
    </div>

    <div class="flex items-center gap-2">
      <!-- Loading indicator -->
      <div id="table-loading" class="htmx-indicator">
        <svg class="h-4 w-4 animate-spin text-brand-500" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" class="opacity-25"/><path d="M4 12a8 8 0 018-8" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
      </div>

      <!-- View toggle -->
      <div class="hidden sm:flex items-center rounded-lg border border-border p-0.5" x-data="{ view: 'table' }">
        <button x-on:click="view = 'table'" :class="view === 'table' ? 'bg-surface-tertiary text-text-primary' : 'text-text-muted'" class="rounded-md p-1.5 transition">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"/></svg>
        </button>
        <button x-on:click="view = 'grid'" :class="view === 'grid' ? 'bg-surface-tertiary text-text-primary' : 'text-text-muted'" class="rounded-md p-1.5 transition">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zm0 9.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zm9.75-9.75A2.25 2.25 0 0115.75 3.75H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zm0 9.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25a2.25 2.25 0 01-2.25-2.25v-2.25z"/></svg>
        </button>
      </div>

      {% block table_actions %}{% endblock %}
    </div>
  </div>

  <!-- Table -->
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-border bg-surface-secondary/50">
          {% for header in headers %}
          <th class="whitespace-nowrap px-5 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-text-muted {% if header.sortable %}cursor-pointer select-none hover:text-text-secondary transition{% endif %}"
              {% if header.sortable %}
              hx-get="{{ sort_url }}?sort={{ header.field }}&dir={% if current_sort == header.field and current_dir == 'asc' %}desc{% else %}asc{% endif %}"
              hx-target="#table-body"
              {% endif %}>
            <span class="inline-flex items-center gap-1">
              {{ header.label }}
              {% if header.sortable and current_sort == header.field %}
              <svg class="h-3 w-3 {% if current_dir == 'desc' %}rotate-180{% endif %}" viewBox="0 0 12 12" fill="currentColor"><path d="M6 2l4 5H2z"/></svg>
              {% endif %}
            </span>
          </th>
          {% endfor %}
        </tr>
      </thead>
      <tbody id="table-body" class="divide-y divide-border">
        {% block table_body %}{% endblock %}
      </tbody>
    </table>
  </div>

  <!-- Pagination -->
  {% if page_obj %}
  <div class="flex items-center justify-between border-t border-border px-5 py-3">
    <p class="text-xs text-text-muted">
      Showing <span class="font-medium text-text-secondary">{{ page_obj.start_index }}-{{ page_obj.end_index }}</span>
      of <span class="font-medium text-text-secondary">{{ page_obj.paginator.count }}</span>
    </p>
    <div class="flex items-center gap-1">
      {% if page_obj.has_previous %}
      <button hx-get="{{ request.path }}?page={{ page_obj.previous_page_number }}" hx-target="#table-body"
              class="rounded-lg p-2 text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
      {% endif %}
      {% for num in page_obj.paginator.page_range %}
        {% if num == page_obj.number %}
        <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-500/10 text-xs font-semibold text-brand-600">{{ num }}</span>
        {% elif num > page_obj.number|add:"-3" and num < page_obj.number|add:"3" %}
        <button hx-get="{{ request.path }}?page={{ num }}" hx-target="#table-body"
                class="flex h-8 w-8 items-center justify-center rounded-lg text-xs text-text-muted transition hover:bg-surface-secondary">{{ num }}</button>
        {% endif %}
      {% endfor %}
      {% if page_obj.has_next %}
      <button hx-get="{{ request.path }}?page={{ page_obj.next_page_number }}" hx-target="#table-body"
              class="rounded-lg p-2 text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/></svg>
      </button>
      {% endif %}
    </div>
  </div>
  {% endif %}
</div>
```

### Glass Modal

```html
<!-- components/modals/_modal.html -->
<div x-data="{ open: false }"
     x-on:open-modal.window="if ($event.detail.id === '{{ modal_id }}') open = true"
     x-on:keydown.escape.window="open = false"
     x-cloak>

  <!-- Backdrop -->
  <template x-teleport="body">
    <div x-show="open" class="fixed inset-0 z-modal-backdrop">
      <div x-show="open"
           x-transition:enter="transition ease-out duration-200"
           x-transition:enter-start="opacity-0"
           x-transition:enter-end="opacity-100"
           x-transition:leave="transition ease-in duration-150"
           x-transition:leave-start="opacity-100"
           x-transition:leave-end="opacity-0"
           class="fixed inset-0 bg-black/40 backdrop-blur-sm"
           x-on:click="open = false"></div>

      <!-- Panel -->
      <div class="fixed inset-0 z-modal flex items-center justify-center p-4" x-on:click.self="open = false">
        <div x-show="open"
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0 scale-95 translate-y-4"
             x-transition:enter-end="opacity-100 scale-100 translate-y-0"
             x-transition:leave="transition ease-in duration-200"
             x-transition:leave-start="opacity-100 scale-100"
             x-transition:leave-end="opacity-0 scale-95"
             class="w-full max-w-{{ size|default:'lg' }} overflow-hidden rounded-3xl bg-surface shadow-modal border border-border"
             x-trap.noscroll="open">

          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-5">
            <div>
              <h2 class="text-lg font-semibold text-text-primary">{{ title }}</h2>
              {% if subtitle %}<p class="mt-0.5 text-sm text-text-muted">{{ subtitle }}</p>{% endif %}
            </div>
            <button x-on:click="open = false"
                    class="flex h-8 w-8 items-center justify-center rounded-lg text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- Divider -->
          <div class="border-t border-border"></div>

          <!-- Body -->
          <div class="px-6 py-5 max-h-[60vh] overflow-y-auto">
            {% block modal_body %}{% endblock %}
          </div>

          <!-- Footer -->
          <div class="flex items-center justify-end gap-3 border-t border-border px-6 py-4 bg-surface-secondary/30">
            {% block modal_footer %}
            <button x-on:click="open = false"
                    class="rounded-xl px-4 py-2.5 text-sm font-medium text-text-secondary transition hover:bg-surface-tertiary">
              Cancel
            </button>
            <button class="rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:ring-offset-2 focus:ring-offset-surface btn-glow">
              {{ confirm_label|default:"Confirm" }}
            </button>
            {% endblock %}
          </div>
        </div>
      </div>
    </div>
  </template>
</div>
```

### Slide-in Drawer

```html
<!-- components/modals/_drawer.html -->
<div x-data="{ open: false }"
     x-on:open-drawer.window="if ($event.detail.id === '{{ drawer_id }}') open = true"
     x-on:keydown.escape.window="open = false"
     x-cloak>
  <template x-teleport="body">
    <div x-show="open" class="fixed inset-0 z-modal-backdrop">
      <!-- Backdrop -->
      <div x-show="open" x-transition.opacity.duration.200ms
           class="fixed inset-0 bg-black/30 backdrop-blur-xs"
           x-on:click="open = false"></div>

      <!-- Panel -->
      <div x-show="open"
           x-transition:enter="transition ease-out duration-300"
           x-transition:enter-start="translate-x-full"
           x-transition:enter-end="translate-x-0"
           x-transition:leave="transition ease-in duration-200"
           x-transition:leave-start="translate-x-0"
           x-transition:leave-end="translate-x-full"
           class="fixed inset-y-0 right-0 z-modal w-full max-w-lg border-l border-border bg-surface shadow-modal"
           x-trap.noscroll="open">

        <!-- Header -->
        <div class="flex items-center justify-between border-b border-border px-6 py-4">
          <h2 class="text-lg font-semibold text-text-primary">{{ title }}</h2>
          <button x-on:click="open = false" class="rounded-lg p-2 text-text-muted hover:bg-surface-secondary transition">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto p-6">
          {% block drawer_body %}{% endblock %}
        </div>
      </div>
    </div>
  </template>
</div>
```

### Skeleton Loader (Premium)

```html
<!-- components/feedback/_skeleton.html -->
{% if type == "stat-cards" %}
<div class="grid grid-cols-2 gap-4 lg:grid-cols-4 stagger-children">
  {% for i in "xxxx"|make_list %}
  <div class="rounded-2xl border border-border bg-surface p-5">
    <div class="space-y-3">
      <div class="skeleton h-3.5 w-20"></div>
      <div class="skeleton h-8 w-28"></div>
      <div class="skeleton h-3 w-16"></div>
    </div>
  </div>
  {% endfor %}
</div>

{% elif type == "card" %}
{% for i in "xxx"|make_list %}
<div class="rounded-2xl border border-border bg-surface p-5">
  <div class="flex items-start justify-between mb-4">
    <div class="skeleton h-4 w-32"></div>
    <div class="skeleton h-5 w-16 rounded-lg"></div>
  </div>
  <div class="space-y-2">
    <div class="skeleton h-6 w-24"></div>
    <div class="skeleton h-3 w-full"></div>
    <div class="skeleton h-3 w-3/4"></div>
  </div>
</div>
{% endfor %}

{% elif type == "table-row" %}
{% for i in "xxxxx"|make_list %}
<tr>
  {% for j in "xxxxx"|make_list %}
  <td class="px-5 py-3.5"><div class="skeleton h-4 {% cycle 'w-24' 'w-32' 'w-16' 'w-20' 'w-12' %}"></div></td>
  {% endfor %}
</tr>
{% endfor %}
{% endif %}
```

### Progress Ring (SVG)

```html
<!-- components/feedback/_progress_ring.html -->
<div class="relative inline-flex items-center justify-center" style="width: {{ size|default:80 }}px; height: {{ size|default:80 }}px;">
  <svg class="h-full w-full ring-progress" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="42" fill="none" stroke="var(--border)" stroke-width="{{ stroke|default:6 }}"/>
    <circle cx="50" cy="50" r="42" fill="none"
            stroke="{{ color|default:'var(--color-brand-500)' }}"
            stroke-width="{{ stroke|default:6 }}"
            stroke-linecap="round"
            stroke-dasharray="263.89"
            stroke-dashoffset="{% widthratio 100|add:'-'|add:percentage 100 263.89 %}"
            class="transition-all duration-1000"/>
  </svg>
  <div class="absolute inset-0 flex flex-col items-center justify-center">
    <span class="text-lg font-bold text-text-primary font-tabular">{{ percentage }}%</span>
    {% if label %}<span class="text-2xs text-text-muted">{{ label }}</span>{% endif %}
  </div>
</div>
```

### Timeline

```html
<!-- components/data/_timeline.html -->
<div class="space-y-0">
  {% for event in events %}
  <div class="flex gap-4 {% if not forloop.last %}pb-6{% endif %}">
    <!-- Line + Dot -->
    <div class="flex flex-col items-center">
      <div class="flex h-7 w-7 items-center justify-center rounded-full border-2
        {% if forloop.first %}border-brand-500 bg-brand-500/10{% else %}border-border bg-surface{% endif %}">
        {% if event.icon %}
        {% include "components/icons/_icon.html" with name=event.icon class="h-3 w-3 text-brand-500" %}
        {% else %}
        <div class="h-2 w-2 rounded-full {% if forloop.first %}bg-brand-500{% else %}bg-border-strong{% endif %}"></div>
        {% endif %}
      </div>
      {% if not forloop.last %}
      <div class="w-px flex-1 bg-border mt-1"></div>
      {% endif %}
    </div>

    <!-- Content -->
    <div class="flex-1 pt-0.5 {% if not forloop.last %}pb-1{% endif %}">
      <p class="text-sm font-medium text-text-primary">{{ event.title }}</p>
      {% if event.description %}
      <p class="mt-0.5 text-sm text-text-secondary">{{ event.description }}</p>
      {% endif %}
      <p class="mt-1 text-xs text-text-muted">{{ event.timestamp|timesince }} ago {% if event.actor %}· {{ event.actor }}{% endif %}</p>
    </div>
  </div>
  {% endfor %}
</div>
```

### Empty State

```html
<!-- components/feedback/_empty_state.html -->
<div class="flex flex-col items-center justify-center py-16 px-4 text-center">
  {% if lottie_src %}
  <div class="mb-6 h-40 w-40" x-data x-init="lottie.loadAnimation({ container: $el, path: '{{ lottie_src }}', renderer: 'svg', loop: true, autoplay: true })"></div>
  {% elif illustration %}
  <img src="{% static illustration %}" alt="" class="mb-6 h-40 w-40 opacity-60 dark:opacity-40" />
  {% else %}
  <div class="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-surface-tertiary">
    {% include "components/icons/_icon.html" with name=icon|default:"inbox" class="h-7 w-7 text-text-muted" %}
  </div>
  {% endif %}
  <h3 class="text-base font-semibold text-text-primary">{{ title|default:"No results found" }}</h3>
  <p class="mt-1.5 max-w-sm text-sm text-text-muted text-balance">{{ description|default:"Try adjusting your search or filters." }}</p>
  {% if action_url %}
  <a href="{{ action_url }}" class="mt-5 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 btn-glow">
    {% if action_icon %}{% include "components/icons/_icon.html" with name=action_icon class="h-4 w-4" %}{% endif %}
    {{ action_label }}
  </a>
  {% endif %}
</div>
```

---

## 7. Layout System (Glass-Morphic)

### Base Layout

```html
<!-- templates/base/_base.html -->
{% load static %}
<!DOCTYPE html>
<html lang="en" class="{% if request.COOKIES.theme == 'dark' %}dark{% endif %}"
      x-data x-bind:class="{ 'dark': $store.theme.dark }">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="csrf-token" content="{{ csrf_token }}" />
  <meta name="color-scheme" content="light dark" />
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#09090b" media="(prefers-color-scheme: dark)" />
  <title>{% block title %}Dashboard{% endblock %} · {{ institution.name|default:"LendFlow" }}</title>

  <!-- Preload critical fonts -->
  <link rel="preload" href="{% static 'fonts/Inter-Variable.woff2' %}" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{% static 'fonts/JetBrainsMono-Variable.woff2' %}" as="font" type="font/woff2" crossorigin />

  <!-- Styles -->
  <link rel="stylesheet" href="{% static 'css/dist/styles.css' %}" />
  <link rel="stylesheet" href="{% static 'css/premium.css' %}" />

  <!-- Institution branding override -->
  {% if institution.branding.colors %}
  <style>
    :root {
      {% for key, val in institution.branding.colors.items %}
      --color-brand-{{ key }}: {{ val }};
      {% endfor %}
    }
  </style>
  {% endif %}

  {% block extra_head %}{% endblock %}

  <!-- Inline critical: prevent FOUC for dark mode -->
  <script>
    if (localStorage.theme === 'dark' || (!localStorage.theme && matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark')
    }
  </script>
</head>
<body class="min-h-screen bg-surface-secondary text-text-primary antialiased grain">

  {% block body %}{% endblock %}

  <!-- Toast container -->
  <div x-data class="fixed bottom-5 right-5 z-toast flex flex-col-reverse gap-2" style="max-width: 380px;">
    <template x-for="toast in $store.toasts.items" :key="toast.id">
      <div x-show="toast.visible"
           x-transition:enter="transition ease-out duration-300"
           x-transition:enter-start="translate-x-full opacity-0"
           x-transition:enter-end="translate-x-0 opacity-100"
           x-transition:leave="transition ease-in duration-200"
           x-transition:leave-start="translate-x-0 opacity-100"
           x-transition:leave-end="translate-x-full opacity-0"
           class="flex items-start gap-3 rounded-2xl border border-border bg-surface p-4 shadow-elevated"
           role="alert">
        <!-- Icon -->
        <div class="mt-0.5 flex-shrink-0">
          <template x-if="toast.type === 'success'"><svg class="h-5 w-5 text-success-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"/></svg></template>
          <template x-if="toast.type === 'error'"><svg class="h-5 w-5 text-danger-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"/></svg></template>
          <template x-if="toast.type === 'info'"><svg class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"/></svg></template>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-text-primary" x-text="toast.title"></p>
          <p class="mt-0.5 text-sm text-text-secondary" x-text="toast.message" x-show="toast.message"></p>
        </div>
        <button x-on:click="$store.toasts.dismiss(toast.id)" class="flex-shrink-0 rounded-lg p-1 text-text-muted hover:text-text-secondary transition">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </template>
  </div>

  <!-- Scripts -->
  <script src="https://unpkg.com/htmx.org@2.0.4" defer></script>
  <script src="https://unpkg.com/htmx-ext-head-support@2.0.2/head-support.js" defer></script>
  <script src="https://unpkg.com/alpinejs@3.14.8/dist/cdn.min.js" defer></script>
  <script src="{% static 'js/app.js' %}" defer></script>
  <script src="{% static 'js/htmx-config.js' %}" defer></script>
  {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### Admin Layout (Glass Sidebar)

```html
<!-- templates/base/_base_admin.html -->
{% extends "base/_base.html" %}

{% block body %}
<div class="flex h-screen overflow-hidden"
     x-data="{
       sidebarExpanded: localStorage.getItem('sidebar') !== 'collapsed',
       mobileSidebar: false,
       toggleSidebar() {
         this.sidebarExpanded = !this.sidebarExpanded;
         localStorage.setItem('sidebar', this.sidebarExpanded ? 'expanded' : 'collapsed');
       }
     }">

  <!-- ===== SIDEBAR ===== -->
  <aside :class="sidebarExpanded ? 'w-[260px]' : 'w-[72px]'"
         class="hidden lg:flex flex-col sidebar-glass transition-all duration-300 ease-out">

    <!-- Logo -->
    <div class="flex h-16 items-center px-4" :class="sidebarExpanded ? 'justify-between' : 'justify-center'">
      <a href="/" class="flex items-center gap-2.5 overflow-hidden">
        {% if institution.branding.logo_url %}
          <img src="{{ institution.branding.logo_url }}" alt="{{ institution.name }}" class="h-8 w-8 flex-shrink-0 rounded-lg" />
        {% else %}
          <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-brand-600">
            <span class="text-sm font-bold text-white">L</span>
          </div>
        {% endif %}
        <span x-show="sidebarExpanded" x-transition.opacity.duration.200ms
              class="text-[15px] font-semibold text-text-primary truncate">
          {{ institution.name|default:"LendFlow" }}
        </span>
      </a>
      <button x-show="sidebarExpanded" x-on:click="toggleSidebar()" x-transition.opacity
              class="rounded-lg p-1.5 text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto overflow-x-hidden px-3 py-4 no-scrollbar">
      <!-- Main section -->
      <div class="space-y-1">
        <p x-show="sidebarExpanded" x-transition.opacity class="mb-2 px-3 text-[10px] font-semibold uppercase tracking-widest text-text-muted">Overview</p>

        {% with nav_items="dashboard:Dashboard:home,applications:Applications:document-text,borrowers:Borrowers:users,loans:Active Loans:banknotes" %}
        {% for item_str in nav_items|split:"," %}
        {% with parts=item_str|split:":" %}
        <a href="{% url 'admin:'|add:parts.0 %}"
           class="group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-150
                  {% if active_nav == parts.0 %}
                    bg-brand-500/10 text-brand-600 dark:text-brand-400
                  {% else %}
                    text-text-secondary hover:bg-surface-secondary hover:text-text-primary
                  {% endif %}"
           :class="sidebarExpanded ? '' : 'justify-center'">
          {% include "components/icons/_icon.html" with name=parts.2 class="h-[18px] w-[18px] flex-shrink-0" %}
          <span x-show="sidebarExpanded" x-transition.opacity.duration.150ms class="truncate">{{ parts.1 }}</span>
          {% if parts.0 == 'applications' and pending_count %}
          <span x-show="sidebarExpanded" class="ml-auto flex h-5 min-w-[20px] items-center justify-center rounded-full bg-brand-500 px-1.5 text-[10px] font-bold text-white">
            {{ pending_count }}
          </span>
          {% endif %}
        </a>
        {% endwith %}
        {% endfor %}
        {% endwith %}
      </div>

      <!-- Finance section -->
      <div class="mt-6 space-y-1">
        <p x-show="sidebarExpanded" x-transition.opacity class="mb-2 px-3 text-[10px] font-semibold uppercase tracking-widest text-text-muted">Finance</p>
        {% with nav_items="collections:Collections:phone,ledger:Ledger:book-open,reports:Reports:chart-bar" %}
        {% for item_str in nav_items|split:"," %}
        {% with parts=item_str|split:":" %}
        <a href="{% url 'admin:'|add:parts.0 %}"
           class="group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-150
                  {% if active_nav == parts.0 %}bg-brand-500/10 text-brand-600 dark:text-brand-400
                  {% else %}text-text-secondary hover:bg-surface-secondary hover:text-text-primary{% endif %}"
           :class="sidebarExpanded ? '' : 'justify-center'">
          {% include "components/icons/_icon.html" with name=parts.2 class="h-[18px] w-[18px] flex-shrink-0" %}
          <span x-show="sidebarExpanded" x-transition.opacity.duration.150ms class="truncate">{{ parts.1 }}</span>
        </a>
        {% endwith %}
        {% endfor %}
        {% endwith %}
      </div>
    </nav>

    <!-- Bottom: User + Collapse -->
    <div class="border-t border-border p-3">
      <!-- Collapsed: expand button -->
      <button x-show="!sidebarExpanded" x-on:click="toggleSidebar()" x-transition.opacity
              class="flex w-full items-center justify-center rounded-xl p-2.5 text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/></svg>
      </button>

      <!-- Expanded: user menu -->
      <div x-show="sidebarExpanded" x-transition.opacity x-data="{ userMenu: false }" class="relative">
        <button x-on:click="userMenu = !userMenu"
                class="flex w-full items-center gap-3 rounded-xl p-2 transition hover:bg-surface-secondary">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-brand-400 to-brand-600 text-xs font-bold text-white">
            {{ request.user.first_name.0|default:"U" }}{{ request.user.last_name.0 }}
          </div>
          <div class="flex-1 text-left overflow-hidden">
            <p class="text-sm font-medium text-text-primary truncate">{{ request.user.get_full_name }}</p>
            <p class="text-xs text-text-muted truncate capitalize">{{ request.user.role }}</p>
          </div>
          <svg class="h-4 w-4 text-text-muted transition" :class="userMenu && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"/></svg>
        </button>

        <!-- Dropdown -->
        <div x-show="userMenu" x-transition x-on:click.outside="userMenu = false"
             class="absolute bottom-full left-0 mb-2 w-full rounded-xl border border-border bg-surface p-1.5 shadow-elevated">
          <a href="{% url 'admin:settings' %}" class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-text-secondary hover:bg-surface-secondary hover:text-text-primary transition">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"/><path stroke-linecap="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            Settings
          </a>
          <hr class="my-1 border-border" />
          <a href="{% url 'auth:logout' %}" class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-500/10 transition">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"/></svg>
            Sign out
          </a>
        </div>
      </div>
    </div>
  </aside>

  <!-- ===== MAIN AREA ===== -->
  <div class="flex flex-1 flex-col overflow-hidden">

    <!-- Top Bar -->
    <header class="flex h-14 items-center justify-between border-b border-border bg-surface/80 backdrop-blur-glass px-6 sticky top-0 z-sticky">
      <!-- Left: Mobile menu + Breadcrumbs -->
      <div class="flex items-center gap-4">
        <button x-on:click="mobileSidebar = true" class="lg:hidden rounded-lg p-2 text-text-muted hover:bg-surface-secondary transition">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
        </button>
        <nav class="hidden lg:flex items-center gap-1.5 text-sm">
          {% block breadcrumbs %}
          <span class="font-medium text-text-primary">Dashboard</span>
          {% endblock %}
        </nav>
      </div>

      <!-- Right: Actions -->
      <div class="flex items-center gap-2">
        <!-- Command Palette trigger -->
        <button x-on:click="$dispatch('open-command-palette')"
                class="hidden md:flex items-center gap-2 rounded-xl border border-border bg-surface-secondary/50 px-3 py-1.5 text-sm text-text-muted transition hover:bg-surface-secondary hover:border-border-strong">
          <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
          Search...
          <kbd class="rounded bg-surface-tertiary px-1.5 py-0.5 text-[10px] font-medium text-text-muted">Ctrl K</kbd>
        </button>

        <!-- Notifications -->
        <div x-data="{ open: false }" class="relative">
          <button x-on:click="open = !open"
                  class="relative rounded-xl p-2 text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"/></svg>
            {% if unread_notifications %}
            <span class="absolute right-1.5 top-1.5 flex h-2 w-2">
              <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-brand-400 opacity-75"></span>
              <span class="relative inline-flex h-2 w-2 rounded-full bg-brand-500"></span>
            </span>
            {% endif %}
          </button>

          <!-- Notification dropdown -->
          <div x-show="open" x-transition x-on:click.outside="open = false"
               class="absolute right-0 top-full mt-2 w-80 rounded-2xl border border-border bg-surface shadow-elevated overflow-hidden">
            <div class="flex items-center justify-between px-4 py-3 border-b border-border">
              <p class="text-sm font-semibold text-text-primary">Notifications</p>
              <button class="text-xs font-medium text-brand-600 hover:text-brand-700 transition">Mark all read</button>
            </div>
            <div class="max-h-80 overflow-y-auto divide-y divide-border"
                 hx-get="{% url 'admin:notifications' %}" hx-trigger="intersect once" hx-swap="innerHTML">
              <div class="p-8 text-center text-sm text-text-muted">Loading...</div>
            </div>
          </div>
        </div>

        <!-- Theme toggle -->
        <button x-on:click="$store.theme.toggle()"
                class="rounded-xl p-2 text-text-muted transition hover:bg-surface-secondary hover:text-text-primary">
          <svg x-show="!$store.theme.dark" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"/></svg>
          <svg x-show="$store.theme.dark" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"/></svg>
        </button>
      </div>
    </header>

    <!-- Page Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="mx-auto max-w-[1440px] p-6 lg:p-8">
        {% block content %}{% endblock %}
      </div>
    </main>
  </div>

  <!-- Mobile sidebar overlay -->
  <div x-show="mobileSidebar" x-cloak class="fixed inset-0 z-modal-backdrop lg:hidden">
    <div x-show="mobileSidebar" x-transition.opacity class="fixed inset-0 bg-black/40 backdrop-blur-xs" x-on:click="mobileSidebar = false"></div>
    <aside x-show="mobileSidebar"
           x-transition:enter="transition ease-out duration-300" x-transition:enter-start="-translate-x-full" x-transition:enter-end="translate-x-0"
           x-transition:leave="transition ease-in duration-200" x-transition:leave-start="translate-x-0" x-transition:leave-end="-translate-x-full"
           class="fixed inset-y-0 left-0 z-modal w-72 border-r border-border bg-surface shadow-modal">
      {% include "components/navigation/_sidebar.html" %}
    </aside>
  </div>
</div>

{% include "components/navigation/_command_palette.html" %}
{% endblock %}
```

---

## 8. Auth Pages (Cinematic)

```html
<!-- templates/auth/login.html -->
{% extends "base/_base_auth.html" %}

{% block auth_content %}
<div class="flex min-h-screen">
  <!-- Left: Mesh Gradient Artwork -->
  <div class="hidden lg:flex lg:w-1/2 xl:w-[55%] relative overflow-hidden">
    <div class="auth-mesh absolute inset-0"></div>
    <div class="absolute inset-0 bg-black/10"></div>

    <!-- Floating content -->
    <div class="relative z-10 flex flex-col justify-between p-12 xl:p-16">
      <!-- Logo -->
      <div>
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm">
            <span class="text-lg font-bold text-white">L</span>
          </div>
          <span class="text-xl font-semibold text-white">{{ institution.name|default:"LendFlow" }}</span>
        </div>
      </div>

      <!-- Testimonial / Value Prop -->
      <div class="max-w-md">
        <blockquote class="text-2xl font-medium leading-relaxed text-white/90 text-balance">
          "The platform reduced our loan processing time from 5 days to under 30 minutes."
        </blockquote>
        <div class="mt-6 flex items-center gap-3">
          <div class="h-10 w-10 rounded-full bg-white/20 backdrop-blur-sm"></div>
          <div>
            <p class="text-sm font-medium text-white">Sarah Chen</p>
            <p class="text-sm text-white/60">VP Operations, First National</p>
          </div>
        </div>
      </div>

      <!-- Stats strip -->
      <div class="flex gap-8">
        <div>
          <p class="text-3xl font-bold text-white font-tabular">$2.4B</p>
          <p class="text-sm text-white/60">Loans Processed</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-white font-tabular">8,000+</p>
          <p class="text-sm text-white/60">Monthly Applications</p>
        </div>
        <div>
          <p class="text-3xl font-bold text-white font-tabular">99.9%</p>
          <p class="text-sm text-white/60">Uptime SLA</p>
        </div>
      </div>
    </div>

    <!-- Floating glass cards (decorative) -->
    <div class="absolute right-12 top-1/4 h-48 w-64 rounded-3xl bg-white/10 backdrop-blur-sm border border-white/20 p-6 rotate-6 animate-float" style="animation-delay: 0s;">
      <div class="h-3 w-20 rounded bg-white/20 mb-3"></div>
      <div class="h-8 w-32 rounded bg-white/20 mb-4"></div>
      <div class="h-2 w-full rounded bg-white/10"></div>
      <div class="h-2 w-3/4 rounded bg-white/10 mt-2"></div>
    </div>
    <div class="absolute right-32 bottom-1/4 h-36 w-56 rounded-3xl bg-white/10 backdrop-blur-sm border border-white/20 p-6 -rotate-3 animate-float" style="animation-delay: 2s;">
      <div class="h-3 w-16 rounded bg-white/20 mb-3"></div>
      <div class="h-6 w-24 rounded bg-white/20 mb-4"></div>
      <div class="flex gap-2 mt-4">
        <div class="h-8 w-8 rounded-full bg-white/20"></div>
        <div class="h-8 w-8 rounded-full bg-white/20"></div>
        <div class="h-8 w-8 rounded-full bg-white/20"></div>
      </div>
    </div>
  </div>

  <!-- Right: Login Form -->
  <div class="flex flex-1 flex-col justify-center px-6 py-12 lg:px-12 xl:px-20">
    <div class="mx-auto w-full max-w-[400px]">
      <!-- Mobile logo -->
      <div class="mb-8 lg:hidden">
        <div class="flex items-center gap-2.5">
          <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-600">
            <span class="text-sm font-bold text-white">L</span>
          </div>
          <span class="text-lg font-semibold text-text-primary">{{ institution.name|default:"LendFlow" }}</span>
        </div>
      </div>

      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-h1 text-text-primary">Welcome back</h1>
        <p class="mt-2 text-base text-text-secondary">Sign in to your account to continue.</p>
      </div>

      <!-- Form -->
      <form method="post" action="{% url 'auth:login' %}" class="space-y-5">
        {% csrf_token %}

        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-text-primary mb-1.5">Email</label>
          <input type="email" id="email" name="email" required autocomplete="email"
                 class="w-full rounded-xl border-0 bg-surface-secondary py-3 px-4 text-sm text-text-primary ring-1 ring-inset ring-border placeholder:text-text-muted transition-shadow focus:bg-surface focus:ring-2 focus:ring-brand-500/40"
                 placeholder="you@company.com" />
        </div>

        <!-- Password -->
        <div x-data="{ show: false }">
          <div class="flex items-center justify-between mb-1.5">
            <label for="password" class="block text-sm font-medium text-text-primary">Password</label>
            <a href="{% url 'auth:forgot-password' %}" class="text-sm font-medium text-brand-600 hover:text-brand-700 transition">Forgot?</a>
          </div>
          <div class="relative">
            <input :type="show ? 'text' : 'password'" id="password" name="password" required autocomplete="current-password"
                   class="w-full rounded-xl border-0 bg-surface-secondary py-3 px-4 pr-11 text-sm text-text-primary ring-1 ring-inset ring-border placeholder:text-text-muted transition-shadow focus:bg-surface focus:ring-2 focus:ring-brand-500/40"
                   placeholder="Enter your password" />
            <button type="button" x-on:click="show = !show" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary transition">
              <svg x-show="!show" class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"/><path stroke-linecap="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              <svg x-show="show" x-cloak class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"/></svg>
            </button>
          </div>
        </div>

        <!-- Error message -->
        {% if form.errors %}
        <div class="flex items-center gap-2 rounded-xl bg-danger-50 dark:bg-danger-500/10 px-4 py-3 text-sm text-danger-700 dark:text-danger-400 animate-fade-in">
          <svg class="h-4 w-4 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"/></svg>
          Invalid email or password. Please try again.
        </div>
        {% endif %}

        <!-- Submit -->
        <button type="submit"
                class="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:ring-offset-2 focus:ring-offset-surface btn-glow">
          Sign in
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/></svg>
        </button>
      </form>

      <!-- Divider -->
      <div class="my-6 flex items-center gap-3">
        <div class="h-px flex-1 bg-border"></div>
        <span class="text-xs text-text-muted">or continue with</span>
        <div class="h-px flex-1 bg-border"></div>
      </div>

      <!-- Social login -->
      <div class="grid grid-cols-2 gap-3">
        <button class="flex items-center justify-center gap-2 rounded-xl border border-border bg-surface py-2.5 text-sm font-medium text-text-primary transition hover:bg-surface-secondary">
          <svg class="h-4 w-4" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
          Google
        </button>
        <button class="flex items-center justify-center gap-2 rounded-xl border border-border bg-surface py-2.5 text-sm font-medium text-text-primary transition hover:bg-surface-secondary">
          <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M16.365 1.43c0 1.14-.493 2.27-1.177 3.08-.744.9-1.99 1.57-2.987 1.57-.18 0-.36-.02-.53-.06-.01-.18-.04-.39-.04-.59 0-1.15.572-2.27 1.206-2.98.804-.94 2.142-1.64 3.248-1.68.03.21.05.43.05.66zm3.518 17.05c-.29.63-1.036 1.91-1.847 2.47-.73.5-1.385.65-2.098.65-.748 0-1.268-.25-1.813-.51-.578-.28-1.2-.57-2.14-.57-1 0-1.66.3-2.28.59-.5.23-.97.45-1.65.49h-.18c-.6-.03-1.08-.27-1.6-.53-.58-.29-1.2-.76-2.02-1.65-1.86-2.04-3.25-5.63-3.25-8.98 0-3.11 1.62-5.42 4.01-6.32 1.08-.41 2.19-.56 3.2-.56 1.1 0 1.95.31 2.68.57.57.2 1.06.38 1.62.38.48 0 .92-.15 1.46-.36.83-.32 1.82-.7 3.07-.58 1.62.15 2.95.81 3.85 2.11-1.56 1.03-2.66 2.77-2.43 5.12.2 2.09 1.39 3.69 3.06 4.49-.24.65-.47 1.25-.78 1.88z"/></svg>
          Apple
        </button>
      </div>

      <!-- Register link -->
      <p class="mt-8 text-center text-sm text-text-muted">
        Don't have an account?
        <a href="{% url 'auth:register' %}" class="font-medium text-brand-600 hover:text-brand-700 transition">Create one</a>
      </p>
    </div>
  </div>
</div>
{% endblock %}
```

---

## 9. Borrower Portal (Trust-First)

### Dashboard

```html
<!-- templates/borrower/dashboard.html -->
{% extends "base/_base_borrower.html" %}

{% block content %}
<div class="space-y-8 animate-fade-in">
  <!-- Welcome Hero -->
  <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-brand-600 via-brand-700 to-brand-800 p-8 text-white">
    <div class="relative z-10">
      <p class="text-sm font-medium text-white/70">Good {{ time_of_day }},</p>
      <h1 class="mt-1 text-h2 text-white">{{ borrower.profile.first_name }} {{ borrower.profile.last_name }}</h1>
      {% if next_payment %}
      <div class="mt-4 inline-flex items-center gap-3 rounded-2xl bg-white/10 backdrop-blur-sm px-5 py-3">
        <div>
          <p class="text-xs text-white/60">Next Payment</p>
          <p class="text-lg font-bold font-tabular">${{ next_payment.amount_due|floatformat:2 }}</p>
        </div>
        <div class="h-8 w-px bg-white/20"></div>
        <div>
          <p class="text-xs text-white/60">Due</p>
          <p class="text-sm font-semibold">{{ next_payment.due_date|date:"M d, Y" }}</p>
        </div>
        <a href="{% url 'borrower:make-payment' %}"
           class="ml-2 rounded-xl bg-white px-4 py-2 text-sm font-semibold text-brand-700 transition hover:bg-white/90">
          Pay Now
        </a>
      </div>
      {% endif %}
    </div>
    <!-- Decorative circles -->
    <div class="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/5"></div>
    <div class="absolute -bottom-10 right-20 h-32 w-32 rounded-full bg-white/5"></div>
    <div class="absolute right-1/3 top-0 h-24 w-24 rounded-full bg-white/5"></div>
  </div>

  <!-- Stats -->
  <div class="grid grid-cols-2 gap-4 lg:grid-cols-4 stagger-children">
    {% include "components/cards/_stat_card.html" with title="Active Loans" value=stats.active_loans sparkline_data=stats.loan_trend %}
    {% include "components/cards/_stat_card.html" with title="Outstanding Balance" value=stats.total_outstanding sparkline_data=stats.balance_trend %}
    {% include "components/cards/_stat_card.html" with title="Credit Score" value=stats.credit_score change=stats.score_change trend="up" %}
    {% include "components/cards/_stat_card.html" with title="Payments Made" value=stats.payments_made change=stats.payments_change trend="up" %}
  </div>

  <!-- Two Column -->
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
    <!-- Active Loans (2/3) -->
    <div class="lg:col-span-2 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-h3 text-text-primary">Your Loans</h2>
        <a href="{% url 'borrower:loans' %}" class="text-sm font-medium text-brand-600 hover:text-brand-700 transition">View all</a>
      </div>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2"
           hx-get="{% url 'borrower:active-loans-partial' %}"
           hx-trigger="load"
           hx-swap="innerHTML">
        {% include "components/feedback/_skeleton.html" with type="card" %}
      </div>
    </div>

    <!-- Recent Activity (1/3) -->
    <div class="rounded-2xl border border-border bg-surface shadow-card">
      <div class="flex items-center justify-between px-5 py-4 border-b border-border">
        <h3 class="text-sm font-semibold text-text-primary">Recent Activity</h3>
      </div>
      <div class="p-5"
           hx-get="{% url 'borrower:activity-timeline' %}"
           hx-trigger="load"
           hx-swap="innerHTML">
        <div class="space-y-4">
          {% for i in "xxx"|make_list %}<div class="flex gap-3"><div class="skeleton h-6 w-6 rounded-full"></div><div class="flex-1 space-y-1.5"><div class="skeleton h-3.5 w-3/4"></div><div class="skeleton h-3 w-1/2"></div></div></div>{% endfor %}
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

---

## 10. Admin Dashboard (Command Center)

```html
<!-- templates/admin/dashboard.html -->
{% extends "base/_base_admin.html" %}

{% block breadcrumbs %}
<span class="font-medium text-text-primary">Dashboard</span>
{% endblock %}

{% block content %}
<div class="space-y-8">
  <!-- Page Header -->
  <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between animate-fade-in">
    <div>
      <h1 class="text-h1 text-text-primary">Dashboard</h1>
      <p class="mt-1 text-sm text-text-muted">Real-time overview of your lending operations.</p>
    </div>
    <div class="flex items-center gap-3">
      <div class="flex items-center rounded-xl border border-border p-0.5" x-data="{ range: '30d' }">
        {% for r in "7d,30d,90d,1y"|split:"," %}
        <button x-on:click="range = '{{ r }}'"
                :class="range === '{{ r }}' ? 'bg-surface-tertiary text-text-primary shadow-xs' : 'text-text-muted hover:text-text-secondary'"
                class="rounded-[10px] px-3 py-1.5 text-xs font-medium transition-all"
                hx-get="{% url 'admin:dashboard-stats' %}?range={{ r }}"
                hx-target="#kpi-grid"
                hx-swap="innerHTML">{{ r|upper }}</button>
        {% endfor %}
      </div>
      <button class="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 btn-glow">
        Export Report
      </button>
    </div>
  </div>

  <!-- KPI Grid -->
  <div id="kpi-grid" class="grid grid-cols-2 gap-4 lg:grid-cols-4 xl:grid-cols-6 stagger-children"
       hx-get="{% url 'admin:dashboard-stats' %}"
       hx-trigger="load"
       hx-swap="innerHTML">
    {% include "components/feedback/_skeleton.html" with type="stat-cards" %}
  </div>

  <!-- Charts Row -->
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-5">
    <!-- Application Pipeline (3/5) -->
    <div class="lg:col-span-3 rounded-2xl border border-border bg-surface p-6 shadow-card animate-fade-up" style="animation-delay: 100ms;">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h3 class="text-h3 text-text-primary">Application Pipeline</h3>
          <p class="text-sm text-text-muted mt-0.5">Volume and approval trends</p>
        </div>
        <div class="flex items-center gap-4 text-xs">
          <span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-brand-500"></span> Applications</span>
          <span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-success-500"></span> Approved</span>
        </div>
      </div>
      <div class="h-72">
        <canvas id="pipelineChart"></canvas>
      </div>
    </div>

    <!-- Risk Distribution (2/5) -->
    <div class="lg:col-span-2 rounded-2xl border border-border bg-surface p-6 shadow-card animate-fade-up" style="animation-delay: 200ms;">
      <h3 class="text-h3 text-text-primary mb-6">Portfolio Risk</h3>
      <div class="flex items-center gap-6">
        <div class="relative h-44 w-44 flex-shrink-0">
          <canvas id="riskDonutChart"></canvas>
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <span class="text-2xl font-bold text-text-primary font-tabular" id="total-loans-count">--</span>
            <span class="text-xs text-text-muted">Total Loans</span>
          </div>
        </div>
        <div class="flex-1 space-y-2.5" id="risk-legend">
          <!-- Populated by chart init -->
        </div>
      </div>
    </div>
  </div>

  <!-- Three Column: Reviews + Activity + Collections -->
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
    <!-- Pending Reviews -->
    <div class="rounded-2xl border border-border bg-surface shadow-card animate-fade-up" style="animation-delay: 300ms;">
      <div class="flex items-center justify-between px-5 py-4 border-b border-border">
        <div class="flex items-center gap-2">
          <h3 class="text-sm font-semibold text-text-primary">Pending Reviews</h3>
          {% if pending_count %}
          <span class="flex h-5 min-w-[20px] items-center justify-center rounded-full bg-brand-500 px-1.5 text-[10px] font-bold text-white">{{ pending_count }}</span>
          {% endif %}
        </div>
        <a href="{% url 'admin:applications-list' %}?status=under_review" class="text-xs font-medium text-brand-600 hover:text-brand-700 transition">View all</a>
      </div>
      <div class="divide-y divide-border max-h-80 overflow-y-auto"
           hx-get="{% url 'admin:pending-reviews-partial' %}"
           hx-trigger="load, every 30s"
           hx-swap="innerHTML">
        {% include "components/feedback/_skeleton.html" with type="table-row" %}
      </div>
    </div>

    <!-- Live Activity Feed -->
    <div class="rounded-2xl border border-border bg-surface shadow-card animate-fade-up" style="animation-delay: 400ms;">
      <div class="flex items-center justify-between px-5 py-4 border-b border-border">
        <div class="flex items-center gap-2">
          <h3 class="text-sm font-semibold text-text-primary">Live Activity</h3>
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-success-400 opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-success-500"></span>
          </span>
        </div>
      </div>
      <div id="activity-feed" class="divide-y divide-border max-h-80 overflow-y-auto mask-fade-b">
        <!-- WebSocket populated -->
        <div class="p-8 text-center text-sm text-text-muted">Connecting...</div>
      </div>
    </div>

    <!-- Collections Pipeline -->
    <div class="rounded-2xl border border-border bg-surface shadow-card animate-fade-up" style="animation-delay: 500ms;">
      <div class="flex items-center justify-between px-5 py-4 border-b border-border">
        <h3 class="text-sm font-semibold text-text-primary">Collections</h3>
        <a href="{% url 'admin:collections' %}" class="text-xs font-medium text-brand-600 hover:text-brand-700 transition">View all</a>
      </div>
      <div class="p-5 space-y-3"
           hx-get="{% url 'admin:collections-summary' %}"
           hx-trigger="load"
           hx-swap="innerHTML">
        {% for i in "xxxx"|make_list %}
        <div class="flex items-center justify-between"><div class="skeleton h-4 w-20"></div><div class="skeleton h-4 w-12"></div></div>
        {% endfor %}
      </div>
    </div>
  </div>

  <!-- Disbursement Heatmap -->
  <div class="rounded-2xl border border-border bg-surface p-6 shadow-card animate-fade-up" style="animation-delay: 600ms;">
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 class="text-h3 text-text-primary">Disbursement Activity</h3>
        <p class="text-sm text-text-muted mt-0.5">Daily disbursement volume over the past year</p>
      </div>
      <div class="text-right">
        <p class="text-2xl font-bold text-text-primary font-tabular">${{ ytd_disbursed|floatformat:0 }}</p>
        <p class="text-xs text-text-muted">Year to date</p>
      </div>
    </div>
    <div id="heatmap-container" class="overflow-x-auto">
      <!-- D3 calendar heatmap rendered here -->
    </div>
  </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="{% static 'js/charts/chart-theme.js' %}"></script>
<script src="{% static 'js/charts/dashboard-charts.js' %}"></script>
<script src="{% static 'js/charts/heatmap.js' %}"></script>
<script src="{% static 'js/websocket.js' %}"></script>
{% endblock %}
```

---

## 11. Investor Portal (Data-Dense)

```html
<!-- templates/investor/dashboard.html -->
{% extends "base/_base_investor.html" %}

{% block content %}
<div class="space-y-8 animate-fade-in">
  <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
    <div>
      <h1 class="text-h1 text-text-primary">Portfolio Overview</h1>
      <p class="mt-1 text-sm text-text-muted">Performance metrics updated daily at 2:00 AM UTC.</p>
    </div>
    <div class="flex items-center gap-3">
      <button class="rounded-xl border border-border px-4 py-2 text-sm font-medium text-text-secondary transition hover:bg-surface-secondary">
        Download Report
      </button>
    </div>
  </div>

  <!-- Hero KPIs (Glass) -->
  <div class="grid grid-cols-2 gap-4 lg:grid-cols-5 stagger-children">
    {% include "components/cards/_stat_card_glass.html" with title="Total Invested" value="$4.2M" icon="banknotes" %}
    {% include "components/cards/_stat_card_glass.html" with title="Current Value" value="$4.6M" icon="trending-up" subtitle="+9.5% all time" %}
    {% include "components/cards/_stat_card_glass.html" with title="IRR" value="14.2%" icon="chart-bar" %}
    {% include "components/cards/_stat_card_glass.html" with title="Default Rate" value="2.1%" icon="shield-exclamation" %}
    {% include "components/cards/_stat_card_glass.html" with title="PAR > 30" value="3.8%" icon="clock" %}
  </div>

  <!-- Returns Chart + Diversification -->
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
    <div class="lg:col-span-2 rounded-2xl border border-border bg-surface p-6 shadow-card">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-h3 text-text-primary">Returns Over Time</h3>
        <div class="flex gap-3 text-xs text-text-muted">
          <span class="flex items-center gap-1"><span class="h-2 w-2 rounded-full bg-brand-500"></span> Portfolio Value</span>
          <span class="flex items-center gap-1"><span class="h-2 w-2 rounded-full bg-success-500"></span> Cumulative Returns</span>
        </div>
      </div>
      <div class="h-72"><canvas id="returnsChart"></canvas></div>
    </div>

    <div class="space-y-6">
      <!-- By Risk Grade -->
      <div class="rounded-2xl border border-border bg-surface p-6 shadow-card">
        <h3 class="text-sm font-semibold text-text-primary mb-4">By Risk Grade</h3>
        <div class="h-40"><canvas id="gradeDonut"></canvas></div>
      </div>
      <!-- By Product -->
      <div class="rounded-2xl border border-border bg-surface p-6 shadow-card">
        <h3 class="text-sm font-semibold text-text-primary mb-4">By Product Type</h3>
        <div class="h-40"><canvas id="productDonut"></canvas></div>
      </div>
    </div>
  </div>

  <!-- Investments Table -->
  <div hx-get="{% url 'investor:investments-table' %}" hx-trigger="load" hx-swap="innerHTML">
    {% include "components/feedback/_skeleton.html" with type="table-row" %}
  </div>
</div>
{% endblock %}
```

---

## 12. Command Palette (Cmd+K)

```html
<!-- components/navigation/_command_palette.html -->
<div x-data="commandPalette()"
     x-on:open-command-palette.window="open()"
     x-on:keydown.meta.k.window.prevent="toggle()"
     x-on:keydown.ctrl.k.window.prevent="toggle()"
     x-cloak>

  <template x-teleport="body">
    <div x-show="isOpen" class="fixed inset-0 z-command-palette">
      <!-- Backdrop -->
      <div x-show="isOpen" x-transition.opacity.duration.150ms
           class="fixed inset-0 bg-black/50 backdrop-blur-sm"
           x-on:click="close()"></div>

      <!-- Panel -->
      <div class="fixed inset-x-0 top-[20vh] mx-auto max-w-xl px-4">
        <div x-show="isOpen"
             x-transition:enter="transition ease-out duration-200"
             x-transition:enter-start="opacity-0 scale-95 -translate-y-4"
             x-transition:enter-end="opacity-100 scale-100 translate-y-0"
             x-transition:leave="transition ease-in duration-100"
             x-transition:leave-start="opacity-100 scale-100"
             x-transition:leave-end="opacity-0 scale-95"
             class="overflow-hidden rounded-2xl border border-border bg-surface shadow-modal"
             x-trap="isOpen">

          <!-- Search Input -->
          <div class="flex items-center gap-3 border-b border-border px-4">
            <svg class="h-5 w-5 text-text-muted flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
            <input x-ref="searchInput"
                   x-model="query"
                   type="text"
                   placeholder="Search applications, borrowers, loans..."
                   class="flex-1 border-0 bg-transparent py-4 text-sm text-text-primary placeholder:text-text-muted focus:ring-0" />
            <kbd class="rounded bg-surface-tertiary px-1.5 py-0.5 text-[10px] font-medium text-text-muted">ESC</kbd>
          </div>

          <!-- Results -->
          <div class="max-h-80 overflow-y-auto p-2"
               x-show="query.length > 0"
               hx-get="{% url 'admin:command-search' %}"
               hx-trigger="input changed delay:200ms from:previous input"
               hx-target="this"
               hx-swap="innerHTML"
               hx-include="previous input">
          </div>

          <!-- Quick Actions (when empty) -->
          <div x-show="query.length === 0" class="p-2">
            <p class="px-3 py-2 text-[10px] font-semibold uppercase tracking-widest text-text-muted">Quick Actions</p>
            <a href="{% url 'admin:applications-list' %}" class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-text-secondary hover:bg-surface-secondary transition">
              <svg class="h-4 w-4 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/></svg>
              View Applications
              <kbd class="ml-auto text-[10px] text-text-muted">A</kbd>
            </a>
            <a href="{% url 'admin:borrowers-list' %}" class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-text-secondary hover:bg-surface-secondary transition">
              <svg class="h-4 w-4 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>
              View Borrowers
              <kbd class="ml-auto text-[10px] text-text-muted">B</kbd>
            </a>
            <a href="{% url 'admin:reports' %}" class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-text-secondary hover:bg-surface-secondary transition">
              <svg class="h-4 w-4 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"/></svg>
              Generate Report
              <kbd class="ml-auto text-[10px] text-text-muted">R</kbd>
            </a>
          </div>
        </div>
      </div>
    </div>
  </template>
</div>
```

---

## 13. Advanced HTMX Patterns

```js
// static/js/htmx-config.js

// CSRF for all requests
document.body.addEventListener('htmx:configRequest', (e) => {
  const token = document.querySelector('meta[name="csrf-token"]')?.content
  if (token) e.detail.headers['X-CSRFToken'] = token
})

// Subtle loading state
document.body.addEventListener('htmx:beforeRequest', (e) => {
  if (!e.detail.elt.closest('[data-no-loading]')) {
    e.detail.elt.style.opacity = '0.6'
    e.detail.elt.style.pointerEvents = 'none'
    e.detail.elt.style.transition = 'opacity 0.15s'
  }
})

document.body.addEventListener('htmx:afterRequest', (e) => {
  e.detail.elt.style.opacity = ''
  e.detail.elt.style.pointerEvents = ''
})

// Error handling
document.body.addEventListener('htmx:responseError', (e) => {
  const status = e.detail.xhr.status
  if (status === 401) window.location.href = '/auth/login/'
  else if (status === 403) Alpine.store('toasts').show('Permission denied', 'error')
  else if (status >= 500) Alpine.store('toasts').show('Something went wrong', 'error')
})

// Animate swapped content
document.body.addEventListener('htmx:afterSwap', (e) => {
  e.detail.target.querySelectorAll('.stagger-children > *').forEach((el, i) => {
    el.style.animationDelay = `${i * 50}ms`
  })
})

// View Transitions API integration
if (document.startViewTransition) {
  htmx.config.globalViewTransitions = true
}
```

### Common Patterns

```html
<!-- Infinite scroll -->
<div hx-get="{{ next_page_url }}" hx-trigger="revealed" hx-swap="afterend" hx-select="tr" data-no-loading>
  <td colspan="6" class="py-4 text-center">
    <svg class="mx-auto h-5 w-5 animate-spin text-brand-500" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" class="opacity-25"/><path d="M4 12a8 8 0 018-8" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
  </td>
</div>

<!-- Optimistic delete with undo -->
<button hx-delete="{% url 'admin:delete-item' item.id %}"
        hx-target="closest tr"
        hx-swap="outerHTML swap:0.3s"
        hx-confirm="Delete this item?"
        class="text-danger-500 hover:text-danger-600 transition">
  Delete
</button>

<!-- Live search with debounce -->
<input type="search"
       hx-get="{% url 'admin:search' %}"
       hx-trigger="input changed delay:250ms, search"
       hx-target="#results"
       hx-indicator="#search-spinner"
       name="q" />
```

---

## 14. Alpine.js Advanced Patterns

```js
// static/js/app.js

document.addEventListener('alpine:init', () => {

  // Theme store
  Alpine.store('theme', {
    dark: localStorage.theme === 'dark' || (!localStorage.theme && matchMedia('(prefers-color-scheme: dark)').matches),
    toggle() {
      this.dark = !this.dark
      localStorage.theme = this.dark ? 'dark' : 'light'
      document.documentElement.classList.toggle('dark', this.dark)
    },
  })

  // Toast notification store
  Alpine.store('toasts', {
    items: [],
    show(title, type = 'info', message = '', duration = 5000) {
      const id = Date.now()
      this.items.push({ id, title, message, type, visible: true })
      if (duration > 0) setTimeout(() => this.dismiss(id), duration)
    },
    dismiss(id) {
      const item = this.items.find(t => t.id === id)
      if (item) item.visible = false
      setTimeout(() => { this.items = this.items.filter(t => t.id !== id) }, 300)
    },
  })
})

// Global helper
window.showToast = (title, type, message) => Alpine.store('toasts').show(title, type, message)

// Count-up animation
window.countUp = (target, duration = 800) => ({
  current: 0,
  display: '0',
  init() {
    const start = performance.now()
    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
      this.current = Math.round(target * eased)
      this.display = this.current.toLocaleString()
      if (progress < 1) requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  },
})

// Command palette
window.commandPalette = () => ({
  isOpen: false,
  query: '',
  open() { this.isOpen = true; this.$nextTick(() => this.$refs.searchInput?.focus()) },
  close() { this.isOpen = false; this.query = '' },
  toggle() { this.isOpen ? this.close() : this.open() },
})
```

---

## 15. Charts & Data Visualization (Premium)

```js
// static/js/charts/chart-theme.js

const isDark = () => document.documentElement.classList.contains('dark')

function getChartTheme() {
  const dark = isDark()
  return {
    text: dark ? '#a1a1aa' : '#71717a',
    grid: dark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)',
    tooltip: {
      bg: dark ? '#18181b' : '#ffffff',
      border: dark ? '#27272a' : '#e4e4e7',
      text: dark ? '#fafafa' : '#09090b',
    },
  }
}

// Shared defaults
Chart.defaults.font.family = 'InterVariable, Inter, system-ui, sans-serif'
Chart.defaults.font.size = 12
Chart.defaults.plugins.legend.display = false
Chart.defaults.plugins.tooltip.backgroundColor = getChartTheme().tooltip.bg
Chart.defaults.plugins.tooltip.titleColor = getChartTheme().tooltip.text
Chart.defaults.plugins.tooltip.bodyColor = getChartTheme().tooltip.text
Chart.defaults.plugins.tooltip.borderColor = getChartTheme().tooltip.border
Chart.defaults.plugins.tooltip.borderWidth = 1
Chart.defaults.plugins.tooltip.padding = 12
Chart.defaults.plugins.tooltip.cornerRadius = 12
Chart.defaults.plugins.tooltip.displayColors = false

// Gradient helper
function createGradient(ctx, color, alpha1 = 0.15, alpha2 = 0) {
  const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height)
  gradient.addColorStop(0, color.replace(')', `, ${alpha1})`).replace('rgb', 'rgba'))
  gradient.addColorStop(1, color.replace(')', `, ${alpha2})`).replace('rgb', 'rgba'))
  return gradient
}
```

### Sparkline (Inline Mini Charts)

```js
// static/js/charts/sparkline.js
document.querySelectorAll('.sparkline').forEach(canvas => {
  const values = canvas.dataset.values.split(',').map(Number)
  const color = canvas.dataset.color || '#6172f3'
  const ctx = canvas.getContext('2d')

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: values.map((_, i) => i),
      datasets: [{
        data: values,
        borderColor: color,
        borderWidth: 1.5,
        fill: true,
        backgroundColor: createGradient(ctx, color, 0.1, 0),
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 3,
        pointHoverBackgroundColor: color,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: { x: { display: false }, y: { display: false } },
      interaction: { intersect: false },
    },
  })
})
```

---

## 16. Micro-Interactions & Animation System

### Page Load Stagger
All major pages use `stagger-children` on grid containers. Children animate in sequence with 50ms delay.

### Card Interactions
- **Hover lift**: `card-lift` class adds `translateY(-2px)` + shadow upgrade
- **Click feedback**: `active:scale-[0.98]` for buttons
- **Focus rings**: `focus-visible:ring-2 focus-visible:ring-brand-500/40 focus-visible:ring-offset-2`

### Status Transitions
When a loan status changes via HTMX swap, the badge animates in with `animate-bounce-subtle`.

### Number Animations
Financial values use `countUp()` Alpine directive to animate from 0 to target on page load.

### Celebration
On loan approval, trigger confetti:
```js
// static/js/utils/confetti.js
function celebrate() {
  const canvas = document.createElement('canvas')
  // ... canvas confetti implementation
  showToast('Application Approved!', 'success', 'The loan has been approved and queued for disbursement.')
}
```

---

## 17. White-Label Theming Engine

### How It Works

1. Institution's `branding` JSONB stores color palette + assets
2. Django context processor injects branding into every template
3. Base template renders CSS custom properties from branding data
4. All Tailwind `brand-*` classes resolve to these CSS variables
5. Result: zero code changes per institution, pure config

### Example Institution Config

```json
{
  "name": "First National Bank",
  "colors": {
    "50": "#f0fdf4", "100": "#dcfce7", "200": "#bbf7d0",
    "300": "#86efac", "400": "#4ade80", "500": "#22c55e",
    "600": "#16a34a", "700": "#15803d", "800": "#166534",
    "900": "#14532d", "950": "#052e16"
  },
  "logo_url": "/media/institutions/fnb/logo.svg",
  "logo_mark_url": "/media/institutions/fnb/mark.svg",
  "favicon_url": "/media/institutions/fnb/favicon.ico",
  "font_family": "IBM Plex Sans",
  "border_radius": "0.75rem",
  "login_image": "/media/institutions/fnb/login-hero.webp",
  "dark_mode_enabled": true
}
```

### Live Theme Preview (Admin Settings)

```html
<!-- admin/settings/branding.html -->
<div x-data="brandingEditor()" class="grid grid-cols-1 gap-8 lg:grid-cols-2">
  <!-- Editor -->
  <div class="space-y-6">
    <div>
      <label class="text-sm font-medium text-text-primary">Primary Color</label>
      <input type="color" x-model="colors[500]" x-on:input="updatePreview()"
             class="mt-1 h-10 w-full cursor-pointer rounded-xl border border-border" />
    </div>
    <!-- ... more controls ... -->
  </div>

  <!-- Live Preview -->
  <div class="rounded-2xl border border-border bg-surface p-4 shadow-card overflow-hidden" :style="previewStyles">
    <div class="rounded-xl bg-surface-secondary p-4">
      <div class="h-4 w-24 rounded" :style="`background: ${colors[600]}`"></div>
      <div class="mt-3 h-8 w-32 rounded" :style="`background: ${colors[500]}20`"></div>
      <button class="mt-4 rounded-lg px-4 py-2 text-sm font-medium text-white" :style="`background: ${colors[600]}`">
        Preview Button
      </button>
    </div>
  </div>
</div>
```

---

## 18. Advanced Forms & Validation

### Drag & Drop File Upload

```html
<!-- components/forms/_file_upload.html -->
<div x-data="fileUpload()" class="space-y-2">
  <label class="block text-sm font-medium text-text-primary">{{ label }}</label>

  <div x-on:dragover.prevent="isDragging = true"
       x-on:dragleave.prevent="isDragging = false"
       x-on:drop.prevent="handleDrop($event)"
       :class="isDragging ? 'border-brand-500 bg-brand-500/5' : 'border-border'"
       class="relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 transition-colors cursor-pointer"
       x-on:click="$refs.fileInput.click()">

    <input type="file" x-ref="fileInput" x-on:change="handleSelect($event)" accept="{{ accept }}" class="hidden" {% if multiple %}multiple{% endif %} name="{{ name }}" />

    <template x-if="!files.length">
      <div class="text-center">
        <svg class="mx-auto h-10 w-10 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"/></svg>
        <p class="mt-3 text-sm font-medium text-text-primary">Drop files here or click to browse</p>
        <p class="mt-1 text-xs text-text-muted">{{ help_text|default:"PDF, JPG, PNG up to 10MB" }}</p>
      </div>
    </template>

    <!-- File preview -->
    <template x-if="files.length">
      <div class="w-full space-y-2">
        <template x-for="(file, i) in files" :key="i">
          <div class="flex items-center gap-3 rounded-xl bg-surface-secondary p-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-500/10 text-brand-500 flex-shrink-0">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/></svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-text-primary truncate" x-text="file.name"></p>
              <p class="text-xs text-text-muted" x-text="formatSize(file.size)"></p>
            </div>
            <button type="button" x-on:click.stop="removeFile(i)" class="rounded-lg p-1.5 text-text-muted hover:text-danger-500 hover:bg-danger-50 transition">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
        </template>
      </div>
    </template>
  </div>
</div>

<script>
window.fileUpload = () => ({
  files: [],
  isDragging: false,
  handleDrop(e) {
    this.isDragging = false
    this.files = [...this.files, ...Array.from(e.dataTransfer.files)]
  },
  handleSelect(e) { this.files = [...this.files, ...Array.from(e.target.files)] },
  removeFile(i) { this.files.splice(i, 1) },
  formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / 1048576).toFixed(1) + ' MB'
  },
})
</script>
```

### OTP Input (MFA)

```html
<!-- components/forms/_otp_input.html -->
<div x-data="otpInput(6)" class="flex justify-center gap-2.5">
  <template x-for="(digit, i) in digits" :key="i">
    <input type="text" inputmode="numeric" maxlength="1"
           x-model="digits[i]"
           x-on:input="handleInput(i, $event)"
           x-on:keydown.backspace="handleBackspace(i, $event)"
           x-on:paste.prevent="handlePaste($event)"
           x-ref="input"
           :autofocus="i === 0"
           class="h-14 w-12 rounded-xl border-0 bg-surface-secondary text-center text-xl font-bold text-text-primary ring-1 ring-inset ring-border transition-shadow focus:bg-surface focus:ring-2 focus:ring-brand-500/40"
           :class="digits[i] && 'ring-brand-500/30'" />
  </template>
  <input type="hidden" name="otp_code" :value="digits.join('')" />
</div>

<script>
window.otpInput = (length) => ({
  digits: Array(length).fill(''),
  handleInput(i, e) {
    const val = e.target.value.replace(/\D/g, '')
    this.digits[i] = val.charAt(0)
    if (val && i < length - 1) this.$refs.input[i + 1]?.focus()
    if (this.digits.every(d => d)) this.$el.closest('form')?.requestSubmit()
  },
  handleBackspace(i, e) {
    if (!this.digits[i] && i > 0) { this.$refs.input[i - 1]?.focus() }
  },
  handlePaste(e) {
    const text = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, length)
    text.split('').forEach((char, i) => { this.digits[i] = char })
    this.$refs.input[Math.min(text.length, length - 1)]?.focus()
  },
})
</script>
```

---

## 19. Real-Time Engine (WebSockets + SSE)

```js
// static/js/websocket.js
class RealtimeConnection {
  constructor() {
    this.url = `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws/dashboard/`
    this.reconnectDelay = 1000
    this.maxDelay = 30000
    this.connect()
  }

  connect() {
    this.ws = new WebSocket(this.url)

    this.ws.onopen = () => {
      this.reconnectDelay = 1000
      document.querySelectorAll('[data-ws-status]').forEach(el => el.dataset.wsStatus = 'connected')
    }

    this.ws.onmessage = (e) => {
      const { type, data } = JSON.parse(e.data)
      this.dispatch(type, data)
    }

    this.ws.onclose = () => {
      document.querySelectorAll('[data-ws-status]').forEach(el => el.dataset.wsStatus = 'disconnected')
      setTimeout(() => this.connect(), this.reconnectDelay)
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxDelay)
    }
  }

  dispatch(type, data) {
    switch (type) {
      case 'loan.approved':
      case 'loan.submitted':
      case 'payment.received':
        this.addActivityItem(data)
        htmx.trigger('#kpi-grid', 'htmx:trigger')
        break
      case 'payment.received':
        showToast('Payment Received', 'success', `$${data.amount} from ${data.borrower_name}`)
        break
    }
  }

  addActivityItem(data) {
    const feed = document.getElementById('activity-feed')
    if (!feed) return

    // Remove "Connecting..." placeholder
    const placeholder = feed.querySelector('.text-center')
    if (placeholder) placeholder.remove()

    const item = document.createElement('div')
    item.className = 'flex items-center gap-3 px-5 py-3 animate-fade-down'
    item.innerHTML = `
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-500/10 flex-shrink-0">
        <svg class="h-4 w-4 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm text-text-primary truncate">${data.message}</p>
        <p class="text-xs text-text-muted">Just now</p>
      </div>
    `
    feed.prepend(item)
    while (feed.children.length > 50) feed.removeChild(feed.lastChild)
  }
}

if (document.getElementById('activity-feed')) new RealtimeConnection()
```

---

## 20. Notification Center

Notifications are rendered server-side via HTMX partial and grouped by time:

```html
<!-- Notification item partial (returned by server) -->
<a href="{{ notification.url }}" class="flex items-start gap-3 px-4 py-3 transition hover:bg-surface-secondary {% if not notification.read %}bg-brand-500/[0.02]{% endif %}">
  <div class="flex h-8 w-8 items-center justify-center rounded-lg flex-shrink-0 mt-0.5
    {% if notification.type == 'approval' %}bg-success-500/10 text-success-500
    {% elif notification.type == 'payment' %}bg-blue-500/10 text-blue-500
    {% elif notification.type == 'alert' %}bg-danger-500/10 text-danger-500
    {% else %}bg-surface-tertiary text-text-muted{% endif %}">
    {% include "components/icons/_icon.html" with name=notification.icon class="h-4 w-4" %}
  </div>
  <div class="flex-1 min-w-0">
    <p class="text-sm text-text-primary {% if not notification.read %}font-medium{% endif %} line-clamp-2">{{ notification.message }}</p>
    <p class="mt-0.5 text-xs text-text-muted">{{ notification.created_at|timesince }} ago</p>
  </div>
  {% if not notification.read %}
  <span class="mt-2 h-2 w-2 rounded-full bg-brand-500 flex-shrink-0"></span>
  {% endif %}
</a>
```

---

## 21. Responsive & Mobile-Native Feel

### Breakpoint Strategy

| Breakpoint | Target | Behavior |
|-----------|--------|----------|
| `< 640px` | Mobile | Single column, bottom tab nav, stacked cards, full-width modals |
| `640-1024px` | Tablet | 2-col grids, collapsible sidebar as overlay |
| `1024-1440px` | Desktop | Full sidebar, 3-4 col grids, side panels |
| `> 1440px` | Wide | Max-width container (1440px), centered content |

### Mobile Bottom Navigation

```html
<nav class="fixed bottom-0 inset-x-0 z-sticky border-t border-border bg-surface/95 backdrop-blur-glass lg:hidden safe-area-bottom">
  <div class="flex items-center justify-around py-1">
    {% for item in mobile_nav %}
    <a href="{{ item.url }}"
       class="flex flex-col items-center gap-0.5 px-4 py-2 text-[10px] font-medium transition
              {% if item.active %}text-brand-600{% else %}text-text-muted{% endif %}">
      {% include "components/icons/_icon.html" with name=item.icon class="h-5 w-5" %}
      {{ item.label }}
    </a>
    {% endfor %}
  </div>
</nav>
```

---

## 22. Accessibility (WCAG 2.2 AA)

- Focus visible: `focus-visible:ring-2 focus-visible:ring-brand-500/40 focus-visible:ring-offset-2`
- Color contrast: All text meets 4.5:1 ratio in both light and dark modes
- Modals: focus trap via `x-trap`, close on Escape, `role="dialog"`, `aria-modal="true"`
- Tables: `<th scope="col">`, `<caption>` for screen readers
- Live regions: `aria-live="polite"` on toast container and activity feed
- Skip nav: `<a href="#main" class="sr-only focus:not-sr-only ...">Skip to content</a>`
- Reduced motion: All animations disabled via `prefers-reduced-motion: reduce`
- Touch targets: Minimum 44x44px on mobile
- Form errors: `aria-invalid="true"`, `aria-describedby` linking to error message

---

## 23. Performance & Core Web Vitals

| Metric | Target | Strategy |
|--------|--------|----------|
| **LCP** | < 1.2s | Preload fonts, inline critical CSS, no render-blocking JS |
| **FID** | < 50ms | All JS deferred, Alpine.js is 15KB, HTMX is 14KB |
| **CLS** | < 0.05 | Skeleton loaders match final dimensions, font `size-adjust` |
| **FCP** | < 0.8s | Server-rendered HTML, no client-side hydration |

### Implementation

- **Font loading**: Self-hosted woff2 with `font-display: swap` + `size-adjust`
- **CSS**: Tailwind purge in production (typically < 20KB gzipped)
- **JS**: HTMX (14KB) + Alpine (15KB) = ~29KB total, deferred
- **Images**: WebP/AVIF, `loading="lazy"`, `srcset` for responsive
- **Charts**: Loaded only on pages that need them via `{% block extra_scripts %}`
- **Caching**: Django template fragment caching for sidebar, header
- **CDN**: Static assets served via CloudFront/CloudFlare
- **Compression**: Brotli via WhiteNoise or reverse proxy

---

## 24. Implementation Phases

### Phase 1 — Design System & Foundations (Week 1)
- [ ] Tailwind config with full token system
- [ ] Premium CSS (glass, grain, mesh gradients, animations)
- [ ] Self-hosted fonts (Inter Variable, JetBrains Mono)
- [ ] All base layouts (admin, borrower, investor, auth)
- [ ] Component library: buttons (5), inputs (8), cards (5), badges (4)
- [ ] Feedback components: toast, skeleton, empty state, spinner
- [ ] Navigation: glass sidebar, topbar, breadcrumbs, mobile nav
- [ ] Modal + drawer components
- [ ] Dark mode with system preference detection

### Phase 2 — Auth & Borrower Portal (Weeks 2-3)
- [ ] Cinematic login page (split-screen + mesh gradient)
- [ ] Register, forgot password, MFA setup/verify (OTP input)
- [ ] Borrower onboarding wizard (4 steps, HTMX partials)
- [ ] Borrower dashboard (hero card, stats, loan cards with progress rings)
- [ ] Loan application form (multi-step)
- [ ] Application status tracker
- [ ] Repayment schedule (visual timeline)
- [ ] Payment history table
- [ ] Profile & document management

### Phase 3 — Admin Command Center (Weeks 4-5)
- [ ] Dashboard: KPI grid, pipeline chart, risk donut, activity feed
- [ ] D3 calendar heatmap (disbursement activity)
- [ ] Command palette (Cmd+K) with server search
- [ ] Application list (table with filters, search, sort, pagination)
- [ ] Application review workspace (split view + timeline + docs)
- [ ] Borrower management (list + 360-degree detail view)
- [ ] Loan management with restructure modal
- [ ] Collections queue with priority sorting
- [ ] WebSocket live activity feed
- [ ] Notification center dropdown

### Phase 4 — Investor Portal (Week 6)
- [ ] Portfolio dashboard (glass KPIs, returns chart, diversification donuts)
- [ ] Performance analytics (time-series with period selection)
- [ ] Investment table with drill-down
- [ ] Loan marketplace (browse + invest modal)
- [ ] Report generation & download

### Phase 5 — White-Label & Polish (Week 7)
- [ ] Theming engine (CSS variables from institution config)
- [ ] Live branding preview in admin settings
- [ ] Sparkline integration in all stat cards
- [ ] Count-up animation on all financial values
- [ ] Stagger animations on all grid layouts
- [ ] Celebration confetti on loan approval
- [ ] Lottie animations for empty states + onboarding success

### Phase 6 — Quality & Production (Week 8)
- [ ] Accessibility audit (axe-core, screen reader testing)
- [ ] Lighthouse audit (target: 95+ on all metrics)
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Responsive audit (320px to 2560px)
- [ ] Performance profiling (60fps animations, no layout shift)
- [ ] Error state coverage (offline, 404, 500, empty data)
- [ ] Print stylesheets for reports
- [ ] Progressive enhancement verification (works without JS)
