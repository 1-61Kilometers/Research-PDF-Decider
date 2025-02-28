"""
Healthcare AI Implementation Paper Analyzer

This script analyzes research papers on AI implementation in healthcare using OpenAI,
specifically tailored to the SLR protocol for Project Group 4's "Healthcare AI Implementation Analysis"
"""

import os
import re
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
from pypdf import PdfReader
from openai import OpenAI

# Initialize OpenAI client
# Note: You'll need to set your API key as an environment variable 
# export OPENAI_API_KEY=your_api_key
client = OpenAI()

class HealthcareAIPaperAnalyzer:
    def __init__(self):
        self.papers = []
        # Pre-defined SLR information based on the protocol document
        self.slr_info = {
            "title": "Healthcare AI Implementation Analysis: A Systematic Literature Review",
            "research_questions": [
                "RQ1: What are the current implementations and applications of AI technologies across different healthcare domains?",
                "RQ2: How do AI-driven systems impact clinical decision-making and patient care outcomes?",
                "RQ3: What are the key challenges and success factors in implementing AI solutions in healthcare settings?"
            ],
            "inclusion_criteria": [
                "IC1: Studies focusing on practical AI implementation in healthcare settings",
                "IC2: Research presenting empirical evidence or case studies of AI applications",
                "IC3: Papers discussing technical implementation details or deployment strategies"
            ],
            "exclusion_criteria": [
                "EC1: Non-peer-reviewed materials (books, keynotes, technical reports, theses)",
                "EC2: Literature reviews or survey papers",
                "EC3: Duplicate studies or similar papers by same authors",
                "EC4: Theoretical papers without practical implementation",
                "EC5: Studies not focused on healthcare applications",
                "EC6: Grey literature, editorials, or opinion pieces"
            ],
            "time_period": "2019-2025",
            "data_extraction_fields": [
                "AI techniques used", "Healthcare domain", "Implementation scope", 
                "Technical infrastructure", "Performance metrics", "Clinical impact",
                "Implementation challenges", "Success factors"
            ]
        }
        
    def extract_text_from_pdf(self, pdf_path, max_pages=None):
        """Extract text content from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            # Limit pages if specified
            pages_to_read = min(len(reader.pages), max_pages) if max_pages else len(reader.pages)
            
            for i in range(pages_to_read):
                text += reader.pages[i].extract_text() + "\n"
                
            return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def load_papers(self, paper_dir):
        """Load all research papers recursively from a directory structure."""
        self.papers = []
        
        print(f"Scanning for papers in {paper_dir} and all subdirectories...")
        
        def process_directory(directory):
            """Recursively process all PDFs in a directory and its subdirectories."""
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    
                    # If directory, recursively process it
                    if os.path.isdir(item_path):
                        process_directory(item_path)
                    
                    # If PDF file, process it
                    elif item.lower().endswith('.pdf'):
                        print(f"Processing: {item_path}")
                        
                        # Extract first few pages (abstract, intro, conclusion are usually enough)
                        paper_text = self.extract_text_from_pdf(item_path, max_pages=10)
                        
                        if paper_text:
                            self.papers.append({
                                'filename': item,
                                'filepath': item_path,
                                'content': paper_text,
                                'scores': {}
                            })
            except Exception as e:
                print(f"Error accessing directory {directory}: {e}")
        
        # Start the recursive processing
        process_directory(paper_dir)
        print(f"Loaded {len(self.papers)} research papers from {paper_dir} and subdirectories")
        
        return len(self.papers) > 0
    
    def analyze_papers(self):
        """Analyze papers using OpenAI for healthcare AI implementation."""
        if not self.papers:
            print("Error: No papers loaded. Cannot analyze.")
            return False
        
        print(f"\nAnalyzing {len(self.papers)} papers for healthcare AI implementation...")
        
        for i, paper in enumerate(self.papers):
            print(f"Analyzing paper {i+1}/{len(self.papers)}: {paper['filename']}")
            
            try:
                # Format the SLR information for OpenAI
                slr_prompt = (
                    f"SYSTEMATIC LITERATURE REVIEW INFORMATION:\n"
                    f"Title: {self.slr_info['title']}\n\n"
                    f"Research Questions:\n" + "\n".join(self.slr_info['research_questions']) + "\n\n"
                    f"Inclusion Criteria:\n" + "\n".join(self.slr_info['inclusion_criteria']) + "\n\n"
                    f"Exclusion Criteria:\n" + "\n".join(self.slr_info['exclusion_criteria']) + "\n\n"
                    f"Time Period: {self.slr_info['time_period']}\n\n"
                    f"Data Extraction Fields: {', '.join(self.slr_info['data_extraction_fields'])}"
                )
                
                # Send to OpenAI for analysis
                response = client.chat.completions.create(
                    model="gpt-4-0125-preview",  # Use appropriate model
                    messages=[
                        {
                            "role": "system",
                            "content": f"""You are an expert in healthcare AI implementation research. Your task is to evaluate 
                            research papers for inclusion in a systematic literature review on AI implementation in healthcare.
                            
{slr_prompt}

Analyze the paper content to determine:
1. If it meets the inclusion criteria and avoids exclusion criteria
2. How well it addresses each research question (RQ1, RQ2, RQ3)
3. The quality and relevance of the implementation details
4. The overall value for this specific healthcare AI implementation literature review

Output your analysis as a JSON object with the following structure:
{{
  "meets_inclusion_criteria": true/false,
  "inclusion_justification": "Brief explanation of why it meets or fails inclusion criteria",
  "relevance_to_rq1": 0-100 score,
  "relevance_to_rq2": 0-100 score,
  "relevance_to_rq3": 0-100 score,
  "implementation_quality": 0-100 score,
  "paper_summary": "2-3 sentence summary of the paper",
  "ai_techniques": ["technique1", "technique2"],
  "healthcare_domain": "The specific healthcare domain addressed",
  "implementation_details": "Brief description of implementation approach",
  "key_findings": "Brief summary of key findings",
  "challenges_identified": ["challenge1", "challenge2"],
  "success_factors": ["factor1", "factor2"],
  "overall_score": 0-100 score,
  "recommendation": "Include" or "Exclude"
}}"""
                        },
                        {
                            "role": "user",
                            "content": f"Here is a research paper to analyze (extracted content from the beginning of the paper):\n\n{paper['content'][:7000]}"
                        }
                    ],
                    temperature=0.1,
                    max_tokens=1500,
                    response_format={"type": "json_object"}
                )
                
                # Parse JSON response
                analysis = json.loads(response.choices[0].message.content)
                
                # Store results
                paper['scores'] = analysis
                
                # Small delay to respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error analyzing paper {paper['filename']}: {e}")
                paper['scores'] = {
                    "error": str(e),
                    "meets_inclusion_criteria": False,
                    "overall_score": 0,
                    "recommendation": "Error"
                }
        
        return True
    
    def rank_papers(self):
        """Rank papers based on their scores."""
        # Filter papers that meet inclusion criteria
        included_papers = [p for p in self.papers if p['scores'].get('meets_inclusion_criteria', False)]
        
        # Sort by overall score
        return sorted(
            included_papers, 
            key=lambda x: x['scores'].get('overall_score', 0), 
            reverse=True
        )
    
    def generate_report(self, output_file="healthcare_ai_paper_analysis.csv"):
        """Generate a CSV report of the paper analysis."""
        report_data = []
        
        for paper in self.papers:
            scores = paper['scores']
            paper_data = {
                'Filename': paper['filename'],
                'Filepath': paper['filepath'],
                'Meets Inclusion': scores.get('meets_inclusion_criteria', False),
                'RQ1 Score': scores.get('relevance_to_rq1', 0),
                'RQ2 Score': scores.get('relevance_to_rq2', 0),
                'RQ3 Score': scores.get('relevance_to_rq3', 0),
                'Implementation Quality': scores.get('implementation_quality', 0),
                'Overall Score': scores.get('overall_score', 0),
                'Recommendation': scores.get('recommendation', 'Unknown'),
                'Healthcare Domain': scores.get('healthcare_domain', ''),
                'AI Techniques': ', '.join(scores.get('ai_techniques', [])),
                'Summary': scores.get('paper_summary', '')
            }
            
            report_data.append(paper_data)
            
        df = pd.DataFrame(report_data)
        df.sort_values(by=['Meets Inclusion', 'Overall Score'], ascending=[False, False], inplace=True)
        df.to_csv(output_file, index=False)
        print(f"Report generated: {output_file}")
        
        return df
    
    def visualize_results(self, top_n=10):
        """Create visualizations for the healthcare AI implementation papers."""
        included_papers = [p for p in self.papers if p['scores'].get('meets_inclusion_criteria', False)]
        
        if not included_papers:
            print("No papers met inclusion criteria. Cannot create visualization.")
            return
            
        ranked_papers = self.rank_papers()[:top_n]
        
        # 1. Create a bar chart of overall scores
        plt.figure(figsize=(12, 8))
        filenames = [os.path.basename(p['filepath']) for p in ranked_papers]
        scores = [p['scores'].get('overall_score', 0) for p in ranked_papers]
        
        # Truncate long filenames
        short_names = [name[:25] + '...' if len(name) > 25 else name for name in filenames]
        
        plt.barh(short_names, scores, color='skyblue')
        plt.xlabel('Overall Score')
        plt.title('Top Healthcare AI Implementation Papers')
        plt.tight_layout()
        plt.savefig('healthcare_ai_papers_ranking.png')
        print("Overall ranking visualization saved: healthcare_ai_papers_ranking.png")
        
        # 2. Create a radar chart for research question coverage for top 5 papers
        try:
            if len(ranked_papers) >= 3:
                top_papers = ranked_papers[:3]
                
                # Data for radar chart
                categories = ['RQ1 Score', 'RQ2 Score', 'RQ3 Score', 'Implementation Quality']
                
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, polar=True)
                
                # Number of variables
                N = len(categories)
                
                # Compute angle for each axis
                angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
                angles += angles[:1]  # Close the loop
                
                # Draw the chart for each paper
                for i, paper in enumerate(top_papers):
                    scores = paper['scores']
                    values = [
                        scores.get('relevance_to_rq1', 0)/100, 
                        scores.get('relevance_to_rq2', 0)/100,
                        scores.get('relevance_to_rq3', 0)/100, 
                        scores.get('implementation_quality', 0)/100
                    ]
                    values += values[:1]  # Close the loop
                    
                    ax.plot(angles, values, linewidth=2, label=os.path.basename(paper['filepath']))
                    ax.fill(angles, values, alpha=0.1)
                
                # Set category labels
                plt.xticks(angles[:-1], categories)
                
                # Add legend
                plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
                plt.title('Research Question Coverage of Top Papers')
                plt.savefig('research_question_coverage.png')
                print("Research question coverage visualization saved: research_question_coverage.png")
        except Exception as e:
            print(f"Error creating radar chart: {e}")
    
    def generate_detailed_review(self, output_file="healthcare_ai_detailed_review.md"):
        """Generate a detailed markdown report of the top papers."""
        ranked_papers = self.rank_papers()
        
        if not ranked_papers:
            print("No papers met inclusion criteria. Cannot generate detailed review.")
            return
            
        with open(output_file, 'w') as f:
            f.write("# Healthcare AI Implementation: Detailed Paper Review\n\n")
            f.write(f"*Generated on {time.strftime('%Y-%m-%d')}*\n\n")
            
            f.write("## Research Questions\n\n")
            for rq in self.slr_info['research_questions']:
                f.write(f"- {rq}\n")
            f.write("\n")
            
            f.write("## Top Papers for Inclusion\n\n")
            
            for i, paper in enumerate(ranked_papers[:10]):
                scores = paper['scores']
                
                f.write(f"### {i+1}. {os.path.basename(paper['filepath'])}\n\n")
                f.write(f"**Overall Score:** {scores.get('overall_score', 0)}/100\n\n")
                f.write(f"**Summary:** {scores.get('paper_summary', 'No summary available')}\n\n")
                
                f.write("**Research Question Relevance:**\n")
                f.write(f"- RQ1 (AI Implementations): {scores.get('relevance_to_rq1', 0)}/100\n")
                f.write(f"- RQ2 (Clinical Impact): {scores.get('relevance_to_rq2', 0)}/100\n")
                f.write(f"- RQ3 (Challenges & Success Factors): {scores.get('relevance_to_rq3', 0)}/100\n\n")
                
                f.write("**Implementation Details:**\n")
                f.write(f"- Healthcare Domain: {scores.get('healthcare_domain', 'Not specified')}\n")
                f.write(f"- AI Techniques: {', '.join(scores.get('ai_techniques', ['Not specified']))}\n")
                f.write(f"- Implementation Approach: {scores.get('implementation_details', 'Not described')}\n\n")
                
                f.write("**Key Findings:**\n")
                f.write(f"{scores.get('key_findings', 'Not described')}\n\n")
                
                if scores.get('challenges_identified'):
                    f.write("**Challenges Identified:**\n")
                    for challenge in scores.get('challenges_identified', []):
                        f.write(f"- {challenge}\n")
                    f.write("\n")
                    
                if scores.get('success_factors'):
                    f.write("**Success Factors:**\n")
                    for factor in scores.get('success_factors', []):
                        f.write(f"- {factor}\n")
                    f.write("\n")
                
                f.write("---\n\n")
            
            # Summary section
            f.write("## Summary of Findings\n\n")
            
            # Count papers by healthcare domain
            domains = {}
            for paper in ranked_papers:
                domain = paper['scores'].get('healthcare_domain', 'Unspecified')
                domains[domain] = domains.get(domain, 0) + 1
            
            f.write("### Healthcare Domains Covered\n\n")
            for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {domain}: {count} papers\n")
            f.write("\n")
            
            # Count papers by AI technique
            techniques = {}
            for paper in ranked_papers:
                for technique in paper['scores'].get('ai_techniques', []):
                    techniques[technique] = techniques.get(technique, 0) + 1
            
            f.write("### AI Techniques Used\n\n")
            for technique, count in sorted(techniques.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {technique}: {count} papers\n")
            f.write("\n")
            
            # Common challenges
            all_challenges = []
            for paper in ranked_papers:
                all_challenges.extend(paper['scores'].get('challenges_identified', []))
            
            challenge_counts = {}
            for challenge in all_challenges:
                challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1
            
            f.write("### Common Implementation Challenges\n\n")
            for challenge, count in sorted(challenge_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                f.write(f"- {challenge}: {count} papers\n")
        
        print(f"Detailed review generated: {output_file}")


def main():
    """Main function to run the healthcare AI paper analyzer."""
    analyzer = HealthcareAIPaperAnalyzer()
    
    # Fixed papers directory
    papers_dir = "papers"
    
    # Check if papers directory exists
    if not os.path.exists(papers_dir):
        print(f"Error: Papers directory not found at {papers_dir}")
        print("Please create a folder named 'papers' and place your research papers inside it.")
        return
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("Error: OpenAI API key not found.")
        print("Please set your API key as an environment variable:")
        print("export OPENAI_API_KEY=your_api_key")
        return
    
    # Load and analyze papers
    if not analyzer.load_papers(papers_dir):
        print("No PDF papers found in the 'papers' folder. Please add some PDF files.")
        return
    
    if not analyzer.analyze_papers():
        return
    
    # Generate reports
    analyzer.generate_report()
    analyzer.visualize_results()
    analyzer.generate_detailed_review()
    
    # Print top papers
    top_papers = analyzer.rank_papers()[:5]
    print("\nTop 5 Recommended Papers for Healthcare AI Implementation Review:")
    for i, paper in enumerate(top_papers):
        scores = paper['scores']
        print(f"{i+1}. {paper['filename']}")
        print(f"   File: {paper['filepath']}")
        print(f"   Healthcare Domain: {scores.get('healthcare_domain', 'Not specified')}")
        print(f"   AI Techniques: {', '.join(scores.get('ai_techniques', ['Not specified']))}")
        print(f"   Overall Score: {scores.get('overall_score', 0)}/100")
        print(f"   Summary: {scores.get('paper_summary', 'No summary available')[:150]}...")
        print()
    
    print("\nAnalysis complete! Check the generated reports and visualizations:")
    print("- healthcare_ai_paper_analysis.csv (Detailed CSV report)")
    print("- healthcare_ai_papers_ranking.png (Visualization of top papers)")
    print("- research_question_coverage.png (Research question coverage visualization)")
    print("- healthcare_ai_detailed_review.md (Detailed review document)")


if __name__ == "__main__":
    main()