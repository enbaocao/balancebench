import json
import argparse

GROUND_TRUTH_FILE = "data.json"

def load_json_file(file_path):
    """Loads data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'. Make sure it is valid JSON.")
        return None

def verify_llm_response(llm_response_data, ground_truth_data):
    """Verifies the LLM's response against the ground truth."""
    if not isinstance(llm_response_data, dict):
        print("Error: LLM response is not in the expected format (should be a JSON object/dictionary).")
        return 0, 0, 0, {}

    # Convert ground truth list to a dictionary for easier lookup
    ground_truth_dict = {item["equation"]: item["coefficients"] for item in ground_truth_data}

    correct_predictions = 0
    incorrect_predictions = 0
    missing_in_llm_response = 0
    total_ground_truth_equations = len(ground_truth_dict)

    comparison_details = []

    # Check equations present in LLM response
    for equation, predicted_coeffs in llm_response_data.items():
        if equation in ground_truth_dict:
            true_coeffs = ground_truth_dict[equation]
            if predicted_coeffs == true_coeffs:
                correct_predictions += 1
                comparison_details.append({"equation": equation, "status": "CORRECT", "predicted": predicted_coeffs, "expected": true_coeffs})
            else:
                incorrect_predictions += 1
                comparison_details.append({"equation": equation, "status": "INCORRECT", "predicted": predicted_coeffs, "expected": true_coeffs})
        else:
            # This case implies the LLM responded with an equation not in our ground truth.
            # Or there's a subtle string difference (e.g. spacing, arrow type)
            print(f"Warning: Equation from LLM response not found in ground truth (or mismatch in key): '{equation}'")
            comparison_details.append({"equation": equation, "status": "UNEXPECTED_IN_LLM", "predicted": predicted_coeffs, "expected": "N/A"})
            # We don't count this towards incorrect_predictions against the ground truth set directly,
            # but it's an anomaly to note.

    # Check for equations in ground truth but missing from LLM response
    llm_responded_equations = set(llm_response_data.keys())
    for equation, true_coeffs in ground_truth_dict.items():
        if equation not in llm_responded_equations:
            missing_in_llm_response += 1
            comparison_details.append({"equation": equation, "status": "MISSING_IN_LLM", "predicted": "N/A", "expected": true_coeffs})

    # Total equations attempted by LLM that were in ground truth
    attempted_and_in_gt = correct_predictions + incorrect_predictions

    print("\n--- Verification Details ---")
    for detail in comparison_details:
        if detail["status"] == "CORRECT":
            print(f"[CORRECT] Equation: {detail['equation']}")
        elif detail["status"] == "INCORRECT":
            print(f"[INCORRECT] Equation: {detail['equation']}")
            print(f"  Predicted: {detail['predicted']}")
            print(f"  Expected:  {detail['expected']}")
        elif detail["status"] == "MISSING_IN_LLM":
            print(f"[MISSING FROM LLM] Equation: {detail['equation']}")
            print(f"  Expected: {detail['expected']}")
        elif detail["status"] == "UNEXPECTED_IN_LLM":
            print(f"[UNEXPECTED IN LLM] Equation: {detail['equation']}")
            print(f"  Predicted: {detail['predicted']}")

    return correct_predictions, incorrect_predictions, missing_in_llm_response, total_ground_truth_equations

def main():
    parser = argparse.ArgumentParser(description="Verify LLM responses for chemical equation balancing.")
    parser.add_argument("llm_response_file", help="Path to the JSON file containing the LLM's response.")
    args = parser.parse_args()

    print(f"Loading ground truth from: {GROUND_TRUTH_FILE}")
    ground_truth_data = load_json_file(GROUND_TRUTH_FILE)
    if ground_truth_data is None:
        return

    print(f"Loading LLM response from: {args.llm_response_file}")
    llm_response_data = load_json_file(args.llm_response_file)
    if llm_response_data is None:
        return

    correct, incorrect, missing, total_gt_eqs = verify_llm_response(llm_response_data, ground_truth_data)

    print("\n--- Verification Summary ---")
    print(f"Total equations in ground truth: {total_gt_eqs}")
    print(f"Equations processed and found in ground truth: {correct + incorrect}")
    print(f"Correctly balanced: {correct}")
    print(f"Incorrectly balanced: {incorrect}")
    print(f"Missing from LLM response (but in ground truth): {missing}")

    if total_gt_eqs > 0:
        # Accuracy based on all equations in the ground truth set
        accuracy_overall = (correct / total_gt_eqs) * 100
        print(f"Overall Accuracy (correct / total ground truth equations): {accuracy_overall:.2f}%")

        if (correct + incorrect) > 0:
            # Accuracy based on equations the LLM actually attempted and were in ground truth
            accuracy_attempted = (correct / (correct + incorrect)) * 100
            print(f"Attempted Accuracy (correct / (correct + incorrect from ground truth)): {accuracy_attempted:.2f}%")
    else:
        print("Accuracy: N/A (No ground truth equations loaded)")

if __name__ == "__main__":
    main()
