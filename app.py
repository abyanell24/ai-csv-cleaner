import streamlit as st
import pandas as pd
import json
import io
import time

from utils.parser import parse_csv_to_list
from utils.generator import generate_csv_from_list
from utils.cerebras_client import CerebrasClient
from utils.cleaner import pre_process_csv, post_process_dataframe
from prompts.prompts import (
    PARSER_SYSTEM_PROMPT,
    PARSER_USER_PROMPT,
    CLEANER_SYSTEM_PROMPT,
    CLEANER_USER_PROMPT
)


st.set_page_config(page_title="CSV AI Parser & Cleaner", page_icon="📊")


def init_cerebras():
    if 'cerebras' not in st.session_state:
        st.session_state.cerebras = CerebrasClient(model="llama-3.1-8b")


def main():
    st.title("📊 CSV AI Parser & Cleaner")
    st.markdown("Upload CSV, parse ke JSON, atau clean data CSV dengan AI (Cerebras llama-3.1-8b - Batch Processing)")

    init_cerebras()

    tab1, tab2 = st.tabs(["CSV Parser", "CSV Cleaner"])

    with tab1:
        st.subheader("Upload CSV → JSON")
        uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"], key="parser_uploader")

        if uploaded_file:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
                st.success(f"Berhasil load {len(df)} baris data")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 📋 Preview Data")
                    st.dataframe(df.head(10), use_container_width=True)

                with col2:
                    st.markdown("### ℹ️ Info CSV")
                    st.json({
                        "columns": list(df.columns),
                        "row_count": len(df),
                        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
                    })

                analyze_with_ai = st.checkbox("Analisa dengan AI (llama-3.1-8b)", key="parser_ai_check")

                if analyze_with_ai:
                    if st.button("Jalankan AI Analysis", key="parser_ai_btn"):
                        progress_bar = st.progress(10)
                        st.status("Menghubungi Cerebras API...")
                        
                        uploaded_file.seek(0)
                        csv_data = parse_csv_to_list(uploaded_file)
                        csv_str = json.dumps(csv_data[:5])
                        
                        progress_bar.progress(30)
                        
                        prompt = PARSER_USER_PROMPT.format(data=csv_str)
                        result = st.session_state.cerebras.generate(
                            prompt=prompt,
                            system_prompt=PARSER_SYSTEM_PROMPT
                        )
                        
                        progress_bar.progress(70)
                        st.markdown("### 🤖 AI Analysis Result")
                        st.markdown(result)
                        
                        progress_bar.progress(100)

                st.markdown("### 📄 JSON Output")
                json_output = df.to_json(orient="records", indent=2)
                st.code(json_output, language="json")

                st.download_button(
                    label="Download JSON",
                    data=json_output,
                    file_name="output.json",
                    mime="application/json",
                    key="parser_download"
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")

    with tab2:
        st.subheader("Upload CSV → Clean dengan AI → Download")
        uploaded_file_clean = st.file_uploader("Pilih file CSV untuk di-clean", type=["csv"], key="cleaner_uploader")

        if uploaded_file_clean:
            try:
                uploaded_file_clean.seek(0)
                df = pd.read_csv(uploaded_file_clean)
                st.success(f"Berhasil load {len(df)} baris data")

                st.markdown("### 📋 Preview Data Asli")
                st.dataframe(df.head(10), use_container_width=True)

                if st.button("Clean dengan AI", key="clean_btn"):
                    progress_bar = st.progress(5)
                    st.status("Step 1: Pre-processing...")
                    
                    uploaded_file_clean.seek(0)
                    
                    df = pre_process_csv(uploaded_file_clean)
                    st.success(f"Pre-processing selesai! {len(df)} baris")
                    
                    progress_bar.progress(15)
                    st.status("Step 2: AI cleaning...")
                    
                    csv_data = df.to_dict(orient="records")
                    total_rows = len(csv_data)
                    total_batches = (total_rows + 49) // 50
                    
                    all_cleaned = []
                    
                    for batch_num in range(0, len(csv_data), 50):
                        batch = csv_data[batch_num:batch_num+50]
                        batch_json = json.dumps(batch)
                        
                        prompt = CLEANER_USER_PROMPT.format(data=batch_json)
                        result = st.session_state.cerebras.generate(
                            prompt=prompt,
                            system_prompt=CLEANER_SYSTEM_PROMPT
                        )
                        
                        try:
                            cleaned_batch = json.loads(result)
                            if isinstance(cleaned_batch, list):
                                all_cleaned.extend(cleaned_batch)
                            else:
                                all_cleaned.extend(batch)
                        except:
                            all_cleaned.extend(batch)
                        
                        current_batch = batch_num // 50 + 1
                        progress_percent = min(15 + int((current_batch / total_batches) * 70), 85)
                        progress_bar.progress(progress_percent)
                        st.status(f"AI processing batch {current_batch}/{total_batches}...")
                    
                    progress_bar.progress(85)
                    st.status("Step 3: Post-processing...")
                    
                    if all_cleaned:
                        df_clean = pd.DataFrame(all_cleaned)
                        df_clean = post_process_dataframe(df_clean)
                        
                        progress_bar.progress(100)
                        st.markdown("### ✅ Cleaned Data")
                        st.dataframe(df_clean.head(10), use_container_width=True)
                        
                        csv_bytes = generate_csv_from_list(df_clean.to_dict(orient="records"))
                        st.download_button(
                            label="Download CSV_cleaned.csv",
                            data=csv_bytes,
                            file_name="output_cleaned.csv",
                            mime="text/csv",
                            key="cleaned_download"
                        )
                        st.success(f"Data berhasil di-clean! {len(df_clean)} baris")
                    else:
                        progress_bar.progress(100)
                        st.warning("Gagal memproses data")

            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()