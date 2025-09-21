#Flipkart Women’s Dress Dataset Analysis  

## 📌 Project Overview  
This project analyzes the **Women’s Dresses category** from Flipkart. The dataset was collected using web scraping techniques and contains information on product pricing, discounts, ratings, reviews, and brand/category trends. The goal was to study **pricing patterns, discount strategies, and customer ratings** across different brands and categories.  

## ⚙️ Tools & Libraries Used  
- **Python** – Data processing & analysis  
- **Selenium** – Automated navigation & handling JavaScript-based loading  
- **BeautifulSoup** – HTML parsing  
- **Pandas** – Data cleaning, transformation & storage  
- **Matplotlib/Seaborn** – Data visualization  

## 📊 Dataset Information  
- **Source:** Flipkart (Women’s Dresses section)  
- **Size:** ~1000 products scraped  
- **Features Collected:**  
  - Product Name  
  - Brand  
  - Category Type (A-line, Bodycon, Maxi, Midi, Shift, Gown, Kaftan, etc.)  
  - Maximum Retail Price (MRP)  
  - Discounted Price / Sale Price  
  - Rating  
  - Number of Reviews  
  - Product URL  

## 🧹 Data Cleaning & Preparation  
- Removed duplicates.  
- Handled missing values:  
  - Prices missing → dropped.  
  - Ratings/Reviews missing → filled with `0`.  
  - Unknown categories → labeled as `"Unknown"`.  
- Standardized brand names using regex + manual mapping.  
- Converted prices, discounts, and ratings into numeric formats.  

## 🔑 Key Findings  
- **Average MRP:** ₹2033 | **Avg Discounted Price:** ₹534.  
- Most dresses priced between **₹300–₹600** (right-skewed distribution).  
- **Top brand:** Tokyo Talkies (107 products).  
- Smaller brands (Tilton, Jkmisti, Kamayra) rely on **deep discounts (85–90%)**.  
- **Maxi & Midi dresses** show premium pricing with luxury outliers, while **Shift & Kaftan** remain affordable.  
- Discounts (60–90%) are common, but **ratings (~3.5–4.0) remain steady**, showing no link between discount % and customer satisfaction.  

## ⚠️ Challenges & Solutions  
- **Dynamic Page Loading:** Used Selenium WebDriverWait.  
- **Inconsistent Brand Names:** Applied regex cleaning + manual mapping.  
- **Outliers in Prices:** Kept them but explained impact.  
- **Scraping Blocks:** Added retry logic & sleep intervals.  

## ✅ Conclusion  
- Majority of dresses are **budget-friendly (₹300–₹600)**.  
- Premium dresses exist but form a smaller share.  
- **Heavy discounting is common** among lesser-known brands.  
- Customer ratings depend more on **quality, design & reputation**, not discounts.  

## 📂 Files in this Repository  
- `women_dresses_raw.csv` – Raw dataset collected from Flipkart.  
- `women_dresses_cleaned.csv` – Cleaned dataset after preprocessing.  
- `analysis.ipynb` – Notebook with exploratory analysis.  
- `visualization.ipynb` – Notebook with visualizations.  
- `clean_data.ipynb` – Notebook for data cleaning.  
- `scrape_flipkart.py` – Script for scraping data.  
- `histogram_prices.png` – Histogram of discounted prices.  
- `bar_top_discount.png` – Top 10 brands by average discount.  
- `boxplot_prices.png` – Price distribution across categories.  
- `scatter_rating_discount.png` – Ratings vs discounts scatter plot.  
- `Flipkart_Womens_Dress_Report.pdf` – Final summarized report.  

---

## ✨ Author  
**Amrutha V.K**  
📧 Email: [amruthavko7@gmail.com](mailto:amruthavko7@gmail.com)  
🔗 LinkedIn: [linkedin.com/in/amruthavk](https://www.linkedin.com/in/amruthavk)  
