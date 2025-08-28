![Banner](<img width="1920" height="960" alt="image" src="https://github.com/user-attachments/assets/0d36a27f-b440-47f7-b9ce-ae3c553d942c" />)


# 🐍 Pokémon Concurrency Benchmark

This project compares different **Python concurrency methods** to determine the most efficient way to download and process a dataset of **151 Pokémon names and sprites** from GitHub.  

We evaluated:  
- ⚡ **Asyncio**  
- 🧩 **Multiprocessing**  
- 🧵 **Threading**  
- 🐢 **Sequential Execution**  

---

## 🎯 Objective
- Find the fastest method for downloading and processing Pokémon data.  
- Compare consistency across multiple runs.  
- Test a **dataloader** for memory-efficient loading.  

---

## 📊 Results

### Concurrency (10 runs avg.)
| Method         | Avg. Time (s) | Std. Dev. (s) |
|----------------|---------------|---------------|
| **Asyncio**    | ~1.3          | Low           |
| Multiprocessing| ~3.1          | Low           |
| Threading      | ~14.0         | ~0.3          |
| Sequential     | ~13.7         | ~0.5          |

---

### Dataloader (1 run)
| Method          | Data Loading (s) | Total Time (s) | Relative Speed* |
|-----------------|------------------|----------------|-----------------|
| **Asyncio**     | 1.77             | 7.08           | 🚀 Baseline (1x) |
| Multiprocessing | 14.45            | 17.69          | ~2.5x slower    |
| Threading       | 15.65            | 18.78          | ~2.6x slower    |
| Sequential      | 90.54            | 167.59         | 🐌 ~23.6x slower |

\*Compared to **Asyncio**.

---

## ✅ Conclusions
- **Asyncio** is the fastest and most consistent.  
- **Multiprocessing** is a strong alternative, especially for CPU-heavy tasks.  
- **Threading** adds little benefit in this case.  
- **Sequential** is by far the least efficient.  

---

## 👤 Author
**Santiago González-Granada**  
_EAFIT – Big Data (Grandes Volúmenes de Datos)_  
