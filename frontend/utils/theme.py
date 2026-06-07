import streamlit as st


def apply_theme():
    """Apply the unified dark theme to Streamlit app."""
    st.markdown(
        """
        <style>
        :root {
          --brand-bg: #081423;
          --brand-surface: rgba(255, 255, 255, 0.06);
          --brand-border: rgba(255, 255, 255, 0.10);
          --brand-text: #e6eff9;
          --brand-muted: #9ab7d1;
          --brand-primary: #01b8aa;
          --brand-secondary: #f2c80f;
          --brand-accent: #f48c06;
          --brand-highlight: #5b9bd5;
          --brand-accent-2: #7c4dff;
          --brand-accent-3: #35a2ff;
        }

        [data-testid="stAppViewContainer"] {
          background: 
                      repeating-linear-gradient(
                        0deg,
                        rgba(255, 255, 255, 0.04) 0px,
                        rgba(255, 255, 255, 0.04) 1px,
                        transparent 1px,
                        transparent 40px
                      ),
                      repeating-linear-gradient(
                        90deg,
                        rgba(255, 255, 255, 0.04) 0px,
                        rgba(255, 255, 255, 0.04) 1px,
                        transparent 1px,
                        transparent 40px
                      ),
                      radial-gradient(circle at top left, rgba(1, 184, 170, 0.24), transparent 24%),
                      radial-gradient(circle at bottom right, rgba(91, 155, 213, 0.16), transparent 28%),
                      linear-gradient(180deg, #0b2032 0%, #081423 100%);
          color: var(--brand-text);
        }

        [data-testid="stSidebar"] {
          background: #0d2941;
          color: var(--brand-text);
        }

        [data-testid="stHeader"] {
          background: transparent;
        }

        .stApp, .streamlit-expanderHeader {
          color: var(--brand-text);
        }

        .hero-title {
          font-size: clamp(2.5rem, 4vw, 4rem);
          line-height: 1.02;
          color: #f8fbff;
          margin: 0;
          letter-spacing: -0.04em;
        }

        .hero-subtitle {
          font-size: 1.05rem;
          color: var(--brand-muted);
          margin: 1rem 0 1.5rem 0;
          max-width: 700px;
        }

        .feature-card {
          padding: 1.4rem;
          border-radius: 1.05rem;
          background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
          border: 1px solid rgba(255, 255, 255, 0.08);
          height: 199px;
          color: var(--brand-text);
          box-shadow: 0 18px 45px rgba(0, 0, 0, 0.12);
          transition: transform 0.24s ease, box-shadow 0.24s ease;
          display: flex;
          flex-direction: column;
        }

        .feature-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 28px 65px rgba(0, 0, 0, 0.18);
        }

        .feature-card h4 {
          margin: 0 0 0.6rem 0;
          color: #ffffff;
          font-size: 1.15rem;
        }

        .feature-card p {
          margin: 0;
          color: var(--brand-muted);
          line-height: 1.65;
        }

        .feature-card.accent-1 {
          border-color: rgba(1, 184, 170, 0.35);
          background: linear-gradient(180deg, rgba(1, 184, 170, 0.18), rgba(255, 255, 255, 0.04));
        }

        .feature-card.accent-2 {
          border-color: rgba(91, 155, 213, 0.35);
          background: linear-gradient(180deg, rgba(91, 155, 213, 0.16), rgba(255, 255, 255, 0.04));
        }

        .feature-card.accent-3 {
          border-color: rgba(244, 140, 6, 0.35);
          background: linear-gradient(180deg, rgba(244, 140, 6, 0.16), rgba(255, 255, 255, 0.03));
        }

        .feature-card.accent-4 {
          border-color: rgba(124, 77, 255, 0.35);
          background: linear-gradient(180deg, rgba(124, 77, 255, 0.16), rgba(255, 255, 255, 0.03));
        }

        .health-card {
          padding: 1.3rem;
          border-radius: 1rem;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.09);
          color: var(--brand-text);
          margin-bottom: 1rem;
        }

        .health-card .label {
          color: var(--brand-muted);
          font-size: 0.95rem;
          margin-bottom: 0.75rem;
          display: block;
        }

        .health-card .status {
          font-size: 1rem;
          font-weight: 600;
          margin-bottom: 0.65rem;
        }

        .health-card .badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0.35rem 0.8rem;
          border-radius: 999px;
          background: var(--brand-primary);
          color: #ffffff;
          font-size: 0.82rem;
          font-weight: 600;
          letter-spacing: 0.02em;
        }

        .nav-list {
          padding-left: 1rem;
          margin: 0;
          color: var(--brand-text);
        }

        .nav-list li {
          margin-bottom: 0.65rem;
          color: var(--brand-muted);
        }

        .nav-list strong {
          color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
