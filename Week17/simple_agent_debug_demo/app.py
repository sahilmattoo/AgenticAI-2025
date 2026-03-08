"""
Entry point: launches Gradio UI for the debugging demo.
"""

import gradio as gr
from core.agent import simple_agent
from config.settings import APP_TITLE, APP_DESC, LOG_FILE
from core.logger import log_to_file

if __name__ == "__main__":
    log_to_file("Starting Simple Agent Debug Demo")

    demo = gr.Interface(
        fn=simple_agent,
        inputs=gr.Textbox(lines=2, placeholder="Try: calc 67 8 or calc 78*7"),
        outputs="text",
        title=APP_TITLE,
        description=APP_DESC
    )

    print(f"Logs are being written to: {LOG_FILE}")
    demo.launch()
