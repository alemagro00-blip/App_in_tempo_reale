import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Crypto & Stock Tracker Live",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Dashboard Finanziaria Live")
st.caption("Esempio di connessione ad API in tempo reale senza file fisici")

# Sidebar per le impostazioni dell'utente
st.sidebar.header("⚙️ Impostazioni")

# Selezione dell'asset da monitorare
asset_dict = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "S&P 500": "^GSPC"
}

scelta = st.sidebar.selectbox("Scegli l'asset da monitorare:", list(asset_dict.keys()))
ticker_symbol = asset_dict[scelta]

periodo = st.sidebar.select_slider(
    "Intervallo temporale:",
    options=["1d", "5d", "1mo", "1y"],
    value="1d"
)

# Pulsante manuale per aggiornare i dati
if st.sidebar.button("🔄 Aggiorna Dati Ora"):
    st.rerun()

# --- CHIAMATA ALLA API IN TEMPO REALE ---
@st.cache_data(ttl=15)  # Mantiene i dati in cache solo per 15 secondi
def fetch_live_data(ticker, period):
    # Determina l'intervallo in base al periodo (es. ogni 1 min per 1 giorno)
    interval = "1m" if period == "1d" else "15m" if period == "5d" else "1d"
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

with st.spinner("Connessione all'API in corso..."):
    df = fetch_live_data(ticker_symbol, periodo)

if not df.empty:
    # Calcolo metriche live
    prezzo_attuale = df["Close"].iloc[-1]
    prezzo_inizio = df["Close"].iloc[0]
    variazione = prezzo_attuale - prezzo_inizio
    variazione_pct = (variazione / prezzo_inizio) * 100
    
    ora_aggiornamento = datetime.now().strftime("%H:%M:%S")

    # Visualizzazione delle metriche
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Prezzo Attuale", f"${prezzo_attuale:,.2f}")
    col2.metric("Variazione Periodo", f"${variazione:,.2f}", f"{variazione_pct:+.2f}%")
    col3.metric("Massimo toccato", f"${df['High'].max():,.2f}")
    col4.metric("Ultimo aggiornamento", ora_aggiornamento)

    st.markdown("---")

    # --- GRAFICO PLOTLY INTERATTIVO ---
    fig = go.Figure()

    # Grafico a candele (Candlestick) o a linea
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Close'], 
        mode='lines',
        name='Prezzo',
        line=dict(color='#00A67E', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 166, 126, 0.1)'
    ))

    fig.update_layout(
        title=f"Andamento in tempo reale per {scelta}",
        xaxis_title="Orario / Data",
        yaxis_title="Prezzo (USD)",
        template="plotly_white",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Mostra gli ultimi dati scaricati dall'API
    with st.expander("👀 Vedi le ultime 5 righe ricevute direttamente dall'API"):
        st.dataframe(df.tail(5))

else:
    st.error("Impossibile recuperare i dati al momento. Riprova tra poco!")