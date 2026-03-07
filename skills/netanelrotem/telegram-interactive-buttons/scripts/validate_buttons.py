#!/usr/bin/env python3
"""
Validate Telegram button JSON structure before sending.
Usage: python3 validate_buttons.py 'BUTTONS_JSON'
"""

import sys
import json

def validate_buttons(buttons_json):
    """Validate button structure."""
    try:
        buttons = json.loads(buttons_json)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    
    # Must be array
    if not isinstance(buttons, list):
        print("❌ Buttons must be an array of arrays")
        return False
    
    # Check each row
    for row_idx, row in enumerate(buttons):
        if not isinstance(row, list):
            print(f"❌ Row {row_idx} must be an array")
            return False
        
        # Check each button in row
        for btn_idx, btn in enumerate(row):
            if not isinstance(btn, dict):
                print(f"❌ Button at row {row_idx}, position {btn_idx} must be an object")
                return False
            
            # Required fields
            if "text" not in btn:
                print(f"❌ Button at row {row_idx}, position {btn_idx} missing 'text'")
                return False
            
            if "callback_data" not in btn:
                print(f"❌ Button at row {row_idx}, position {btn_idx} missing 'callback_data'")
                return False
            
            # Optional style validation
            if "style" in btn and btn["style"] not in ["primary", "success", "danger"]:
                print(f"⚠️  Button at row {row_idx}, position {btn_idx} has invalid style '{btn['style']}'")
                print("   Valid styles: primary, success, danger")
    
    # UX recommendations
    total_buttons = sum(len(row) for row in buttons)
    if total_buttons > 10:
        print(f"⚠️  {total_buttons} buttons might overwhelm users (consider < 10)")
    
    for row_idx, row in enumerate(buttons):
        if len(row) > 2:
            print(f"⚠️  Row {row_idx} has {len(row)} buttons (consider 1-2 per row for mobile)")
    
    print(f"✅ Valid button structure: {len(buttons)} rows, {total_buttons} total buttons")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_buttons.py 'BUTTONS_JSON'")
        print("")
        print("Example:")
        print('  python3 validate_buttons.py \'[[{"text": "Yes", "callback_data": "yes"}]]\'')
        sys.exit(1)
    
    buttons_json = sys.argv[1]
    if not validate_buttons(buttons_json):
        sys.exit(1)
