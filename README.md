# JARVIS HUD - PySide6 Application

A futuristic Heads-Up Display (HUD) application built with PySide6, featuring real-time system stats, particle effects, and chat interface.

## Features

- **System Monitoring**: Real-time CPU and RAM usage display
- **3D Particle Sphere**: Animated rotating particle sphere with depth perception
- **Chat Interface**: Communication panel with styled chat bubbles
- **Frameless Window**: Draggable and resizable window with custom edge detection
- **Fullscreen Mode**: Toggle between windowed and fullscreen modes

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python jarvis_hud.py
```

## Bug Fixes Applied

### 1. nativeEvent() Return Type Mismatch (CRITICAL)
- **Issue**: Returned bare integers causing crashes on Windows
- **Fix**: Returns proper tuple format `(True, HT_VALUE)` for Qt compatibility

### 2. ParticleSphere Depth-Based Division Vulnerability (CRITICAL)
- **Issue**: Division by zero when `rz_final * 0.6` approached 1.8
- **Fix**: Clamps `rz` to safe bounds [-0.95, 0.95] before depth calculation

### 3. ChatBubble Border-Radius CSS Invalid Syntax (HIGH)
- **Issue**: Used f-string inside CSS property name (invalid syntax)
- **Fix**: Builds CSS string with conditional `border_style` variable

### 4. QListWidget Transparent Background Rendering Issues (HIGH)
- **Issue**: `background: transparent` caused rendering artifacts
- **Fix**: Uses semi-transparent panel color `rgba(20, 20, 40, 150)`

### 5. Worker Thread Blocking msleep() (MEDIUM)
- **Issue**: `self.msleep(1000)` blocked thread causing UI lag
- **Fix**: Reduced to `QThread.msleep(50)` and added non-blocking `QTimer.singleShot()` alternative

### 6. nativeEvent() Platform-Specific Logic Flaw (MEDIUM)
- **Issue**: Linux/macOS silently skipped all window edge detection
- **Fix**: Added proper exception handling and platform checks

### 7. ParticleSphere Cleanup Incomplete (MEDIUM)
- **Issue**: Didn't reset rotation angles on cleanup
- **Fix**: Resets `angle_x` and `angle_y` to 0.0 in `cleanup()`

### 8. Fullscreen Toggle State Race Condition (MEDIUM)
- **Issue**: Set `is_fullscreen` flag before async `showFullScreen()` completed
- **Fix**: Uses `self.isFullScreen()` instead of custom bool tracking

### 9. Missing Null Check in update_stats() (MEDIUM)
- **Issue**: Assumed `cpu_bar`/`ram_bar` exist, could crash if worker emits before UI ready
- **Fix**: Added `hasattr()` checks before accessing widgets

### 10. QColor Alpha Channel Mutation Loop Bug (HIGH)
- **Issue**: `base_color.setAlpha()` mutated object across iterations causing color artifacts
- **Fix**: Creates copy `QColor(self.base_color)` for each particle before setting alpha

## Requirements

- Python 3.8+
- PySide6 6.0.0+

## License

MIT
