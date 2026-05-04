
import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks.base import BaseCallbackHandler
from fpdf import FPDF
import tempfile

# API Keys
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

# Setup
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.5)
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert AI research assistant.
Your job is to search the web for information on a given topic and write a well-structured research report.

The report should have:
- A clear Introduction
- Key Findings (from search results)
- Current Trends
- Conclusion

Always base your report strictly on the search results you find."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Custom Callback to capture sources + show live progress
class SourceCallbackHandler(BaseCallbackHandler):
    def __init__(self, status_box):
        self.sources = []
        self.status_box = status_box

    def on_tool_end(self, output, **kwargs):
        # output is a list of search results
        if isinstance(output, list):
            for item in output:
                url = item.get("url", "")
                if url and url not in self.sources:
                    self.sources.append(url)
                    domain = url.split("/")[2]  # extract domain name
                    self.status_box.markdown(f"🔍 Fetching results from **{domain}**...")

agent = create_tool_calling_agent(llm, tools, prompt)

# PDF Generator Function
def generate_pdf(topic, report_text, sources):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", style="B", size=20)
    pdf.cell(0, 15, "AI Research Report", ln=True, align="C")

    # Topic
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 10, f"Topic: {topic}", ln=True, align="C")
    pdf.ln(5)

    # Divider
    pdf.set_draw_color(100, 100, 100)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(8)

    # Report content
    pdf.set_font("Helvetica", size=11)
    clean_text = report_text.encode("latin-1", errors="replace").decode("latin-1")
    pdf.multi_cell(0, 8, clean_text)

    # Sources section
    if sources:
        pdf.ln(5)
        pdf.set_font("Helvetica", style="B", size=12)
        pdf.cell(0, 10, "Sources:", ln=True)
        pdf.set_font("Helvetica", size=9)
        for i, src in enumerate(sources, 1):
            # Truncate to 90 chars safely
            truncated = src[:90] + "..." if len(src) > 90 else src
            clean_src = truncated.encode("latin-1", errors="replace").decode("latin-1")
            pdf.cell(0, 7, f"{i}. {clean_src}", ln=True)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name

# Session state
if "report" not in st.session_state:
    st.session_state.report = None
if "topic" not in st.session_state:
    st.session_state.topic = None
if "sources" not in st.session_state:
    st.session_state.sources = []

# Streamlit UI
st.set_page_config(page_title="AI Research Agent", page_icon="🔍")
st.title("🔍 AI Research Agent")
st.markdown("Enter any topic and the agent will search the web and generate a research report for you!")

topic = st.text_input("Enter a research topic:", placeholder="e.g. Agentic AI in 2025")
length = st.selectbox("Report Length:", ["Short", "Medium", "Detailed"])

if st.button("Generate Report 🚀"):
    if topic.strip() == "":
        st.warning("Please enter a topic!")
    else:
        status_box = st.empty()
        status_box.markdown("⏳ Agent is starting...")

        callback = SourceCallbackHandler(status_box)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False,
            callbacks=[callback]
        )

        length_instruction = {
              "Short": "Write a SHORT research report in 200-300 words covering only the key points.",
              "Medium": "Write a MEDIUM length research report in 400-500 words with good detail.",
              "Detailed": "Write a DETAILED research report in 700-900 words covering everything thoroughly."
          }

        response = agent_executor.invoke(
              {"input": f"Research the topic: {topic}. {length_instruction[length]}"},
              config={"callbacks": [callback]}
          )

        status_box.markdown("✅ Report generated successfully!")

        st.session_state.report = response["output"]
        st.session_state.topic = topic
        st.session_state.sources = callback.sources

# Show report
if st.session_state.report:
    st.success("Report Ready!")
    st.markdown("---")
    st.markdown(st.session_state.report)

    # Show Sources
    if st.session_state.sources:
        st.markdown("---")
        st.markdown("### 📎 Sources")
        for i, src in enumerate(st.session_state.sources, 1):
            st.markdown(f"{i}. [{src}]({src})")

    # PDF Download
    st.markdown("---")
    pdf_path = generate_pdf(
        st.session_state.topic,
        st.session_state.report,
        st.session_state.sources
    )
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Download Report as PDF",
            data=f,
            file_name=f"{st.session_state.topic[:30]}_report.pdf",
            mime="application/pdf"
        )
