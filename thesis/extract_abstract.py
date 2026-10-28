from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

links = [
"https://link.springer.com/article/10.1007/s00287-019-01185-y",
    "https://link.springer.com/chapter/10.1007/978-3-319-69179-4_44",
    "https://link.springer.com/article/10.1007/s11390-015-1576-4",
    "https://link.springer.com/chapter/10.1007/978-3-032-30008-9_14",
    "https://link.springer.com/chapter/10.1007/978-3-031-88759-8_4",
    "https://link.springer.com/article/10.1007/s11042-023-15974-x",
    "https://link.springer.com/article/10.1007/s11042-023-16592-3",
    "https://link.springer.com/chapter/10.1007/978-981-99-1435-7_48",
    "https://link.springer.com/chapter/10.1007/978-981-96-9275-0_34",
    "https://link.springer.com/chapter/10.1007/978-981-19-9483-8_28",
    "https://link.springer.com/chapter/10.1007/978-981-97-2031-6_3",
    "https://link.springer.com/chapter/10.1007/978-981-33-4046-6_13",
    "https://link.springer.com/chapter/10.1007/978-981-96-8898-2_22",
    "https://link.springer.com/chapter/10.1007/978-981-15-8221-9_63",
    "https://link.springer.com/article/10.1007/s00521-019-04592-0",
    "https://link.springer.com/chapter/10.1007/978-3-030-68449-5_2",
    "https://link.springer.com/chapter/10.1007/978-981-15-5243-4_31",
    "https://link.springer.com/chapter/10.1007/978-981-15-5619-7_23",
    "https://link.springer.com/chapter/10.1007/978-3-319-93037-4_9",
    "https://link.springer.com/article/10.1007/s41870-022-01012-w",
    "https://link.springer.com/chapter/10.1007/978-3-030-36718-3_35",
    "https://link.springer.com/article/10.1007/s12559-022-10102-7",
    "https://link.springer.com/chapter/10.1007/978-3-030-59413-8_9",
    "https://link.springer.com/chapter/10.1007/978-3-030-28577-7_8",
    "https://link.springer.com/article/10.1007/s10664-016-9430-z",
    "https://link.springer.com/chapter/10.1007/978-3-319-56608-5_34",
    "https://link.springer.com/chapter/10.1007/978-3-319-42089-9_40",
    "https://link.springer.com/chapter/10.1007/978-3-031-36597-3_12",
    "https://link.springer.com/article/10.1007/s10664-021-10058-6"]

# Setup Selenium pakai Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless') # Jalan di background
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# Buka browser otomatis
print("Menyiapkan Chrome WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

nama_file = "hasil_abstrak_springer_selenium.csv"

with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["link", "abstract"])
    
    for link in links:
        print(f"Membuka: {link}")
        driver.get(link)
        
        # Kasih waktu 3 detik biar JavaScript Springer selesai ngerender halaman
        time.sleep(3)
        
        try:
            # Langsung sikat pakai XPath lu
            elements = driver.find_elements(By.XPATH, '//*[@id="Abs1-content"]/p')
            
            # Kalau kosong, coba fallback (biasanya buat halaman chapter buku)
            if not elements:
                elements = driver.find_elements(By.XPATH, '//*[@class="c-article-section__content"]/p')
            
            if elements:
                # Gabungin teks dari semua elemen <p> yang ketemu
                abstrak = ' '.join([el.text.strip() for el in elements])
            else:
                abstrak = "Abstrak tidak ditemukan di halaman ini."
                
        except Exception as e:
            abstrak = f"Error: {e}"
            
        print(f"Preview: {abstrak[:100]}...\n")
        writer.writerow([link, abstrak])

# Tutup browser kalau udah selesai
driver.quit()
print(f"Beres coy! Cek file '{nama_file}'. Cara ini anti badai JavaScript.")