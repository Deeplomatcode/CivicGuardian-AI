# Design Specification: CivicGuardian AI (Sky-Blue Fluent)

## Aesthetic Foundation

**Theme:** Professional Sky-Blue Fluent - Trust-centered caseworker tool

**Color Palette:**
- Base Background: Ultra-White (#FFFFFF) with Sky Wash (#F0F9FF)
- Primary Accent: Deep Sky Blue (#005EB8) - headers, core identity
- AI Energy: Electric Cyan (#00A9CE) - glowing borders, active states
- Success: NHS Green (#007F3B)
- Alert: Warm Amber (#FFA500)
- Text Primary: Near-Black (#1A1A1A)
- Text Secondary: Steel Gray (#64748B)

**Typography:**
- UI Text: Inter (Sans-Serif) - clean, professional
- AI Streams: JetBrains Mono (Monospace) - technical authenticity
- Headers: Inter Bold
- Metrics: Inter Medium

## Component Architecture

**Layout System:**
- Bento Grid: 12-column CSS Grid with variable-sized cards
- Responsive breakpoints: Mobile (1 col), Tablet (2 col), Desktop (12 col)
- Gap: 24px between cards

**Glassmorphism Standard:**
```css
background: rgba(255, 255, 255, 0.75);
backdrop-filter: blur(12px) saturate(180%);
border: 1.5px solid rgba(0, 94, 184, 0.08);
box-shadow: 0 20px 25px -5px rgba(0, 94, 184, 0.04);
border-radius: 16px;
```

**Animation Principles:**
- Smooth, professional (cubic-bezier(0.4, 0, 0.2, 1))
- Slow, deliberate (0.4s-0.6s transitions)
- Purposeful glows (not jarring)
- Accessibility: respect prefers-reduced-motion

**Trust Signals:**
- NHS-style color palette
- Clear, large typography
- Abundant whitespace
- Professional metrics display
- Calm, measured animations

## 5-Section Command Center Layout

1. **Header Analytics Bar** - Live KPI metrics
2. **Forensic Drop Zone** - Document upload with cyan glow
3. **Agentic Thinking Stream** - Real-time AI processing log
4. **Impact Visualization** - Risk radar chart
5. **Drafting Suite** - AI-generated response display

## Design Goals

- Professional tool for NHS/Government caseworkers
- Trust-centered, not cybersecurity-focused
- Data-dense but readable
- Demonstrates AI transparency
- Social Good category positioning
