# High-Fidelity Mockups - CDST Optimization Platform

## Overview

These high-fidelity mockups translate the wireframes into pixel-perfect designs using the established design system. Each mockup includes detailed specifications for colors, typography, spacing, interactions, and component states.

## Design Specifications

### Visual Hierarchy
- **Primary Actions**: Primary blue (#0ea5e9) with medium font weight
- **Secondary Actions**: Outlined buttons with primary blue border
- **Destructive Actions**: Error red (#ef4444) with appropriate warnings
- **Data Emphasis**: Bold typography (#374151) for key metrics
- **Supporting Text**: Medium gray (#6b7280) for descriptions

### Interactive States
- **Default**: Base colors with subtle shadows
- **Hover**: Slight elevation (2px transform) and deeper shadows
- **Focus**: 2px primary blue outline with 2px offset
- **Active**: Pressed state with reduced elevation
- **Disabled**: 50% opacity with not-allowed cursor

## 1. Login Page - High Fidelity

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │                           PATH CDST Platform                           │  ║
║  │                        Background: #f9fafb                            │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║    ┌─────────────────┐                                                       ║
║    │                 │                                                       ║
║    │   [PATH LOGO]   │  Color: #0ea5e9, Size: 64px height                   ║
║    │                 │                                                       ║
║    └─────────────────┘                                                       ║
║                                                                              ║
║         CDST Diagnostic Network Optimization                                 ║
║         Font: Inter Display, 24px, Weight: 600, Color: #374151              ║
║                                                                              ║
║    ┌─────────────────────────────────────────────────────────────────────┐  ║
║    │                                                                     │  ║
║    │  Username or Email                                                  │  ║
║    │  Font: Inter, 14px, Weight: 500, Color: #374151                    │  ║
║    │  ┌─────────────────────────────────────────────────────────────┐   │  ║
║    │  │ sarah.chen@hospital.org                                     │   │  ║
║    │  │ Font: Inter, 16px, Color: #111827                          │   │  ║
║    │  │ Background: #ffffff, Border: 1px #d1d5db                   │   │  ║
║    │  │ Padding: 12px 16px, Border-radius: 6px                     │   │  ║
║    │  └─────────────────────────────────────────────────────────────┘   │  ║
║    │                                                                     │  ║
║    └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║    ┌─────────────────────────────────────────────────────────────────────┐  ║
║    │                                                                     │  ║
║    │  Password                                                           │  ║
║    │  Font: Inter, 14px, Weight: 500, Color: #374151                    │  ║
║    │  ┌─────────────────────────────────────────────────────────────┐   │  ║
║    │  │ ••••••••••••••                                    [👁️ Show] │   │  ║
║    │  │ Font: Inter, 16px, Color: #111827                          │   │  ║
║    │  │ Background: #ffffff, Border: 1px #d1d5db                   │   │  ║
║    │  └─────────────────────────────────────────────────────────────┘   │  ║
║    │                                                                     │  ║
║    └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║    ☐ Remember me                    Forgot Password?                        ║
║    Font: Inter, 14px, Color: #6b7280   Font: Inter, 14px, Color: #0ea5e9   ║
║                                                                              ║
║    ┌─────────────────────────────────────────────────────────────────────┐  ║
║    │                                                                     │  ║
║    │                           Sign In                                   │  ║
║    │  Background: #0ea5e9, Color: #ffffff                               │  ║
║    │  Font: Inter, 16px, Weight: 500                                    │  ║
║    │  Padding: 12px 24px, Border-radius: 6px                           │  ║
║    │  Box-shadow: 0 1px 3px rgba(0,0,0,0.1)                            │  ║
║    │  Hover: Background: #0284c7, Transform: translateY(-1px)           │  ║
║    │                                                                     │  ║
║    └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║    Need help? Contact your administrator                                     ║
║    Font: Inter, 14px, Color: #9ca3af                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Interaction Specifications:**
- **Email Field Focus**: Border changes to #0ea5e9, box-shadow: 0 0 0 3px rgba(14,165,233,0.1)
- **Password Toggle**: Eye icon changes to crossed-eye when active, password text toggles visibility
- **Remember Me**: Custom checkbox with primary blue when checked
- **Sign In Hover**: Background darkens to #0284c7, subtle upward movement (1px)
- **Loading State**: Button shows spinner, text changes to "Signing In...", disabled state

## 2. Network Analyst Dashboard - High Fidelity

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ PATH CDST │ Dashboard │ Networks │ Optimization │ Results │ Reports │ Data │ ║
║ │ Background: #ffffff, Border-bottom: 1px #e5e7eb                         │ ║
║ │ Font: Inter, 14px, Weight: 500, Active: #0ea5e9                         │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ Dr. Sarah Chen                                          [🔔 2] [👤 SC] │ ║
║ │ Font: Inter, 16px, Weight: 500, Color: #111827                          │ ║
║ │ Background: #f9fafb, Padding: 12px 24px                                 │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Welcome back, Sarah                        Last Login: Today at 8:34 AM     ║
║ Font: Inter Display, 28px, Weight: 600     Font: Inter, 14px, Color: #6b7280 ║
║ Color: #111827                                                               ║
║                                                                              ║
║ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ ║
║ │   Active    │ │ Completed   │ │    Data     │ │      Quick Actions      │ ║
║ │  Scenarios  │ │ This Week   │ │   Quality   │ │                         │ ║
║ │             │ │             │ │             │ │ ┌─────────────────────┐ │ ║
║ │      3      │ │     12      │ │   98.5%     │ │ │   + New Scenario    │ │ ║
║ │   Running   │ │  Scenarios  │ │    Valid    │ │ │ Background: #0ea5e9 │ │ ║
║ │             │ │             │ │             │ │ │ Color: #ffffff      │ │ ║
║ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │ │ └─────────────────────┘ │ ║
║ │ │ ████    │ │ │ │ ✅ +25% │ │ │ │ ✅ Good │ │ │ ┌─────────────────────┐ │ ║
║ │ │ 75% Avg │ │ │ │ vs Last │ │ │ │ Status  │ │ │ │   📥 Import Data    │ │ ║
║ │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │ │ │ Background: #ffffff │ │ ║
║ └─────────────┘ └─────────────┘ └─────────────┘ │ │ Border: 1px #0ea5e9 │ │ ║
║ Background: #ffffff              Background: #f0fdf4 │ └─────────────────────┘ │ ║
║ Border: 1px #e5e7eb             Border: 1px #bbf7d0 └─────────────────────────┘ ║
║ Border-radius: 12px             Border-radius: 12px   Background: #ffffff      ║
║ Box-shadow: 0 1px 3px rgba(0,0,0,0.1)              Border: 1px #e5e7eb       ║
║                                                     Border-radius: 12px       ║
║                                                                              ║
║ Recent Activity                                           View All →         ║
║ Font: Inter, 18px, Weight: 600, Color: #111827                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ ⚙️  Cost Optimization Scenario completed                            2h │ ║
║ │ 📊  Regional Network analysis generated                             4h │ ║
║ │ ⬆️  Laboratory data imported successfully                           6h │ ║
║ │ 🔍  Performance review completed                                    1d │ ║
║ │                                                                       │ ║
║ │ Background: #ffffff, Border: 1px #e5e7eb                             │ ║
║ │ Border-radius: 8px, Padding: 16px                                    │ ║
║ │ Font: Inter, 14px, Color: #374151                                    │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Active Optimizations                                       Manage All →      ║
║ Font: Inter, 18px, Weight: 600, Color: #111827                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ Scenario Name           │ Progress      │ ETA        │ Actions          │ ║
║ │ Font: Inter, 12px, Weight: 600, Color: #6b7280                         │ ║
║ │─────────────────────────│───────────────│────────────│──────────────────│ ║
║ │ Regional Cost Opt.      │ ████████ 75%  │ 5 min      │ [View Details]   │ ║
║ │ Urban Access Study      │ ███    25%    │ 12 min     │ [View Details]   │ ║
║ │ Capacity Planning       │ █      10%    │ 18 min     │ [View Details]   │ ║
║ │                                                                         │ ║
║ │ Background: #ffffff, Border: 1px #e5e7eb                               │ ║
║ │ Progress bars: Background: #0ea5e9                                      │ ║
║ │ Font: Inter, 14px, Color: #374151                                      │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Interaction Specifications:**
- **Dashboard Cards**: Hover effect with subtle elevation (box-shadow: 0 4px 6px rgba(0,0,0,0.1))
- **Quick Actions**: Primary button hover darkens background, secondary button gets light blue background
- **Progress Bars**: Animated progress with smooth transitions, color coding by status
- **Activity Items**: Hover background changes to #f9fafb, clickable items have pointer cursor
- **Navigation**: Active tab has primary blue color and bottom border, hover states for inactive tabs

## 3. Optimization Scenario Builder - High Fidelity

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ PATH CDST │ Optimization │ Create Scenario                              │ ║
║ │ Breadcrumb: Font: Inter, 14px, Color: #6b7280                           │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Create Optimization Scenario                                                 ║
║ Font: Inter Display, 32px, Weight: 700, Color: #111827                      ║
║                                                                              ║
║ Step 2 of 4: Objective Weights                    ●●○○                      ║
║ Font: Inter, 16px, Weight: 500, Color: #6b7280                              ║
║ Progress dots: Active: #0ea5e9, Inactive: #d1d5db                           ║
║                                                                              ║
║ Adjust the importance of each optimization goal                              ║
║ (Total must equal 100%)                                                     ║
║ Font: Inter, 16px, Color: #6b7280                                           ║
║                                                                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │                                                                         │ ║
║ │ Distance Minimization                                            35%    │ ║
║ │ Font: Inter, 18px, Weight: 600, Color: #111827                         │ ║
║ │ ┌─────────────────────────────────────────────────────────────────────┐ │ ║
║ │ │████████████████████████████████████████████████████████████████████ │ │ ║
║ │ │ Background: #0ea5e9, Height: 8px, Border-radius: 4px              │ │ ║
║ │ │ Track background: #e5e7eb                                          │ │ ║
║ │ └─────────────────────────────────────────────────────────────────────┘ │ ║
║ │ Reduce transportation distances between service areas and labs          │ ║
║ │ Font: Inter, 14px, Color: #6b7280                                      │ ║
║ │                                                                         │ ║
║ │ Time Optimization                                                15%    │ ║
║ │ ┌─────────────────────────────────────────────────────────────────────┐ │ ║
║ │ │████████████████████████████                                        │ │ ║
║ │ │ Background: #10b981, Height: 8px, Border-radius: 4px              │ │ ║
║ │ └─────────────────────────────────────────────────────────────────────┘ │ ║
║ │ Minimize processing and transport time                                  │ ║
║ │                                                                         │ ║
║ │ Cost Reduction                                                   30%    │ ║
║ │ ┌─────────────────────────────────────────────────────────────────────┐ │ ║
║ │ │████████████████████████████████████████████████████████████         │ │ ║
║ │ │ Background: #f59e0b, Height: 8px, Border-radius: 4px              │ │ ║
║ │ └─────────────────────────────────────────────────────────────────────┘ │ ║
║ │ Lower operational and transport costs                                   │ ║
║ │                                                                         │ ║
║ │ Utilization Maximization                                         15%    │ ║
║ │ ┌─────────────────────────────────────────────────────────────────────┐ │ ║
║ │ │████████████████████████████                                        │ │ ║
║ │ │ Background: #8b5cf6, Height: 8px, Border-radius: 4px              │ │ ║
║ │ └─────────────────────────────────────────────────────────────────────┘ │ ║
║ │ Optimize laboratory capacity usage                                      │ ║
║ │                                                                         │ ║
║ │ Accessibility Enhancement                                         5%    │ ║
║ │ ┌─────────────────────────────────────────────────────────────────────┐ │ ║
║ │ │████████████                                                        │ │ ║
║ │ │ Background: #ef4444, Height: 8px, Border-radius: 4px              │ │ ║
║ │ └─────────────────────────────────────────────────────────────────────┘ │ ║
║ │ Ensure equitable service access                                         │ ║
║ │                                                                         │ ║
║ │ Background: #ffffff, Border: 1px #e5e7eb, Border-radius: 12px          │ ║
║ │ Padding: 24px, Box-shadow: 0 1px 3px rgba(0,0,0,0.1)                  │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Total: 100% ✅                                                               ║
║ Font: Inter, 16px, Weight: 600, Color: #16a34a                              ║
║                                                                              ║
║ ┌──────────────────┐  ┌─────────────────────────────────────────────────┐   ║
║ │ Reset to Defaults│  │ Use Preset ▼                                   │   ║
║ │ Background:      │  │ ┌─────────────────────────────────────────────┐ │   ║
║ │ #ffffff          │  │ │ • Cost-Focused (Cost 40%, Distance 30%)    │ │   ║
║ │ Border: 1px      │  │ │ • Access-Focused (Access 35%, Distance 25%)│ │   ║
║ │ #d1d5db          │  │ │ • Balanced (Equal weights)                  │ │   ║
║ └──────────────────┘  │ │ • Utilization-Focused (Util 40%, Cost 25%) │ │   ║
║                       │ └─────────────────────────────────────────────┘ │   ║
║                       └─────────────────────────────────────────────────┘   ║
║                                                                              ║
║                 ┌─────────────┐    ┌────────────────────────────┐            ║
║                 │ ← Previous  │    │ Next: Constraints →        │            ║
║                 │ Background: │    │ Background: #0ea5e9        │            ║
║                 │ #ffffff     │    │ Color: #ffffff             │            ║
║                 │ Border: 1px │    │ Font: Inter, 16px, 500    │            ║
║                 │ #d1d5db     │    │ Padding: 12px 24px        │            ║
║                 └─────────────┘    └────────────────────────────┘            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Interaction Specifications:**
- **Slider Controls**: Interactive sliders with custom styling, thumb color matches objective color
- **Real-time Updates**: Percentage values update as sliders move, total recalculates instantly
- **Validation**: Total percentage turns red if not 100%, prevents proceeding
- **Preset Dropdown**: Hover states for menu items, smooth slide-down animation
- **Progress Indicators**: Step completion animates with check marks and color changes

## 4. Results Map Visualization - High Fidelity

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ PATH CDST │ Results │ Regional Cost Optimization │ Map View             │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Geographic Visualization                                  Layers ▼          ║
║ Font: Inter Display, 24px, Weight: 600, Color: #111827                      ║
║                                                                              ║
║ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    ┌─────────────────────┐ ║
║ │   Current   │ │  Optimized  │ │ Comparison  │    │    Reset View       │ ║
║ │ Background: │ │ Background: │ │ Background: │    │ Background: #ffffff │ ║
║ │ #ffffff     │ │ #0ea5e9     │ │ #ffffff     │    │ Border: 1px #d1d5db │ ║
║ │ Border: 1px │ │ Color:      │ │ Border: 1px │    │ Color: #6b7280      │ ║
║ │ #d1d5db     │ │ #ffffff     │ │ #d1d5db     │    └─────────────────────┘ ║
║ └─────────────┘ └─────────────┘ └─────────────┘                            ║
║                                                                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │                                                                         │ ║
║ │    🏥 Central Lab (78% → 85%)                                           │ ║
║ │    Color: #16a34a (improved), Size: 24px                               │ ║
║ │         ╱╲╱╲╱╲╱╲╱╲                                                     │ ║
║ │        ╱            ╲                                                   │ ║
║ │       ╱  📍 Downtown  ╲ (25 → 31 tests)                                │ ║
║ │      ╱   Color: #0ea5e9 ╲ Font: Inter, 12px                           │ ║
║ │     ╱   📍 Midtown      ╲ (18 → 22 tests)                              │ ║
║ │    ╱    Color: #0ea5e9   ╲                                              │ ║
║ │   ╱     📍 Eastside      ╲ (12 → 15 tests)                             │ ║
║ │  ╱      Color: #0ea5e9    ╲                                             │ ║
║ │                                                                         │ ║
║ │  🏥 Regional Med (82% → 79%)                                            │ ║
║ │  Color: #f59e0b (decreased utilization)                                │ ║
║ │    ╱╲╱╲╱╲                                                               │ ║
║ │   ╱        ╲                                                            │ ║
║ │  ╱  📍 Northside ╲ (22 → 18 tests)                                     │ ║
║ │ ╱   📍 Westside   ╲ (15 → 12 tests)                                    │ ║
║ │                                                                         │ ║
║ │     🏥 Community Hub (65% → 88%)                                        │ ║
║ │     Color: #16a34a (significant improvement)                           │ ║
║ │       ╱╲╱╲                                                              │ ║
║ │      ╱    ╲                                                             │ ║
║ │     ╱ 📍   ╲ Suburbs (8 → 15 tests)                                    │ ║
║ │    ╱ Color: ╲                                                           │ ║
║ │   ╱  #10b981 ╲                                                          │ ║
║ │                                                                         │ ║
║ │ Background: #f9fafb (map background)                                    │ ║
║ │ Border: 1px #e5e7eb, Border-radius: 12px                               │ ║
║ │ Flow lines: Stroke-width varies by volume (2px-8px)                    │ ║
║ │ Flow colors: #0ea5e9 with 0.7 opacity                                  │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Legend                                                                       ║
║ Font: Inter, 16px, Weight: 600, Color: #111827                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ 🏥 Laboratory (utilization: before → after)                            │ ║
║ │ 📍 Service Area (tests: before → after)                                │ ║
║ │ ╱╲╱ Allocation flow (thickness = volume)                                │ ║
║ │ 🔴 Over-utilized  🟡 Under-utilized  🟢 Optimal                         │ ║
║ │                                                                         │ ║
║ │ Color coding:                                                           │ ║
║ │ • Green (#16a34a): Improved utilization                                 │ ║
║ │ • Blue (#0ea5e9): Service areas and flows                               │ ║
║ │ • Orange (#f59e0b): Decreased utilization                               │ ║
║ │ • Red (#ef4444): Over-utilized (>90%)                                   │ ║
║ │                                                                         │ ║
║ │ Background: #ffffff, Border: 1px #e5e7eb                                │ ║
║ │ Border-radius: 8px, Padding: 16px                                       │ ║
║ │ Font: Inter, 14px, Color: #374151                                       │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Map Controls: [+] [-] [🎯] [📍] [📏] [🔍]                                    ║
║ Background: #ffffff, Border: 1px #d1d5db, Border-radius: 6px                ║
║ Box-shadow: 0 2px 4px rgba(0,0,0,0.1)                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Interaction Specifications:**
- **Map Controls**: Hover effects with subtle background color changes
- **Laboratory Icons**: Hover shows tooltip with detailed utilization data
- **Service Area Markers**: Click to show allocation details in sidebar
- **Flow Lines**: Hover highlights the specific flow and shows transfer volume
- **Layer Toggle**: Smooth transitions between current/optimized views
- **Zoom Controls**: Smooth zoom animations with appropriate detail levels

## 5. Data Import Validation - High Fidelity

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ PATH CDST │ Data Management │ Import Data                              │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Import Data                                                                  ║
║ Font: Inter Display, 32px, Weight: 700, Color: #111827                      ║
║                                                                              ║
║ Step 2 of 3: Upload File                        ●●○                         ║
║ Font: Inter, 16px, Weight: 500, Color: #6b7280                              ║
║                                                                              ║
║ Upload your service areas data file                                          ║
║ Font: Inter, 16px, Color: #6b7280                                           ║
║                                                                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │                                                                         │ ║
║ │    📁 Drag and drop your file here                                      │ ║
║ │    Font: Inter, 18px, Weight: 500, Color: #6b7280                      │ ║
║ │    Icon: 48px, Color: #9ca3af                                           │ ║
║ │                                                                         │ ║
║ │                    or                                                   │ ║
║ │              ┌─────────────────┐                                        │ ║
║ │              │  Browse Files   │                                        │ ║
║ │              │ Background:     │                                        │ ║
║ │              │ #0ea5e9         │                                        │ ║
║ │              │ Color: #ffffff  │                                        │ ║
║ │              │ Border-radius:  │                                        │ ║
║ │              │ 6px             │                                        │ ║
║ │              └─────────────────┘                                        │ ║
║ │                                                                         │ ║
║ │ Supported formats: CSV, Excel (.xlsx), JSON                            │ ║
║ │ Maximum file size: 50 MB                                                │ ║
║ │ Font: Inter, 14px, Color: #9ca3af                                       │ ║
║ │                                                                         │ ║
║ │ Background: #f9fafb, Border: 2px dashed #d1d5db                        │ ║
║ │ Border-radius: 12px, Padding: 48px                                      │ ║
║ │ Hover: Border-color: #0ea5e9, Background: #f0f9ff                      │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ ✅ service_areas.csv uploaded successfully                                   ║
║ Font: Inter, 16px, Weight: 500, Color: #16a34a                              ║
║ File size: 2.3 MB │ 150 rows detected                                       ║
║ Font: Inter, 14px, Color: #6b7280                                           ║
║                                                                              ║
║ Validation Results                                                           ║
║ Font: Inter, 18px, Weight: 600, Color: #111827                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ ✅ File format valid                                                    │ ║
║ │ ✅ Required columns present                                             │ ║
║ │ ✅ Data types correct                                                   │ ║
║ │ ⚠️  3 warnings found                                                   │ ║
║ │ ❌ 2 errors found                                                       │ ║
║ │                                                                         │ ║
║ │ Success items: Color: #16a34a                                           │ ║
║ │ Warning items: Color: #f59e0b                                           │ ║
║ │ Error items: Color: #ef4444                                             │ ║
║ │ Font: Inter, 14px, Weight: 500                                          │ ║
║ │                                                                         │ ║
║ │ Background: #ffffff, Border: 1px #e5e7eb                                │ ║
║ │ Border-radius: 8px, Padding: 16px                                       │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║ Issues Found                                        Download Error Log →     ║
║ Font: Inter, 18px, Weight: 600, Color: #111827                              ║
║ ┌─────────────────────────────────────────────────────────────────────────┐ ║
║ │ ❌ Row 15: Invalid latitude value "invalid"                             │ ║
║ │ ❌ Row 23: Missing required field "population"                          │ ║
║ │ ⚠️  Row 45: Duplicate area_id "AREA012" - will be renamed               │ ║
║ │ ⚠️  Row 67: Population value seems high (5,000,000) - please verify    │ ║
║ │ ⚠️  Row 89: Coordinates place location in ocean - please verify        │ ║
║ │                                                                         │ ║
║ │ Error rows: Background: #fef2f2, Border-left: 4px #ef4444              │ ║
║ │ Warning rows: Background: #fffbeb, Border-left: 4px #f59e0b            │ ║
║ │ Font: Inter, 14px, Color: #374151                                       │ ║
║ │                                                                         │ ║
║ │ Background: #ffffff, Border: 1px #e5e7eb                                │ ║
║ │ Border-radius: 8px, Padding: 16px                                       │ ║
║ └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║         ┌─────────────┐    ┌─────────────┐    ┌────────────────────────────┐ ║
║         │ ← Previous  │    │ Fix Issues  │    │ Next: Review →             │ ║
║         │ Background: │    │ Background: │    │ Background: #d1d5db        │ ║
║         │ #ffffff     │    │ #f59e0b     │    │ Color: #9ca3af             │ ║
║         │ Border: 1px │    │ Color:      │    │ (Disabled - errors exist)  │ ║
║         │ #d1d5db     │    │ #ffffff     │    │ Cursor: not-allowed        │ ║
║         └─────────────┘    └─────────────┘    └────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Interaction Specifications:**
- **Drag & Drop Zone**: Visual feedback on dragover (border becomes solid, background lightens)
- **File Upload Progress**: Animated progress bar during upload with percentage
- **Validation Icons**: Animated check marks, warning triangles, and error X's
- **Error Highlighting**: Specific rows highlighted with appropriate colors and borders
- **Fix Issues Button**: Opens modal with inline editing capabilities for errors
- **Disabled Next Button**: Clear visual indication why progression is blocked

## Component States Documentation

### Button States
```css
/* Primary Button */
.btn-primary {
  /* Default */
  background: #0ea5e9;
  color: #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  
  /* Hover */
  background: #0284c7;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  
  /* Focus */
  outline: 2px solid #0ea5e9;
  outline-offset: 2px;
  
  /* Active */
  background: #0369a1;
  transform: translateY(0px);
  
  /* Disabled */
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}
```

### Form Input States
```css
.input {
  /* Default */
  border: 1px solid #d1d5db;
  background: #ffffff;
  
  /* Focus */
  border-color: #0ea5e9;
  box-shadow: 0 0 0 3px rgba(14,165,233,0.1);
  outline: none;
  
  /* Error */
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239,68,68,0.1);
  
  /* Success */
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22,163,74,0.1);
  
  /* Disabled */
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}
```

### Card Hover Effects
```css
.dashboard-card {
  transition: all 0.2s ease;
  
  /* Hover */
  transform: translateY(-2px);
  box-shadow: 0 10px 15px rgba(0,0,0,0.1);
}
```

These high-fidelity mockups provide pixel-perfect specifications for implementing the CDST Optimization Platform's user interface, ensuring consistency with the design system and optimal user experience across all workflows.