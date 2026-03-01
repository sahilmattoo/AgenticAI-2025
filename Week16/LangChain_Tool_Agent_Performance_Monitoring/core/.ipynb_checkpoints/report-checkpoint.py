"""
Module: Report
Generates and saves Evidently Data Drift report as HTML.
"""

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from pathlib import Path


def generate_drift_report(ref_df, cur_df, save_path="reports/drift_report.html"):
    """Generate Evidently drift report and save it as HTML."""
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_df, current_data=cur_df)

    # Save report as HTML
    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    html = report.get_html()
    path.write_text(html, encoding="utf-8")

    print(f"✅ Drift report saved to: {path.resolve()}")
    return report
