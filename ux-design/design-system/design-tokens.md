# CDST Optimization Platform - Design System

## Design Philosophy

The CDST platform design system is built on principles of **clarity, efficiency, and accessibility**. It reflects the professional healthcare environment while maintaining the approachability needed for diverse user types. The system emphasizes data-driven decision making through clear visual hierarchy and intuitive interactions.

### Core Principles
1. **Healthcare Professional** - Clean, trustworthy, and authoritative
2. **Data-Centric** - Prioritizes information clarity and readability
3. **Efficient Workflows** - Reduces cognitive load and task completion time
4. **Inclusive Design** - Accessible to users with diverse abilities and contexts
5. **Scalable Consistency** - Maintains coherence across all interfaces and devices

## Design Tokens

### Color Palette

#### Primary Colors
```css
/* PATH Brand Colors */
--color-primary-50: #f0f9ff;   /* Lightest blue */
--color-primary-100: #e0f2fe;  /* Very light blue */
--color-primary-200: #bae6fd;  /* Light blue */
--color-primary-300: #7dd3fc;  /* Medium light blue */
--color-primary-400: #38bdf8;  /* Medium blue */
--color-primary-500: #0ea5e9;  /* Primary blue */
--color-primary-600: #0284c7;  /* Dark blue */
--color-primary-700: #0369a1;  /* Darker blue */
--color-primary-800: #075985;  /* Very dark blue */
--color-primary-900: #0c4a6e;  /* Darkest blue */
```

#### Secondary Colors
```css
/* Healthcare Green - for success, health, positive metrics */
--color-secondary-50: #f0fdf4;
--color-secondary-100: #dcfce7;
--color-secondary-200: #bbf7d0;
--color-secondary-300: #86efac;
--color-secondary-400: #4ade80;
--color-secondary-500: #22c55e;  /* Secondary green */
--color-secondary-600: #16a34a;
--color-secondary-700: #15803d;
--color-secondary-800: #166534;
--color-secondary-900: #14532d;
```

#### Semantic Colors
```css
/* Status Colors */
--color-success-50: #f0fdf4;
--color-success-500: #22c55e;
--color-success-600: #16a34a;

--color-warning-50: #fffbeb;
--color-warning-500: #f59e0b;
--color-warning-600: #d97706;

--color-error-50: #fef2f2;
--color-error-500: #ef4444;
--color-error-600: #dc2626;

--color-info-50: #eff6ff;
--color-info-500: #3b82f6;
--color-info-600: #2563eb;
```

#### Neutral Colors
```css
/* Grayscale for text, backgrounds, borders */
--color-neutral-0: #ffffff;    /* Pure white */
--color-neutral-50: #f9fafb;   /* Background light */
--color-neutral-100: #f3f4f6;  /* Background */
--color-neutral-200: #e5e7eb;  /* Border light */
--color-neutral-300: #d1d5db;  /* Border */
--color-neutral-400: #9ca3af;  /* Text light */
--color-neutral-500: #6b7280;  /* Text medium */
--color-neutral-600: #4b5563;  /* Text */
--color-neutral-700: #374151;  /* Text dark */
--color-neutral-800: #1f2937;  /* Text darker */
--color-neutral-900: #111827;  /* Text darkest */
```

#### Data Visualization Colors
```css
/* Chart and map colors - colorblind friendly */
--color-data-1: #3b82f6;   /* Blue */
--color-data-2: #10b981;   /* Emerald */
--color-data-3: #f59e0b;   /* Amber */
--color-data-4: #ef4444;   /* Red */
--color-data-5: #8b5cf6;   /* Violet */
--color-data-6: #06b6d4;   /* Cyan */
--color-data-7: #84cc16;   /* Lime */
--color-data-8: #f97316;   /* Orange */

/* Heatmap colors */
--color-heatmap-low: #dbeafe;     /* Light blue */
--color-heatmap-medium: #3b82f6;  /* Medium blue */
--color-heatmap-high: #1d4ed8;    /* Dark blue */
--color-heatmap-critical: #1e40af; /* Very dark blue */
```

### Typography

#### Font Families
```css
/* Primary font - excellent readability for data */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Monospace for data tables and code */
--font-mono: 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', monospace;

/* Display font for headings (optional) */
--font-display: 'Inter Display', 'Inter', sans-serif;
```

#### Font Sizes
```css
/* Type scale - Major Third (1.25) */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
```

#### Font Weights
```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### Line Heights
```css
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### Spacing

#### Spacing Scale
```css
/* 8px base unit for consistent spacing */
--space-0: 0;
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-20: 5rem;    /* 80px */
--space-24: 6rem;    /* 96px */
```

### Border Radius
```css
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-base: 0.25rem;  /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-full: 9999px;   /* Fully rounded */
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

### Breakpoints
```css
--breakpoint-sm: 640px;   /* Tablet portrait */
--breakpoint-md: 768px;   /* Tablet landscape */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
--breakpoint-2xl: 1536px; /* Extra large desktop */
```

## Component Specifications

### Buttons

#### Primary Button
```css
.btn-primary {
  background-color: var(--color-primary-500);
  color: var(--color-neutral-0);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  font-size: var(--text-base);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--color-primary-600);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-primary:focus {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

.btn-primary:disabled {
  background-color: var(--color-neutral-300);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

#### Secondary Button
```css
.btn-secondary {
  background-color: transparent;
  color: var(--color-primary-600);
  border: 1px solid var(--color-primary-500);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  font-size: var(--text-base);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: var(--color-primary-50);
  border-color: var(--color-primary-600);
}
```

#### Button Sizes
```css
.btn-xs { padding: var(--space-1) var(--space-2); font-size: var(--text-xs); }
.btn-sm { padding: var(--space-2) var(--space-4); font-size: var(--text-sm); }
.btn-base { padding: var(--space-3) var(--space-6); font-size: var(--text-base); }
.btn-lg { padding: var(--space-4) var(--space-8); font-size: var(--text-lg); }
```

### Form Elements

#### Input Fields
```css
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-neutral-300);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-family: var(--font-primary);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}

.input:invalid {
  border-color: var(--color-error-500);
}

.input:disabled {
  background-color: var(--color-neutral-100);
  cursor: not-allowed;
}
```

#### Labels
```css
.label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-neutral-700);
  margin-bottom: var(--space-2);
}

.label-required::after {
  content: " *";
  color: var(--color-error-500);
}
```

### Cards

#### Base Card
```css
.card {
  background: var(--color-neutral-0);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
  border: 1px solid var(--color-neutral-200);
  overflow: hidden;
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-neutral-200);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--color-neutral-200);
  background: var(--color-neutral-50);
}
```

#### Dashboard Cards
```css
.dashboard-card {
  background: var(--color-neutral-0);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-neutral-200);
  padding: var(--space-6);
  transition: box-shadow 0.2s ease;
}

.dashboard-card:hover {
  box-shadow: var(--shadow-md);
}

.dashboard-card-metric {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-primary-600);
  line-height: var(--leading-tight);
}

.dashboard-card-label {
  font-size: var(--text-sm);
  color: var(--color-neutral-600);
  margin-top: var(--space-2);
}
```

### Navigation

#### Main Navigation
```css
.nav-main {
  background: var(--color-neutral-0);
  border-bottom: 1px solid var(--color-neutral-200);
  box-shadow: var(--shadow-sm);
}

.nav-item {
  padding: var(--space-4) var(--space-6);
  color: var(--color-neutral-600);
  text-decoration: none;
  font-weight: var(--font-medium);
  transition: color 0.2s ease, background-color 0.2s ease;
}

.nav-item:hover {
  color: var(--color-primary-600);
  background-color: var(--color-primary-50);
}

.nav-item.active {
  color: var(--color-primary-600);
  background-color: var(--color-primary-100);
  border-bottom: 2px solid var(--color-primary-500);
}
```

### Tables

#### Data Table
```css
.table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-neutral-0);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-base);
}

.table th {
  background: var(--color-neutral-50);
  padding: var(--space-4) var(--space-6);
  text-align: left;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
  color: var(--color-neutral-700);
  border-bottom: 1px solid var(--color-neutral-200);
}

.table td {
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-neutral-200);
  font-size: var(--text-sm);
  color: var(--color-neutral-700);
}

.table tr:hover {
  background-color: var(--color-neutral-50);
}

.table tr:last-child td {
  border-bottom: none;
}
```

### Status Indicators

#### Status Badges
```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-success {
  background: var(--color-success-50);
  color: var(--color-success-600);
}

.badge-warning {
  background: var(--color-warning-50);
  color: var(--color-warning-600);
}

.badge-error {
  background: var(--color-error-50);
  color: var(--color-error-600);
}

.badge-info {
  background: var(--color-info-50);
  color: var(--color-info-600);
}
```

### Loading States

#### Skeleton Loader
```css
.skeleton {
  background: linear-gradient(90deg, 
    var(--color-neutral-200) 25%, 
    var(--color-neutral-100) 50%, 
    var(--color-neutral-200) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: var(--radius-base);
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text {
  height: 1em;
  margin-bottom: var(--space-2);
}

.skeleton-title {
  height: 1.5em;
  width: 60%;
  margin-bottom: var(--space-4);
}
```

#### Progress Indicators
```css
.progress {
  width: 100%;
  height: var(--space-2);
  background: var(--color-neutral-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--color-primary-500);
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

.progress-indeterminate {
  background: linear-gradient(90deg, 
    transparent, 
    var(--color-primary-500), 
    transparent
  );
  background-size: 200% 100%;
  animation: progress-indeterminate 1.5s infinite;
}

@keyframes progress-indeterminate {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## Accessibility Specifications

### Focus Management
```css
/* High contrast focus indicators */
.focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

/* Skip links for keyboard navigation */
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--color-neutral-900);
  color: var(--color-neutral-0);
  padding: var(--space-2) var(--space-4);
  text-decoration: none;
  border-radius: var(--radius-base);
  z-index: 1000;
}

.skip-link:focus {
  top: 6px;
}
```

### Color Contrast
All color combinations meet WCAG 2.1 AA standards:
- Normal text: 4.5:1 contrast ratio minimum
- Large text: 3:1 contrast ratio minimum  
- UI components: 3:1 contrast ratio minimum

### Motion Preferences
```css
/* Respect user's motion preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

This design system provides a comprehensive foundation for creating consistent, accessible, and professional interfaces across the entire CDST Optimization Platform.