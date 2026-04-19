import sys
import re

def validate_invest(content):
    gaps = []
    
    # 1. Check for Standard Story Format
    if not re.search(r"As a .* I want to .* so that .*", content, re.IGNORECASE | re.DOTALL):
        gaps.append("Format error: Story must follow 'As a... I want to... so that...'")

    # 2. Check for Gherkin Acceptance Criteria (Functional)
    functional_keywords = ["Given", "When", "Then"]
    missing_gherkin = [k for k in functional_keywords if k not in content]
    if missing_gherkin:
        gaps.append(f"Gherkin error: Functional ACs are missing keywords: {', '.join(missing_gherkin)}")

    # 3. Check for Non-Functional Requirements (Checklist)
    if "- [ ]" not in content:
        gaps.append("Checklist error: Missing non-functional requirement checkboxes.")

    # 4. Check for Traceability (BKI ID)
    if not re.search(r"BKI-\d+", content):
        gaps.append("Traceability error: Missing unique BKI-XXX identifier.")

    return gaps

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 invest_validator.py <story_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            story_content = f.read()
            
        validation_gaps = validate_invest(story_content)
        
        if validation_gaps:
            print("--- DoR GATE: FAILED ---")
            for gap in validation_gaps:
                print(f"FAILED: {gap}")
            sys.exit(1) # Block the gate
        else:
            print("--- DoR GATE: PASSED ---")
            print("INVEST Audit successful. Requirement is Ready.")
            sys.exit(0) # Allow transition to Phase 2
            
    except FileNotFoundError:
        print(f"Error: File {sys.argv[4]} not found.")
        sys.exit(1)
