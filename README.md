# hashmon

`hashmon` is a fast, terminal-based TUI monitor for watching hashrate and worker stats from multiple mining pools.

It supports both [FastPool](https://fastpool.xyz)'s **XLA** and **SALV** endpoints, with per-worker hashrate tracking, best-performer highlighting, and a clean live-updating display.

---

## 🔧 Features

- Real-time stats from XLA and SALV pools  
- Bold highlighting for top-performing worker  
- Countdown bar between refreshes  
- Clean TUI with minimal dependencies  
- Configurable via `.env` file or environment variables  

---

## 🚀 Installation

1. Clone the repo or copy the script:

    ```bash
    git clone https://github.com/yourusername/hashmon.git
    cd hashmon
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    Or manually:

    ```bash
    pip install rich python-dotenv
    ```

---

## ⚙️ Setup

Create a `.env` file in the project root with your wallet addresses:

```env
HASHMON_XLA_ADDRESS=your_xla_wallet_here
HASHMON_SALV_ADDRESS=your_salv_wallet_here
```

You can also export them manually:

```bash
export HASHMON_XLA_ADDRESS=your_xla_wallet_here
export HASHMON_SALV_ADDRESS=your_salv_wallet_here
```

---

## 🧱 Running the monitor

```bash
python hashmon.py
```

You’ll see a live terminal dashboard with worker breakdowns for each pool.  
Press **`q`** to quit gracefully.

---

## 📸 Screenshot

*(insert screenshot here)*

---

## 🗂 .gitignore and structure

This repo ignores:
- Python cache files
- Virtual environments
- Logs
- `.env` secrets

---

## 📄 License

MIT — do what you want with it. Contributions welcome.

---

## 🛠️ Coming Soon?

- Configurable refresh time  
- Worker history / trend lines  
- Multi-address support
