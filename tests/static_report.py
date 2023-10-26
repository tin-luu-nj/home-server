import radon
from radon.cli import tools
from radon.metrics import h_visit
from radon.raw import analyze
from radon.metrics import mi_visit
import jinja2
from itertools import groupby

def compute_metrics(files):
    """
    Compute the cyclomatic complexity and other metrics for each method or function in a file.

    Args:
        files (list): A list of file paths.

    Returns:
        cc_results (list): A list of dictionaries containing the file name, method/function name, and cyclomatic complexity.
        other_results (list): A list of dictionaries containing the file name, method/function name, and other metrics.
    """
    cc_results = []
    other_results = []
    for file in files:
        with open(file, 'r') as f:
            code = f.read()
            blocks = radon.complexity.cc_visit(code)
            raw = analyze(code)
            hal = h_visit(code)
            mi = mi_visit(code, True)  # Consider multi-line strings
            for block in blocks:
                cc_results.append({
                    "file": file,
                    "type": block.letter,
                    "name": block.name,
                    "complexity": round(block.complexity, 3),
                    "rank": radon.complexity.cc_rank(block.complexity),
                })
            other_results.append({
                "file": file,
                "loc": raw.loc,
                "lloc": raw.lloc,
                "sloc": raw.sloc,
                "comments": raw.comments,
                "multi": raw.multi,
                "blank": raw.blank,
                "h1": round(hal.total.h1, 3),
                "h2": round(hal.total.h2, 3),
                "N1": round(hal.total.N1, 3),
                "N2": round(hal.total.N2, 3),
                "vocabulary": round(hal.total.vocabulary, 3),
                "length": round(hal.total.length, 3),
                "calculated_length": round(hal.total.calculated_length, 3),
                "volume": round(hal.total.volume, 3),
                "difficulty": round(hal.total.difficulty, 3),
                "effort": round(hal.total.effort, 3),
                "mi": round(mi, 3),
                "mi_rank": 'A' if mi >= 20 else 'B' if mi >= 10 else 'C'
            })
    return cc_results, other_results

def generate_report(cc_results, other_results):
    """
    Generate an HTML report of the cyclomatic complexity and other metrics.

    Args:
        cc_results (list): A list of dictionaries containing the file name, method/function name, and cyclomatic complexity.
        other_results (list): A list of dictionaries containing the file name, method/function name, and other metrics.

    Returns:
        html (str): An HTML string of the report.
    """

    with open("report/static/template/index.jinja") as file_:
        report = jinja2.Template(file_.read())
    
    # Group the results by file name
    cc_files = [(file, list(blocks)) for file, blocks in groupby(cc_results, key=lambda x: x['file'])]
    
    html = report.render(cc_files=cc_files, other_files=other_results)
    return html

def export_to_md(cc_results, other_results):
    """
    Export the results to a Markdown file.

    Args:
        results (list): A list of dictionaries containing the file name, method/function name, and metrics.

    Returns:
        None
    """
    # Open a new file with write mode
    with open("report/static/radon_report.md", "w") as f:
        # Write the title and a horizontal rule
        f.write("# Radon Report\n")
        f.write("---\n")

        # Write the cyclomatic complexity table
        f.write("## Cyclomatic Complexity\n")
        f.write("| File | Type | Name | Complexity | Rank |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        for result in cc_results:
            f.write(f"| {result['file']} | {result['type']} | {result['name']} | {result['complexity']} | {result['rank']} |\n")
        f.write("\n")

        # Write the other metrics table
        f.write("## Other Metrics\n")
        f.write("| File | LOC | LLOC | SLOC | Comments | Multi | Blank | H1 | H2 | N1 | N2 | Vocabulary | Length | Calculated Length | Volume | Difficulty | Effort | MI |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for result in other_results:
            f.write(f"| {result['file']} ")
            for metric in ['loc', 'lloc', 'sloc', 'comments', 'multi', 'blank', 'h1', 'h2', 'N1', 'N2', 'vocabulary', 'length', 'calculated_length', 'volume', 'difficulty', 'effort', 'mi']:
                f.write(f"| {result[metric]} ")
            f.write("|\n")
        f.write("\n")

def main():
    """
    The main function to generate a cyclomatic complexity report.
    """
    files = tools.iter_filenames(["./src/"])
    cc_results, other_results = compute_metrics(files)
    
    html = generate_report(cc_results, other_results)
    
    with open("report/static/index.html", "w") as f:
        f.write(html)

    export_to_md(cc_results, other_results)

if __name__ == "__main__":
    main()
