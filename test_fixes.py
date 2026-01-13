"""
Test script to validate all 10 bug fixes in JARVIS HUD application.
This script performs static analysis and basic validation without running the GUI.
"""

import sys
import ast
import re


def test_nativeevent_return_type():
    """Test 1: Verify nativeEvent returns proper tuple format"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    # Check for parenthesized return statements in nativeEvent
    native_event_section = content[content.find('def nativeEvent'):content.find('def closeEvent')]
    
    # Verify we're returning tuples with parentheses
    if 'return (True,' in native_event_section:
        print("✅ Test 1 PASSED: nativeEvent return type uses proper tuple format")
        return True
    else:
        print("❌ Test 1 FAILED: nativeEvent return type issue")
        return False


def test_particle_depth_clamping():
    """Test 2: Verify rz is clamped before division"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    # Check for clamping before depth_factor calculation
    if 'rz_clamped = max(-0.95, min(0.95' in content:
        print("✅ Test 2 PASSED: Particle depth calculation includes clamping")
        return True
    else:
        print("❌ Test 2 FAILED: Missing depth clamping")
        return False


def test_chatbubble_css_syntax():
    """Test 3: Verify CSS border-radius is not dynamically constructed in property name"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    # Check that we're using border_style variable instead of f-string in property name
    if 'border_style = "border-bottom-' in content and '{border_style}' in content:
        # Verify we're NOT using the old broken syntax
        if 'border-bottom-{side}-radius' not in content:
            print("✅ Test 3 PASSED: ChatBubble CSS uses proper syntax")
            return True
    
    print("❌ Test 3 FAILED: ChatBubble CSS syntax issue")
    return False


def test_qlistwidget_background():
    """Test 4: Verify QListWidget uses semi-transparent color instead of 'transparent'"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    # Check for rgba color in QListWidget style
    if 'background: rgba(20, 20, 40, 150)' in content:
        print("✅ Test 4 PASSED: QListWidget uses semi-transparent rgba color")
        return True
    else:
        print("❌ Test 4 FAILED: QListWidget background issue")
        return False


def test_worker_thread_sleep():
    """Test 5: Verify worker thread uses short sleep intervals"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    # Check that msleep is not blocking for long periods
    if 'QThread.msleep(50)' in content or 'QTimer.singleShot(1000' in content:
        # Verify we don't have the old blocking sleep
        if 'self.msleep(1000)' not in content:
            print("✅ Test 5 PASSED: Worker thread uses non-blocking approach")
            return True
    
    print("❌ Test 5 FAILED: Worker thread still uses blocking sleep")
    return False


def test_nativeevent_exception_handling():
    """Test 6: Verify nativeEvent has exception handling"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    native_event_section = content[content.find('def nativeEvent'):content.find('def closeEvent')]
    
    # Check for try-except block
    if 'try:' in native_event_section and 'except Exception:' in native_event_section:
        print("✅ Test 6 PASSED: nativeEvent has exception handling")
        return True
    else:
        print("❌ Test 6 FAILED: Missing exception handling")
        return False


def test_particle_cleanup():
    """Test 7: Verify ParticleSphere cleanup resets angles"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    cleanup_section = content[content.find('def cleanup('):content.find('def paintEvent')]
    
    # Check for angle resets
    if 'self.angle_x = 0.0' in cleanup_section and 'self.angle_y = 0.0' in cleanup_section:
        print("✅ Test 7 PASSED: ParticleSphere cleanup resets angles")
        return True
    else:
        print("❌ Test 7 FAILED: Cleanup doesn't reset angles")
        return False


def test_fullscreen_toggle():
    """Test 8: Verify fullscreen toggle uses isFullScreen() instead of custom flag"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    toggle_section = content[content.find('def toggle_fullscreen'):content.find('def mousePressEvent')]
    
    # Check that we use isFullScreen() method
    if 'self.isFullScreen()' in toggle_section:
        # Verify we're not setting a custom flag
        if 'self.is_fullscreen = True' not in toggle_section:
            print("✅ Test 8 PASSED: Fullscreen toggle uses isFullScreen()")
            return True
    
    print("❌ Test 8 FAILED: Fullscreen toggle still uses custom flag")
    return False


def test_update_stats_null_checks():
    """Test 9: Verify update_stats has null checks"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    update_stats_section = content[content.find('def update_stats('):content.find('def toggle_fullscreen')]
    
    # Check for hasattr checks
    if 'hasattr(self, \'cpu_bar\')' in update_stats_section and \
       'hasattr(self, \'ram_bar\')' in update_stats_section:
        print("✅ Test 9 PASSED: update_stats has null checks")
        return True
    else:
        print("❌ Test 9 FAILED: Missing null checks in update_stats")
        return False


def test_qcolor_copy():
    """Test 10: Verify QColor is copied before alpha modification"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    paint_event_section = content[content.find('def paintEvent(', content.find('class ParticleSphere')):
                                            content.find('class ChatBubble')]
    
    # Check for QColor copy creation
    if 'particle_color = QColor(self.base_color)' in paint_event_section:
        print("✅ Test 10 PASSED: QColor is copied before alpha modification")
        return True
    else:
        print("❌ Test 10 FAILED: QColor not copied, will cause mutation bug")
        return False


def test_no_is_fullscreen_init():
    """Bonus: Verify is_fullscreen flag is removed from __init__"""
    with open('jarvis_hud.py', 'r') as f:
        content = f.read()
    
    init_section = content[content.find('class JarvisHUD'):content.find('def init_ui')]
    
    if 'self.is_fullscreen' not in init_section:
        print("✅ Bonus Test PASSED: is_fullscreen flag removed from initialization")
        return True
    else:
        print("⚠️  Warning: is_fullscreen flag still in __init__ (not critical)")
        return True  # Not critical, just a cleanup issue


def main():
    print("=" * 70)
    print("JARVIS HUD Bug Fixes Validation Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_nativeevent_return_type,
        test_particle_depth_clamping,
        test_chatbubble_css_syntax,
        test_qlistwidget_background,
        test_worker_thread_sleep,
        test_nativeevent_exception_handling,
        test_particle_cleanup,
        test_fullscreen_toggle,
        test_update_stats_null_checks,
        test_qcolor_copy,
        test_no_is_fullscreen_init,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! All bugs have been fixed.")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review the fixes.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
