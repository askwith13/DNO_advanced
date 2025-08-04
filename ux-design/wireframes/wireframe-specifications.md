# Wireframe Specifications - CDST Optimization Platform

## Overview

These wireframes represent the core user interfaces and workflows for the CDST Diagnostic Network Optimization Platform. Each wireframe is designed to support the user personas and journeys identified in our research, with a focus on efficiency, clarity, and accessibility.

## Wireframe Key
```
[Button]     - Interactive button element
{Input}      - Form input field
<Dropdown>   - Dropdown/select element
[Tab 1|Tab 2] - Tabbed interface
+----------+  - Card/container boundary
|          |  - Content area
============  - Navigation separator
```

## 1. Authentication Flow

### 1.1 Login Page
```
+----------------------------------------------------------+
|                    PATH CDST Platform                    |
+----------------------------------------------------------+
|                                                          |
|    +----------------+                                    |
|    |   PATH Logo    |                                    |
|    +----------------+                                    |
|                                                          |
|         CDST Diagnostic Network Optimization            |
|                                                          |
|    +----------------------------------------+           |
|    |                                        |           |
|    |  {Username or Email}                   |           |
|    |                                        |           |
|    +----------------------------------------+           |
|                                                          |
|    +----------------------------------------+           |
|    |                                        |           |
|    |  {Password}                    [Show]  |           |
|    |                                        |           |
|    +----------------------------------------+           |
|                                                          |
|    [ ] Remember me        [Forgot Password?]            |
|                                                          |
|    +----------------------------------------+           |
|    |              [Sign In]                 |           |
|    +----------------------------------------+           |
|                                                          |
|    Need help? Contact your administrator                |
|                                                          |
+----------------------------------------------------------+
```

### 1.2 Password Reset
```
+----------------------------------------------------------+
|  [← Back to Login]              PATH CDST Platform      |
+----------------------------------------------------------+
|                                                          |
|                Reset Your Password                       |
|                                                          |
| Enter your email address and we'll send you a link      |
| to reset your password.                                 |
|                                                          |
|    +----------------------------------------+           |
|    |                                        |           |
|    |  {Email Address}                       |           |
|    |                                        |           |
|    +----------------------------------------+           |
|                                                          |
|    +----------------------------------------+           |
|    |           [Send Reset Link]            |           |
|    +----------------------------------------+           |
|                                                          |
|    [← Back to Sign In]                                  |
|                                                          |
+----------------------------------------------------------+
```

## 2. Dashboard Layouts

### 2.1 Network Analyst Dashboard
```
+----------------------------------------------------------+
| PATH CDST | [Dashboard] [Networks] [Optimization] [Results] [Reports] [Data] [Admin] |
+----------------------------------------------------------+
|  Dr. Sarah Chen                                [🔔] [👤] |
+----------------------------------------------------------+
|                                                          |
| Welcome back, Sarah                      Last Login: ... |
|                                                          |
| +-------------+ +-------------+ +-------------+ +-------+ |
| | Active      | | Completed   | | Data        | | Quick | |
| | Scenarios   | | This Week   | | Quality     | | Actions||
| |             | |             | |             | |       | |
| |     3       | |     12      | |    98.5%    | |[New]  | |
| |   Running   | | Scenarios   | |   Valid     | |[Import]||
| +-------------+ +-------------+ +-------------+ +-------+ |
|                                                          |
| Recent Activity                          [View All]      |
| +----------------------------------------------------+   |
| | ⚙️  Cost Optimization Scenario completed        2h |   |
| | 📊  Regional Network analysis generated         4h |   |
| | ⬆️  Laboratory data imported successfully       6h |   |
| | 🔍  Performance review completed                1d |   |
| +----------------------------------------------------+   |
|                                                          |
| Active Optimizations                     [Manage All]    |
| +----------------------------------------------------+   |
| | Scenario Name        | Progress | ETA      | Actions |   |
| |--------------------- |----------|----------|---------|   |
| | Regional Cost Opt.   | ████ 75% | 5 min    | [View]  |   |
| | Urban Access Study   | ██   25% | 12 min   | [View]  |   |
| | Capacity Planning    | █    10% | 18 min   | [View]  |   |
| +----------------------------------------------------+   |
|                                                          |
| System Alerts                            [Dismiss All]   |
| +----------------------------------------------------+   |
| | ⚠️  High utilization detected at Central Lab      |   |
| | ℹ️  New optimization algorithm available          |   |
| +----------------------------------------------------+   |
|                                                          |
+----------------------------------------------------------+
```

### 2.2 Laboratory Manager Dashboard
```
+----------------------------------------------------------+
| PATH CDST | [Dashboard] [Networks] [Results] [Reports]    |
+----------------------------------------------------------+
|  Michael Rodriguez                           [🔔] [👤] |
+----------------------------------------------------------+
|                                                          |
| Central Laboratory Performance Overview                  |
|                                                          |
| +-------------+ +-------------+ +-------------+ +-------+ |
| | Current     | | Today's     | | Staff       | | Alerts| |
| | Utilization | | Tests       | | On Duty     | |       | |
| |             | |             | |             | |   2   | |
| |    78%      | |    156      | |    12/15    | |Active | |
| |   Good      | |  +12% ↗️     | |   Available | |       | |
| +-------------+ +-------------+ +-------------+ +-------+ |
|                                                          |
| Weekly Utilization Trend                                 |
| +----------------------------------------------------+   |
| |    %                                               |   |
| | 100|                                               |   |
| |  75|     ●●●                                       |   |
| |  50|   ●     ●●●                                   |   |
| |  25| ●         ●●                                  |   |
| |   0+----+----+----+----+----+----+----+----+-----|   |
| |    Mon  Tue  Wed  Thu  Fri  Sat  Sun  Mon  Tue   |   |
| +----------------------------------------------------+   |
|                                                          |
| Recent Optimization Impact                               |
| +----------------------------------------------------+   |
| | Metric              | Before | After  | Change     |   |
| |---------------------|--------|--------|------------|   |
| | Daily Tests         |   142  |   156  | +14 (+9%)  |   |
| | Avg Distance (km)   |  12.5  |  10.8  | -1.7 (-14%)|   |
| | Cost per Test ($)   |  28.50 |  26.20 | -2.30 (-8%)|   |
| +----------------------------------------------------+   |
|                                                          |
| [View Detailed Report] [Download Analysis] [Contact IT] |
|                                                          |
+----------------------------------------------------------+
```

### 2.3 Healthcare Planner Dashboard
```
+----------------------------------------------------------+
| PATH CDST | [Dashboard] [Results] [Reports]              |
+----------------------------------------------------------+
|  Dr. Jennifer Park                           [🔔] [👤] |
+----------------------------------------------------------+
|                                                          |
| Regional Healthcare Network Executive Summary            |
|                                                          |
| +------------------+ +------------------+ +------------+ |
| | Total Monthly    | | Cost Savings     | | Service    | |
| | Tests Processed  | | This Quarter     | | Coverage   | |
| |                  | |                  | |            | |
| |     24,567       | |    $127,400      | |    94.2%   | |
| |   +8.3% ↗️        | |   +$23K ↗️        | |   +2.1% ↗️  | |
| +------------------+ +------------------+ +------------+ |
|                                                          |
| Key Performance Indicators                               |
| +----------------------------------------------------+   |
| | Metric                    | Current | Target | Status|   |
| |---------------------------|---------|--------|-------|   |
| | Average Distance (km)     |   11.2  |  <12   | ✅ Met |   |
| | Cost per Test ($)         |   24.80 |  <25   | ✅ Met |   |
| | Network Utilization (%)   |   76.5  |  >75   | ✅ Met |   |
| | Service Accessibility (%) |   89.3  |  >85   | ✅ Met |   |
| +----------------------------------------------------+   |
|                                                          |
| Strategic Insights                       [View Details]  |
| +----------------------------------------------------+   |
| | 💡 Opportunity: Eastern region shows 15% capacity  |   |
| |    surplus - consider expanding service areas      |   |
| |                                                    |   |
| | 📈 Trend: Urban laboratories achieving 95%+       |   |
| |    efficiency - model for rural expansion         |   |
| |                                                    |   |
| | ⚠️  Risk: Rural access declining in 3 counties    |   |
| |    - intervention recommended                      |   |
| +----------------------------------------------------+   |
|                                                          |
| [Generate Executive Report] [Schedule Review Meeting]    |
|                                                          |
+----------------------------------------------------------+
```

## 3. Network Management

### 3.1 Network List View
```
+----------------------------------------------------------+
| PATH CDST | Dashboard | [Networks] | Optimization | ... |
+----------------------------------------------------------+
|                                                          |
| Laboratory Networks                  [+ Create Network]  |
|                                                          |
| [All] [Active] [Inactive]           {Search networks...} |
|                                                          |
| +----------------------------------------------------+   |
| | Network Name         | Labs | Areas | Status | Actions|   |
| |----------------------|------|-------|--------|--------|   |
| | Regional Network     |  15  |  25   | Active | [Edit] |   |
| | Urban District       |   8  |  12   | Active | [Edit] |   |
| | Rural Expansion      |   5  |  18   | Draft  | [Edit] |   |
| | Pilot Program        |   3  |   6   |Inactive| [Edit] |   |
| +----------------------------------------------------+   |
|                                                          |
| [Bulk Actions ▼] [Import Network] [Export Selected]     |
|                                                          |
| Showing 4 of 4 networks                                 |
|                                                          |
+----------------------------------------------------------+
```

### 3.2 Network Details View
```
+----------------------------------------------------------+
| PATH CDST | Networks | [Regional Network]               |
+----------------------------------------------------------+
|                                                          |
| Regional Network                              [⚙️ Settings]|
| Created: Jan 15, 2024 | Last Modified: 2 days ago      |
|                                                          |
| [Overview] [Laboratories] [Service Areas] [Test Demand] |
|                                                          |
| Network Summary                                          |
| +----------------------------------------------------+   |
| | Laboratories: 15    | Service Areas: 25            |   |
| | Total Capacity: 3,500 tests/month                  |   |
| | Current Utilization: 76.5%                         |   |
| | Geographic Coverage: 2,400 km²                     |   |
| +----------------------------------------------------+   |
|                                                          |
| Quick Actions                                            |
| +----------------------------------------------------+   |
| | [📊 Run Optimization] [📈 View Analytics]          |   |
| | [📥 Import Data]      [📤 Export Network]          |   |
| +----------------------------------------------------+   |
|                                                          |
| Recent Activity                                          |
| +----------------------------------------------------+   |
| | • Optimization "Cost Reduction" completed      2h   |   |
| | • Laboratory "Central Lab" capacity updated    1d   |   |
| | • Service area "Downtown" demand data added    3d   |   |
| +----------------------------------------------------+   |
|                                                          |
| Performance Overview                                     |
| +----------------------------------------------------+   |
| |    Utilization %                                   |   |
| | 100|                                               |   |
| |  75|   ●●●●●                                       |   |
| |  50| ●       ●●                                    |   |
| |  25|           ●                                   |   |
| |   0+----+----+----+----+----+----+----+----+-----|   |
| |    Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep   |   |
| +----------------------------------------------------+   |
|                                                          |
+----------------------------------------------------------+
```

### 3.3 Laboratory Management
```
+----------------------------------------------------------+
| PATH CDST | Networks | Regional Network | [Laboratories]|
+----------------------------------------------------------+
|                                                          |
| Laboratories (15)                    [+ Add Laboratory]  |
|                                                          |
| [List View] [Map View]              {Search labs...}     |
|                                                          |
| Filters: <All Regions> <All Sizes> <All Status>         |
|                                                          |
| +----------------------------------------------------+   |
| | Lab ID  | Name           | Location    | Capacity |Status|
| |---------|----------------|-------------|----------|-----|
| | LAB001  | Central Lab    | Downtown    |   500    |Active|
| | LAB002  | Regional Med   | Midtown     |   300    |Active|
| | LAB003  | Community Hub  | Northside   |   200    |Active|
| | LAB004  | Express Center | Eastside    |   150    |Draft |
| | LAB005  | Rural Clinic   | Westfield   |   100    |Active|
| +----------------------------------------------------+   |
|                                                          |
| [Select All] [Bulk Edit] [Import Labs] [Export Data]    |
|                                                          |
| Showing 5 of 15 laboratories        [Previous] [Next]   |
|                                                          |
+----------------------------------------------------------+
```

### 3.4 Laboratory Details Form
```
+----------------------------------------------------------+
| PATH CDST | Networks | Regional Network | Laboratories | [Central Lab] |
+----------------------------------------------------------+
|                                                          |
| Central Laboratory                    [Save] [Cancel]    |
|                                                          |
| [Basic Info] [Capacity] [Test Types] [Hours] [Location] |
|                                                          |
| Basic Information                                        |
| +----------------------------------------------------+   |
| | Laboratory ID*  {LAB001}                           |   |
| | Name*          {Central Laboratory}                |   |
| | Address        {123 Main St, Downtown}            |   |
| | Phone          {+1-555-0101}                      |   |
| | Email          {central@example.com}              |   |
| +----------------------------------------------------+   |
|                                                          |
| Capacity & Resources                                     |
| +----------------------------------------------------+   |
| | Max Tests/Day*     {500}                           |   |
| | Max Tests/Month*   {12000}                         |   |
| | Staff Count*       {25}                            |   |
| | Equipment Units    {12}                            |   |
| | Utilization Factor {0.85}                          |   |
| +----------------------------------------------------+   |
|                                                          |
| Geographic Location                                      |
| +----------------------------------------------------+   |
| | Latitude*  {40.7128}    Longitude* {-74.0060}     |   |
| |                                                    |   |
| | +--------------------------------------------+     |   |
| | |                                            |     |   |
| | |              [MAP VIEW]                    |     |   |
| | |                 📍                         |     |   |
| | |                                            |     |   |
| | +--------------------------------------------+     |   |
| +----------------------------------------------------+   |
|                                                          |
| [Save Changes] [Reset Form] [Delete Laboratory]         |
|                                                          |
+----------------------------------------------------------+
```

## 4. Optimization Workflow

### 4.1 Scenario List
```
+----------------------------------------------------------+
| PATH CDST | Dashboard | Networks | [Optimization]       |
+----------------------------------------------------------+
|                                                          |
| Optimization Scenarios              [+ Create Scenario]  |
|                                                          |
| [All] [Running] [Completed] [Failed]  {Search scenarios}|
|                                                          |
| +----------------------------------------------------+   |
| | Scenario Name        | Network  | Status    | Actions |   |
| |----------------------|----------|-----------|---------|   |
| | Cost Optimization    | Regional | Running   | [View]  |   |
| | Access Improvement   | Urban    | Completed | [View]  |   |
| | Capacity Planning    | Rural    | Completed | [View]  |   |
| | Emergency Response   | Regional | Draft     | [Edit]  |   |
| +----------------------------------------------------+   |
|                                                          |
| Running Optimizations (2)                               |
| +----------------------------------------------------+   |
| | Cost Optimization    | ████████  75% | ETA: 5 min   |   |
| | Urban Redistribution | ███       25% | ETA: 12 min  |   |
| +----------------------------------------------------+   |
|                                                          |
| [Templates] [Import Scenario] [Bulk Actions]            |
|                                                          |
+----------------------------------------------------------+
```

### 4.2 Scenario Builder - Step 1: Configuration
```
+----------------------------------------------------------+
| PATH CDST | Optimization | [Create Scenario]            |
+----------------------------------------------------------+
|                                                          |
| Create Optimization Scenario                             |
|                                                          |
| Step 1 of 4: Basic Configuration    [●○○○]              |
|                                                          |
| +----------------------------------------------------+   |
| | Scenario Name*                                     |   |
| | {Regional Cost Optimization}                       |   |
| |                                                    |   |
| | Description                                        |   |
| | {Focus on reducing transportation costs while}    |   |
| | {maintaining service quality standards}           |   |
| |                                                    |   |
| | Network*                                           |   |
| | <Regional Network (15 labs, 25 areas)>            |   |
| |                                                    |   |
| | Optimization Type                                  |   |
| | ○ Balanced (recommended)                           |   |
| | ● Cost-focused                                     |   |
| | ○ Access-focused                                   |   |
| | ○ Utilization-focused                              |   |
| | ○ Custom                                           |   |
| +----------------------------------------------------+   |
|                                                          |
| Template Options                                         |
| +----------------------------------------------------+   |
| | [Use Template ▼] [Save as Template]                |   |
| +----------------------------------------------------+   |
|                                                          |
|                    [Cancel] [Next: Objectives →]        |
|                                                          |
+----------------------------------------------------------+
```

### 4.3 Scenario Builder - Step 2: Objective Weights
```
+----------------------------------------------------------+
| PATH CDST | Optimization | Create Scenario              |
+----------------------------------------------------------+
|                                                          |
| Create Optimization Scenario                             |
|                                                          |
| Step 2 of 4: Objective Weights      [●●○○]              |
|                                                          |
| Adjust the importance of each optimization goal          |
| (Total must equal 100%)                                 |
|                                                          |
| +----------------------------------------------------+   |
| | Distance Minimization                          35% |   |
| | ████████████████████████████████████████████████   |   |
| | Reduce transportation distances                    |   |
| |                                                    |   |
| | Time Optimization                              15% |   |
| | ████████████████████████                           |   |
| | Minimize processing and transport time             |   |
| |                                                    |   |
| | Cost Reduction                                 30% |   |
| | ████████████████████████████████████████████       |   |
| | Lower operational and transport costs              |   |
| |                                                    |   |
| | Utilization Maximization                       15% |   |
| | ████████████████████████                           |   |
| | Optimize laboratory capacity usage                 |   |
| |                                                    |   |
| | Accessibility Enhancement                       5% |   |
| | ████████                                           |   |
| | Ensure equitable service access                    |   |
| +----------------------------------------------------+   |
|                                                          |
| Total: 100% ✓                                           |
|                                                          |
| [Reset to Defaults] [Use Preset ▼]                      |
|                                                          |
|              [← Previous] [Next: Constraints →]         |
|                                                          |
+----------------------------------------------------------+
```

### 4.4 Scenario Builder - Step 3: Constraints
```
+----------------------------------------------------------+
| PATH CDST | Optimization | Create Scenario              |
+----------------------------------------------------------+
|                                                          |
| Create Optimization Scenario                             |
|                                                          |
| Step 3 of 4: Constraints            [●●●○]              |
|                                                          |
| Set limits and requirements for the optimization        |
|                                                          |
| Geographic Constraints                                   |
| +----------------------------------------------------+   |
| | [✓] Maximum Distance                               |   |
| |     {50} km from service area to laboratory        |   |
| |                                                    |   |
| | [✓] Maximum Travel Time                            |   |
| |     {90} minutes including transport delays        |   |
| +----------------------------------------------------+   |
|                                                          |
| Operational Constraints                                  |
| +----------------------------------------------------+   |
| | [✓] Enforce Laboratory Hours                       |   |
| |     Only assign tests during operational hours     |   |
| |                                                    |   |
| | [✓] Utilization Limits                             |   |
| |     Min: {30}% Max: {90}% capacity usage          |   |
| |                                                    |   |
| | [✓] Quality Threshold                              |   |
| |     Minimum {0.7} quality score required          |   |
| +----------------------------------------------------+   |
|                                                          |
| Advanced Options                                         |
| +----------------------------------------------------+   |
| | [ ] Priority Areas (weight certain areas higher)   |   |
| | [ ] Seasonal Adjustments (account for variations) |   |
| | [ ] Staff Constraints (detailed staffing limits)  |   |
| +----------------------------------------------------+   |
|                                                          |
|              [← Previous] [Next: Review →]               |
|                                                          |
+----------------------------------------------------------+
```

### 4.5 Optimization Progress Monitor
```
+----------------------------------------------------------+
| PATH CDST | Optimization | Regional Cost Optimization   |
+----------------------------------------------------------+
|                                                          |
| Regional Cost Optimization                    [Cancel]   |
| Status: Running | Started: 10:34 AM | ETA: 5 minutes    |
|                                                          |
| Overall Progress                                         |
| +----------------------------------------------------+   |
| | ████████████████████████████████████████████ 75%  |   |
| +----------------------------------------------------+   |
|                                                          |
| Algorithm Details                                        |
| +----------------------------------------------------+   |
| | Current Generation:  375 / 500                    |   |
| | Population Size:     200 individuals              |   |
| | Best Fitness:        0.847                        |   |
| | Convergence Rate:    0.023                        |   |
| | Elapsed Time:        11m 23s                      |   |
| +----------------------------------------------------+   |
|                                                          |
| Objective Progress                                       |
| +----------------------------------------------------+   |
| | Distance (35%):    ████████████████████ 87%       |   |
| | Cost (30%):        ████████████████ 72%           |   |
| | Time (15%):        ██████████████████████ 91%     |   |
| | Utilization (15%): ████████████ 58%               |   |
| | Access (5%):       ████████████████████████ 94%   |   |
| +----------------------------------------------------+   |
|                                                          |
| Live Updates                            [Auto-refresh ✓] |
| +----------------------------------------------------+   |
| | 10:45:23 - Generation 375 completed, fitness: 0.847|   |
| | 10:45:15 - Convergence improving, rate: 0.023      |   |
| | 10:44:58 - Generation 370 completed, fitness: 0.843|   |
| | 10:44:42 - Best solution updated                   |   |
| +----------------------------------------------------+   |
|                                                          |
| [View Intermediate Results] [Download Progress Log]     |
|                                                          |
+----------------------------------------------------------+
```

## 5. Results and Analytics

### 5.1 Results Dashboard
```
+----------------------------------------------------------+
| PATH CDST | Dashboard | Networks | Optimization | [Results] |
+----------------------------------------------------------+
|                                                          |
| Optimization Results: Regional Cost Optimization        |
| Completed: 10:47 AM | Duration: 13m 45s | Status: ✅    |
|                                                          |
| [Summary] [Map View] [Detailed Analysis] [Comparison]   |
|                                                          |
| Key Improvements                                         |
| +------------------+ +------------------+ +------------+ |
| | Distance         | | Cost Savings     | | Utilization| |
| | Reduction        | | Per Month        | | Improvement| |
| |                  | |                  | |            | |
| |    -18.3%        | |    $12,400       | |   +11.2%   | |
| |   (2.1 km avg)   | |   (-15.8%)       | |  (to 78.5%)| |
| +------------------+ +------------------+ +------------+ |
|                                                          |
| Allocation Changes Summary                               |
| +----------------------------------------------------+   |
| | Total Test Reallocations: 1,247 (52% of network)  |   |
| | Laboratories Affected: 12 of 15                   |   |
| | Service Areas Affected: 18 of 25                  |   |
| | Average Distance: 10.2 km (was 12.5 km)           |   |
| +----------------------------------------------------+   |
|                                                          |
| Top Recommendations                                      |
| +----------------------------------------------------+   |
| | 1. Redirect 85 tests from Rural Clinic to Central |   |
| | 2. Increase Community Hub utilization by 23%      |   |
| | 3. Consolidate specialized tests at Regional Med   |   |
| +----------------------------------------------------+   |
|                                                          |
| Implementation Impact                                    |
| +----------------------------------------------------+   |
| | Implementation Difficulty: Medium                  |   |
| | Staff Training Required: 3 laboratories           |   |
| | Expected ROI: 6.2 months                          |   |
| | Risk Level: Low                                    |   |
| +----------------------------------------------------+   |
|                                                          |
| [Generate Report] [Export Data] [Implement Changes]     |
|                                                          |
+----------------------------------------------------------+
```

### 5.2 Interactive Map View
```
+----------------------------------------------------------+
| PATH CDST | Results | Regional Cost Optimization | [Map View] |
+----------------------------------------------------------+
|                                                          |
| Geographic Visualization                  [Layers ▼]     |
|                                                          |
| [Current] [Optimized] [Comparison]       [Reset View]    |
|                                                          |
| +----------------------------------------------------+   |
| |                                                    |   |
| |    🏥 Central Lab (78% → 85%)                      |   |
| |         ╱╲╱╲╱                                      |   |
| |        ╱  📍  ╲ Downtown (25 → 31 tests)          |   |
| |       ╱   📍   ╲ Midtown (18 → 22 tests)          |   |
| |      ╱    📍    ╲ Eastside (12 → 15 tests)        |   |
| |                                                    |   |
| |  🏥 Regional Med (82% → 79%)                       |   |
| |    ╱╲╱╲                                            |   |
| |   ╱  📍  ╲ Northside (22 → 18 tests)              |   |
| |  ╱   📍   ╲ Westside (15 → 12 tests)              |   |
| |                                                    |   |
| |     🏥 Community Hub (65% → 88%)                   |   |
| |       ╱╲╱                                          |   |
| |      ╱ 📍 ╲ Suburbs (8 → 15 tests)                |   |
| |                                                    |   |
| +----------------------------------------------------+   |
|                                                          |
| Legend                                                   |
| +----------------------------------------------------+   |
| | 🏥 Laboratory (utilization: before → after)       |   |
| | 📍 Service Area (tests: before → after)           |   |
| | ╱╲╱ Allocation flow (thickness = volume)           |   |
| | 🔴 Over-utilized  🟡 Under-utilized  🟢 Optimal   |   |
| +----------------------------------------------------+   |
|                                                          |
| Map Controls: [+] [-] [🎯] [📍] [📏] [🔍]              |
|                                                          |
+----------------------------------------------------------+
```

### 5.3 Detailed Analysis Table
```
+----------------------------------------------------------+
| PATH CDST | Results | Regional Cost Optimization | [Analysis] |
+----------------------------------------------------------+
|                                                          |
| Detailed Allocation Analysis                             |
|                                                          |
| [By Laboratory] [By Service Area] [By Test Type]        |
|                                                          |
| Filter: <All Labs> <All Areas> <All Tests> {Search...}  |
|                                                          |
| +----------------------------------------------------+   |
| |Service Area|Lab      |Test Type |Before|After|Change|   |
| |------------|---------|----------|------|-----|------|   |
| |Downtown    |Central  |Culture   |  18  | 22  | +4   |   |
| |Downtown    |Central  |Sensitivity|  7  |  9  | +2   |   |
| |Midtown     |Regional |Culture   |  15  | 12  | -3   |   |
| |Midtown     |Central  |Culture   |   3  |  6  | +3   |   |
| |Northside   |Community|Culture   |  12  | 15  | +3   |   |
| |Eastside    |Central  |Rapid     |   8  | 11  | +3   |   |
| +----------------------------------------------------+   |
|                                                          |
| Summary Statistics                                       |
| +----------------------------------------------------+   |
| | Total Reallocations: 1,247 tests                  |   |
| | Average Distance Change: -2.3 km (-18.3%)         |   |
| | Cost Impact: -$12,400/month (-15.8%)              |   |
| | Utilization Improvement: +11.2 percentage points  |   |
| +----------------------------------------------------+   |
|                                                          |
| [Export to Excel] [Generate Summary] [Save Analysis]    |
|                                                          |
| Showing 6 of 247 allocations       [Previous] [Next]    |
|                                                          |
+----------------------------------------------------------+
```

## 6. Data Management

### 6.1 Import Data Wizard
```
+----------------------------------------------------------+
| PATH CDST | Dashboard | Networks | Optimization | Results | [Data] |
+----------------------------------------------------------+
|                                                          |
| Import Data                                              |
|                                                          |
| Step 1 of 3: Select Data Type       [●○○]               |
|                                                          |
| What type of data are you importing?                     |
|                                                          |
| +----------------------------------------------------+   |
| | ○ Laboratory Information                           |   |
| |   Import laboratory details, capacity, and        |   |
| |   test capabilities                                |   |
| |                                                    |   |
| | ● Service Areas                                    |   |
| |   Import geographic service areas and             |   |
| |   population data                                  |   |
| |                                                    |   |
| | ○ Test Demand                                      |   |
| |   Import historical or projected test             |   |
| |   demand by area and type                         |   |
| |                                                    |   |
| | ○ Cost Parameters                                  |   |
| |   Import transportation and processing            |   |
| |   cost data                                        |   |
| +----------------------------------------------------+   |
|                                                          |
| Target Network                                           |
| +----------------------------------------------------+   |
| | <Regional Network>                                 |   |
| +----------------------------------------------------+   |
|                                                          |
| [Download Template] [View Sample Data]                   |
|                                                          |
|                    [Cancel] [Next: Upload File →]       |
|                                                          |
+----------------------------------------------------------+
```

### 6.2 File Upload and Validation
```
+----------------------------------------------------------+
| PATH CDST | Data | Import Data                           |
+----------------------------------------------------------+
|                                                          |
| Import Data                                              |
|                                                          |
| Step 2 of 3: Upload File            [●●○]               |
|                                                          |
| Upload your service areas data file                     |
|                                                          |
| +----------------------------------------------------+   |
| |                                                    |   |
| |    📁 Drag and drop your file here                |   |
| |                                                    |   |
| |              or [Browse Files]                     |   |
| |                                                    |   |
| | Supported formats: CSV, Excel (.xlsx), JSON       |   |
| | Maximum file size: 50 MB                          |   |
| +----------------------------------------------------+   |
|                                                          |
| ✅ service_areas.csv uploaded successfully               |
| File size: 2.3 MB | 150 rows detected                   |
|                                                          |
| Validation Results                                       |
| +----------------------------------------------------+   |
| | ✅ File format valid                               |   |
| | ✅ Required columns present                        |   |
| | ✅ Data types correct                              |   |
| | ⚠️  3 warnings found                              |   |
| | ❌ 2 errors found                                  |   |
| +----------------------------------------------------+   |
|                                                          |
| Issues Found                         [Download Error Log]|
| +----------------------------------------------------+   |
| | Row 15: Invalid latitude value "invalid"          |   |
| | Row 23: Missing required field "population"       |   |
| | Row 45: Duplicate area_id "AREA012"               |   |
| +----------------------------------------------------+   |
|                                                          |
|         [← Previous] [Fix Issues] [Next: Review →]      |
|                                                          |
+----------------------------------------------------------+
```

## 7. Mobile Responsive Layouts

### 7.1 Mobile Dashboard
```
+---------------------------+
| PATH CDST          [☰] [👤] |
+---------------------------+
|                           |
| Dashboard                 |
|                           |
| +-----+ +-----+ +-------+ |
| |Active| |Done | |Quality| |
| |  3   | | 12  | | 98.5% | |
| |Scen. | |Week | | Valid | |
| +-----+ +-----+ +-------+ |
|                           |
| Recent Activity    [All]  |
| +-----------------------+ |
| | ⚙️ Cost Opt.      2h  | |
| | 📊 Analysis       4h  | |
| | ⬆️ Data Import    6h  | |
| +-----------------------+ |
|                           |
| Active Optimizations      |
| +-----------------------+ |
| | Regional Cost         | |
| | ████ 75% | 5 min      | |
| | [View Details]        | |
| +-----------------------+ |
| | Urban Access          | |
| | ██   25% | 12 min     | |
| | [View Details]        | |
| +-----------------------+ |
|                           |
| [+ New] [Import] [Help]   |
|                           |
+---------------------------+
```

### 7.2 Mobile Navigation Menu
```
+---------------------------+
| PATH CDST          [×]     |
+---------------------------+
|                           |
| Dr. Sarah Chen            |
| Network Analyst           |
|                           |
| +-----------------------+ |
| | 🏠 Dashboard          | |
| | 🏥 Networks           | |
| | ⚙️ Optimization       | |
| | 📊 Results & Analytics| |
| | 📋 Reports            | |
| | 💾 Data Management    | |
| | ⚡ Administration     | |
| +-----------------------+ |
|                           |
| +-----------------------+ |
| | 🔔 Notifications (2)  | |
| | ⚙️ Settings           | |
| | 📚 Help & Support     | |
| | 🚪 Sign Out           | |
| +-----------------------+ |
|                           |
+---------------------------+
```

These wireframes provide a comprehensive foundation for developing the user interfaces of the CDST Optimization Platform. Each screen is designed to support the identified user journeys while maintaining consistency with the design system and accessibility requirements.