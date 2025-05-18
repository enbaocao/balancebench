# BalanceBench

A deterministic benchmark for evaluating the ability of LLMs to balance chemical equations.

## Data

The `data.json` file contains a list of chemical equations and their corresponding smallest positive integer coefficients.

## Prompt

The `prompt.txt` file contains the specific prompt to be used when querying the language model.

## Benchmark Results

The following table summarizes the performance of various language models on the chemical equation balancing task. The task consists of 47 equations.

| Model                 | Correctly Balanced | Accuracy (%) |
|-----------------------|--------------------|--------------|
| 3.7 sonnet thinking   | 47/47              | 100.00%      |
| Deepseek R1           | 47/47              | 100.00%      |
| Gemini 2.5 Pro        | 47/47              | 100.00%      |
| o3                    | 47/47              | 100.00%      |
| o4-mini               | 47/47              | 100.00%      |
| 3.7 sonnet            | 46/47              | 97.87%       |
| Gemini 2.0 Flash      | 44/47              | 93.62%       |
| o1                    | 44/47              | 93.62%       |
| 4.1-mini              | 42/47              | 89.36%       |
| 4.1                   | 41/47              | 87.23%       |
| 3.5 sonnet            | 39/47              | 82.98%       |
| 4o                    | 39/47              | 82.98%       |

### Performance Visualization (Image)

![Model Performance Comparison](./model_performance_comparison_sorted.png)

### Performance Visualization (Text-based)

```
Model                 | Accuracy
----------------------|--------------------------------------------------
3.7 sonnet thinking   | ################################################## (100.00%)
Deepseek R1           | ################################################## (100.00%)
Gemini 2.5 Pro        | ################################################## (100.00%)
o3                    | ################################################## (100.00%)
o4-mini               | ################################################## (100.00%)
3.7 sonnet            | ################################################ (97.87%)
Gemini 2.0 Flash      | ############################################## (93.62%)
o1                    | ############################################## (93.62%)
4.1-mini              | ############################################ (89.36%)
4.1                   | ########################################### (87.23%)
3.5 sonnet            | ######################################### (82.98%)
4o                    | ######################################### (82.98%)
```

## Key Findings

*   Reasoning traces matter - all models that achieved a perfect score are reasoning models.
