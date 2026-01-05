# PythonScript_TaxAssist

# TaxAssist ('taxassist.py')

A simple interactive **Python CLI** tool that collects your income sources, deductions/credits, and then estimates your **Canadian federal tax + Saskatchewan provincial tax** (default: **tax year 2025**), including basic CPP and EI estimates.

> ⚠️ This is an educational estimator and **not professional tax advice**. Always confirm results with CRA guidance or a qualified tax professional.

---

## Features

- Prompt-based entry for **multiple income sources**
- Supports slip tagging: `T4`, `T4A`, `T5`, `T3`, or `None`
- Optional notes for common income types (employment, scholarship, rental)
- Basic **investment income breakdown**:
  - Capital gains (50% taxable)
  - Dividends (simplified)
  - Interest income (fully taxable)
- Deduction/credit inputs:
  - RRSP contributions
  - Union/professional dues
  - Childcare expenses
  - Tuition
  - Medical expenses (above 3% threshold)
  - Charitable donations (tiered federal credit)
- Outputs a tax summary:
  - Gross income
  - Taxable income (after deductions)
  - Federal + provincial tax (after credits)
  - CPP + EI estimates
  - Total tax payable
  - Net income
  - Effective tax rate

---

## Requirements

- Python 3.8+ (recommended)

No external libraries required.

---

## How to Run

1. Clone the repo (or download the file)
2. Run the script:

```bash
python taxassist.py
```

---

## Screenshot
![DEMO](Screenshot/image.png)
