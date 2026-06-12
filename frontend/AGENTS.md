# Frontend - Kanban Studio

## Tech Stack
- NextJS 16 (React 19) with App Router
- Tailwind CSS 4 for styling
- `@dnd-kit/core` + `@dnd-kit/sortable` for drag and drop
- Vitest + Testing Library for unit tests
- Playwright for e2e tests

## Structure

```
src/
  app/
    layout.tsx       - Root layout with fonts (Space_Grotesk + Manrope), globals.css
    page.tsx         - Home page, renders <KanbanBoard />
    globals.css      - CSS variables for color scheme + Tailwind import
  components/
    KanbanBoard.tsx       - Main board component (client), manages board state, DnD context
    KanbanBoard.test.tsx  - Unit tests for board (render columns, rename, add/remove cards)
    KanbanColumn.tsx      - Column component with droppable area, card list, rename input
    KanbanCard.tsx        - Sortable card component with delete button
    KanbanCardPreview.tsx - Drag overlay preview of a card
    NewCardForm.tsx       - Inline form to add a new card to a column
  lib/
    kanban.ts       - Types (Card, Column, BoardData), initialData, moveCard logic, createId
    kanban.test.ts  - Unit tests for moveCard (reorder, move between columns, drop to end)
  test/
    setup.ts        - Imports @testing-library/jest-dom
    vitest.d.ts     - Type declarations
tests/
  kanban.spec.ts   - Playwright e2e tests (load board, add card, drag card)
```

## Key Design Decisions
- Board state lives in `KanbanBoard` via `useState`, initialized from `initialData` in `kanban.ts`
- Cards are keyed by ID in a `Record<string, Card>` map; columns store ordered `cardIds` arrays
- Column titles are editable via inline `<input>`
- Drag and drop uses dnd-kit's `DndContext` with `closestCorners` collision detection
- CSS variables defined in `globals.css` match the project color scheme

## Commands
- `npm run dev` - Start dev server on port 3000
- `npm run build` - Production build (will be configured for static export)
- `npm run test:unit` - Run Vitest unit tests
- `npm run test:e2e` - Run Playwright e2e tests
- `npm run lint` - Run ESLint

## Current State
- Fully functional client-side Kanban demo with hardcoded data
- Drag-and-drop, column rename, card create/delete all work
- Unit tests and e2e tests pass
- Not yet configured for static export or backend integration
- All text is in English (needs French translation)
