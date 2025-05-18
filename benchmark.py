import json
import os

# --- Configuration ---
DATA_FILE = "data.json"
PROMPT_FILE = "prompt.txt"
LLM_API_KEY = os.environ.get("OPENAI_API_KEY") # Example: Load API key from environment variable

# --- Helper Functions ---

def load_data(file_path):
    """Loads chemical equations and coefficients from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'.")
        return []

def load_prompt(file_path):
    """Loads the base prompt from a text file."""
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Prompt file '{file_path}' not found.")
        return ""

def get_llm_prediction(equation_str, base_prompt):
    """
    Placeholder function to simulate an LLM call.
    Replace this with your actual LLM API call.
    """
    full_prompt = f"{base_prompt}\n\nInput: {equation_str}\nOutput:"
    print(f"\n--- Sending to LLM (Simulated) ---")
    print(full_prompt)
    print("------------------------------------")

    # **TODO**: Replace this with your actual LLM API call.
    # Example using OpenAI (you'll need the 'openai' library: pip install openai):
    #
    # import openai
    # openai.api_key = LLM_API_KEY
    #
    # if not openai.api_key:
    #     print("Error: OPENAI_API_KEY not set. Please set it as an environment variable.")
    #     print("Skipping actual LLM call for: ", equation_str)
    #     # Return a dummy response that will likely fail, to indicate a problem
    #     return "[-1]" # Or raise an exception
    #
    # try:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo", # Or your preferred model
    #         messages=[
    #             {"role": "user", "content": full_prompt}
    #         ],
    #         max_tokens=50,
    #         temperature=0.0 # For deterministic output
    #     )
    #     llm_output_str = response.choices[0].message.content.strip()
    # except Exception as e:
    #     print(f"Error calling OpenAI API: {e}")
    #     return "[-1]" # Return a dummy error response

    # For now, let's return a dummy response.
    # This response simulates a correct output for the first equation if it were "Fe + O2 -> Fe2O3"
    # and an incorrect one for others to show the comparison logic.
    if "H3PO4 + KOH" in equation_str: # Simulate a specific known response for testing
         llm_output_str = "[1,3,1,3]"
    elif "Fe + O2 -> Fe2O3" in equation_str: # Example from prompt
        llm_output_str = "[4,3,2]"
    else:
        llm_output_str = "[0,0,0]" # Dummy incorrect response

    print(f"LLM Raw Output (Simulated): {llm_output_str}")

    try:
        # The prompt asks for "Output: [x,y,z]", so we expect the LLM to return just the list.
        # If the LLM includes "Output: ", we might need to strip it.
        # For simplicity, we assume the LLM returns *only* the JSON array string.
        predicted_coeffs = json.loads(llm_output_str)
        if not isinstance(predicted_coeffs, list) or not all(isinstance(c, int) for c in predicted_coeffs):
            print(f"Warning: LLM output for '{equation_str}' was not a list of integers: {llm_output_str}")
            return None
        return predicted_coeffs
    except json.JSONDecodeError:
        print(f"Warning: Could not decode LLM output for '{equation_str}' as JSON: {llm_output_str}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while parsing LLM output for '{equation_str}': {e}")
        return None

def main():
    """Main function to run the benchmark."""
    base_prompt = load_prompt(PROMPT_FILE)
    equations_data = load_data(DATA_FILE)

    if not base_prompt or not equations_data:
        print("Exiting due to missing prompt or data.")
        return

    correct_predictions = 0
    total_equations = len(equations_data)

    print("Starting Chemical Equation Balancing Benchmark...")
    print("==============================================")

    for item in equations_data:
        equation = item.get("equation")
        true_coefficients = item.get("coefficients")

        if not equation or true_coefficients is None:
            print(f"Warning: Skipping invalid data item: {item}")
            continue

        print(f"\nProcessing Equation: {equation}")
        print(f"Expected Coefficients: {true_coefficients}")

        predicted_coefficients = get_llm_prediction(equation, base_prompt)

        if predicted_coefficients is not None:
            print(f"Predicted Coefficients: {predicted_coefficients}")
            if predicted_coefficients == true_coefficients:
                print("Result: CORRECT")
                correct_predictions += 1
            else:
                print("Result: INCORRECT")
        else:
            print("Result: FAILED (Could not get or parse LLM prediction)")

        print("----------------------------------------------")

    print("\n==============================================")
    print("Benchmark Summary:")
    print(f"Total Equations Processed: {total_equations}")
    print(f"Correct Predictions: {correct_predictions}")
    if total_equations > 0:
        accuracy = (correct_predictions / total_equations) * 100
        print(f"Accuracy: {accuracy:.2f}%")
    else:
        print("Accuracy: N/A (No equations processed)")
    print("==============================================")

if __name__ == "__main__":
    main()
