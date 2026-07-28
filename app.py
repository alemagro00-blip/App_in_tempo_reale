import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Terminal Mercati Live",
    page_icon="📊",
    layout="wide"
)

# --- CSS PERSONALIZZATO PER DESIGN PRO DARK & RESPONSIVE MOBILE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* FORZATURA TEMA SCURO REALE GLOBALE */
    :root {
        --background-color: #131722 !important;
        --secondary-background-color: #1E222D !important;
        --text-color: #F0F3FA !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #131722 !important;
        color: #F0F3FA !important;
    }
    
    /* SIDEBAR COMPLETA SCURA & TESTI BIANCHI FORZATI */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background-color: #1E222D !important;
        border-right: 1px solid #2A2E39;
    }
    
    /* FORZATURA TOTALE TESTO SIDEBAR (Risolve il testo nero nella sidebar) */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div {
        color: #F0F3FA !important;
    }

    /* FIX MENU A TENDINA & INPUT */
    div[data-baseweb="select"], div[data-baseweb="select"] * {
        background-color: #1E222D !important;
        color: #F0F3FA !important;
        border-color: #2A2E39 !important;
    }
    ul[data-baseweb="menu"], ul[data-baseweb="menu"] * {
        background-color: #1E222D !important;
        color: #F0F3FA !important;
    }
    div[role="listbox"] div {
        color: #F0F3FA !important;
    }
    li[data-baseweb="option"] {
        background-color: #1E222D !important;
        color: #F0F3FA !important;
    }
    li[data-baseweb="option"]:hover {
        background-color: #2A2E39 !important;
    }
    [data-baseweb="popover"] {
        background-color: #1E222D !important;
    }
    .stSelectbox label, .stMultiSelect label, .stRadio label, .stSlider label, .stCheckbox label {
        color: #F0F3FA !important;
    }

    /* Header elegante */
    .title-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #1E222D 0%, #171B26 100%);
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid #2A2E39;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .title-text h1 {
        margin: 0;
        font-size: 24px;
        color: #F0F3FA !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .title-text p {
        margin: 4px 0 0 0;
        color: #787B86 !important;
        font-size: 13px;
        font-weight: 400;
    }
    
    /* Badge Live */
    .live-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(8, 153, 129, 0.12);
        border: 1px solid rgba(8, 153, 129, 0.3);
        color: #089981 !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.8px;
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        background-color: #089981;
        border-radius: 50%;
        box-shadow: 0 0 0 rgba(8, 153, 129, 0.7);
        animation: pulse 1.6s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(8, 153, 129, 0.7); }
        70% { box-shadow: 0 0 0 6px rgba(8, 153, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(8, 153, 129, 0); }
    }

    /* Card metriche */
    [data-testid="stMetric"] {
        background: #1E222D !important;
        border: 1px solid #2A2E39 !important;
        padding: 14px 18px !important;
        border-radius: 10px !important;
        margin-bottom: 10px;
    }
    [data-testid="stMetricLabel"] {
        color: #787B86 !important;
        font-size: 13px !important;
    }
    [data-testid="stMetricValue"] {
        color: #F0F3FA !important;
        font-size: 22px !important;
        font-weight: 600 !important;
    }

    /* Stile per i Badge della Legenda */
    .legend-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 14px;
    }
    .badge-tag {
        font-family: monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        min-width: 85px;
        text-align: center;
    }
    .badge-green { background: rgba(8, 153, 129, 0.2); color: #089981 !important; border: 1px solid #089981; }
    .badge-red { background: rgba(242, 54, 69, 0.2); color: #F23645 !important; border: 1px solid #F23645; }
    .badge-vol { background: rgba(120, 123, 134, 0.2); color: #B2B5BE !important; border: 1px solid #787B86; }
    .badge-sma { background: rgba(247, 166, 0, 0.2); color: #F7A600 !important; border: 1px solid #F7A600; }
    .badge-boll { background: rgba(41, 98, 255, 0.2); color: #2962FF !important; border: 1px solid #2962FF; }
    .legend-desc {
        font-size: 13px;
        color: #B2B5BE !important;
        line-height: 1.5;
    }

    /* OPTIMIZATIONS SPECIFICHE PER SMARTPHONE */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-top: 1rem !important;
        }
        .title-container {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
            padding: 16px;
        }
        .title-text h1 {
            font-size: 19px !important;
        }
        .title-text p {
            font-size: 11px !important;
        }
        .live-badge {
            align-self: flex-start;
        }
        [data-testid="stMetricValue"] {
            font-size: 17px !important;
        }
        .legend-item {
            flex-direction: column;
            gap: 6px;
        }
        .badge-tag {
            min-width: auto;
            align-self: flex-start;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER APP ---
st.markdown("""
    <div class="title-container">
        <div class="title-text">
            <h1>Terminal Mercati Live</h1>
            <p>Analisi Finanziaria Interattiva e Dati in Tempo Reale</p>
        </div>
        <div class="live-badge">
            <div class="pulse-dot"></div>
            CONNESSO
        </div>
    </div>
""", unsafe_allow_html=True)

# Lista Asset Globale
asset_dict = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "NVIDIA (NVDA)": "NVDA",
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Amazon (AMZN)": "AMZN",
    "Gold / Oro": "GC=F",
    "Crude Oil / Petrolio": "CL=F",
    "Indice S&P 500": "^GSPC"
}

# --- SIDEBAR ---
st.sidebar.header("🎛️ Pannello di Controllo")

modalita = st.sidebar.radio("Modalità di Visualizzazione:", ["Singolo Asset", "Confronto Multi-Asset"])

periodo = st.sidebar.select_slider(
    "Periodo di Analisi:",
    options=["1d", "5d", "1mo", "1y"],
    value="1d"
)

# --- FETCH API FUNZIONE ---
@st.cache_data(ttl=15)
def fetch_live_data(ticker, period):
    interval = "1m" if period == "1d" else "15m" if period == "5d" else "1d"
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

# ==========================================
# MODALITÀ 1: SINGOLO ASSET
# ==========================================
if modalita == "Singolo Asset":
    scelta = st.sidebar.selectbox("Scegli lo Strumento:", list(asset_dict.keys()))
    ticker_symbol = asset_dict[scelta]
    
    tipo_grafico = st.sidebar.radio("Stile del Grafico:", ["Linea con Area", "Candele Giapponesi"])
    
    st.sidebar.subheader("📈 Indicatori Tecnici")
    mostra_sma = st.sidebar.checkbox("Media Mobile (SMA 20)", value=True)
    mostra_bollinger = st.sidebar.checkbox("Bande di Bollinger", value=False)

    with st.spinner("Sincronizzazione dati in corso..."):
        df = fetch_live_data(ticker_symbol, periodo)

    if not df.empty:
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['STD20'] = df['Close'].rolling(window=20).std()
        df['Upper_Bollinger'] = df['SMA20'] + (df['STD20'] * 2)
        df['Lower_Bollinger'] = df['SMA20'] - (df['STD20'] * 2)

        prezzo_attuale = df["Close"].iloc[-1]
        prezzo_inizio = df["Close"].iloc[0]
        variazione = prezzo_attuale - prezzo_inizio
        variazione_pct = (variazione / prezzo_inizio) * 100
        ora_aggiornamento = datetime.now().strftime("%H:%M:%S")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Prezzo Attuale", f"${prezzo_attuale:,.2f}")
        col2.metric("Variazione Periodo", f"${variazione:,.2f}", f"{variazione_pct:+.2f}%")
        col3.metric("Massimo toccato", f"${df['High'].max():,.2f}")
        col4.metric("Ultimo Aggiornamento", ora_aggiornamento)

        st.markdown("<br>", unsafe_allow_html=True)

        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_heights=[0.75, 0.25]
        )

        if tipo_grafico == "Candele Giapponesi":
            fig.add_trace(go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name='Prezzo',
                increasing_line_color='#089981', decreasing_line_color='#F23645'
            ), row=1, col=1)
        else:
            color = '#089981' if variazione >= 0 else '#F23645'
            fill_color = 'rgba(8, 153, 129, 0.12)' if variazione >= 0 else 'rgba(242, 54, 69, 0.12)'
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Close'], mode='lines', name='Prezzo',
                line=dict(color=color, width=2), fill='tozeroy', fillcolor=fill_color
            ), row=1, col=1)

        if mostra_sma:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], mode='lines', name='SMA 20', line=dict(color='#F7A600', width=1.5)), row=1, col=1)

        if mostra_bollinger:
            fig.add_trace(go.Scatter(x=df.index, y=df['Upper_Bollinger'], mode='lines', name='Boll. Sup.', line=dict(color='rgba(41, 98, 255, 0.5)', width=1, dash='dot')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['Lower_Bollinger'], mode='lines', name='Boll. Inf.', line=dict(color='rgba(41, 98, 255, 0.5)', width=1, dash='dot'), fill='tonexty', fillcolor='rgba(41, 98, 255, 0.05)'), row=1, col=1)

        colors_vol = ['#089981' if c >= o else '#F23645' for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=colors_vol, opacity=0.5), row=2, col=1)

        fig.update_layout(
            template="plotly_dark", paper_bgcolor="#131722", plot_bgcolor="#131722",
            height=480, margin=dict(l=5, r=5, t=10, b=10),
            xaxis_rangeslider_visible=False, showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_yaxes(gridcolor='#2A2E39', row=1, col=1)
        fig.update_yaxes(gridcolor='#2A2E39', row=2, col=1)
        fig.update_xaxes(gridcolor='#2A2E39')

        st.plotly_chart(fig, use_container_width=True)

        # LEGENDA PROFESSIONALE CON BADGE CSS
        with st.expander("ℹ️ Guida e Legenda Indicatori Tecnici"):
            st.markdown("""
            <div style="padding-top: 5px;">
                <div class="legend-item">
                    <span class="badge-tag badge-green">CANDELA +</span>
                    <span class="badge-tag badge-red">CANDELA -</span>
                    <div class="legend-desc"><strong>Prezzo e Trend:</strong> Rappresenta l'oscillazione del valore. Il colore <strong>Verde</strong> indica una chiusura in rialzo, il <strong>Rosso</strong> una chiusura in ribasso nell'intervallo di tempo selezionato.</div>
                </div>
                <div class="legend-item">
                    <span class="badge-tag badge-vol">VOLUME</span>
                    <div class="legend-desc"><strong>Volume Scambi:</strong> Istogramma in basso che mostra la quantità di titoli o contratti scambiati. Barre elevate indicano un forte interesse operativo sul mercato.</div>
                </div>
                <div class="legend-item">
                    <span class="badge-tag badge-sma">SMA 20</span>
                    <div class="legend-desc"><strong>Media Mobile Semplice (20 periodi):</strong> Calcola il prezzo medio degli ultimi 20 intervalli per smussare le fluttuazioni di breve termine e identificare la direzione primaria del trend.</div>
                </div>
                <div class="legend-item">
                    <span class="badge-tag badge-boll">BOLLINGER</span>
                    <div class="legend-desc"><strong>Bande di Volatilità:</strong> Canale statistico calcolato attorno alla media mobile. L'allontanamento delle bande segnala un incremento di volatilità nel mercato.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # TABELLA DATI GREZZI
        with st.expander("📋 Tabella dei Dati Grezzi (Ultimi Record)"):
            df_display = df[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA20']].tail(15)
            st.dataframe(df_display.sort_index(ascending=False), use_container_width=True)

# ==========================================
# MODALITÀ 2: CONFRONTO MULTI-ASSET
# ==========================================
else:
    st.sidebar.subheader("⚔️ Selezione Strumenti")
    scelte_multi = st.sidebar.multiselect(
        "Scegli 2 o più elementi da confrontare:",
        list(asset_dict.keys()),
        default=["Bitcoin (BTC)", "NVIDIA (NVDA)", "Gold / Oro"]
    )

    if len(scelte_multi) < 2:
        st.warning("⚠️ Seleziona almeno 2 strumenti dal menu a sinistra per avviare il confronto.")
    else:
        fig_multi = go.Figure()
        cols = st.columns(len(scelte_multi))
        
        with st.spinner("Calcolo delle performance relative in corso..."):
            for idx, nome_asset in enumerate(scelte_multi):
                ticker = asset_dict[nome_asset]
                df_temp = fetch_live_data(ticker, periodo)
                
                if not df_temp.empty:
                    prezzo_iniziale = df_temp['Close'].iloc[0]
                    prezzo_finale = df_temp['Close'].iloc[-1]
                    perf_pct_serie = ((df_temp['Close'] - prezzo_iniziale) / prezzo_iniziale) * 100
                    tot_perf = ((prezzo_finale - prezzo_iniziale) / prezzo_iniziale) * 100

                    fig_multi.add_trace(go.Scatter(
                        x=df_temp.index,
                        y=perf_pct_serie,
                        mode='lines',
                        name=nome_asset,
                        line=dict(width=2.5)
                    ))

                    cols[idx].metric(
                        label=nome_asset,
                        value=f"${prezzo_finale:,.2f}",
                        delta=f"{tot_perf:+.2f}%"
                    )

        fig_multi.update_layout(
            title="Confronto della Performance Relativa (%)",
            template="plotly_dark",
            paper_bgcolor="#131722",
            plot_bgcolor="#131722",
            height=450,
            margin=dict(l=5, r=5, t=40, b=10),
            yaxis_title="Variazione % dall'inizio",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_multi.update_yaxes(gridcolor='#2A2E39', zerolinecolor='#787B86')
        fig_multi.update_xaxes(gridcolor='#2A2E39')

        st.plotly_chart(fig_multi, use_container_width=True)

        with st.expander("❓ Come funziona il confronto percentuale?"):
            st.markdown("""
            Dato che strumenti diversi hanno prezzi di partenza molto lontani tra loro (es. Bitcoin vale decine di migliaia di dollari, mentre un'azione può valere $100), il grafico **imposta tutti i prezzi di partenza a 0%**. 
            
            In questo modo puoi confrontare direttamente la **resa percentuale effettiva** e vedere subito chi sta performando meglio nello stesso arco di tempo!
            """)
