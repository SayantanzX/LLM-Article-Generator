import streamlit as st
import os
import csv
import pandas as pd
import plotly.express as px
from datetime import datetime
from llm_handler import get_llm_response, get_model_info, clear_model_cache
from analytics import track_interaction, get_analytics

# Page configuration
st.set_page_config(
    page_title="Article Generator with LLMs",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .model-info {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        color: #ff4444;
        background-color: #ffe6e6;
        padding: 10px;
        border-radius: 5px;
    }
    .success-message {
        color: #00aa00;
        background-color: #e6ffe6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def save_interaction(user_query, llm_name, response):
    """Save interaction data to both CSV and JSON formats."""
    try:
        # Save to CSV
        file_path = "interactions.csv"
        file_exists = os.path.isfile(file_path)
        
        interaction_data = {
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "llm_name": llm_name,
            "response": response,
        }
        
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "user_query", "llm_name", "response"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(interaction_data)
        
        # Also save to analytics JSON
        track_interaction(llm_name, user_query, response)
        
    except Exception as e:
        st.error(f"Error saving interaction: {str(e)}")

def article_generator():
    """Main article generation interface."""
    st.markdown("<h1 class='main-header'>🤖 Article Generator with Multiple LLMs</h1>", unsafe_allow_html=True)
    
    # Model information sidebar
    with st.sidebar:
        st.header("Model Information")
        model_info = get_model_info()
        for name, info in model_info.items():
            status = "✅ Loaded" if info["loaded"] else "⏳ Not loaded"
            st.markdown(f"""
            <div class='model-info'>
                <strong>{name}</strong><br>
                Parameters: {info['parameters']}<br>
                Status: {status}
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Clear Model Cache", help="Free up memory by clearing loaded models"):
            clear_model_cache()
            st.success("Model cache cleared!")
            st.experimental_rerun()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_query = st.text_area(
            "Enter your article topic or query:",
            height=150,
            placeholder="e.g., The importance of renewable energy in combating climate change"
        )
    
    with col2:
        selected_llm = st.selectbox(
            "Select an LLM:",
            list(get_model_info().keys()),
            help="Choose which language model to use for generation"
        )
        
        max_length = st.slider(
            "Max response length:",
            min_value=50,
            max_value=500,
            value=200,
            step=50,
            help="Maximum number of tokens to generate"
        )
        
        generate_button = st.button(
            "🚀 Generate Article",
            type="primary",
            use_container_width=True
        )
    
    # Generation logic
    if generate_button:
        if user_query.strip():
            with st.spinner(f"Generating article using {selected_llm}..."):
                try:
                    response = get_llm_response(selected_llm, user_query, max_length)
                    
                    st.success("Article generated successfully!")
                    
                    # Display the response
                    st.markdown("### Generated Article")
                    st.markdown("---")
                    st.write(response)
                    
                    # Save the interaction
                    save_interaction(user_query, selected_llm, response)
                    
                    # Add download button
                    st.download_button(
                        label="📥 Download Article",
                        data=f"# Generated Article\n\n**Query:** {user_query}\n**Model:** {selected_llm}\n**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n{response}",
                        file_name=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating article: {str(e)}")
        else:
            st.warning("⚠️ Please enter a topic or query.")

def display_analytics():
    """Display comprehensive analytics dashboard."""
    st.markdown("<h1 class='main-header'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    # Load data from both sources
    csv_data = load_csv_data()
    json_data = get_analytics()
    
    if not csv_data and not json_data:
        st.warning("No interaction data found. Generate some articles first!")
        return
    
    # Use CSV data if available, otherwise use JSON data
    data = csv_data if csv_data else json_data
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Ensure timestamp column exists
    if 'timestamp' not in df.columns:
        df['timestamp'] = datetime.now().isoformat()
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Queries", len(df))
    
    with col2:
        unique_queries = df['user_query'].nunique() if 'user_query' in df.columns else df['prompt'].nunique()
        st.metric("Unique Queries", unique_queries)
    
    with col3:
        model_col = 'llm_name' if 'llm_name' in df.columns else 'model'
        most_used = df[model_col].mode().iloc[0] if len(df) > 0 else "N/A"
        st.metric("Most Used Model", most_used)
    
    with col4:
        avg_length = df['response'].str.len().mean() if 'response' in df.columns else 0
        st.metric("Avg Response Length", f"{avg_length:.0f} chars")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Usage Distribution")
        model_counts = df[model_col].value_counts()
        fig_pie = px.pie(
            values=model_counts.values,
            names=model_counts.index,
            title="Distribution of Model Usage"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Queries Over Time")
        daily_counts = df.groupby('date').size().reset_index(name='count')
        fig_line = px.line(
            daily_counts,
            x='date',
            y='count',
            title="Number of Queries per Day"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Response length analysis
    st.subheader("Response Length Analysis")
    df['response_length'] = df['response'].str.len()
    fig_hist = px.histogram(
        df,
        x='response_length',
        nbins=20,
        title="Distribution of Response Lengths"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Raw data table
    st.subheader("Recent Interactions")
    display_df = df.sort_values('timestamp', ascending=False).head(10)
    
    # Format the display
    if 'user_query' in display_df.columns:
        display_columns = ['timestamp', 'user_query', model_col, 'response']
    else:
        display_columns = ['timestamp', 'prompt', model_col, 'response']
    
    # Truncate long responses for display
    display_df_copy = display_df[display_columns].copy()
    display_df_copy['response'] = display_df_copy['response'].str[:100] + "..."
    
    st.dataframe(display_df_copy, use_container_width=True)
    
    # Export functionality
    st.subheader("Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = df.to_json(orient='records', date_format='iso')
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def load_csv_data():
    """Load data from interactions.csv."""
    file_path = "interactions.csv"
    if os.path.exists(file_path):
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
    return []

def settings_page():
    """Settings and configuration page."""
    st.markdown("<h1 class='main-header'>⚙️ Settings</h1>", unsafe_allow_html=True)
    
    st.subheader("Model Management")
    model_info = get_model_info()
    
    for name, info in model_info.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{name}**")
            st.write(f"Parameters: {info['parameters']}")
        
        with col2:
            status = "✅ Loaded" if info["loaded"] else "❌ Not loaded"
            st.write(f"Status: {status}")
        
        with col3:
            if info["loaded"]:
                if st.button(f"Unload {name}", key=f"unload_{name}"):
                    clear_model_cache()
                    st.success(f"{name} unloaded!")
                    st.experimental_rerun()
    
    st.markdown("---")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Analytics Data", type="secondary"):
            try:
                if os.path.exists("interactions.csv"):
                    os.remove("interactions.csv")
                if os.path.exists("analytics.json"):
                    os.remove("analytics.json")
                st.success("All analytics data cleared!")
            except Exception as e:
                st.error(f"Error clearing data: {str(e)}")
    
    with col2:
        if st.button("🧹 Clear Model Cache", type="secondary"):
            clear_model_cache()
            st.success("Model cache cleared!")
    
    st.markdown("---")
    
    st.subheader("System Information")
    import torch
    import sys
    
    st.write(f"**Python Version:** {sys.version}")
    st.write(f"**PyTorch Version:** {torch.__version__}")
    st.write(f"**CUDA Available:** {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        st.write(f"**CUDA Device:** {torch.cuda.get_device_name()}")
        st.write(f"**GPU Memory:** {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

def main():
    """Main application router."""
    # Sidebar navigation
    st.sidebar.title("🤖 LLM Article Generator")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Article Generator", "📊 Analytics", "⚙️ Settings"],
        index=0
    )
    
    # Route to appropriate page
    if page == "🏠 Article Generator":
        article_generator()
    elif page == "📊 Analytics":
        display_analytics()
    elif page == "⚙️ Settings":
        settings_page()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Version:** 2.0")
    st.sidebar.markdown("**Models:** GPT-Neo, Bloom, OPT")

if __name__ == "__main__":
    main()