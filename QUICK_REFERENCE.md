# Quick Reference - MedAssist Design System

## 🎨 Color Classes

```html
<!-- Text Colors -->
<p class="text-primary">Primary text (#111827)</p>
<p class="text-secondary">Secondary text (#6B7280)</p>
<p class="text-tertiary">Tertiary text (#9CA3AF)</p>
<p class="text-blue">Blue accent (#2563EB)</p>
<p class="text-success">Success (#059669)</p>
<p class="text-warning">Warning (#D97706)</p>
<p class="text-error">Error (#DC2626)</p>

<!-- Background Colors -->
<div class="bg-white">White background</div>
<div class="bg-gray-50">Light gray background</div>
<div class="bg-primary">Primary blue background</div>
```

## 🔘 Buttons

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-ghost">Ghost</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-success">Success</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>
<button class="btn btn-primary btn-full">Full Width</button>

<!-- With Icon -->
<button class="btn btn-primary">
    <i class="fas fa-save"></i> Save
</button>
```

## 📝 Forms

```html
<div class="form-group">
    <label class="form-label">Label</label>
    <input type="text" class="form-input" placeholder="Enter text">
    <span class="form-helper">Helper text</span>
</div>

<!-- Required Field -->
<label class="form-label form-label-required">Email</label>

<!-- Error State -->
<input class="form-input form-input-error" />
<span class="form-error">Error message</span>

<!-- Select -->
<select class="form-select">
    <option>Option 1</option>
</select>

<!-- Textarea -->
<textarea class="form-textarea"></textarea>

<!-- Checkbox -->
<div class="form-check">
    <input type="checkbox" class="form-check-input" id="check1">
    <label class="form-check-label" for="check1">Label</label>
</div>
```

## 📦 Cards

```html
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Title</h3>
        <p class="card-subtitle">Subtitle</p>
    </div>
    <div class="card-body">
        Content
    </div>
    <div class="card-footer">
        Footer
    </div>
</div>

<!-- Variants -->
<div class="card card-hover">Hoverable</div>
<div class="card card-flat">No shadow</div>
<div class="card card-elevated">Large shadow</div>
```

## 📐 Layout

```html
<!-- Container -->
<div class="container">Max-width 1200px</div>
<div class="container container-sm">Max-width 640px</div>

<!-- Grid -->
<div class="grid grid-cols-2 gap-6">
    <div>Column 1</div>
    <div>Column 2</div>
</div>

<div class="grid grid-cols-3 gap-4">
    <div>Col 1</div>
    <div>Col 2</div>
    <div>Col 3</div>
</div>

<!-- Flexbox -->
<div class="flex items-center justify-between">
    <span>Left</span>
    <span>Right</span>
</div>

<div class="flex flex-col gap-4">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

## 🏷️ Badges

```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-error">Error</span>
<span class="badge badge-gray">Gray</span>
```

## 🚨 Alerts

```html
<div class="alert alert-info">Info message</div>
<div class="alert alert-success">Success message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-error">Error message</div>
```

## 📊 Tables

```html
<div class="table-container">
    <table class="table">
        <thead>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </tbody>
    </table>
</div>
```

## 🎯 Spacing

```html
<!-- Margin -->
<div class="mt-4">Margin top 16px</div>
<div class="mb-6">Margin bottom 24px</div>

<!-- Padding -->
<div class="p-4">Padding 16px</div>
<div class="p-6">Padding 24px</div>
```

## 🎨 Borders & Shadows

```html
<div class="border rounded">With border</div>
<div class="rounded-lg">Large rounded corners</div>
<div class="shadow-sm">Small shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
```

## 🎭 Typography

```html
<h1>Heading 1 (36px)</h1>
<h2>Heading 2 (30px)</h2>
<h3>Heading 3 (24px)</h3>

<p class="text-large">Large (18px)</p>
<p>Normal (16px)</p>
<p class="text-small">Small (14px)</p>
<p class="text-tiny">Tiny (12px)</p>

<p class="text-bold">Bold</p>
<p class="text-medium">Medium</p>
```

## 🔄 Loading States

```html
<!-- Spinner -->
<div class="spinner"></div>

<!-- Loading Button -->
<button class="btn btn-primary" disabled>
    <div class="spinner"></div> Loading...
</button>

<!-- Skeleton -->
<div class="skeleton" style="height: 20px; width: 100%;"></div>
```

## 📱 Responsive

Grids automatically become single column on mobile (< 768px)

```html
<!-- Desktop: 3 cols, Mobile: 1 col -->
<div class="grid grid-cols-3 gap-6">
    <div>Card 1</div>
    <div>Card 2</div>
    <div>Card 3</div>
</div>
```

## 🎨 CSS Variables

Use in custom CSS:

```css
.custom {
    color: var(--color-primary);
    background: var(--color-gray-50);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    box-shadow: var(--shadow-sm);
}
```

## 📋 Common Patterns

### Login Form
```html
<div class="card" style="max-width: 400px; margin: 80px auto;">
    <div class="card-body">
        <h2 class="mb-6">Sign In</h2>
        <form>
            <div class="form-group">
                <label class="form-label">Email</label>
                <input type="email" class="form-input" />
            </div>
            <div class="form-group">
                <label class="form-label">Password</label>
                <input type="password" class="form-input" />
            </div>
            <button class="btn btn-primary btn-full">Login</button>
        </form>
    </div>
</div>
```

### Stats Cards
```html
<div class="grid grid-cols-3 gap-6">
    <div class="card">
        <div class="card-body">
            <p class="text-secondary text-small mb-1">Total Users</p>
            <h2 class="text-primary">1,234</h2>
        </div>
    </div>
</div>
```

### Action Bar
```html
<div class="flex items-center justify-between mb-6">
    <h2>Page Title</h2>
    <div class="flex gap-3">
        <button class="btn btn-secondary">Cancel</button>
        <button class="btn btn-primary">Save</button>
    </div>
</div>
```
