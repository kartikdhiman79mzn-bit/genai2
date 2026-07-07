import streamlit as st
from weather_agent_module import process_query

st.set_page_config(page_title="Weather Agent", layout="wide")

st.title("🌤️ Weather Agent Assistant")
st.markdown("Get weather information and advice with AI-powered insights")

# Add sidebar for instructions
with st.sidebar:
    st.header("📋 Instructions")
    st.info("""
    1. Enter your question about weather or related queries
    2. The AI agent will think through the problem step by step
    3. It will fetch real-time weather data when needed
    4. Get personalized advice based on the weather
    """)

# Main input area
st.subheader("Ask me about the weather")

user_query = st.text_input(
    "Enter your question:",
    placeholder="e.g., What's the weather in Mumbai? What should I wear in London?"
)

if st.button("🔍 Get Answer", use_container_width=True):
    if user_query.strip():
        st.write("---")
        st.info("🤔 Processing your query...")
        
        try:
            response_steps = process_query(user_query)
            
            # Show the thinking process
            with st.expander("📊 View Agent's Thinking Process", expanded=False):
                for i, step in enumerate(response_steps):
                    step_name = step.get('step', 'UNKNOWN')
                    
                    if step_name == 'START':
                        st.write(f"**Step {i+1}: START**")
                        st.write(f"Query: {step.get('content')}")
                    
                    elif step_name == 'PLAN':
                        st.write(f"**Step {i+1}: PLAN**")
                        st.write(f"Thinking: {step.get('content')}")
                    
                    elif step_name == 'ACTION':
                        st.write(f"**Step {i+1}: ACTION**")
                        st.write(f"Tool: `{step.get('tool')}`")
                        st.write(f"Input: {step.get('input')}")
                    
                    elif step_name == 'OBSERVE':
                        st.write(f"**Step {i+1}: OBSERVE**")
                        st.write(f"Result: {step.get('output')}")
                    
                    elif step_name == 'OUTPUT':
                        st.write(f"**Step {i+1}: OUTPUT**")
                        st.write(f"Final Answer: {step.get('content')}")
            
            # Show final answer prominently
            st.write("---")
            final_answer = response_steps[-1].get('content', 'No answer generated')
            st.success(f"**Answer:** {final_answer}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a question")

# Add footer
st.write("---")
st.caption("Powered by Gemini AI + Weather API")