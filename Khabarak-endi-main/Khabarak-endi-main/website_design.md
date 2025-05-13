# Website Design for "خبرك عندي" (Your News)

## Overview
This document outlines the design specifications for "خبرك عندي", a Yemeni news aggregator website that will collect and display news from various Yemeni sources. The website will feature RTL (Right-to-Left) support for Arabic content and will be responsive for both desktop and mobile devices.

## Design Requirements

### 1. RTL Support
- Full Right-to-Left text direction support for Arabic content
- Proper text alignment and layout for RTL reading
- RTL-compatible navigation and UI elements
- Proper handling of mixed content (Arabic text and Latin numbers/URLs)

### 2. Responsive Design
- Mobile-first approach to ensure optimal experience on smartphones
- Fluid layout that adapts to tablet and desktop screens
- Touch-friendly UI elements for mobile users
- Optimized reading experience across all device sizes

### 3. Branding
- Logo design for "خبرك عندي" that reflects Yemeni identity
- Color scheme inspired by Yemeni flag (red, white, black, green)
- Modern, clean typography using Arabic web fonts
- Consistent visual identity across all pages

### 4. Layout Structure
- Header with logo, navigation, and search functionality
- Main content area with featured news and category sections
- Sidebar for trending/most read news
- Footer with additional links and information
- Sticky navigation for easy access to categories

## Wireframes

### Desktop Layout
```
+---------------------------------------------------------------+
|  LOGO  |  SEARCH  |  NAVIGATION MENU  |  DATE/TIME  | LANG    |
+---------------------------------------------------------------+
|                       FEATURED NEWS                           |
|  +---------------------+  +---------------------+             |
|  |                     |  |                     |             |
|  |    MAIN HEADLINE    |  |   SECOND HEADLINE   |             |
|  |                     |  |                     |             |
|  +---------------------+  +---------------------+             |
+---------------------------------------------------------------+
|  CATEGORY TABS: Politics | Economy | Local | Sports | Culture |
+---------------------------------------------------------------+
|                         |                                     |
|                         |                                     |
|   CATEGORY NEWS LIST    |      TRENDING/MOST READ NEWS        |
|                         |                                     |
|                         |                                     |
|                         |                                     |
+---------------------------------------------------------------+
|                         FOOTER                                |
|  About | Contact | Sources | Privacy Policy | Terms of Use    |
+---------------------------------------------------------------+
```

### Mobile Layout
```
+----------------------------+
|  LOGO  |  SEARCH  | MENU ≡ |
+----------------------------+
|                            |
|      FEATURED NEWS         |
|                            |
+----------------------------+
| CATEGORY TABS (scrollable) |
+----------------------------+
|                            |
|    CATEGORY NEWS LIST      |
|                            |
|                            |
+----------------------------+
|    TRENDING/MOST READ      |
|                            |
+----------------------------+
|          FOOTER            |
+----------------------------+
```

## Color Scheme
- Primary: #CE1126 (Red - from Yemeni flag)
- Secondary: #007A3D (Green - from Yemeni flag)
- Neutral: #FFFFFF (White - from Yemeni flag)
- Background: #F5F5F5 (Light gray)
- Text: #333333 (Dark gray)
- Accent: #000000 (Black - from Yemeni flag)

## Typography
- Headings: "Tajawal Bold" - A modern Arabic font with good readability
- Body text: "Dubai Regular" - Clean and legible for longer text
- Font sizes:
  - Main headlines: 24px (desktop) / 20px (mobile)
  - Section headings: 20px (desktop) / 18px (mobile)
  - Body text: 16px (desktop) / 14px (mobile)
  - Metadata: 12px (desktop) / 11px (mobile)

## UI Components

### News Card
```
+----------------------------------+
|                                  |
|             IMAGE                |
|                                  |
+----------------------------------+
| HEADLINE (2 lines max)           |
+----------------------------------+
| SOURCE | CATEGORY | TIME         |
+----------------------------------+
| Brief excerpt (3 lines max)...   |
+----------------------------------+
```

### Navigation Menu
- Sticky top navigation on desktop
- Hamburger menu on mobile that expands to full-screen overlay
- Category navigation as horizontal scrollable tabs on mobile

### Search Functionality
- Search icon that expands to full-width search bar when clicked
- Auto-suggestions based on popular searches
- Filter options by date, source, and category

## Technical Implementation Notes

### RTL Support
- Use `dir="rtl"` on HTML elements
- Use CSS `direction: rtl;` and `text-align: right;`
- Implement logical properties (e.g., `margin-inline-start` instead of `margin-left`)
- Use CSS Grid and Flexbox for layout to handle RTL/LTR switching

### Responsive Design
- Use CSS media queries for different screen sizes
- Implement a mobile-first approach with progressive enhancement
- Use relative units (rem, em, %) instead of fixed pixels
- Ensure touch targets are at least 44x44px for mobile usability

### Performance Optimization
- Lazy loading for images and non-critical content
- Optimize images for web (WebP format with fallbacks)
- Implement caching strategies for news content
- Minimize HTTP requests by combining CSS/JS files

## Next Steps
1. Create detailed mockups based on these wireframes
2. Develop HTML/CSS templates with RTL support
3. Implement responsive design
4. Create logo and branding elements
5. Develop UI components
6. Integrate with news aggregation system
