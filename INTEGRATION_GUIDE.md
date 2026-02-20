# MedAssist Global Design System - Integration Guide

## 📋 Overview

This document provides complete instructions for integrating the global design system into your Flask medical application.

---

## 🔗 Step 1: Link Theme to All Templates

Add this line to the `<head>` section of every HTML template:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
```

### Example Template Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title - MedAssist</title>
    
    <!-- Font Awesome (if needed) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Global Theme -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
    
    <!-- Page-specific styles (if needed) -->
    <style>
        /* Custom page styles here */
    </style>
</head>
<body>
    <!-- Content -->
</body>
</html>
```

---

## 🎨 Step 2: Remove Inline Styles

Replace all inline `<style>` blocks that duplicate the global theme.

**Before:**
```html
<style>
    :root {
        --primary: #2F80ED;
        --bg: #F5F7FA;
    }
    .btn { padding: 10px; }
</style>
```

**After:**
```html
<!-- Use theme.css classes instead -->
```

---

## 📦 Component Examples

### Buttons

```html
<!-- Primary Button -->
<button class="btn btn-primary">Save Changes</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Cancel</button>

<!-- Ghost Button -->
<button class="btn btn-ghost">Learn More</button>

<!-- Danger Button -->
<button class="btn btn-danger">Delete Account</button>

<!-- Success Button -->
<button class="btn btn-success">Confirm</button>

<!-- Button Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>

<!-- Full Width Button -->
<button class="btn btn-primary btn-full">Full Width</button>

<!-- Icon Button -->
<button class="btn btn-primary">
    <i class="fas fa-save"></i>
    Save
</button>

<!-- Icon Only Button -->
<button class="btn btn-secondary btn-icon">
    <i class="fas fa-edit"></i>
</button>
```

---

### Cards

```html
<!-- Basic Card -->
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Patient Information</h3>
        <p class="card-subtitle">Complete medical profile</p>
    </div>
    <div class="card-body">
        <p>Card content goes here</p>
    </div>
    <div class="card-footer">
        <button class="btn btn-primary btn-sm">Update</button>
    </div>
</div>

<!-- Hoverable Card -->
<div class="card card-hover">
    <div class="card-body">
        <h4 class="mb-2">Interactive Card</h4>
        <p class="text-secondary">Hover to see effect</p>
    </div>
</div>

<!-- Flat Card (no shadow) -->
<div class="card card-flat">
    <div class="card-body">
        <p>Minimal card design</p>
    </div>
</div>
```

---

### Forms

```html
<form>
    <!-- Text Input -->
    <div class="form-group">
        <label class="form-label form-label-required">Email Address</label>
        <input type="email" class="form-input" placeholder="you@example.com">
        <span class="form-helper">We'll never share your email</span>
    </div>

    <!-- Input with Error -->
    <div class="form-group">
        <label class="form-label">Password</label>
        <input type="password" class="form-input form-input-error" value="123">
        <span class="form-error">Password must be at least 8 characters</span>
    </div>

    <!-- Select -->
    <div class="form-group">
        <label class="form-label">Country</label>
        <select class="form-select">
            <option>United States</option>
            <option>Canada</option>
            <option>Other</option>
        </select>
    </div>

    <!-- Textarea -->
    <div class="form-group">
        <label class="form-label">Medical History</label>
        <textarea class="form-textarea" placeholder="Describe your medical history"></textarea>
    </div>

    <!-- Checkbox -->
    <div class="form-check mb-4">
        <input type="checkbox" class="form-check-input" id="terms">
        <label class="form-check-label" for="terms">
            I agree to the terms and conditions
        </label>
    </div>

    <!-- Submit Button -->
    <button type="submit" class="btn btn-primary btn-full">Submit</button>
</form>
```

---

### Layout Grid

```html
<!-- 2-Column Grid -->
<div class="grid grid-cols-2 gap-6">
    <div class="card">
        <div class="card-body">Column 1</div>
    </div>
    <div class="card">
        <div class="card-body">Column 2</div>
    </div>
</div>

<!-- 3-Column Grid -->
<div class="grid grid-cols-3 gap-4">
    <div class="card">...</div>
    <div class="card">...</div>
    <div class="card">...</div>
</div>

<!-- Responsive Container -->
<div class="container">
    <h1>Page Title</h1>
    <p>Content within max-width container</p>
</div>
```

---

### Navbar

```html
<nav class="navbar">
    <div class="navbar-container">
        <a href="/" class="navbar-brand">
            <div class="navbar-logo">
                <i class="fas fa-heartbeat"></i>
            </div>
            MedAssist
        </a>
        
        <ul class="navbar-nav">
            <li><a href="/dashboard" class="navbar-link active">Dashboard</a></li>
            <li><a href="/chat" class="navbar-link">Chat</a></li>
            <li><a href="/profile" class="navbar-link">Profile</a></li>
            <li><button class="btn btn-primary btn-sm">Logout</button></li>
        </ul>
    </div>
</nav>
```

---

### Sidebar

```html
<div class="sidebar">
    <div class="sidebar-header">
        <a href="/" class="navbar-brand">
            <div class="navbar-logo">
                <i class="fas fa-heartbeat"></i>
            </div>
            MedAssist
        </a>
    </div>
    
    <div class="sidebar-body">
        <ul class="sidebar-nav">
            <li class="sidebar-nav-item">
                <a href="/dashboard" class="sidebar-nav-link active">
                    <i class="fas fa-home sidebar-nav-icon"></i>
                    Dashboard
                </a>
            </li>
            <li class="sidebar-nav-item">
                <a href="/chat" class="sidebar-nav-link">
                    <i class="fas fa-comments sidebar-nav-icon"></i>
                    Chat
                </a>
            </li>
            <li class="sidebar-nav-item">
                <a href="/health-tracker" class="sidebar-nav-link">
                    <i class="fas fa-heart-pulse sidebar-nav-icon"></i>
                    Health Tracker
                </a>
            </li>
        </ul>
    </div>
    
    <div class="sidebar-footer">
        <button class="btn btn-ghost btn-full">Logout</button>
    </div>
</div>
```

---

### Alerts

```html
<!-- Info Alert -->
<div class="alert alert-info">
    This is an informational message
</div>

<!-- Success Alert -->
<div class="alert alert-success">
    Your changes have been saved successfully
</div>

<!-- Warning Alert -->
<div class="alert alert-warning">
    Your session will expire in 5 minutes
</div>

<!-- Error Alert -->
<div class="alert alert-error">
    An error occurred. Please try again
</div>
```

---

### Badges

```html
<span class="badge badge-primary">Active</span>
<span class="badge badge-success">Completed</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-error">Critical</span>
<span class="badge badge-gray">Draft</span>
```

---

### Tables

```html
<div class="table-container">
    <table class="table">
        <thead>
            <tr>
                <th>Patient Name</th>
                <th>Appointment</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>John Doe</td>
                <td>Feb 21, 2026</td>
                <td><span class="badge badge-success">Confirmed</span></td>
                <td>
                    <button class="btn btn-sm btn-secondary">View</button>
                </td>
            </tr>
            <tr>
                <td>Jane Smith</td>
                <td>Feb 22, 2026</td>
                <td><span class="badge badge-warning">Pending</span></td>
                <td>
                    <button class="btn btn-sm btn-secondary">View</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

---

### Loading States

```html
<!-- Spinner -->
<div class="spinner"></div>

<!-- Loading Button -->
<button class="btn btn-primary" disabled>
    <div class="spinner"></div>
    Loading...
</button>

<!-- Skeleton Loader -->
<div class="skeleton" style="height: 20px; width: 100%; margin-bottom: 8px;"></div>
<div class="skeleton" style="height: 20px; width: 80%;"></div>
```

---

## 🎯 Typography Examples

```html
<h1>Main Heading (36px)</h1>
<h2>Section Heading (30px)</h2>
<h3>Subsection (24px)</h3>
<h4>Card Title (20px)</h4>
<h5>Small Heading (18px)</h5>
<h6>Tiny Heading (16px)</h6>

<p class="text-large">Large paragraph text (18px)</p>
<p>Normal paragraph text (16px)</p>
<p class="text-small">Small text (14px)</p>
<p class="text-tiny">Tiny text (12px)</p>

<p class="text-primary">Primary text color</p>
<p class="text-secondary">Secondary gray text</p>
<p class="text-tertiary">Light gray text</p>
<p class="text-blue">Blue accent text</p>
<p class="text-success">Success green text</p>
<p class="text-error">Error red text</p>

<p class="text-bold">Bold weight text</p>
<p class="text-medium">Medium weight text</p>
<p class="text-normal">Normal weight text</p>
```

---

## 🔧 Utility Classes

```html
<!-- Spacing -->
<div class="mt-4">Margin top 16px</div>
<div class="mb-6">Margin bottom 24px</div>
<div class="p-6">Padding 24px all sides</div>

<!-- Flexbox -->
<div class="flex items-center justify-between">
    <span>Left</span>
    <span>Right</span>
</div>

<div class="flex flex-col gap-4">
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<!-- Borders & Shadows -->
<div class="border rounded p-4">Bordered box</div>
<div class="shadow-md rounded-lg p-6">Shadowed card</div>

<!-- Width -->
<input class="w-full" />  <!-- 100% width -->

<!-- Text Alignment -->
<p class="text-center">Centered text</p>
<p class="text-right">Right-aligned text</p>

<!-- Display -->
<span class="block">Block element</span>
<div class="hidden">Hidden element</div>
```

---

## 🎨 Color Palette Reference

Use CSS variables in custom styles:

```css
/* In your custom CSS */
.custom-element {
    color: var(--color-primary);
    background-color: var(--color-gray-50);
    border: 1px solid var(--color-border);
}
```

**Available Colors:**
- `--color-primary` - Main blue (#2563EB)
- `--color-primary-hover` - Darker blue (#1D4ED8)
- `--color-gray-50` to `--color-gray-900` - Gray scale
- `--color-success` - Green (#059669)
- `--color-warning` - Orange (#D97706)
- `--color-error` - Red (#DC2626)
- `--color-white` - White (#FFFFFF)
- `--color-text-primary` - Dark text (#111827)
- `--color-text-secondary` - Medium gray text (#6B7280)
- `--color-text-tertiary` - Light gray text (#9CA3AF)

---

## 📱 Complete Page Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - MedAssist</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
</head>
<body style="display: flex;">
    
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-header">
            <a href="/" class="navbar-brand">
                <div class="navbar-logo">
                    <i class="fas fa-heartbeat"></i>
                </div>
                MedAssist
            </a>
        </div>
        <div class="sidebar-body">
            <ul class="sidebar-nav">
                <li class="sidebar-nav-item">
                    <a href="/dashboard" class="sidebar-nav-link active">
                        <i class="fas fa-home sidebar-nav-icon"></i>
                        Dashboard
                    </a>
                </li>
                <li class="sidebar-nav-item">
                    <a href="/chat" class="sidebar-nav-link">
                        <i class="fas fa-comments sidebar-nav-icon"></i>
                        Chat
                    </a>
                </li>
            </ul>
        </div>
    </div>
    
    <!-- Main Content -->
    <div style="flex: 1; overflow-y: auto;">
        <div class="container" style="padding-top: 40px; padding-bottom: 40px;">
            
            <!-- Page Header -->
            <div class="mb-8">
                <h1 class="mb-2">Dashboard</h1>
                <p class="text-secondary">Welcome back, John Doe</p>
            </div>
            
            <!-- Stats Grid -->
            <div class="grid grid-cols-3 gap-6 mb-8">
                <div class="card">
                    <div class="card-body">
                        <p class="text-secondary text-small mb-1">Total Appointments</p>
                        <h2 class="text-primary">24</h2>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <p class="text-secondary text-small mb-1">Pending Reviews</p>
                        <h2 class="text-warning">5</h2>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <p class="text-secondary text-small mb-1">Completed</p>
                        <h2 class="text-success">19</h2>
                    </div>
                </div>
            </div>
            
            <!-- Recent Activity -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Recent Activity</h3>
                </div>
                <div class="card-body p-0">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Patient</th>
                                    <th>Date</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>John Smith</td>
                                    <td>Feb 21, 2026</td>
                                    <td><span class="badge badge-success">Completed</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
    
</body>
</html>
```

---

## ⚙️ Migration Checklist

1. ✅ Create `static/css/theme.css` file
2. ✅ Add `<link>` tag to all templates
3. ✅ Replace inline color variables with theme variables
4. ✅ Replace custom button styles with `.btn` classes
5. ✅ Replace custom card styles with `.card` classes
6. ✅ Replace custom form styles with `.form-*` classes
7. ✅ Update navbar/sidebar to use theme classes
8. ✅ Remove duplicate CSS from individual pages
9. ✅ Test all pages for consistency
10. ✅ Verify responsive behavior on mobile

---

## 🚀 Best Practices

1. **Always use theme classes** instead of inline styles
2. **Use CSS variables** for custom colors: `var(--color-primary)`
3. **Combine utility classes** for quick layouts
4. **Keep page-specific CSS minimal** - only add what's unique
5. **Use semantic HTML** with appropriate ARIA labels
6. **Test accessibility** with keyboard navigation
7. **Verify mobile responsiveness** on all pages

---

## 🐛 Troubleshooting

**Problem**: Styles not applying
- **Solution**: Check that theme.css is linked before page-specific styles

**Problem**: Colors look different
- **Solution**: Remove conflicting CSS variables from inline `<style>` blocks

**Problem**: Buttons don't match design
- **Solution**: Ensure using `.btn .btn-primary` classes, not custom CSS

**Problem**: Layout breaks on mobile
- **Solution**: Use `.grid-cols-*` classes which are responsive by default

---

## 📧 Support

For design system questions or issues:
1. Check this integration guide
2. Review the component examples
3. Verify theme.css is properly linked
4. Check browser console for CSS errors
