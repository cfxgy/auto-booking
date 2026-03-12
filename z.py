from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import datetime

# ---------- 配置 ----------
VENUE_NO = "001"
FIELD_TYPE_NO = "13"
ORDER_PAGE = f"https://webvpn.zzuli.edu.cn/http/77726476706e69737468656265737421f3f05885692a72457201c7a99c406d3651/Views/Field/FieldOrder.html?VenueNo={VENUE_NO}&FieldTypeNo={FIELD_TYPE_NO}"

# ---------- Edge浏览器 ----------
edge_options = Options()
edge_options.add_argument("--start-maximized")

driver = webdriver.Edge(
    service=Service(EdgeChromiumDriverManager().install()),
    options=edge_options
)

# ---------- 打开 WebVPN 登录 ----------
driver.get("https://webvpn.zzuli.edu.cn/")
print("请登录 WebVPN，然后按回车继续...")
input()

# ---------- 打开预约页面 ----------
driver.get(ORDER_PAGE)
time.sleep(5)

# ---------- 等待每天 6:00 ----------

while True:
    now = datetime.datetime.now()
    if now.hour == 6 and now.minute >= 0:  # 6:00 开始
        print("开始抢场...")
        break
    else:
        remain = (datetime.datetime(now.year, now.month, now.day, 6, 0) - now).seconds
        print(f"等待 {remain} 秒到 6:00...")
        time.sleep(min(60, remain))  # 每分钟检查一次

# ---------- 自动抢场 ----------
success = False
while not success:
    try:
        driver.refresh()
        time.sleep(2)

        # 找可预约场地
        slots = driver.find_elements(By.CLASS_NAME, "kyd")  # kyd = 可预订
        if len(slots) > 0:
            slots[0].click()
            time.sleep(1)
            submit_btn = driver.find_element(By.ID, "atj")
            submit_btn.click()
            print("抢场提交成功！")
            success = True
        else:
            print("暂无可预约，继续刷新...")
            time.sleep(1)  # 每秒刷新一次

    except Exception as e:
        print("发生错误:", e)
        time.sleep(1)