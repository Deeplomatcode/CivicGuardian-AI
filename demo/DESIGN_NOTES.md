# CivicGuardian AI - UI Design Notes

## Design Philosophy

This interface follows modern SaaS design principles with a focus on clarity, professionalism, and accessibility. The design system prioritizes generous spacing, subtle depth through shadows, and a refined colour palette suitable for government/civic applications.

## Design System

### Colour Palette

**Primary (Blues)**: Professional and trustworthy
- Primary-500: `#3b82f6` - Main interactive elements
- Primary-600: `#2563eb` - Hover states
- Primary-700: `#1d4ed8` - Active states

**Neutral (Greys)**: Clean and modern
- Neutral-50: `#f9fafb` - Background
- Neutral-100-300: Borders and dividers
- Neutral-600-900: Text hierarchy

**Semantic Colours**:
- Success (Green): `#22c55e` - Approvals, positive states
- Warning (Amber): `#f59e0b` - Demo banner, cautions
- Danger (Red): `#ef4444` - High risk, critical alerts
- Info (Blue): `#3b82f6` - Informational elements

### Typography

**Font Stack**: System fonts for optimal performance
- Sans: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`
- Mono: `'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace`

**Scale**: Modular scale from 12px to 30px
- Headers: 20-24px, weight 700
- Body: 14-16px, weight 400-500
- Small text: 12px, weight 500

### Spacing System

Consistent 4px base unit:
- Tight: 4-12px (components)
- Medium: 16-24px (sections)
- Generous: 32-48px (major sections)

### Shadows & Depth

Subtle layering for card-based layouts:
- `shadow-sm`: Minimal elevation for cards
- `shadow-md`: Hover states
- `shadow-lg`: Modals and overlays

### Border Radius

Rounded corners for modern feel:
- Small: 6px (badges, small elements)
- Medium: 8-12px (cards, buttons)
- Large: 16px (major sections)
- Full: 9999px (pills, status indicators)

## Component Design

### Demo Banner
- Sticky positioning at top
- Gradient background (amber)
- Icon + text for clear messaging
- Always visible to indicate demo mode

### Header
- Clean top navigation
- Logo with shield icon
- Status indicator with animated pulse
- Sticky below demo banner

### Cards
- White background with subtle border
- Generous padding (24px)
- Hover effect with shadow transition
- Rounded corners (16px)

### Badges
- Pill-shaped with uppercase text
- Colour-coded by semantic meaning
- Border for definition
- Small size (12px text)

### Buttons
- Three variants: Primary, Secondary, Success
- Hover lift effect (-1px translateY)
- Focus ring for accessibility
- Disabled state with reduced opacity

### Results Grid
- Single column on mobile
- Three columns on desktop (1024px+)
- Equal-width cards
- Consistent gap (24px)

## Accessibility Features

### WCAG AA Compliance
- Colour contrast ratios meet 4.5:1 minimum
- Focus indicators on all interactive elements
- Semantic HTML structure
- Keyboard navigation support

### Responsive Design
- Mobile-first approach
- Breakpoints: 768px (tablet), 1024px (desktop)
- Flexible grid layouts
- Touch-friendly tap targets (44px minimum)

### Motion & Animation
- Respects `prefers-reduced-motion`
- Subtle transitions (150-300ms)
- Purposeful animations only

### High Contrast Mode
- Increased border widths
- Enhanced visual separation
- Tested with system preferences

## Layout Structure

```
┌─────────────────────────────────────┐
│ Demo Banner (sticky)                │
├─────────────────────────────────────┤
│ Header (sticky)                     │
│ Logo | Status                       │
├─────────────────────────────────────┤
│                                     │
│ Main Content (max-width: 1400px)   │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Upload Section (card)           │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Preview Section (card)          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌───────┬───────┬───────┐          │
│ │ Risk  │Policy │Governor│          │
│ │ Panel │ Panel │ Panel  │          │
│ └───────┴───────┴───────┘          │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Action Buttons                  │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ Footer                              │
│ Links | Copyright                   │
└─────────────────────────────────────┘
```

## Design Constraints

### Preserved Functionality
- All JavaScript behaviour unchanged
- Same mock data and flows
- Identical file structure
- No new dependencies

### Technical Constraints
- Pure CSS (no preprocessors)
- No external CSS frameworks
- System fonts only
- Minimal JavaScript for styling

### Content Constraints
- "Demo Mode" banner always visible
- UK English spelling throughout
- AWS service names accurate
- Professional tone maintained

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Performance

- No external font loading
- Minimal CSS (< 15KB)
- No CSS-in-JS overhead
- Hardware-accelerated transforms

## Future Enhancements

Potential improvements for production:
- Dark mode support
- Additional colour themes
- Print stylesheet
- Offline support
- Progressive Web App features

## Design Rationale

### Why Card-Based Layout?
- Clear visual hierarchy
- Scannable information
- Modern SaaS aesthetic
- Easy to extend

### Why Generous Spacing?
- Reduces cognitive load
- Improves readability
- Professional appearance
- Better mobile experience

### Why Subtle Shadows?
- Depth without distraction
- Guides user attention
- Modern design trend
- Accessible contrast

### Why System Fonts?
- Instant loading
- Native feel
- Excellent readability
- Zero performance cost

## Maintenance Notes

### Updating Colours
All colours defined in `:root` CSS variables. Update once, applies everywhere.

### Adding Components
Follow existing patterns:
1. Use design system variables
2. Add hover/focus states
3. Test responsive behaviour
4. Verify accessibility

### Testing Checklist
- [ ] Test on mobile (375px width)
- [ ] Test on tablet (768px width)
- [ ] Test on desktop (1400px+ width)
- [ ] Test keyboard navigation
- [ ] Test with screen reader
- [ ] Test high contrast mode
- [ ] Test reduced motion preference
- [ ] Verify colour contrast ratios

---

**Last Updated**: March 2025  
**Design Version**: 1.0  
**Designer**: Kiro AI Assistant
