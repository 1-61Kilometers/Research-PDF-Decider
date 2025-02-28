# Healthcare AI Implementation Paper Analyzer

A tool to automate the analysis of research papers for a systematic literature review on AI implementation in healthcare settings.

## Overview

This project provides a Python-based solution for researchers conducting a systematic literature review (SLR) on artificial intelligence implementations in healthcare. The tool automates the paper analysis process by:

1. Extracting text from PDF research papers
2. Analyzing papers based on predefined SLR criteria
3. Scoring papers on relevance to specific research questions
4. Generating comprehensive reports and visualizations
5. Identifying the most relevant papers for inclusion

The analyzer is specifically tailored to the "Healthcare AI Implementation Analysis" SLR protocol developed by CMSC 691 Project Group 4.

## Features

- **Recursive PDF scanning**: Automatically finds all PDFs in your papers directory and subdirectories
- **Intelligent paper analysis**: Uses OpenAI to evaluate papers against your specific inclusion/exclusion criteria
- **Research question scoring**: Rates papers based on relevance to each research question
- **Domain and technique extraction**: Identifies healthcare domains and AI techniques used in each paper
- **Implementation quality assessment**: Evaluates the quality of implementation details provided
- **Multi-format reporting**: Generates CSV reports, visualizations, and a detailed markdown review

## Requirements

- Python 3.7 or higher
- OpenAI API key
- Required Python packages:
  - pypdf
  - openai
  - pandas
  - matplotlib

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/1-61Kilometers/Research-PDF-Decider/tree/main
cd healthcare-ai-paper-analyzer
```

2. Install required packages:

```bash
pip install pypdf openai pandas matplotlib
```

3. Set up your OpenAI API key:

For Mac/Linux:
```bash
export OPENAI_API_KEY=your_api_key
```

For Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY = "your_api_key"
```

For Windows (Command Prompt):
```cmd
set OPENAI_API_KEY=your_api_key
```

## Folder Structure

Create the following folder structure:

```
project_folder/
├── healthcare_ai_analyzer.py  (The main script)
└── papers/                    (Folder for research papers)
    ├── paper1.pdf
    ├── paper2.pdf
    └── subdirectory/
        ├── paper3.pdf
        └── paper4.pdf
```

## Usage

1. Place your research papers (in PDF format) in the `papers` folder
2. Run the script:

```bash
python healthcare_ai_analyzer.py
```

3. Review the generated outputs:
   - `healthcare_ai_paper_analysis.csv`: Detailed paper analysis in CSV format
   - `healthcare_ai_papers_ranking.png`: Visualization of top papers
   - `research_question_coverage.png`: Research question coverage visualization
   - `healthcare_ai_detailed_review.md`: Comprehensive markdown report

## Output Details

### CSV Report (healthcare_ai_paper_analysis.csv)

Contains detailed information for each paper:
- Basic file information (filename, filepath)
- Inclusion status
- Scores for each research question (RQ1, RQ2, RQ3)
- Implementation quality
- Overall score
- Healthcare domain
- AI techniques used
- Paper summary

### Visualizations

1. **Paper Ranking Chart (healthcare_ai_papers_ranking.png)**:
   - Bar chart showing top papers by overall score

2. **Research Question Coverage (research_question_coverage.png)**:
   - Radar chart showing how well top papers address each research question

### Detailed Review (healthcare_ai_detailed_review.md)

A comprehensive markdown document with:
- Summaries of top papers
- Scores for each research question
- Implementation details
- Key findings
- Challenges identified
- Success factors
- Aggregate analysis of domains, techniques, and common challenges

## SLR Criteria

The analyzer is preconfigured with the following SLR details:

### Research Questions
- RQ1: What are the current implementations and applications of AI technologies across different healthcare domains?
- RQ2: How do AI-driven systems impact clinical decision-making and patient care outcomes?
- RQ3: What are the key challenges and success factors in implementing AI solutions in healthcare settings?

### Inclusion Criteria
- IC1: Studies focusing on practical AI implementation in healthcare settings
- IC2: Research presenting empirical evidence or case studies of AI applications
- IC3: Papers discussing technical implementation details or deployment strategies

### Exclusion Criteria
- EC1: Non-peer-reviewed materials (books, keynotes, technical reports, theses)
- EC2: Literature reviews or survey papers
- EC3: Duplicate studies or similar papers by same authors
- EC4: Theoretical papers without practical implementation
- EC5: Studies not focused on healthcare applications
- EC6: Grey literature, editorials, or opinion pieces

## Costs

This script uses the OpenAI API, which has usage costs:
- Approximately $0.10-0.30 per paper analyzed
- For analyzing 30-50 papers, expect $3-15 in API costs

## Customization

You can modify the `HealthcareAIPaperAnalyzer` class initialization to customize:
- Research questions
- Inclusion criteria
- Exclusion criteria
- Time period
- Data extraction fields

## License

[MIT License](LICENSE)

## Contributors

CMSC 691 - Software Engineering for AI-Enabled Systems
Project Group 4: Shon Bennett, Charles Ganey, Bella Larkin, Miles Popiela

## Acknowledgments

- This tool uses OpenAI's GPT models for intelligent paper analysis
- Thanks to the PyPDF, Pandas, and Matplotlib libraries