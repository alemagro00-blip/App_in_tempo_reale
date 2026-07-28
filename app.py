import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Crypto & Stock Live Terminal",
    page_icon="⚡",
    layout="wide"
)

# --- CSS PERSONALIZZATO PER DESIGN PRO DARK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Titolo principale stilizzato */
    .title-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #1E222D 0%, #131722 100%);
        padding: 20px 30px;
        border-radius: 16px;
        border: 1px solid #2A2E39;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .title-text h1 {
        font-family: 'Space Grotesk', sans-serif;
        margin: 0;
        font-size: 28px;
        color: #F0F3FA;
        font-weight: 700;
    }
    .title-text p {
        margin: 5px 0 0 0;
        color: #787B86;
        font-size: 14px;
    }
    
    /* Indicatore Live Pulsante */
    .live-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(8, 153, 129, 0.15);
        border: 1px solid rgba(8, 153, 129, 0.4);
        color: #089981;
        padding: 6px 14px;
        border-radius: 99px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #089981;
        border-radius: 50%;
        box-shadow: 0 0 0 rgba(8, 153, 129, 0.7);
        animation: pulse 1.6s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(8, 153, 129, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(8, 153, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(8, 153, 129, 0); }
    }

    /* Card metriche personalizzate */
    [data-testid="stMetric"] {
        background: #1E222D;
        border: 1px solid #2A2E39;
        padding: 16px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px !important;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER APP ---
st.markdown("""
    <div class="title-container">
        <div class="title-text">
            <h1>⚡ Terminal Financial Live</h1>
            <p>Connessione diretta tramite API in tempo reale · Yahoo Finance Feed</p>
        </div>
        <div class="live-badge">
            <div class="pulse-dot"></div>
            LIVE FEED
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("🎛️ Pannello di Controllo")

asset_dict = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "NVIDIA (NVDA)": "NVDA",
    "S&P 500 Index": "^GSPC"
}

scelta = st.sidebar.selectbox("Scegli l'Asset:", list(asset_dict.keys()))
ticker_symbol = asset_dict[scelta]

periodo = st.sidebar.select_slider(
    "Periodo di analisi:",
    options=["1d", "5d", "1mo", "1y"],
    value="1d"
)

tipo_grafico = st.sidebar.radio("Stile Grafico:", ["Sfumato (Line)", "Candele Giapponesi (Candlestick)"])

if st.sidebar.button("🔄 Forza Aggiornamento Dati"):
    st.rerun()

# --- FETCH API ---
@st.cache_data(ttl=15)
def fetch_live_data(ticker, period):
    interval = "1m" if period == "1d" else "15m" if period == "5d" else "1d"
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

with st.spinner("Connessione all'API in corso..."):
    df = fetch_live_data(ticker_symbol, periodo)

if not df.empty:
    # Calcoli finanziari
    prezzo_attuale = df["Close"].iloc[-1]
    prezzo_inizio = df["Close"].iloc[0]
    variazione = prezzo_attuale - prezzo_inizio
    variazione_pct = (variazione / prezzo_inizio) * 100
    volume_totale = df["Volume"].sum() if "Volume" in df else 0
    ora_aggiornamento = datetime.now().strftime("%H:%M:%S")

    # Visualizzazione metriche
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Prezzo Attuale", f"${prezzo_attuale:,.2f}")
    col2.metric("Variazione", f"${variazione:,.2f}", f"{variazione_pct:+.2f}%")
    col3.metric("Massimo Periodo", f"${df['High'].max():,.2f}")
    col4.metric("Ultimo Tick", ora_aggiornamento)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRAFICO PLOTLY CON VOLUMI ---
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03, 
        row_heights=[0.75, 0.25]
    )

    if tipo_grafico == "Candele Giapponesi (Candlestick)":
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#089981', 
            decreasing_line_color='#F23645'
        ), row=1, col=1)
    else:
        color = '#089981' if variazione >= 0 else '#F23645'
        fill_color = 'rgba(8, 153, 129, 0.15)' if variazione >= 0 else 'rgba(242, 54, 69, 0.15)'
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['Close'], 
            mode='lines',
            name='Prezzo',
            line=dict(color=color, width=2.5),
            fill='tozeroy',
            fillcolor=fill_color
        ), row=1, col=1)

    # Istogramma dei volumi
    colors_vol = ['#089981' if c >= o else '#F23645' for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(
        x=df.index, 
        y=df['Volume'],
        name='Volume',
        marker_color=colors_vol,
        opacity=0.6
    ), row=2, col=1)

    # Layout Dark TradingView Style
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#131722",
        plot_bgcolor="#131722",
        height=550,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_rangeslider_visible=False,
        showlegend=False
    )
    fig.update_yaxes(gridcolor='#2A2E39', row=1, col=1)
    fig.update_yaxes(gridcolor='#2A2E39', row=2, col=1)
    fig.update_xaxes(gridcolor='#2A2E39')

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 Tabella Dati API Grezzi"):
        st.dataframe(df.tail(10), use_container_width=True)

else:
    st.error("Errore di connessione con l'API. Riprova tra qualche secondo!")
