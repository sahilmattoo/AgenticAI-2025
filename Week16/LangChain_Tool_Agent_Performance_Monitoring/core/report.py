from pathlib import Path

def generate_drift_report(ref_df, cur_df, save_path="reports/drift_report.html"):
    """Generate Evidently drift report and save it as HTML."""
    try:
        from evidently.report import Report
        from evidently.metric_preset import DataDriftPreset
    except Exception as e:
        print(f"[WARNING] Could not import evidently: {e}")
        return None
        
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_df, current_data=cur_df)

    # Save report as HTML
    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    html = report.get_html()
    path.write_text(html, encoding="utf-8")

    print(f"✅ Drift report saved to: {path.resolve()}")
    return report

def generate_fallback_report(ref_df, cur_df, save_path):
    """Generates a basic HTML report if Evidently fails."""
    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    html = f"""
    <html>
    <head><title>Drift Report (Fallback)</title></head>
    <body>
        <h1>Drift Report (Fallback)</h1>
        <p>Evidently failed to load. Showing raw comparison.</p>
        <h2>Reference Data (Snippet)</h2>
        {ref_df.head().to_html()}
        <h2>Current Data (Snippet)</h2>
        {cur_df.head().to_html()}
        <h2>Statistics</h2>
        <h3>Latency</h3>
        <p>Ref Mean: {ref_df['latency'].mean():.4f}</p>
        <p>Cur Mean: {cur_df['latency'].mean():.4f}</p>
        <h3>Token Count</h3>
        <p>Ref Mean: {ref_df['token_count'].mean():.4f}</p>
        <p>Cur Mean: {cur_df['token_count'].mean():.4f}</p>
    </body>
    </html>
    """
    path.write_text(html, encoding="utf-8")
    print(f"⚠️ Generated fallback report at: {path.resolve()}")
    return None

def generate_drift_report(ref_df, cur_df, save_path="reports/drift_report.html"):
    """Generate Evidently drift report or fallback."""
    try:
        from evidently.report import Report
        from evidently.metric_preset import DataDriftPreset
        
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=ref_df, current_data=cur_df)

        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        html = report.get_html()
        path.write_text(html, encoding="utf-8")
        print(f"✅ Drift report saved to: {path.resolve()}")
        return report

    except Exception as e:
        print(f"[WARNING] Evidently Drift Analysis failed: {e}")
        return generate_fallback_report(ref_df, cur_df, save_path)
