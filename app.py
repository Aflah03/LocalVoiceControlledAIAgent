import gradio as gr
import os
from agent.executor import AgentExecutor

# Initialize the brain of the agent
executor = AgentExecutor()

def process_voice_input(audio_path):
    """
    Gradio wrapper for the executor.
    Uses a generator to stream results to the UI.
    """
    if audio_path is None:
        yield "No audio provided.", "[]", "No execution log."
        return

    # 1. Transcription (STT)
    # We manually call STT first to stream the text immediately
    text = executor.stt.transcribe_file(audio_path)

    # Update UI with transcription immediately
    yield text, "Identifying intents...", "Transcribing audio..."

    if not text:
        yield text, "[]", "No speech detected."
        return

    # 2. Intent Classification & Execution
    # We reuse the executor's logic but capture the progression
    result = executor.process_audio(audio_path, is_file=True)

    transcription = result["transcription"]
    intents = result["intents"]
    log = "\n".join(result["execution_log"])

    yield transcription, str(intents), log

def list_output_files():
    """Lists files in the output directory for the UI."""
    output_dir = "output"
    if not os.path.exists(output_dir):
        return "Output folder not yet created."

    files = os.listdir(output_dir)
    if not files:
        return "No files generated yet."

    return "\n".join(files)

# --- Gradio UI Layout ---
with gr.Blocks(title="Local Voice AI Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ️ Local Voice AI Agent")
    gr.Markdown("Transcribe speech $\rightarrow$ Classify Intent $\rightarrow$ Execute Tools")

    with gr.Row():
        with gr.Column():
            gr.Markdown("###  Input")
            # Audio input supporting both upload and mic
            audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Speak or Upload Audio")
            submit_btn = gr.Button("Process Voice Command", variant="primary")

            with gr.Accordion("Output File Browser", open=True):
                refresh_btn = gr.Button("Refresh File List")
                file_list = gr.Textbox(label="Files in /output", value=list_output_files(), interactive=False)

        with gr.Column():
            gr.Markdown("### ⚙️ Pipeline View")

            with gr.Group():
                transcription_out = gr.Textbox(label="1. Transcription", interactive=False)
                intent_out = gr.Textbox(label="2. Identified Intents (JSON)", interactive=False)
                log_out = gr.Textbox(label="3. Execution Log", lines=10, interactive=False)

    # Define interactions
    submit_btn.click(
        fn=process_voice_input,
        inputs=[audio_input],
        outputs=[transcription_out, intent_out, log_out]
    )

    refresh_btn.click(
        fn=list_output_files,
        outputs=[file_list]
    )

if __name__ == "__main__":
    # Launch the app
    demo.launch()
